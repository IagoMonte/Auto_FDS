from utils.translator import translateText
from utils.docxFormater.easySections import mkSec3
from dataclasses import dataclass

@dataclass
class secThreeInfo:
    subOrMix:str
    synonym:str
    impure:str

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
        
    return secThreeInfo(subOrMix = subOrMix,
                        synonym  = synonym,
                        impure   = impure)

def generate(Document,info:secThreeInfo,productName,cas):
    mkSec3(Document,info.subOrMix,productName,info.synonym,cas,info.impure)