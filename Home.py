import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from datetime import date, timedelta, datetime
from streamlit_extras.metric_cards import style_metric_cards
import time 
from API.request import request
from API.library_ubidots_v2 import Ubidots as ubi
from reports.sabana import *
import plotly.express as px


load_data = False


LST_VAR = [
    "ilu-consumo-activa",
    "aa-consumo-activa",
    "front-consumo-activa"]

LST_DVC = ['bc49','bc-291-las-palmas','bc37','bc38']
    

st.set_page_config(page_title="Solstice Dashboard",page_icon="📊",layout="wide")
st.write("<div style='text-align: center;'><h1>🔋 Monitoreo de Energia Solstice Bank</h1></div>", unsafe_allow_html=True)
st.markdown("##")

#st.write(df) # df is the dataframe from the request.py file 



## widget reloj
# def reloj():
#     widget_container_reloj = st.container()
#     clock_date_placeholder = widget_container_reloj.empty()

#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     current_date = now.strftime("%Y-%m-%d")
#     clock_date_placeholder.markdown(
#         f'<div style="border: 2px solid #e0e0e0; border-radius: 10px; padding: 10px;width:15%;text-align: center;">'
#         f'<p>Hora y Fecha<p>'
#         f'<p>{current_time}</p>'
#         f'<p>{current_date}</p>'
#         f'</div>',
#         unsafe_allow_html=True
#     )




    

#sidebar
def sideBarOptions():
    df = pd.read_csv('/Users/jennymunera/Documents/GitHub/SolsticeBank_python/API/datos.csv')
    # df=[]

    st.sidebar.image("/Users/jennymunera/Documents/GitHub/SolsticeBank_python/img/logosolstice.png",use_column_width=True)
    st.sidebar.markdown("##")

    ##select page
    page = st.sidebar.selectbox("Selecciona una Sede", ["Sabana", "Palmas", "Olimpica","Mayales"])

    st.sidebar.markdown("##")
    start_date=st.sidebar.date_input("Start Date",date.today()-timedelta(days=1))
    end_date=st.sidebar.date_input(label="End Date")
    rq_time = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]
    st.sidebar.markdown("##")

    if page == "Sabana":
        st.title("Sede Sabana de Torres")
        # reloj()

    elif page == "Palmas":
        st.title("Sede Las Palmas")
        # reloj()

    elif page == "Olimpica":
        st.title("Sede Olimpica")
        # reloj()

    elif page == "Mayales":
        st.title("Sede Mayales")
        # reloj()

    load_data=st.sidebar.button('Cargar datos')

    if load_data:
        # df = request(rq_time,LST_VAR, LST_DVC)
        load_data = False

    st.sidebar.image("/Users/jennymunera/Documents/GitHub/SolsticeBank_python/img/logonexus.png",use_column_width=True)

    return df, page, load_data

def graficas(df, page):

    if page == 'Sabana':

        df_sabana = df[df['device']== 'bc49']


        fig = px.bar(
            df_sabana,
            x="datetime",
            y="value",
            barmode='group',
            color='variable',
            labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
            title=f"Consumo diario de energía activa [kWh]",
        )

        left,right,center=st.columns(3)
        left.plotly_chart(fig,use_container_width=True)
        right.plotly_chart(fig,use_container_width=True)
    
        with center:
            st.plotly_chart(fig, use_container_width=True)
    return





df, page, load_data = sideBarOptions()

print(len(df))

if len(df) > 0:
    graficas(df, page)
    











