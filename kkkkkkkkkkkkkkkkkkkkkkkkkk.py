import re
import os
import json

def extrair_dados_toxicologicos(arquivo):
    """
    Extrai informações toxicológicas completas do arquivo
    """
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except:
        return None
    
    # Inicializar com "Não disponível"
    dados = {
        "Toxicidade aguda": "Não disponível",
        "Corrosão/irritação à pele": "Não disponível",
        "Lesões oculares graves/irritação ocular": "Não disponível",
        "Sensibilização respiratória ou à pele": "Não disponível",
        "Mutagenicidade em células germinativas": "Não disponível",
        "Carcinogenicidade": "Não disponível",
        "Toxicidade à reprodução": "Não disponível",
        "Toxicidade para órgãos-alvo específicos – exposição única": "Não disponível",
        "Toxicidade para órgãos-alvo específicos – exposição repetida": "Não disponível",
        "Perigo por aspiração": "Não disponível"
    }
    
    # 1. TOXICIDADE AGUDA - procurar LD50, LC50, dados toxicológicos
    toxicidade_aguda = []
    
    # LD50 oral
    ld50_matches = re.findall(r'LD50\s+oral.*?(?:Reference:|$)', conteudo, re.DOTALL | re.IGNORECASE)
    toxicidade_aguda.extend(ld50_matches)
    
    # LC50
    lc50_matches = re.findall(r'LC50.*?(?:Reference:|$)', conteudo, re.DOTALL | re.IGNORECASE)
    toxicidade_aguda.extend(lc50_matches)
    
    # TOXICOLOGICAL DATA section
    tox_data = re.search(r'TOXICOLOGICAL DATA(.+?)(?:ECOTOXICOLOGICAL|SAFE HANDLING|$)', conteudo, re.DOTALL | re.IGNORECASE)
    if tox_data:
        toxicidade_aguda.append(tox_data.group(1).strip())
    
    if toxicidade_aguda:
        dados["Toxicidade aguda"] = " | ".join([t.strip()[:500] for t in toxicidade_aguda if t.strip()])
    
    # 2. CORROSÃO/IRRITAÇÃO À PELE
    pele_patterns = [
        r'(?:Skin corrosion|Corrosão.*?pele|irritation.*?skin).*?(?:\n\n|\Z)',
        r'Corrosion/irritation.*?pele.*?(?:Categoria.*?)(?:\n|$)',
    ]
    for pattern in pele_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Corrosão/irritação à pele"] = match.group(0).strip()[:500]
            break
    
    # 3. LESÕES OCULARES
    ocular_patterns = [
        r'(?:eye damage|Lesões oculares|eye irritation).*?(?:\n\n|\Z)',
        r'Serious eye damage.*?(?:Categoria.*?)(?:\n|$)',
    ]
    for pattern in ocular_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Lesões oculares graves/irritação ocular"] = match.group(0).strip()[:500]
            break
    
    # 4. SENSIBILIZAÇÃO
    sensib_patterns = [
        r'(?:Respiratory sensitization|Sensibilização respiratória).*?(?:\n\n|\Z)',
        r'(?:Skin sensitization|Sensibilização.*?pele).*?(?:\n\n|\Z)',
    ]
    sensibilizacao = []
    for pattern in sensib_patterns:
        matches = re.findall(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        sensibilizacao.extend(matches)
    if sensibilizacao:
        dados["Sensibilização respiratória ou à pele"] = " | ".join([s.strip()[:300] for s in sensibilizacao])
    
    # 5. MUTAGENICIDADE
    mutag_patterns = [
        r'(?:Mutagenicity|Mutagenicidade).*?células germinativas.*?(?:\n\n|\Z)',
        r'Germ cell mutagenicity.*?(?:\n\n|\Z)',
    ]
    for pattern in mutag_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Mutagenicidade em células germinativas"] = match.group(0).strip()[:500]
            break
    
    # 6. CARCINOGENICIDADE
    carcin_patterns = [
        r'Carcinogenicity:.*?(?:\[.*?\]|\n\n)',
        r'Carcinogenicidade.*?(?:\n\n|\Z)',
    ]
    for pattern in carcin_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Carcinogenicidade"] = match.group(0).strip()[:500]
            break
    
    # 7. TOXICIDADE À REPRODUÇÃO
    reprod_patterns = [
        r'Reproductive toxicity:.*?(?:\[.*?\]|\n\n)',
        r'Toxicidade à reprodução.*?(?:\n\n|\Z)',
    ]
    for pattern in reprod_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Toxicidade à reprodução"] = match.group(0).strip()[:500]
            break
    
    # 8. STOT - EXPOSIÇÃO ÚNICA
    stot_single_patterns = [
        r'Specific target organ toxicity.*?single exposure.*?(?:\n\n|\Z)',
        r'Toxicidade para órgãos-alvo específicos.*?exposição única.*?(?:\n\n|\Z)',
    ]
    for pattern in stot_single_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Toxicidade para órgãos-alvo específicos – exposição única"] = match.group(0).strip()[:500]
            break
    
    # 9. STOT - EXPOSIÇÃO REPETIDA
    stot_repeat_patterns = [
        r'Specific target organ toxicity.*?repeated exposure.*?(?:\n\n|\Z)',
        r'Toxicidade para órgãos-alvo específicos.*?exposição repetida.*?(?:\n\n|\Z)',
    ]
    for pattern in stot_repeat_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Toxicidade para órgãos-alvo específicos – exposição repetida"] = match.group(0).strip()[:500]
            break
    
    # 10. PERIGO POR ASPIRAÇÃO
    aspir_patterns = [
        r'Aspiration hazard.*?(?:\n\n|\Z)',
        r'Perigo por aspiração.*?(?:\n\n|\Z)',
    ]
    for pattern in aspir_patterns:
        match = re.search(pattern, conteudo, re.DOTALL | re.IGNORECASE)
        if match:
            dados["Perigo por aspiração"] = match.group(0).strip()[:500]
            break
    
    return dados


# SCRIPT PRINCIPAL
print("=" * 80)
print("EXTRAÇÃO DE INFORMAÇÕES TOXICOLÓGICAS")
print("=" * 80)

arquivos = [
    "7681-52-9DATA.txt",
    "57-13-6DATA.txt", 
    "7647-01-0DATA.txt",
    "7664-93-9DATA.txt",
    "7647-14-5DATA.txt"
]

# Processar cada arquivo
resultados = {}

for arquivo in arquivos:
    if os.path.exists(arquivo):
        print(f"\n{'=' * 80}")
        print(f"PROCESSANDO: {arquivo}")
        print('=' * 80)
        
        dados = extrair_dados_toxicologicos(arquivo)
        
        if dados:
            resultados[arquivo] = dados
            for campo, valor in dados.items():
                print(f"\n{campo}:")
                print(f"  {valor[:200]}..." if len(valor) > 200 else f"  {valor}")
        else:
            print("  ERRO ao processar arquivo")
    else:
        print(f"\nArquivo NÃO ENCONTRADO: {arquivo}")

# Salvar em JSON
with open('dados_toxicologicos.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("EXTRAÇÃO CONCLUÍDA - Dados salvos em 'dados_toxicologicos.json'")
print("=" * 80)
