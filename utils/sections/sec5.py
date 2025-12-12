from utils.docxFormater.easySections import mkSec5
from utils.translator import translateText
from dataclasses import dataclass
import re

@dataclass
class secFiveInfo:
    extinction: str
    esp_dangerous: str
    firefighters: str


def getICSCText(index,data):
        try:
            text = data['icsc']['td_list'][index].text.replace('\xa0', ' ')
            translated = translateText(text)
            return translated if translated.strip() else None
        except (KeyError, IndexError, AttributeError, TypeError):
            return None

def getGestisRegex(pattern, fire_fighting_text = ''):
    if not fire_fighting_text:
        return None
    match = re.search(pattern, fire_fighting_text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        return translateText(content) if content else None
    return None

def infoGet(data:dict) -> secFiveInfo:
    gestis_handling = data.get('gestis', {}).get('SAFE HANDLING', [])
    fire_fighting_text = next(
        (item.get('text', '') for item in gestis_handling if item.get('text', '').startswith('FIRE FIGHTING MEASURES')), 
        None
    )

    #extinction
    extinction = (
        getICSCText(8,data) or 
        getGestisRegex(r'Instructions(.*?)(Special protective equipment|$)',fire_fighting_text) or 
        'Não disponível'
    )

    #Especial Dangerous
    esp_dangerous = getICSCText(6,data) or 'Não disponível'

    #firefighters
    firefighters = (
        getGestisRegex(r'Special protective equipment(.*?)(\n[A-Z ]{3,}|$)',fire_fighting_text) or 
        'Não disponível'
    )
    
    return  secFiveInfo(extinction      = extinction,
                        esp_dangerous   = esp_dangerous,
                        firefighters    = firefighters)
def generate(Document,info:secFiveInfo):
    mkSec5(Document,info.extinction,info.EspDangerous,info.firefighters)