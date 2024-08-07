### Importando módulos:
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import text as txt
from PIL import Image
from re import match
from streamlit_extras.metric_cards import style_metric_cards
from wordcloud import WordCloud

#Styling & useful settings
pd.options.mode.chained_assignment = None
st.set_page_config(page_title="ANAC UAV Database")
style_metric_cards(
    background_color=None, border_color="#cccccc", border_left_color="#cccccc"
)
title_font = dict(color="rgb(150,150,150)", family="Roboto", size=24)



# loading CSS style
# with open('style.css') as css:
#     st.markdown(
#         f'<style>{css.read()}</style>',
#         unsafe_allow_html=True
#     )

# setting up the sidebar
left_co, cent_co, right_co = st.sidebar.columns([0.4, 0.2, 0.4])
with cent_co:
    lang = st.sidebar.radio(
        label="Select your language:",
        options=[":flag-us: english", ":flag-br: pt-br"],
        label_visibility="visible",
        horizontal=True
    )

lang = "en" if lang == ":flag-us: english" else "pt-br"
st.sidebar.markdown(txt.SB_TITLE.get(lang))
st.sidebar.markdown(txt.SECTIONS.get(lang))

st.sidebar.markdown(txt.SB_MENU1.get(lang))
st.sidebar.markdown(txt.SB_MENU2.get(lang))
st.sidebar.markdown(txt.SB_MENU3.get(lang))

# creating the document
st.header(
    txt.HEADER.get(lang),
    divider="rainbow",
)

left_co, cent_co, right_co = st.columns([0.2, 0.6, 0.2])
with cent_co:
    img = Image.open("img/drone.jpg")
    new_img = img.resize((int(img.width * 0.05), int(img.height * 0.05)))
    st.image(new_img)

st.markdown(txt.INTRO1.get(lang))
 
st.markdown(txt.INTRO2.get(lang))

st.markdown(txt.INTRO3.get(lang))

# loading data, dropping NAs and renaming features
@st.cache_resource(ttl="3d")
def download_data(url):
    df = pd.read_csv(
        url,
        delimiter=";",
        skiprows=1,
        parse_dates=["DATA_VALIDADE"],
        #date_parser=lambda x: pd.to_datetime(x, format=r"%d/%m/%Y"),
        date_format="%d/%m/%Y"
    )
    return df

try:
    url = r"https://sistemas.anac.gov.br/dadosabertos/Aeronaves/drones%20cadastrados/SISANT.csv"
    
    df = download_data(url)

except Exception as e:
    st.error(f"The data could not be downloaded. Error: {e}")

df.dropna(inplace=True)

df.columns = [
    "AIRCRAFT_ID",
    "EXPIRATION_DATE",
    "OPERATOR",
    "CPF_CNPJ",
    "TYPE_OF_USE",
    "MANUFACTURER",
    "MODEL",
    "SERIAL_NUMBER",
    "MAX_WEIGHT_TAKEOFF",
    "TYPE_OF_ACTIVITY",
]

st.info(
    txt.INFO.get(lang),
    icon="📊",
)

st.write(txt.BLT_FEATURES.get(lang))

with st.container():
    import io

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(info_string)

st.dataframe(df, height=250, use_container_width=True)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code("""
            #importing libs
            import numpy as np
            import pandas as pd
            import streamlit as st
            import matplotlib.pyplot as plt
            import plotly.express as px
            import plotly.graph_objects as go
            import plotly.subplots as sp
            from PIL import Image
            from re import match
            from wordcloud import WordCloud

            # loading data, dropping NAs and renaming features
url = r"https://sistemas.anac.gov.br/dadosabertos/Aeronaves/drones%20cadastrados/SISANT.csv"

try:
    df = pd.read_csv(
        url,
        delimiter=";",
        skiprows=1,
        parse_dates=["DATA_VALIDADE"],
        date_parser=lambda x: pd.to_datetime(x, format=r"%d/%m/%Y"),
    )

except Exception as e:
    st.error(f"The data could not be downloaded. Error: {e}")

df.dropna(inplace=True)

df.columns = [
    "AIRCRAFT_ID",
    "EXPIRATION_DATE",
    "OPERATOR",
    "CPF_CNPJ",
    "TYPE_OF_USE",
    "MANUFACTURER",
    "MODEL",
    "SERIAL_NUMBER",
    "MAX_WEIGHT_TAKEOFF",
    "TYPE_OF_ACTIVITY",
]
                """)

st.write("___")
st.subheader("Dataframe metadata:")

left_co, cent_co, right_co = st.columns([0.1, 0.8, 0.1])
with cent_co:
    img = Image.open("img/features.jpg")
    # new_img = img.resize(
    #     (
    #         int(img.width * 0.05),
    #         int(img.height * 0.05)
    #         )
    #     )
    st.image(img)

st.markdown(txt.METADATA.get(lang))

st.subheader("Data pre-processing")

left_co, cent_co, right_co = st.columns([0.1, 0.8, 0.1])
with cent_co:
    img = Image.open("img/aerial_farm.jpg")
    st.image(img)

st.markdown(txt.DPP_MD1.get(lang))

# checking the duplicates
dupl = df[df.duplicated(subset=["AIRCRAFT_ID"], keep=False)]

# removing whitespaces
df["AIRCRAFT_ID"] = df["AIRCRAFT_ID"].str.replace(" ", "")

# removing duplicates
df = df.drop_duplicates(subset=["AIRCRAFT_ID"], keep="last")

# check if the ID codes for each aircraft comply to the patterns set in the metadata, and removing those that do not.
nrows_before = df.shape[0]

pattern = r"^(PR|PP|PS)-\d{9}$"
mask = [bool(match(pattern, code)) for code in df["AIRCRAFT_ID"]]
df = df[mask]

nrows_after = df.shape[0]

st.markdown(
    f""":x: Duplicated entries: {dupl.shape[0]}    
:x: Invalid ID entries: **{nrows_before - nrows_after}**    
:heavy_check_mark: Valid entries in the dataframe: **{nrows_after}**"""
)

# setting index:
df = df.set_index(df["AIRCRAFT_ID"])
df = df.drop(("AIRCRAFT_ID"), axis=1)

st.dataframe(df, height=250, use_container_width=True)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code("""
    #removing whitespaces
    df['AIRCRAFT_ID'] = df['AIRCRAFT_ID'].str.replace(" ", "")

    #removing duplicates
    df = df.drop_duplicates(subset=['AIRCRAFT_ID'], keep='last')

    #ensuring that all ID codes comply to the patterns set in the metadata
    pattern = r'^(PR|PP|PS)-\d{9}$'
    mask = [bool(match(pattern, code)) for code in df['AIRCRAFT_ID']]
    df = df[mask]

    #setting index
    df = df.set_index(df['AIRCRAFT_ID'])
    df = df.drop(('AIRCRAFT_ID'), axis=1)""")

st.markdown(txt.DPP_MD2.get(lang))

# creating a function that sorts dates according to register status (register ok, renew ou inactive)
def reg_status(date):
    today = pd.Timestamp.today()
    if date < today:
        return "renew"
    elif date < today - pd.DateOffset(months=6):
        return "inactive"
    else:
        return "ok"


# creating a 'STATUS' feature, containing categorized data about each aircraft
df["STATUS"] = df["EXPIRATION_DATE"].apply(reg_status)
df["STATUS"] = df["STATUS"].astype("category")

# creating feature 'REG_DATE'
df["REG_DATE"] = df["EXPIRATION_DATE"] - pd.DateOffset(years=2)

# st.write(df[['STATUS', 'REG_DATE']])

# st.markdown(
# '''Following, the `CPF_CNPJ` feature was worked on.'''
# )

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#     '''#removing whitespaces from the 'CPF_CNPJ'
#     df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")'''
#     )

# removing whitespaces from the 'CPF_CNPJ'
df["CPF_CNPJ"] = df["CPF_CNPJ"].str.replace(" ", "")

st.markdown(txt.DPP_MD3.get(lang))

# st.write(df['CPF_CNPJ'])

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#     '''df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
#         lambda x: 'individual' if x.startswith('CPF') else 'company'
#         ).astype('category')

#     df['ENT_NUM'] = df['CPF_CNPJ'].apply(
#         lambda x: ''.join(filter(str.isdigit, x.replace(':', '')))
#         ).astype('category')

#     #dropping CPF_CNPJ
#     df = df.drop(('CPF_CNPJ'), axis=1)'''
#     )

# Splitting the 'CPF_CNPJ' feature into 'LEGAL_ENT' and 'ENT_NUM'
df["LEGAL_ENT"] = (
    df["CPF_CNPJ"]
    .apply(lambda x: "individual" if x.startswith("CPF") else "company")
    .astype("category")
)

df["ENT_NUM"] = (
    df["CPF_CNPJ"]
    .apply(lambda x: "".join(filter(str.isdigit, x.replace(":", ""))))
    .astype("category")
)

# dropping CPF_CNPJ
df = df.drop(("CPF_CNPJ"), axis=1)

# st.write(df[['LEGAL_ENT', 'ENT_NUM']])
st.write(df[["STATUS", "REG_DATE", "LEGAL_ENT", "ENT_NUM"]])

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """#function that sorts dates according to register status
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

#removing whitespaces from the 'CPF_CNPJ'
df['CPF_CNPJ'] = df['CPF_CNPJ'].str.replace(" ", "")

#splitting the 'CPF_CNPJ' feature into 'LEGAL_ENT' and 'ENT_NUM'
df['LEGAL_ENT'] = df['CPF_CNPJ'].apply(
    lambda x: 'individual' if x.startswith('CPF') else 'company'
    ).astype('category')

df['ENT_NUM'] = df['CPF_CNPJ'].apply(
    lambda x: ''.join(filter(str.isdigit, x.replace(':', '')))
    ).astype('category')

#dropping CPF_CNPJ
df = df.drop(('CPF_CNPJ'), axis=1)"""
    )

# converting dtype
df["TYPE_OF_USE"] = (
    df["TYPE_OF_USE"]
    .apply(lambda x: "basic" if x == "Básico" else "advanced")
    .astype("category")
)
# df['TYPE_OF_USE'] = df['TYPE_OF_USE'].astype('category')


st.markdown(txt.DPP_MD4.get(lang))

# creating function so that, given a dataframe column and a map, the names are replaced by standardized names
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name


df["MANUFACTURER"] = df["MANUFACTURER"].str.lower()
df["MANUFACTURER"] = df["MANUFACTURER"].str.replace(" ", "")

# the dictionary was created based on the most common values, however, given the high amount of unique values, lesser expressed and unknown manufacturers were grouped in the 'others' category
man_map = {
    "autelrobotics": "autel",
    "c-fly": "cfly|c-fly",
    "custom": "fabrica|aeromodelo|propria|própria|proprio|próprio|caseiro|montado|artesanal|constru",
    "dji": "dji|mavic|phanton|phantom",
    "flyingcircus": "circus",
    "geprc": "gepr",
    "highgreat": "highgreat",
    "horus": "horus",
    "hubsan": "hubsan|hubsen",
    "lumasky": "lumasky",
    "kfplan": "kfp",
    "nuvemuav": "nuvem",
    "others": "outro",
    "parrot": "parrot",
    "phoenixmodel": "phoenix",
    "santiago-cintra": "santiago|cintra",
    "sensefly": "sensefly",
    "speedbird-aero": "speedbird",
    "crostars": "crostar",
    "shantou": "shantou",
    "sjrc": "sjrc|srjc",
    "visuo": "visuo",
    "x-fly": "xfly|x-fly",
    "xiaomi": "xiaomi|fimi|xiomi",
    "xmobots": "xmobots",
    "zll": "zll|sg906",
}

# transforming the feature with the manufacturers' names
fix_names("MANUFACTURER", man_map)

df["MANUFACTURER"] = df["MANUFACTURER"].astype("category")

# st.write(
# '''Finally, the `TYPE_OF_ACTIVITY` feature was also validated and transformed. It categorizes the drones into 'Recreational', 'Experimental', and 'Other activities', the latter category being specified in text provided by the user.'''
# )

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#     '''#cleaning feature
#     df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
#     df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#     #again transforming the values of the feature
#     act_map = {
#         'education': 'treinamento|educa|ensin|pesquis',
#         'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',
#         'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
#         'logistics': 'transport|carga|delivery',
#         'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
#         'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
#         }

#     #reclassifying more specific activities into 'other' and converting the feature dtype
#     fix_names('TYPE_OF_ACTIVITY', act_map, df)

#     df.loc[
#         ~df['TYPE_OF_ACTIVITY'].isin(
#             df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
#             ), 'TYPE_OF_ACTIVITY'
#         ] = 'others'

#     df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')'''
#     )

# cleaning feature
df["TYPE_OF_ACTIVITY"] = df["TYPE_OF_ACTIVITY"].str.replace(" ", "")
df["TYPE_OF_ACTIVITY"] = df["TYPE_OF_ACTIVITY"].str.lower()

# again transforming the values of the feature
act_map = {
    "education": "treinamento|educa|ensin|pesquis",
    "engineering": "pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente",
    "photo&film": "fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis",
    "logistics": "transport|carga|delivery",
    "publicity": "publicid|letreir|show|marketing|demonstr|eventos|comercial",
    "recreative": "recreativo",
    "safety": "seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura",
}

# reclassifying more specific activities into 'other' and converting the feature dtype
fix_names("TYPE_OF_ACTIVITY", act_map, df)

df.loc[
    ~df["TYPE_OF_ACTIVITY"].isin(df["TYPE_OF_ACTIVITY"].value_counts().head(8).index),
    "TYPE_OF_ACTIVITY",
] = "others"

df["TYPE_OF_ACTIVITY"] = df["TYPE_OF_ACTIVITY"].astype("category")
df["OPERATOR"] = df["OPERATOR"].astype("string")
df["MODEL"] = df["MODEL"].astype("string")

# dropping features that won't be used
df = df.drop(["SERIAL_NUMBER", "MAX_WEIGHT_TAKEOFF"], axis=1)

# st.markdown(
# 'Lastly, features that would not be used in the analysis were removed from the dataframe.'
# )

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#     '''#dropping features that won't be used
#     df = df.drop(
#         [('SERIAL_NUMBER'), ('MAX_WEIGHT_TAKEOFF')],
#         axis=1
#         )''')

st.markdown(txt.BLT_DDF.get(lang))

with st.container():
    import io

    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    st.code(info_string)

st.write(df)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """#creating function for fixing the names based on a map
def fix_names(column, namemap, df=df):
    for fixed_name, bad_names in namemap.items():
        df.loc[df[column].str.contains(bad_names, regex=True), column] = fixed_name
        
#setting lowercase and removing whitespaces
df['MANUFACTURER'] = df['MANUFACTURER'].str.lower()
df['MANUFACTURER'] = df['MANUFACTURER'].str.replace(" ", "")

#the following map was created based on the most common values
man_map = {
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
fix_names('MANUFACTURER', man_map)

df['MANUFACTURER'] = df['MANUFACTURER'].astype('category')

#now its time to fix the 'TYPE_OF_ACTIVITY'
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.replace(" ", "")
df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].str.lower()

#again transforming the values of the feature based on a map
act_map = {
    'education': 'treinamento|educa|ensin|pesquis',
    'engineering': 'pulveriz|aeroagr|agricultura|levantamento|fotograme|prospec|topografia|minera|capta|avalia|mapea|geoproc|engenharia|energia|solar|ambiental|constru|obras|industria|arquitetura|meioambiente',    
    'photo&film': 'fotografia|cinema|inspe|vídeo|video|fotos|jornal|filma|maker|audit|monit|perícia|audiovisu|vistoria|imagens|turismo|youtube|imobili|imóveis',
    'logistics': 'transport|carga|delivery',
    'publicity': 'publicid|letreir|show|marketing|demonstr|eventos|comercial',
    'recreative': 'recreativo',
    'safety': 'seguran|fiscaliza|reporta|vigi|policia|bombeiro|defesa|combate|emergencia|infraestrutura'
    }

#transformin the feature
fix_names('TYPE_OF_ACTIVITY', act_map, df)

df.loc[
    ~df['TYPE_OF_ACTIVITY'].isin(
        df['TYPE_OF_ACTIVITY'].value_counts().head(8).index
        ), 'TYPE_OF_ACTIVITY'
    ] = 'others'

df['TYPE_OF_ACTIVITY'] = df['TYPE_OF_ACTIVITY'].astype('category')

df = df.drop(
    ['OPERATOR', 'SERIAL_NUMBER', 'MAX_WEIGHT_TAKEOFF'],
    axis=1
    )
"""
    )

st.divider()

st.subheader(txt.EX_SUBHEADER.get(lang))

left_co, cent_co, right_co = st.columns([0.1, 0.8, 0.1])
with cent_co:
    img = Image.open("img/aerial_roof.jpg")
    # new_img = img.resize(
    #     (
    #         int(img.width * 0.05),
    #         int(img.height * 0.05)
    #         )
    #     )
    st.image(img)

st.markdown(txt.EX_MD1.get(lang))

# aggregating data by month
agg_data = df.resample("ME", on="REG_DATE").count()
agg_data.reset_index(inplace=True)

# creating and displaying line plot
fig = px.line(
    agg_data,
    x="REG_DATE",
    y="OPERATOR",
    title=None,
    labels={"REG_DATE": "", "OPERATOR": "new registers"},
)

# adding a customized title
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0,
    y=1.1,
    text="Compliance with the system has increased over the time",
    showarrow=False,
    font=title_font,
)

st.plotly_chart(fig, use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    week_data = df.resample("W", on="REG_DATE").count()
    st.metric(
        label="New registers this week:",
        value=week_data.OPERATOR.iloc[-1],
    )
with col2:
    st.metric(
        label="Registers last six months:", value=agg_data.OPERATOR.iloc[-7:-1].sum()
    )
with col3:
    st.metric(label="Total registers:", value=df.shape[0])

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """
    #aggregating data by month
    agg_data = df.resample('M', on='REG_DATE').count()
    agg_data.reset_index(inplace=True)

    #creating line plot
    fig = px.line(
        agg_data, 
        x='REG_DATE', 
        y='OPERATOR', 
        title=None,
        labels={'REG_DATE': '', 'OPERATOR': 'new registers'}
        )

    #adding a customized title
    fig.add_annotation(
        xref='paper', yref='paper',
        x=0, y=1.1,
        text="Compliance with the system has increased over the time",
        showarrow=False,
        font=dict(
            color='rgb(150,150,150)',
            size=22,
            family='Arial'
        )
    )
    
    #displaying line plot    
    st.plotly_chart(fig)

    #displaying metrics cards
    col1, col2, col3 = st.columns(3)
    with col1:
        week_data = df.resample('W', on='REG_DATE').count()
        st.metric(
            label="New registers this week:",
            value=week_data.OPERATOR.iloc[-1],
        )
    with col2:
        st.metric(
            label="Registers last six months:",
            value=agg_data.OPERATOR.iloc[-7:-1].sum()
        )
    with col3:
        st.metric(
            label="Total registers:",
            value=df.shape[0]
            )"""
    )

# calculating the number of aircraft in each category
n_inact = df[df["STATUS"] == "inactive"].shape[0]
n_renew = df[df["STATUS"] == "renew"].shape[0]
n_ok = df[df["STATUS"] == "ok"].shape[0]

fig = go.Figure()

# creating the gauge plot
fig.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=round(n_ok / df.shape[0] * 100, ndigits=1),
        number=dict(suffix="%"),
        title=None,
        gauge=dict(axis=dict(range=[0, 100], ticksuffix="%")),
    )
)

# adding a customized title
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0,
    y=1.2,
    text="Active drones are in the majority",
    showarrow=False,
    font=title_font,
)

st.plotly_chart(fig)

# creating the card metrics
col1, col2 = st.columns(2)
with col1:
    week_data = df.resample("W", on="REG_DATE").count()
    st.metric(label="Expiring drone licenses:", value=n_renew)
with col2:
    st.metric(label="Expired:", value=n_inact)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """
        #calculating the number of aircraft in each category
        n_inact = df[df['STATUS']=='inactive'].shape[0]
        n_renew = df[df['STATUS']=='renew'].shape[0]
        n_ok = df[df['STATUS']=='ok'].shape[0]

        fig = go.Figure()

        #creating the gauge plot
        fig.add_trace(
            go.Indicator(
                mode = "gauge+number",
                value = round(n_ok / df.shape[0] * 100, ndigits=1),
                number=dict(
                    suffix="%"
                ),
                title = None,
                gauge=dict(
                    axis=dict(
                        range=[0, 100],
                        ticksuffix="%"
                        )
                    )
                )
            )

        #adding a customized title
        fig.add_annotation(
            xref='paper', yref='paper',
            x=0, y=1.2,
            text="Active drones are in the majority",
            showarrow=False,
            font=dict(
                color='rgb(150,150,150)',
                size=22,
                family='Arial'
            )
        )

        st.plotly_chart(fig)

        #creating the card metrics
        col1, col2 = st.columns(2)
        with col1:
            week_data = df.resample('W', on='REG_DATE').count()
            st.metric(
                label="Expiring drone licenses:",
                value=n_renew
            )
        with col2:
            st.metric(
                label="Expired:",
                value=n_inact
            )"""
    )

st.markdown(txt.EX_MD2.get(lang))

# calculate the value counts for each type of use
value_counts = df["TYPE_OF_USE"].value_counts()

# creating an indicator chart
fig = go.Figure(
    go.Indicator(
        mode="number",
        title=dict(text="Currently,"),
        value=value_counts.values[0] / value_counts.sum() * 100,
        number=dict(suffix="%", font=dict(family="Open Sans", size=96)),
        domain=dict(x=[0, 1], y=[0.6, 1]),
    )
)

# adding text to the chart
fig.add_annotation(
    xref="paper",
    yref="paper",
    xanchor="center",
    yanchor="middle",
    x=0.5,
    y=0.5,
    text="of the aircrafts are in basic operations<br><span style='color:gray'>(up to 25 kg, operated within line of sight and below 400 ft).</span>",
    font=dict(color="white", size=20, family="Open Sans"),
    showarrow=False,
)

# adding more text to the chart
fig.add_annotation(
    xref="paper",
    yref="paper",
    xanchor="center",
    yanchor="middle",
    x=0.5,
    y=0.01,
    text=f"<span style='color:gray'>There are only</span><br><br><span style='font-size:48px'>{value_counts.values[1]}</span><br>UAVs registered for advanced operations.",
    font=dict(color="white", size=20, family="Open Sans"),
    showarrow=False,
)

# setting the chart's background to transparent
fig.update_layout(dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"))

st.plotly_chart(fig)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """#calculate the value counts for each type of use
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
    )"""
    )

st.markdown(txt.EX_MD3.get(lang))

# create the histogram plot
fig = px.histogram(
    df,
    y="TYPE_OF_ACTIVITY",
    color="LEGAL_ENT",
    category_orders={
        "TYPE_OF_ACTIVITY": df["TYPE_OF_ACTIVITY"].value_counts().iloc[:10].index
    },
    height=500,
)

# setting histogram plot attributes
fig.update_layout(
    legend=dict(
        title=None,
        xanchor="right",
        yanchor="bottom",
        x=0.92,
        y=0.05,
    ),
    xaxis=dict(title=None),
    yaxis=dict(title=None),
)

fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0,
    y=1.15,
    text="Recreational drones are in the majority",
    showarrow=False,
    font=title_font,
)

fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0,
    y=1.08,
    text="and they are the favorite of the individuals.",
    showarrow=False,
    font=dict(color="white", size=16, family="Open Sans"),
)

# displaying plot
st.plotly_chart(fig)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """#create the histogram plot
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
    )"""
    )

st.markdown(txt.EX_MD4.get(lang))

counts = df["MANUFACTURER"].value_counts()
percentages = counts / counts.sum()
percentages = percentages.apply(lambda x: f"{round(x * 100, 1)}")

# creating figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_alpha(0.0)
fig.patch.set_edgecolor('white')

def create_wordcloud(image):
    mask = Image.open(image)
    mask = np.array(mask)
    wordcloud = WordCloud(
        width=1200,
        height=600,
        mask=mask,
        relative_scaling=0.4,
        max_words=2000,
        min_word_length=3,
        colormap="tab10",
    ).generate_from_frequencies(
        df["MANUFACTURER"].value_counts()
        .drop(labels=["custom", "others"])
        .to_dict()
    )
    return wordcloud

#creating wordcloud
wordcloud = create_wordcloud("img/brazil_mask.png")

# setting axis attributes
ax.axis("off")
ax.imshow(wordcloud, interpolation="bilinear")

st.markdown(
    f"""<p style="text-align:center"><span style="font-family:Gravitas One,sans-serif"><span style="color:#ffffff"><strong><span style="font-size:32px">{percentages.iloc[0]}% of the registered brazilian drones<br>were provided by {percentages.index[0].upper()}.</span></strong></span><br><span style="color:#dddddd"><span style="font-size:18px"> {percentages.index[1].upper()} ({percentages.iloc[1]}%) and {percentages.index[2].upper()} ({percentages.iloc[2]}%) come next.</span></span><br><span style="color:#999999"><span style="font-size:16px">Each of the other manufacturers are represented by {percentages.iloc[3]}% or less of the registered aircrafts.</span></span></span></p>""",
    unsafe_allow_html=True,
)

st.pyplot(fig)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """#creating figure and axis
    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_alpha(0.0)

    #creating word cloud
    brazil_mask = Image.open("img/brazil_mask.png")
    brazil_mask = np.array(brazil_mask)
    wordcloud = WordCloud(   
    width=1200, height=600,
    mask=brazil_mask,
    relative_scaling=0.4,
    max_words=2000,
    min_word_length=3,
    colormap='tab10'
    ).generate_from_frequencies(
        df['MANUFACTURER'].value_counts().drop(labels=['custom', 'others'])
        )

    #setting axis attributes
    ax.axis("off")
    ax.imshow(wordcloud, interpolation='bilinear')"""
    )
    
st.markdown(txt.EX_MD5.get(lang))

st.info(txt.INFO2.get(lang), icon="🚀")

# st.markdown(
#     "It was then checked which are the main aircraft models provided by DJI in the system data. For this, the `MODEL` feature was finally preprocessed."
# )

# # criando subset contendo os drones fabricados pela dji
# dji_df = df.loc[df["MANUFACTURER"] == "dji"]

# # removendo espaços em branco
# dji_df["MODEL"] = dji_df["MODEL"].str.lower()
# dji_df["MODEL"] = dji_df["MODEL"].str.replace(" ", "")

# # criando dicionário de modelos
# dji_model_map = {
#     "mavic": "mav|air|ma2ue3w|m1p|da2sue1|1ss5|u11x|rc231|m2e|l1p|enterprisedual",
#     "phantom": "phan|wm331a|p4p|w322b|p4mult|w323|wm332a|hanto",
#     "mini": "min|mt2pd|mt2ss5|djimi|mt3m3vd",
#     "spark": "spa|mm1a",
#     "matrice": "matrice|m300",
#     "avata": "avata|qf2w4k",
#     "inspire": "inspire",
#     "tello": "tello|tlw004",
#     "agras": "agras|mg-1p|mg1p|t16|t10|t40|3wwdz",
#     "fpv": "fpv",
#     "others": "dji",
# }

# # novamente utilizando a função fix_names, dessa vez com argumentos
# # relativos a coluna MODEL
# fix_names("MODEL", dji_model_map, dji_df)

# # renomeando modelos não reconhecidos como "others"
# dji_df.loc[
#     ~dji_df["MODEL"].isin(dji_df["MODEL"].value_counts().head(14).index), "MODEL"
# ] = "others"

# dji_df["MODEL"] = dji_df["MODEL"].astype("category")

# # creating the histogram plot
# fig = px.histogram(
#     dji_df,
#     y="MODEL",
#     category_orders={"MODEL": dji_df["MODEL"].value_counts().iloc[:14].index},
#     text_auto=True,
# )

# # set histogram plot attributes
# fig.update_layout(
#     title="Distribution of aircraft models manufactured by DJI in SISANT",
#     title_font=dict(size=24),
#     xaxis=dict(title=None),
#     yaxis=dict(title=None),
# )

# # Display the plot
# st.plotly_chart(fig)

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#         """#creating subset containing dji aircrafts
#     dji_df = df.loc[df['MANUFACTURER']=='dji']

#     #cleaning whitespaces
#     dji_df['MODEL'] = dji_df['MODEL'].str.lower()
#     dji_df['MODEL'] = dji_df['MODEL'].str.replace(" ", "")

#     #creating a model dictionary
#     dji_model_map = {
#         'mavic': 'mav|air|ma2ue3w|m1p|da2sue1|1ss5|u11x|rc231|m2e|l1p|enterprisedual',
#         'phantom': 'phan|wm331a|p4p|w322b|p4mult|w323|wm332a|hanto',
#         'mini': 'min|mt2pd|mt2ss5|djimi|mt3m3vd',
#         'spark': 'spa|mm1a',
#         'matrice': 'matrice|m300',
#         'avata': 'avata|qf2w4k',
#         'inspire': 'inspire',
#         'tello': 'tello|tlw004',
#         'agras': 'agras|mg-1p|mg1p|t16|t10|t40|3wwdz',
#         'fpv': 'fpv',
#         'others': 'dji'
#         }

#     applying the fix_names function to the MODEL feature
#     fix_names('MODEL', dji_model_map, dji_df)

#     #renaming unknown models as "others"
#     dji_df.loc[~dji_df['MODEL'].isin(dji_df['MODEL'].value_counts().head(14).index), 'MODEL'] = 'others'

#     dji_df['MODEL'] = dji_df['MODEL'].astype('category')

#     #creating the histogram plot
#     fig = px.histogram(
#         dji_df, 
#         y='MODEL',
#         category_orders={'MODEL': dji_df['MODEL'].value_counts().iloc[:14].index}
#         )

#     #set histogram plot attributes
#     fig.update_layout(
#         title='Distribution of aircraft models manufactured by DJI in SISANT',
#         title_font=dict(size=24),
#         xaxis=dict(title=None),
#         yaxis=dict(title=None),
#     )"""
#     )

# st.markdown("Which brands do individuals and companies prefer?")

# with st.expander(txt.CHECK_CODE.get(lang):
#     st.code(
#         """#creating subsets based on LEGAL_ENT
#     ind_df = df.loc[df['LEGAL_ENT'] == 'individual', 'MANUFACTURER']
#     co_df = df.loc[df['LEGAL_ENT'] == 'company', 'MANUFACTURER']

#     #creating figure and subplots
#     fig = sp.make_subplots(
#         rows=1, 
#         cols=2, 
#         subplot_titles=('individuals', 'companies'), 
#         shared_yaxes=True
#         )

#     #creating the first histogram plot (individuals)
#     fig.add_trace(
#         go.Bar(
#             x=ind_df.value_counts().iloc[:7].index,
#             y=ind_df.value_counts().iloc[:7],
#             marker_color='lightskyblue',
#             text=ind_df.value_counts().iloc[:7],
#             ),
#         row=1,
#         col=1
#         )

#     #creating the second histogram plot (companies)
#     fig.add_trace(
#         go.Bar(
#             x=co_df.value_counts().iloc[:7].index,
#             y=co_df.value_counts().iloc[:7],
#             marker_color='lightgreen',
#             text=co_df.value_counts().iloc[:7],
#             ),
#         row=1, 
#         col=2
#         )

#     #updating layout and axis labels
#     fig.update_layout(
#         title='Distribution of aircraft manufacturers by legal nature',
#         title_font=dict(size=24),
#         showlegend=False,
#         yaxis=dict(title=None),
#         yaxis2=dict(title=None)
#         )"""
#     )

# # creating subsets based on LEGAL_ENT
# ind_df = df.loc[df["LEGAL_ENT"] == "individual", "MANUFACTURER"]
# co_df = df.loc[df["LEGAL_ENT"] == "company", "MANUFACTURER"]

# # creating figure and subplots
# fig = sp.make_subplots(
#     rows=1, cols=2, subplot_titles=("individuals", "companies"), shared_yaxes=True
# )

# # creating the first histogram plot (individuals)
# fig.add_trace(
#     go.Bar(
#         x=ind_df.value_counts().iloc[:7].index,
#         y=ind_df.value_counts().iloc[:7],
#         marker_color="lightskyblue",
#         text=ind_df.value_counts().iloc[:7],
#     ),
#     row=1,
#     col=1,
# )

# # creating the second histogram plot (companies)
# fig.add_trace(
#     go.Bar(
#         x=co_df.value_counts().iloc[:7].index,
#         y=co_df.value_counts().iloc[:7],
#         marker_color="lightgreen",
#         text=co_df.value_counts().iloc[:7],
#     ),
#     row=1,
#     col=2,
# )

# # updating layout and axis labels
# fig.update_layout(
#     title="Distribution of aircraft manufacturers...",
#     title_font=dict(size=24),
#     showlegend=False,
#     yaxis=dict(title=None),
#     yaxis2=dict(title=None),
# )

# # displaying
# st.plotly_chart(fig)

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

# ind_models = dji_df.loc[dji_df["LEGAL_ENT"] == "individual", "MODEL"]

# co_models = dji_df.loc[dji_df["LEGAL_ENT"] == "company", "MODEL"]

# # creating figure and subplots
# fig = sp.make_subplots(
#     rows=1, cols=2, subplot_titles=("individuals", "companies"), shared_yaxes=True
# )

# # creating the first histogram plot (individuals)
# fig.add_trace(
#     go.Bar(
#         x=ind_models.value_counts().iloc[:7].index,
#         y=ind_models.value_counts().iloc[:7],
#         # marker_color='lightskyblue',
#         text=ind_models.value_counts().iloc[:7],
#     ),
#     row=1,
#     col=1,
# )

# # creating the second histogram plot (companies)
# fig.add_trace(
#     go.Bar(
#         x=co_models.value_counts().iloc[:7].index,
#         y=co_models.value_counts().iloc[:7],
#         # marker_color='lightgreen',
#         text=co_models.value_counts().iloc[:7],
#     ),
#     row=1,
#     col=2,
# )

# # updating layout and axis labels
# fig.update_layout(
#     title="...and the distribution of DJI models.",
#     title_font=dict(size=24),
#     title_x=0.45,
#     showlegend=False,
#     yaxis=dict(title=None),
#     yaxis2=dict(title=None),
# )

# # displaying
# st.plotly_chart(fig)

# #//CONSULT CNPJS TO CHECK WHICH BRAZILIAN STATE THE DRONE WAS REGISTERED IN
# co_ids = df.loc[df['LEGAL_ENT'] == 'company']

# def get_cnpj_data(cnpj):  # sourcery skip: raise-specific-error
#     api_url = 'https://minhareceita.org'
#     r = requests.get(
#         f"{api_url}/{cnpj}"
#     )
#     if r.status_code != 200:
#         raise Exception(f'Erro na API: {r.status_code}')
#     try:
#         r_dict = json.loads(r.content)
#         return r_dict.get('uf')
#     except:
#         return 0


# Group by MANUFACTURER and use pd.Grouper to group by month, then unstack to pivot the data
manuf_count = (
    df.groupby(["MANUFACTURER", pd.Grouper(key="REG_DATE", freq="ME")], observed=False)
    .size()
    .unstack(fill_value=0)
)

top10_manuf = df["MANUFACTURER"].value_counts().index[:12].drop(["custom", "others"])

fig = go.Figure()

for act in top10_manuf:
    fig.add_trace(
        go.Scatter(
            x=manuf_count.loc[act].index, y=manuf_count.loc[act], name=act, mode="lines"
        )
    )

fig.add_annotation(
    text="Although DJI UAV always represented a large part of the new <br>registrations in the system, other manufacturers sometimes cause <br> some spikes in the number of registrations.",
    align="left",
    xref="paper",
    yref="paper",
    x=0,
    y=1.3,
    showarrow=False,
    font=dict(color="rgb(150,150,150)", family="Roboto", size=20),
)

st.plotly_chart(fig)

# Group by TYPE_OF_ACTIVITY and use pd.Grouper to group by month, then unstack to pivot the data
act_count = (
    df.groupby(
        ["TYPE_OF_ACTIVITY", pd.Grouper(key="REG_DATE", freq="ME")], observed=False
    )
    .size()
    .unstack(fill_value=0)
)

top10_act = df["TYPE_OF_ACTIVITY"].value_counts().index

fig = go.Figure()

for act in top10_act:
    fig.add_trace(go.Scatter(x=act_count.loc[act].index, y=act_count.loc[act], name=act, mode="lines"))

fig.add_annotation(
    text="""Recreation”, “photo & filming”, and “engineering” had the<br>most registrations over time. Recently, there was a surge in<br>UAV registrations for “publicity”""",
    align="left",
    xref="paper",
    yref="paper",
    x=0,
    y=1.3,
    showarrow=False,
    font=dict(color="rgb(150,150,150)", family="Roboto", size=20),
)

st.plotly_chart(fig)

with st.expander(txt.CHECK_CODE.get(lang)):
    st.code(
        """# Group by TYPE_OF_ACTIVITY and use pd.Grouper to group by month, then unstack to pivot the data
act_count = (
    df.groupby(["TYPE_OF_ACTIVITY", pd.Grouper(key="REG_DATE", freq="M")])
    .size()
    .unstack(fill_value=0)
)

top10_act = df["TYPE_OF_ACTIVITY"].value_counts().index

fig = go.Figure()

for act in top10_act:
    fig.add_trace(go.Scatter(x=act_count.loc[act].index, y=act_count.loc[act], name=act, mode="lines"))

fig.add_annotation(
    text="Recreation”, “photo & filming”, and “engineering” had the<br>most registrations over time. Recently, there was a surge in<br>UAV registrations for “publicity”",
    align="left",
    xref="paper",
    yref="paper",
    x=0,
    y=1.3,
    showarrow=False,
    font=dict(color="rgb(150,150,150)", family="Roboto", size=20),
)

st.plotly_chart(fig)""")

# creating subsets based on LEGAL_ENT
ind_df = df.loc[df["LEGAL_ENT"] == "individual", "MANUFACTURER"]
co_df = df.loc[df["LEGAL_ENT"] == "company", "MANUFACTURER"]

# creating figure and subplots
fig = sp.make_subplots(
    rows=1, 
    cols=2, 
    #subplot_titles=("individuals", "companies"), 
    shared_yaxes=True
)

# creating the first histogram plot (individuals)
fig.add_trace(
    go.Bar(
        name="individuals",
        x=ind_df.value_counts().iloc[:7].index.drop("custom"),
        y=ind_df.value_counts().iloc[:7],
        # marker_color="lightskyblue",
        text=ind_df.value_counts().iloc[:7],
    ),
    row=1,
    col=1,
)

# creating the second histogram plot (companies)
fig.add_trace(
    go.Bar(
        name="companies",
        x=co_df.value_counts().iloc[:7].index.drop("others"),
        y=co_df.value_counts().iloc[:7],
        # marker_color="lightgreen",
        text=co_df.value_counts().iloc[:7],
    ),
    row=1,
    col=2,
)

# updating layout and axis labels
fig.update_layout(
    legend=dict(
        orientation="h",
        xref="container",
        xanchor="center",
        yref="container",
        yanchor="bottom",
        x=0.5,
        y=0,
    ),
    yaxis=dict(title=None),
    yaxis2=dict(title=None),
)

fig.add_annotation(
    text="""Distribution of aircraft manufacturer according to<br>the nature of the operators""",
    align="left",
    xref="paper",
    yref="paper",
    x=0,
    y=1.3,
    showarrow=False,
    font=title_font,
)

# displaying
st.plotly_chart(fig)