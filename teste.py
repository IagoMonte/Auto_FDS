from ICSC_Scrap import getDataByCas

cas = '7664-93-9' # Sulfurico
print(getDataByCas(cas)['text_list'][52])
cas = '7647-14-5' # Sal
print(getDataByCas(cas)['text_list'][52])
cas = '57-13-6'   # Ureia
print(getDataByCas(cas)['text_list'][52])
cas = '7681-52-9' # Hipo
print(getDataByCas(cas)['text_list'][52])
cas = '7647-01-0' # HCL
print(getDataByCas(cas)['text_list'][52])