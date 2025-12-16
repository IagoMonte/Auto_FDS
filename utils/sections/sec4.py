from utils.translator import translateText
from utils.docxFormater.easySections import mkSec4
from dataclasses import dataclass
import re

DEFAULTS = {
    'inhalation': '''Remova a vítima para um local ventilado e mantenha-a em repouso, numa posição que não dificulte a respiração. Caso a pessoa sinta indisposição, contate imediatamente um médico. Se possível, leve consigo o rótulo ou a embalagem da substancia.''',
    'skin': '''Lave imediatamente a pele exposta com quantidade suficiente de água para remoção do material. Retire as roupas ou acessórios contaminados. Em caso de contato menor com a pele, evite espalhar o produto em áreas não atingidas. Consulte um médico. Leve este documento.''',
    'eyes': '''Lave imediatamente os olhos com quantidade suficiente de água, mantendo as pálpebras abertas, durante vários minutos. No caso de uso de lentes de contato, remova-as, se for fácil e enxague novamente. Consulte um médico. Leve este documento.''',
    'intake': '''Não induza o vômito. Nunca forneça algo por via oral a uma pessoa inconsciente. Lave a boca da vítima com água em abundância. Consulte imediatamente um médico. Leve este documento.''',
    'after': 'Não disponível',
    'doctor': '''Ao prestar socorro, proteja-se para evitar contato com a substância causadora do dano. O tratamento deve focar em aliviar os sintomas e garantir o suporte das funções vitais, como repor fluidos e eletrólitos, corrigir problemas metabólicos e, se necessário, auxiliar na respiração. Em caso de contato com a pele, evite esfregar a área afetada.'''
}

@dataclass
class sec4Info:
    inhalation : str
    skin : str
    eyes : str
    intake : str
    after : str
    doctor : str

def extractGestis(gestisData):
    if not gestisData: return {}
    
    try:
        rawText = gestisData.get('OCCUPATIONAL HEALTH AND FIRST AID', [{},{},{}])[2].get('text', '')
        if not rawText: return {}

        start = rawText.find("FIRST AID")
        start = 0 if start == -1 else start
        
        candidates = [
            rawText.find(marker, start) 
            for marker in ["Information for physicians", "Recommendations", "Annotation"]
        ]
        ends = [i for i in candidates if i != -1]
        end = min(ends) if ends else len(rawText)
        
        block = rawText[start:end]
        
        mapping = {
            "Eyes": "eyes",
            "Skin": "skin",
            "Respiratory tract": "inhalation",
            "Swallowing": "intake",
        }
        
        headerRE = re.compile(r"\b(" + "|".join(mapping.keys()) + r")\b(?!:)")
        matches = list(headerRE.finditer(block))
        
        result = {}
        for i, m in enumerate(matches):
            key = mapping[m.group(1)]
            start_content = m.end()
            end_content = matches[i + 1].start() if i + 1 < len(matches) else len(block)
            content = block[start_content:end_content].strip(" -:\n\t ")
            result[key] = translateText(re.sub(r"\[.*?\]", "", content).strip())
            
        return result
    except (IndexError, KeyError, AttributeError):
        return {}

def extractIcsc(icscData, index):
    if not icscData or 'td_list' not in icscData: return None
    try:
        text = icscData['td_list'][index].text
        clean_text = text.replace('\xa0', ' ').strip()
        return translateText(clean_text) if clean_text else None
    except (IndexError, AttributeError):
        return None



def infoGet(data: dict) -> sec4Info:
    gestisInfo = extractGestis(data.get('gestis'))
    
    fieldMap = {
        'inhalation': 11,
        'skin': 14,
        'eyes': 17,
        'intake': 20
    }
    
    finalValues = {}
    
    for field, icscIDX in fieldMap.items():
        val = gestisInfo.get(field)
        
        if not val:
            val = extractIcsc(data.get('icsc'), icscIDX)
            
        if not val:
            val = DEFAULTS[field]
            
        finalValues[field] = val

    afterVal = DEFAULTS['after']
    if data.get('icsc'):
        symptomsMap = {
            'Inalação': 9,
            'Contato com a pele': 12,
            'Contato com os olhos': 15,
            'Ingestão': 18
        }
        parts = []
        for label, idx in symptomsMap.items():
            desc = extractIcsc(data['icsc'], idx)
            if desc:
                parts.append(f"{label}: {desc}")
        
        if parts:
            afterVal = "\n".join(parts)

    return sec4Info(
        inhalation=finalValues['inhalation'],
        skin=finalValues['skin'],
        eyes=finalValues['eyes'],
        intake=finalValues['intake'],
        after=afterVal,
        doctor=DEFAULTS['doctor']
    )

def generate(Document,info:sec4Info):
    mkSec4(Document, info.inhalation,info.skin,info.eyes,info.intake,info.after,info.doctor)