import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time 
# from request import make_request



st.set_page_config(page_title="Solstice Dashboard", page_icon="📊", layout="wide")
st.write("<div style='text-align: center;'><h1>🔋 Monitoreo de Energia Solstice Bank</h1></div>", unsafe_allow_html=True)
st.markdown("##")



#sidebar
def sideBarOptions():
    st.sidebar.image("img/logosolstice.png", use_column_width=True)
    st.sidebar.markdown("##")
        
    page = st.sidebar.selectbox("Selecciona una Sede", ["Sabana", "Palmas", "Olimpica","Mayales"])

    if page == "Sabana":
        st.title("Sede Sabana de Torres")
        #st.write("Esta es la página de 'Acerca de nosotros'. Aquí puedes describir tu empresa o proyecto.")
    elif page == "Palmas":
        st.title("Sede Las Palmas")
        #st.write("Esta es la página de 'Acerca de nosotros'. Aquí puedes describir tu empresa o proyecto.")
    elif page == "Olimpica":
        st.title("Sede Olimpica")
        #st.write("Puedes contactarnos en support@example.com o en el número de teléfono XXX-XXXX.")
    elif page == "Mayales":
        st.title("Sede Mayales")
        #st.write("Puedes contactarnos en support@example.com o en el número de teléfono XXX-XXXX.")
    
    st.sidebar.markdown("##")
    st.sidebar.image("img/logonexus.png", use_column_width=True)


sideBarOptions()