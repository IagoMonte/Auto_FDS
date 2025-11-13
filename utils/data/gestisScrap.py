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

GESTIS_BEARER_TOKEN = 'Bearer dddiiasjhduuvnnasdkkwUUSHhjaPPKMasd'


def getGestisUrlByCas(CAS):
    res = rq.get(f'https://gestis-api.dguv.de/api/search/en?stoffname=&nummern={CAS}&summenformel=&volltextsuche=&branche=&risikogruppe=&kategorie=&anmerkung=&erweitert=false&exact=false')

    try:    
        return res.json()[0]['zvg_nr']
    except Exception:
        print('CAS Não encontrado na DATABASE Gestis')
        return []
        
def cleanHtml(html_str):
    if not isinstance(html_str, str):
        return html_str
    soup = bs(html_str, "html.parser")
    return soup.get_text(separator=" ", strip=True).replace("\xa0", " ")

def cleanStructure(data):
    if isinstance(data, dict):
        return {k: cleanStructure(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [cleanStructure(item) for item in data]
    elif isinstance(data, str):
        return cleanHtml(data)
    else:
        return data

def organizeByChapter(cleaData):
    chapters = {}
    for kapitel in cleaData.get("hauptkapitel", []):
        title = kapitel.get("ueberschrift")
        if not title:
            pass
        titleClean = cleanHtml(title)
        chapterContent = []
        for sub in kapitel.get("unterkapitel", []):
            subClean = cleanStructure(sub)
            chapterContent.append(subClean)
        chapters[titleClean] = chapterContent
    return chapters

def getDataByCas(cas_Number: str):
    gestisDataUrl = f'https://gestis-api.dguv.de/api/article/en/{getGestisUrlByCas(cas_Number)}' 
    headers = {'Authorization': GESTIS_BEARER_TOKEN}

    res = rq.get(gestisDataUrl, headers=headers)

    data = organizeByChapter(cleanStructure(res.json()))
    return data
