import streamlit as st

# Nombre exacto del archivo de la imagen que subiste a GitHub
LOGO_PATH = "logo-vector-universidad-san-sebastian.jpg"

# --- ÁREA PRINCIPAL ---
st.title("Mi primera aplicación de Streamlit")

st.subheader("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")

# Mostrar imagen en el área principal
st.image(LOGO_PATH, width=300)

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

# Mostrar imagen en la barra lateral
st.sidebar.image(LOGO_PATH, width=200)

# Botón interactivo en la barra lateral
if st.sidebar.button("Haz clic pero en la barra lateral"):
    st.sidebar.write("¡Hiciste clic en la barra lateral!")

# Campo de texto interactivo en la barra lateral
texto_lateral = st.sidebar.text_input("Escribe algo en la barra:")
if texto_lateral:
    st.sidebar.write(f"Escribiste en la barra: {texto_lateral}")
