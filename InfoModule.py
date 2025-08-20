from main import getData

data = getData('7647-14-5')

ProductName = 'Não disponível'
if data['cetesb'][0][1][0] != '':
    ProductName = data['cetesb'][0][1][0]
elif data['gestis']['IDENTIFICATION'] !='':
    text = data['gestis']['IDENTIFICATION'][0].text
    for marker in ["ZVG No:", "CAS No:", "EC No:"]:
        if marker in text:
            text = text.split(marker)[0].strip()
            break
    ProductName =" ".join(text.split()[:2])
elif data['icsc'] != '':
    ProductName = data['icsc']['b_list'][0].text.split(",")[0].strip()
else:
    ProductName = input('Nome do produto')


print(ProductName)