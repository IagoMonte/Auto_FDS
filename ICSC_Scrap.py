import requests as rq
from bs4 import BeautifulSoup as bs


def getUrlByCAS(CasNumber: str) -> str:
    url = f'https://www.inchem.org/lucidworks-solr-api/?locale=en&echoParams=none&wt=json&json.nl=arrarr&fl=Title_s%2CShortSummary_t%2CURL_s&sort=score%20desc&start=0&rows=10&q={CasNumber}%20ICSC&facet.limit=-1'

    res = rq.get(url).json()

    docURL = res['response']['docs'][0]['URL_s']

    return docURL

icscUrl = getUrlByCAS('7664-93-9')

resIcsc = rq.get(icscUrl)

icscSoup = bs(resIcsc.content, 'html.parser')

b_list = icscSoup.select('b')
p_list = icscSoup.select('p')
td_list = icscSoup.select('td')

pass