## SIDEBAR
SB_TITLE = {
    "en": "# Sections",
    "pt-br": "# Seções",
}

SECTIONS = {
    "en": "[Getting Started](#anac-s-uav-database-charting-trends-in-brazilian-unmanned-aviation)",
    "pt-br": "[Introdução](#anac-s-uav-database-charting-trends-in-brazilian-unmanned-aviation)",
}

SB_MENU1 = {
    "en": "[Dataframe metadata](#dataframe-metadata)",
    "pt-br": "[Metadados do dataframe](#dataframe-metadata)",
}

SB_MENU2 = {
    "en": "[Data pre-processing](#data-pre-processing)",
    "pt-br": "[Pré-processamento dos dados](#data-pre-processing)",
}

SB_MENU3 = {
    "en": "[Explanatory analysis](#explanatory-analysis)",
    "pt-br": "[Análise explicativa](#explanatory-analysis)",
}

## TITLE
HEADER = {
    "en": "Charting trends in Brazilian unmanned aviation: ANAC's UAV Database",
    "pt-br": "Explorando as tendências da aviação não-tripulada do Brasil: Banco de dados de VANTs da ANAC",
}

## INTRO
INTRO1 = {
    "en": "The use of UAVs (Unmanned Aerial Vehicles), popularly known as drones, to provide services in Brazil gained popularity in the 2010s. However, the legal framework for their use of airspace is still being developed, as are the systems for registering and regulating these aircraft. SISANT (Unmanned Aircraft System) is a national system that stores data on the owner of the aircraft, also referred to as the operator, as well as the activities for which the drone is employed. The operator is legally responsible for the information provided and is only authorized to operate a UAV in Brazilian territory once it has been properly registered in this system.",
    "pt-br": "A utilização de VANTs (Veículos Aéreos Não Tripulados), mais conhecidos como drones, para prestação de serviços no Brasil ganhou popularidade na década de 2010. No entanto, o arcabouço legal para o uso do espaço aéreo ainda está em desenvolvimento, assim como os sistemas de cadastro e regulamentação dessas aeronaves. O SISANT (Sistema de Aeronaves Não Tripuladas) é um sistema nacional que armazena dados sobre o proprietário da aeronave, também chamado de operador, bem como as atividades para as quais o drone é empregado. O operador é o responsável legal pelas informações prestadas e só está autorizado a operar um VANT em território brasileiro quando ele estiver devidamente cadastrado nesse sistema.",
}

INTRO2 = {
    "en": "This application uses public data updated daily from SISANT, under the management of Brazil's National Civil Aviation Agency (ANAC). The data is available on the [Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/aeronaves-drones-cadastrados) portal and includes the records of unmanned aircraft that comply with [RBAC-E No. 94](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-e-94).",
    "pt-br": "",
}

INTRO3 = {
    "en": "The goal of this project was to study and apply data analysis practices, mainly pre-processing and a bit of explanatory analysis. The cool thing about this application is that the source data is frequently updated, triggering automatic updates to all the graphs and charts.",
    "pt-br": "",
}

## INFO & BULLETS
INFO = {
    "en": "Click on Explanatory Analysis, on the sidebar,if you want to go straight to the data visualization.",
    "pt-br": "Clique em Análise Explicativa, na barra lateral, se quiser ir direto para a visualização dos dados.",
}

CHECK_CODE = {"en": "Check the code :bulb:", "pt-br": "Veja o código :bulb:"}

BLT_FEATURES = {
    "en": ":arrow_right: Features and dataframe information:",
    "pt-br": ":arrow_right: Features e informações do dataframe:",
}

BLT_DDF = {
    "en": ":arrow_right: Pre-processed dataframe:",
    "pt-br": ":arrow_right: Dataframe pré-processado:",
}

INFO2 = {
    "en": "Click on the labels of the legend to hide/unhide the corresponding lines.",
    "pt-br": "Clique nos rótulos da legenda para ocultar/desativar as linhas correspondentes."
}

## METADATA
METADATA = {
    "en": """- `AIRCRAFT_ID`: Aircraft ID code. Follows rules:
    - Recreational use (aircraft models): PR-XXXXXXXXX; 
    - Basic non-recreational use (Class 3 UAV operated in line-of-sight below 400 feet): PP-XXXXXXXXX;
    - Advanced use (Class 2 UAV and other Class 3): PS-XXXXXXXXX;  
    - Note: each X represents a number from 0 to 9.

- `EXPIRATION_DATE`: the date when the two-year validity period expires.  

- `OPERATOR`: Name of the person responsible for operating the drone.

- `CPF/CNPJ`: CPF or CNPJ number of the person responsible for operating the drone.

- `TYPE_OF_USE`:
    - Basic: aircraft models or Class 3 UAV operated exclusively in line-of-sight below 400 feet AGL;
    - Advanced: Class 2 UAV or other Class 3 UAV.

- `MANUFACTURER`: Name of aircraft manufacturer.
  
- `MODEL`: Aircraft model name. 

- `SERIAL_NUMBER`: Aircraft serial number. 
 
- `MAX_WEIGHT_TAKEOFF`: Maximum takeoff weight (numeric, two decimal places, in kilograms).

- `TYPE_OF_ACTIVITY`: 
    - Recreational (aircraft models);
    - Experimental (advanced aircraft intended exclusively for operations with experimental purposes);
    - Other fields of activity as declared by the registrant.
    
_____
""",
    "pt-br": """- `AIRCRAFT_ID`: Código da aeronave. Segue regras:
    - Recreacional (aeromodelos): PR-XXXXXXXXX 
    - Uso não recreativo básico (RPA Classe 3 operada em linha de visada visual abaixo de 400 pés): PP-XXXXXXXXX
    - Uso avançado (RPA Classe 2 e demais Classe 3): PS-XXXXXXXXX  
    - Nota: cada X representa um número de 0 a 9

- `EXPIRATION_DATE`: Data de validade, que é igual a data em que o cadastro foi feito ou renovado mais dois anos  

- `OPERATOR`: Nome do responsável pela operação do drone

- `CPF/CNPJ`: Número do CPF ou do CNPJ do responsável pela operação do drone

- `TYPE_OF_USE`:
    - Basic: aeromodelos ou RPA Classe 3 operada exclusivamente na linha de visada visual abaixo de 400 pés AGL
    - Advanced: RPA Classe 2 ou demais RPA classe 3

- `MANUFACTURER`: Nome do fabricante da aeronave
  
- `MODEL`: Nome do modelo da aeronave 

- `SERIAL_NUMBER`: Número de série da aeronave 
 
- `MAX_WEIGHT_TAKEOFF`: Peso máximo de decolagem, numérico com 2 (duas casas decimais) em kg

- `TYPE_OF_ACTIVITY`: 
    - Recreational (aeromodelos)
    - Experimental (aeronave avançada destinada exclusivamente a operações com propósitos experimentais)
    - Outros ramos de atividade conforme declarado pelo cadastrante
    
_____
""",
}

## DATA PRE-PROCESSING
DPP_SUBHEADER = {"en": "Data pre-processing", "pt-br": "Pré-processamento dos dados"}

DPP_MD1 = {
    "en": """The `AIRCRAFT_ID` feature would be used to index the dataframe at first. However, duplicated values were found and removed. The feature was then tested for values that did not match the digit patterns shown in the metadata. Finally, `AIRCRAFT_ID` was assigned as the dataframe index.""",
    "pt-br": """A feature `AIRCRAFT_ID` foi escolhida para indexar o dataframe. Registros com valores duplicados foram encontrados e removidos. A feature foi então testada para registros com valores que não correspondiam aos padrões mostrados nos metadados, que também foram removidos. Por último, `AIRCRAFT_ID` foi atribuído como indexador do dataframe.""",
}

DPP_MD2 = {
    "en": """The `EXPIRATION_DATE` was already parsed to datetime format. Even though the feature is already informative enough for some time series analysis, from it we can derive:
- `STATUS` - A categorical feature including each aircraft registration status. According to the regulation, the expiration date is two years from the date of its registration. After six months of expiration the register is no longer renewable (it becomes inactive); and
- `REG_DATE` - The date of the registration, calculated from `EXPIRATION_DATE` minus the standard validity period (two years).""",
    "pt-br": """A feature `EXPIRATION_DATE` foi convertida para o formato datetime. E ainda que ela já seja informativa o suficiente para uma análise temporal, ainda podemos derivar:
- `STATUS` - Uma feature categórica que inclui o estado de registro de cada aeronave. De acordo com o regulamento, a data de expiração é de dois anos a partir da data de registo. Após seis meses de expiração, o registo deixa de ser renovável (torna-se inativo); e
- `REG_DATE` - A data do registro, calculada a partir de `EXPIRATION_DATE` menos o período de validade padrão (dois anos).""",
}

DPP_MD3 = {
    "en": """Following, the `CPF_CNPJ` feature was worked on. After a close look on its values, it's possible to see that it holds two types of information:
- CPF or CNPJ: individuals or companies, respectively;
- Numbers 0-9: its proper number code. It's important to note that the CPF numbers are distributed in suppressed form due to privacy. The CNPJ numbers are public information however.    

So we are going to split this feature into: 
- `LEGAL_ENT`, with two categories (individual or company); and
- `ENT_NUM`, containing its number code.

Here are the new features:""",
    "pt-br": """Logo em seguida, a feature `CPF_CNPJ` foi tratada. Após uma observação atenta dos seus valores, foi possível perceber que ela carrega dois tipos de informação:
- CPF ou CNPJ: pessoas físicas ou jurídicas, respetivamente;
- Números de 0 a 9: seu código numérico e único. É importante ressaltar que os números do CPF são distribuídos de forma censurada por questões de privacidade. Já os números do CNPJ são informações de acesso público.    

Por isso, vamos dividir essa feature em: 
- `ENT_LEGAL`, com duas categorias (pessoa física ou jurídica); e
- `NUM_ENT`, que contém o número.

Aqui estão as novas features:""",
}

DPP_MD4 = {
    "en": """The `MANUFACTURER` and `TYPE_OF_ACTIVITY` features demanded more attention. Because they contain text input from the drone operator, it is not expected that the values will be standardized in the way they are written. For example, `DJI`, `Dji` and `dji` may be interpreted differently within the analysis, although they represent the same manufacturer. 

To solve this problem it was created a function that, given a dataframe column and a map, the names were replaced by standardized names.

Lastly, features that would not be used in the analysis were dropped from the dataframe.""",
    "pt-br": """As features `MANUFACTURER` e `TYPE_OF_ACTIVITY` precisaram de mais atenção. Como elas contêm entrada de texto feita pelo operador do drone, não é esperado que os valores estejam padronizados na maneira como são escritos. Por exemplo, `DJI`, `Dji` e `dji` podem ser interpretados de forma diferente na análise, embora representem o mesmo fabricante. 

Para resolver esse problema, foi criada uma função onde, dada uma coluna do dataframe e um dicionário, os valores fossem substituídos por valores padronizados.

Por fim, os dados que não seriam usados na análise foram retirados do dataframe.""",
}

## EXPLANATORY ANALYSIS
EX_SUBHEADER = {
    "en": "Explanatory analysis",
    "pt-br": "Análise explanatória",
}

EX_MD1 = {
    "en": """Let's start by checking the dates related to each aircraft registration. By comparing data of `STATUS`, `REG_DATE` and `EXPIRATON_DATE` features we can better understand the rate of adherence to the system and also about the maintenance of these registers.""",
    "pt-br": """Vamos começar verificando as datas relacionadas a cada registro de aeronave. Comparando os dados das features `STATUS`, `REG_DATE` e `EXPIRATON_DATE` podemos entender melhor a taxa de adesão ao sistema e também quanto à manutenção desses registros."""
}

EX_MD2 = {
    "en": "Now, through the `TYPE_OF_USE` feature, we will check how the drones perform their activities, in other words, how each drone is operated. The possible categories are 'basic' and 'advanced'.",
    "pt-br": """Agora, usando a feature `TYPE_OF_USE`, podemos verificar de que modo os drones são utilizados, em outras palavras, como cada drone é operado. As categorias possíveis são “básico” e “avançado”.""",
}

EX_MD3 = {
    "en": """To further the understanding of drone usage, the `TYPE_OF_ACTIVITY` feature was then evaluated. The numbers were compared with the newly created `LEGAL_ENT` feature.""",
    "pt-br": """Para aprofundar o entendimento do uso dos drones, a feature `TYPE_OF_ACTIVITY` foi avaliada. Os números foram comparados com a feature recém-criada `LEGAL_ENT`."""
}

EX_MD4 = {
    "en": """Finally, the questions regarding manufacturers and their aircraft models were analyzed. We used a word cloud for that (which basically displays words according to their frequency - the higher the frequency, the bigger the word - to visualize the distribution of manufacturers.""",
    "pt-br": """Por fim, foram analisadas as perguntas sobre os fabricantes e seus modelos de aeronaves. Para isso, foi utilizada uma nuvem de palavras (que basicamente exibe palavras de acordo com sua frequência - quanto maior a frequência, maior a palavra) para visualizar a distribuição das fabricantes."""
}

EX_MD5 = {
    "en": "Some trends and events can be observed by analyzing data related to the manufacturer and the type of activity over time.",
    "pt-br": "Algumas tendências e eventos podem ser observados por meio da análise de dados relacionados ao fabricante e ao tipo de atividade ao longo do tempo.",
}