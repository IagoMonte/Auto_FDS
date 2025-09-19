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

import re
from bs4 import BeautifulSoup
from main import getData, translate
import re
from bs4 import BeautifulSoup
from json import loads as loadjs

def extract_property_value(text, prop):
    values = []
    
    if prop == "melting_point":
        matches = re.findall(r"Melting point:\s*([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?", text, flags=re.I)
        for val, purity in matches:
            try:
                val_num = float(val.replace(",", "."))
            except:
                continue
            values.append((val_num, purity if purity else None))
        if not values:
            return "Não disponível"
        # Priorizar pureza 100%, senão maior pureza, senão menor valor
        values.sort(key=lambda x: (-(int(x[1]) if x[1] else 0), x[0]))
        chosen = values[0]
        return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")
    
    if prop == "boiling_point":
        matches = re.findall(r"Boiling Point:\s*(?:ca\.\s*)?([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?", text, flags=re.I)
        for val, purity in matches:
            try:
                val_num = float(val.replace(",", "."))
            except:
                continue
            values.append((val_num, purity if purity else None))
        if not values:
            return "Não disponível"
        # Priorizar pureza 100%, senão maior pureza, senão maior valor
        values.sort(key=lambda x: (-(int(x[1]) if x[1] else 0), -x[0]))
        chosen = values[0]
        return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")
    
    return "Não disponível"

def extrair_dados_dinamico(entradas):
    dados = {
        "physical_state": "Não disponível",
        "color": "Não disponível",
        "odor": "Não disponível",
        "melting_point": "Não disponível",
        "boiling_point": "Não disponível",
        "flammability": "Não disponível",
        "explosive_limit": "Não disponível",
        "flash_point": "Não disponível",
        "auto_ignition_temperature": "Não disponível",
        "decomposition_temperature": "Não disponível",
        "pH": "Não disponível",
        "kinematic_viscosity": "Não disponível",
        "water_solubility": "Não disponível",
        "partition_coefficient": "Não disponível",
        "vapor_pressure": "Não disponível",
        "relative_density": "Não disponível",
        "relative_vapor_density": "Não disponível",
        "particle_characteristics": "Não disponível",
        "OtherInfo": ""
    }

    # --- Normaliza entradas (html, listas, dicts, números soltos) ---
    textos = []
    for e in entradas:
        if isinstance(e, dict) and "text" in e:
            textos.append(e["text"])
        elif isinstance(e, str):  # pode ser HTML
            soup = BeautifulSoup(e, "html.parser")
            textos.append(soup.get_text(" "))
        elif isinstance(e, list):
            for sub in e:
                if isinstance(sub, str):
                    textos.append(sub)
                elif isinstance(sub, list):
                    textos.extend(sub)
                elif isinstance(sub, dict) and "text" in sub:
                    textos.append(sub["text"])
        elif isinstance(e, (int, float)):
            textos.append(str(e))

    texto_total = " ".join(textos)

    # --- Regras dinâmicas: campo → regex ---
    regras = {
    "relative_density": r"(?:Density|Densidade).*?([\d\.,]+ ?g/(?:cm³|ml)|[\d\.,]+ ?a ?\d* ?°C)",
    "vapor_pressure": r"(?:Vapou?r pressure|Press[aã]o do vapor).*?([\d\.,]+ ?(Pa|hPa|kPa|mmHg)|negligible.*?\([\w <>\.=]+\))",
    "water_solubility": r"(?:Solubility.*?water|Solubilidade na [aá]gua).*?(:?miscible|entirely mixable|[\d\.,]+ ?g/(?:l|100ml).*?)",
    "relative_vapor_density": r"(?:Relative vapou?r density|Densidade relativa do g[aá]s).*?([\d\.,]+)",
    "decomposition_temperature": r"(?:Decomposition temperature|Decomp[oó]e).*?([>\-]?\s*[\d\.,]+ ?°C)",
    "pH": r"(?:pH).*?([<>\d\.,]+ ?-? ?\d*\.?\d*)",
    "kinematic_viscosity": r"(?:Viscosity).*?([\d\.,]+ ?mPa\*?s|[\d\.,]+ ?cP)",
    "partition_coefficient": r"(?:partition|Kow|Pow).*?([-\d\.,]+)",
    "color": r"(colourless|colorless|incol[oó]r|amarelo|yellow|marrom|branco|white)",
    "odor": r"(odourless|odorless|inodoro|cheiro.*?|odor.*?)",  
    "physical_state": r"(liquid|solid|gas|powder|solution|líquido|sólido|gasoso|solução|aqueous)"
}

    # --- Melting/Boiling com tratamento especial ---
    dados["melting_point"] = extract_property_value(texto_total, "melting_point")
    dados["boiling_point"] = extract_property_value(texto_total, "boiling_point")

    # --- Aplicar regras para os demais ---
    for campo, padrao in regras.items():
        if dados[campo] != "Não disponível":
            continue  # já preenchido
        match = re.search(padrao, texto_total, flags=re.IGNORECASE)
        if match:
            dados[campo] = match.group(1).strip()

    # --- Detecta inflamabilidade de forma semântica ---
    if re.search(r"non-?combustible|não inflamável|not flammable", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Não inflamável"
    elif re.search(r"flammable|inflamável|combustible", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Inflamável"

    # --- Preenche OtherInfo com termos relevantes ---
    extras = []
    palavras_chave = ["viscous", "hygroscopic", "oxidizing", "ácido", "não volátil", "not volatile", "reacts", "decomposes"]
    for linha in textos:
        if any(x in linha.lower() for x in palavras_chave):
            extras.append(linha.strip())
    if extras:
        dados["OtherInfo"] = "\n".join(set(extras))

    return dados


cas = '7664-93-9' # Sulfurico
#cas = '7647-14-5' # Sal
#cas = '57-13-6'   # Ureia
#cas = '7681-52-9' # Hipo
#cas = '7647-01-0' # HCL

saida = getData(cas)

entrada1,entrada2,entrada3,entrada4 = [],[],[],[]
pass
if saida["cetesb"]:
    entrada1 = saida['cetesb'][7]
if saida['icsc']:
    entrada2 = saida['icsc']['td_list'][32] or []
if saida["gestis"]:
    entrada4 = saida['gestis']['PHYSICAL AND CHEMICAL PROPERTIES'] or []
    entrada3 = saida['gestis']['CHARACTERISATION'] or []


entradas = [entrada1, entrada2, entrada3, entrada4]
saida = translate(extrair_dados_dinamico(entradas))

parts = [p.strip() for p in saida.split(",")]

saida = {}
current_key = None

for part in parts:
    if ":" in part:
        key, value = part.split(":", 1)  # só divide na primeira ocorrência
        current_key = key.strip()
        saida[current_key] = value.strip()
    else:
        # se não houver ":", provavelmente é continuação da chave anterior
        if current_key:
            saida[current_key] += "," + part.strip()


print(f'\n---{cas}---')
for k, v in saida.items():
    print(f"{k}: {v}")
