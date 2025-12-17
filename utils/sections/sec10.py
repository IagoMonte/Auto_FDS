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


def getInfo(OtherInfo):
    other_info_sorted = otherInfoSort(OtherInfo)

    if other_info_sorted['Reatividade'][0].strip():
        reactivity = other_info_sorted['Reatividade'][0]

    if other_info_sorted['Produtos perigosos da decomposição'][0].strip():
        hazardous_decomposition_products = other_info_sorted['Produtos perigosos da decomposição'][0]

    if other_info_sorted['Possibilidade de reações perigosas'][0].strip():
        possibility_of_dangerous_reactions = other_info_sorted['Possibilidade de reações perigosas'][0]

    if other_info_sorted['Condições a serem evitadas'][0].strip():
        conditions_to_avoid = other_info_sorted['Condições a serem evitadas'][0]

    if other_info_sorted['Materiais incompatíveis'][0].strip():
        incompatible_materials = other_info_sorted['Materiais incompatíveis'][0]
