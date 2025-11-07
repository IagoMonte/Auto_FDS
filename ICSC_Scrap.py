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


def getUrlByCAS(CasNumber: str) -> str:
    url = f'https://www.inchem.org/lucidworks-solr-api/?locale=en&echoParams=none&wt=json&json.nl=arrarr&fl=Title_s%2CShortSummary_t%2CURL_s&sort=score%20desc&start=0&rows=10&q={CasNumber}%20ICSC&facet.limit=-1'

    res = rq.get(url).json()

    docURL = res['response']['docs'][0]['URL_s']

    return docURL

def getDataByCas(Cas: str):
    
    icscUrl = getUrlByCAS(Cas)

    resIcsc = rq.get(icscUrl)

    icscSoup = bs(resIcsc.content, 'html.parser')

    data = {
        "b_list": icscSoup.select('b'),
        "p_list": icscSoup.select('p'),
        "td_list": icscSoup.select('td'),
        "strong_list": icscSoup.select('strong')
    }
    

    return data