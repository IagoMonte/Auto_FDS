import unicodedata, re
from pathlib import Path
from ast import literal_eval
from bs4 import BeautifulSoup as bs


def parseHtmlTag(inner, k, n, items):
    gt = inner.find(">", k + 1)
    if gt == -1:
        items.append(inner[k:].strip())
        return n
    
    openTag = inner[k:gt+1]
    mtag = re.match(r"<\s*/?\s*([a-zA-Z0-9:_-]+)", openTag)
    tag = mtag.group(1).lower() if mtag else None
    
    if openTag.endswith("/>") or openTag.startswith("</"):
        items.append(openTag)
        return gt + 1
    
    depth = 1
    p = gt + 1
    
    while p < n and depth > 0:
        nx = inner.find("<", p)
        if nx == -1:
            items.append(inner[k:].strip())
            return n
        
        if inner.startswith("<!--", nx):
            nxEnd = inner.find("-->", nx + 4)
            p = nxEnd + 3 if nxEnd != -1 else n
            continue
        
        gt2 = inner.find(">", nx + 1)
        if gt2 == -1:
            items.append(inner[k:].strip())
            return n
        
        tagTxt = inner[nx:gt2+1]
        
        if re.match(rf"<\s*{re.escape(tag)}(\s|>|/)", tagTxt, flags=re.I):
            if not tagTxt.endswith("/>"):
                depth += 1
            p = gt2 + 1
        elif re.match(rf"</\s*{re.escape(tag)}\s*>", tagTxt, flags=re.I):
            depth -= 1
            p = gt2 + 1
        else:
            p = gt2 + 1
        
        if depth == 0:
            items.append(inner[k:p].strip())
            while p < n and inner[p] in " \t\r\n":
                p += 1
            if p < n and inner[p] == ",":
                p += 1
            return p
    
    return p

def saveDataTxt(data: dict):
    filename = f'{data['CAS']} DATA.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(data))

def readNclean(path):
    text = unicodedata.normalize("NFKC", Path(path).read_text(encoding="utf-8", errors="ignore"))
    striped = text.replace("\u00A0", " ").replace("\u202F", " ").replace("\u2007", " ")
    cleaned = "".join(ch for ch in striped if (ch in "\n\r\t" or unicodedata.category(ch)[0] != "C"))
    return cleaned

def html_to_text_list(html_list):
    return [bs(h, "html.parser").get_text(" ", strip=True) for h in html_list]

def extractValueSpanHtml(text, key, expectedOpen):
    m = re.search(rf"['\"]{re.escape(key)}['\"]\s*:\s*{re.escape(expectedOpen)}", text)
    if not m:
        raise KeyError(f"Chave não encontrada: {key}")
    
    i = m.end() - 1
    openCh = text[i]
    closeCh = {'[': ']', '{': '}'}[openCh]
    stack = [openCh]
    start = i
    i += 1
    
    inStr = None
    esc = False
    inComment = False 
    inTag = False
    
    while i < len(text) and stack:
        ch = text[i]
        if inComment:
            inComment = not text.startswith("-->", i)
            i += 3 if text.startswith("-->", i) else 1
            pass
        if inTag:
            inTag = ch != ">"
            i += 1
            pass        
        if inStr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == inStr:
                inStr = None
            i += 1
            pass
        if ch in ("'", '"'):
            inStr = ch
        elif text.startswith("<!--", i):
            inComment = True
            i += 3  
        elif ch == "<":
            inTag = True
        elif ch == openCh or ch in "[{":
            stack.append(ch)
        elif ch == closeCh:
            stack.pop()
        elif ch in "]}":
            top = stack[-1]
            if (top == '[' and ch == ']') or (top == '{' and ch == '}'):
                stack.pop()        
        i += 1
    if stack:
        raise SyntaxError(f"Bloco não fechado para {key}")
    return text[start:i]

def extractHtmlListFromICSCBlock(icscBlock, listKey):
    m = re.search(rf"['\"]{re.escape(listKey)}['\"]\s*:\s*\[", icscBlock)
    if not m:
        return []
    
    i = m.end() - 1
    stack = ['[']
    j = i + 1
    inStr = None
    esc = False
    inComment = False
    inTag = False
    
    while j < len(icscBlock) and stack:
        ch = icscBlock[j]
        
        if inComment:
            inComment = not icscBlock.startswith("-->", j)
            j += 3 if icscBlock.startswith("-->", j) else 1
            continue
        
        if inTag:
            inTag = ch != ">"
            j += 1
            continue
        
        if inStr:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == inStr:
                inStr = None
            j += 1
            continue
        
        if ch in ("'", '"'):
            inStr = ch
        elif icscBlock.startswith("<!--", j):
            inComment = True
            j += 3
        elif ch == "<":
            inTag = True
        elif ch == "[":
            stack.append("[")
        elif ch == "]":
            stack.pop()
        
        j += 1
    
    inner = icscBlock[i+1:j-1]
    items = []
    k = 0
    n = len(inner)
    
    while k < n:
        while k < n and inner[k] in " \t\r\n,":
            k += 1
        if k >= n:
            break
        
        if inner.startswith("<!--", k):
            endc = inner.find("-->", k + 4)
            if endc == -1:
                items.append(inner[k:].strip())
                break
            items.append(inner[k:endc+3])
            k = endc + 3
            continue
        
        if inner[k] == "<":
            k = parseHtmlTag(inner, k, n, items)
            continue
        
        comma = inner.find(",", k)
        if comma == -1:
            items.append(inner[k:].strip())
            break
        items.append(inner[k:comma].strip())
        k = comma + 1
    
    return [it for it in items if it]



def parse_icsc(text):
    icsc_block = extractValueSpanHtml(text, "icsc", "{")
    out = {}
    for key in ("b_list", "p_list", "td_list", "strong_list"):
        out[key] = extractHtmlListFromICSCBlock(icsc_block, key)
    return out

def parse_gestis(text):
    frag = extractValueSpanHtml(text, "gestis", "{")
    return literal_eval(frag)

def parse_cetesb(text):
    frag = extractValueSpanHtml(text, "cetesb", "[")
    return literal_eval(frag)

def textToData(path:str):
    txt = readNclean(path)
    cetesb = parse_cetesb(txt)
    icsc = parse_icsc(txt)
    gestis = parse_gestis(txt)
    
    data = {
        'cetesb' :cetesb,
        'icsc' :icsc,
        'gestis' :gestis
    }
    return data