from utils.translator import translateText
from utils.docxFormater.easySections import mkSec9
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re

DEFAULT_VALUE = "Não disponível"

@dataclass
class sec9Info:
    physical_state: str
    color: str
    odor: str
    melting_point: str
    boiling_point: str
    flammability: str
    explosive_limit: str
    flash_point: str
    auto_ignition_temperature: str
    decomposition_temperature: str
    pH: str
    kinematic_viscosity: str
    water_solubility: str
    partition_coefficient: str
    vapor_pressure: str
    relative_density: str
    relative_vapor_density: str
    particle_characteristics: str
    other_info: str

# --- Helper: Normalização de Entradas ---
def _normalize_inputs(entradas):
    """Converte diferentes formatos (dict, HTML, list, números) em texto unificado."""
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

# --- Helper: Extração de Melting/Boiling Points com Pureza ---
def _extract_temperature_with_purity(text, temp_type):
    """
    Extrai temperaturas (melting/boiling) considerando pureza.
    Prioriza: pureza 100% > maior pureza > menor/maior valor (depende do tipo).
    """
    if temp_type == "melting":
        pattern = r"Melting point:\s*([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?"
        sort_key = lambda x: (-(int(x[1]) if x[1] else 0), x[0])  # Menor valor
    elif temp_type == "boiling":
        pattern = r"Boiling Point:\s*(?:ca\.\s*)?([\-\d,\.]+)\s*°C(?:.*?(\d+)\s*%)?"
        sort_key = lambda x: (-(int(x[1]) if x[1] else 0), -x[0])  # Maior valor
    else:
        return DEFAULT_VALUE
    
    matches = re.findall(pattern, text, flags=re.I)
    values = []
    
    for val, purity in matches:
        try:
            val_num = float(val.replace(",", "."))
            values.append((val_num, purity if purity else None))
        except ValueError:
            continue
    
    if not values:
        return DEFAULT_VALUE
    
    values.sort(key=sort_key)
    chosen = values[0]
    return f"{chosen[0]} °C" + (f" ({chosen[1]}%)" if chosen[1] else "")

# --- Helper: Extração por Regex com Padrões Dinâmicos ---
def _extract_by_regex(text, pattern):
    """Aplica regex e retorna o primeiro grupo capturado ou valor padrão."""
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match and match.group(1):
        return match.group(1).strip()
    return DEFAULT_VALUE

# --- Helper: Detecção de Inflamabilidade ---
def _detect_flammability(text):
    """Detecta inflamabilidade de forma semântica."""
    if re.search(r"non-?combustible|não inflamável|not flammable", text, flags=re.IGNORECASE):
        return "Não inflamável"
    elif re.search(r"flammable|inflamável|combustible", text, flags=re.IGNORECASE):
        return "Inflamável"
    return DEFAULT_VALUE

# --- Helper: Extração de Informações Adicionais ---
def _extract_other_info(textos):
    """Extrai linhas com palavras-chave relevantes para OtherInfo."""
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
    
    return "\n".join(set(extras)) if extras else DEFAULT_VALUE

# --- Função Principal de Extração ---
def infoGet(data: dict) -> sec9Info:
    """
    Extrai propriedades físico-químicas de múltiplas fontes.
    Fontes: CETESB, ICSC, Gestis
    """
    
    # 1. Coleta de Dados das Fontes
    entrada1 = data.get('cetesb', [])[7] if data.get('cetesb') and len(data['cetesb']) > 7 else []
    entrada2 = data.get('icsc', {}).get('td_list', [])[32] if data.get('icsc') and 'td_list' in data['icsc'] and len(data['icsc']['td_list']) > 32 else []
    entrada3 = data.get('gestis', {}).get('CHARACTERISATION', []) if data.get('gestis') else []
    entrada4 = data.get('gestis', {}).get('PHYSICAL AND CHEMICAL PROPERTIES', []) if data.get('gestis') else []
    
    # 2. Normalização
    textos, texto_total = _normalize_inputs([entrada1, entrada2, entrada3, entrada4])
    
    # 3. Extração com Regex (Padrões Dinâmicos)
    regex_patterns = {
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
    
    # Aplica regex para cada campo
    extracted = {}
    for field, pattern in regex_patterns.items():
        extracted[field] = _extract_by_regex(texto_total, pattern)
    
    # 4. Tratamento Especial: Melting/Boiling Points
    melting_point = _extract_temperature_with_purity(texto_total, "melting")
    boiling_point = _extract_temperature_with_purity(texto_total, "boiling")
    
    # 5. Inflamabilidade
    flammability = _detect_flammability(texto_total)
    
    # 6. Limites Explosivos (placeholder - não havia extração no código original)
    explosive_limit = DEFAULT_VALUE
    
    # 7. Outras Informações
    other_info = _extract_other_info(textos)
    
    # 8. Tradução dos Campos Necessários
    return sec9Info(
        physical_state=translateText(extracted["physical_state"]),
        color=translateText(extracted["color"]),
        odor=translateText(extracted["odor"]),
        melting_point=melting_point,
        boiling_point=boiling_point,
        flammability=flammability,
        explosive_limit=explosive_limit,
        flash_point=extracted["flash_point"],
        auto_ignition_temperature=extracted["auto_ignition_temperature"],
        decomposition_temperature=extracted["decomposition_temperature"],
        pH=extracted["pH"],
        kinematic_viscosity=extracted["kinematic_viscosity"],
        water_solubility=extracted["water_solubility"],
        partition_coefficient=extracted["partition_coefficient"],
        vapor_pressure=extracted["vapor_pressure"],
        relative_density=extracted["relative_density"],
        relative_vapor_density=extracted["relative_vapor_density"],
        particle_characteristics=DEFAULT_VALUE,
        other_info=translateText(other_info)
    )

def generate(document, info: sec9Info):
    mkSec9(
        document,
        info.physical_state,
        info.color,
        info.odor,
        info.melting_point,
        info.boiling_point,
        info.flammability,
        info.explosive_limit,
        info.flash_point,
        info.auto_ignition_temperature,
        info.decomposition_temperature,
        info.pH,
        info.kinematic_viscosity,
        info.water_solubility,
        info.partition_coefficient,
        info.vapor_pressure,
        info.relative_density,
        info.relative_vapor_density,
        info.particle_characteristics,
        info.other_info
    )
