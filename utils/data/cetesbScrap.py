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

import requests as rq
from bs4 import BeautifulSoup as bs

def getCetesbByCas(Cas: str):
    res = rq.get('https://produtosquimicos.cetesb.sp.gov.br/Ficha/_Produtos')

    data = res.json()['data']

    for i in data:
        if i[3].strip() == Cas:
            return i[0]

def parseCetesbHtml(content: bytes):
    soup = bs(content, 'html.parser')
    tables = []
    for tbl in soup.select("div.container table"):
        tableData = []
        for row in tbl.select("tr"):
            rowData = []
            for cell in row.select("td, th"):
                rowData.append(cell.get_text(strip=True))
            if rowData:
                tableData.append(rowData)
        if tableData:
            tables.append(tableData)
    return tables

def getDataByCas(Cas: str): 
    CetesbRes = rq.get(f'https://produtosquimicos.cetesb.sp.gov.br/ficha/produto/{getCetesbByCas(Cas)}')
    CetesbData = parseCetesbHtml(CetesbRes.content)
    return CetesbData