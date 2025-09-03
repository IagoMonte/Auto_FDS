import Gestis_Scrap
import Cetesb_Scrap
import ICSC_Scrap
from Header import HeaderGen
from docx import Document
from cerebras.cloud.sdk import Cerebras
import os
from dotenv import load_dotenv
load_dotenv()

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

def translate(text: str):

    completion_create_response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f"Me responda apenas o texto traduzido em Portugues do Brasil: {text}"
        }
    ],
    model="qwen-3-235b-a22b-instruct-2507",
    stream=False,
    max_completion_tokens=2048,
    temperature=0.2,
    top_p=1
    )
    res = completion_create_response
    return res.choices[0].message.content


# def translate(text: str):
#     #return GoogleTranslator(source='auto',target='portuguese').translate(text)
#     return text # traduzindo por fora por enquanto.................
def getData(Cas : str):
    cetesbData = Cetesb_Scrap.getDataByCas(Cas)
    gestisData = Gestis_Scrap.getDataByCas(Cas)
    if gestisData != {} or cetesbData != []:
        icscData = ICSC_Scrap.getDataByCas(Cas)
        print('Data coletada!!')
    else:
        raise Exception("Error: data not found")

    data = {'cetesb': cetesbData,
            'icsc': icscData,
            'gestis': gestisData}
    return data

if __file__ == 'main':
    nome_produto = "Ácido Nítrico"

    doc = HeaderGen(Document(),nome_produto)

    nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
    doc.save(nome_arquivo)
    print(f'Documento \"{nome_arquivo}\" criado com sucesso.')