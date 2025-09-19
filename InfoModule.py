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
from bs4 import BeautifulSoup
from main import getData, translate
from Header import HeaderGen
from pictograms import class_to_pictograms
from docx import Document
from Section import mkSec1,mkSec2,mkSec3,mkSec4,mkSec5,mkSec6,mkSec7,mkSec8,mkSec9

def extract_property_value(text, prop):
    values = []
    
    if prop == "melting_point":
        matches = re.findall(r"Melting point:\s*([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?", text, flags=re.I)
        for val, purity in matches:
            try:
                val_num = float(val.replace(",", "."))
            except:
                continue
            values.append((val_num, purity if purity else None))
        if not values:
            return "Não disponível"
        # Priorizar pureza 100%, senão maior pureza, senão menor valor
        values.sort(key=lambda x: (-(int(x[1]) if x[1] else 0), x[0]))
        chosen = values[0]
        return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")
    
    if prop == "boiling_point":
        matches = re.findall(r"Boiling Point:\s*(?:ca\.\s*)?([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?", text, flags=re.I)
        for val, purity in matches:
            try:
                val_num = float(val.replace(",", "."))
            except:
                continue
            values.append((val_num, purity if purity else None))
        if not values:
            return "Não disponível"
        # Priorizar pureza 100%, senão maior pureza, senão maior valor
        values.sort(key=lambda x: (-(int(x[1]) if x[1] else 0), -x[0]))
        chosen = values[0]
        return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")
    
    return "Não disponível"

def extrair_dados_dinamico(entradas):
    dados = {
        "physical_state": "Não disponível",
        "color": "Não disponível",
        "odor": "Não disponível",
        "melting_point": "Não disponível",
        "boiling_point": "Não disponível",
        "flammability": "Não disponível",
        "explosive_limit": "Não disponível",
        "flash_point": "Não disponível",
        "auto_ignition_temperature": "Não disponível",
        "decomposition_temperature": "Não disponível",
        "pH": "Não disponível",
        "kinematic_viscosity": "Não disponível",
        "water_solubility": "Não disponível",
        "partition_coefficient": "Não disponível",
        "vapor_pressure": "Não disponível",
        "relative_density": "Não disponível",
        "relative_vapor_density": "Não disponível",
        "particle_characteristics": "Não disponível",
        "OtherInfo": ""
    }

    # --- Normaliza entradas (html, listas, dicts, números soltos) ---
    textos = []
    for e in entradas:
        if isinstance(e, dict) and "text" in e:
            textos.append(e["text"])
        elif isinstance(e, str):  # pode ser HTML
            soup = BeautifulSoup(e, "html.parser")
            textos.append(soup.get_text(" "))
        elif isinstance(e, list):
            for sub in e:
                if isinstance(sub, str):
                    textos.append(sub)
                elif isinstance(sub, list):
                    textos.extend(sub)
                elif isinstance(sub, dict) and "text" in sub:
                    textos.append(sub["text"])
        elif isinstance(e, (int, float)):
            textos.append(str(e))

    texto_total = " ".join(textos)

    # --- Regras dinâmicas: campo → regex ---
    regras = {
    "relative_density": r"(?:Density|Densidade).*?([\d\.,]+ ?g/(?:cm³|ml)|[\d\.,]+ ?a ?\d* ?°C)",
    "vapor_pressure": r"(?:Vapou?r pressure|Press[aã]o do vapor).*?([\d\.,]+ ?(Pa|hPa|kPa|mmHg)|negligible.*?\([\w <>\.=]+\))",
    "water_solubility": r"(?:Solubility.*?water|Solubilidade na [aá]gua).*?(:?miscible|entirely mixable|[\d\.,]+ ?g/(?:l|100ml).*?)",
    "relative_vapor_density": r"(?:Relative vapou?r density|Densidade relativa do g[aá]s).*?([\d\.,]+)",
    "decomposition_temperature": r"(?:Decomposition temperature|Decomp[oó]e).*?([>\-]?\s*[\d\.,]+ ?°C)",
    "pH": r"(?:pH).*?([<>\d\.,]+ ?-? ?\d*\.?\d*)",
    "kinematic_viscosity": r"(?:Viscosity).*?([\d\.,]+ ?mPa\*?s|[\d\.,]+ ?cP)",
    "partition_coefficient": r"(?:partition|Kow|Pow).*?([-\d\.,]+)",
    "color": r"(colourless|colorless|incol[oó]r|amarelo|yellow|marrom|branco|white)",
    "odor": r"(odourless|odorless|inodoro|cheiro.*?|odor.*?)",  
    "physical_state": r"(liquid|solid|gas|powder|solution|líquido|sólido|gasoso|solução|aqueous)"
}

    # --- Melting/Boiling com tratamento especial ---
    dados["melting_point"] = extract_property_value(texto_total, "melting_point")
    dados["boiling_point"] = extract_property_value(texto_total, "boiling_point")

    # --- Aplicar regras para os demais ---
    for campo, padrao in regras.items():
        if dados[campo] != "Não disponível":
            continue  # já preenchido
        match = re.search(padrao, texto_total, flags=re.IGNORECASE)
        if match:
            dados[campo] = match.group(1).strip()

    # --- Detecta inflamabilidade de forma semântica ---
    if re.search(r"non-?combustible|não inflamável|not flammable", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Não inflamável"
    elif re.search(r"flammable|inflamável|combustible", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Inflamável"

    # --- Preenche OtherInfo com termos relevantes ---
    extras = []
    palavras_chave = ["viscous", "hygroscopic", "oxidizing", "ácido", "não volátil", "not volatile", "reacts", "decomposes"]
    for linha in textos:
        if any(x in linha.lower() for x in palavras_chave):
            extras.append(linha.strip())
    if extras:
        dados["OtherInfo"] = "\n".join(set(extras))

    return dados


cas = '7664-93-9' # Sulfurico
#cas = '7647-14-5' # Sal
#cas = '57-13-6'   # Ureia
#cas = '7681-52-9' # Hipo
#cas = '7647-01-0' # HCL

data = getData(cas)

ProductName = 'Não disponível'

#Product Name Processing
if data['cetesb'] != []:
    ProductName = data['cetesb'][0][1][0]
elif data['gestis']['IDENTIFICATION'] !='':
    text = data['gestis']['IDENTIFICATION'][0]['text']
    for marker in ["ZVG No:", "CAS No:", "EC No:"]:
        if marker in text:
            text = text.split(marker)[0].strip()
            break
    ProductName =translate(" ".join(text.split()[:2]))

    casGestis = re.search(r'\d{2,7}-\d{2}-\d', data['gestis']['IDENTIFICATION'][0]['text']).group(0)
    casICSC = re.search(r'\d{2,7}-\d{2}-\d', data['icsc']['b_list'][2].text).group(0)
    if casGestis != casICSC:
        data['icsc'] = []
elif data['icsc'] != []:
    ProductName = translate(data['icsc']['b_list'][0].text.split(",")[0].strip()) 
else:
    ProductName = input('Nome do produto')


# Uses Processing
Uses = ''
if Uses == '':
    Uses = 'Este produto químico é formulado para atender a diversas aplicações industriais e laboratoriais.'
if data['cetesb'] != []:
    Uses = data['cetesb'][1][3][0][4::]

#PROVIDERS INFO
ProviderInfo ='''
PORTUGAL QUÍMICA LTDA.

Endereço: Av. Marcelo Zanarotti, 465 - Distrito Industrial - Dumont/SP - Brasil - Cep: 14120-000
Telefone: +55 16 3844-0999
E-mail: portugal@portugalquimica.com.br
''' 
Emergency = 'AMBIPAR - 0800-117-2020'

#Section2 - Classification
Classfication='''Produto não perigoso'''
#gestis
if data['gestis']:
    text = data['gestis']['REGULATIONS'][0]['text']
    match = re.search(r'Classification\s+(.*?)\s+Signal Word', text, re.DOTALL)
    classificationGestis = match.group(1).strip() if match else ""
    classification_clean = re.sub(r'H\d{3}\s*', '\n', classificationGestis)
    lines = [line.strip().rstrip(';') + ';' for line in classification_clean.split('\n') if line.strip()]
    ClassficationGestis = "\n".join(lines)

    if ClassficationGestis != '':
        Classfication = translate(ClassficationGestis)
#cetesb
if data['cetesb'] != []:
    Classfication= data['cetesb'][3][0][0]
    text = Classfication.replace("Classificação de perigo", "").strip()
    parts = re.split(r'(?=(Toxicidade|Corrosão|Lesões|Perigoso|Corrosivo))', text)
    classifications = []
    buffer = ""
    for p in parts:
        if not p.strip():
            continue
        if p in ["Toxicidade", "Corrosão", "Lesões", "Perigoso", "Corrosivo"]:
            if buffer:
                classifications.append(buffer.strip())
            buffer = ''
        else:
            buffer += p
    if buffer:
        classifications.append(buffer.strip())
    classifications = [c.replace(",", " -") for c in classifications]
    Classfication = ";\n".join(classifications[:-1]) + "."

ClassSystem = '''Norma ABNT-NBR 14725-2023.\nSistema Globalmente Harmonizado para a Classificação e Rotulagem de Produtos Químicos, ONU.'''
OtherDangerous = '''Não são conhecidos outros perigos do produto.'''
PictoPath = class_to_pictograms(Classfication)
pictoWidth = 4 #inches
pictoHeight = 2 #inches

warningWord = 'Não disponível'

if data['gestis']:
    text = re.search(r'Signal Word\s*"?(\w+)"?', data['gestis']['REGULATIONS'][0]['text'])
    if text:
        text = text.group(1)
        warningWord = translate(text)

if data['cetesb']:
    text = re.search(r'Palavra de advertência(\w+)', data['cetesb'][3][2][0])
    if text:
        text = text.group(1)
        warningWord = text

warningPhrases = 'Não disponível'
if data['gestis']:
    h_phrases = re.split(r'H-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
    if len(h_phrases) > 2:
        phrases = re.findall(r'(H\d+:.*?\.)', h_phrases[1])
        formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
        if formatedPhrases:
            formatedPhrases = "\n".join(formatedPhrases)
            warningPhrases = translate(formatedPhrases)

if data['cetesb']:
    text = re.sub(r'^Frase\(s\) de perigo', '', data['cetesb'][3][3][0])
    phrases = re.findall(r'H\d+\s*-\s*[^H]+', text)
    formatedPhrases = [f.strip() + ";\n" for f in phrases]
    if formatedPhrases:
        warningPhrases = formatedPhrases

worryPhrases ='Não disponível'
if data['gestis']:
    p_phrases = re.split(r'P-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
    if len(h_phrases) > 2:
        phrases = re.findall(r'(P[\d\+]+:.*?\.)', p_phrases[1])
        formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
        if formatedPhrases:
            formatedPhrases = "\n".join(formatedPhrases)
            worryPhrases = translate(formatedPhrases)

if data['cetesb']:
    p_phrases = re.sub(r'^Frase\(s\) de precaução.*?\)', '', data['cetesb'][3][4][0])
    phrases = re.findall(r'(P[\d\+ ]+-.*?\.)', p_phrases)
    formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
    if formatedPhrases:
        worryPhrases = "\n".join(formatedPhrases)

#section 3
subOrMix = 'SUBSTÂNCIA'#Always
synonym = 'Não disponível'
if data['icsc']:
    synonym = ";".join(
        translate(content) 
        for i, content in enumerate(data['icsc']['td_list'][2].contents) 
        if i % 2 == 0
        )
if data['cetesb']:
    synonym = data['cetesb'][1][0][0][9::]
    
chemID = ProductName #Always
impure = 'Não apresenta impurezas que contribuam para o perigo.'#Always


#Section4
#first aid gestis
if data['gestis']:
    sec4Gestis = None
    try:
        raw_text = data['gestis']['OCCUPATIONAL HEALTH AND FIRST AID'][2]['text']
        start = raw_text.find("FIRST AID")
        if start == -1:
            start = 0

        candidates = [
            raw_text.find("Information for physicians", start),
            raw_text.find("Recommendations", start),
            raw_text.find("Annotation", start),
        ]
        ends = [i for i in candidates if i != -1]
        end = min(ends) if ends else len(raw_text)
        block = raw_text[start:end]


        header_re = re.compile(r"\b(Eyes|Skin|Respiratory tract|Swallowing)\b(?!:)")
        matches = list(header_re.finditer(block))


        mapping = {
            "Eyes": "eyes",
            "Skin": "skin",
            "Respiratory tract": "inhalation",
            "Swallowing": "intake",
        }
        result = {v: "" for v in mapping.values()}

        for i, m in enumerate(matches):
            header = m.group(1)
            start_content = m.end()
            end_content = matches[i + 1].start() if i + 1 < len(matches) else len(block)
            content = block[start_content:end_content].strip(" -:\n\t ").strip()
            result[mapping[header]] = content

        sec4Gestis = result
    except:
        pass

inhalation = ''
#gestis
if sec4Gestis:
    inhalation = translate(re.sub(r"\[.*?\]", "", sec4Gestis['inhalation']).strip())
#icsc
if data['icsc']:
    text = data['icsc']['td_list'][11].text
    clean_text = text.replace('\xa0', ' ')
    if clean_text != ' ':
        inhalation = translate(clean_text)
if inhalation == '':
    inhalation = '''Remova a vítima para um local ventilado e mantenha-a em repouso, numa posição que não dificulte a respiração. Caso a pessoa sinta indisposição, contate imediatamente um médico. Se possível, leve consigo o rótulo ou a embalagem da substancia.'''


skin = ''
#gestis
if sec4Gestis:
    skin = translate(re.sub(r"\[.*?\]", "", sec4Gestis['skin']).strip())
#icsc
if data['icsc']:
    text = data['icsc']['td_list'][14].text
    clean_text = text.replace('\xa0', ' ')
    if clean_text != ' ':
        skin = translate(clean_text)
if skin == '':
    skin = '''Lave imediatamente a pele exposta com quantidade suficiente de água para remoção do material. Retire as roupas ou acessórios contaminados. Em caso de contato menor com a pele, evite espalhar o produto em áreas não, atingidas. Consulte um médico. Leve este documento.'''

eyes = ''
#gestis
if sec4Gestis:
    eyes = translate(re.sub(r"\[.*?\]", "", sec4Gestis['eyes']).strip())
#icsc
if data['icsc']:
    text = data['icsc']['td_list'][17].text
    clean_text = text.replace('\xa0', ' ')
    if clean_text != ' ':
        eyes = translate(clean_text)
if eyes == '':
    eyes = '''Lave imediatamente os olhos com quantidade suficiente de água, mantendo as pálpebras abertas, durante vários minutos. No caso de uso de lentes de contato, remova-as, se for fácil e enxague novamente. Consulte um médico. Leve este documento.'''

#gestis
if sec4Gestis:
    intake = translate(re.sub(r"\[.*?\]", "", sec4Gestis['intake']).strip())
#icsc
if data['icsc']:
    text = data['icsc']['td_list'][20].text
    clean_text = text.replace('\xa0', ' ')
    if clean_text != ' ':
        intake = translate(clean_text)
if intake == '':
    intake ='''Não induza o vômito. Nunca forneça algo por via oral a uma pessoa inconsciente. Lave a boca da vítima com água em abundância. Consulte imediatamente um médico. Leve este documento.'''

#symptoms
after = '''Não disponível'''
if data['icsc']:
    symptoms = {
            'Inalação': translate(data['icsc']['td_list'][9].text.replace('\xa0', ' ')),
            'Contato com a pele': translate(data['icsc']['td_list'][12].text.replace('\xa0', ' ')),
            'Contato com os olhos': translate(data['icsc']['td_list'][15].text.replace('\xa0', ' ')),
            'Ingestão': translate(data['icsc']['td_list'][18].text.replace('\xa0', ' '))
        }
    after = "\n".join(f"{label}: {desc}" for label, desc in symptoms.items() if desc.strip())

doctor = '''Ao prestar socorro, proteja-se para evitar contato com a substância causadora do dano. O tratamento deve focar em aliviar os sintomas e garantir o suporte das funções vitais, como repor fluidos e eletrólitos, corrigir problemas metabólicos e, se necessário, auxiliar na respiração. Em caso de contato com a pele, evite esfregar a área afetada.'''
#Section 5
#Meios de extinção:
extinction = ''
if data.get('gestis') and data['gestis'].get('SAFE HANDLING'):
    safe_handling_list = data['gestis']['SAFE HANDLING']
    fire_fighting_text = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('FIRE FIGHTING MEASURES'):
            fire_fighting_text = text
            break
    if fire_fighting_text:
        match = re.search(r'Instructions(.*?)(Special protective equipment|$)', fire_fighting_text, re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            extinction = translate(conteudo)
        else:
            extinction = 'Não disponível'
    else:
        extinction = 'Não disponível'    
if data['icsc']:
    text = translate(data['icsc']['td_list'][8].text.replace('\xa0', ' '))
    if text != '':
        extinction = text
        
if extinction == '':
    extinction = 'Não disponível'
    
    
#Perigos específicos da mistura ou substância:
EspDangerous = 'Não disponível'
if data['icsc']:
    text = translate(data['icsc']['td_list'][6].text.replace('\xa0', ' '))
    if text.strip():
        EspDangerous= text
    
#Medidas de proteção especiais para a equipe de combate a incêndio:
firefighters = 'Não disponível'
if data.get('gestis') and data['gestis'].get('SAFE HANDLING'):
    safe_handling_list = data['gestis']['SAFE HANDLING']
    fire_fighting_text = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('FIRE FIGHTING MEASURES'):
            fire_fighting_text = text
            break
    if fire_fighting_text:
        match = re.search(r'Special protective equipment(.*?)(\n[A-Z ]{3,}|$)', fire_fighting_text, re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                firefighters = translate(conteudo)

#sec 6
#Para o pessoal que não faz parte dos serviços de emergência:
NonEmergencyPP = '''Não fume. Evite contato com o produto. Caso necessário, utilize equipamento de proteção individual conforme descrito na seção 8.''' #always

#Para pessoal de serviço de emergência:
EmergencyPP = '''Isole o vazamento de fontes de ignição preventivamente.''' #always

#Precauções ao meio ambiente:
environment = '''Não deve ser jogado no meio ambiente.''' #always

#Métodos e materiais para contenção e limpeza:
containmentClean = '''Coletar tanto quanto possível do derramamento com um material absorvente adequado.
Contenha o vazamento, absorva com material absorvente não combustível (por exemplo, areia, terra, terra diatomácea, vermiculita) e transfira para um recipiente para descarte de acordo com os regulamentos locais/nacionais (consulte a seção 13).
Varrer e escavar para recipientes adequados para eliminação de resíduos.
Depois de limpar, lavar os traços da substância com água.
Para a limpeza do chão e dos objectos contaminados por este produto, utilizar muita água''' #default
#TECHNICAL MEASURES - HANDLING->Cleaning and maintenance
if data['icsc']:
    text = data['icsc']['td_list'][21].text.replace('\xa0', ' ')
    if text.strip():
        containmentClean = translate(text)

if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('TECHNICAL MEASURES - HANDLING'):
            handling = text
            break
    if handling:
        match = re.search(r'Cleaning and maintenance\s*(.*?)(?=\n[A-Z][A-Z ]{2,}|$)', handling, re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                containmentClean = translate(conteudo)

#section 7
#Precauções para manuseio seguro:
SafeHandling = '''Manuseie em local arejado e com ventilação adequada. Evite a formação de poeiras, vapores ou névoas. Reduza a exposição direta ao produto sempre que possível. Utilize os equipamentos de proteção individual apropriados. Evite contato com substâncias ou materiais incompatíveis.'''
#TECHNICAL MEASURES - HANDLING -> Workplace
if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('TECHNICAL MEASURES - HANDLING'):
            handling = text
            break
    if handling:
        match = re.search(r'Workplace\s*(.*?)(?=\n[A-Z][A-Z ]{2,}|$)', handling, re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                SafeHandling = translate(conteudo)

#Medidas de higiene:
hygiene = '''Lave as mãos e o rosto cuidadosamente após o manuseio e antes de comer, beber, fumar ou ir ao banheiro. Roupas contaminadas devem ser trocadas e lavadas antes de sua reutilização. Remova a roupa e o equipamento de proteção contaminado antes de entrar nas áreas de alimentação.'''#always

#Prevenção de incêndio e explosão:
FireExplosion = '''Não se espera que o produto apresente risco significativo de incêndio ou explosão em condições normais de uso e armazenamento.'''
#icsc prevention fire & explosion
if data['icsc']:
    text = data['icsc']['td_list'][7].text.replace('\xa0', ' ')
    if text.strip():
        FireExplosion = translate(text)

#Condições adequadas:
adqCondition = '''Armazene em local seco, fresco e bem ventilado. Mantenha os recipientes fechados e protegidos da luz solar direta e da umidade. Evite a proximidade de materiais incompatíveis.'''
#icsc storage
if data['icsc']:
    text = data['icsc']['td_list'][7].text.replace('\xa0', ' ')
    if text.strip():
        FireExplosion = translate(text)

#Materiais adequados para embalagem:
adqPackage = '''Não disponível'''
#icsc packaging
if data['icsc']:
    text = data['icsc']['td_list'][24].text.replace('\xa0', ' ')
    if text.strip():
        adqPackage = translate(text)

#TECHNICAL MEASURES - STORAGE -> Conditions of collocated storage
if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('TECHNICAL MEASURES - STORAGE'):
            handling = text
            break
    if handling:
        match = re.search(r'Conditions of collocated storage\s*(.*?)(?=\n[A-Z][A-Z ]{2,}|$)', handling, re.DOTALL)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                adqPackage = translate(conteudo)

#Sec8

#Limites de exposição ocupacional:
exposure = '''Não disponível'''
#ICSC->OCCUPATIONAL EXPOSURE LIMITS
if data['icsc']:
    text = data['icsc']['td_list'][35].text.replace('\xa0', ' ')
    if text.strip():
        exposure = translate(text)
#CETESB
if data['cetesb']:
    lines = [" | ".join(item) for item in data['cetesb'][8]]
    text = "\n".join(lines)
    if text.strip():
        exposure = text

#Indicadores biológicos:
biology = 'Não disponível.' #NOT FOUND IN GESTIS, ICSC, CETESB

#Outros limites e valores:
otherLimits = 'Não disponível.' #NOT FOUND IN GESTIS, ICSC, CETESB

#Medidas de controle de engenharia:
engineeringCtrl = '''Recomenda-se o uso de ventilação adequada para manter as concentrações de vapores, névoas ou poeiras abaixo dos limites de exposição ocupacional. Sempre que possível, utilize sistemas de exaustão local e ventilação geral para reduzir a exposição no ambiente de trabalho.
Instalações de lavagem de olhos e chuveiros de emergência devem estar disponíveis próximas às áreas de manuseio do produto.
Assegurar que os procedimentos de higiene e segurança sejam seguidos, evitando contato direto com a substância e prevenindo a inalação de partículas, vapores ou gases liberados durante o uso.'''

#Proteção dos olhos/face:
eyesFace = 'Não disponível'
#gestis
if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('PERSONAL PROTECTION'):
            handling = text
            break
    if handling:
        match = re.search(
    r'Eye protection\s*(.*?)(?=(?:Body protection|Respiratory protection|Hand protection|Skin protection|Occupational hygiene|$))',
    handling, re.DOTALL | re.IGNORECASE
)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                eyesFace = translate(conteudo)
#Proteção da pele e do corpo:
skinBody = 'Não disponível'
#gestis
if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('PERSONAL PROTECTION'):
            handling = text
            break
    if handling:
        match = re.search(
    r'Body protection\s*(.*?)(?=(?:Respiratory protection|Eye protection|Hand protection|Skin protection|Occupational hygiene|$))',
    handling, re.DOTALL | re.IGNORECASE
)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                skinBody = translate(conteudo)
#Proteção respiratória:
Breathing = 'Não disponível'
#gestis
if data['gestis'] and data['gestis']['SAFE HANDLING']:
    safe_handling_list = data['gestis']['SAFE HANDLING']
    handling = None
    for item in safe_handling_list:
        text = item.get('text', '')
        if text.startswith('PERSONAL PROTECTION'):
            handling = text
            break
    if handling:
        match = re.search(
    r'Respiratory protection\s*(.*?)(?=(?:Body protection|Eye protection|Hand protection|Skin protection|Occupational hygiene|$))',
    handling, re.DOTALL | re.IGNORECASE
)
        if match:
            conteudo = match.group(1).strip()
            if conteudo:
                Breathing = translate(conteudo)
#Perigos térmicos:
Termic = '''Evitar a exposição do produto a fontes de calor, superfícies aquecidas, faíscas ou chamas abertas. O contato com temperaturas elevadas pode provocar decomposição, alteração das propriedades químicas ou liberação de vapores/gases perigosos. Adotar medidas de prevenção para reduzir riscos de queimaduras e acidentes térmicos durante o manuseio, armazenamento e transporte.'''
#section9

entrada1,entrada2,entrada3,entrada4 = [],[],[],[]
pass
if data["cetesb"]:
    entrada1 = data['cetesb'][7]
if data['icsc']:
    entrada2 = data['icsc']['td_list'][32] or []
if data["gestis"]:
    entrada4 = data['gestis']['PHYSICAL AND CHEMICAL PROPERTIES'] or []
    entrada3 = data['gestis']['CHARACTERISATION'] or []


entradas = [entrada1, entrada2, entrada3, entrada4]
saida = extrair_dados_dinamico(entradas)

physical_state = translate(saida["physical_state"])
color = translate(saida['color'])
odor = translate(saida['odor'])
melting_point = translate(saida['melting_point'])
boiling_point = translate(saida['boiling_point'])
flammability = translate(saida['flammability'])
explosive_limit = translate(saida['explosive_limit'])
flash_point = translate(saida['flash_point'])
auto_ignition_temperature = translate(saida['auto_ignition_temperature'])
decomposition_temperature = translate(saida['decomposition_temperature'])
pH = translate(saida['pH'])
kinematic_viscosity = translate(saida['kinematic_viscosity'])
water_solubility = translate(saida['water_solubility'])
partition_coefficient = translate(saida['partition_coefficient'])
vapor_pressure = translate(saida['vapor_pressure'])
relative_density = translate(saida['relative_density'])
relative_vapor_density = translate(saida['relative_vapor_density'])
particle_characteristics = translate(saida['particle_characteristics'])
OtherInfo = translate(saida['OtherInfo'])


doc = HeaderGen(Document(),ProductName)
mkSec1(doc,ProductName,Uses,ProviderInfo,Emergency)
mkSec2(doc,Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases)
mkSec3(doc,subOrMix,chemID,synonym,cas,impure)
mkSec4(doc, inhalation,skin,eyes,intake,after,doctor)
mkSec5(doc,extinction,EspDangerous,firefighters)
mkSec6(doc,NonEmergencyPP,EmergencyPP,environment,containmentClean)
mkSec7(doc,SafeHandling,hygiene,FireExplosion,adqCondition,adqPackage)
mkSec8(doc,exposure,biology,otherLimits,engineeringCtrl,eyesFace,skinBody,Breathing,Termic)
mkSec9(doc, physical_state,color,odor,melting_point,boiling_point,
       flammability,explosive_limit,flash_point,auto_ignition_temperature,
       decomposition_temperature,pH,kinematic_viscosity,water_solubility,
       partition_coefficient,vapor_pressure,relative_density,relative_vapor_density,
       particle_characteristics,OtherInfo)



nome_arquivo = f'FDS_{ProductName.replace(" ", "_")}_EN.docx'
doc.save(nome_arquivo)