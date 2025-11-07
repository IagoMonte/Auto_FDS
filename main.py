#           ▄▄▄▄▄▄▄▄▄          
#        ▄▄▀         ▀▄▄       
#      ▄▀               ▀▄     
#    ▄▀                   ▀▄   
#  ▐▀     ▄▄         ▄▄     ▀▌ 
#  ▐    ▐▀  ▀▌     ▐▀  ▀▌    ▌ 
# ▐▀   ▐▀    ▀▌   ▐▀    ▀▌   ▀▌
# ▐    ▐      ▌   ▐      ▌    ▌
# ▐▄                         ▄▌
#  ▐      _____________      ▌ 
#  ▐▄         ▐   ▌          ▌ █  ███   ████   ████  ████  █████      
#   ▀▄        ▐▄ ▄▌        ▄▀  █ █   █ █      █    █ █   █   █        
#     ▀▄       ▀▀▀       ▄▀    █ █████ █   ██ █    █ █   █   █        
#       ▀▄▄           ▄▄▀      █ █   █ █    █ █    █ █   █   █        
#          ▀▄▄▄▄▄▄▄▄▄▀         █ █   █  ████   ████  ████    █        
#                                                 

import Gestis_Scrap
import Cetesb_Scrap
import ICSC_Scrap
from Header import HeaderGen
from docx import Document
from Section import mkSec1
from cerebras.cloud.sdk import Cerebras
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = Cerebras(
    api_key=os.environ.get("CEREBRAS_API_KEY")
)

def translate(text: str):
    if text.strip():
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
        top_p=1,
        seed=1234
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

    filename = f"{Cas}DATA.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(data))

    return data


# nome_produto = "Ácido Nítrico"

# doc = HeaderGen(Document(),nome_produto)

# ProviderInfo ='''
# PORTUGAL QUÍMICA LTDA.

# Endereço: Av. Marcelo Zanarotti, 465 - Distrito Industrial - Dumont/SP - Brasil - Cep: 14120-000
# Telefone: +55 16 3844-0999
# E-mail: portugal@portugalquimica.com.br
# ''' 
# Emergency = 'AMBIPAR - 0800-117-2020'

# mkSec1(doc,nome_produto,'aaaaaaa',ProviderInfo,Emergency)


# nome_arquivo = f'FDS_{nome_produto.replace(" ", "_")}.docx'
# doc.save(nome_arquivo)
# print(f'Documento \"{nome_arquivo}\" criado com sucesso.')