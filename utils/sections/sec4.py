from utils.translator import translateText
from utils.docxFormater.easySections import mkSec4
import re

def infoGet(data:dict):

    #first aid gestis
    if data['gestis']:
        sec4Gestis = None
        try:
            rawText = data['gestis']['OCCUPATIONAL HEALTH AND FIRST AID'][2]['text']
            start = rawText.find("FIRST AID")
            if start == -1:
                start = 0

            candidates = [
                rawText.find("Information for physicians", start),
                rawText.find("Recommendations", start),
                rawText.find("Annotation", start),
            ]
            ends = [i for i in candidates if i != -1]
            end = min(ends) if ends else len(rawText)
            block = rawText[start:end]

            headerRE = re.compile(r"\b(Eyes|Skin|Respiratory tract|Swallowing)\b(?!:)")
            matches = list(headerRE.finditer(block))

            mapping = {
                "Eyes": "eyes",
                "Skin": "skin",
                "Respiratory tract": "inhalation",
                "Swallowing": "intake",
            }
            result = {v: "" for v in mapping.values()}

            for i, m in enumerate(matches):
                header = m.group(1)
                startContent = m.end()
                endContent = matches[i + 1].start() if i + 1 < len(matches) else len(block)
                content = block[startContent:endContent].strip(" -:\n\t ").strip()
                result[mapping[header]] = content

            sec4Gestis = result
        except:
            pass

    #inhalation
    inhalation = ''
    if sec4Gestis:
        inhalation = translateText(re.sub(r"\[.*?\]", "", sec4Gestis['inhalation']).strip())
    if data['icsc']:
        text = data['icsc']['td_list'][11].text
        clean_text = text.replace('\xa0', ' ')
        if clean_text != ' ':
            inhalation = translateText(clean_text)
    if inhalation == '':
        inhalation = '''Remova a vítima para um local ventilado e mantenha-a em repouso, numa posição que não dificulte a respiração. Caso a pessoa sinta indisposição, contate imediatamente um médico. Se possível, leve consigo o rótulo ou a embalagem da substancia.'''

    #skin
    skin = ''
    if sec4Gestis:
        skin = translateText(re.sub(r"\[.*?\]", "", sec4Gestis['skin']).strip())

    if data['icsc']:
        text = data['icsc']['td_list'][14].text
        clean_text = text.replace('\xa0', ' ')
        if clean_text != ' ':
            skin = translateText(clean_text)
    
    if skin == '':
        skin = '''Lave imediatamente a pele exposta com quantidade suficiente de água para remoção do material. Retire as roupas ou acessórios contaminados. Em caso de contato menor com a pele, evite espalhar o produto em áreas não, atingidas. Consulte um médico. Leve este documento.'''

    #eyes
    eyes = ''
    if sec4Gestis:
        eyes = translateText(re.sub(r"\[.*?\]", "", sec4Gestis['eyes']).strip())
    
    if data['icsc']:
        text = data['icsc']['td_list'][17].text
        clean_text = text.replace('\xa0', ' ')
        if clean_text != ' ':
            eyes = translateText(clean_text)
    
    if eyes == '':
        eyes = '''Lave imediatamente os olhos com quantidade suficiente de água, mantendo as pálpebras abertas, durante vários minutos. No caso de uso de lentes de contato, remova-as, se for fácil e enxague novamente. Consulte um médico. Leve este documento.'''

    #intake
    if sec4Gestis:
        intake = translateText(re.sub(r"\[.*?\]", "", sec4Gestis['intake']).strip())
    
    if data['icsc']:
        text = data['icsc']['td_list'][20].text
        clean_text = text.replace('\xa0', ' ')
        if clean_text != ' ':
            intake = translateText(clean_text)
    
    if intake == '':
        intake ='''Não induza o vômito. Nunca forneça algo por via oral a uma pessoa inconsciente. Lave a boca da vítima com água em abundância. Consulte imediatamente um médico. Leve este documento.'''

    #after
    after = '''Não disponível'''
    if data['icsc']:
        symptoms = {
                'Inalação': translateText(data['icsc']['td_list'][9].text.replace('\xa0', ' ')),
                'Contato com a pele': translateText(data['icsc']['td_list'][12].text.replace('\xa0', ' ')),
                'Contato com os olhos': translateText(data['icsc']['td_list'][15].text.replace('\xa0', ' ')),
                'Ingestão': translateText(data['icsc']['td_list'][18].text.replace('\xa0', ' '))
            }
        after = "\n".join(f"{label}: {desc}" for label, desc in symptoms.items() if desc is not None and desc.strip())


    doctor = '''Ao prestar socorro, proteja-se para evitar contato com a substância causadora do dano. O tratamento deve focar em aliviar os sintomas e garantir o suporte das funções vitais, como repor fluidos e eletrólitos, corrigir problemas metabólicos e, se necessário, auxiliar na respiração. Em caso de contato com a pele, evite esfregar a área afetada.'''

    return inhalation,skin,eyes,intake,after,doctor

def generate(Document,data:dict):
    inhalation,skin,eyes,intake,after,doctor = infoGet
    mkSec4(Document, inhalation,skin,eyes,intake,after,doctor)