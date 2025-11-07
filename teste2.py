from pathlib import Path
from ast import literal_eval
from bs4 import BeautifulSoup
import unicodedata, re

# Leitura e limpeza leve (mantém {}[])
def read_and_clean(path):
    s = Path(path).read_text(encoding="utf-8", errors="ignore")
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00A0", " ").replace("\u202F", " ").replace("\u2007", " ")
    s = "".join(ch for ch in s if (ch in "\n\r\t" or unicodedata.category(ch)[0] != "C"))
    return s

# Extrai o valor textual de 'key': { ... } ou 'key': [ ... ] ignorando TAGS e COMENTÁRIOS HTML
def extract_value_span_html_aware(text, key, expected_open):
    # casa "'key' : {" ou "\"key\" : {"
    m = re.search(rf"['\"]{re.escape(key)}['\"]\s*:\s*{re.escape(expected_open)}", text)
    if not m:
        raise KeyError(f"Chave não encontrada: {key}")
    i = m.end() - 1  # posição do '{' ou '['
    opens = {'[': ']', '{': '}'}
    open_ch = text[i]
    close_ch = opens[open_ch]
    stack = [open_ch]
    start = i
    i += 1

    in_str = None
    esc = False
    in_comment = False  # <!-- ... -->
    in_tag = False      # <tag ...>
    while i < len(text) and stack:
        ch = text[i]
        # Comentário HTML
        if in_comment:
            if text.startswith("-->", i):
                in_comment = False
                i += 3
            else:
                i += 1
            continue
        # Dentro de TAG <...>
        if in_tag:
            if ch == ">":
                in_tag = False
            i += 1
            continue
        # Dentro de string Python
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == in_str:
                in_str = None
            i += 1
            continue
        # Fora de tudo: detectar entradas especiais
        if ch in ("'", '"'):
            in_str = ch
            i += 1
            continue
        if text.startswith("<!--", i):
            in_comment = True
            i += 4
            continue
        if ch == "<":
            in_tag = True
            i += 1
            continue
        # Balanceamento real de { } [ ]
        if ch == open_ch:
            stack.append(ch)
            i += 1
            continue
        if ch == close_ch:
            stack.pop()
            i += 1
            continue
        # Se encontrar outros pares, balanceie também
        if ch in "[{":
            stack.append(ch)
            i += 1
            continue
        if ch in "]}":
            # fecha o topo se combinar
            top = stack[-1]
            if (top == '[' and ch == ']') or (top == '{' and ch == '}'):
                stack.pop()
            i += 1
            continue
        i += 1

    if stack:
        raise SyntaxError(f"Bloco não fechado para {key}")
    end = i  # índice após o fechamento
    return text[start:end]

# CETESB: array sem HTML “nu” => literal_eval direto
def parse_cetesb(text):
    frag = extract_value_span_html_aware(text, "cetesb", "[")
    return literal_eval(frag)

# Extrai uma lista HTML do icsc tratando cada item como nó completo (<p>...</p>, <!--...-->, <b/>)
def extract_html_list_from_icsc_block(icsc_block, list_key):
    m = re.search(rf"['\"]{re.escape(list_key)}['\"]\s*:\s*\[", icsc_block)
    if not m:
        return []
    i = m.end() - 1  # posição do '['
    # Delimitar a lista com o mesmo scanner HTML-aware (apenas [] aqui)
    opens = {'[': ']'}
    stack = ['[']
    j = i + 1
    in_str = None
    esc = False
    in_comment = False
    in_tag = False
    while j < len(icsc_block) and stack:
        ch = icsc_block[j]
        if in_comment:
            if icsc_block.startswith("-->", j):
                in_comment = False
                j += 3
            else:
                j += 1
            continue
        if in_tag:
            if ch == ">":
                in_tag = False
            j += 1
            continue
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == in_str:
                in_str = None
            j += 1
            continue
        if ch in ("'", '"'):
            in_str = ch
            j += 1
            continue
        if icsc_block.startswith("<!--", j):
            in_comment = True
            j += 4
            continue
        if ch == "<":
            in_tag = True
            j += 1
            continue
        if ch == "[":
            stack.append("[")
            j += 1
            continue
        if ch == "]":
            stack.pop()
            j += 1
            continue
        j += 1

    inner = icsc_block[i+1:j-1]  # conteúdo interno da lista

    # Agora varrer itens: iniciar em '<' ou '<!--', capturar nó completo, pular vírgulas entre itens
    items = []
    k = 0
    n = len(inner)
    while k < n:
        # pular espaços e vírgulas
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
            # pegar tag de abertura
            gt = inner.find(">", k + 1)
            if gt == -1:
                items.append(inner[k:].strip())
                break
            open_tag = inner[k:gt+1]
            # nome
            mtag = re.match(r"<\s*/?\s*([a-zA-Z0-9:_-]+)", open_tag)
            tag = mtag.group(1).lower() if mtag else None
            # self-closing ou fechamento
            if open_tag.endswith("/>") or open_tag.startswith("</"):
                items.append(open_tag)
                k = gt + 1
                continue
            # procurar fechamento correspondente
            depth = 1
            p = gt + 1
            while p < n and depth > 0:
                nx = inner.find("<", p)
                if nx == -1:
                    items.append(inner[k:].strip())
                    k = n
                    break
                # comentário
                if inner.startswith("<!--", nx):
                    nx_end = inner.find("-->", nx + 4)
                    p = nx_end + 3 if nx_end != -1 else n
                    continue
                gt2 = inner.find(">", nx + 1)
                if gt2 == -1:
                    items.append(inner[k:].strip())
                    k = n
                    break
                tag_txt = inner[nx:gt2+1]
                # abertura da mesma tag
                if re.match(rf"<\s*{re.escape(tag)}(\s|>|/)", tag_txt, flags=re.I):
                    if tag_txt.endswith("/>"):
                        p = gt2 + 1
                    else:
                        depth += 1
                        p = gt2 + 1
                # fechamento da mesma tag
                elif re.match(rf"</\s*{re.escape(tag)}\s*>", tag_txt, flags=re.I):
                    depth -= 1
                    p = gt2 + 1
                else:
                    p = gt2 + 1
                if depth == 0:
                    items.append(inner[k:p].strip())
                    k = p
                    # consumir vírgula separadora
                    while k < n and inner[k] in " \t\r\n":
                        k += 1
                    if k < n and inner[k] == ",":
                        k += 1
                    break
            continue
        # fallback: caso raro de item não começando com '<'
        comma = inner.find(",", k)
        if comma == -1:
            items.append(inner[k:].strip())
            break
        items.append(inner[k:comma].strip())
        k = comma + 1
    return [it for it in items if it]


def parse_icsc(text):
    icsc_block = extract_value_span_html_aware(text, "icsc", "{")
    out = {}
    for key in ("b_list", "p_list", "td_list", "strong_list"):
        out[key] = extract_html_list_from_icsc_block(icsc_block, key)
    return out


def parse_gestis(text):
    frag = extract_value_span_html_aware(text, "gestis", "{")
    return literal_eval(frag)


def html_to_text_list(html_list):
    return [BeautifulSoup(h, "html.parser").get_text(" ", strip=True) for h in html_list]

def getData():
    # Execução
    txt = read_and_clean("7681-52-9DATA.txt")
    cetesb = parse_cetesb(txt)
    icsc = parse_icsc(txt)
    gestis = parse_gestis(txt)
    
    data = {
        'cetesb' :cetesb,
        'icsc' :icsc,
        'gestis' :gestis
    }
    return data