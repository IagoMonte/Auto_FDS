from .cetesbScrap import getDataByCas as cetesbByCas
from .gestisScrap import getDataByCas as gestisByCas
from .icscScrap   import getDataByCas as icscByCas

def getData(Cas: str):
    cetesbData = cetesbByCas(Cas)
    gestisData = gestisByCas(Cas)
    if gestisData != {} or cetesbData != []:
        icscData = icscByCas(Cas)
        print('DATA COLETADA!!')
    data = {
        'CAS'   : Cas,
        'cetesb': cetesbData,
        'icsc'  : icscData,
        'gestis': gestisData
    }
    return data