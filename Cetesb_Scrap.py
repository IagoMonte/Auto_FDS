import requests as rq

def getCetesbByCas(Cas: str):
    res = rq.get('https://produtosquimicos.cetesb.sp.gov.br/Ficha/_Produtos')

    data = res.json()['data']

    for i in data:
        if i[3] == Cas:
            return i[0]


CetesbUrl = f'https://produtosquimicos.cetesb.sp.gov.br/ficha/produto/{getCetesbByCas('7664-93-9')}'

CetesbData = rq.get(CetesbUrl)





