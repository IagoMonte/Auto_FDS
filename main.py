import Gestis_Scrap
from Header import HeaderGen
from docx import Document
from deep_translator import GoogleTranslator

import ICSC_Scrap

def translate(text: str):
    return GoogleTranslator(source='auto',target='portuguese').translate(text)


Cas = '7654-93-9'

gestisData = Gestis_Scrap.dataGestisByCas(Cas)
if gestisData != [] || :
    icscData = ICSC_Scrap.getDataByCas(Cas)
    print('Data coletada!!')
pass

if __file__ == 'main':
    nome_produto = "Ácido Nítrico"

    doc = HeaderGen(Document(),nome_produto)

    nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
    doc.save(nome_arquivo)
    print(f'Documento \"{nome_arquivo}\" criado com sucesso.')