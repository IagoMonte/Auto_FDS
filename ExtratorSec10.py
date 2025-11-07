#           ▄▄▄▄▄▄▄▄▄          
#        ▄▄▀         ▀▄▄       
#      ▄▀               ▀▄     
#    ▄▀                   ▀▄   
#  ▐▀     ▄▄         ▄▄     ▀▌ 
#  ▐    ▐▀  ▀▌     ▐▀  ▀▌    ▌ 
# ▐▀   ▐▀    ▀▌   ▐▀    ▀▌   ▀▌
# ▐    ▐      ▌   ▐      ▌    ▌
# ▐▄                         ▄▌
#  ▐      _____________      ▌ 
#  ▐▄         ▐   ▌          ▌ █  ███   ████   ████  ████  █████      
#   ▀▄        ▐▄ ▄▌        ▄▀  █ █   █ █      █    █ █   █   █        
#     ▀▄       ▀▀▀       ▄▀    █ █████ █   ██ █    █ █   █   █        
#       ▀▄▄           ▄▄▀      █ █   █ █    █ █    █ █   █   █        
#          ▀▄▄▄▄▄▄▄▄▄▀         █ █   █  ████   ████  ████    █        
#                                                 


import re
import unicodedata
from typing import Dict, List

class ExtractorSecoesQuimicasCorrigido:
    """
    Extrator corrigido para seções de estabilidade e reatividade química.
    Baseado na análise dos resultados esperados vs encontrados.
    """
    
    def __init__(self):
        pass
    
    @staticmethod
    def normalizar(txt: str) -> str:
        """Normaliza texto removendo acentos e convertendo para minúsculas."""
        if not txt:
            return ""
        txt_lower = txt.lower()
        txt_norm = unicodedata.normalize("NFKD", txt_lower)
        return "".join(c for c in txt_norm if not unicodedata.combining(c))
    
    def _limpar_ruidos_especificos(self, texto: str) -> str:
        """Remove ruídos específicos identificados nos exemplos."""
        if not texto:
            return ""
        
        # Remove prefixos truncados como "ção:"
        texto = re.sub(r'^[^:]*?ção:\s*', '', texto.strip())
        
        # Remove referências específicas
        texto = re.sub(r'ver\s+ZVG-Nr\.\s+\d+.*$', '', texto, flags=re.IGNORECASE)
        texto = re.sub(r'Referência:\s*\d+.*$', '', texto, flags=re.IGNORECASE | re.MULTILINE)
        texto = re.sub(r'Fonte:\s*[\d\s]+$', '', texto, flags=re.IGNORECASE | re.MULTILINE)
        #Fonte: 
        # Remove seções de caracterização que não são relevantes
        texto = re.sub(r'CARACTERIZAÇÃO QUÍMICA:.*?(?=\n[A-Z]|\n\n|$)', '', texto, flags=re.IGNORECASE | re.DOTALL)
        texto = re.sub(r'PROPRIEDADES:.*?(?=\n[A-Z]|\n\n|$)', '', texto, flags=re.IGNORECASE | re.DOTALL)
        texto = re.sub(r'PONTO DE EBULIÇÃO.*?(?=\n[A-Z]|\n\n|$)', '', texto, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove títulos soltos
        texto = re.sub(r'^\s*REAÇÕES PERIGOSAS\s*$', '', texto, flags=re.IGNORECASE | re.MULTILINE)
        texto = re.sub(r'Decomposição térmica:.*?(?=\n|$)', '', texto, flags=re.IGNORECASE)
        
        # Remove linhas com apenas palavras soltas
        texto = re.sub(r'^\s*fortes\s*$', '', texto, flags=re.MULTILINE)
        texto = re.sub(r'^\s*-\s*$', '', texto, flags=re.MULTILINE)
        
        # Remove múltiplas quebras de linha
        texto = re.sub(r'\n\s*\n', '\n', texto)
        
        return texto.strip()
    
    def _extrair_materiais_incompativeis(self, texto: str) -> List[str]:
        """Extrai especificamente materiais incompatíveis."""
        resultados = []
        
        # Padrão 1: "Incompatível com..."
        pattern1 = r'incompativel\s+com\s+([^.]+(?:\.|$))'
        matches1 = re.findall(pattern1, self.normalizar(texto), re.IGNORECASE | re.DOTALL)
        
        # Padrão 2: Lista após "A substância pode reagir perigosamente com:"
        pattern2 = r'a\s+substancia\s+pode\s+reagir\s+perigosamente\s+com\s*:?\s*([^.]+(?:\.|$))'
        matches2 = re.findall(pattern2, self.normalizar(texto), re.IGNORECASE | re.DOTALL)
        
        # Padrão 3: "Materiais incompatíveis:"
        pattern3 = r'materiais?\s+incompativeis\s*:?\s*([^.]+(?:\.|$))'
        matches3 = re.findall(pattern3, self.normalizar(texto), re.IGNORECASE | re.DOTALL)
        
        for matches in [matches1, matches2, matches3]:
            for match in matches:
                limpo = self._limpar_ruidos_especificos(match)
                if limpo and len(limpo) > 5:
                    resultados.append(limpo)
        
        return resultados
    
    def _extrair_reacoes_perigosas(self, texto: str) -> List[str]:
        """Extrai reações perigosas com melhor precisão."""
        resultados = []
        
        # Busca por blocos que começam com "Reações" e continuam até próxima seção
        linhas = texto.split('\n')
        capturando = False
        bloco_atual = []
        
        for linha in linhas:
            linha_norm = self.normalizar(linha.strip())
            
            # Inicia captura
            if re.search(r'reac[oõ]es\s+(?:quimicas\s+)?perigosas', linha_norm):
                capturando = True
                bloco_atual = [linha.strip()]
                continue
            
            # Para captura em nova seção
            elif capturando and re.search(r'^(?:materiais?\s+incompativeis|condic[oõ]es\s+a\s+evitar|caracterizac[aã]o\s+quimica|propriedades)', linha_norm):
                if bloco_atual:
                    conteudo = '\n'.join(bloco_atual)
                    limpo = self._limpar_ruidos_especificos(conteudo)
                    if limpo and len(limpo) > 20:
                        resultados.append(limpo)
                capturando = False
                bloco_atual = []
            
            # Continua captura
            elif capturando:
                if linha.strip():
                    bloco_atual.append(linha.strip())
        
        # Processa último bloco se necessário
        if capturando and bloco_atual:
            conteudo = '\n'.join(bloco_atual)
            limpo = self._limpar_ruidos_especificos(conteudo)
            if limpo and len(limpo) > 20:
                resultados.append(limpo)
        
        return resultados
    
    def _extrair_produtos_decomposicao(self, texto: str) -> List[str]:
        """Extrai produtos de decomposição."""
        resultados = []
        
        # Busca por "Produtos de decomposição:" seguido de lista
        pattern = r'produtos?\s+de\s+decomposic[aã]o\s*:?\s*([^.]*(?:amonia|acido|oxigenio|cloro|hidrogenio)[^.]*\.?)'
        matches = re.findall(pattern, self.normalizar(texto), re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            limpo = self._limpar_ruidos_especificos(match)
            if limpo and len(limpo) > 5:
                resultados.append(limpo)
        
        return resultados
    
    def _extrair_condicoes_evitadas(self, texto: str) -> List[str]:
        """Extrai condições a serem evitadas."""
        resultados = []
        
        # Padrão específico encontrado nos exemplos
        pattern = r'houver\s+uma\s+fonte\s+de\s+ignic[aã]o\s+presente\s*[^.]*'
        matches = re.findall(pattern, self.normalizar(texto), re.IGNORECASE)
        
        for match in matches:
            limpo = self._limpar_ruidos_especificos(match)
            if limpo and len(limpo) > 10:
                resultados.append(limpo)
        
        return resultados
    
    def _extrair_reatividade(self, texto: str) -> List[str]:
        """Extrai informações de reatividade."""
        resultados = []
        
        # Busca por "Reatividade com materiais comuns"
        pattern = r'reatividade\s+com\s+materiais\s+comuns\s*:?\s*([^.]+(?:\.|$))'
        matches = re.findall(pattern, self.normalizar(texto), re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            limpo = self._limpar_ruidos_especificos(match)
            if limpo and len(limpo) > 20:
                resultados.append(limpo)
        
        return resultados
    
    def extrair_todas_secoes(self, texto: str) -> Dict[str, List[str]]:
        """Método principal otimizado."""
        if not texto or not texto.strip():
            return {
                "Reatividade": [" "],
                "Produtos perigosos da decomposição": [" "],
                "Possibilidade de reações perigosas": [" "],
                "Condições a serem evitadas": [" "],
                "Materiais incompatíveis": [" "]
            }
        
        resultados = {
            "Reatividade": self._extrair_reatividade(texto),
            "Produtos perigosos da decomposição": self._extrair_produtos_decomposicao(texto),
            "Possibilidade de reações perigosas": self._extrair_reacoes_perigosas(texto),
            "Condições a serem evitadas": self._extrair_condicoes_evitadas(texto),
            "Materiais incompatíveis": self._extrair_materiais_incompativeis(texto)
        }
        
        # Limpeza final
        for secao, conteudos in resultados.items():
            if not conteudos or all(not c.strip() for c in conteudos):
                resultados[secao] = [" "]
            else:
                # Remove duplicatas preservando ordem
                conteudos_unicos = []
                for conteudo in conteudos:
                    if conteudo.strip() and conteudo.strip() not in conteudos_unicos:
                        conteudos_unicos.append(conteudo.strip())
                resultados[secao] = conteudos_unicos if conteudos_unicos else [" "]
        
        return resultados


def processar_textos_quimicos(textos: List[str], arquivo_saida: str = "saida_secoes_corrigida.txt") -> None:
    """Processa textos químicos com o extrator corrigido."""
    extrator = ExtractorSecoesQuimicasCorrigido()
    
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for idx, texto in enumerate(textos, 1):
            f.write(f"------- Exemplo {idx} -------\n\n")
            dados = extrator.extrair_todas_secoes(texto)
            
            for secao, conteudos in dados.items():
                f.write(f"{secao}:\n")
                for conteudo in conteudos:
                    if conteudo == " ":
                        f.write(f"  {conteudo}\n")
                    else:
                        # Indenta cada linha do conteúdo
                        linhas_conteudo = conteudo.split('\n')
                        for linha in linhas_conteudo:
                            if linha.strip():
                                f.write(f"  {linha.strip()}\n")
                f.write("\n")
            f.write("\n")

def otherInfoSort(Produto):
    extrator = ExtractorSecoesQuimicasCorrigido()
    dados =extrator.extrair_todas_secoes(Produto) 
    return dados

# Ácido_Cloridrico='''CARACTERIZAÇÃO QUÍMICA  
# Misturável com água. Características de uma solução de ácido clorídrico a 36%: altamente corrosivo. Reage com o ar formando fumos ácidos corrosivos mais pesados que o ar. Ácido forte que reage vigorosamente com bases. Metais não nobres são dissolvidos com formação de hidrogênio. Óxidos também são dissolvidos. Carbonatos são convertidos com formação de dióxido de carbono. Na presença de agentes oxidantes, forma-se cloro. Resultam riscos à saúde agudos ou crônicos decorrentes da substância. (ver: capítulo REGULAMENTAÇÕES).  
# Reações perigosas com outros produtos químicos: reage violentamente com oxidantes, liberando gás cloro.  
# REAÇÕES PERIGOSAS  
# Reações químicas perigosas  
# Risco de explosão em contato com: potássio, sódio, permanganato de potássio (raramente), ácido sulfúrico concentrado.  
# A substância pode reagir perigosamente com: alumínio, aminas, flúor, soda cáustica concentrada, agentes oxidantes, césio, carbetos; carbeto de cálcio; hidreto de cálcio; formaldeído; sulfeto de cobre; siliceto de lítio; metais; hidreto de sódio; hipoclorito de sódio e suas soluções; solução de natrão e alvejante; carbeto de rubídio; silanos; dióxido de silício; éter vinil metílico; zinco
# '''
# Ácido_sulfurico='''CARACTERIZAÇÃO QUÍMICA Substância não inflamável. Ligeiramente viscosa, fortemente higroscópica. Miscível com água. A solução aquosa reage de forma ácida. Não volátil. Age como agente oxidante com aumento de temperatura. O ácido sulfúrico concentrado pode destruir substâncias orgânicas por desidratação com carbonização. Resultam riscos agudos ou crônicos à saúde decorrentes da substância. (ver: capítulo REGULAMENTAÇÕES).  
# PROPRIEDADES incolor, inodora  
# Reações perigosas com outros produtos químicos Reage violentamente com materiais combustíveis, redutores, bases, produtos orgânicos, cloratos, carbetos, fulminatos, picratos e metais.  
# Reatividade com materiais comuns Extremamente perigoso em contato com muitos materiais, particularmente metais e combustíveis; o ácido diluído reage com a maioria dos metais, liberando hidrogênio, que pode formar mistura explosiva com o ar em áreas confinadas.  
# REAÇÕES PERIGOSAS Temperatura de decomposição: 340 °C Reações químicas perigosas Risco de explosão em contato com: metais alcalinos/ alcalino-terrosos substâncias combustíveis hidróxido de potássio soda cáustica hidróxido de sódio peróxido de hidrogênio acetaldeído; acetoncianidrina; óxidos alcalinos (raros); alquilnitratos (raros); solução de amônia; sulfato férrico de amônio dodecaidratado (raro); peróxido de benzaldeído-p-bromofenilhidrazone; álcool benzílico (calor); bromatos; carbetos; cloratos; cloritos; ácido clorossulfônico; ciclopentadieno; dietilamina; 1,5-dinitronaftaleno; hidróxidos alcalino-terrosos (raros); ácido fluorídrico; fulminatos; tert-butoxido de potássio; permanganatos; peróxido de metil etil cetona; tetrahidroborato de sódio; óxido de sódio (raro); nitramida; nitratos (raros); o-nitroanilina (calor), nitrometano; N-nitrometilamina; nitrotolueno; percloratos; ácido perclórico (raro); ácido permangânico (raro); picratos; 2-propen-1-ol; 2-propin-1-ol; nitreto de mercúrio; ácido nítrico + substâncias orgânicas; trinitrotolueno A substância polimeriza em contato com: 1-cloro-2,3-epoxipropano A substância pode reagir perigosamente com: alumínio substâncias orgânicas agentes redutores ácido nítrico acetonitrila; acroleína/oclusão; acrilonitrila; alumínio; aminoetanol; amônia concentrada; anilina; pentafluoreto de bromo; hidreto de cálcio; p-cloronitrobenzeno + trióxido de enxofre (calor); trifluoreto de cloro; cloreto de hidrogênio/ácido sulfúrico concentrado; 2-ciano-2-propanol; oxima de ciclopentanona (calor); 1,4-diazidobenzeno; éter dietílico; p-dimetilaminobenzaldeído; óxidos alcalino-terrosos; ácido acético; anidrido acético/inclusão; cianidrina do etileno; etilenodiamina; síntese; calor; cobre; siliceto de lítio; solventes altamente inflamáveis; metais/ácido diluído; 4-metilpiridina; carbonato de sódio; tiocianato de sódio; p-nitroacetanilida (calor); p-nitroanilina (calor); sulfato de p-nitroanilina (calor); ácido p-nitroanilinasulfônico (calor); ácido m-nitrobenzenossulfônico; fósforo, vermelho e branco; trióxido de fósforo; óxido de propeno; mercúrio; prata; tetrametilbenzeno; 1,2,4,5-tetrazina; água/ácido sulfúrico concentrado; açúcar Para oleum (ácido sulfúrico fumegante) ver ZVG-Nr. 520023
# '''
# Cloreto_de_sódio='''EXPLOSIVIDADE DE PÓ: não. Sem risco de explosão de pó. Fonte: 99999  
# REAÇÕES PERIGOSAS: Reações químicas perigosas. Risco de explosão em contato com: metais alcalinos (raro). A substância pode reagir perigosamente com: lítio -> sódio (O lítio em chamas pode liberar o sódio mais reativo do cloreto de sódio).  
# CARACTERIZAÇÃO QUÍMICA: Substância não combustível. Solúvel livremente em água.  
# PROPRIEDADES: cristalino, incolor, inodoro
# '''
# Hipoclorito_de_sódio='''CARACTERIZAÇÃO QUÍMICA  
# O hipoclorito de sódio é durável apenas em solução aquosa. Substância não inflamável. Miscível com água. A solução aquosa reage fortemente de maneira alcalina. O hexahidrato precipita de soluções concentradas ao ser resfriado a -10 °C. A substância apresenta riscos à saúde agudos ou crônicos. A substância é perigosa para o meio aquático. (ver: capítulo REGULAMENTAÇÕES).  
# REAÇÕES PERIGOSAS COM OUTROS PRODUTOS QUÍMICOS  
# Incompatível com aminas, amônia, substâncias orgânicas, agentes oxidantes, agentes redutores, ácido fórmico, metanol, benzaldeído, arsênio, ureia e cianetos.  
# REAÇÕES PERIGOSAS  
# Decomposição térmica: decomposição ao ser aquecido. Produtos de decomposição: oxigênio, cloro, cloreto de hidrogênio, dióxido de cloro.  
# Reações químicas perigosas: risco de explosão em contato com: aminas, amônia, substâncias orgânicas, agentes redutores, ácido fórmico/calor (raro), acetato de amônio, sais de amônio/ácido (raro), aziridina, benzaldeído, anidrido acético, furfural, ureia, metanol, ácido oxálico/sólidos, agentes oxidantes/sólidos, fenilacetonitrila/sólido, fricção/calor/sólido.  
# A substância pode reagir perigosamente com: peróxido de hidrogênio, arsênio, cianetos → cianeto de cloro, etanodiol/armazenamento em solução → oxigênio, luz (decomposição) → oxigênio, agentes oxidantes/solução, permanganatos, ácido nítrico → cloro, gases nitrosos, ácido clorídrico/solução → cloro, ácidos/soluções → cloro. Metais pesados e seus sais catalisam a decomposição.
# '''

# Ureia_Carbamida='''
# EXPLOSIVIDADE DO PÓ  
# Existe risco de explosão de poeira se as seguintes condições forem atendidas:  
# - A substância estiver em forma muito finamente distribuída (pó, poeira).  
# - A substância for suspensa em quantidade suficiente no ar.  
# - Houver uma fonte de ignição presente (chama, faísca, descarga eletrostática, etc.).  
# Fonte: 01211 06806

# REAÇÕES PERIGOSAS  
# Temperatura de decomposição: > 132 °C  
# Produtos de decomposição:  
# - Amônia  
# - Ácido isociânico  

# Reações químicas perigosas  
# Risco de explosão em contato com:  
# - Cloro  
# - Nitrato de amônio  
# - Hipoclorito de cálcio  
# - Agentes de cloração  
# - Cloreto de cromila  
# - Hexanitroetano  
# - Hipoclorito de sódio  
# - Nitrito de sódio  
# - Perclorato de sódio  
# - Perclorato de nitrosila  
# - Pentacloreto de fósforo  

# A substância pode reagir perigosamente com:  
# - Flúor  
# - Agentes oxidantes fortes  
# - Peróxido de hidrogênio  
# - Cloritos alcalinos  
# - Cromatos alcalinos  
# - Alcalis  
# - Nitratos alcalinos  
# - Percloratos  
# - Tetracloreto de titânio

# PONTO DE EBULIÇÃO  
# A substância se decompõe quando aquecida (ver temperatura de decomposição).  
# Referência: 01211

# CARACTERIZAÇÃO QUÍMICA  
# Substância não inflamável.  
# Acima de 130 °C, a ureia se decompõe em amônia e ácido isociânico.  
# Solúvel livremente em água. Higroscópica.
# '''

# textos = [Ácido_Cloridrico, Ácido_sulfurico, Cloreto_de_sódio, Hipoclorito_de_sódio, Ureia_Carbamida]
# processar_textos_quimicos(textos)