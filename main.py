import Gestis_Scrap
import Cetesb_Scrap
import ICSC_Scrap
from Header import HeaderGen
from docx import Document
from deep_translator import GoogleTranslator



def translate(text: str):
    return GoogleTranslator(source='auto',target='portuguese').translate(text)


Cas = '7664-93-9'

cetesbData = Cetesb_Scrap.getDataByCas(Cas)
gestisData = Gestis_Scrap.getDataByCas(Cas)
if gestisData != {} or cetesbData != []:
    icscData = ICSC_Scrap.getDataByCas(Cas)
    print('Data coletada!!')
else:
    raise Exception("Error: data not found")

if __file__ == 'main':
    nome_produto = "Ácido Nítrico"

    doc = HeaderGen(Document(),nome_produto)

    nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
    doc.save(nome_arquivo)
    print(f'Documento \"{nome_arquivo}\" criado com sucesso.')