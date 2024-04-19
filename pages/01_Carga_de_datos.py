# Importar las bibliotecas necesarias
import streamlit as st
from utils import backend
import database

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
        
        # Título de la página
        st.title("Base de datos :card_file_box:")

        # Permite al usuario cargar un archivo
        uploaded_data = st.file_uploader(label="", label_visibility='collapsed')

        if uploaded_data:
            # Verifica la extensión del archivo y las columnas del DataFrame
            backend.check_extension(uploaded_data)
            # backend.check_dataframe_columns(uploaded_data)
            
            # Sube el archivo a la base de datos
            with st.spinner('Subiendo archivo a la base de datos'):
                database.create_drive(st.session_state["username"], uploaded_data)
            st.toast('Archivo subido correctamente!', icon='✔️')

        # Obtiene la respuesta (archivo Excel) desde la base de datos
        response = database.get_drive(st.session_state["username"])

        # si se va a cargar un archivo por primera vez se muestra en la interfaz un mensaje
        if response is None:
            st.info("Por favor, carga un archivo Excel utilizando el botón de arriba.")
            st.stop()  

        # Crea dos pestañas para mostrar el contenido y permitir la exportación
        tab_1, tab_2 = st.tabs(["Tabla 📄", "Exportar 📁"])
        with tab_1:
            # Carga el DataFrame transformado 
            df_transformed = backend.get_transformed_dataframe(response)
            
            # Dataframe para mostrar en la interdaz, solo las 100 primeras filas
            df_transformed = df_transformed.head(100)

            # Aplica estilos al DataFrame transformado 
            df_styled = backend.get_styled_dataframe(df_transformed)
            
            # Muestra el DataFrame con estilos en la aplicación Streamlit, ocultando el índice
            st.dataframe(df_styled, hide_index=True)
        with tab_2:
            # Permite la descarga del DataFrame en formatos CSV y Excel
            backend.download_dataframe(df_transformed, name="base_de_datos")

if __name__ == '__main__':
    main()




