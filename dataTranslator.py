import time, asyncio, os, copy, re
from teste2 import getData
from cerebras.cloud.sdk import AsyncCerebras
from dotenv import load_dotenv
from groq import AsyncGroq, RateLimitError

load_dotenv()
groq_client = AsyncGroq(api_key=os.environ.get('GROQ_API_KEY'))   
cerebras_client = AsyncCerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

DELIMITER = "\n<<<SPLIT_HERE>>>\n"
DELIMITER_PATTERN = r"\s*<<<SPLIT_HERE>>>\s*"

BATCH_SIZE = 9  # Começa conservador
MAX_TOKENS_PER_TEXT = 3000  # Textos maiores que isso traduz individualmente

async def translate(text: str):
    """Traduz texto simples, mantendo formatação"""
    print(f"🔄 Traduzindo: {text[:50]}...")  # DEBUG
    try:
        response = await cerebras_client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Traduza para Português do Brasil mantendo EXATAMENTE a mesma formatação, se houver o separador <<<SPLIT_HERE>>> no texto, mantenha-o EXATAMENTE como está. Retorne APENAS o texto traduzido:\n\n{text}"
            }],
            model="qwen-3-235b-a22b-instruct-2507",
            stream=False,
            temperature=0.2,
            top_p=1,
            seed=1234
        )
        result = response.choices[0].message.content
        print(f"✅ Traduzido: {result[:50]}...")  # DEBUG
        return result
    
    except Exception as e:
        print(f"⚠️ Erro Cerebras: {e}, usando Groq fallback")  # DEBUG
        while True:
            try:
                response = await groq_client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": f"Traduza para Português do Brasil mantendo EXATAMENTE a mesma formatação, se houver o separador <<<SPLIT_HERE>>> no texto, mantenha-o EXATAMENTE como está. Retorne APENAS o texto traduzido:\n\n{text}"
                    }],
                    model='moonshotai/kimi-k2-instruct-0905',
                    stream=False,
                    temperature=0.2,
                    top_p=1,
                    seed=1234,
                )
                result = response.choices[0].message.content
                print(f"✅ Traduzido (Groq): {result[:50]}...")  # DEBUG
                return result
            except RateLimitError:
                print("⏳ Rate limit, aguardando 60s...")  # DEBUG
                await asyncio.sleep(60)

async def translate_batch(texts):
    """Traduz múltiplos textos em uma única requisição"""
    if not texts:
        return []
    
    # Concatena textos com delimitador
    combined = DELIMITER.join(texts)
    
    # Traduz tudo de uma vez
    translated_combined = await translate(combined)
    
    # Separa as traduções
    translated_texts = re.split(DELIMITER_PATTERN,translated_combined)
    
    translated_texts = [t.strip() for t in translated_texts if t.strip()]
    # Validação: garante mesmo número de resultados
    if len(translated_texts) != len(texts):
        print(f"⚠️ Split falhou: esperado {len(texts)}, recebido {len(translated_texts)}")
        # Fallback: traduz individualmente
        f"🤦‍♂️ Usando fallback: tradução individual"
        return [await translate(text) for text in texts]
    
    return translated_texts


async def translateData(data):
    """Traduz usando batching inteligente"""
    print(f"\n📊 Estrutura recebida: {list(data.keys())}")
    
    # Separa textos pequenos e grandes
    small_texts = []
    small_positions = []
    large_texts = []
    large_positions = []
    
    for source_key, source_data in data.items():
        if source_key == 'cetesb' and isinstance(source_data, list):
            for idx, item_list in enumerate(source_data):
                if isinstance(item_list, list):
                    for sub_idx, text in enumerate(item_list):
                        if isinstance(text, str) and text.strip():
                            pos = ('cetesb', idx, sub_idx)
                            if len(text) > MAX_TOKENS_PER_TEXT * 4:  # 4 chars ≈ 1 token
                                large_texts.append(text)
                                large_positions.append(pos)
                            else:
                                small_texts.append(text)
                                small_positions.append(pos)
        
        elif source_key == 'icsc' and isinstance(source_data, dict):
            for key, item_list in source_data.items():
                if isinstance(item_list, list):
                    for sub_idx, text in enumerate(item_list):
                        if isinstance(text, str) and text.strip():
                            pos = ('icsc', key, sub_idx)
                            if len(text) > MAX_TOKENS_PER_TEXT * 4:
                                large_texts.append(text)
                                large_positions.append(pos)
                            else:
                                small_texts.append(text)
                                small_positions.append(pos)
        
        elif source_key == 'gestis' and isinstance(source_data, dict):
            for key, item_list in source_data.items():
                if isinstance(item_list, list):
                    for sub_idx, item in enumerate(item_list):
                        if isinstance(item, dict) and 'text' in item:
                            text = item['text']
                            if isinstance(text, str) and text.strip():
                                pos = ('gestis', key, sub_idx, 'text')
                                if len(text) > MAX_TOKENS_PER_TEXT * 4:
                                    large_texts.append(text)
                                    large_positions.append(pos)
                                else:
                                    small_texts.append(text)
                                    small_positions.append(pos)
    
    print(f"📝 Textos pequenos/médios: {len(small_texts)}")
    print(f"📝 Textos grandes (tradução individual): {len(large_texts)}")
    
    # Divide textos pequenos em batches
    small_batches = []
    for i in range(0, len(small_texts), BATCH_SIZE):
        batch = small_texts[i:i + BATCH_SIZE]
        small_batches.append(batch)
    
    print(f"📦 Batches pequenos: {len(small_batches)}")
    print(f"🎯 Total de requisições: {len(small_batches) + len(large_texts)}")
    print(f"🎯 Redução: {len(small_texts) + len(large_texts)} → {len(small_batches) + len(large_texts)}")
    
    # Traduz batches pequenos
    print(f"\n🚀 Traduzindo {len(small_batches)} batches...")
    batch_tasks = [translate_batch(batch) for batch in small_batches]
    batch_results = await asyncio.gather(*batch_tasks)
    
    # Traduz textos grandes individualmente
    print(f"🚀 Traduzindo {len(large_texts)} textos grandes...")
    large_tasks = [translate(text) for text in large_texts]
    large_results = await asyncio.gather(*large_tasks)
    
    # Junta todos os resultados
    all_small_translations = []
    for batch_result in batch_results:
        all_small_translations.extend(batch_result)
    
    all_positions = small_positions + large_positions
    all_translations = all_small_translations + large_results
    
    print(f"✅ {len(all_translations)} textos traduzidos")
    
    # Aplica traduções
    translated_data = copy.deepcopy(data)
    
    for pos, translated in zip(all_positions, all_translations):
        if pos[0] == 'cetesb':
            _, idx, sub_idx = pos
            translated_data['cetesb'][idx][sub_idx] = translated
        elif pos[0] == 'icsc':
            _, key, sub_idx = pos
            translated_data['icsc'][key][sub_idx] = translated
        elif pos[0] == 'gestis':
            _, key, sub_idx, field = pos
            translated_data['gestis'][key][sub_idx][field] = translated
    
    return translated_data



async def main():
    print("🔍 Obtendo dados...")
    data = getData()
    
    print(f"\n📦 Dados obtidos:")
    print(f"   - Tipo: {type(data)}")
    print(f"   - Keys: {list(data.keys()) if isinstance(data, dict) else 'não é dict'}")
    
    if not isinstance(data, dict):
        print("❌ ERRO: getData() não retornou um dicionário!")
        return None
    
    print("\n🌐 Iniciando tradução...")
    translated_data = await translateData(data)
    
    print("\n✅ Tradução concluída!")
    return translated_data


# Executa com debug
if __name__ == "__main__":
    final_data = asyncio.run(main())

    compareData = getData()

    if final_data:
        print("\n" + "="*50)
        print("📊 RESULTADO FINAL:")
        print(f"   CETESB items: {len(final_data.get('cetesb', []))}")
        print(f"   ICSC keys: {list(final_data.get('icsc', {}).keys())}")
        print(f"   GESTIS keys: {list(final_data.get('gestis', {}).keys())}")
        print("="*50)

##usado sem sistea de lotes em 06/11/2025 14:27
# async def translateData(data, translator):
#     """Traduz strings dentro de estruturas aninhadas complexas"""
#     print(f"\n📊 Estrutura recebida: {list(data.keys())}")
    
#     tasks = []
#     positions = []
    
#     for source_key, source_data in data.items():
#         print(f"\n🔍 Processando '{source_key}'...")
        
#         if source_key == 'cetesb' and isinstance(source_data, list):
#             # cetesb é lista de listas
#             for idx, item_list in enumerate(source_data):
#                 if isinstance(item_list, list):
#                     for sub_idx, text in enumerate(item_list):
#                         if isinstance(text, str) and text.strip():
#                             tasks.append(translator(text))
#                             positions.append(('cetesb', idx, sub_idx))
#                             print(f"   ✓ Agendado: cetesb[{idx}][{sub_idx}]")
        
#         elif source_key == 'icsc' and isinstance(source_data, dict):
#             # icsc é dict onde cada valor é uma lista
#             for key, item_list in source_data.items():
#                 if isinstance(item_list, list):
#                     for sub_idx, text in enumerate(item_list):
#                         if isinstance(text, str) and text.strip():
#                             tasks.append(translator(text))
#                             positions.append(('icsc', key, sub_idx))
#                             print(f"   ✓ Agendado: icsc['{key}'][{sub_idx}]")
        
#         elif source_key == 'gestis' and isinstance(source_data, dict):
#             # gestis é dict onde cada valor é uma lista de dicts com 'drnr' e 'text'
#             for key, item_list in source_data.items():
#                 if isinstance(item_list, list):
#                     for sub_idx, item in enumerate(item_list):
#                         # Verifica se é um dict com a chave 'text'
#                         if isinstance(item, dict) and 'text' in item:
#                             text = item['text']
#                             if isinstance(text, str) and text.strip():
#                                 tasks.append(translator(text))
#                                 positions.append(('gestis', key, sub_idx, 'text'))
#                                 print(f"   ✓ Agendado: gestis['{key}'][{sub_idx}]['text']")
    
#     print(f"\n📝 Total de tasks criadas: {len(tasks)}")
    
#     if not tasks:
#         print("❌ ERRO: Nenhuma task foi criada!")
#         return data
    
#     # Traduz tudo em paralelo
#     print(f"\n🚀 Iniciando traduções em paralelo ({len(tasks)} textos)...")
#     results = await asyncio.gather(*tasks)
#     print(f"✅ {len(results)} traduções completadas")
    
#     # Faz deep copy da estrutura original
#     translated_data = copy.deepcopy(data)
    
#     # Preenche com traduções
#     print("\n📝 Aplicando traduções...")
#     for pos, translated in zip(positions, results):
#         if pos[0] == 'cetesb':
#             _, idx, sub_idx = pos
#             translated_data['cetesb'][idx][sub_idx] = translated
            
#         elif pos[0] == 'icsc':
#             _, key, sub_idx = pos
#             translated_data['icsc'][key][sub_idx] = translated
            
#         elif pos[0] == 'gestis':
#             _, key, sub_idx, field = pos
#             # Só traduz o campo 'text', mantém 'drnr' intacto
#             translated_data['gestis'][key][sub_idx][field] = translated
    
#     print("✅ Todas as traduções aplicadas!")
#     return translated_data
