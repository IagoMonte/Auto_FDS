from utils.docxFormater.easySections import mkSec2
from utils.docxFormater.pictograms import classToPictograms
from utils.translator import translateText
import re

def getinfo(data:dict):
    Classfication='''Produto não perigoso'''
    #gestis
    if data['gestis']:
        text = data['gestis']['REGULATIONS'][0]['text']
        match = re.search(r'Classification\s+(.*?)\s+Signal Word', text, re.DOTALL)
        classificationGestis = match.group(1).strip() if match else ""
        classificationClean = re.sub(r'H\d{3}\s*', '\n', classificationGestis)
        lines = [line.strip().rstrip(';') + ';' for line in classificationClean.split('\n') if line.strip()]
        ClassficationGestis = "\n".join(lines)

        if ClassficationGestis != '':
            Classfication = translateText(ClassficationGestis)
    
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
    PictoPath = classToPictograms(Classfication)
    pictoWidth = 4 #inches
    pictoHeight = 2 #inches

    warningWord = 'Não disponível'

    if data['gestis']:
        text = re.search(r'Signal Word\s*"?(\w+)"?', data['gestis']['REGULATIONS'][0]['text'])
        if text:
            text = text.group(1)
            warningWord = translateText(text)

    if data['cetesb']:
        text = re.search(r'Palavra de advertência(\w+)', data['cetesb'][3][2][0])
        if text:
            text = text.group(1)
            warningWord = text

    warningPhrases = 'Não disponível'
    if data['gestis']:
        hPhrases = re.split(r'H-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
        if len(hPhrases) > 2:
            phrases = re.findall(r'(H\d+:.*?\.)', hPhrases[1])
            formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
            if formatedPhrases:
                formatedPhrases = "\n".join(formatedPhrases)
                warningPhrases = translateText(formatedPhrases)

    if data['cetesb']:
        text = re.sub(r'^Frase\(s\) de perigo', '', data['cetesb'][3][3][0])
        phrases = re.findall(r'H\d+\s*-\s*[^H]+', text)
        formatedPhrases = [f.strip() + ";\n" for f in phrases]
        if formatedPhrases:
            warningPhrases = formatedPhrases

    worryPhrases ='Não disponível'
    if data['gestis']:
        pPhrases = re.split(r'P-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
        if len(hPhrases) > 2:
            phrases = re.findall(r'(P[\d\+]+:.*?\.)', pPhrases[1])
            formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
            if formatedPhrases:
                formatedPhrases = "\n".join(formatedPhrases)
                worryPhrases = translateText(formatedPhrases)

    if data['cetesb']:
        pPhrases = re.sub(r'^Frase\(s\) de precaução.*?\)', '', data['cetesb'][3][4][0])
        phrases = re.findall(r'(P[\d\+ ]+-.*?\.)', pPhrases)
        formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
        if formatedPhrases:
            worryPhrases = "\n".join(formatedPhrases)

    return Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases

def generate(Document,data:dict):
    Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases = getinfo(data)
    mkSec2(Document,Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases)