# Importar las bibliotecas necesarias
import streamlit as st
from utils import backend
import database
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)

def main():
    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        # Muestra un mensaje de error si la autenticación es incorrecta
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        # Muestra un mensaje de advertencia si aún no se ha ingresado usuario y contraseña
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, muestra el contenido principal
        # Título principal de la aplicación
        st.title("normal")
        if 'producto' not in st.session_state:
            st.error("Debes escoger un producto")
        
        # Obtiene los datos de la base de datos según el usuario autenticado
        database_res = database.get_drive(st.session_state["username"])
        # Transforma los datos de la base de datos utilizando funciones del módulo "backend"
        saved_database = backend.get_transformed_dataframe(database_res)
        def graficar_dist(promedio,stdev,nombre="Distribución"):
                # Parámetros de la distribución normal
                media = promedio  # Cambia esto por el valor de la media deseada
                desviacion = stdev  # Cambia esto por el valor de la desviación estándar deseada
                intervalo_tiempo = 0.5  # Intervalo de tiempo en segundos entre cada actualización

                # Definir la secuencia de números de datos a generar
                num_datos = [50, 100, 250, 500, 1000, 1500, 2500]

                # Crear un contenedor vacío para el gráfico
                container = st.empty()

                # Loop para mostrar los gráficos
                for cantidad_datos in num_datos:
                    # Generar números aleatorios con distribución normal
                    datos = np.random.normal(media, desviacion, cantidad_datos)

                    # Crear el histograma de barras
                    histograma = go.Histogram(x=datos,
                                    marker=dict(line=dict(color='black', width=1)))

                    # Definir el diseño del gráfico
                    layout = go.Layout(title=f'{nombre}',
                                    showlegend=False)

                    # Crear la figura
                    fig = go.Figure(data=[histograma], layout=layout)

                    # Actualizar el contenedor con el nuevo gráfico
                    container.plotly_chart(fig, use_container_width=True)

                    # Pausar la ejecución durante el intervalo de tiempo
                    time.sleep(intervalo_tiempo)

        producto = st.session_state["producto"]

        col1, col2, col3 = st.columns([0.2, 0.5,0.3])
        with col1:
            columnas_demanda_mes = [col for col in saved_database.columns if col.startswith("demanda_mes")]
            df_demanda = saved_database[saved_database["cod_producto"] == producto][columnas_demanda_mes].iloc[0].astype(int)
            df_demanda.index = range(1,13)
            df_demanda.index.name = "Períodos"
            df_demanda.name = "Demanda"
            st.dataframe(df_demanda, height=458, use_container_width=True)
        
        with col2:
            descripcion = saved_database[saved_database["cod_producto"] == producto]["desc_producto"].iloc[0]
            promedio = round(df_demanda.mean())
            stdev = round(df_demanda.std(),2)
            mas3_sigma = round(promedio+stdev*3,2)
            menos3_sigma = round(promedio-stdev*3,2)
            stats = {
                'Descripción': descripcion,
                'Promedio': promedio,
                'Desv estandar': stdev,
                '+3 sigma': mas3_sigma,
                '-3 sigma': menos3_sigma,
            }
            stats_df = pd.DataFrame(stats, index=[f"{producto}"]).T
            stats_df.index.name = "Código"
            st.dataframe(stats_df, use_container_width=True)

            # fig = go.Figure(data=go.Scatter(x=[i for i in range(1,13)], y=df_demanda, mode='lines+markers'))
            # st.plotly_chart(fig, use_container_width=True)
        with col3:
            with st.form("my_form"):
                # col1, col2, col3 = st.columns(3)
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("")
                    with col2:
                        st.write("Mean %")
                    with col3:
                        st.write("Desviación %")
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Historico")
                    with col2:
                        st.write(round(promedio,2))
                    with col3:
                        st.write(round(stdev,2))
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Crecimiento")
                    with col2:
                        mean_perc_cre = st.number_input("", step=1, label_visibility="collapsed", key="cremean")
                    with col3:
                        std_perc_cre = st.number_input("", step=1, label_visibility="collapsed", key="crestd")
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Historico con crecimiento")
                    with col2:
                        meanh_con_creci = round(promedio*(mean_perc_cre/100),2)
                        st.write(meanh_con_creci)
                    with col3:
                        stdh_con_creci = round(stdev*(std_perc_cre/100),2)
                        st.write(stdh_con_creci)
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Competencia")
                    with col2:
                        mean_perc_com = st.number_input("", step=1, label_visibility="collapsed", key="commean")
                    with col3:
                        std_perc_com = st.number_input("", step=1, label_visibility="collapsed", key="comstd")
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Historico con competencia")
                    with col2:
                        incre_comp_mean = round(promedio*(mean_perc_com/100),2)
                        st.write(incre_comp_mean)
                    with col3:
                        incre_comp_std = round(stdev*(std_perc_com/100),2)
                        st.write(incre_comp_std)
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Distribución con crecimiento")
                    with col2:
                        meanh_con_creciyprom = round(promedio+meanh_con_creci,2)
                        st.write(meanh_con_creciyprom)
                    with col3:
                        stdh_con_creciystd = round((stdev**2-stdh_con_creci**2)**(1/2),2)
                        st.write(stdh_con_creciystd)
                with st.container():
                    col1, col2, col3 = st.columns([0.6,0.2,0.2])
                    with col1:
                        st.write("Distribución con crecimiento y competencia")
                    with col2:
                        meanh_con_creciyprom_con_com = round(meanh_con_creciyprom-incre_comp_mean,2)
                        st.write(meanh_con_creciyprom_con_com)
                    with col3:
                        stdh_con_creciystd_con_com = round((stdh_con_creciystd**2-incre_comp_std**2)**(1/2),2)
                        st.write(stdh_con_creciystd_con_com)

                submitted = st.form_submit_button("Enviar")
        if submitted:
            col1, col2, col3 = st.columns(3)
            with col1:
                graficar_dist(promedio, stdev)
            with col2:
                graficar_dist(meanh_con_creciyprom, stdh_con_creciystd,"Distribución con crecimiento")
            with col3:
                graficar_dist(meanh_con_creciyprom_con_com, stdh_con_creciystd_con_com,"Distribución con crecimiento y competencia")
            
if __name__ == '__main__':
    main()
    