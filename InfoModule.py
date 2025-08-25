import re
from main import getData, translate
from Header import HeaderGen
from pictograms import class_to_pictograms
from docx import Document
from Section import mkSec1,mkSec2,mkSec3


#cas = '7664-93-9' # Sulfurico
#cas = '7647-14-5' # Sal
#cas = '57-13-6'   # Ureia
cas = '7681-52-9' # Hipo
#cas = '7647-01-0' # HCL

data = getData(cas)

ProductName = 'Não disponível'

#Product Name Processing
if data['cetesb'] != []:
    ProductName = data['cetesb'][0][1][0]
elif data['gestis']['IDENTIFICATION'] !='':
    text = data['gestis']['IDENTIFICATION'][0]['text']
    for marker in ["ZVG No:", "CAS No:", "EC No:"]:
        if marker in text:
            text = text.split(marker)[0].strip()
            break
    ProductName =" ".join(text.split()[:2])

    casGestis = re.search(r'\d{2,7}-\d{2}-\d', data['gestis']['IDENTIFICATION'][0]['text']).group(0)
    casICSC = re.search(r'\d{2,7}-\d{2}-\d', data['icsc']['b_list'][2].text).group(0)
    if casGestis != casICSC:
        data['icsc'] = []
elif data['icsc'] != []:
    ProductName = data['icsc']['b_list'][0].text.split(",")[0].strip() 
else:
    ProductName = input('Nome do produto')

ProductName = translate(ProductName)

# Uses Processing
Uses = ''
if Uses == '':
    Uses = 'Este produto químico é formulado para atender a diversas aplicações industriais e laboratoriais.'
if data['cetesb'] != []:
    Uses = data['cetesb'][1][3][0][4::]

#PROVIDERS INFO
ProviderInfo ='''
PORTUGAL QUÍMICA LTDA.

Endereço: Av. Marcelo Zanarotti, 465 - Distrito Industrial - Dumont/SP - Brasil - Cep: 14120-000
Telefone: +55 16 3844-0999
E-mail: portugal@portugalquimica.com.br
''' 
Emergency = 'AMBIPAR - 0800-117-2020'

#Section2 - Classification
Classfication='''Produto não perigoso'''
#gestis
if data['gestis']:
    text = data['gestis']['REGULATIONS'][0]['text']
    match = re.search(r'Classification\s+(.*?)\s+Signal Word', text, re.DOTALL)
    classificationGestis = match.group(1).strip() if match else ""
    classification_clean = re.sub(r'H\d{3}\s*', '\n', classificationGestis)
    lines = [line.strip().rstrip(';') + ';' for line in classification_clean.split('\n') if line.strip()]
    ClassficationGestis = "\n".join(lines)

    if ClassficationGestis != '':
        Classfication = translate(ClassficationGestis)
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
PictoPath = class_to_pictograms(Classfication)
pictoWidth = 4 #inches
pictoHeight = 2 #inches

warningWord = 'Não disponível'

if data['gestis']:
    text = re.search(r'Signal Word\s*"?(\w+)"?', data['gestis']['REGULATIONS'][0]['text'])
    if text:
        text = text.group(1)
        warningWord = translate(text)

if data['cetesb']:
    text = re.search(r'Palavra de advertência(\w+)', data['cetesb'][3][2][0])
    if text:
        text = text.group(1)
        warningWord = text

warningPhrases = 'Não disponível'
if data['gestis']:
    h_phrases = re.split(r'H-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
    if len(h_phrases) > 2:
        phrases = re.findall(r'(H\d+:.*?\.)', h_phrases[1])
        formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
        if formatedPhrases:
            formatedPhrases = "\n".join(formatedPhrases)
            warningPhrases = translate(formatedPhrases)

if data['cetesb']:
    text = re.sub(r'^Frase\(s\) de perigo', '', data['cetesb'][3][3][0])
    phrases = re.findall(r'H\d+\s*-\s*[^H]+', text)
    formatedPhrases = [f.strip() + ";\n" for f in phrases]
    if formatedPhrases:
        warningPhrases = formatedPhrases

worryPhrases ='Não disponível'
if data['gestis']:
    p_phrases = re.split(r'P-phrases', data['gestis']['REGULATIONS'][0]['text'], maxsplit=1)
    if len(h_phrases) > 2:
        phrases = re.findall(r'(P[\d\+]+:.*?\.)', p_phrases[1])
        formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
        if formatedPhrases:
            formatedPhrases = "\n".join(formatedPhrases)
            worryPhrases = translate(formatedPhrases)

if data['cetesb']:
    p_phrases = re.sub(r'^Frase\(s\) de precaução.*?\)', '', data['cetesb'][3][4][0])
    phrases = re.findall(r'(P[\d\+ ]+-.*?\.)', p_phrases)
    formatedPhrases = [f.strip().rstrip('.') + ";\n" for f in phrases]
    if formatedPhrases:
        worryPhrases = "\n".join(formatedPhrases)

#section 3
subOrMix = 'SUBSTÂNCIA'#Always
synonym = 'Não disponível'
if data['icsc']:
    synonym = ";".join(
        translate(content) 
        for i, content in enumerate(data['icsc']['td_list'][2].contents) 
        if i % 2 == 0
        )
if data['cetesb']:
    synonym = data['cetesb'][1][0][0][9::]
    
chemID = ProductName #Always
impure = 'Não apresenta impurezas que contribuam para o perigo.'#Always

doc = HeaderGen(Document(),ProductName)
mkSec1(doc,ProductName,Uses,ProviderInfo,Emergency)
mkSec2(doc,Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases)
mkSec3(doc,subOrMix,chemID,synonym,cas,impure)

nome_arquivo = f'FDS_{ProductName.replace(" ", "_")}.docx'
doc.save(nome_arquivo)