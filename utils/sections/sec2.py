from utils.docxFormater.easySections import mkSec2
from utils.docxFormater.pictograms import classToPictograms
from utils.translator import translateText
from dataclasses import dataclass
import re

@dataclass
class secTwoInfo:
    Classification: str
    ClassSystem:str
    OtherDangerous:str
    PictoPath:str
    pictoWidth:int
    pictoHeight:int
    warningWord:str
    warningPhrases:str
    worryPhrases:str


DEFAULT_TEXT = "Não disponível"
DEFAULT_CLASS = "Produto não perigoso"
CLASS_SYSTEM = "Norma ABNT-NBR 14725-2023.\nSistema Globalmente Harmonizado para a Classificação e Rotulagem de Produtos Químicos, ONU."
OTHER_DANGEROUS = "Não são conhecidos outros perigos do produto."

def extractPhrases(marker, rawText, pattern):
    parts = re.split(marker, rawText, maxsplit=1)
    if len(parts) > 1:
        found = re.findall(pattern, parts[1])
        if found:
            joined = "\n".join([f.strip().rstrip('.') + ";" for f in found])
            return translateText(joined)
    return DEFAULT_TEXT

def extractGestis(gestisData):
    if not gestisData or 'REGULATIONS' not in gestisData or not gestisData['REGULATIONS']:
        return None

    rawText = gestisData['REGULATIONS'][0]['text']
    
    classification = ""
    matchClass = re.search(r'Classification\s+(.*?)\s+Signal Word', rawText, re.DOTALL)
    if matchClass:
        cleanText = re.sub(r'H\d{3}\s*', '\n', matchClass.group(1))
        classification = "\n".join([line.strip().rstrip(';') + ';' for line in cleanText.split('\n') if line.strip()])
        classification = translateText(classification)

    matchSignal = re.search(r'Signal Word\s*"?(\w+)"?', rawText)
    signalWord = translateText(matchSignal.group(1)) if matchSignal else DEFAULT_TEXT

    hPhrases = extractPhrases(r'H-phrases',rawText , r'(H\d+:.*?\.)')
    pPhrases = extractPhrases(r'P-phrases',rawText ,r'(P[\d\+]+:.*?\.)')

    return {
        'classification': classification,
        'signal_word': signalWord,
        'h_phrases': hPhrases,
        'p_phrases': pPhrases
    }

def extractCetesb(cetesbData):
    if not cetesbData or len(cetesbData) < 4:
        return None
    
    try:
        dataBlock = cetesbData[3]
        
        rawClass = dataBlock[0][0].replace("Classificação de perigo", "").strip()
     
        parts = re.split(r'(?=(?:Toxicidade|Corrosão|Lesões|Perigoso|Corrosivo))', rawClass)
        cleanParts = [p.strip().replace(",", " -") for p in parts if p.strip()]
        classification = ";\n".join(cleanParts) + "."

        rawSignal = dataBlock[2][0]
        matchSignal = re.search(r'Palavra de advertência(\w+)', rawSignal)
        signalWord = matchSignal.group(1) if matchSignal else DEFAULT_TEXT

        rawH = re.sub(r'^Frase\(s\) de perigo', '', dataBlock[3][0])
        hPhrasesList = re.findall(r'H\d+\s*-\s*[^H]+', rawH)
        hPhrases = "\n".join([f.strip() + ";" for f in hPhrasesList]) if hPhrasesList else DEFAULT_TEXT

        rawP = re.sub(r'^Frase\(s\) de precaução.*?\)', '', dataBlock[4][0])
        pPhrasesList = re.findall(r'(P[\d\+ ]+-.*?\.)', rawP)
        pPhrases = "\n".join([f.strip().rstrip('.') + ";" for f in pPhrasesList]) if pPhrasesList else DEFAULT_TEXT

        return {
            'classification': classification,
            'signal_word': signalWord,
            'h_phrases': hPhrases,
            'p_phrases': pPhrases
        }

    except (IndexError, AttributeError):
        return None

def infoGet(data:dict):
    cetesbResult = extractCetesb(data.get('cetesb'))
    gestisResult = extractGestis(data.get('gestis'))

    finalData = cetesbResult or gestisResult or {}

    Classification = finalData.get('classification', DEFAULT_CLASS)
    if not Classification: Classification = DEFAULT_CLASS
    PictoPath = classToPictograms(Classification)

    warningWord = finalData.get('signal_word',DEFAULT_TEXT)
    warningPhrases = finalData.get('h_phrases',DEFAULT_TEXT)
    worryPhrases = finalData.get('p_phrases',DEFAULT_TEXT)

    return secTwoInfo(
            Classification = Classification,
            ClassSystem = CLASS_SYSTEM,
            OtherDangerous = OTHER_DANGEROUS,
            PictoPath = PictoPath,
            pictoWidth = 4,
            pictoHeight = 2,
            warningWord = warningWord,
            warningPhrases = warningPhrases,
            worryPhrases = worryPhrases)

def generate(Document,info:secTwoInfo):
    
    mkSec2(Document,info.Classification,info.ClassSystem,info.OtherDangerous,info.PictoPath,info.pictoWidth,info.pictoHeight,info.warningWord,info.warningPhrases,info.worryPhrases)