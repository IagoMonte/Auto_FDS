import requests as rq
from bs4 import BeautifulSoup as bs
from lxml import html

def getCetesbByCas(Cas: str):
    res = rq.get('https://produtosquimicos.cetesb.sp.gov.br/Ficha/_Produtos')

    data = res.json()['data']

    for i in data:
        if i[3] == Cas:
            return i[0]


CetesbUrl = f'https://produtosquimicos.cetesb.sp.gov.br/ficha/produto/{getCetesbByCas('7664-93-9')}'

CetesbRes = rq.get(CetesbUrl)


CetesbSoup = bs(CetesbRes.content, 'html.parser')




pass

