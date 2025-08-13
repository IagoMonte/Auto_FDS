import requests as rq
from bs4 import BeautifulSoup as bs

def getGestisUrlByCas(CAS):
    res = rq.get(f'https://gestis-api.dguv.de/api/search/en?stoffname=&nummern={CAS}&summenformel=&volltextsuche=&branche=&risikogruppe=&kategorie=&anmerkung=&erweitert=false&exact=false')

    try:    
        return res.json()[0]['zvg_nr']
    except:
        print('Cas not found in Gestis Data Base')
        return []
def clean_html(html_str):
    if not isinstance(html_str, str):
        return html_str
    soup = bs(html_str, "html.parser")
    return soup.get_text(separator=" ", strip=True).replace("\xa0", " ")

def clean_structure(data):
    if isinstance(data, dict):
        return {k: clean_structure(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_structure(item) for item in data]
    elif isinstance(data, str):
        return clean_html(data)
    else:
        return data

def organize_by_chapter(clean_data):
    chapters = {}
    for kapitel in clean_data.get("hauptkapitel", []):
        title = kapitel.get("ueberschrift")
        if not title:
            pass
        title_clean = clean_html(title)
        chapter_content = []
        for sub in kapitel.get("unterkapitel", []):
            sub_clean = clean_structure(sub)
            chapter_content.append(sub_clean)
        chapters[title_clean] = chapter_content
    return chapters

def dataGestisByCas(cas_Number: str):
    gestisDataUrl = f'https://gestis-api.dguv.de/api/article/en/{getGestisUrlByCas(cas_Number)}' 
    headers = {'Authorization': 'Bearer dddiiasjhduuvnnasdkkwUUSHhjaPPKMasd'}

    res = rq.get(gestisDataUrl, headers=headers)

    data = organize_by_chapter(clean_structure(res.json()))
    return data


