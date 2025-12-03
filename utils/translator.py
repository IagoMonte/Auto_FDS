import asyncio, copy, re,os
from groq import RateLimitError,AsyncGroq, Groq
from dotenv import load_dotenv
from cerebras.cloud.sdk import AsyncCerebras, Cerebras

load_dotenv()
groqClientAsync = AsyncGroq(api_key=os.environ.get('GROQ_API_KEY'))   
cerebrasClientAsync = AsyncCerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))

groqClient = Groq(api_key=os.environ.get('GROQ_API_KEY'))   
cerebrasClient = Cerebras(api_key=os.environ.get("CEREBRAS_API_KEY"))


DELIMITER = "\n<<<SPLIT_HERE>>>\n"
DELIMITER_PATTERN = r"\s*<<<SPLIT_HERE>>>\s*"

BATCH_SIZE = 9
MAX_TOKENS_PER_TEXT = 3000

async def aiTranslate(text: str):
    try:
        response = await cerebrasClientAsync.chat.completions.create(
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
        return result
    
    except Exception as e:
        while True:
            try:
                response = await groqClientAsync.chat.completions.create(
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
                return result
            except RateLimitError:
                await asyncio.sleep(60)

async def batchTranslate(texts):
    if not texts:
        return []

    combined = DELIMITER.join(texts)
    
    translatedCombined = await aiTranslate(combined)
    
    translatedTexts = re.split(DELIMITER_PATTERN,translatedCombined)
    
    translatedTexts = [t.strip() for t in translatedTexts if t.strip()]
    if len(translatedTexts) != len(texts):
        return [await aiTranslate(text) for text in texts]
    
    return translatedTexts

async def translateData(data):
    if not isinstance(data, dict):
        raise NotADirectoryError
             
    smallTexts = []
    smallPositions = []
    largeTexts = []
    largePositions = []
    
    for sourceKey, sourceData in data.items():
        if sourceKey == 'cetesb' and isinstance(sourceData, list):
            for idx, itemList in enumerate(sourceData):
                if isinstance(itemList, list):
                    for subIdx, text in enumerate(itemList):
                        if isinstance(text, str) and text.strip():
                            pos = ('cetesb', idx, subIdx)
                            if len(text) > MAX_TOKENS_PER_TEXT * 4:
                                largeTexts.append(text)
                                largePositions.append(pos)
                            else:
                                smallTexts.append(text)
                                smallPositions.append(pos)
        
        elif sourceKey == 'icsc' and isinstance(sourceData, dict):
            for key, itemList in sourceData.items():
                if isinstance(itemList, list):
                    for subIdx, text in enumerate(itemList):
                        if isinstance(text, str) and text.strip():
                            pos = ('icsc', key, subIdx)
                            if len(text) > MAX_TOKENS_PER_TEXT * 4:
                                largeTexts.append(text)
                                largePositions.append(pos)
                            else:
                                smallTexts.append(text)
                                smallPositions.append(pos)
        
        elif sourceKey == 'gestis' and isinstance(sourceData, dict):
            for key, itemList in sourceData.items():
                if isinstance(itemList, list):
                    for subIdx, item in enumerate(itemList):
                        if isinstance(item, dict) and 'text' in item:
                            text = item['text']
                            if isinstance(text, str) and text.strip():
                                pos = ('gestis', key, subIdx, 'text')
                                if len(text) > MAX_TOKENS_PER_TEXT * 4:
                                    largeTexts.append(text)
                                    largePositions.append(pos)
                                else:
                                    smallTexts.append(text)
                                    smallPositions.append(pos)
    smallBatches = []
    for i in range(0, len(smallTexts), BATCH_SIZE):
        batch = smallTexts[i:i + BATCH_SIZE]
        smallBatches.append(batch)

    batchTasks = [batchTranslate(batch) for batch in smallBatches]
    batchResults = await asyncio.gather(*batchTasks)
    
    largeTasks = [aiTranslate(text) for text in largeTexts]
    largeResults = await asyncio.gather(*largeTasks)
    
    allSmallTranslations = []
    for batchResult in batchResults:
        allSmallTranslations.extend(batchResult)
    
    allPositions = smallPositions + largePositions
    allTranslations = allSmallTranslations + largeResults
    
    translatedData = copy.deepcopy(data)
    
    for pos, translated in zip(allPositions, allTranslations):
        if pos[0] == 'cetesb':
            _, idx, subIdx = pos
            translatedData['cetesb'][idx][subIdx] = translated
        elif pos[0] == 'icsc':
            _, key, subIdx = pos
            translatedData['icsc'][key][subIdx] = translated
        elif pos[0] == 'gestis':
            _, key, subIdx, field = pos
            translatedData['gestis'][key][subIdx][field] = translated
    
    return translatedData

def translateText(text:str):
    try:
        response = cerebrasClient.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Me responda apenas o texto traduzido em Portugues do Brasil: {text}"
            }],
            model="qwen-3-235b-a22b-instruct-2507",
            stream=False,
            temperature=0.2,
            top_p=1,
            seed=1234
        )
        result = response.choices[0].message.content
        return result
    
    except Exception as e:
        response = groqClient.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Me responda apenas o texto traduzido em Portugues do Brasil: {text}"
            }],
            model='moonshotai/kimi-k2-instruct-0905',
            stream=False,
            temperature=0.2,
            top_p=1,
            seed=1234,
        )
        result = response.choices[0].message.content
        return result