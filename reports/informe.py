import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_extras.metric_cards import style_metric_cards
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from model.train import train

dct_dow = {
        0: 'lunes',
        1: 'martes',
        2: 'miércoles',
        3: 'jueves',
        4: 'viernes',
        5: 'sábado',
        6: 'domingo',
    }

NIGHT_HOURS = [0, 1, 2, 3, 4, 5, 19, 20, 21, 22, 23]



def datetime_attributes(df):
        df['hour'] = df.index.hour
        df['day'] = df.index.day
        df['dow'] = df.index.dayofweek.map(dct_dow)
        df['cont_dow'] = (24 * df.index.dayofweek + df.index.hour) / 24
        df['week'] = df.index.isocalendar().week
        df['month'] = df.index.month
        df['year'] = df.index.year
        return df

def makegraphs_informe(df_baseline, df, page):

    fechas_train = ['2023-01-01','2023-02-28']
    fechas_test = ['2023-03-01','2023-03-31']

    if page == "Informe de Consumo":



        sede = st.selectbox("Selecciona una opción: ", ["Sabana", "Palmas", "Olimpica","Mayales"])
        
        

        # make a dict with equivalences of sede with LST_DVC = ['bc49','bc-291-las-palmas','bc37','bc38']
        dct_sede = {
            "Sabana": "bc49",
            "Palmas": "bc-291-las-palmas",
            "Olimpica": "bc37",
            "Mayales": "bc38"
        }

        st.write(f"<div><h1> Informe de consumo {sede} </h1></div>", unsafe_allow_html=True)

        df_st = df[df['device']==dct_sede[sede]].copy()

        df_st.index = pd.to_datetime(df_st['datetime'])
        df_st.drop(columns=['datetime'], inplace=True)

        df_bl = df_baseline[df_baseline['device']==dct_sede[sede]].copy()
        df_bl.index = pd.to_datetime(df_bl['datetime'])
        df_bl.drop(columns=['datetime'], inplace=True)

        df_bl['Periodo'] = 'Baseline'
        df_st['Periodo'] = 'Estudio'
        

        cargas_st = df_st[df_st['variable'].isin(['aa-consumo-activa', 'ilu-consumo-activa'])].copy()
        front_st = df_st[df_st['variable'].isin(['front-consumo-activa'])].copy()

        front_st_pred = datetime_attributes(front_st).copy()

        front_bl = df_bl[df_bl['variable'].isin(['front-consumo-activa'])].copy()
        cargas_bl = df_bl[df_bl['variable'].isin(['aa-consumo-activa', 'ilu-consumo-activa'])].copy()

        front_day_bl = front_bl.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        front_day_bl = datetime_attributes(front_day_bl)
        front_day_bl['Periodo'] = 'Baseline'

        front_day_st = front_st.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        front_day_st = datetime_attributes(front_day_st)
        front_day_st['Periodo'] = 'Estudio'

        cargas_day_bl = cargas_bl.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        cargas_day_bl = datetime_attributes(cargas_day_bl)
        cargas_day_bl['Periodo'] = 'Baseline'

        cargas_day_st = cargas_st.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        cargas_day_st = datetime_attributes(cargas_day_st)
        cargas_day_st['Periodo'] = 'Estudio'

        cargas_month = cargas_st.groupby(by=["variable"]).resample('1M').sum().reset_index().set_index('datetime')
        cargas_month = datetime_attributes(cargas_month)

        df_concat_st = pd.concat([cargas_day_st, front_day_st])


        df_concat_st['month_day'] = df_concat_st['month'].astype(str) + '-' + df_concat_st['day'].astype(str)
        df_concat_st = df_concat_st.sort_values('datetime')
        agg_df = df_concat_st.groupby(['month_day', 'variable'])['value'].sum().reset_index()

        model, MSE = train(front_bl, fechas_train, fechas_test)

        st.write(f"El error cuadrático medio del modelo es de {MSE:.2f} kWh/día")
        front_st_pred['value_pred'] = model.predict(front_st_pred[['hour', 'cont_dow']])
        ## TODO: add a graph showing predictions vs actual consumption
        front_st_pred['Periodo'] = 'Predicción'
        front_st_pred_daily = front_st_pred.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        front_st_pred_daily = datetime_attributes(front_st_pred_daily)
        front_st_pred_daily['Periodo'] = 'Predicción'
        front_st_pred_daily['month_day'] = front_st_pred_daily['month'].astype(str) + '-' + front_st_pred_daily['day'].astype(str)

        #calculate difference between prediction and actual consumption and sum it
        front_st_pred_daily['value_diff'] = front_st_pred_daily['value'] - front_st_pred_daily['value_pred']
        consumption_pred= front_st_pred_daily['value_diff'].sum()

        fig_bar_diario = px.bar(
            df_concat_st,
            x="month_day",
            y="value",
            barmode='group',
            color='variable',
            labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
            title=f"Consumo diario de energía activa [kWh]",
        )

        


        fig_bar_diario.add_hline(y=front_day_bl['value'].mean(), line_dash="dash", annotation_text=f"Línea base: {front_day_bl['value'].mean():.2f} kWh/dia", annotation_position="top left")

        # Add a new trace with front_st_pred_daily['value_pred']
        fig_bar_diario.add_trace(go.Bar(x=front_st_pred_daily['month_day'], y=front_st_pred_daily['value_pred'], name='Predicción'))


        # Ajustamos la escala y el formato del eje x
        fig_bar_diario.update_xaxes(
            type='category',  # Usar una escala categórica en lugar de fecha
            tickvals=list(agg_df['month_day']),  # Valores en el eje x
            ticktext=list(agg_df['month_day']),  # Etiquetas en el eje x
            title_text='Mes - Día',  # Título del eje x
        )

        st.plotly_chart(fig_bar_diario, use_container_width=True)


        #calculate how many days does df_concat have
        days = df_concat_st['month_day'].nunique()
        tipical_consumption = front_day_bl['value'].mean() * days
        actual_consumption = front_day_st['value'].sum()
        savings = tipical_consumption - actual_consumption

        if savings > 0:
            st.write(f"Durante el periodo de estudio se ahorró {abs(savings):.0f} kWh respecto a la línea base y se esperaba un ahorro de {abs(abs(savings)-abs(consumption_pred)):.0f} kWh respecto al consumo de la línea base, te recomendamos continuar con tu plan de ahorro de energía")
        else:
            st.write(f"Durante el periodo de estudio se consumió {abs(savings):.0f} kWh más respecto a la línea base y se esperaba un consumo superior de {abs(savings)-abs(consumption_pred):.0f} kWh respecto al consumo de la línea base, te recomendamos revisar patrón de consumo propendiendo por un ahorro de energía")
            


        fig_box = px.box(
            pd.concat([front_day_bl, front_day_st]),
            y="value",
            color='Periodo',
            labels={'day':'Día', 'value':'Consumo [kWh/dia]'},
            title=f"Consumo típico diario",
            
        )

        fig_box.add_hline(y=front_day_bl['value'].mean(), line_dash="dash", annotation_text=f"Línea base: {front_day_bl['value'].mean():.2f} kWh/dia", annotation_position="top left")
        fig_box.add_hline(y=front_day_st['value'].mean(), line_dash="dash", annotation_text=f"Consumo semana : {front_day_st['value'].mean():.2f} kWh/dia", annotation_position="top right")




        st.plotly_chart(fig_box,use_container_width=True)


        if front_day_bl['value'].mean() - front_day_st['value'].mean() > 0:
            
            st.write(f"Se evidencia una diferencia del consumo promedio diario de {abs(front_day_bl['value'].mean() - front_day_st['value'].mean()):.2f} kWh/dia, lo que representa un {abs(front_day_bl['value'].mean() - front_day_st['value'].mean()) / front_day_bl['value'].mean() * 100:.0f} % de disminución respecto a la línea base. Te recomendamos continuar con tu plan de ahorro de energía")
        else:
            st.write(f"Se evidencia una diferencia del consumo promedio diario de {abs(front_day_bl['value'].mean() - front_day_st['value'].mean()):.2f} kWh/dia, lo que representa un {abs(front_day_bl['value'].mean() - front_day_st['value'].mean()) / front_day_bl['value'].mean() * 100:.0f} % de aumento respecto a la línea base. Te recomendamos revisar patrón de consumo propendiendo por un ahorro de energía")



        df_front_cargas = pd.concat([cargas_st, cargas_bl])

        front_st['hour'] = front_st.index.hour
        df_front_cargas['hour'] = df_front_cargas.index.hour

        front_nighttime_cons = front_st[front_st["hour"].isin(NIGHT_HOURS)].copy()

        cargas_nighttime_cons = df_front_cargas[df_front_cargas["hour"].isin(NIGHT_HOURS)].copy()
        cargas_nighttime_cons = datetime_attributes(cargas_nighttime_cons)

        cargas_nighttime_cons_bl = cargas_nighttime_cons[cargas_nighttime_cons["Periodo"] == "Baseline"].copy()
        cargas_nighttime_cons_st = cargas_nighttime_cons[cargas_nighttime_cons["Periodo"] == "Estudio"].copy()

        cargas_nighttime_cons_bl_daily = cargas_nighttime_cons_bl.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        cargas_nighttime_cons_bl_daily = datetime_attributes(cargas_nighttime_cons_bl_daily)
        cargas_nighttime_cons_bl_daily['Periodo'] = 'Baseline'

        cargas_nighttime_cons_st_daily = cargas_nighttime_cons_st.groupby(by=["variable"]).resample('1D').sum().reset_index().set_index('datetime')
        cargas_nighttime_cons_st_daily = datetime_attributes(cargas_nighttime_cons_st_daily)
        cargas_nighttime_cons_st_daily['Periodo'] = 'Estudio'


        # Crear una columna 'month_day' combinando 'month' y 'day'
        cargas_nighttime_cons_st_daily['month_day'] = cargas_nighttime_cons_st_daily['month'].astype(str) + '-' + cargas_nighttime_cons_st_daily['day'].astype(str)
        # Ordenar los datos por la columna 'datetime'
        cargas_nighttime_cons_st_daily = cargas_nighttime_cons_st_daily.sort_values('datetime')
        # Agregamos los valores de las dos variables por month_day
        agg_cargas_nighttime_cons_st_daily = cargas_nighttime_cons_st_daily.groupby(['month_day', 'variable'])['value'].sum().reset_index()


        if (cargas_nighttime_cons_st_daily.shape[0] > 0):
            fig_night = px.bar(
                cargas_nighttime_cons_st_daily.reset_index(),
                x="month_day",
                y="value",
                barmode='group',
                labels={'month_day':'Mes - Día', 'value':'Consumo [kWh]'},
                title=f"Consumo nocturno de energía activa AA/Ilu [kWh/día]",
            )

            fig_night.add_hline(y=cargas_nighttime_cons_bl_daily['value'].mean(), line_dash="dash", annotation_text=f"Línea base: {cargas_nighttime_cons_bl_daily['value'].mean():.2f} kWh/día", annotation_position="top left")
            fig_night.add_hline(y=cargas_nighttime_cons_st_daily['value'].mean(), line_dash="dash", annotation_text=f"Consumo semana : {cargas_nighttime_cons_st_daily['value'].mean():.2f} kWh/dia", annotation_position="top right")

            # Ajustamos la escala y el formato del eje x
            fig_night.update_xaxes(
            type='category',  # Usar una escala categórica en lugar de fecha
            tickvals=list(agg_cargas_nighttime_cons_st_daily['month_day']),  # Valores en el eje x
            ticktext=list(agg_cargas_nighttime_cons_st_daily['month_day']),  # Etiquetas en el eje x
            title_text='Mes - Día',  # Título del eje x
)
        
            st.plotly_chart(fig_night,use_container_width=True)


        fig_night_box = px.box(
        pd.concat([cargas_nighttime_cons_bl_daily,cargas_nighttime_cons_st_daily]),
        y="value",
        color='Periodo',
        labels={'day':'Día', 'value':'Consumo [kWh/dia]'},
        title=f"Consumo nocturno típico diario",
        
    )

        # add 2 columns
        graph1, graph2 = st.columns([0.7, 0.3])

        with graph1:
            fig_night_box.add_hline(y=cargas_nighttime_cons_bl_daily['value'].mean(), line_dash="dash",  annotation_text=f"Línea base: {cargas_nighttime_cons_bl_daily['value'].mean():.2f} kWh/dia", annotation_position="top left")
            fig_night_box.add_hline(y=cargas_nighttime_cons_st_daily['value'].mean(), line_dash="dash",  annotation_text=f"Consumo semana: {cargas_nighttime_cons_st_daily['value'].mean():.2f} kWh/dia", annotation_position="top right")

            total_night_cons = front_nighttime_cons.query("variable == 'front-consumo-activa'")
            consumo_nocturno = total_night_cons["value"].sum()

            st.write(f"Durante el periodo de estudio se consumió un total de {consumo_nocturno:.0f}kWh fuera del horario establecido. Te recomendamos revisar patrón de consumo nocturno propendiendo por un ahorro de energía")

            st.plotly_chart(fig_night_box,use_container_width=True)

            total_night_cons = front_nighttime_cons.query("variable == 'front-consumo-activa'")

            consumo_nocturno = total_night_cons["value"].sum()

            night_cons_percent = 100 * consumo_nocturno / actual_consumption

            st.write(f"Durante el periodo de estudio el consumo nocturno representó el {night_cons_percent:.1f}% del consumo total")

        with graph2:
            cargas_cons_total = cargas_month['value'].sum()
            consumo_otros =  actual_consumption - cargas_cons_total

            if (consumo_otros < 0):
                consumo_otros = 0

            df_pie = cargas_month[['variable','value']].copy()

            df_pie.loc[-1] = ['otros', consumo_otros]
            df_pie = df_pie.reset_index(drop=True)
            df_pie['value'] = df_pie['value'].round(1)


            if (df_pie.value >= 0).all():
                fig_pie = px.pie(
                    df_pie, 
                    values="value", 
                    names='variable', 
                    hover_data=['value'], 
                    labels={'variable':'Carga', 'value':'Consumo [kWh]'},
                    title=f"Consumo total de energía activa por carga [kWh]"
                )


                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent', 
                    insidetextorientation='radial'
                )

                fig_pie.update(
                    layout_showlegend=True
                )

                st.plotly_chart(fig_pie,use_container_width=True)

        return












