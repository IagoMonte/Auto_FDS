from utils.data.getData import getData
from utils.docxFormater.header import HeaderGen
from utils import sections


data = getData("7647-01-0")

docm = HeaderGen("teste")

sections.sec1.generate(docm,data)
sections.sec2.generate(docm,data)
sections.sec3.generate(docm,data)

docm.save("teste_docx.docx")