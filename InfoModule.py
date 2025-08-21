import re
from main import getData, translate
from Header import HeaderGen
from pictograms import class_to_pictograms
from docx import Document
from Section import mkSec2,mkSec1
data = getData('7664-93-9')

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
    if re.search(r'\d{2,7}-\d{2}-\d', 
                 data['gestis']['IDENTIFICATION'][0]['text']
                 ) != re.search(r'\d{2,7}-\d{2}-\d', 
                                data['icsc']['b_list'][2].text):
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
print(Classfication)
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
warningPhrases = 'Não disponível'
worryPhrases ='Não disponível'


doc = HeaderGen(Document(),ProductName)
mkSec1(doc,ProductName,Uses,ProviderInfo,Emergency)
mkSec2(doc,Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases)

nome_arquivo = f'FDS_{ProductName.replace(" ", "_")}.docx'
doc.save(nome_arquivo)