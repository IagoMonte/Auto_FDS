from .docx import addLine, addTitle, addSubTitle, addVersionControl, addPictogram

def mkSec1(Document,ProductName,Uses,ProviderInfo,Emergency):
    addTitle(Document,'1 - IDENTIFICAÇÃO')
    addLine(Document,'Identificação do produto:',ProductName,True)
    addLine(Document,'Usos recomendados:',Uses)
    addLine(Document,'Detalhes do fornecedor:',ProviderInfo,True)
    addLine(Document,'Número do telefone de emergência:',Emergency)

def mkSec2(Document,Classfication,ClassSystem,OtherDangerous,PictoPath,pictoWidth,pictoHeight,warningWord,warningPhrases,worryPhrases):
    addTitle(Document,'2 - IDENTIFICAÇÃO DE PERIGOS')
    addLine(Document,'Classificação da substância ou mistura:',Classfication,True)
    addLine(Document,'Sistema de classificação utilizado:',ClassSystem)
    addLine(Document,'Outros perigos que não resultam em uma classificação:',OtherDangerous,True)
    addSubTitle(Document,'Elementos de rotulagem do GHS, incluindo frases de precaução')
    addLine(Document,'Pictogramas:','',True)
    addPictogram(Document,PictoPath,pictoWidth,pictoHeight)
    addLine(Document,'Palavra de advertência:',warningWord,True)
    addLine(Document,'Frases de perigo:',warningPhrases)
    addLine(Document,'Frases de precaução:',worryPhrases,True)
    
def mkSec3(Document,subOrMix,chemID,synonym,cas,impure):
    addTitle(Document,'3 - COMPOSIÇÃO E INFORMAÇÕES SOBRE OS INGREDIENTES')
    addSubTitle(Document,subOrMix)
    addLine(Document,'Identidade química:',chemID,True)
    addLine(Document,'Sinônimo:',synonym)
    addLine(Document,'Número de registro CAS:',cas,True)
    addLine(Document,'Impurezas que contribuem para o perigo:',impure)
    
def mkSec4(Document,inhalation,skin,eyes,intake,after,doctor):
    addTitle(Document,'4 - MEDIDAS DE PRIMEIROS-SOCORROS')
    addLine(Document,'Inalação:',inhalation,True)
    addLine(Document,'Contato com a pele:',skin)
    addLine(Document,'Contato com os olhos:',eyes,True)
    addLine(Document,'Ingestão:',intake)
    addLine(Document,'Sintomas e efeitos mais importantes, agudos ou tardios:',after,True)
    addLine(Document,'Notas para o médico:',doctor)
    
def mkSec5(Document,extinction,EspDangerous,firefighters):
    addTitle(Document,'5 - MEDIDAS DE COMBATE A INCÊNDIO')
    addLine(Document,'Meios de extinção:',extinction,True)
    addLine(Document,'Perigos específicos da mistura ou substância:',EspDangerous)
    addLine(Document,'Medidas de proteção especiais para a equipe de combate a incêndio:',firefighters,True)

def mkSec6(Document,NonEmergencyPP,EmergencyPP,environment,containmentClean):
    addTitle(Document,'6 - MEDIDAS DE CONTROLE PARA DERRAMAMENTO OU VAZAMENTO')
    addSubTitle(Document,'Precauções pessoais')
    addLine(Document,'Para o pessoal que não faz parte dos serviços de emergência:',NonEmergencyPP,True)
    addLine(Document,'Para pessoal de serviço de emergência:',EmergencyPP)
    addLine(Document,'Precauções ao meio ambiente:',environment,True)
    addLine(Document,'Métodos e materiais para contenção e limpeza:',containmentClean) 

def mkSec7(Document,SafeHandling,hygiene,FireExplosion,adqCondition,adqPackage):
    addTitle(Document,'7- MANUSEIO E ARMAZENAMENTO')
    addSubTitle(Document,'Medidas técnicas apropriadas para o manuseio')
    addLine(Document,'Precauções para manuseio seguro:',SafeHandling,True)
    addLine(Document,'Medidas de higiene:',hygiene)
    addSubTitle(Document,'Condições de armazenamento seguro, incluindo qualquer incompatibilidade')
    addLine(Document,'Prevenção de incêndio e explosão:',FireExplosion,True)
    addLine(Document,'Condições adequadas:',adqCondition)
    addLine(Document,'Métodos e Materiais adequados para embalagem:',adqPackage,True)

def mkSec8(Document,exposure,biology,otherLimits,engineeringCtrl,eyesFace,skinBody,Breathing,Termic):
    addTitle(Document,'8- CONTROLE DE EXPOSIÇÃO E PROTEÇÃO INDIVIDUAL')
    addSubTitle(Document,'Parâmetros de controle')
    addLine(Document,'Limites de exposição ocupacional:',exposure,True)
    addLine(Document,'Indicadores biológicos:',biology)
    addLine(Document,'Outros limites e valores:',otherLimits,True)
    addLine(Document,'Medidas de controle de engenharia:', engineeringCtrl)
    addSubTitle(Document,'Medidas de proteção pessoal')
    addLine(Document,'Proteção dos olhos/face:',eyesFace,True)
    addLine(Document,'Proteção da pele e do corpo:',skinBody)
    addLine(Document,'Proteção respiratória:',Breathing,True)
    addLine(Document,'Perigos térmicos:',Termic)

def mkSec9(Document,physicalState,color,odor,meltingPoint,boilingPoint,flammability,explosiveLimit,
           flashPoint,autoIgnitionTemperature,decompositionTemperature,pH,kinematicViscosity,
           waterSolubility,partitionCoefficient,vaporPressure,relativeDensity,relativeVaporDensity,
           particleCharacteristics,OtherInfo):
    addTitle(Document,'9- PROPRIEDADES FÍSICAS E QUÍMICAS')
    addLine(Document, 'Estado físico:', physicalState, True,Aligment='Start')
    addLine(Document, 'Cor:', color,Aligment='Start')
    addLine(Document, 'Odor e limite de odor:', odor, True,Aligment='Start')
    addLine(Document, 'Ponto de fusão/ponto de congelamento:', meltingPoint,Aligment='Start')
    addLine(Document, 'Ponto de ebulição ou ponto de ebulição inicial e faixa de ebulição:', boilingPoint,True,Aligment='Start')
    addLine(Document, 'Inflamabilidade (sólido; líquidos e gás):', flammability,Aligment='Start')
    addLine(Document, 'Limite inferior/superior de inflamabilidade ou explosividade:', explosiveLimit,True,Aligment='Start')
    addLine(Document, 'Ponto de fulgor:', flashPoint,Aligment='Start')
    addLine(Document, 'Temperatura de autoignição:', autoIgnitionTemperature,True,Aligment='Start')
    addLine(Document, 'Temperatura de decomposição:', decompositionTemperature,Aligment='Start')
    addLine(Document, 'pH:', pH,True,Aligment='Start')
    addLine(Document, 'Viscosidade cinemática:', kinematicViscosity,Aligment='Start')
    addLine(Document, 'Solubilidade:', waterSolubility,True,Aligment='Start')
    addLine(Document, 'Coeficiente de partição - noctanol/água:', partitionCoefficient,Aligment='Start')
    addLine(Document, 'Pressão de vapor:', vaporPressure,True,Aligment='Start')
    addLine(Document, 'Densidade relativa:', relativeDensity,Aligment='Start')
    addLine(Document, 'Densidade de vapor relativa:', relativeVaporDensity,True,Aligment='Start')
    addLine(Document, 'Características das partículas (sólidos):', particleCharacteristics,Aligment='Start')
    addLine(Document, 'Outras informações:', OtherInfo,True,Aligment='Start')

def mkSec10(Document,Stability,reactivity,possibilityDangerousReactions,
conditionsToAvoid,incompatibleMaterials,hazardousDecompositionProducts):
    addTitle(Document,'10 - ESTABILIDADE E REATIVIDADE')
    addLine(Document,'Estabilidade:',Stability,True)
    addLine(Document,'Reatividade:',reactivity)
    addLine(Document,'Possibilidade de reações perigosas:',possibilityDangerousReactions,True)
    addLine(Document,'Condições a serem evitadas:',conditionsToAvoid)
    addLine(Document,'Materiais incompatíveis:',incompatibleMaterials,True)
    addLine(Document,'Produtos perigosos da decomposição:',hazardousDecompositionProducts)

def mksec11(Document,acuteToxicity,skinCorrosionIrritation,seriousEyeDamageEyeIrritation,
respiratorySkinSensitization,germCellMutagenicity,carcinogenicity,reproductiveToxicity,
stotSingleExposure,stotRepeatedExposure,aspirationHazard):
    addTitle(Document,'11 - INFORMAÇÕES TOXICOLÓGICAS')
    addLine(Document,'Toxicidade aguda:',acuteToxicity,True)
    addLine(Document,'Corrosão/irritação à pele:',skinCorrosionIrritation)
    addLine(Document,'Lesões oculares graves/irritação ocular:',seriousEyeDamageEyeIrritation,True)
    addLine(Document,'Sensibilização respiratória ou à pele:',respiratorySkinSensitization)
    addLine(Document,'Mutagenicidade em células germinativas:',germCellMutagenicity,True)
    addLine(Document,'Carcinogenicidade:',carcinogenicity)
    addLine(Document,'Toxicidade à reprodução:',reproductiveToxicity,True)
    addLine(Document,'Toxicidade para órgãos-alvo específicos - exposição única:',stotSingleExposure)
    addLine(Document,'Toxicidade para órgãos-alvo específicos - exposição repetida:',stotRepeatedExposure,True)
    addLine(Document,'Perigo por aspiração:',aspirationHazard)

def mkSec12(Document,ecotoxicity,persistenceDegradability,
            bioaccumulationPotential,soilMobility,otherAdverseEffects):
    addTitle(Document,'12 - INFORMAÇÕES ECOLÓGICAS')
    addSubTitle(Document,'Efeitos ambientais, comportamento e impactos do produto')
    addLine(Document,'Ecotoxicidade:',ecotoxicity,True)
    addLine(Document,'Persistência e degradabilidade:',persistenceDegradability)
    addLine(Document,'Potencial bioacumulativo:',bioaccumulationPotential,True)
    addLine(Document,'Mobilidade no solo:',soilMobility)
    addLine(Document,'Outros efeitos adversos:',otherAdverseEffects,True)

def mkSec13(Document,productTreatment,productLeftovers,usedPackaging):
    addTitle(Document,'13- CONSIDERAÇÕES SOBRE DESTINAÇÃO FINAL')
    addSubTitle(Document,'Métodos recomendados para destinação final')
    addLine(Document,'Produto:',productTreatment,True)
    addLine(Document,'Restos de produtos:',productLeftovers)
    addLine(Document,'Embalagem usada:',usedPackaging,True)

def mkSec14(Document,terrestrial,terrestrialONU,terrestrialShippingName,terrestrialPrimaryClass,
            terrestrialSubsidiaryClass,terrestrialRiskNumber,terrestrialPackingGroup,
            hydroviario,hydroviarioONU,hydroviarioShippingName,hydroviarioPrimaryClass,
            hydroviarioSubsidiaryClass,hydroviarioPackingGroup,hydroviarioEMs,hydroviarioMarinePollutant,
            aereo,aereoONU,aereoShippingName,aereoPrimaryClass,aereoSubsidiaryClass,aereoPackingGroup):
    addTitle(Document,'14 - INFORMAÇÕES SOBRE TRANSPORTE')
    addSubTitle(Document,'Regulamentações nacionais e internacionais')
    addLine(Document,'Terrestre:',terrestrial,True)
    addLine(Document,'Número ONU:',terrestrialONU)
    addLine(Document,'Nome apropriado para embarque:',terrestrialShippingName,True)
    addLine(Document,'Classe ou subclasse de risco principal:',terrestrialPrimaryClass)
    addLine(Document,'Classe ou subclasse de risco subsidiário:',terrestrialSubsidiaryClass,True)
    addLine(Document,'Número de risco:',terrestrialRiskNumber)
    addLine(Document,'Grupo de embalagem:',terrestrialPackingGroup,True)

    addLine(Document,'Hidroviário:', hydroviario)
    addLine(Document,'Número ONU:', hydroviarioONU,True)
    addLine(Document,'Nome apropriado para embarque:', hydroviarioShippingName)
    addLine(Document,'Classe ou subclasse de risco principal:', hydroviarioPrimaryClass,True)
    addLine(Document,'Classe ou subclasse de risco subsidiário:', hydroviarioSubsidiaryClass)
    addLine(Document,'Grupo de embalagem:', hydroviarioPackingGroup,True)
    addLine(Document,'EmS:', hydroviarioEMs)
    addLine(Document,'Poluente marinho:', hydroviarioMarinePollutant,True)

    addLine(Document,'Aéreo:', aereo)
    addLine(Document,'Número ONU:', aereoONU,True)
    addLine(Document,'Nome apropriado para embarque:', aereoShippingName)
    addLine(Document,'Classe ou subclasse de risco principal:', aereoPrimaryClass,True)
    addLine(Document,'Classe ou subclasse de risco subsidiário:', aereoSubsidiaryClass)
    addLine(Document,'Grupo de embalagem:', aereoPackingGroup,True)

def mkSec15(Document,laws):
    addTitle(Document,'15 - INFORMAÇÕES SOBRE REGULAMENTAÇÕES')
    addLine(Document,'Regulamentações específicas para o produto químico:',laws,True)

def mkSec16(Document,disclaimer,subs,refs):
    addTitle(Document,'16 - OUTRAS INFORMAÇÕES')
    addSubTitle(Document,'Informações importantes, mas não especificamente descritas às seções anteriores.')
    addLine(Document,disclaimer,'',True)
    addSubTitle(Document,'Controle de alterações:')
    addVersionControl(Document,'01','28/07/2025','Alteração da seção: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 e 16.')
    addSubTitle(Document,'Legendas e abreviaturas:')
    addLine(Document,subs,'',True, Aligment='Start')
    addSubTitle(Document,'Referências bibliográficas:')
    addLine(Document,refs,'',True, Aligment='Start')