from utils.data.getData import getData
from utils.docxFormater.header import HeaderGen
from utils.sections import sec1,sec2,sec3


data = getData("7647-01-0")

docm = HeaderGen("teste")

sec1.generate(docm,data)
sec2.generate(docm,data)
sec3.generate(docm,data)

docm.save("teste_docx.docx")