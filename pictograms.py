from PIL import Image
import os

def mergepictograns(pictogram_paths, spacing=10, bg_color=(255, 255, 255)):
    imagens = [Image.open(p).convert("RGBA") for p in pictogram_paths]

    larguras = [img.width for img in imagens]
    alturas = [img.height for img in imagens]

    largura_total = sum(larguras) + spacing * (len(imagens) - 1)
    altura_max = max(alturas)

    final = Image.new("RGBA", (largura_total, altura_max), bg_color + (255,))

    x = 0
    for img in imagens:
        final.paste(img, (x, (altura_max - img.height)//2), mask=img)
        x += img.width + spacing

    return final

def class_to_pictograms(classifications: str):
    mapping = {
        "GHS08": [
            ("Sensibilização respiratória", ["1"]),
            ("Mutagenicidade em células germinativas", ["1A", "1B", "2"]),
            ("Carcinogenicidade", ["1A", "1B", "2"]),
            ("Toxicidade reprodutiva", ["1A", "1B", "2"]),
            ("Toxicidade para órgãos-alvo específicos - Exposição única", ["1", "2"]),
            ("Toxicidade para órgãos-alvo específicos - Exposição repetida", ["1", "2"]),
            ("Perigo de aspiração", ["1", "2"]),
        ],
        "GHS07": [
            ("Toxicidade aguda - Oral", ["4"]),
            ("Toxicidade aguda - Dérmica", ["4"]),
            ("Toxicidade aguda - Inalatória", ["4"]),
            ("Irritação da pele", ["2", "3"]),
            ("Irritação ocular", ["2A"]),
            ("Sensibilização cutânea", ["1"]),
            ("Toxicidade para órgãos-alvo específicos - Exposição única", ["3"]),
        ],
        "GHS06": [
            ("Toxicidade aguda - Oral", ["1", "2", "3"]),
            ("Toxicidade aguda - Dérmica", ["1", "2", "3"]),
            ("Toxicidade aguda - Inalatória", ["1", "2", "3"]),
        ],
        "GHS05": [
            ("Corrosivo para os metais", ["1"]),
            ("Corrosão/irritação da pele", ["1A", "1B", "1C"]),
            ("Lesões oculares graves/irritação ocular", ["1"]),
        ],
        "GHS03": [
            ("Gases oxidantes", ["1"]),
            ("Líquidos oxidantes", ["1", "2", "3"]),
            ("Sólidos oxidantes", ["1", "2", "3"]),
        ],
        "GHS02": [
            ("Gases inflamáveis", ["1"]),
            ("Aerossóis inflamáveis", ["1", "2"]),
            ("Líquidos inflamáveis", ["1", "2", "3", "4"]),
            ("Sólidos inflamáveis", ["1", "2"]),
            ("Substâncias e misturas autorreativas", ["B", "C", "D", "E", "F"]),
            ("Líquidos pirofóricos", ["1"]),
            ("Sólidos pirofóricos", ["1"]),
            ("Substâncias e misturas autoaquecíveis", ["1", "2"]),
            ("Substâncias e misturas que, em contato com a água, emitem gases inflamáveis", ["1", "2", "3"]),
            ("Peróxidos orgânicos", ["B", "C", "D", "E", "F"]),
        ],
        "GHS01": [
            ("Explosivos instáveis", []),
            ("Explosivos", ["1.1", "1.2", "1.3", "1.4", "1.5", "1.6"]),
            ("Substâncias e misturas autorreativas", ["A", "B"]),
            ("Peróxidos orgânicos", ["A", "B"]),
        ],
    }

    pictograms = set()
    lines = [line.strip(" ;.") for line in classifications.splitlines() if line.strip()]

    for line in lines:
        for ghs, rules in mapping.items():
            for hazard, categories in rules:
                if hazard.lower() in line.lower():
                    # Se não tiver categorias, vale sempre
                    if not categories:
                        pictograms.add(ghs)
                    else:
                        for cat in categories:
                            if f"Categoria {cat}" in line or f"- {cat}" in line:
                                pictograms.add(ghs)
    
    result = {ghs: os.path.join('./Pictos', f"{ghs}.png") for ghs in sorted(pictograms)}

    return mergepictograns(result)
