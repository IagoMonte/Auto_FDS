from utils.data.getData import getData
from utils.docxFormater.header import HeaderGen
from utils.docxFormater import easySections
from utils import sections


data = getData("7647-01-0")

i1 = sections.sec1.infoGet(data)
docm = HeaderGen(i1.ProductName)
easySections.mkSec1(docm,i1.ProductName,i1.Uses,i1.ProviderInfo,i1.Emergency)

i9 = sections.sec9.infoGet(data)
easySections.mkSec9(docm,i9.physicalState,i9.color,i9.odor,
                    i9.meltingPoint,i9.boilingPoint,
                    i9.flammability,i9.explosiveLimit,i9.flashPoint,
                    i9.autoIgnitionTemperature,i9.decompositionTemperature,
                    i9.pH,i9.kinematicViscosity,i9.waterSolubility,
                    i9.partitionCoefficient,i9.vaporPressure,i9.relativeDensity,
                    i9.relativeVaporDensity,i9.particleCharacteristics,i9.otherInfo)
i10 = sections.sec10.getInfo(i9.otherInfo)
print(i10)
docm.save("teste_docx.docx")