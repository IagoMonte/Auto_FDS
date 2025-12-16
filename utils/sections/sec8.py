from utils.docxFormater.easySections import mkSec8
from utils.translator import translateText
from dataclasses import dataclass
import re

DEFAULTS = {
    'exposure': 'Não disponível',
    'biology': 'Não disponível.',
    'otherLimits': 'Não disponível.',
    'engineeringCtrl': '''Recomenda-se o uso de ventilação adequada para manter as concentrações de vapores, névoas ou poeiras abaixo dos limites de exposição ocupacional. Sempre que possível, utilize sistemas de exaustão local e ventilação geral para reduzir a exposição no ambiente de trabalho.
Instalações de lavagem de olhos e chuveiros de emergência devem estar disponíveis próximas às áreas de manuseio do produto.
Assegurar que os procedimentos de higiene e segurança sejam seguidos, evitando contato direto com a substância e prevenindo a inalação de partículas, vapores ou gases liberados durante o uso.''',
    'eyesFace': 'Não disponível',
    'skinBody': 'Não disponível',
    'breathing': 'Não disponível',
    'termic': '''Evitar a exposição do produto a fontes de calor, superfícies aquecidas, faíscas ou chamas abertas. O contato com temperaturas elevadas pode provocar decomposição, alteração das propriedades químicas ou liberação de vapores/gases perigosos. Adotar medidas de prevenção para reduzir riscos de queimaduras e acidentes térmicos durante o manuseio, armazenamento e transporte.'''
}

@dataclass
class sec8Info:
    exposure: str
    biology: str
    otherLimits: str
    engineeringCtrl: str
    eyesFace: str
    skinBody: str
    breathing: str
    termic: str

def extractCetesbTable(cetesbData, index):
    if not cetesbData or len(cetesbData) <= index:
        return None
    
    try:
        lines = [" | ".join(item) for item in cetesbData[index]]
        text = "\n".join(lines).strip()
        return text if text else None
    except (IndexError, TypeError):
        return None

def extractIcscField(icscData, index):
    if not icscData or 'td_list' not in icscData:
        return None
    
    try:
        text = icscData['td_list'][index].text.replace('\xa0', ' ').strip()
        return translateText(text) if text else None
    except (IndexError, AttributeError):
        return None

def extractGestisPersonalProtection(gestisData, protectionType):
    if not gestisData or not gestisData.get('SAFE HANDLING'):
        return None
    
    try:
        personalProtectionBlock = None
        for item in gestisData['SAFE HANDLING']:
            text = item.get('text', '')
            if text.startswith('PERSONAL PROTECTION'):
                personalProtectionBlock = text
                break
        
        if not personalProtectionBlock:
            return None
        
        delimiters = [
            'Body protection',
            'Respiratory protection', 
            'Eye protection',
            'Hand protection',
            'Skin protection',
            'Occupational hygiene'
        ]
        
        delimiters = [d for d in delimiters if d != protectionType]
        
        delimiterPattern = '|'.join(delimiters)
        pattern = rf'{protectionType}\s*(.*?)(?=(?:{delimiterPattern}|$))'
        
        match = re.search(pattern, personalProtectionBlock, re.DOTALL | re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            return translateText(content) if content else None
            
    except (KeyError, AttributeError, IndexError):
        pass
    
    return None

def infoGet(data: dict) -> sec8Info:
    
    exposure = (
        extractCetesbTable(data.get('cetesb'), 8)
        or extractIcscField(data.get('icsc'), 35)
        or DEFAULTS['exposure']
    )
    
    biology = DEFAULTS['biology']
    
    otherLimits = DEFAULTS['otherLimits']
    
    engineeringCtrl = DEFAULTS['engineeringCtrl']
    
    gestisData = data.get('gestis')
    
    eyesFace = (
        extractGestisPersonalProtection(gestisData, 'Eye protection')
        or DEFAULTS['eyesFace']
    )
    
    skinBody = (
        extractGestisPersonalProtection(gestisData, 'Body protection')
        or DEFAULTS['skinBody']
    )
    
    breathing = (
        extractGestisPersonalProtection(gestisData, 'Respiratory protection')
        or DEFAULTS['breathing']
    )
    
    termic = DEFAULTS['termic']
    
    return sec8Info(
        exposure=exposure,
        biology=biology,
        otherLimits=otherLimits,
        engineeringCtrl=engineeringCtrl,
        eyesFace=eyesFace,
        skinBody=skinBody,
        breathing=breathing,
        termic=termic
    )

def generate(Document,info:sec8Info):
    mkSec8(Document,info.exposure,info.biology,info.otherLimits,
           info.engineeringCtrl,info.eyesFace,info.skinBody,
           info.breathing,info.termic)