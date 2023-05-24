### Importando módulos:
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from re import match, sub
from wordcloud import WordCloud

pd.options.mode.chained_assignment = None
sns.set_theme(
    style = 'white',
    palette = 'tab10')

st.set_page_config(page_title="caioems - Aircrafts in SISANT (ANAC)")

with open('style.css') as css:
    st.markdown(
        f'<style>{css.read()}</style>',
        unsafe_allow_html=True
    )

# st.markdown(
# '<div class="header"><h1>Aeronaves no SISANT (ANAC)</h1></div>',
# unsafe_allow_html=True
# )

st.header('Database analysis of aircrafts registered in the brazilian System of Unmanned Aircraft (SISANT) of the National Civil Aviation Agency of Brazil (ANAC)')

st.markdown('''The use of UAVs (drones) for services in Brazil became popular in the 2010s. However, the legal framework for the use of airspace, as well as methods for the registration and regulation of these aircraft, is still being built. SISANT is a national system that collects information about the aircraft's owner (operator), as well as the activities for which it is employed. The aircraft owner is responsible for the data submitted, and he can only legally operate a UAV after its registering.'''
)

st.markdown(
'''This project is using public data from the Unmanned Aircraft System (SISANT) of the National Civil Aviation Agency of Brazil (ANAC), hosted on the [Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/aeronaves-drones-cadastrados) portal and contains the unmanned aircraft registered in compliance with paragraph E94.301(b) of [RBAC-E No 94](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-e-94).'''
) 

st.markdown('''The goal of this project is to apply data preprocessing methods and perform an exploratory analysis of the processed data.
_____'''
)

st.code(
'''#importing libs
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from re import match
from wordcloud import WordCloud'''
)

st.code(
'''#loading and visualizing the data 
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
    df.columns = ['EXPIRATION_DATE', 'OPERATOR', 'CPF_CNPJ', 'TYPE_OF_USE', 'MANUFACTURER', 'MODEL', 'TYPE_OF_ACTIVITY']
    return df
    
df = load_data()'''
)

#loading and visualizing the data 
#@st.cache_data
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
    df.columns = ['AIRCRAFT_ID', 'EXPIRATION_DATE', 'OPERATOR', 'CPF_CNPJ', 'TYPE_OF_USE', 'MANUFACTURER', 'MODEL', 'SERIAL_NUMBER', 'MAX_WEIGHT_TAKEOFF','TYPE_OF_ACTIVITY']
    return df
    
df = load_data()

st.dataframe(
    df,
    height=250,
    use_container_width=True
    )

with st.container():
    import io

    st.write('>Dataframe description:')

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(info_string)

    st.dataframe(
        df.describe(
            include='all',  
            #datetime_is_numeric=True
            ),
        height=150
        )


st.subheader('Dataframe metadata:')
st.markdown(
    '''- `AIRCRAFT_ID`: Aircraft ID code. Follows rules:
    - Recreational use (aircraft models): PR-XXXXXXXXX; 
    - Basic non-recreational use (Class 3 UAV operated in line-of-sight below 400 feet): PP-XXXXXXXXX;
    - Advanced use (Class 2 UAV and other Class 3): PS-XXXXXXXXX;  
    - Note: each X represents a number from 0 to 9.

- `EXPIRATION_DATE`: Expiration date, same as the date the registration was made or renewed (for another two years).  

- `OPERATOR`: Name of the person responsible for operating the drone.

- `CPF/CNPJ`: CPF or CNPJ number of the person responsible for operating the drone.

- `TYPE_OF_USE`:
    - Básico: aircraft models or Class 3 UAV operated exclusively in line-of-sight below 400 feet AGL;
    - Avançado: Class 2 UAV or other Class 3 UAV.

- `MANUFACTURER`: Name of aircraft manufacturer.
  
- `MODEL`: Aircraft model name. 

- `SERIAL_NUMBER`: Aircraft serial number. 
 
- `MAX_WEIGHT_TAKEOFF`: Maximum takeoff weight (numeric, two decimal places, in kilograms).

- `TYPE_OF_ACTIVITY`: 
    - Recreational (aircraft models);
    - Experimental (advanced aircraft intended exclusively for operations with experimental purposes);
    - Other fields of activity as declared by the registrant.
    
_____
''')

st.subheader('Data pre-processing')
st.markdown(
'''Initially the dataframe would be indexed by the column AIRCRAFT_ID. However, duplicate values were observed in the column that needed to be dropped.'''
)

st.code(
'''#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.strip().replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')'''
)

#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.strip().replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')

#checking the duplicates to understand if the other columns also have repeated data
# dupl = df[df.duplicated(subset=['AIRCRAFT_ID'], keep=False)]
# print(dupl.sort_values(by=['AIRCRAFT_ID']).head())

st.markdown(
'''Next, the column was also checked for values that did not follow the digit patterns presented in the dataset metadata.  
    
And finally, the column 'AIRCRAFT_ID' was ready to be set as the dataframe index.'''
)

st.code(
'''#checking that the codes for each aircraft conform to the patterns established in the metadata, and removing those that do not

pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
df = df[mask]

#setting index:
df = df.set_index(df['AIRCRAFT_ID'])
df = df.drop(('AIRCRAFT_ID'), axis=1)'''
)

#checking that the codes for each aircraft conform to the patterns established in the metadata, and removing those that do not
nrows_before = df.shape[0]

pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
df = df[mask]

nrows_after = df.shape[0]

st.markdown(
f'''>Entries removed by invalid patterns: **{nrows_before - nrows_after}**  
Valid entries in the dataframe: **{nrows_after}**''')

#setting index:
df = df.set_index(df['AIRCRAFT_ID'])
df = df.drop(('AIRCRAFT_ID'), axis=1)

st.dataframe(
    df,
    height=250,
    use_container_width=True)

st.markdown(
'''Following the data preprocessing, the columns `CPF_CNPJ` and `OPERATOR` were worked on. So first we are going to clean the CPF_CNPJ column.'''
)

st.code(
'''#removing whitespaces from the 'CPF_CNPJ' column'
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.strip().replace(" ", "")'''
)

#removing whitespaces from the 'CPF_CNPJ' column
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.strip().str.replace(" ", "")

#TODO: LEGAL_ENT must be created here because CPF_CNPJ holds two kinds of information: the type of entity and its number
st.markdown(
'''Now we will crosscheck the data in the `CPF_CNPJ` column with the `OPERATOR` column. The latter contains direct input from users, and in multiple entries different names were found for the same CPF/CNPJ. 

It is important to mention that the values related to the CPF are partially censored when stored in the database, aiming to preserve personal data.''')

st.code(
'''#grouping data by the column CPF_CNPJ, and the possible values for the column OPERATOR were sent to a list
op_group = df.groupby('CPF_CNPJ')['OPERATOR'].apply(list).to_dict()

#creating a map in dictionary format where the values of CPF_CNPJ will be the keys and the first value of the list of operators will be the name defined as default
op_dict = {k: v[0] for k, v in op_group.items()}

#replacing old values in the OPERATOR column with the default names
df['OPERATOR'] = df['CPF_CNPJ'].map(op_dict)'''
)

#grouping data by the column CPF_CNPJ, and the possible values for the column OPERATOR were sent to a list
op_group = df.groupby('CPF_CNPJ')['OPERATOR'].apply(list).to_dict()

#creating a map in dictionary format where the values of CPF_CNPJ will be the keys and the first value of the list of operators will be the name defined as default 
op_dict = {k: v[0] for k, v in op_group.items()}

#replacing old values in the OPERATOR column with the default names
unique_ops1 = df['OPERATOR'].nunique()
df['OPERATOR'] = df['CPF_CNPJ'].map(op_dict)
unique_ops2 = df['OPERATOR'].nunique()

st.markdown(f'''>The `OPERATOR` column had {unique_ops1 - unique_ops2} names fixed. ops = {df['OPERATOR'].nunique()} and cpfs = {df["CPF_CNPJ"].nunique()}''')

#converting dtype
df['TYPE_OF_USE'] = df['TYPE_OF_USE'].astype('category')

st.markdown(
'''The columns `MANUFACTURER` and `MODEL` needed more attention because, given the nature of their input, they present different values for the same category  
Example: `DJI`, `Dji` and `dji` representing same manufacturer. Therefore, it is necessary to decrease the number of categories in the column. 

We started with the `MANUFACTURER` column. The `MODEL` column will be transformed in another moment (we will work only with the models provided by the largest drone manufacturer in the database).''')

st.code(
'''#creating function that, given a dataframe column and a map, the names are replaced by standardized names
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['MANUFACTURER'] = df['MANUFACTURER'].str.lower().strip().replace(" ", "")

#the dictionary was created based on the most common values, however, given the high amount of unique values, lesser expressed and unknown manufacturers were grouped in the 'outros' category       
fab_map = {
    'autelrobotics': 'autel',
    'c-fly': 'cfly|c-fly',
    'custom': 'fabrica|aeromodelo|propria|própria|proprio|próprio|caseiro|montado|artesanal|constru',
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

#transforming the column with the manufacturers' names
fix_names('MANUFACTURER', fab_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')'''
)

#creating function so that, given a dataframe column and a map, the names are replaced by standardized names 
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['MANUFACTURER'] = df['MANUFACTURER'].str.lower()
df['MANUFACTURER'] = df['MANUFACTURER'].str.strip().replace(" ", "")

#the dictionary was created based on the most common values, however, given the high amount of unique values, lesser expressed and unknown manufacturers were grouped in the 'outros' category
fab_map = {
    'autelrobotics': 'autel',
    'c-fly': 'cfly|c-fly',
    'custom': 'fabrica|aeromodelo|propria|própria|proprio|próprio|caseiro|montado|artesanal|constru',
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

#transforming the column with the manufacturers' names
fix_names('MANUFACTURER', fab_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')

if df['MANUFACTURER'].value_counts().sum() == nrows_after:
    print('Column MANUFACTURER: OK')
else:
    print('Column MANUFACTURER: Problem')

st.write(
'''Finally, the `TYPE_OF_ACTIVITY` column was also validated and transformed. This column classifies the drones into the categories Recreational, Experimental, and Other activities, the latter category being specified in text form by the user.'''
)

st.code(
'''#cleaning column
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower().strip().replace(" ", "")

#again transforming the values of a column
act_map = {
    'educação': 'treinamento|educa|ensin|pesquis',
    'engenharia': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'foto&cinem': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logística': 'transport|carga|delivery',
    'publicidade': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'segurança': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the column dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)
df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'outros'
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')'''
)

#cleaning column
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.strip().replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the column
act_map = {
    'educação': 'treinamento|educa|ensin|pesquis',
    'engenharia': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'foto&cinem': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logística': 'transport|carga|delivery',
    'publicidade': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'segurança': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the column dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)
df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'outros'
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')

st.markdown(
'Finally, data that would not be used in the analysis were removed from the dataframe.'
)

st.code(
'''#dropping columns that will not be used
df = df.drop(('SERIAL_NUMBER'), axis=1)
df = df.drop(('MAX_WEIGHT_TAKEOFF'), axis=1)

#checking the data in the pre-processed dataset
df.describe(include='all', datetime_is_numeric=True)''')

#dropping columns that will not be used
df = df.drop(('SERIAL_NUMBER'), axis=1)
df = df.drop(('MAX_WEIGHT_TAKEOFF'), axis=1)

st.markdown('>Pre-processed dataframe:')

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
            #datetime_is_numeric=True
            ),
        height=150
    )
    st.markdown('___')

st.subheader('Exploratory dataframe analysis')
st.markdown(
'''The `EXPIRATION_DATE` column, as the name suggests, shows the dates on which the entries must be renewed. According to the regulation, it is known that the expiration date is two years from the date of registration. And that after six months of expiration the registration is no longer renewable (it becomes inactive). We can get two types of information from this column:  
- The date the aircraft joined the system;
- How many registrations are past their expiration date, in need of renewal or re-registration.''')

st.code(
'''#creating 'REG_DATE' column, containing the date of registration
df['REG_DATE'] = df['EXPIRATION_DATE'] - pd.DateOffset(years=2)

#creating a function that sorts dates according to register status
def status_cadastro(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renovar'
    elif date + pd.DateOffset(months=6) < today:
        return 'inativo'
    return 'ok'

#creating a 'STATUS' column, containing categorized data about each aircraft (registration ok, renew or inactive)
df['STATUS'] = df['EXPIRATION_DATE'].apply(status_cadastro)
df['STATUS'] = df['STATUS'].astype('category')

#aggregating data by month
agg_data = df.resample('M', on='REG_DATE').count()
agg_data.reset_index(inplace=True)

#setting up figure and axes
fig, axs = plt.subplots(1, 2, figsize=(12,6))
fig.suptitle('Cadastros bimestrais e status do cadastro', weight='bold')
fig.tight_layout()

#criando o gráfico de linha
sns.lineplot(
    agg_data,
    x='REG_DATE', 
    y='OPERATOR',     
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

#criando coluna 'REG_DATE'
df['REG_DATE'] = df['EXPIRATION_DATE'] - pd.DateOffset(years=2)

#criando função que classifica datas conforme situação do cadastro
def reg_status(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renovar'
    elif date + pd.DateOffset(months=6) < today:
        return 'inativo'
    return 'ok'

#criando coluna 'STATUS', contendo dados categorizados sobre cada aeronave (cadastro ok, renovar ou inativo)
df['STATUS'] = df['EXPIRATION_DATE'].apply(reg_status)
df['STATUS'] = df['STATUS'].astype('category')

#agregando dados por mês
agg_data = df.resample('M', on='REG_DATE').count()
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
    x='REG_DATE', 
    y='OPERATOR',    
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
n_inact = df[df['STATUS']=='inativo'].shape[0]
n_renew = df[df['STATUS']=='renovar'].shape[0]
n_ok = df[df['STATUS']=='ok'].shape[0]

st.markdown(
f'''>De forma geral, observou-se que a taxa de adesão de aeronaves ao sistema vem crescendo a cada mês. E do total de cadastros verificados ({df.shape[0]}), {n_inact} ({round(n_inact / df.shape[0] * 100, ndigits=1)}%) estão inativos, {n_renew} ({round(n_renew / df.shape[0] * 100, ndigits=1)}%) precisam ser renovados  e {n_ok} ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) estão regularizados.''')

st.pyplot(fig)

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
    df['TYPE_OF_USE'].value_counts(), 
    startangle=315,
    )

#configurando atributos do gráfico
fig.patch.set_alpha(0.3) 
ax.axis('equal')    
sns.despine(ax=ax)
        
#adicionando legenda
fig.legend(
    labels = df['TYPE_OF_USE'].value_counts().index.tolist(), 
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
    df['TYPE_OF_USE'].value_counts(), 
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
    labels = df['TYPE_OF_USE'].value_counts().index.tolist(), 
    loc = 'lower right'
    )

percentage = df['TYPE_OF_USE'].value_counts() / df['TYPE_OF_USE'].value_counts().sum()
st.markdown(f'>O tipo de uso mais frequente é o {percentage.index[0]}, registrado em {round(percentage[0] * 100, 1)}% dos registros.') 

st.pyplot(fig)

st.markdown(
'''Para avançar no entendimento do uso das aeronaves, avaliou-se então a coluna `TYPE_OF_ACTIVITY`. Primeiramente, observou-se que a grande maioria dos drones registrados são destinados a atividades recreativas, sendo as atividades de 'fotografia e cinema' e 'engenharia' vindo logo após.

Adicionalmente esses números ainda foram comparados com recém-criada a coluna `LEGAL_ENT`, onde verificou-se que as pessoas físicas são maioria em quase todas as atividades, com exceção da engenharia e da segurança.'''
)

st.code(
'''#criando coluna LEGAL_ENT contendo classificação dos operadores entre pessoa física ou jurídica
df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'PF' if x.startswith('CPF') else 'PJ'
    ).astype('category')

fig, ax = plt.subplots(figsize = (12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme os ramos de atividade no SISANT', 
    weight = 'bold'
    )

sns.countplot(
    df, 
    y = 'TYPE_OF_ACTIVITY', 
    hue = 'LEGAL_ENT',
    order = df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index,
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

#criando coluna LEGAL_ENT contendo classificação dos operadores entre pessoa física ou jurídica
df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'PF' if x.startswith('CPF') else 'PJ'
    ).astype('category')

fig, ax = plt.subplots(figsize = (12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição das aeronaves conforme os ramos de atividade no SISANT', 
    weight = 'bold'
    )

sns.countplot(
    df, 
    y = 'TYPE_OF_ACTIVITY', 
    hue = 'LEGAL_ENT',
    order = df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index,
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
    'Principais fabricantes das aeronaves no SISANT', 
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
        df['MANUFACTURER'].value_counts().to_dict()
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
        df['MANUFACTURER'].value_counts().to_dict()
        )

#alterando atributos do axis
ax.axis("off")
ax.imshow(wordcloud, interpolation='bilinear')
ax.set_facecolor('none')


counts = df['MANUFACTURER'].value_counts()
percentages = counts / counts.sum()
percentages = percentages.apply(
    lambda x: f'{round(x * 100, 1)}'
    )

st.pyplot(fig)

st.markdown(f'>A maior fornecedora é {percentages.index[0].upper()}, com frequência de {percentages[0]}%.')

st.write(percentages.head(5))

st.markdown('Foram então verificados quais os principais modelos de aeronaves fornecidas pela DJI nos dados do sistema. Para isso, a coluna `MODEL` foi finalmente pré-processada.')

st.code(
'''#criando subset contendo os drones fabricados pela dji
dji_df = df.loc[df['MANUFACTURER']=='dji']

#removendo espaços em branco
dji_df['MODEL'] = dji_df['MODEL'].str.lower()
dji_df['MODEL'] = dji_df['MODEL'].str.strip()
dji_df['MODEL'] = dji_df['MODEL'].str.replace(" ", "")

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
#relativos a coluna MODEL
fix_names('MODEL', dji_model_map, dji_df)

#renomeando modelos não reconhecidos como "outros"
dji_df.loc[~dji_df['MODEL'].isin(dji_df['MODEL'].value_counts().head(14).index), 'MODEL'] = 'outros'

dji_df['MODEL'] = dji_df['MODEL'].astype('category')

#criando estrutura para o gráfico
fig, ax = plt.subplots(figsize=(12,6))
fig.tight_layout(pad=2)
fig.suptitle(
    'Distribuição dos modelos de aeronave fabricadas pela DJI no SISANT',
    weight='bold'
    )

#criando gráfico de barras
sns.countplot(
    y = dji_df['MODEL'],
    order = dji_df['MODEL'].value_counts().iloc[:10].index,
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
dji_df = df.loc[df['MANUFACTURER']=='dji']

#removendo espaços em branco
dji_df['MODEL'] = dji_df['MODEL'].str.lower()
dji_df['MODEL'] = dji_df['MODEL'].str.strip()
dji_df['MODEL'] = dji_df['MODEL'].str.replace(" ", "")

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
#relativos a coluna MODEL
fix_names('MODEL', dji_model_map, dji_df)

#renomeando modelos não reconhecidos como "outros"
dji_df.loc[~dji_df['MODEL'].isin(dji_df['MODEL'].value_counts().head(14).index), 'MODEL'] = 'outros'

dji_df['MODEL'] = dji_df['MODEL'].astype('category')

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
    y = dji_df['MODEL'],
    order = dji_df['MODEL'].value_counts().iloc[:10].index,
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
'''#criando subsets baseados na coluna LEGAL_ENT
pf_df = df.loc[df['LEGAL_ENT']=='PF', 'MANUFACTURER']
pj_df = df.loc[df['LEGAL_ENT']=='PJ', 'MANUFACTURER']

#criando estrutura dos gráficos
fig, axs = plt.subplots(1, 2, figsize=(12,6), sharey=True)
fig.suptitle(
    'Distribuição das fabricantes de aeronaves conforme a natureza jurídica do operador', 
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

#criando subsets baseados na coluna LEGAL_ENT
ind_df = df.loc[df['LEGAL_ENT']=='PF', 'MANUFACTURER']
co_df = df.loc[df['LEGAL_ENT']=='PJ', 'MANUFACTURER']

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
    x=ind_df, 
    order=ind_df.value_counts().iloc[:7].index, 
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
    x=co_df, 
    order=co_df.value_counts().iloc[:7].index, 
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





