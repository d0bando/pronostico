# Importar las bibliotecas necesarias
import streamlit as st
import streamlit_authenticator as stauth
import database

# Configurar la página de Streamlit
st.set_page_config(
    page_title="Scorecard Software",  # Título de la página
    page_icon="🏗️",  # Ícono de la página
    layout="wide"  # Diseño de la página
)
def main():
    # --- AUTENTICACIÓN DE USUARIO ---

    # Establecer el número máximo de intentos para obtener credenciales de la base de datos
    max_attempts = 3
    attempts = 0

    # Realizar un bucle para intentar obtener las credenciales de la base de datos
    while attempts < max_attempts:
        try:
            # Intenta obtener las credenciales de todos los usuarios desde la base de datos
            credentials = database.fetch_all_users()
            break  # Sale del bucle si se obtienen las credenciales con éxito
        except Exception as e:
            if attempts < max_attempts:
                attempts += 1
                st.warning(f"Error al obtener datos de la base de datos, intento {attempts}/{max_attempts}.")
            else:
                st.error(f"No se pudieron obtener los datos después de {max_attempts} intentos: {e}")
                break  # Sale del bucle en caso de no poder obtener los datos después de los intentos máximos
    # Crear una instancia del autenticador
    authenticator = stauth.Authenticate(
        credentials=credentials,          # Credenciales obtenidas de la base de datos
        cookie_name="scorecard_software",  # Nombre de la cookie para la autenticación
        key="abcdef",                      # Clave para la autenticador
        cookie_expiry_days=30              # Duración de la cookie de autenticación en días
    )

    # Intentar autenticar al usuario
    name, authentication_status, username = authenticator.login("Iniciar sesión", "main")

    # Comprueba el estado de autenticación del usuario
    if st.session_state["authentication_status"] is False:
        # Muestra un mensaje de error si la autenticación es incorrecta
        st.error('Usuario/contraseña incorrecto')
    elif st.session_state["authentication_status"] is None:
        # Muestra un mensaje de advertencia si aún no se ha ingresado usuario y contraseña
        st.warning('Por favor ingresa tu usuario y contraseña')
    elif st.session_state["authentication_status"]:
        # Si la autenticación es exitosa, mostrar un mensaje de bienvenida  
        st.title(f'Bienvenido _{st.session_state["name"]}_')
        authenticator.logout('Cerrar sesión', 'main', key='unique_key')

if __name__ == '__main__':
    main()