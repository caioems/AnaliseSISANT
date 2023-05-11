### Importando módulos:
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from re import match
from wordcloud import WordCloud

pd.options.mode.chained_assignment = None
sns.set_theme(
    style = 'white',
    palette = 'tab10')

st.set_page_config(page_title="caioems - Aeronaves no SISANT (ANAC)")

with open('style.css') as css:
    st.markdown(
        f'<style>{css.read()}</style>',
        # '<style>{}</style>'.format(
        #     css.read()
        # ),
        unsafe_allow_html=True
    )

# st.markdown(
# '<div class="header"><h1>Aeronaves no SISANT (ANAC)</h1></div>',
# unsafe_allow_html=True
# )

st.header('Aeronaves no SISANT (ANAC)')

st.markdown(
'''Para este projeto foram utilizados dados públicos do Sistema de Aeronaves não Tripuladas (SISANT), um orgão da Agência Nacional de Aviação Civil (ANAC), hospedados no portal [Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/aeronaves-drones-cadastrados), contendo as aeronaves não tripuladas cadastradas em cumprimento ao parágrafo E94.301(b) do [RBAC-E No 94](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-e-94).'''
)
 
st.markdown('''O objetivo deste projeto é fixar métodos e práticas de data analytics utilizando Python. Considerando que os dados são crus, a experiência torna-se mais didática, uma vez que precisarão de pré-processamento.''')
 
st.markdown('''Assim sendo, pretende-se responder as seguintes perguntas:
- Quantos drones estão cadastrados no dataset? Qual o status de cada cadastro?
- Quantos diferentes OPERADORes estão cadastrados? Quais suas naturezas?
- Qual uso é feito desses drones?
- Qual empresa é a maior FABRICANTE? E quais seus os MODELOs mais populares?
_____'''
)

st.code(
'''#importando bibliotecas
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from re import match
from wordcloud import WordCloud''',
language='python'
)

st.code(
'''#carregando dados e visualizando a tabela
@st.cache_data
def load_data():
    url = r'https://sistemas.anac.gov.br/dadosabertos/Aeronaves/drones%20cadastrados/SISANT.csv'

    df = pd.read_csv(
        url,
        delimiter=';',
        skiprows=1,
        parse_dates=['DATA_VALIDADE'],
        date_parser=lambda x: pd.to_datetime(x, format=r'%d/%m/%Y')
        )
    df.dropna(inplace=True)
    return df
    
df = load_data()''',
language='python'
)

#carregando dados e visualizando a tabela
@st.cache_data
def load_data():
    url = r'https://sistemas.anac.gov.br/dadosabertos/Aeronaves/drones%20cadastrados/SISANT.csv'

    df = pd.read_csv(
        url,
        delimiter=';',
        skiprows=1,
        parse_dates=['DATA_VALIDADE'],
        date_parser=lambda x: pd.to_datetime(x, format=r'%d/%m/%Y')
        )
    df.dropna(inplace=True)
    return df
    
df = load_data()

st.dataframe(
    df,
    height=250,
    use_container_width=True
    )

with st.container():
    import io

    st.write('>Descrição da tabela:')

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(
        info_string,
        language='python'
        )

    st.dataframe(
        df.describe(
            include='all',  
            #datetime_is_numeric=True
            ),
        height=150
        )


st.subheader('Metadados da tabela:')
st.markdown(
    '''- `CODIGO_AERONAVE`: Código da Aeronave. Segue regras:
    - Uso Recreativo (Aeromodelo): PR-XXXXXXXXX; 
    - Uso não recreativo básico (RPA Classe 3 operada em linha de visada visual abaixo de 400 pés): PP-XXXXXXXXX;
    - Uso avançado (RPA Classe 2 e demais Classe 3): PS-XXXXXXXXX;  
    - Obs: cada X representa um número 0-9.

- `DATA_VALIDADE`: Data de validade, igual a data em que o cadastro foi feito ou renovado mais 2 (dois) anos.  

- `OPERADOR`: Nome do responsável pela operação do drone.

- `CPF/CNPJ`: Número do CPF ou do CNPJ do responsável pela operação do drone.

- `TIPO_USO`:
    - Básico: aeroMODELOs ou RPA Classe 3 operada exclusivamente na linha de visada visual abaixo de 400 pés AGL;
    - Avançado: RPA Classe 2 ou demais RPA classe 3.

- `FABRICANTE`: Nome do FABRICANTE da aeronave.
  
- `MODELO`: Nome do MODELO da aeronave. 

- `NUMERO_SERIE`: Número de série da aeronave. 
 
- `PESO_MAXIMO_DECOLAGEM_KG`: Peso máximo de decolagem, numérico, com duas casas decimais, em kilogramas.

- `RAMO_ATIVIDADE`: 
    - Recreativo (aeromodelos);
    - Experimental (aeronave avançada destinada exclusivamente a operações com propósitos experimentais);
    - Outros ramos de atividade conforme declarado pelo cadastrante.
    
_____
''')

st.subheader('Pré-processamento dos dados')
st.markdown(
'''Inicialmente a tabela foi indexada. A coluna CODIGO_AERONAVE era ideal para esse fim, já que teoricamente apresentava valores únicos e padronizados para cada aeronave do sistema. Porém, foram observados valores duplicados na coluna que precisaram ser removidos.'''
)

st.code(
'''#removendo espaços em branco e registros duplicados
df['CODIGO_AERONAVE'] = df['CODIGO_AERONAVE'].str.strip()
df['CODIGO_AERONAVE'] = df['CODIGO_AERONAVE'].str.replace(" ", "")

df = df.drop_duplicates(subset=['CODIGO_AERONAVE'], keep='first')''',
language='python'
)

#removendo possíveis espaços em branco
df['CODIGO_AERONAVE'] = df['CODIGO_AERONAVE'].str.strip()
df['CODIGO_AERONAVE'] = df['CODIGO_AERONAVE'].str.replace(" ", "")

#removendo duplicatas
df = df.drop_duplicates(subset=['CODIGO_AERONAVE'], keep='first')

#checando as duplicatas para entender se as outras colunas também possuem dados repetidos
# dupl = df[df.duplicated(subset=['CODIGO_AERONAVE'], keep=False)]
# print(dupl.sort_values(by=['CODIGO_AERONAVE']).head(6))

st.markdown(
'''Em seguida, a coluna também foi verificada quanto a valores que não seguiam os padrões de dígitos apresentados nos metadados do dataset.  
    
Finalmente, a coluna 'CODIGO_AERONAVE' foi transformada no index do dataframe.'''
)

st.code(
'''#checando se os padrões de código seguem o padrão dos metadados 
#e removendo os que não seguirem
nrows_before = df.shape[0]

mask = []
pattern = '^(PR|PP|PS)-\d{9}$'
for code in df['CODIGO_AERONAVE']:
    mask.append(bool(match(pattern, code)))
df = df[mask]

nrows_after = df.shape[0]

#transformando a coluna no index do dataframe:
df = df.set_index(df['CODIGO_AERONAVE'])
df = df.drop(('CODIGO_AERONAVE'), axis=1)''',
language='python'
)

#checando se os padrões de código seguem os descritos nos metadados e removendo os que não seguirem
nrows_before = df.shape[0]

pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['CODIGO_AERONAVE']]
df = df[mask]

nrows_after = df.shape[0]

st.markdown(
f'''>Registros removidos por padrão inválido: **{nrows_before - nrows_after}**  
Quantidade de registros válidos na tabela: **{nrows_after}**''')

#transformando a coluna no index do dataframe:
df = df.set_index(df['CODIGO_AERONAVE'])
df = df.drop(('CODIGO_AERONAVE'), axis=1)

st.dataframe(
    df,
    height=250,
    use_container_width=True)

st.markdown(
'Seguindo com a preparação dos dados,  as colunas `CPF_CNPJ`, `TIPO_USO`, `FABRICANTE` e `RAMO_ATIVIDADE` foram validadas e, quando necessário, transformadas.'
)

st.code(
'''#limpando a coluna 'CPF_CNPJ'
df['CPF_CNPJ'].str.strip()
df['CPF_CNPJ'].str.replace(" ", "")

#convertendo dtype
df['TIPO_USO'] = df['TIPO_USO'].astype('category')''',
language='python'
)

#limpando a coluna 'CPF_CNPJ'
df['CPF_CNPJ'].str.strip()
df['CPF_CNPJ'].str.replace(" ", "")

#convertendo dtype da coluna 'TIPO_USO'
df['TIPO_USO'] = df['TIPO_USO'].astype('category')

st.markdown(
'''As colunas `FABRICANTE` e `MODELO` precisaram de maior atenção pois, dada a natureza de seu input, apresentam diferentes valores para mesma categoria  
Exemplo: 'DJI', 'dji' e 'Dji' representam a mesma fabricante, DJI. Sendo assim, é necessário diminuir a quantidade de categorias da coluna. 

Iniciou-se pela coluna `FABRICANTE`, sendo que a `MODELO` será transformada posteriormente, pois iremos trabalhar apenas com os modelos fornecidos pela maior fabricante de drones da base de dados.''')

st.code(
'''#criando função para, dada uma coluna e um dicionário de sinônimos, 
#os nomes sejam substituídos por valores padronizados 
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['FABRICANTE'] = df['FABRICANTE'].str.lower()
df['FABRICANTE'] = df['FABRICANTE'].str.strip()
df['FABRICANTE'] = df['FABRICANTE'].str.replace(" ", "")

#o dicionario foi criado a partir dos valores mais comuns, 
#porém, dada a alta quantidade de valores únicos, fabricantes de
#menor expressão e desconhecidos foram agrupados na categoria 'outros'       
fab_map = {
    'autelrobotics': 'autel',
    'c-fly': 'cfly|c-fly',
    'custom': 'fabrica|aeroMODELO|propria|própria|proprio|próprio|caseiro|montado|artesanal|constru',
    'dji': 'dji|mavic|phanton|phantom',
    'flyingcircus': 'circus',
    'geprc': 'gepr',
    'highgreat': 'highgreat',
    'horus': 'horus',
    'hubsan': 'hubsan|hubsen',
    'nuvemuav': 'nuvem',
    'outros': 'outro',
    'parrot': 'parrot',
    'phoenixmodel': 'phoenix',
    'santiago&cintra': 'santiago|cintra',
    'sensefly': 'sensefly',
    'shantou': 'shantou',
    'sjrc': 'sjrc|srjc',
    'visuo': 'visuo',
    'x-fly': 'xfly|x-fly',
    'xiaomi': 'xiaomi|fimi|xiomi',
    'xmobots': 'xmobots',
    'zll': 'zll|sg906'
    }

#transformando nomes de FABRICANTEs
fix_names('FABRICANTE', fab_map)

df['FABRICANTE'] = df['FABRICANTE'].astype('category')''',
language='python'
)

#criando função para, dada uma coluna e um dicionário de sinônimos, os nomes sejam substituídos por valores padronizados 
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['FABRICANTE'] = df['FABRICANTE'].str.lower()
df['FABRICANTE'] = df['FABRICANTE'].str.strip()
df['FABRICANTE'] = df['FABRICANTE'].str.replace(" ", "")

#o dicionario foi criado a partir dos valores mais comuns (value_counts()), porém, dada a alta quantidade de valores únicos, FABRICANTEs de
#menor expressão e desconhecidos foram agrupados na categoria 'outros'       
fab_map = {
    'autelrobotics': 'autel',
    'c-fly': 'cfly|c-fly',
    'custom': 'fabrica|aeroMODELO|propria|própria|proprio|próprio|caseiro|montado|artesanal|constru',
    'dji': 'dji|mavic|phanton|phantom',
    'flyingcircus': 'circus',
    'geprc': 'gepr',
    'highgreat': 'highgreat',
    'horus': 'horus',
    'hubsan': 'hubsan|hubsen',
    'nuvemuav': 'nuvem',
    'outros': 'outro',
    'parrot': 'parrot',
    'phoenixmodel': 'phoenix',
    'santiago&cintra': 'santiago|cintra',
    'sensefly': 'sensefly',
    'shantou': 'shantou',
    'sjrc': 'sjrc|srjc',
    'visuo': 'visuo',
    'x-fly': 'xfly|x-fly',
    'xiaomi': 'xiaomi|fimi|xiomi',
    'xmobots': 'xmobots',
    'zll': 'zll|sg906'
    }

#transformando nomes de FABRICANTEs
fix_names('FABRICANTE', fab_map)

df['FABRICANTE'] = df['FABRICANTE'].astype('category')

if df['FABRICANTE'].value_counts().sum() == nrows_after:
    print('Coluna FABRICANTE: OK')
else:
    print('Coluna FABRICANTE: Problema')



st.write(
'''Finalmente, a coluna `RAMO_ATIVIDADE` também foi validada e transformada. Essa coluna classifica os drones nas categorias Recreativo, Experimental e Outras atividades, sendo essa última categoria especificada em forma de texto pelo usuário.'''
)

st.code(
'''df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.lower()
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.strip()
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.replace(" ", "")

#novamente foi criado um dicionário baseado nos valores mais comuns
#para padronizá-los e reduzir a quantidade de categorias
act_map = {
    'educação': 'treinamento|educa|ensin|pesquis',
    'engenharia': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'foto&cinem': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logística': 'transport|carga|delivery',
    'publicidade': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'segurança': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#corrigindo nomes a partir do dicionário, reclassificando atividades 
#mais específicas em 'outros' e convertendo o dtype da coluna
fix_names('RAMO_ATIVIDADE', act_map, df)
df.loc[
    ~df['RAMO_ATIVIDADE'].isin(
        df['RAMO_ATIVIDADE'].value_counts().head(8).index
        ), 'RAMO_ATIVIDADE'
    ] = 'outros'
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].astype('category')''',
language='python'
)

df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.lower()
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.strip()
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].str.replace(" ", "")

#novamente foi criado um dicionário baseado nos valores mais comuns para padronizá-los e reduzir a quantidade de categorias
act_map = {
    'educação': 'treinamento|educa|ensin|pesquis',
    'engenharia': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'foto&cinem': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logística': 'transport|carga|delivery',
    'publicidade': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'segurança': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#corrigindo nomes a partir do dicionário, reclassificando atividades mais específicas em 'outros' e convertendo o dtype da coluna
fix_names('RAMO_ATIVIDADE', act_map, df)
df.loc[
    ~df['RAMO_ATIVIDADE'].isin(
        df['RAMO_ATIVIDADE'].value_counts().head(8).index
        ), 'RAMO_ATIVIDADE'
    ] = 'outros'
df['RAMO_ATIVIDADE'] = df['RAMO_ATIVIDADE'].astype('category')

st.markdown(
'Por último, foram removidos da tabela os dados que não seriam utilizados nas análises.'
)

st.code(
'''#dropando colunas que não serão utilizadas na análise
df = df.drop(('NUMERO_SERIE'), axis=1)
df = df.drop(('PESO_MAXIMO_DECOLAGEM_KG'), axis=1)

#conferindo as informações do dataset pré-processado
df.describe(include='all', datetime_is_numeric=True)''')

#dropando colunas que não serão utilizadas na análise
df = df.drop(('NUMERO_SERIE'), axis=1)
df = df.drop(('PESO_MAXIMO_DECOLAGEM_KG'), axis=1)

st.markdown('>Versão final da tabela:')

with st.container():
    import io
    
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(
        info_string,
        language='python'
        )

    st.dataframe(
        df.describe(
            include='all', 
            datetime_is_numeric=True
            ),
        height=150
    )
    st.markdown('___')

st.subheader('Análise exploratória do dataframe:')
st.markdown(
'''A coluna `DATA_VALIDADE`, como o próprio nome sugere, apresenta as datas em que os cadastros devem ser renovados. Conforme a legislação, sabe-se que o prazo de expiração é de dois anos contados a partir da data de cadastro, e que após seis meses de expiração o cadastro não é mais renovável (torna-se inativo), podemos obter dois tipos de informação a partir dessa coluna:  
- A data de adesão da aeronave ao sistema;
- Quantos cadastros encontram-se fora do prazo de validade, carecem de renovação ou recadastramento.''')

st.code(
'''#criando coluna 'DATA_CADASTRO'
df['DATA_CADASTRO'] = df['DATA_VALIDADE'] - pd.DateOffset(years=2)

#criando função que classifica datas conforme situação do cadastro
def status_cadastro(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renovar'
    elif date + pd.DateOffset(months=6) < today:
        return 'inativo'
    return 'ok'

#criando coluna 'STATUS', contendo dados categorizados 
#sobre cada aeronave (cadastro ok, renovar ou inativo)
df['STATUS'] = df['DATA_VALIDADE'].apply(status_cadastro)
df['STATUS'] = df['STATUS'].astype('category')

#agregando dados por mês
agg_data = df.resample('M', on='DATA_CADASTRO').count()
agg_data.reset_index(inplace=True)

#configurando figure e os axes
fig, axs = plt.subplots(1, 2, figsize=(12,6))
fig.suptitle('Cadastros bimestrais e status do cadastro', weight='bold')
fig.tight_layout()

#criando o gráfico de linha
sns.lineplot(
    agg_data,
    x='DATA_CADASTRO', 
    y='OPERADOR',     
    ax=axs[0]
    )

#configurando atributos do gráfico de linhas
axs[0].grid(axis='x', linestyle='--')
axs[0].yaxis.grid(False)
axs[0].set(
    xticks=['2020-12-31', '2021-12-31', '2022-12-31', '2022-12-31'], 
    ylabel=None, 
    xlabel='Data de cadastro',
    )
sns.despine(ax=axs[0])

#criando o gráfico de barras
sns.countplot(
    df, 
    y='STATUS',
    order=df['STATUS'].value_counts().iloc[:3].index, 
    ax=axs[1]
    )

#configurando atributos do gráfico de barras
axs[1].set(
    xlabel='Qtd. cadastros',
    ylabel=None,
    )
sns.despine(ax=axs[1])''',
language='python'
)

#criando coluna 'DATA_CADASTRO'
df['DATA_CADASTRO'] = df['DATA_VALIDADE'] - pd.DateOffset(years=2)

#criando função que classifica datas conforme situação do cadastro
def status_cadastro(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renovar'
    elif date + pd.DateOffset(months=6) < today:
        return 'inativo'
    return 'ok'

#criando coluna 'STATUS', contendo dados categorizados sobre cada aeronave (cadastro ok, renovar ou inativo)
df['STATUS'] = df['DATA_VALIDADE'].apply(status_cadastro)
df['STATUS'] = df['STATUS'].astype('category')

#agregando dados por mês
agg_data = df.resample('M', on='DATA_CADASTRO').count()
agg_data.reset_index(inplace=True)

#configurando figure e os axes
fig, axs = plt.subplots(1, 2, figsize=(12,6))
fig.suptitle(
    'Cadastros bimestrais e status do cadastro', 
    weight='bold', 
    size='x-large'
    )
fig.tight_layout()
fig.patch.set_alpha(0.6) 

#criando o gráfico de linha
sns.lineplot(
    agg_data,
    x='DATA_CADASTRO', 
    y='OPERADOR',    
    ax=axs[0],
    )

#configurando atributos do gráfico de linhas
axs[0].grid(axis='x', linestyle='--', color='black')
axs[0].yaxis.grid(False)
axs[0].set(
    xticks=['2020-12-31', '2021-12-31', '2022-12-31', '2022-12-31'], 
    ylabel=None, 
    xlabel='Data de cadastro',
    fc='none'
    )
sns.despine(ax=axs[0])

#criando o gráfico de barras
sns.countplot(
    df, 
    y='STATUS',
    order=df['STATUS'].value_counts().iloc[:3].index, 
    ax=axs[1]
    )

#configurando atributos do gráfico de barras
axs[1].set(
    xlabel='Qtd. cadastros',
    ylabel=None,
    fc='none'
    )

sns.despine(ax=axs[1])

#calculando numero de aeronaves em cada categoria
num_inat = df[df['STATUS']=='inativo'].shape[0]
num_renov = df[df['STATUS']=='renovar'].shape[0]
num_ok = df[df['STATUS']=='ok'].shape[0]

st.markdown(
f'''>De forma geral, observou-se que a taxa de adesão de aeronaves ao sistema vem crescendo a cada mês. E do total de cadastros verificados ({df.shape[0]}), {num_inat} ({round(num_inat / df.shape[0] * 100, ndigits=1)}%) estão inativos, {num_renov} ({round(num_renov / df.shape[0] * 100, ndigits=1)}%) precisam ser renovados  e {num_ok} ({round(num_ok / df.shape[0] * 100, ndigits=1)}%) estão regularizados.''')

st.pyplot(fig)

 
st.markdown(
'''Antes de analisar a coluna `OPERADOR` é preciso confrontar os dados com a coluna `CPF_CNPJ`, uma vez que os valores da última são únicos. A coluna `OPERADOR` contém input de texto humano e, em múltiplos registros, foram encontrados diferentes nomes para o mesmo CPF/CNPJ. 
 
Foi ainda criada uma coluna chamada `NATUREZA_OP` contendo a classificação do operador entre pessoa física (PF) ou jurídica (PJ). É importante mencionar que os valores relacionados ao CPF fornecidos pelo sistema são parcialmente censurados, visando a preservação de dados pessoais.''')

st.code(
'''#agrupando dados pela coluna CPF_CNPJ, sendo que os possíveis 
#valores para a coluna OPERADOR foram enviados para uma lista
op_group = df.groupby('CPF_CNPJ')['OPERADOR'].apply(list).to_dict()

#criando mapa no formato de dicionário onde o valor de CPF_CNPJ será a chave 
#e o primeiro valor da lista de operadores será o nome padrão 
op_dict = {k: v[0] for k, v in op_group.items()}

#substituindo valores antigos da coluna OPERADOR pelos nomes corrigidos
unique_ops1 = len(df['OPERADOR'].unique())
df['OPERADOR'] = df['CPF_CNPJ'].map(op_dict)
unique_ops2 = len(df['OPERADOR'].unique())

#criando coluna NATUREZA_OP contendo classificação dos operadores entre pessoa física ou jurídica
df['NATUREZA_OP'] = df['CPF_CNPJ'].apply(
    lambda x: 'PF' if x.startswith('CPF') else 'PJ'
    ).astype('category')''',
    language='python')

#agrupando dados pela coluna de valores únicos CPF_CNPJ, sendo que os respectivos valores para a coluna OPERADOR foram enviados para uma lista
op_group = df.groupby('CPF_CNPJ')['OPERADOR'].apply(list).to_dict()

#criando mapa no formato de dicionário onde CPF_CNPJ será a chave e o primeiro valor da lista de operadores será o nome padrão 
op_dict = {k: v[0] for k, v in op_group.items()}

#substituindo valores antigos da coluna OPERADOR pelos nomes corrigidos
unique_ops1 = len(df['OPERADOR'].unique())
df['OPERADOR'] = df['CPF_CNPJ'].map(op_dict)
unique_ops2 = len(df['OPERADOR'].unique())

#criando coluna NATUREZA_OP contendo classificação dos operadores entre pessoa física ou jurídica
df['NATUREZA_OP'] = df['CPF_CNPJ'].apply(
    lambda x: 'PF' if x.startswith('CPF') else 'PJ'
    ).astype('category')

st.markdown(f'>A coluna `OPERADOR` teve {unique_ops1 - unique_ops2} nomes corrigidos.')

st.code(
'''#criando figure e axis    
fig, ax = plt.subplots(figsize=(12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme o tipo de uso', 
    weight='bold',
    size='x-large'
    )

#criando gráfico de pizza
ax.pie(
    df['TIPO_USO'].value_counts(), 
    startangle=315,
    )

#configurando atributos do gráfico
fig.patch.set_alpha(0.3) 
ax.axis('equal')    
sns.despine(ax=ax)
        
#adicionando legenda
fig.legend(
    labels = df['TIPO_USO'].value_counts().index.tolist(), 
    loc = 'lower right'
    )'''
    )

#criando figure e axis    
fig, ax = plt.subplots(figsize=(12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme o tipo de uso', 
    weight='bold',
    size='x-large'
    )

#criando gráfico de pizza
ax.pie(
    df['TIPO_USO'].value_counts(), 
    startangle=315,
    )

#configurando atributos do gráfico
fig.patch.set_alpha(0.6) 
# fig.patch.set_facecolor('none') 
# fig.patch.set_edgecolor('white')
#fig.patch.set_linewidth(1)
ax.axis('equal')  
sns.despine(ax=ax)
# for text in fig.findobj(plt.Text):
#     if text.get_color() != 'white':
#         text.set_color('white')
        
#adicionando legenda
fig.legend(
    labels = df['TIPO_USO'].value_counts().index.tolist(), 
    loc = 'lower right'
    )

percentage = df['TIPO_USO'].value_counts() / df['TIPO_USO'].value_counts().sum()
st.markdown(f'>O tipo de uso mais frequente é o {percentage.index[0]}, registrado em {round(percentage[0] * 100, 1)}% dos registros.') 

st.pyplot(fig)

st.markdown(
'''Para avançar no entendimento do uso das aeronaves, avaliou-se então a coluna `RAMO_ATIVIDADE`. Primeiramente, observou-se que a grande maioria dos drones registrados são destinados a atividades recreativas, sendo as atividades de 'fotografia e cinema' e 'engenharia' vindo logo após.

Adicionalmente esses números ainda foram comparados com a coluna `NATUREZA_OP`, onde verificou-se que as pessoas físicas são maioria em quase todas as atividades, com exceção da engenharia e da segurança.'''
)

st.code(
'''fig, ax = plt.subplots(figsize = (12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme os ramos de atividade no SISANT', 
    weight = 'bold'
    )

sns.countplot(
    df, 
    y = 'RAMO_ATIVIDADE', 
    hue = 'NATUREZA_OP',
    order = df['RAMO_ATIVIDADE'].value_counts().iloc[:10].index,
    ax=ax
    )

ax.grid(axis = 'x', linestyle = '--')
ax.yaxis.grid(False)
ax.set(xlabel = None, ylabel = None)
ax.legend(
    loc = 'lower right',
    labels = ['Pessoas físicas', 'Pessoas jurídicas']
    )

sns.despine(ax=ax)'''
)

fig, ax = plt.subplots(figsize = (12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme os ramos de atividade no SISANT', 
    weight = 'bold'
    )

sns.countplot(
    df, 
    y = 'RAMO_ATIVIDADE', 
    hue = 'NATUREZA_OP',
    order = df['RAMO_ATIVIDADE'].value_counts().iloc[:10].index,
    ax=ax
    )

ax.grid(axis = 'x', linestyle = '--', color='black')
#ax.yaxis.grid(False)

ax.set(
    xlabel = None, 
    ylabel = None,
    fc='none'
    )

ax.legend(
    loc = 'lower right',
    labels = ['Pessoas físicas', 'Pessoas jurídicas']
    )

fig.patch.set_alpha(0.6)
sns.despine(ax=ax)

st.pyplot(fig)

st.markdown(
'''Por fim, foram analisadas as questões relativas aos fabricantes e seus modelos de aeronaves. Primeiro utilizou-se um gráfico em formato "word cloud"(que basicamente exibe palavras de acordo com sua frequência (quanto maior a frequência, maior a palavra)) para visualizar a distribuição das fabricantes.'''
)

st.code(
'''#criando estrutura do gráfico
fig, ax = plt.subplots(figsize=(12,6))

#alterando atributos da figure
fig.tight_layout(pad=2)
fig.suptitle(
    'Principais FABRICANTEs das aeronaves no SISANT', 
    weight='bold'
    )

#criando grafico word cloud para representar a frequência das fabricantes
wordcloud = WordCloud(
    width=1200, height=600,
    mode='RGBA', 
    background_color='white',
    #min_font_size=15,
    colormap='tab10'
    ).fit_words(
        df['FABRICANTE'].value_counts().to_dict()
        )

#alterando atributos do axis
ax.axis("off")
ax.imshow(wordcloud, interpolation='bilinear')''',
language='python'
)

#criando estrutura do gráfico
fig, ax = plt.subplots(figsize=(12,6))

#alterando atributos da figure
fig.tight_layout(pad=2)
fig.suptitle(
    'Principais fabricantes das aeronaves no SISANT', 
    weight='bold'
    )
fig.patch.set_alpha(0.6)

#criando grafico word cloud para representar a frequência das fabricantes
wordcloud = WordCloud(
    width=1200, height=600,
    mode='RGBA', 
    background_color='white',
    #min_font_size=15,
    colormap='tab10'
    ).fit_words(
        df['FABRICANTE'].value_counts().to_dict()
        )

#alterando atributos do axis
ax.axis("off")
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_facecolor('none')


counts = df['FABRICANTE'].value_counts()
percentages = counts / counts.sum()
percentages = percentages.apply(
    lambda x: f'{round(x * 100, 1)}'
    )

st.pyplot(fig)

st.markdown(f'>A maior fornecedora é {percentages.index[0].upper()}, com frequência de {percentages[0]}%.')

st.write(percentages.head(5))

st.markdown('Foram então verificados quais os principais modelos de aeronaves fornecidas pela DJI nos dados do sistema. Para isso, a coluna `MODELO` foi finalmente pré-processada.')

st.code(
'''#criando subset contendo os drones fabricados pela dji
dji_df = df.loc[df['FABRICANTE']=='dji']

#removendo espaços em branco
dji_df['MODELO'] = dji_df['MODELO'].str.lower()
dji_df['MODELO'] = dji_df['MODELO'].str.strip()
dji_df['MODELO'] = dji_df['MODELO'].str.replace(" ", "")

#criando dicionário de modelos
dji_model_map = {
    'mavic': 'mav|air|ma2ue3w|m1p|da2sue1|1ss5|u11x|rc231|m2e|l1p|enterprisedual',
    'phantom': 'phan|wm331a|p4p|w322b|p4mult|w323|wm332a|hanto',
    'mini': 'min|mt2pd|mt2ss5|djimi|mt3m3vd',
    'spark': 'spa|mm1a',
    'matrice': 'matrice|m300',
    'avata': 'avata|qf2w4k',
    'inspire': 'inspire',
    'tello': 'tello|tlw004',
    'agras': 'agras|mg-1p|mg1p|t16|t10|t40|3wwdz',
    'fpv': 'fpv',
    'outros': 'dji'
    }

#novamente utilizando a função fix_names, dessa vez com argumentos
#relativos a coluna MODELO
fix_names('MODELO', dji_model_map, dji_df)

#renomeando modelos não reconhecidos como "outros"
dji_df.loc[~dji_df['MODELO'].isin(dji_df['MODELO'].value_counts().head(14).index), 'MODELO'] = 'outros'

dji_df['MODELO'] = dji_df['MODELO'].astype('category')

#criando estrutura para o gráfico
fig, ax = plt.subplots(figsize=(12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição dos modelos de aeronave fabricadas pela DJI no SISANT',
    weight='bold'
    )

#criando gráfico de barras
sns.countplot(
    y = dji_df['MODELO'],
    order = dji_df['MODELO'].value_counts().iloc[:10].index,
    ax=ax
    )

#adicionando grid
ax.grid(
    axis='x', 
    linestyle='--'
    )
#ax.yaxis.grid(False)

#alterando atributos do gráfico de barras
ax.set(
    xlabel=None,
    ylabel=None,
)
sns.despine(ax=ax)''',
language='python'
)

#criando subset contendo os drones fabricados pela dji
dji_df = df.loc[df['FABRICANTE']=='dji']

#removendo espaços em branco
dji_df['MODELO'] = dji_df['MODELO'].str.lower()
dji_df['MODELO'] = dji_df['MODELO'].str.strip()
dji_df['MODELO'] = dji_df['MODELO'].str.replace(" ", "")

#criando dicionário de modelos
dji_model_map = {
    'mavic': 'mav|air|ma2ue3w|m1p|da2sue1|1ss5|u11x|rc231|m2e|l1p|enterprisedual',
    'phantom': 'phan|wm331a|p4p|w322b|p4mult|w323|wm332a|hanto',
    'mini': 'min|mt2pd|mt2ss5|djimi|mt3m3vd',
    'spark': 'spa|mm1a',
    'matrice': 'matrice|m300',
    'avata': 'avata|qf2w4k',
    'inspire': 'inspire',
    'tello': 'tello|tlw004',
    'agras': 'agras|mg-1p|mg1p|t16|t10|t40|3wwdz',
    'fpv': 'fpv',
    'outros': 'dji'
    }

#novamente utilizando a função fix_names, dessa vez com argumentos
#relativos a coluna MODELO
fix_names('MODELO', dji_model_map, dji_df)

#renomeando modelos não reconhecidos como "outros"
dji_df.loc[~dji_df['MODELO'].isin(dji_df['MODELO'].value_counts().head(14).index), 'MODELO'] = 'outros'

dji_df['MODELO'] = dji_df['MODELO'].astype('category')

#criando estrutura para o gráfico
fig, ax = plt.subplots(figsize=(12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição dos modelos de aeronave fabricadas pela DJI no SISANT',
    weight='bold'
    )
fig.patch.set_alpha(0.6)

#criando gráfico de barras
sns.countplot(
    y = dji_df['MODELO'],
    order = dji_df['MODELO'].value_counts().iloc[:10].index,
    ax=ax
    )

#adicionando grid
ax.grid(
    axis='x', 
    linestyle='--',
    color='black'
    )
#ax.yaxis.grid(False)

#alterando atributos do gráfico de barras
ax.set(
    xlabel=None,
    ylabel=None,
    fc='none'
)

sns.despine(ax=ax)

st.pyplot(fig)



st.markdown('Quais as marcas preferidas dos PF e dos PJ?')

st.code(
'''#criando subsets baseados na coluna NATUREZA_OP
pf_df = df.loc[df['NATUREZA_OP']=='PF', 'FABRICANTE']
pj_df = df.loc[df['NATUREZA_OP']=='PJ', 'FABRICANTE']

#criando estrutura dos gráficos
fig, axs = plt.subplots(1, 2, figsize=(12,6), sharey=True)
fig.suptitle(
    'Distribuição das FABRICANTEs de aeronaves conforme a natureza jurídica do OPERADOR', 
    weight='bold'
    )
fig.tight_layout(pad=2)

#criando gráfico de barras 1 (pessoas físicas)
sns.countplot(
    x=pf_df, 
    order=pf_df.value_counts().iloc[:7].index, 
    ax=axs[0]
    )

#adicionando labels contendo seu respectivo valor a cada uma das barras
for bar in axs[0].patches:
    height = bar.get_height()
    axs[0].annotate(
        text=f"{int(height)}", 
        xy=(bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom'
        )

#alterando atributos do gráfico 1   
axs[0].set(
    xlabel=None, 
    ylabel=None,
    title='PF'
    )

sns.despine(ax=axs[0])

#criando gráfico de barras 2 (pessoas jurídicas)    
sns.countplot(
    x=pj_df, 
    order=pj_df.value_counts().iloc[:7].index, 
    ax=axs[1]
    )

#adicionando labels
for bar in axs[1].patches:
    height = bar.get_height()
    axs[1].annotate(
        text=f"{int(height)}", 
        xy=(bar.get_x() + bar.get_width() / 2, height),
        ha='center', 
        va='bottom'
        )

#alterando atributos do gráfico 2
axs[1].set(
    xlabel=None, 
    ylabel=None,
    title='PJ'
    )

sns.despine(ax=axs[1])''',
language='python'
)

#criando subsets baseados na coluna NATUREZA_OP
pf_df = df.loc[df['NATUREZA_OP']=='PF', 'FABRICANTE']
pj_df = df.loc[df['NATUREZA_OP']=='PJ', 'FABRICANTE']

#criando estrutura dos gráficos
fig, axs = plt.subplots(1, 2, figsize=(12,6), sharey=True)
fig.suptitle(
    'Distribuição das fabricantes de aeronaves conforme natureza jurídica', 
    weight='bold'
    )
fig.tight_layout(pad=2)
fig.patch.set_alpha(0.6)

#criando gráfico de barras 1 (pessoas físicas)
sns.countplot(
    x=pf_df, 
    order=pf_df.value_counts().iloc[:7].index, 
    ax=axs[0]
    )

#adicionando labels contendo seu respectivo valor a cada uma das barras
for bar in axs[0].patches:
    height = bar.get_height()
    axs[0].annotate(
        text=f"{int(height)}", 
        xy=(bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom'
        )

#alterando atributos do gráfico 1   
axs[0].set(
    xlabel=None, 
    ylabel=None,
    title='PF',
    fc='none'
    )

sns.despine(ax=axs[0])

#criando gráfico de barras 2 (pessoas jurídicas)    
sns.countplot(
    x=pj_df, 
    order=pj_df.value_counts().iloc[:7].index, 
    ax=axs[1]
    )

#adicionando labels
for bar in axs[1].patches:
    height = bar.get_height()
    axs[1].annotate(
        text=f"{int(height)}", 
        xy=(bar.get_x() + bar.get_width() / 2, height),
        ha='center', 
        va='bottom'
        )

#alterando atributos do gráfico 2
axs[1].set(
    xlabel=None, 
    ylabel=None,
    title='PJ',
    fc='none'
    )

sns.despine(ax=axs[1])

st.pyplot(fig)





