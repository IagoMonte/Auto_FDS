from utils.docxFormater.easySections import mkSec7
from utils.translator import translateText
from dataclasses import dataclass
import re

@dataclass
class sec7Info:
    safeHandling: str
    hygiene: str
    fireExplosion: str
    storageConditions: str
    packaging: str

DEFAULTS = {
    'safeHandling': '''Manuseie em local arejado e com ventilação adequada. Evite a formação de poeiras, vapores ou névoas. Reduza a exposição direta ao produto sempre que possível. Utilize os equipamentos de proteção individual apropriados. Evite contato com substâncias ou materiais incompatíveis.''',
    'hygiene': '''Lave as mãos e o rosto cuidadosamente após o manuseio e antes de comer, beber, fumar ou ir ao banheiro. Roupas contaminadas devem ser trocadas e lavadas antes de sua reutilização. Remova a roupa e o equipamento de proteção contaminado antes de entrar nas áreas de alimentação.''',
    'fireExplosion': '''Não se espera que o produto apresente risco significativo de incêndio ou explosão em condições normais de uso e armazenamento.''',
    'storageConditions': '''Armazene em local seco, fresco e bem ventilado. Mantenha os recipientes fechados e protegidos da luz solar direta e da umidade. Evite a proximidade de materiais incompatíveis.''',
    'packaging': 'Não disponível'
}

def extractGestisSection(gestisData, sectionPrefix, subsectionName):
    if not gestisData or not gestisData.get('SAFE HANDLING'):
        return None
    
    try:
        targetBlock = None
        for item in gestisData['SAFE HANDLING']:
            text = item.get('text', '')
            if text.startswith(sectionPrefix):
                targetBlock = text
                break
        
        if not targetBlock:
            return None
        
        pattern = rf'{subsectionName}\s*(.*?)(?=\n[A-Z][A-Z ]{{2,}}|$)'
        match = re.search(pattern, targetBlock, re.DOTALL)
        
        if match:
            content = match.group(1).strip()
            return translateText(content) if content else None
            
    except (KeyError, AttributeError, IndexError):
        pass
    
    return None

def extractIcscField(icscData, index):
    if not icscData or 'td_list' not in icscData:
        return None
    
    try:
        text = icscData['td_list'][index].text.replace('\xa0', ' ').strip()
        return translateText(text) if text else None
    except (IndexError, AttributeError):
        return None


def infoGet(data: dict) -> sec7Info:
    safeHandling = (
        extractGestisSection(data.get('gestis'), 'TECHNICAL MEASURES - HANDLING', 'Workplace') 
        or DEFAULTS['safeHandling']
    )
    
    hygiene = DEFAULTS['hygiene']
    
    fireExplosion = (
        extractIcscField(data.get('icsc'), 7) 
        or DEFAULTS['fireExplosion']
    )
    
    storageConditions = (
        extractIcscField(data.get('icsc'), 7)  # Ajuste o índice se necessário
        or DEFAULTS['storageConditions']
    )
    
    packaging = (
        extractIcscField(data.get('icsc'), 24)
        or extractGestisSection(data.get('gestis'), 'TECHNICAL MEASURES - STORAGE', 'Conditions of collocated storage')
        or DEFAULTS['packaging']
    )
    
    return sec7Info(
        safeHandling=safeHandling,
        hygiene=hygiene,
        fireExplosion=fireExplosion,
        storageConditions=storageConditions,
        packaging=packaging
    )

def generate(Document,info:sec7Info):
    mkSec7(Document,info.safeHandling,info.hygiene,
    info.fireExplosion,info.storageConditions,
    info.packaging)