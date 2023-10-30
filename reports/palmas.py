import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
import plotly.express as px





def makegraphs_Palmas(df):
        
        df_Palmas = df[df['device']== 'bc-291-las-palmas']
        df_Palmas.reset_index(inplace=True)
        df_Palmas_tension = df_Palmas[df_Palmas['variable'].isin(['front-tension-1','front-tension-2','front-tension-3'])]
        df_Palmas = df_Palmas[df_Palmas['variable'].isin(['front-consumo-activa','aa-consumo-activa','ilu-consumo-activa'])]

        df_Palmas_front = df_Palmas[df_Palmas['variable'] == 'front-consumo-activa']
        df_Palmas_front['datetime'] = pd.to_datetime(df_Palmas_front['datetime'	])
        df_Palmas_front['hour'] = df_Palmas_front['datetime'].dt.hour





        df_locations = pd.DataFrame(
            {'lat': [7.1170],
            'lon': [-73.1120]})

        consumo_front = np.sum(df_Palmas[df_Palmas['variable'] == 'front-consumo-activa']['value'])
        potencia_maxima = np.max(df_Palmas[df_Palmas['variable'] == 'front-consumo-activa']['value'])
        maxima_demanda = np.max(df_Palmas[df_Palmas['variable'] == 'aa-consumo-activa']['value'])/12


        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")

        total0,total1,total2,total3,=st.columns(4,gap='large')
        with total0:
            st.info('Fecha y hora de actualización',icon="📌")
            st.metric(value=f"{current_time}",label=f"{current_date}")
        with total1:
            st.info('Consumo periodo actual',icon="📌")
            st.metric(label="kWh",value=f"{consumo_front:,.0f}")
        with total2:
            st.info('Potencia máxima',icon="📌")
            st.metric(label="(kW)",value=f"{potencia_maxima:,.0f}")
        with total3:
            st.info('Máxima demanda AA',icon="📌")
            st.metric(label="(KW/TR)",value=f"{maxima_demanda:,.0f}")
        style_metric_cards(background_color="#00588E",border_left_color="#FF4B4B",border_color="#1f66bd",box_shadow="#F71938")
        st.markdown("""---""")

        graph1, graph2 = st.columns([0.7, 0.3])


        with graph1:

            # make a plotly line chart
            fig_line = px.line(
                df_Palmas,
                x="datetime",
                y="value",
                color='variable',
                labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
                title=f"Consumo de energía activa [kWh] por hora",
            )
            st.plotly_chart(fig_line,use_container_width=True)

        with graph2:
            # make a map for streamlit using st.map()

            st.map(df_locations, zoom=12)

        st.markdown("""---""")

        # make a histogram of 'front-consumo-activa' using plotly 

        graph3, graph4 = st.columns([0.7, 0.3])

        with graph3:
            fig_hist = px.histogram(df_Palmas_front, x='value', nbins=12, title="Histograma de potencia activa (kW)")
            st.plotly_chart(fig_hist,use_container_width=True)

        with graph4:
            fig_pie = px.pie(df_Palmas, values='value', names='variable', title='Consumo total por dispositivo')
            st.plotly_chart(fig_pie,use_container_width=True)


        fig_bar = px.bar(
            df_Palmas,
            x="datetime",
            y="value",
            barmode='group',
            color='variable',
            labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
            title=f"Consumo por hora de energía activa [kWh] por dispositivo",
        )


        st.plotly_chart(fig_bar,use_container_width=True)

        st.markdown("""---""")

        # make a plotly line chart with tension
        fig_line_tension = px.line(
            df_Palmas_tension,
            x="datetime",
            y="value",
            color='variable',
            labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
            title=f"Tensión [V]",
        )
        st.plotly_chart(fig_line_tension,use_container_width=True)

        st.markdown("""---""")

        
        fig_scatter = px.scatter(
            df_Palmas_front,
            x="hour",
            y="value",
            color='variable',
            labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
            title=f"Curva típica de consumo [kWh]",
        )

        st.plotly_chart(fig_scatter, use_container_width=True)
