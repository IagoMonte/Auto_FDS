from utils.docxFormater.easySections import mkSec1
from utils.translator import translateText
from dataclasses import dataclass
import re

@dataclass
class secOneInfo:
    ProductName : str
    Uses: str    
    ProviderInfo: str
    Emergency: str

def infoGet(data: str) ->secOneInfo:
    ProductName = 'Não disponível'
    ProviderInfo ='''
    PORTUGAL QUÍMICA LTDA.

    Endereço: Av. Marcelo Zanarotti, 465 - Distrito Industrial - Dumont/SP - Brasil - Cep: 14120-000
    Telefone: +55 16 3844-0999
    E-mail: portugal@portugalquimica.com.br
    ''' 
    Emergency = 'AMBIPAR - 0800-117-2020'

    if data['cetesb'] != []:
        ProductName = data['cetesb'][0][1][0]
    elif data['gestis']['IDENTIFICATION'] !='':
        text = data['gestis']['IDENTIFICATION'][0]['text']
        for marker in ["ZVG No:", "CAS No:", "EC No:"]:
            if marker in text:
                text = text.split(marker)[0].strip()
                break
        ProductName =translateText(" ".join(text.split()[:2]))

        casGestis = re.search(r'\d{2,7}-\d{2}-\d', data['gestis']['IDENTIFICATION'][0]['text']).group(0)
        casICSC = re.search(r'\d{2,7}-\d{2}-\d', data['icsc']['b_list'][2].text).group(0)
        if casGestis != casICSC:
            data['icsc'] = []
    elif data['icsc'] != []:
        ProductName = translateText(data['icsc']['b_list'][0].text.split(",")[0].strip()) 
    else:
        ProductName = input('Nome do produto')

    Uses = ''
    if Uses == '':
        Uses = 'Este produto químico é formulado para atender a diversas aplicações industriais e laboratoriais.'
    if data['cetesb'] != []:
        Uses = data['cetesb'][1][3][0][4::]
    
    return secOneInfo(
        ProductName = ProductName,
        Uses = Uses,
        ProviderInfo = ProviderInfo,
        Emergency = Emergency
    )

def generate(Document,info:secOneInfo):
    mkSec1(Document, info.ProductName, info.Uses, info.ProviderInfo, info.Emergency)