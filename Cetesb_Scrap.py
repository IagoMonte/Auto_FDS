import requests as rq
from bs4 import BeautifulSoup as bs

def getCetesbByCas(Cas: str):
    res = rq.get('https://produtosquimicos.cetesb.sp.gov.br/Ficha/_Produtos')

    data = res.json()['data']

    for i in data:
        if i[3] == Cas:
            return i[0]

def parseCetesbHtml(content: bytes):
    """Transforma as tabelas do HTML em um array estruturado"""
    soup = bs(content, 'html.parser')
    tables = []
    for tbl in soup.select("div.container table"):
        table_data = []
        for row in tbl.select("tr"):
            row_data = []
            for cell in row.select("td, th"):
                row_data.append(cell.get_text(strip=True))
            if row_data:
                table_data.append(row_data)
        if table_data:
            tables.append(table_data)
    return tables


def getDataByCas(Cas: str):
    CetesbUrl = f'https://produtosquimicos.cetesb.sp.gov.br/ficha/produto/{getCetesbByCas(Cas)}'

    CetesbRes = rq.get(CetesbUrl)

    CetesbData = parseCetesbHtml(CetesbRes.content)

    return CetesbData

