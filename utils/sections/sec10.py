from utils.docxFormater.easySections import mkSec10
from dataclasses import dataclass
import re, unicodedata

DEFAULT_VALUE = "Não disponível"

@dataclass
class SecTenInfo:
    reactivity: str
    chemical_stability: str
    possibility_of_dangerous_reactions: str
    conditions_to_avoid: str
    incompatible_materials: str
    hazardous_decomposition_products: str

def _normalize_text(text: str) -> str:
    if not text:
        return ""
    text_lower = text.lower()
    text_norm = unicodedata.normalize("NFKD", text_lower)
    return "".join(c for c in text_norm if not unicodedata.combining(c))


def _clean_noise(text: str) -> str:
    if not text:
        return ""
    
    # Remove prefixos truncados
    text = re.sub(r'^[^:]*?ção:\s*', '', text.strip())
    
    # Remove referências específicas
    text = re.sub(r'ver\s+ZVG-Nr\.\s+\d+.*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Referência:\s*\d+.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'Fonte:\s*[\d\s]+$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove seções irrelevantes
    text = re.sub(r'CARACTERIZAÇÃO QUÍMICA:.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'PROPRIEDADES:.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'PONTO DE EBULIÇÃO.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove títulos soltos
    text = re.sub(r'^\s*REAÇÕES PERIGOSAS\s*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'Decomposição térmica:.*?(?=\n|$)', '', text, flags=re.IGNORECASE)
    
    # Remove palavras soltas
    text = re.sub(r'^\s*fortes\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s*$', '', text, flags=re.MULTILINE)
    
    # Remove múltiplas quebras de linha
    text = re.sub(r'\n\s*\n+', '\n', text)
    
    return text.strip()