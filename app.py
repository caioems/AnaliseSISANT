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

st.header('''Database analysis of aircrafts registered in the System of Unmanned Aircraft (SISANT) of the National Civil Aviation Agency of Brazil (ANAC)
_____''')

st.markdown('''The use of UAVs (drones) for services in Brazil became popular in the 2010s. However, the legal framework for the use of airspace, as well as methods for the registration and regulation of these aircraft, is still being built. SISANT is a national system that collects information about the aircraft's owner (operator), as well as the activities for which it is employed. The aircraft owner is responsible for the data submitted, and he can only legally operate a UAV after its registering.'''
)

st.markdown(
'''This project is using public data from the Unmanned Aircraft System (SISANT) of the National Civil Aviation Agency of Brazil (ANAC), hosted on the [Dados Abertos](https://dados.gov.br/dados/conjuntos-dados/aeronaves-drones-cadastrados) portal and contains the unmanned aircraft registered in compliance with paragraph E94.301(b) of [RBAC-E No 94](https://www.anac.gov.br/assuntos/legislacao/legislacao-1/rbha-e-rbac/rbac/rbac-e-94).'''
) 

st.markdown('''The goal of this project is to apply data preprocessing methods and perform an exploratory analysis of the processed data. Python was selected for the task and all the data was handled with Pandas. The plotting libraries selected were Pyplot, Plotly and WordCloud.
_____'''
)

st.code(
'''#importing libs
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
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

    st.write('>Raw dataframe description:')

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
'''The dataframe would be initially indexed by the column `AIRCRAFT_ID`. However, duplicate values were found in the column and had to be removed.'''
)

#checking the duplicates to understand if the other columns also have repeated data
dupl = df[df.duplicated(subset=['AIRCRAFT_ID'], keep=False)]

st.write(
    dupl.sort_values(by=['AIRCRAFT_ID'])
)

st.code(
'''#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')'''
)

#removing whitespaces
df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.replace(" ", "")

#removing duplicates
df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='first')


# dupl = df[df.duplicated(subset=['AIRCRAFT_ID'], keep=False)]
# print(dupl.sort_values(by=['AIRCRAFT_ID']).head())

st.markdown(
'''Next, the column was also checked for values that did not follow the digit patterns presented in the dataset metadata.  
    
And finally, the column `AIRCRAFT_ID` was ready to be set as the dataframe index.'''
)

st.code(
'''#checking that the codes for each aircraft conform to the patterns established in the metadata, and removing those that do not
pattern = '^(PR|PP|PS)-\d{9}$'
mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
df = df[mask]

#setting index
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
>Valid entries in the dataframe: **{nrows_after}**''')

#setting index:
df = df.set_index(df['AIRCRAFT_ID'])
df = df.drop(('AIRCRAFT_ID'), axis=1)

st.dataframe(
    df,
    height=250,
    use_container_width=True)

st.markdown(
'''The `EXPIRATION_DATE` was already parsed to datetime format. Even though the column is already informative as it is, from it we can derive two other columns that will also be useful:
- `STATUS` - A categorical column including each aircraft registration status. According to the regulation, the expiration date is two years from the date of registration. After six months of expiration the registration is no longer renewable (it becomes inactive); and
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

#creating a 'STATUS' column, containing categorized data about each aircraft
df['STATUS'] = df['EXPIRATION_DATE'].apply(reg_status)
df['STATUS'] = df['STATUS'].astype('category')

#creating column 'REG_DATE'
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

#creating a 'STATUS' column, containing categorized data about each aircraft
df['STATUS'] = df['EXPIRATION_DATE'].apply(reg_status)
df['STATUS'] = df['STATUS'].astype('category')

#creating column 'REG_DATE'
df['REG_DATE'] = df['EXPIRATION_DATE'] - pd.DateOffset(years=2)

st.write(df[['STATUS', 'REG_DATE']])

st.markdown(
'''Following, the column `CPF_CNPJ` was worked on.'''
)

st.code(
'''#removing whitespaces from the 'CPF_CNPJ' column'
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")'''
)

#removing whitespaces from the 'CPF_CNPJ' column
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")

st.write(df['CPF_CNPJ'])

st.markdown(
'''After a close look at the values of `CPF_CNPJ`, it's possible to see that it holds two types of information:
- CPF or CNPJ: individuals or companies, respectively;
- Numbers 0-9: its proper number code. It's important to note that the CPF numbers are distributed in suppressed form due to privacy. The CNPJ numbers are public information however.    

So we are going to split this column into: 
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

#dropping the CPF_CNPJ column
df = df.drop(('CPF_CNPJ'), axis=1)'''   
)

# Splitting the 'CPF_CNPJ' column into 'LEGAL_ENT' and 'ENT_NUM'
df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'individual' if x.startswith('CPF') else 'company'
    ).astype('category')

df['ENT_NUM'] = df['CPF_CNPJ'].apply(
    lambda x: ''.join(filter(str.isdigit, x.replace(':', '')))
    ).astype('category')

#dropping the CPF_CNPJ column
df = df.drop(('CPF_CNPJ'), axis=1)

st.write(df[['LEGAL_ENT', 'ENT_NUM']])

#converting dtype
df['TYPE_OF_USE'] = df['TYPE_OF_USE'].astype('category')

st.markdown(
'''The columns `MANUFACTURER` and `MODEL` needed more attention because, as they contain text input, they may have different values for the same category.
  
Example: `DJI`, `Dji` and `dji` represents same manufacturer. 

We started with the `MANUFACTURER` column. The `MODEL` column will be transformed in another moment (we will work only with the models provided by the largest drone manufacturer in the database).''')

st.code(
'''#creating function that, given a dataframe column and a map, the names are replaced by standardized names
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name

df['MANUFACTURER'] = df['MANUFACTURER'].str.lower().strip().replace(" ", "")

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

#transforming the column with the manufacturers names
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

#transforming the column with the manufacturers' names
fix_names('MANUFACTURER', fab_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')

#TODO: max weight takeoff analysis

st.write(
'''Finally, the `TYPE_OF_ACTIVITY` column was also validated and transformed. This column categorizes the drones into 'Recreational', 'Experimental', and 'Other activities', the latter category being specified in text provided by the user.'''
)

st.code(
'''#cleaning column
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the column
act_map = {
    'education': 'treinamento|educa|ensin|pesquis',
    'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logistics': 'transport|carga|delivery',
    'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the column dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)

df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'others'

df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')'''
)

#cleaning column
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the column
act_map = {
    'education': 'treinamento|educa|ensin|pesquis',
    'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logistics': 'transport|carga|delivery',
    'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#reclassifying more specific activities into 'other' and converting the column dtype
fix_names('TYPE_OF_ACTIVITY', act_map, df)

df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'others'

df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')

st.markdown(
'Finally, data that would not be used in the analysis were removed from the dataframe.'
)

st.code(
'''#dropping columns that won't be used
df = df.drop([('SERIAL_NUMBER'), ('MAX_WEIGHT_TAKEOFF')], axis=1)''')

#dropping columns that won't be used
df = df.drop([('SERIAL_NUMBER')], axis=1)

st.markdown('>Pre-processed dataframe:')

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

st.subheader('Exploratory dataframe analysis')

st.markdown(
'''Let's start by checking the dates related to each aircraft registration. By comparing information of columns `STATUS`, `REG_DATE` and `EXPIRATON_DATE` we can better understand the rate of adherence to the system and also about the maintenance of these registers. .''')

st.code(
'''#aggregating data by month
agg_data = df.resample('M', on='REG_DATE').count()
agg_data.reset_index(inplace=True)

#creating line plot
fig = px.line(
    agg_data, 
    x='REG_DATE', 
    y='OPERATOR', 
    title='Monthly registrations',
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
fig.update_layout(showlegend=False)

#adding an annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.02,
    y=1.1,
    text=f'The majority ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) of the aircrafts are fine...',
    showarrow=False,
    font=dict(
        color='white',
        size=24,
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

st.markdown(
f'''>Considering the total number of registrations ({df.shape[0]}):
>- {n_inact} ({round(n_inact / df.shape[0] * 100, ndigits=1)}%) are inactive;
>- {n_renew} ({round(n_renew / df.shape[0] * 100, ndigits=1)}%) need to be renewed; and
>- {n_ok} ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) are up to date.''')

#creating and displaying line plot
fig = px.line(
    agg_data, 
    x='REG_DATE', 
    y='OPERATOR', 
    title='Monthly registrations',
    labels={'REG_DATE': '', 'OPERATOR': 'new registers'}
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
fig.update_layout(showlegend=False)

#adding an annotation
fig.add_annotation(
    xref='paper',
    yref='paper',
    x=0.02,
    y=1.1,
    text=f'The majority ({round(n_ok / df.shape[0] * 100, ndigits=1)}%) of the aircrafts are fine...',
    showarrow=False,
    font=dict(
        color='white',
        size=24,
        family='Open Sans'
    )
)

#displaying the histogram plot
st.plotly_chart(fig)

st.code(
'''# Create the pie plot using Plotly Express
fig = px.pie(df, values=df['TYPE_OF_USE'].value_counts(), names=df['TYPE_OF_USE'].value_counts().index.tolist())

# Set pie plot attributes
fig.update_layout(
    title='Distribution of aircrafts by type of use',
    title_font=dict(size=24, family='Open Sans'),
    showlegend=True
    )'''
    )

# Create the pie plot using Plotly Express
fig = px.pie(df, values=df['TYPE_OF_USE'].value_counts(), names=df['TYPE_OF_USE'].value_counts().index.tolist())

# Set pie plot attributes
fig.update_layout(
    title='Distribution of aircrafts by type of use',
    title_font=dict(size=24, family='Open Sans'),
    showlegend=True
    )

# Display the plot
st.plotly_chart(fig)

#TODO: rewrite text, leave insights to plot
st.markdown(
'''To further the understanding of drone usage, the `TYPE_OF_ACTIVITY` column was then evaluated. First, it was observed that the vast majority of drones registered are intended for recreational activities, with 'photography and film' and 'engineering' activities coming soon after.

Additionally, these numbers were compared with the newly created `LEGAL_ENT` column, where it was found that individuals are the majority in almost all activities except engineering and security.'''
)

st.code(
'''#create the histogram plot
fig = px.histogram(df, y='TYPE_OF_ACTIVITY', color='LEGAL_ENT',
                   category_orders={'TYPE_OF_ACTIVITY': df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index},
                   height=500)

#setting histogram plot attributes
fig.update_layout(
    title='Distribution of aircrafts by the type of activity',
    title_font=dict(size=24, family='Open Sans'),
    xaxis=dict(title=None),
    yaxis=dict(title=None)
)'''
)

#create the histogram plot
fig = px.histogram(df, y='TYPE_OF_ACTIVITY', color='LEGAL_ENT',
                   category_orders={'TYPE_OF_ACTIVITY': df['TYPE_OF_ACTIVITY'].value_counts().iloc[:10].index},
                   height=500)

#setting histogram plot attributes
fig.update_layout(
    title='Distribution of aircrafts by the type of activity',
    title_font=dict(size=24, family='Open Sans'),
    xaxis=dict(title=None),
    yaxis=dict(title=None)
)

#displaying plot
st.plotly_chart(fig)

st.markdown(
'''Finally, the questions regarding manufacturers and their aircraft models were analyzed. First a word cloud plot was used (which basically displays words according to their frequency (the higher the frequency, the bigger the word)) to visualize the distribution of manufacturers.'''
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

st.pyplot(fig)

#TODO: fix the percentages
st.markdown(
    f'The manufacturer that supplies most drones is {percentages.index[0].upper()}, as {percentages[0]}% of the drones were made by it. Its followed by {percentages.index[1].upper()} ({percentages[1]}%) and {percentages.index[2].upper()} ({percentages[2]}%). All the other manufacturers together represent {percentages[2:].astype(float).sum()}%.'
)

st.markdown('It was then checked which are the main aircraft models provided by DJI in the system data. For this, the `MODEL` column was finally preprocessed.')

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

applying the fix_names function to the MODEL column
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
    category_orders={'MODEL': dji_df['MODEL'].value_counts().iloc[:14].index}
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

st.markdown('Quais as marcas preferidas dos PF e dos PJ?')

st.code(
'''#creating subsets based on the LEGAL_ENT column
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
        marker_color='lightskyblue'),
    row=1,
    col=1
    )

#adding labels to each bar for individuals plot
for i, count in enumerate(ind_df.value_counts().iloc[:7]):
    fig.add_annotation(
        x=ind_df.value_counts().iloc[:7].index[i],
        y=count,
        text=str(count),
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='bottom'
        )

#creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        x=co_df.value_counts().iloc[:7].index,
        y=co_df.value_counts().iloc[:7],
        marker_color='lightgreen'),
    row=1, 
    col=2
    )

#adding labels to each bar for companies plot
for i, count in enumerate(co_df.value_counts().iloc[:7]):
    fig.add_annotation(
        x=co_df.value_counts().iloc[:7].index[i],
        y=count,
        text=str(count),
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='bottom'
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

#creating subsets based on the LEGAL_ENT column
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
        y=ind_df.value_counts().iloc[:7],               marker_color='lightskyblue'),
    row=1,
    col=1
    )

#adding labels to each bar for individuals plot
for i, count in enumerate(ind_df.value_counts().iloc[:7]):
    fig.add_annotation(
        x=ind_df.value_counts().iloc[:7].index[i],
        y=count,
        text=str(count),
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='bottom'
        )

#creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        x=co_df.value_counts().iloc[:7].index,
        y=co_df.value_counts().iloc[:7],                   marker_color='lightgreen'),
    row=1, 
    col=2
    )

#adding labels to each bar for companies plot
for i, count in enumerate(co_df.value_counts().iloc[:7]):
    fig.add_annotation(
        x=co_df.value_counts().iloc[:7].index[i],
        y=count,
        text=str(count),
        showarrow=False,
        font=dict(size=12),
        xanchor='center',
        yanchor='bottom'
        )

#updating layout and axis labels
fig.update_layout(
    title='Distribution of aircraft manufacturers by legal nature',   title_font=dict(size=24),
    showlegend=False,
    yaxis=dict(title=None),
    yaxis2=dict(title=None)
    )

#displaying
st.plotly_chart(fig)





