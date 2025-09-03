from re import A
from Header import HeaderGen
from docx import Document
from Section import mkSec1, mkSec10, mkSec12, mkSec13, mkSec14, mkSec15, mkSec16, mkSec2, mkSec3, mkSec4, mkSec5, mkSec6, mkSec7, mkSec8, mkSec9, mksec11

doc = HeaderGen(Document(),'Ácido Sulfúrico')


ProductName = 'Ácido Sulfúrico'
Uses = 'Utilizado nas indústrias para fabricação de ácidos, fertilizantes, refino de petróleo e outros.'
ProviderInfo ='''
PORTUGAL QUÍMICA LTDA.

Endereço: Av. Marcelo Zanarotti, 465 - Distrito Industrial - Dumont/SP - Brasil - Cep: 14120-000
Telefone: +55 16 3844-0999
E-mail: portugal@portugalquimica.com.br
''' 
Emergency = 'SUATRANS - 0800-707-7022'

mkSec1(doc,ProductName,Uses,ProviderInfo,Emergency)

Classfication='''Corrosivo para os metais - Categoria 1;
Toxicidade aguda - Oral - Categoria 5;
Corrosão/irritação da pele - Categoria 1A;
Lesões oculares graves/irritação ocular - Categoria 1;
Toxicidade para órgãos-alvo específicos - Exposição única - Categoria 3 - Respiratório;
Perigoso ao ambiente aquático - Agudo - Categoria 3.'''
ClassSystem = '''Norma ABNT-NBR 14725-2023.\nSistema Globalmente Harmonizado para a Classificação e Rotulagem de Produtos Químicos, ONU.'''
OtherDangerous= '''Não são conhecidos outros perigos do produto.'''
PictoPath = './src/Pictogram.png'
pictoWidth = 4 #inches
pictoHeight = 2 #inches
warningWord = 'PERIGO'
warningPhrases = '''H290 Pode ser corrosivo para os metais.
H303 Pode ser nocivo se ingerido.
H314 Provoca queimaduras graves à pele e lesões oculares graves.
H335 Pode provocar irritação das vias respiratórias.
H402 Nocivo para os organismos aquáticos.'''
worryPhrases= '''PREVENÇÃO:
P234 Conserve somente na embalagem original.
P260 Não inale poeiras/fumos/gases/névoas/vapores/aerossóis.
P261 Evite inalar poeiras/fumos/gases/névoas/vapores/aerossóis.
P264 Lave as mãos cuidadosamente após o manuseio.
P271 Utilize apenas ao ar livre ou em locais bem ventilados.
P273 Evite a liberação para o meio ambiente.
P280 Use luvas de proteção, roupa de proteção, proteção ocular, proteção facial e proteção
auricular.

RESPOSTA À EMERGÊNCIA:
P301 + P312 EM CASO DE INGESTÃO: Em caso de mal-estar, contate um CENTRO DE INFORMAÇÃO TOXICOLÓGICA ou médico.
P301 + P330 + P331 EM CASO DE INGESTÃO: Enxague a boca. NÃO provoque vômito. P303 + P361 + P353 EM CASO DE CONTATO COM A PELE (ou com cabelo): Retire imediatamente toda a roupa contaminada. Enxague a pele com água ou tome uma ducha. P304 + P340 EM CASO DE INALAÇÃO: Remova a pessoa para local ventilado e a mantenha em repouso em uma posição que não dificulte a respiração. P305 + P351 + P338 EM CASO DE CONTATO COM OS OLHOS: Enxague cuidadosamente com água durante vários minutos. No caso de uso de lentes de contatos, remova-as, se for fácil. Continue enxaguando. P310 Contate imediatamente um CENTRO DE INFORMAÇÃO TOXICOLÓGICA ou médico. P312 Em caso de mal-estar, contate um CENTRO DE INFORMAÇÃO TOXICOLÓGICA ou médico. P321 Tratamento específico. P363 Lave a roupa contaminada antes de usá-la novamente. P390 Absorva o produto derramado, a fim de evitar danos materiais.

ARMAZENAMENTO:
P403 + P233 Armazene em local bem ventilado. Mantenha o recipiente hermeticamente fechado.
P405 Armazene em local fechado à chave.
P406 Armazene em um recipiente resistente à corrosão com um revestimento interno resistente.

DISPOSIÇÃO:
P501 Descarte o conteúdo e o recipiente em conformidade com as regulamentações locais.'''

mkSec2(doc,Classfication,ClassSystem,OtherDangerous,
       PictoPath,pictoWidth,pictoHeight,warningWord,
       warningPhrases,worryPhrases)

subOrMix = 'SUBSTÂNCIA'
synonym = 'Hidrogenossulfato; Óleo de vitriolo.'
chemID = 'Ácido sulfúrico.'
cas = '7664-93-9'
impure = 'Não apresenta impurezas que contribuam para o perigo.'

mkSec3(doc,subOrMix,chemID,synonym,cas,impure)

inhalation = '''Remova a vítima para local ventilado e a mantenha em repouso numa posição que não dificulte a respiração. Caso sinta indisposição, contate um CENTRO DE INFORMAÇÃO TOXICOLÓGICA ou um médico. Leve este documento'''
skin = '''Lave imediatamente a pele exposta com quantidade suficiente de água para remoção do material. Retire as roupas ou acessórios contaminados. Em caso de contato menor com a pele, evite espalhar o produto em áreas não, atingidas. Consulte um médico. Leve este documento.'''
eyes = '''Lave imediatamente os olhos com quantidade suficiente de água, mantendo as pálpebras abertas, durante vários minutos. No caso de uso de lentes de contato, remova-as, se for fácil e enxague novamente. Consulte um médico. Leve este documento.'''
intake ='''Não induza o vômito. Nunca forneça algo por via oral a uma pessoa inconsciente. Lave a boca da vítima com água em abundância. Consulte imediatamente um médico. Leve este documento.'''
after = '''Provoca queimaduras graves à pele com dor, formação de bolhas e descamação. Provoca lesões oculares graves com queimadura, lacrimejamento e dor. Pode ser nocivo se ingerido. Pode provocar irritação das vias respiratórias, podendo ocasionar espirros e tosse.'''
doctor = '''Evite contato com o produto ao socorrer a vítima. Se necessário, o tratamento sintomático deve compreender, sobretudo, medidas de suporte como correção de distúrbios hidroeletrolíticos, metabólicos, além de assistência respiratória. Em caso de contato com a pele não friccione o local atingido'''

mkSec4(doc, inhalation,skin,eyes,intake,after,doctor)

extinction = '''Adequados: dióxido de carbono (CO2), espuma e pó químico seco.\nInadequados: qualquer forma de água.'''
EspDangerous = '''A combustão do produto químico ou de sua embalagem pode formar gases irritantes e tóxicos como monóxido e dióxido de carbono e óxidos de enxofre.'''
firefighters = '''Equipamento de proteção respiratória do tipo autônomo (SCBA) com pressão positiva e vestuário protetor completo. Contêineres e tanques envolvidos no incêndio podem ser resfriados com neblina d'água.'''

mkSec5(doc,extinction,EspDangerous,firefighters)

NonEmergencyPP = '''Não fume. Evite contato com o produto. Caso necessário, utilize equipamento de proteção individual conforme descrito na seção 8.'''
EmergencyPP = '''Isole o vazamento de fontes de ignição preventivamente.'''
environment = '''Evite que o produto derramado atinja cursos d'água e rede de esgotos.'''
containmentClean = '''Utilize névoa de água ou espuma supressora de vapor para reduzir a dispersão dos vapores. Utilize barreiras naturais ou de contenção de derrame. Colete o produto derramado e coloque em recipientes próprios. Adsorva o produto remanescente, com areia seca, terra, vermiculite, ou qualquer outro material inerte. Coloque o material adsorvido em recipientes apropriados e removaos para local seguro. Utilize ferramentas que não provoquem faíscas para recolher o material absorvido.'''

mkSec6(doc,NonEmergencyPP,EmergencyPP,environment,containmentClean)

SafeHandling = '''Manuseie em uma área ventilada ou com sistema geral de ventilação/exaustão local. Evite formação de vapores e névoas. Evite exposição ao produto, pois os efeitos podem não ser sentidos de imediato. Utilize equipamento de proteção individual conforme descrito na seção 8. Evite contato com materiais incompatíveis.'''
hygiene = '''Lave as mãos e o rosto cuidadosamente após o manuseio e antes de comer, beber, fumar ou ir ao banheiro. Roupas contaminadas devem ser trocadas e lavadas antes de sua reutilização. Remova a roupa e o equipamento de proteção contaminado antes de entrar nas áreas de alimentação.'''
FireExplosion = '''Não é esperado que o produto apresente perigo de incêndio ou explosão.'''
adqCondition = '''Armazene em local bem ventilado e longe da luz solar e de umidade. Mantenha o recipiente fechado. Não é necessária adição de estabilizantes e antioxidantes para garantir a durabilidade. Este produto pode reagir de forma perigosa com alguns materiais incompatíveis, conforme destacado na Seção 10.\nMantenha afastado de materiais incompatíveis.'''
adqPackage = '''Tanques: aço carbono - ASTM A 283 + revestimento de borracha + tijolo antiácido. Em pequenas quantidades, pode ser armazenado em recipientes de vidro.'''
idqPackage = '''Não são conhecidos materiais inadequados.'''

mkSec7(doc,SafeHandling,hygiene,FireExplosion,adqCondition,adqPackage,idqPackage)

exposure = '''Os valores abaixo são aplicáveis para ambientes de trabalho.
OSHA - PEL - TWA: 1 mg/m³ (29 CFR 1910.1000 Table Z-1) (CFR);
NIOSH - REL - TWA: 1 mg/m³;
ACGIH - TLV - TWA: 0,2 mg/m³ (T).
T: Partículas torácicas;
CFR: Consulte o item mencionado no CFR da OSHA.'''
biology = 'Não estabelecidos.'
otherLimits = 'Não estabelecidos.'
engineeringCtrl = 'Promova ventilação mecânica e sistema de exaustão direta para o meio exterior. Estas medidas auxiliam na redução da exposição ao produto. Manter as concentrações atmosféricas dos constituintes do material abaixo dos limites de exposição ocupacional indicados.'
eyesFace = 'Óculos de segurança contra respingos e capuz com resistência a ácidos líquidos.'
skinBody = 'Sapatos fechados, vestimenta de segurança para proteção de todo o corpo contra respingos de produtos químicos. Vestimenta de proteção química resistente a ácidos líquidos. Calçado de cano longo de PVC. Respirador facial completo de partículas tipo N99 ou tipo P2. Luvas de proteção do tipo borracha butílica. Luvas de proteção de borracha fluorada. Luvas de cano longo para proteção química resistente a ácidos líquidos.'
Breathing = '''Máscara de proteção com filtro contra vapores e névoas. Máscara panorâmica com filtro contra gases ácidos ou multiuso. Em grandes concentrações do produto utilize máscara autônoma.'''
Termic = '''Não apresenta perigos térmicos.'''

mkSec8(doc,exposure,biology,otherLimits,engineeringCtrl,
       eyesFace,skinBody,Breathing,Termic)

physical_state = "Líquido oleoso"
color = "Denso, incolor quando puro e amarelo a marrom-escuro quando impuro"
odor = "Inodoro"
melting_point = "10.3 °C"
boiling_point = "337 °C"
flammability = "Não disponível"
explosive_limit = "Não disponível"
flash_point = "Não disponível"
auto_ignition_temperature = "Não disponível"
decomposition_temperature = "340 °C"
pH = "0.3 a 1.2 (Solução aquosa de 0,1 a 1 N a 25°C)"
kinematic_viscosity = "Não disponível"
water_solubility = "Miscível em água (1000 g/L a 25 °C)"
partition_coefficient = "Não disponível"
vapor_pressure = "< 0.3 mmHg (< 39.9966 Pa) a 25 °C"
relative_density = "Densidade absoluta: 1.8302 g/cm³ a 20 °C"
relative_vapor_density = "3.4 (ar = 1)"
particle_characteristics = "Não disponível"
OtherInfo = '''Viscosidade dinâmica: 21 mPa.s a 25 °C.
pKa = 1,98 (25°C);
Peso molecular: 98,08 g/mol;
Substância altamente higroscópica.'''

mkSec9(doc, physical_state,color,odor,melting_point,boiling_point,
       flammability,explosive_limit,flash_point,auto_ignition_temperature,
       decomposition_temperature,pH,kinematic_viscosity,water_solubility,
       partition_coefficient,vapor_pressure,relative_density,relative_vapor_density,
       particle_characteristics,OtherInfo)

stability = "Produto estável em condições normais de temperatura e pressão."
reactivity = "Acetileno e cloreto de alila podem polimerizar-se violentamente na presença de ácido sulfúrico."
possibility_of_dangerous_reactions = "Reage violentamente com materiais combustíveis, redutores, bases, água e materiais orgânicos e é corrosivo para a maioria dos metais comuns. O produto pode inflamar outros materiais combustíveis e reagir perigosamente ou explosivamente com: pentafluoreto de bromo, tetrafluoreto de cloro, ácido clorossulfônico, ácido clorídrico, ácido fluorídrico, heptafluoreto de iodo, nitrato de mercúrio, trihidroxiamino, fosfato de prata, percloratos, ácido perclórico, fósforo, isocianato de fósforo, butóxido de potássio, cloreto de potássio, permanganato de potássio, permanganato de potássio + cloreto de potássio, óxido de propileno, permanganato de prata, carbonato de sódio, cloreto de sódio e cloreto de zinco."
conditions_to_avoid = "Temperaturas elevadas, fonte de ignição e contato com materiais incompatíveis."
incompatible_materials = "Ácido clorídrico, ácido clorosulfônico, ácido fluorídrico, ácido perclórico, agentes oxidantes, agentes redutores, água, bases, carbonato de sódio, cloratos, cloreto de potássio, cloreto de sódio, cloreto de zinco, fosfato de prata, fósforo, heptafluoreto de iodo, materiais combustíveis, metais, nitratos, óxido de propileno, pentafluoreto de bromo, percloratos, permanganato de potássio, permanganato de prata, substâncias orgânicas e tert-butóxido de potássio."
hazardous_decomposition_products = "A decomposição pode gerar óxidos de enxofre."

mkSec10(doc,stability,reactivity,possibility_of_dangerous_reactions,
        conditions_to_avoid,incompatible_materials,
        hazardous_decomposition_products)

acute_toxicity = '''Pode ser nocivo se ingerido.
DL50 Oral (ratos): 2140 mg/kg.'''
skin_corrosion_irritation = "Provoca lesões oculares graves com queimadura, lacrimejamento e dor."
serious_eye_damage_eye_irritation = "O contato com o produto provoca lesões oculares graves, com danos irreversíveis, vermelhidão, dor e lacrimejamento."
respiratory_skin_sensitization = "Não classificado para sensibilização da pele. Não é esperado que provoque sensibilização respiratória"
germ_cell_mutagenicity = "Não classificado para mutagenicidade em células germinativas. Estudos para mutações genéticas realizadas in vitro em bactérias obtiveram resultados negativos (método de ames)."
carcinogenicity = "Não é esperado que apresente carcinogenicidade."
reproductive_toxicity = "Não é esperado que apresente toxicidade à reprodução."
stot_single_exposure = "Pode provocar irritação das vias respiratórias, podendo ocasionar espirros e tosse."
stot_repeated_exposure = "Não é esperado que apresente toxicidade ao órgão-alvo específico por exposição repetida."
aspiration_hazard = "Não é esperado que apresente perigo por aspiração"

mksec11(doc,acute_toxicity,skin_corrosion_irritation,serious_eye_damage_eye_irritation,
        respiratory_skin_sensitization,germ_cell_mutagenicity,carcinogenicity,
        reproductive_toxicity,stot_single_exposure,stot_repeated_exposure,
        aspiration_hazard)

ecotoxicity = "Nocivo para os organismos aquáticos. CE50 (Daphnia magna, 48 h): > 100 mg/L; CL50 (Lepomis macrochirus, 96 h): 16 - 28 mg/L."
persistence_degradability = "Em função da ausência de dados, espera-se que apresente persistência e não seja rapidamente degradado."
bioaccumulation_potential = "Em função da ausência de dados, não é esperado potencial bioacumulativo em organismos aquáticos."
soil_mobility = "Não determinada."
other_adverse_effects = "Devido ao caráter ácido do produto, pode causar alterações nos compartimentos ambientais, provocando danos aos organismos. Devido ao caráter ácido do produto pode causar alterações nos compartimentos ambientais provocando danos aos organismos."

mkSec12(doc,ecotoxicity,persistence_degradability,bioaccumulation_potential,
        soil_mobility,other_adverse_effects)

product_treatment = "Treatment and disposal must be assessed specifically for each product. Federal, state, and municipal legislation should be consulted, including Law No. 12,305 of August 2, 2010 (National Solid Waste Policy)."
product_leftovers = "Keep leftover product in its original, properly sealed packaging. Disposal should be carried out as established for the product."
used_packaging = "Do not reuse empty packaging.  These may contain product residue and must be kept closed and sent for proper disposal as established for the product."

mkSec13(doc,product_treatment,product_leftovers,used_packaging)

terrestrial= '''ANTT - Agência Nacional de Transportes Terrestres: • Resolução nº 5.998, de 3 de novembro de 2022: Atualiza o Regulamento para o Transporte Rodoviário de Produtos Perigosos, aprova suas Instruções Complementares, e dá outras providências.'''
terrestrial_ONU = '''1830'''
terrestrial_shipping_name='''ÁCIDO SULFÚRICO'''
terrestrial_primary_class = '8'
terrestrial_subsidiary_class = 'N.A.'
terrestrial_risk_number = '80'
terrestrial_packing_group = "II"

hydroviario = '''DPC - Diretoria de Portos e Costas (Transporte em águas brasileiras). Normas de Autoridade Marítima:
• NORMAM 201/DPC: Embarcações Empregadas na Navegação em Mar Aberto.
• NORMAM 202/DPC: Embarcações Empregadas na Navegação Interior.
• NORMAM 321/DPC: Homologação de Material.'''
hydroviario_ONU = '''1830'''
hydroviario_shipping_name = '''SULPHURIC ACID'''
hydroviario_primary_class = '8'
hydroviario_subsidiary_class = 'N.A.'
hydroviario_packing_group = "II"
hydroviario_ems = '''F-A, S-B'''
hydroviario_marine_pollutant = '''O produto é considerado poluente marinho.'''

aereo = '''ANAC - Agência Nacional de Aviação Civil: Resolução nº 714, de 26 de abril de 2023. RBAC
(Regulamento Brasileiro da Aviação Civil) Nº 175:
• Transporte de Artigos Perigosos em Aeronaves Civis.
• IS N° 175-001 - Instrução Suplementar.'''
aereo_ONU = '''1830'''
aereo_shipping_name = '''SULPHURIC ACID'''
aereo_primary_class = '8'
aereo_subsidiary_class = 'N.A.'
aereo_packing_group = "II"

mkSec14(doc,terrestrial,terrestrial_ONU,terrestrial_shipping_name,terrestrial_primary_class,
terrestrial_subsidiary_class,terrestrial_risk_number,terrestrial_packing_group,
hydroviario,hydroviario_ONU,hydroviario_shipping_name,hydroviario_primary_class,
hydroviario_subsidiary_class,hydroviario_packing_group,hydroviario_ems,
hydroviario_marine_pollutant,aereo,aereo_ONU,aereo_shipping_name,
aereo_primary_class,aereo_subsidiary_class,aereo_packing_group)

legislacao = '''Decreto Federal nº 10.088, de 5 de novembro de 2019;
Norma ABNT-NBR 14725;
Norma Regulamentadora nº 26 (Sinalização de segurança), do Ministério do Trabalho e Emprego.'''

mkSec15(doc,legislacao)

disclaimer = 'Esta FDS foi elaborada com base nos atuais conhecimentos sobre o manuseio apropriado do produto e sob as condições normais de uso e de acordo com a recomendação de uso, e conforme descrita e especificada na sua embalagem. Qualquer outra forma de uso do produto que envolva a sua combinação com outros materiais, além de formas de uso diversas daquelas indicadas, são de responsabilidade do usuário. Adverte-se que o manuseio de qualquer substância química requer o conhecimento prévio de seus perigos pelo usuário. No local de trabalho cabe à empresa usuária do produto promover o treinamento de seus colaboradores quanto aos possíveis riscos advindos da exposição ao produto químico.'
subs='''ACGIH - American Conference of Governmental Industrial Hygienists (Conferência Americana de Higienistas Industriais Governamentais);

CAS - Chemical Abstracts Service (Número de registro na Sociedade Americana de Química);

CE50 - Concentração efetiva da substância para 50 % dos indivíduos;

CL50 - Concentração efetiva aou concentração letal da substância para 50 % dos indivíduos;

DL50 - Dose capaz de provocar a morte de 50 % dos animais;

EC - European Community (Comunidade Europeia);

EEC - European Economic Community (Comunidade Econômica Europeia);

IARC - International Agency for Research on Cancer (Agência Internacional de Pesquisa sobre 
o Câncer);

NIOSH - National Institute for Occupational Safety and Health (Instituto Nacional de Segurança e Saúde Ocupacional);

NR - Norma Regulamentadora;

ONU - Organização das Nações Unidas;

OSHA - Occupational Safety & Health Administration (Administração de Segurança e Saúde Ocupacional);

PEL - Permissible Exposure Limit (Limite de exposição permissível);

REL - Recommended Exposure Limit (Limite de exposição recomendado);

TLV - Threshold Limit Value (Valor Limite);

TWA - Time Weighted Average (Média ponderada de tempo).'''
refs ='''ACGIH - AMERICAN CONFERENCE OF GOVERNMENTAL INDUSTRIALS HYGIENISTS. TLVs® and BEIs®: Based on the Documentation of the Threshold Limit Values (TLVs®) for Chemical Substances and Physical Agents & Biological Exposure Indices (BEIs®). Cincinnati-USA, 2023.

BRASIL. MINISTÉRIO DO TRABALHO E EMPREGO (MTE). Norma Regulamentadora (NR) n°15: Atividades e operações insalubres. Brasília, DF. Abr. 2022.

BRASIL. MINISTÉRIO DO TRABALHO E EMPREGO (MTE). Norma Regulamentadora (NR) n°7: Programa de controle médico de saúde ocupacional. Brasília, DF. Jan. 2022.

ECHA - EUROPEAN CHEMICAL AGENCY. Disponível em: < http://echa.europa.eu/web/guest >. Acesso em: mar 2020.

GESTIS - SUBSTANCE DATABASE. Disponível em: <https://gestis-database.dguv.de/>. Acesso em: mar 2020.

GHS - GLOBALLY HARMONIZED SYSTEM OF CLASSIFICATION AND LABELLING OF CHEMICALS. 10th rev. ed. New York and Geneva: United Nations, 2023.

HSDB - HAZARDOUS SUBSTANCES DATA BANK. Disponível em: <http://pubchem.ncbi.nlm.nih.gov/ >. Acesso em: mar 2020.

IARC - INTERNATIONAL AGENCY FOR RESEARCH ON CANCER. Disponível em: <
http://monographs.iarc.fr/ENG/Classification/index.php >. Acesso em: mar 2020.

IPCS - INTERNATIONAL PROGRAMME ON CHEMICAL SAFETY - INCHEM. Disponível em: < http://www.inchem.org/ >. Acesso em: mar 2020.

IUCLID - INTERNATIONAL UNIFORM CHEMICAL INFORMATION DATABASE. [S.l.]: European chemical Bureau. Acesso em: mar 2020.

NIOSH - NATIONAL INSTITUTE OF OCCUPATIONAL AND SAFETY. International Chemical Safety Cards. Disponível em: <
http://www.cdc.gov/niosh/ >. Acesso em: mar 2020.

REACH - REGISTRATION, EVALUATION, AUTHORIZATION AND RESTRICTION OF CHEMICALS. Commission Regulation
(EC) No 1272/2008 of December 2008 amending and repealing Directives 67/548/EEC and 1999/45/EC, and amending
Regulation (EC) No 1907/2006 of the European Parliament and of the Council on the Registration, Evaluation, Authorization
and Restriction of Chemicals. Disponível em: < http://eurlex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2008:353:0001:1355:en:PDF >. Acesso em: mar 2020.

TOXNET - TOXICOLOGY DATA NETWORKING. ChemIDplus Lite. Disponível em: < http://chem.sis.nlm.nih.gov/ >. Acesso em: mar 2020.'''

mkSec16(doc,disclaimer,subs,refs)

doc.save('Section1.docx')
print(f'Documento criado com sucesso.')