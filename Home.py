
#%%
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from datetime import date, timedelta, datetime
from streamlit_extras.metric_cards import style_metric_cards
import time 
import numpy as np
from API.request import request
from API.library_ubidots_v2 import Ubidots as ubi
from reports.sabana import *
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
import statsmodels.api as sm

from reports.sabana import *
from reports.palmas import *
from reports.olimpica import *
from reports.mayales import *
from reports.informe import *
#%%
load_data = False
informe = False

LST_VAR = [
    "ilu-consumo-activa",
    "aa-consumo-activa",
    "front-consumo-activa",
    "front-tension-3",
    "front-tension-2",
    "front-tension-1"]

LST_DVC = ['bc49','bc-291-las-palmas','bc37','bc38']
    

st.set_page_config(page_title="Solstice Dashboard",page_icon="📊",layout="wide")
st.write("<div style='text-align: center;'><h1>🔋 Monitoreo de Energia Solstice Bank</h1></div>", unsafe_allow_html=True)
st.markdown("##")


#sidebar
def sideBarOptions():

    df = pd.read_csv('API/datos.csv')
    df_baseline = pd.read_csv('API/datos_baseline.csv')
    

    st.sidebar.image("img/logosolstice.png",use_column_width=True)
    st.sidebar.markdown("##")

    ##select page
    page = st.sidebar.selectbox("Selecciona una opción: ", ["Dashboard Sabana", "Dashboard Palmas", "Dashboard Olimpica","Dashboard Mayales","Informe de Consumo"])
    

    st.sidebar.markdown("##")
    start_date=st.sidebar.date_input("Start Date",date.today()-timedelta(days=1))
    end_date=st.sidebar.date_input(label="End Date")
    rq_time = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
    st.sidebar.markdown("##")

    load_data = st.sidebar.button("Cargar Datos")


    if load_data:
        df = request(rq_time,LST_VAR, LST_DVC)
        load_data = False



    st.sidebar.image("img/logonexus.png",use_column_width=True)

    return df, page, load_data, df_baseline

def graficas(df, page):

    df_baseline = pd.read_csv('API/datos_baseline.csv')

    title_map = {
        "Dashboard Sabana": "Sede Sabana de Torres",
        "Dashboard Palmas": "Sede Las Palmas",
        "Dashboard Olimpica": "Sede Olimpica",
        "Dashboard Mayales": "Sede Mayales"
    }

    if page in title_map:
        st.title(title_map[page])

    graph_map = {
        "Dashboard Sabana": makegraphs_Sabana,
        "Dashboard Palmas": makegraphs_Palmas,
        "Dashboard Olimpica": makegraphs_Olimpica,
        "Dashboard Mayales": makegraphs_Mayales,
        "Informe  de Consumo": makegraphs_informe(df_baseline, df, page)
    }

    if page in graph_map:
        graph_map[page](df)


try:
    df, page, load_data, df_baseline = sideBarOptions() # carga la barra lateral
    graficas(df, page) if df is not None else None

except Exception as e:
    st.error(f"Error: {e}")












