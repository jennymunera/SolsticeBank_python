import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from datetime import date, timedelta, datetime
from streamlit_extras.metric_cards import style_metric_cards
import time 


#from API.request import df
from reports.sabana import *



st.set_page_config(page_title="Solstice Dashboard",page_icon="📊",layout="wide")
st.write("<div style='text-align: center;'><h1>🔋 Monitoreo de Energia Solstice Bank</h1></div>", unsafe_allow_html=True)
st.markdown("##")

#st.write(df) # df is the dataframe from the request.py file 



## widget reloj
def reloj():
    widget_container_reloj = st.container()
    clock_date_placeholder = widget_container_reloj.empty()
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%Y-%m-%d")

        clock_date_placeholder.markdown(
            f'<div style="border: 2px solid #e0e0e0; border-radius: 10px; padding: 10px;width:15%;text-align: center;">'
            f'<p>Hora y Fecha<p>'
            f'<p>{current_time}</p>'
            f'<p>{current_date}</p>'
            f'</div>',
            unsafe_allow_html=True
        )
        time.sleep(1)


#sidebar
def sideBarOptions():
    st.sidebar.image("img/logosolstice.png",use_column_width=True)
    st.sidebar.markdown("##")

    ##select page
    page = st.sidebar.selectbox("Selecciona una Sede", ["Sabana", "Palmas", "Olimpica","Mayales"])
    
    st.sidebar.markdown("##")
    st.sidebar.markdown("##")
    st.sidebar.image("img/logonexus.png",use_column_width=True)

    if page == "Sabana":
        st.title("Sede Sabana de Torres")
        reloj()

    elif page == "Palmas":
        st.title("Sede Las Palmas")
        reloj()

    elif page == "Olimpica":
        st.title("Sede Olimpica")
        reloj()

    elif page == "Mayales":
        st.title("Sede Mayales")
        reloj()

sideBarOptions()


