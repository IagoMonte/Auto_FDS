import re
from bs4 import BeautifulSoup


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
    # Densidade relativa / gravidade específica
    "relative_density": r"(?:Density|Densidade|Specific gravity|Gravidade espec[ií]fica|Rel\.? density|SG|Dens\.? relativa?)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:g/(?:cm³|ml)|kg/l|a\s*\d+\s*°C|@ ?\d+ ?°C)?)",

    # Pressão de vapor
    "vapor_pressure": r"(?:Vapou?r pressure|Press[aã]o do vapor|Tensi[oã]o de vapor|P\.? vapor|Pvap)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:Pa|hPa|kPa|mmHg|bar|atm|torr)?( ?@ ?\d+ ?°C)?|negligible.*?\([\w\s<>=.]+\)|atmospheric.* pressure)",

    # Solubilidade em água
    "water_solubility": r"(?:Solubility.*?water|Solubilidade na [aá]gua|Mixable|Mixable with water|Water solubility|Solubilidade em [aá]gua|Solu[ci][aá]vel em [aá]gua)\s*[:\-]?\s*(miscible|immiscible|entirely mixable|completely soluble|slightly soluble|not soluble|insoluble|sparingly soluble|practically insoluble|[\d.,]+\s*g/(?:l|100ml|L|kg).*)",

    # Densidade relativa do vapor
    "relative_vapor_density": r"(?:Relative vapou?r density|Densidade relativa do g[aá]s|Gas density|Densidade do vapor|Dens\.? vapor)\s*[:\-]?\s*([>\-]?\s*[\d.,]+(\s*a\s*\d+\s*°C)?|\(air ?= ?1\))",

    # Temperatura de decomposição
    "decomposition_temperature": r"(?:Decomposition temperature|Temperatura de decomposi[cç][aã]o|Decomp[oó]e|Temp\.? decomp)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*°C)",

    # pH (faixas)
    "pH": r"(?:pH)[^a-zA-Z0-9]{0,4}([<>=]*\s*\d{0,2}\.?\,?\d{0,2}\s*(?:to|-|–)?\s*\d*\.?\d*)",

    # Viscosidade cinemática
    "kinematic_viscosity": r"(?:Viscosity|Viscosidade|Kinematic viscosity|Viscosidade cinem[aá]tica|Visc\.? cinem[aá]tica?)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:mPa\s?s|mPa\.s|cP|mm²/s|centistokes|St|cp))",

    # Coeficiente de partição (Kow, Log Kow, Pow, LogP)
    "partition_coefficient": r"(?:Partition coefficient|Coeficiente de partilh[aã]o|Coeficiente de reparti[cç][aã]o|Kow|Pow|Log ?Kow|LogP|LogP(ow)?)\s*[:\-]?\s*([-\d.,]+)",

    # Cor (mais opções, plurais/invariantes)
    "color": r"\b(colourless|colorless|incol[oó]r(?:es)?|amarelo(?:s)?|yellow|marrom|brown|vermelho(?:s)?|red|verde(?:s)?|green|azul(?:es)?|blue|preto(?:s)?|black|branco(?:s)?|white|cinza|grey|gray|rosado|pink|violeta|violet|roxo|purple|transparente|opaque)\b",

    # Odor
    "odor": r"\b(odourless|odorless|inodoro|sem odor|sem cheiro|cheiro\s*(?:forte|fraco|caracter[ií]stico|pungente)|odor\s*(?:forte|fraco|characteristic|pungent)|cheiro desagrad[aá]vel|odor desagrad[aá]vel)\b",

    # Estado físico (incluir mais variações, combinações e plurais)
    "physical_state": r"\b(liquid|solid|gas|powder|solution|paste|gel|slurry|emulsion|suspension|granules?|pellets?|flakes?|crystals?|líquido(?:s)?|sólido(?:s)?|gasoso|gases|p[oó] em|p[oó]|solução|aqua[so]{2}|aqueous|pasta|gel|lama|emuls[aã]o|suspens[aã]o|gr[aâ]nulos?|pelotas?|flocos?|cristais?|aerossol|vapor|mistura|mixture)\b"
}

    # --- Melting/Boiling com tratamento especial ---
    dados["melting_point"] = extract_property_value(texto_total, "melting_point")
    dados["boiling_point"] = extract_property_value(texto_total, "boiling_point")

    # --- Aplicar regras para os demais ---
    for campo, padrao in regras.items():
        if dados[campo] != "Não disponível":
            continue  # já preenchido
        match = re.search(padrao, texto_total, flags=re.IGNORECASE)
        valor = match.group(1) if (match and match.group(1)) else None
        if valor:
            dados[campo] = valor.strip()
        else:
            dados[campo] = "Não disponível"

    # --- Detecta inflamabilidade de forma semântica ---
    if re.search(r"non-?combustible|não inflamável|not flammable", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Não inflamável"
    elif re.search(r"flammable|inflamável|combustible", texto_total, flags=re.IGNORECASE):
        dados["flammability"] = "Inflamável"

    # --- Preenche OtherInfo com termos relevantes ---
    extras = []
    
    palavras_chave = [
    # físico-químicas gerais
    "viscous", "viscoso", "vítreo", "hygroscopic", "higroscópico", "deliquescent", "deliquescente", 
    "oxidizing", "oxidante", "oxidizing agent", "reducing", "redutor", "reducing agent", "corrosive", "corrosivo", 
    "inflam", "inflamável", "non-flammable", "não inflamável", "sem ponto de inflamação", "flammable", "combust", "combustível", "explosive", "explosivo", "pyrophoric", "pirofórico",
    "ácido", "básico", "alcalino", "alcaline", "caustic", "cáustico", "caústico",
    "não volátil", "not volatile", "volatile", "evapora", "evapora facilmente", "evaporates", "sublimes", "sublima", "sublimação",
    "reacts", "decomposes", "unstable", "instável", "instÁvel em calor", "unstable on heating", "estável", "stable",

    # propriedades de solubilidade/absorção
    "insoluble", "not soluble", "insolúvel", "slightly soluble", "pouco solúvel", "miscible", "miscível", "immiscible", "não miscível",
    "soluble", "solúvel", "sparingly soluble", "absorbs moisture", "absorve umidade", "deliquescent", "deliquescente",
    "absorvente", "absorvent", "absorbs water",

    # estabilidade/reação
    "reactive", "reativo", "polymerizes", "polimeriza", "polymerisable", "polymerizable", "incompatible", "incompatível",
    "oxidant", "oxidizer", "oxidiser", "reducing agent",

    # outras descrições úteis
    "toxic", "tóxico", "harmful", "nocivo", "irritant", "irritante", "allergenic", "alergênico", "inodoro", "sem odor", "odorless", "odourless",
    "colored", "coloured", "colorido", "colored liquid", "líquido colorido", "unstable when heated", "instável ao calor","instável quando aquecido",
    "transparente", "opaque", "opaco", "perigoso", "hazardous", "estável em condições normais", "stable under normal conditions"
]

    for linha in textos:
        if any(x in linha.lower() for x in palavras_chave):
            extras.append(linha.strip())
    if extras:
        dados["OtherInfo"] = "\n".join(set(extras))
        # dados["OtherInfo"] =  re.sub(r'ver\s+ZVG-Nr\.\s+\d+.*$', '', dados["OtherInfo"], flags=re.IGNORECASE)
        # dados["OtherInfo"] = re.sub(r'Referência:\s*\d+.*$', '', dados["OtherInfo"], flags=re.IGNORECASE | re.MULTILINE)
        # dados["OtherInfo"] =  re.sub(r'Fonte:\s*[\d\s]+$', '', dados["OtherInfo"], flags=re.IGNORECASE | re.MULTILINE)
    return dados