import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Mi primera aplicación de Streamlit", page_icon="🎓", layout="wide"
)

# --- ÁREA PRINCIPAL ---
st.title("Mi primera aplicación de Streamlit")

st.subheader("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")

# Imagen en el área principal (puedes usar una URL pública del logo de la USS o asegurarte de subirla)
logo_uss = "https://upload.wikimedia.org/wikipedia/commons/2/23/Logo_Universidad_San_Sebastián.png"
st.image(logo_uss, width=300)

# Botón interactivo principal
if st.button("Haz clic"):
    st.write("¡Hiciste clic en el botón principal!")

# Campo de texto interactivo principal
texto_principal = st.text_input("Escribe algo:")
if texto_principal:
    st.write(f"Escribiste: {texto_principal}")


# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.title("Mi primera barra lateral de Streamlit")

st.sidebar.subheader("¡Hola, Barra Lateral!")
st.sidebar.write("Esto es una barra lateral")

st.sidebar.image(logo_uss, width=200)

# Botón interactivo en la barra lateral
if st.sidebar.button("Haz clic pero en la barra lateral"):
    st.sidebar.write("¡Hiciste clic en la barra lateral!")

# Campo de texto interactivo en la barra lateral
texto_lateral = st.sidebar.text_input("Escribe algo en la barra:")
if texto_lateral:
    st.sidebar.write(f"Escribiste en la barra: {texto_lateral}")
