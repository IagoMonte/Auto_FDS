from utils.docxFormater.easySections import mkSec10
<<<<<<< HEAD
import re
import unicodedata
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class sec10Info:
    reactivity: str
    hazardousDecompositionProducts: str
    possibilityOfDangerousReactions: str
    conditionsToAvoid: str
    incompatibleMaterials: str

def normalize(txt: str) -> str:
    if not txt:
        return ""
    txtLower = txt.lower()
    txtNorm = unicodedata.normalize("NFKD", txtLower)
    return "".join(c for c in txtNorm if not unicodedata.combining(c))

def removeSpecifiedFlags(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r'^[^:]*?ção:\s*', '', text.strip())
    text = re.sub(r'ver\s+ZVG-Nr\.\s+\d+.*$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Referência:\s*\d+.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'Fonte:\s*[\d\s]+$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'CARACTERIZAÇÃO QUÍMICA:.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'PROPRIEDADES:.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'PONTO DE EBULIÇÃO.*?(?=\n[A-Z]|\n\n|$)', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'^\s*REAÇÕES PERIGOSAS\s*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r'Decomposição térmica:.*?(?=\n|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^\s*fortes\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def extractIncompatibleMaterials(texto: str) -> List[str]:
    results = []
    textNorm = normalize(texto)
    
    patterns = [
        r'incompativel\s+com\s+([^.]+(?:\.|$))',
        r'a\s+substancia\s+pode\s+reagir\s+perigosamente\s+com\s*:?\s*([^.]+(?:\.|$))',
        r'materiais?\s+incompativeis\s*:?\s*([^.]+(?:\.|$))'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, textNorm, re.IGNORECASE | re.DOTALL)
        for match in matches:
            clean = removeSpecifiedFlags(match)
            if clean and len(clean) > 5:
                results.append(clean)
    
    return results

def extractReactions(texto: str) -> List[str]:
    results = []
    lines = texto.split('\n')
    capturando = False
    blocoAtual = []
    
    for line in lines:
        lineNorm = normalize(line.strip())
        
        if re.search(r'reac[oõ]es\s+(?:quimicas\s+)?perigosas', lineNorm):
            capturando = True
            blocoAtual = [line.strip()]
            continue
        
        elif capturando and re.search(r'^(?:materiais?\s+incompativeis|condic[oõ]es\s+a\s+evitar|caracterizac[aã]o\s+quimica|propriedades)', lineNorm):
            if blocoAtual:
                content = '\n'.join(blocoAtual)
                clean = removeSpecifiedFlags(content)
                if clean and len(clean) > 20:
                    results.append(clean)
            capturando = False
            blocoAtual = []
        
        elif capturando and line.strip():
            blocoAtual.append(line.strip())
    
    if capturando and blocoAtual:
        content = '\n'.join(blocoAtual)
        clean = removeSpecifiedFlags(content)
        if clean and len(clean) > 20:
            results.append(clean)
    
    return results

def extractDecompositionProducts(texto: str) -> List[str]:
    results = []
    textNorm = normalize(texto)
    
    pattern = r'produtos?\s+de\s+decomposic[aã]o\s*:?\s*([^.]*(?:amonia|acido|oxigenio|cloro|hidrogenio)[^.]*\.?)'
    matches = re.findall(pattern, textNorm, re.IGNORECASE | re.DOTALL)
    
    for match in matches:
        clean = removeSpecifiedFlags(match)
        if clean and len(clean) > 5:
            results.append(clean)
    
    return results

def extractAvoidConditions(texto: str) -> List[str]:
    results = []
    textNorm = normalize(texto)
    
    pattern = r'houver\s+uma\s+fonte\s+de\s+ignic[aã]o\s+presente\s*[^.]*'
    matches = re.findall(pattern, textNorm, re.IGNORECASE)
    
    for match in matches:
        clean = removeSpecifiedFlags(match)
        if clean and len(clean) > 10:
            results.append(clean)
    
    return results

def extractReactivity(texto: str) -> List[str]:
    results = []
    textNorm = normalize(texto)
    
    pattern = r'reatividade\s+com\s+materiais\s+comuns\s*:?\s*([^.]+(?:\.|$))'
    matches = re.findall(pattern, textNorm, re.IGNORECASE | re.DOTALL)
    
    for match in matches:
        clean = removeSpecifiedFlags(match)
        if clean and len(clean) > 20:
            results.append(clean)
    
    return results

def extractAll(texto: str) -> Dict[str, List[str]]:
    if not texto or not texto.strip():
        return {
            "Reatividade": [" "],
            "Produtos perigosos da decomposição": [" "],
            "Possibilidade de reações perigosas": [" "],
            "Condições a serem evitadas": [" "],
            "Materiais incompatíveis": [" "]
        }
    
    results = {
        "Reatividade": extractReactivity(texto),
        "Produtos perigosos da decomposição": extractDecompositionProducts(texto),
        "Possibilidade de reações perigosas": extractReactions(texto),
        "Condições a serem evitadas": extractAvoidConditions(texto),
        "Materiais incompatíveis": extractIncompatibleMaterials(texto)
    }
    
    for sec, content in results.items():
        if not content or all(not c.strip() for c in content):
            results[sec] = [" "]
        else:
            unicContent = []
            for conteudo in content:
                if conteudo.strip() and conteudo.strip() not in unicContent:
                    unicContent.append(conteudo.strip())
            results[sec] = unicContent if unicContent else [" "]
    
    return results

def otherInfoSort(Produto: str) -> Dict[str, List[str]]:
    return extractAll(Produto)

def processar_textos_quimicos(textos: List[str], arquivo_saida: str = "saida_secoes_corrigida.txt") -> None:
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for idx, texto in enumerate(textos, 1):
            f.write(f"------- Exemplo {idx} -------\n\n")
            dados = extractAll(texto)
            
            for sec, content in dados.items():
                f.write(f"{sec}:\n")
                for cont in content:
                    if cont == " ":
                        f.write(f"  {cont}\n")
                    else:
                        linesContent = cont.split('\n')
                        for line in linesContent:
                            if line.strip():
                                f.write(f"  {line.strip()}\n")
                f.write("\n")
            f.write("\n")

def getInfo(OtherInfo)->sec10Info:
    other_info_sorted = otherInfoSort(OtherInfo)
    
    reactivity = other_info_sorted['Reatividade'][0] if other_info_sorted['Reatividade'][0].strip() else " "

    hazardous_decomposition_products = other_info_sorted['Produtos perigosos da decomposição'][0] if other_info_sorted['Produtos perigosos da decomposição'][0].strip() else " "

    possibility_of_dangerous_reactions = other_info_sorted['Possibilidade de reações perigosas'][0] if other_info_sorted['Possibilidade de reações perigosas'][0].strip() else " "

    conditions_to_avoid = other_info_sorted['Condições a serem evitadas'][0] if other_info_sorted['Condições a serem evitadas'][0].strip() else " "

    incompatible_materials = other_info_sorted['Materiais incompatíveis'][0] if other_info_sorted['Materiais incompatíveis'][0].strip() else " "

    return sec10Info(reactivity=reactivity,
                     hazardousDecompositionProducts=hazardous_decomposition_products,
                     possibilityOfDangerousReactions=possibility_of_dangerous_reactions,
                     conditionsToAvoid=conditions_to_avoid,
                     incompatibleMaterials=incompatible_materials)

def generate(document, info: sec10Info):
    mkSec10(document,
            "Produto estável em condições normais de temperatura e pressão.",
            info.reactivity,
            info.possibilityOfDangerousReactions,
            info.conditionsToAvoid,
            info.incompatibleMaterials,
            info.hazardousDecompositionProducts)
    
=======
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
>>>>>>> ca09c7c66f8f3af85e17f6f2c17b003e957511eb
