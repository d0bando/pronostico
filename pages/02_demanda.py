# Importar las bibliotecas necesarias
import streamlit as st
from utils import backend
import database
import pandas as pd
import plotly.graph_objects as go

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
        st.title("CERTIFICACIÓN DE DATOS PARA PRONÓSTICO")
        
        # Obtiene los datos de la base de datos según el usuario autenticado
        database_res = database.get_drive(st.session_state["username"])
        # Transforma los datos de la base de datos utilizando funciones del módulo "backend"
        saved_database = backend.get_transformed_dataframe(database_res)
        saved_database["cod_producto"] = saved_database["cod_producto"].astype(str)
        container = st.container()
        col1, col2, col3 = st.columns(3)
        with col1:
            
            # Filtrar por categoría
            cat = st.selectbox('Ingresa la categoría que quieres filtrar', ["Todos"]+saved_database["cat_producto"].unique().tolist())
            
            if cat is not "Todos":
                df_filtered = saved_database[saved_database["cat_producto"] == cat]
            else:
                df_filtered = saved_database

            # Filtrar por subcategoría
            subcat = st.selectbox('Ingresa la subcategoría que quieres filtrar', ["Todos"]+df_filtered["subcat_producto"].unique().tolist())
            # Si el usuario selecciona una subcategoría se filtra por esta misma
            if subcat is not "Todos":
                df_filtered = df_filtered[df_filtered["subcat_producto"] == subcat]


            # if 'producto' not in st.session_state:
            #     st.session_state['producto'] = df_filtered["cod_producto"].tolist()[0]
            selected_prod = st.selectbox("Selecciona un código de producto", df_filtered["cod_producto"].tolist(), index=df_filtered["cod_producto"].tolist().index(st.session_state['producto']))
            st.session_state['producto'] = selected_prod

            descripcion = saved_database[saved_database["cod_producto"] == selected_prod]["desc_producto"].iloc[0]
            categoria = saved_database[saved_database["cod_producto"] == selected_prod]["cat_producto"].iloc[0]
            subcategoria = saved_database[saved_database["cod_producto"] == selected_prod]["subcat_producto"].iloc[0]
            descr = {
                'Descripción': descripcion,
                'Categoría': categoria,
                'Subcategoría': subcategoria
            }
            descr_df = pd.DataFrame(descr, index=[f"{selected_prod}"]).T
            descr_df.index.name = "Código"
            st.dataframe(descr_df, use_container_width=True)

            columnas_demanda_mes = [col for col in saved_database.columns if col.startswith("demanda_mes")]
            df_demanda = saved_database[saved_database["cod_producto"] == selected_prod][columnas_demanda_mes].iloc[0].astype(int)
            df_demanda.index.name = "Período"
            df_demanda.name = "Demanda"
            st.dataframe(df_demanda, height=458, use_container_width=True)

            promedio = round(df_demanda.mean())
            stdev = round(df_demanda.std(),2)
            var_coef = round(stdev/promedio,2)
            aceptacion = "Si" if var_coef <= 0.3 else "No"
            stats = {
                'Promedio': promedio,
                'Desv estandar': stdev,
                'Coeficiente variac.': var_coef,
                'Se aceptan los datos': aceptacion
            }
            stats_df = pd.DataFrame(stats, index=["Estadísticas"]).T
            st.dataframe(stats_df, use_container_width=True)
            
        if aceptacion == "No":
                container.error("Data histórica no apta para hacer pronóstico")
        with col2:
            fig = go.Figure(data=[go.Bar(x=[i for i in range(1,13)], y=df_demanda)])
            st.plotly_chart(fig, use_container_width=True)

            fig = go.Figure(data=go.Scatter(x=[i for i in range(1,13)], y=df_demanda, mode='lines+markers'))
            st.plotly_chart(fig)
        with col3:
            fig = go.Figure(data=go.Box(y=df_demanda, boxmean=True))
            st.plotly_chart(fig, use_container_width=True)

            


if __name__ == '__main__':
    main()