from utils.translator import translateText
from utils.docxFormater.easySections import mkSec6
from dataclasses import dataclass
import re

@dataclass
class sec6Info:
    nonEmergencyPP:str
    emergencyPP:str
    Environment:str
    ContainmentClean:str


NONEMERGENCYPP = '''Não fume. Evite contato com o produto. Caso necessário, utilize equipamento de proteção individual conforme descrito na seção 8.''' #always

EMERGENCYPP = '''Isole o vazamento de fontes de ignição preventivamente.''' #always

ENVIRONMENT = '''Não deve ser jogado no meio ambiente.''' #always

CONTAINMENTCLEAN = '''Coletar tanto quanto possível do derramamento com um material absorvente adequado.
Contenha o vazamento, absorva com material absorvente não combustível (por exemplo, areia, terra, terra diatomácea, vermiculita) e transfira para um recipiente para descarte de acordo com os regulamentos locais/nacionais (consulte a seção 13).
Varrer e escavar para recipientes adequados para eliminação de resíduos.
Depois de limpar, lavar os traços da substância com água.
Para a limpeza do chão e dos objectos contaminados por este produto, utilizar muita água''' #default

def infoGet(data:dict)->sec6Info:
    if data['icsc']:
        text = data['icsc']['td_list'][21].text.replace('\xa0', ' ')
        if text.strip():
            CONTAINMENTCLEAN = translateText(text)

    if data['gestis'] and data['gestis']['SAFE HANDLING']:
        safeHandlingList = data['gestis']['SAFE HANDLING']
        handling = None
        for item in safeHandlingList:
            text = item.get('text', '')
            if text.startswith('TECHNICAL MEASURES - HANDLING'):
                handling = text
                break
        if handling:
            match = re.search(r'Cleaning and maintenance\s*(.*?)(?=\n[A-Z][A-Z ]{2,}|$)', handling, re.DOTALL)
            if match:
                conteudo = match.group(1).strip()
                if conteudo:
                    CONTAINMENTCLEAN = translateText(conteudo)
    
    return sec6Info(
        nonEmergencyPP=NONEMERGENCYPP,
        emergencyPP=EMERGENCYPP,
        Environment=ENVIRONMENT,
        ContainmentClean=CONTAINMENTCLEAN
        )

def generate(Document,info:sec6Info):
    mkSec6(Document,info.nonEmergencyPP,info.emergencyPP,info.Environment,info.ContainmentClean)
