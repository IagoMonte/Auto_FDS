from utils.translator import translateText
import utils.sections.sec1 as sc1
from utils.docxFormater.easySections import mkSec3

def infoGet(data:dict):
    subOrMix = 'SUBSTÂNCIA'#Always
    impure = 'Não apresenta impurezas que contribuam para o perigo.'#Always
    
    synonym = 'Não disponível'
    if data['icsc']:
        synonym = ";".join(
            translateText(content)
            for i, content in enumerate(data['icsc']['td_list'][2].contents) 
            if i % 2 == 0
            )
    if data['cetesb']:
        synonym = data['cetesb'][1][0][0][9::]
        
    return subOrMix,synonym,impure
    

def generate(Document,data:dict):
    subOrMix,synonym,impure = infoGet(data)
    mkSec3(Document,subOrMix,sc1.infoGet(data)[0],synonym,data['CAS'],impure)
    pass