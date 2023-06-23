### Importando módulos:
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from re import match
from wordcloud import WordCloud

pd.options.mode.chained_assignment = None
st.set_page_config(page_title="Aircrafts of SISANT (ANAC) - by Caio Souza")

#loading CSS style
# with open('style.css') as css:
#     st.markdown(
#         f'<style>{css.read()}</style>',
#         unsafe_allow_html=True
#     )

#setting up the sidebar
st.sidebar.markdown("# Sections")
st.sidebar.markdown('[Getting Started](#an-investigation-of-the-national-civil-aviation-agency-of-brazil-s-database-of-unmanned-aircrafts-uavs)')
st.sidebar.markdown('[Dataframe metadata](#dataframe-metadata)')
st.sidebar.markdown('[Data pre-processing](#data-pre-processing)')
st.sidebar.markdown('[Explanatory analysis](#explanatory-analysis)')

#creating the document
st.header('''An investigation of the National Civil Aviation Agency of Brazil's database of unmanned aircrafts (UAVs)
_____''')

st.markdown('''The use of UAVs (drones) for services in Brazil became popular in the 2010s. However, the legal framework for airspace use is still being built, as well as systems for registering and regulating these aircraft. SISANT (Unmanned Aircraft System) is a national system that collects data about the owner (operator) of the aircraft as well as the activities for which it is used. The aircraft owner is accountable for the information provided, and he can only legally operate a UAV in Brazilian territory after registering in this system.'''
)

st.markdown(
'''This project uses weekly updated public data from SISANT, under the National Civil Aviation Agency of Brazil (ANAC) administration. The data is hosted at the [Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/aeronaves-drones-cadastrados) portal and contains the unmanned aircraft registered in compliance with paragraph E94.301(b) of [RBAC-E No 94](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-e-94).'''
) 

st.markdown('''This project's purpose is to use data preparation methods and then perform a quick explanatory analysis. Python was used for the work, and all data was handled using the Pandas module. Matplotlib, Plotly, and WordCloud were chosen as plotting libraries.
            
The sections of this project are presented in the left sidebar. Select the last section if you want to jump right to the graphics.
_____'''
)

st.code(
'''#importing libs
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from re import match
from wordcloud import WordCloud

#loading data, dropping NAs and renaming features
url = r'https://sistemas.anac.gov.br/dadosabertos/Aeronaves/drones%20cadastrados/SISANT.csv'

df = pd.read_csv(
    url,
    delimiter=';',
    skiprows=1,
    parse_dates=['DATA_VALIDADE'],
    date_parser=lambda x: pd.to_datetime(x, format=r'%d/%m/%Y')
    )

df.dropna(inplace=True)

df.columns = ['AIRCRAFT_ID', 'EXPIRATION_DATE', 'OPERATOR', 'CPF_CNPJ', 'TYPE_OF_USE', 'MANUFACTURER', 'MODEL', 'SERIAL_NUMBER', 'MAX_WEIGHT_TAKEOFF','TYPE_OF_ACTIVITY']'''
)

#loading data, dropping NAs and renaming features
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

st.write(':arrow_right: Raw dataframe and features description:')
st.dataframe(
    df,
    height=250,
    use_container_width=True
    )

with st.container():
    import io

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
''')

st.subheader('Data pre-processing')
st.markdown(
'''The `AIRCRAFT_ID` feature would be used to index the dataframe at first. However, duplicate values were found and removed. The feature was then tested for values that did not match the digit patterns shown in the dataset information. Finally, `AIRCRAFT_ID` was assigned as the dataframe index.'''
)

#checking the duplicates
dupl = df[df.duplicated(subset=['AIRCRAFT_ID'], keep=False)]

st.markdown(':arrow_right: Duplicated entries:')
st.dataframe(
    dupl.sort_values(by=['AIRCRAFT_ID']),
    height= 100
)

st.code(
'''#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')

#ensuring that each aircraft's ID codes comply to the patterns set 
#in the metadata, and removing those that do not
pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
df = df[mask]

#setting index
df = df.set_index(df['AIRCRAFT_ID'])
df = df.drop(('AIRCRAFT_ID'), axis=1)'''
)

#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')

#checking that the codes for each aircraft conform to the patterns established in the metadata, and removing those that do not
nrows_before = df.shape[0]

pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
df = df[mask]

nrows_after = df.shape[0]

st.markdown(
f''':arrow_right: Entries removed by invalid ID code patterns: **{nrows_before - nrows_after}**  
:arrow_right: Valid entries in the dataframe: **{nrows_after}**''')

#setting index:
df = df.set_index(df['AIRCRAFT_ID'])
df = df.drop(('AIRCRAFT_ID'), axis=1)

st.dataframe(
    df,
    height=250,
    use_container_width=True)

st.markdown(
'''The `EXPIRATION_DATE` was already parsed to datetime format. Even though the feature is already informative as it is, from it we can derive:
- `STATUS` - A categorical feature including each aircraft registration status. According to the regulation, the expiration date is two years from the date of registration. After six months of expiration the registration is no longer renewable (it becomes inactive); and
- `REG_DATE` - The date of the registration, calculated from `EXPIRATION_DATE` minus the standard validity period (two years).'''
)

st.code(
'''#creating a function that sorts dates according to register status
def reg_status(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renew'
    elif date < today - pd.DateOffset(months=6):
        return 'inactive'
    else:
        return 'ok'

#creating a 'STATUS' feature, containing categorized data about each aircraft
df['STATUS'] = df['EXPIRATION_DATE'].apply(reg_status)
df['STATUS'] = df['STATUS'].astype('category')

#creating feature 'REG_DATE'
df['REG_DATE'] = df['EXPIRATION_DATE'] - pd.DateOffset(years=2)'''
)

#creating a function that sorts dates according to register status (register ok, renew ou inactive)
def reg_status(date):
    today = pd.Timestamp.today()
    if date < today:
        return 'renew'
    elif date < today - pd.DateOffset(months=6):
        return 'inactive'
    else:
        return 'ok'

#creating a 'STATUS' feature, containing categorized data about each aircraft
df['STATUS'] = df['EXPIRATION_DATE'].apply(reg_status)
df['STATUS'] = df['STATUS'].astype('category')

#creating feature 'REG_DATE'
df['REG_DATE'] = df['EXPIRATION_DATE'] - pd.DateOffset(years=2)

st.write(df[['STATUS', 'REG_DATE']])

st.markdown(
'''Following, the `CPF_CNPJ` feature was worked on.'''
)

st.code(
'''#removing whitespaces from the 'CPF_CNPJ'
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")'''
)

#removing whitespaces from the 'CPF_CNPJ'
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")

st.write(df['CPF_CNPJ'])

st.markdown(
'''After a close look at the values of `CPF_CNPJ`, it's possible to see that it holds two types of information:
- CPF or CNPJ: individuals or companies, respectively;
- Numbers 0-9: its proper number code. It's important to note that the CPF numbers are distributed in suppressed form due to privacy. The CNPJ numbers are public information however.    

So we are going to split this feature into: 
- `LEGAL_ENT`, with two categories (individual or company); and
- `ENT_NUM`, containing its number code.'''
)

st.code(
'''df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'individual' if x.startswith('CPF') else 'company'
    ).astype('category')

df['ENT_NUM'] = df['CPF_CNPJ'].apply(
    lambda x: ''.join(filter(str.isdigit, x.replace(':', '')))
    ).astype('category')

#dropping CPF_CNPJ 
df = df.drop(('CPF_CNPJ'), axis=1)'''   
)

# Splitting the 'CPF_CNPJ' feature into 'LEGAL_ENT' and 'ENT_NUM'
df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'individual' if x.startswith('CPF') else 'company'
    ).astype('category')

df['ENT_NUM'] = df['CPF_CNPJ'].apply(
    lambda x: ''.join(filter(str.isdigit, x.replace(':', '')))
    ).astype('category')

#dropping CPF_CNPJ
df = df.drop(('CPF_CNPJ'), axis=1)

st.write(df[['LEGAL_ENT', 'ENT_NUM']])

#converting dtype
df['TYPE_OF_USE'] = df['TYPE_OF_USE'].apply(
    lambda x: 'basic' if x == 'Básico' else 'advanced'
).astype('category')
#df['TYPE_OF_USE'] = df['TYPE_OF_USE'].astype('category')


st.markdown(
'''The `MANUFACTURER` and `MODEL` features demanded more attention because, as they contain text input, they may have different values for the same category.
  
Example: `DJI`, `Dji` and `dji` represents same manufacturer. 

We started with `MANUFACTURER` (`MODEL` will be transformed in another moment because we will work only with the models provided by the most frequent drone manufacturer in the database).''')

st.code(
'''#creating function that, given a dataframe column and a map, the names 
#are replaced by standardized names
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['MANUFACTURER'] = df['MANUFACTURER'].str.lower().strip().replace(" ", "")

#the dictionary was created based on the most common values, however,
#given the high amount of unique values, lesser expressed and 
#unknown manufacturers were grouped in the 'others' category       
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
    'others': 'outro',
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

#transforming the feature with the manufacturers names
fix_names('MANUFACTURER', fab_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')'''
)

#creating function so that, given a dataframe column and a map, the names are replaced by standardized names 
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['MANUFACTURER'] = df['MANUFACTURER'].str.lower()
df['MANUFACTURER'] = df['MANUFACTURER'].str.replace(" ", "")

#the dictionary was created based on the most common values, however, given the high amount of unique values, lesser expressed and unknown manufacturers were grouped in the 'others' category
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
    'others': 'outro',
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

#transforming the feature with the manufacturers' names
fix_names('MANUFACTURER', fab_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')

st.write(
'''Finally, the `TYPE_OF_ACTIVITY` feature was also validated and transformed. It categorizes the drones into 'Recreational', 'Experimental', and 'Other activities', the latter category being specified in text provided by the user.'''
)

st.code(
'''#cleaning feature
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the feature
act_map = {
    'education': 'treinamento|educa|ensin|pesquis',
    'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logistics': 'transport|carga|delivery',
    'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the feature dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)

df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'others'

df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')'''
)

#cleaning feature
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the feature
act_map = {
    'education': 'treinamento|educa|ensin|pesquis',
    'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logistics': 'transport|carga|delivery',
    'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'recreative': 'recreativo',
    'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the feature dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)

df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'others'

df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')

st.markdown(
'Lastly, features that would not be used in the analysis were removed from the dataframe.'
)

st.code(
'''#dropping features that won't be used
df = df.drop(
    [('SERIAL_NUMBER'), ('MAX_WEIGHT_TAKEOFF')],
    axis=1
    )''')

#dropping features that won't be used
df = df.drop(
    [('SERIAL_NUMBER')],
    axis=1
    )

st.markdown(':arrow_right: Pre-processed dataframe:')

with st.container():
    import io

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(
        info_string
        )

    st.dataframe(
        df.describe(
            include='all', 
            #datetime_is_numeric=True
            ),
        height=150
    )
    st.markdown('___')

st.subheader('Explanatory analysis')

st.markdown(
'''Let's start by checking the dates related to each aircraft registration. By comparing data of `STATUS`, `REG_DATE` and `EXPIRATON_DATE` features we can better understand the rate of adherence to the system and also about the maintenance of these registers.''')

st.code(
'''#aggregating data by month
agg_data = df.resample('M', on='REG_DATE').count()
agg_data.reset_index(inplace=True)

#creating line plot
fig = px.line(
    agg_data, 
    x='REG_DATE', 
    y='OPERATOR', 
    title='Monthly new registrations',
    labels={'REG_DATE': '', 'OPERATOR': 'new registers'}
    )

#creating histogram plot
fig = px.histogram(
    df,
    x='STATUS',
    color='STATUS',
    text_auto=True
)

#removing legend
fig.update_layout(
    showlegend=False,
    xaxis=dict(title=f'There was {n_inact} inactive registers.'),
    yaxis=dict(title=None)
    )

#adding an annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.02,
    y=1.1,
    text=f'Most of the aircrafts ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) are fine...',
    showarrow=False,
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
    )
)

#adding another annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.95,
    y=0.2,
    text=f'...whilst {round(n_renew / df.shape[0] * 100, ndigits=1)}% needs renewal.',
    showarrow=False,
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
    )
)'''
)

#aggregating data by month
agg_data = df.resample('M', on='REG_DATE').count()
agg_data.reset_index(inplace=True)

#calculating the number of aircraft in each category
n_inact = df[df['STATUS']=='inactive'].shape[0]
n_renew = df[df['STATUS']=='renew'].shape[0]
n_ok = df[df['STATUS']=='ok'].shape[0]

#creating and displaying line plot
fig = px.line(
    agg_data, 
    x='REG_DATE', 
    y='OPERATOR', 
    title=None,
    labels={'REG_DATE': '', 'OPERATOR': 'new registers'}
    )

#adding an annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0,
    y=1.1,
    text="Compliance with the system has increased over the time.",
    showarrow=False,
    font=dict(
        color='white',
        size=22,
        family='Open Sans'
    )
)

#adding another annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.02,
    y=1,
    text=f"This month, {agg_data['EXPIRATION_DATE'].iloc[-1]} new registers have already been made.",
    showarrow=False,
    font=dict(
        color='white',
        size=16,
        family='Open Sans'
    )
)

st.plotly_chart(fig)

#creating histogram plot
fig = px.histogram(
    df,
    x='STATUS',
    color='STATUS',
    text_auto=True
)

#removing legend
fig.update_layout(
    showlegend=False,
    xaxis=dict(title=f'There was {n_inact} inactive registers.'),
    yaxis=dict(title=None)
    )

#adding an annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.02,
    y=1.1,
    text=f'Most of the aircrafts ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) are fine...',
    showarrow=False,
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
    )
)

#adding another annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.95,
    y=0.2,
    text=f'...whilst {round(n_renew / df.shape[0] * 100, ndigits=1)}% needs renewal.',
    showarrow=False,
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
    )
)

#displaying the histogram plot
st.plotly_chart(fig)

st.markdown("Now, through the `TYPE_OF_USE` feature, we will check how the drones perform their activities, in other words, how each drone is operated. The possible categories are 'basic' and 'advanced'. ")

st.code(
'''#calculate the value counts for each type of use
value_counts = df['TYPE_OF_USE'].value_counts()

#creating an indicator chart
fig = go.Figure(go.Indicator(
    mode="number",
    title=dict(text='Currently,'),
    value=value_counts.values[0] / value_counts.sum() * 100,
    number=dict(
        suffix='%', 
        font=dict(
            family='Open Sans', 
            size=96
            )
        ),
    domain=dict(x=[0,1], y=[0.6, 1])
    )
)

#adding text to the chart
fig.add_annotation(
    xref='paper',
    yref='paper',
    xanchor='center',
    yanchor='middle',
    x=0.5,
    y=0.5,
    text="of the aircrafts are in basic operations<br><span style='color:gray'>(up to 25 kg, operated within line of sight and below 400 ft).</span>",
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
        ),
    showarrow=False
)

#adding more text to the chart
fig.add_annotation(
    xref='paper',
    yref='paper',
    xanchor='center',
    yanchor='middle',
    x=0.5,
    y=0.01,
    text=f"<span style='color:gray'>There are only</span><br><br><span style='font-size:48px'>{value_counts.values[1]}</span><br>UAVs registered for advanced operations.",
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
        ),
    showarrow=False
)

#setting the chart's background to transparent
fig.update_layout(
    dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
)'''
)

#calculate the value counts for each type of use
value_counts = df['TYPE_OF_USE'].value_counts()

#creating an indicator chart
fig = go.Figure(go.Indicator(
    mode="number",
    title=dict(text='Currently,'),
    value=value_counts.values[0] / value_counts.sum() * 100,
    number=dict(
        suffix='%', 
        font=dict(
            family='Open Sans', 
            size=96
            )
        ),
    domain=dict(x=[0,1], y=[0.6, 1])
    )
)

#adding text to the chart
fig.add_annotation(
    xref='paper',
    yref='paper',
    xanchor='center',
    yanchor='middle',
    x=0.5,
    y=0.5,
    text="of the aircrafts are in basic operations<br><span style='color:gray'>(up to 25 kg, operated within line of sight and below 400 ft).</span>",
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
        ),
    showarrow=False
)

#adding more text to the chart
fig.add_annotation(
    xref='paper',
    yref='paper',
    xanchor='center',
    yanchor='middle',
    x=0.5,
    y=0.01,
    text=f"<span style='color:gray'>There are only</span><br><br><span style='font-size:48px'>{value_counts.values[1]}</span><br>UAVs registered for advanced operations.",
    font=dict(
        color='white',
        size=20,
        family='Open Sans'
        ),
    showarrow=False
)

#setting the chart's background to transparent
fig.update_layout(
    dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
)

st.plotly_chart(fig)

st.markdown(
'''To further the understanding of drone usage, the `TYPE_OF_ACTIVITY` feature was then evaluated. The numbers were compared with the newly created `LEGAL_ENT` feature.'''
)

st.code(
'''#create the histogram plot
fig = px.histogram(
    df,
    y='TYPE_OF_ACTIVITY',
    color='LEGAL_ENT',
    category_orders={'TYPE_OF_ACTIVITY': df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index},
    height=500
    )

#setting histogram plot attributes
fig.update_layout(
    title=dict(
        text='Recreational drones are in the majority,',
        font=dict(
            size=24,
            family='Open Sans'
            )
        ),
    legend=dict(
        title=None,
        xanchor='right',
        yanchor='bottom', 
        x=0.92,
        y=0.05,
        ),
    xaxis=dict(title=None),
    yaxis=dict(title=None)
)

fig.add_annotation(
    xref='paper',
    yref='paper',
    x=-0.1,
    y=1.08,
    text="and this is the favorite activity of the individuals.",
    showarrow=False,
    font=dict(
        color='white',
        size=16,
        family='Open Sans'
    )
)'''
)

#create the histogram plot
fig = px.histogram(
    df,
    y='TYPE_OF_ACTIVITY',
    color='LEGAL_ENT',
    category_orders={'TYPE_OF_ACTIVITY': df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index},
    height=500
    )

#setting histogram plot attributes
fig.update_layout(
    title=dict(
        text='Recreational drones are in the majority,',
        font=dict(
            size=24,
            family='Open Sans'
            )
        ),
    legend=dict(
        title=None,
        xanchor='right',
        yanchor='bottom', 
        x=0.92,
        y=0.05,
        ),
    xaxis=dict(title=None),
    yaxis=dict(title=None)
)

fig.add_annotation(
    xref='paper',
    yref='paper',
    x=-0.1,
    y=1.08,
    text="and this is the favorite activity of the individuals.",
    showarrow=False,
    font=dict(
        color='white',
        size=16,
        family='Open Sans'
    )
)

#displaying plot
st.plotly_chart(fig)

st.markdown(
'''Finally, the questions regarding manufacturers and their aircraft models were analyzed. We used a word cloud for that (which basically displays words according to their frequency - the higher the frequency, the bigger the word - to visualize the distribution of manufacturers.'''
)

st.code(
'''#creating figure and axis
fig, ax = plt.subplots(figsize=(12,6))
fig.patch.set_alpha(0.0)

#creating word cloud
wordcloud = WordCloud(
    width=1200, height=600, 
    colormap='tab10'
    ).generate_from_frequencies(
        df['MANUFACTURER'].value_counts()
        )

#setting axis attributes
ax.axis("off")
ax.imshow(wordcloud, interpolation='bilinear')'''
)

counts = df['MANUFACTURER'].value_counts()
percentages = counts / counts.sum()
percentages = percentages.apply(
    lambda x: f'{round(x * 100, 1)}'
    )

#creating figure and axis
fig, ax = plt.subplots(figsize=(12,6))
fig.patch.set_alpha(0.0)

#creating word cloud
wordcloud = WordCloud(
    width=1200, height=600, 
    colormap='tab10'
    ).generate_from_frequencies(
        df['MANUFACTURER'].value_counts()
        )

#setting axis attributes
ax.axis("off")
ax.imshow(wordcloud, interpolation='bilinear')

st.markdown(
    f"""<p style="text-align:center"><span style="font-family:Open Sans,sans-serif"><span style="color:#ffffff"><strong><span style="font-size:32px">{percentages.index[0].upper()} is the most common drone maker, with {percentages[0]}% of all the drones registered.</span></strong></span><br><span style="color:#dddddd"><span style="font-size:18px">Its followed by {percentages.index[1].upper()} ({percentages[1]}%) and {percentages.index[2].upper()} ({percentages[2]}%).</span></span><br><span style="color:#999999"><span style="font-size:16px">Each of the other manufacturers are represented by {percentages[3]}% or less of the registered aircrafts.</span></span></span></p>""",
    unsafe_allow_html=True
)

st.pyplot(fig)

st.markdown('It was then checked which are the main aircraft models provided by DJI in the system data. For this, the `MODEL` feature was finally preprocessed.')

st.code(
'''#creating subset containing dji aircrafts
dji_df = df.loc[df['MANUFACTURER']=='dji']

#cleaning whitespaces
dji_df['MODEL'] = dji_df['MODEL'].str.lower()
dji_df['MODEL'] = dji_df['MODEL'].str.replace(" ", "")

#creating a model dictionary
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
    'others': 'dji'
    }

applying the fix_names function to the MODEL feature
fix_names('MODEL', dji_model_map, dji_df)

#renaming unknown models as "others"
dji_df.loc[~dji_df['MODEL'].isin(dji_df['MODEL'].value_counts().head(14).index), 'MODEL'] = 'others'

dji_df['MODEL'] = dji_df['MODEL'].astype('category')

#creating the histogram plot
fig = px.histogram(
    dji_df, 
    y='MODEL',
    category_orders={'MODEL': dji_df['MODEL'].value_counts().iloc[:14].index}
    )

#set histogram plot attributes
fig.update_layout(
    title='Distribution of aircraft models manufactured by DJI in SISANT',
    title_font=dict(size=24),
    xaxis=dict(title=None),
    yaxis=dict(title=None),
)'''
)

#criando subset contendo os drones fabricados pela dji
dji_df = df.loc[df['MANUFACTURER']=='dji']

#removendo espaços em branco
dji_df['MODEL'] = dji_df['MODEL'].str.lower()
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
    'others': 'dji'
    }

#novamente utilizando a função fix_names, dessa vez com argumentos
#relativos a coluna MODEL
fix_names('MODEL', dji_model_map, dji_df)

#renomeando modelos não reconhecidos como "others"
dji_df.loc[~dji_df['MODEL'].isin(dji_df['MODEL'].value_counts().head(14).index), 'MODEL'] = 'others'

dji_df['MODEL'] = dji_df['MODEL'].astype('category')

#creating the histogram plot
fig = px.histogram(
    dji_df, 
    y='MODEL',
    category_orders={'MODEL': dji_df['MODEL'].value_counts().iloc[:14].index},
    text_auto=True
    )

#set histogram plot attributes
fig.update_layout(
    title='Distribution of aircraft models manufactured by DJI in SISANT',
    title_font=dict(size=24),
    xaxis=dict(title=None),
    yaxis=dict(title=None),
)

# Display the plot
st.plotly_chart(fig)

st.markdown('Which brands do individuals and companies prefer?')

st.code(
'''#creating subsets based on LEGAL_ENT
ind_df = df.loc[df['LEGAL_ENT'] == 'individual', 'MANUFACTURER']
co_df = df.loc[df['LEGAL_ENT'] == 'company', 'MANUFACTURER']

#creating figure and subplots
fig = sp.make_subplots(
    rows=1, 
    cols=2, 
    subplot_titles=('individuals', 'companies'), 
    shared_yaxes=True
    )

#creating the first histogram plot (individuals)
fig.add_trace(
    go.Bar(
        x=ind_df.value_counts().iloc[:7].index,
        y=ind_df.value_counts().iloc[:7],
        marker_color='lightskyblue',
        text=ind_df.value_counts().iloc[:7],
        ),
    row=1,
    col=1
    )

#creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        x=co_df.value_counts().iloc[:7].index,
        y=co_df.value_counts().iloc[:7],
        marker_color='lightgreen',
        text=co_df.value_counts().iloc[:7],
        ),
    row=1, 
    col=2
    )

#updating layout and axis labels
fig.update_layout(
    title='Distribution of aircraft manufacturers by legal nature',
    title_font=dict(size=24),
    showlegend=False,
    yaxis=dict(title=None),
    yaxis2=dict(title=None)
    )'''
)

#creating subsets based on LEGAL_ENT
ind_df = df.loc[df['LEGAL_ENT'] == 'individual', 'MANUFACTURER']
co_df = df.loc[df['LEGAL_ENT'] == 'company', 'MANUFACTURER']

#creating figure and subplots
fig = sp.make_subplots(
    rows=1, 
    cols=2, 
    subplot_titles=('individuals', 'companies'), 
    shared_yaxes=True
    )

#creating the first histogram plot (individuals)
fig.add_trace(
    go.Bar(
        x=ind_df.value_counts().iloc[:7].index,
        y=ind_df.value_counts().iloc[:7],
        marker_color='lightskyblue',
        text=ind_df.value_counts().iloc[:7],
        ),
    row=1,
    col=1
    )

#creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        x=co_df.value_counts().iloc[:7].index,
        y=co_df.value_counts().iloc[:7],
        marker_color='lightgreen',
        text=co_df.value_counts().iloc[:7],
        ),
    row=1, 
    col=2
    )

#updating layout and axis labels
fig.update_layout(
    title='Distribution of aircraft manufacturers...',
    title_font=dict(size=24),
    showlegend=False,
    yaxis=dict(title=None),
    yaxis2=dict(title=None)
    )

#displaying
st.plotly_chart(fig)

# weight = df[
#     (df['MAX_WEIGHT_TAKEOFF'] > df['MAX_WEIGHT_TAKEOFF'].quantile(0.02))
#     & (df['MAX_WEIGHT_TAKEOFF'] < df['MAX_WEIGHT_TAKEOFF'].quantile(0.98))
#     ]
# fig = px.histogram(
#     weight['MAX_WEIGHT_TAKEOFF'],
#     color=weight['LEGAL_ENT'],
#     #nbins=20,
#     #histnorm='probability density'
#     )

# st.plotly_chart(fig)

ind_models = dji_df.loc[
    dji_df['LEGAL_ENT'] == 'individual',
    'MODEL'
    ]

co_models = dji_df.loc[
    dji_df['LEGAL_ENT'] == 'company',
    'MODEL'
    ]

#creating figure and subplots
fig = sp.make_subplots(
    rows=1, 
    cols=2, 
    subplot_titles=('individuals', 'companies'), 
    shared_yaxes=True
    )

#creating the first histogram plot (individuals)
fig.add_trace(
    go.Bar(
        x=ind_models.value_counts().iloc[:7].index,
        y=ind_models.value_counts().iloc[:7],
        marker_color='lightskyblue',
        text=ind_models.value_counts().iloc[:7],
        ),
    row=1,
    col=1
    )

#creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        x=co_models.value_counts().iloc[:7].index,
        y=co_models.value_counts().iloc[:7],
        marker_color='lightgreen',
        text=co_models.value_counts().iloc[:7],
        ),
    row=1, 
    col=2
    )

#updating layout and axis labels
fig.update_layout(
    title='...and the distribution of DJI models.',
    title_font=dict(size=24),
    title_x=0.45,
    showlegend=False,
    yaxis=dict(title=None),
    yaxis2=dict(title=None)
    )

#displaying
st.plotly_chart(fig)

# fig = px.bar(
#     dji_df,
#     x=dji_df['MODEL'],
#     y=counts,
#     color=dji_df['LEGAL_ENT']
# )

# st.plotly_chart(fig)
