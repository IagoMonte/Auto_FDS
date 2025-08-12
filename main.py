from Header import HeaderGen
from docx import Document
from deep_translator import GoogleTranslator

def translate(text: str):
    return GoogleTranslator(source='auto',target='portuguese').translate(text)


if __file__ == 'main':
    nome_produto = "Ácido Nítrico"

    doc = HeaderGen(Document(),nome_produto)

    nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
    doc.save(nome_arquivo)
    print(f'Documento \"{nome_arquivo}\" criado com sucesso.')