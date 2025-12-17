from utils.docxFormater.easySections import mkSec9
from utils.translator import translateText
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re

DEFAULT = "Não disponível"

@dataclass
class sec9Info:
    physicalState: str
    color: str
    odor: str
    meltingPoint: str
    boilingPoint: str
    flammability: str
    explosiveLimit: str
    flashPoint: str
    autoIgnitionTemperature: str
    decompositionTemperature: str
    pH: str
    kinematicViscosity: str
    waterSolubility: str
    partitionCoefficient: str
    vaporPressure: str
    relativeDensity: str
    relativeVaporDensity: str
    particleCharacteristics: str
    otherInfo: str

def normalizeInputs(entradas):
    textos = []
    
    for e in entradas:
        if isinstance(e, dict) and "text" in e:
            textos.append(e["text"])
        elif isinstance(e, str):
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
    
    return textos, " ".join(textos)

def extractTemperatureWithPurity(text, tempType):
    if tempType == "melting":
        pattern = r"Melting point:\s*([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?"
        sortKey = lambda x: (-(int(x[1]) if x[1] else 0), x[0])  # Menor valor
    elif tempType == "boiling":
        pattern = r"Boiling Point:\s*(?:ca\.\s*)?([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?"
        sortKey = lambda x: (-(int(x[1]) if x[1] else 0), -x[0])  # Maior valor
    else:
        return DEFAULT
    
    matches = re.findall(pattern, text, flags=re.I)
    values = []
    
    for val, purity in matches:
        try:
            valNum = float(val.replace(",", "."))
            values.append((valNum, purity if purity else None))
        except ValueError:
            continue
    
    if not values:
        return DEFAULT
    
    values.sort(key=sortKey)
    chosen = values[0]
    return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")

def extractByRegex(text, pattern):
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match and match.group(1):
        return match.group(1).strip()
    return DEFAULT

def detectFlammability(text):
    if re.search(r"non-?combustible|não inflamável|not flammable", text, flags=re.IGNORECASE):
        return "Não inflamável"
    elif re.search(r"flammable|inflamável|combustible", text, flags=re.IGNORECASE):
        return "Inflamável"
    return DEFAULT

def extractOtherInfo(textos):
    keywords = [
        "viscous", "viscoso", "hygroscopic", "higroscópico", "deliquescent", 
        "oxidizing", "oxidante", "reducing", "redutor", "corrosive", "corrosivo",
        "inflam", "inflamável", "explosive", "explosivo", "pyrophoric", "pirofórico",
        "ácido", "básico", "alcalino", "caustic", "cáustico",
        "volatile", "evapora", "sublimes", "sublima",
        "reacts", "decomposes", "unstable", "instável", "stable", "estável",
        "insoluble", "insolúvel", "miscible", "miscível", "soluble", "solúvel",
        "reactive", "reativo", "polymerizes", "polimeriza", "incompatible", "incompatível",
        "toxic", "tóxico", "harmful", "nocivo", "irritant", "irritante",
        "transparent", "transparente", "opaque", "opaco", "hazardous", "perigoso"
    ]
    
    extras = []
    for linha in textos:
        if any(kw in linha.lower() for kw in keywords):
            extras.append(linha.strip())
    
    return "\n".join(set(extras)) if extras else DEFAULT

def infoGet(data: dict) -> sec9Info:
    
    entrada1 = data.get('cetesb', [])[7] if data.get('cetesb') and len(data['cetesb']) > 7 else []
    entrada2 = data.get('icsc', {}).get('td_list', [])[32] if data.get('icsc') and 'td_list' in data['icsc'] and len(data['icsc']['td_list']) > 32 else []
    entrada3 = data.get('gestis', {}).get('CHARACTERISATION', []) if data.get('gestis') else []
    entrada4 = data.get('gestis', {}).get('PHYSICAL AND CHEMICAL PROPERTIES', []) if data.get('gestis') else []
    
    textos, textoTotal = normalizeInputs([entrada1, entrada2, entrada3, entrada4])
    
    regexPatterns = {
        "relative_density": r"(?:Density|Densidade|Specific gravity|Gravidade espec[ií]fica|Rel\.? density)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:g/(?:cm³|ml)|kg/l|a\s*\d+\s*°C)?)",
        "vapor_pressure": r"(?:Vapou?r pressure|Press[aã]o do vapor|Tensi[oã]o de vapor)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:Pa|hPa|kPa|mmHg|bar)?(?:\s*@ ?\d+ ?°C)?|negligible|atmospheric)",
        "water_solubility": r"(?:Solubility.*?water|Solubilidade na [aá]gua|Mixable)\s*[:\-]?\s*(miscible|immiscible|insoluble|[\d.,]+\s*g/(?:l|100ml))",
        "relative_vapor_density": r"(?:Relative vapou?r density|Densidade relativa do g[aá]s)\s*[:\-]?\s*([>\-]?\s*[\d.,]+(?:\s*a\s*\d+\s*°C)?)",
        "decomposition_temperature": r"(?:Decomposition temperature|Temperatura de decomposi[cç][aã]o)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*°C)",
        "pH": r"(?:pH)[^a-zA-Z0-9]{0,4}([<>=]*\s*\d{0,2}\.?\,?\d{0,2}\s*(?:to|-|–)?\s*\d*\.?\d*)",
        "kinematic_viscosity": r"(?:Viscosity|Viscosidade|Kinematic viscosity)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*(?:mPa\s?s|cP|mm²/s))",
        "partition_coefficient": r"(?:Partition coefficient|Coeficiente de partilh[aã]o|Kow|LogP)\s*[:\-]?\s*([-\d.,]+)",
        "color": r"\b(colourless|colorless|incol[oó]r|amarelo|yellow|marrom|brown|vermelho|red|verde|green|azul|blue|preto|black|branco|white|cinza|grey|transparente)\b",
        "odor": r"\b(odourless|odorless|inodoro|sem odor|cheiro\s*(?:forte|fraco|caracter[ií]stico)|odor\s*(?:forte|fraco|characteristic|pungent))\b",
        "physical_state": r"\b(liquid|solid|gas|powder|solution|paste|gel|líquido|sólido|gasoso|pó|solução|pasta|gel|cristais?|granules?)\b",
        "flash_point": r"(?:Flash point|Ponto de fulgor|Ponto de inflamação)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*°C)",
        "auto_ignition_temperature": r"(?:Auto-?ignition temperature|Temperatura de autoigni[cç][aã]o)\s*[:\-]?\s*([>\-]?\s*[\d.,]+\s*°C)"
    }
    
    extracted = {}
    for field, pattern in regexPatterns.items():
        extracted[field] = extractByRegex(textoTotal, pattern)
    
    meltingPoint = extractTemperatureWithPurity(textoTotal, "melting")
    boilingPoint = extractTemperatureWithPurity(textoTotal, "boiling")
    
    flammability = detectFlammability(textoTotal)
    
    explosiveLimit = DEFAULT
    
    otherInfo = extractOtherInfo(textos)
    
    return sec9Info(
        physicalState=translateText(extracted["physical_state"]),
        color=translateText(extracted["color"]),
        odor=translateText(extracted["odor"]),
        meltingPoint=meltingPoint,
        boilingPoint=boilingPoint,
        flammability=flammability,
        explosiveLimit=explosiveLimit,
        flashPoint=extracted["flash_point"],
        autoIgnitionTemperature=extracted["auto_ignition_temperature"],
        decompositionTemperature=extracted["decomposition_temperature"],
        pH=extracted["pH"],
        kinematicViscosity=extracted["kinematic_viscosity"],
        waterSolubility=extracted["water_solubility"],
        partitionCoefficient=extracted["partition_coefficient"],
        vaporPressure=extracted["vapor_pressure"],
        relativeDensity=extracted["relative_density"],
        relativeVaporDensity=extracted["relative_vapor_density"],
        particleCharacteristics=DEFAULT,
        otherInfo=translateText(otherInfo)
    )

def generate(document, info: sec9Info):
    mkSec9(
        document,
        info.physicalState,info.color,info.odor,info.meltingPoint,info.boilingPoint,
        info.flammability,info.explosiveLimit,info.flashPoint,info.autoIgnitionTemperature,
        info.decompositionTemperature,info.pH,info.kinematicViscosity,info.waterSolubility,
        info.partitionCoefficient,info.vaporPressure,info.relativeDensity,info.relativeVaporDensity,
        info.particleCharacteristics,info.otherInfo
    )
