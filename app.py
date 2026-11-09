import os
import streamlit as st

# El logo debe estar en la MISMA carpeta que este archivo (y subido a GitHub con ese nombre exacto)
RUTA_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-vector-universidad-san-sebastian.jpg")


def mostrar_logo(**kwargs):
    if os.path.exists(RUTA_LOGO):
        st.image(RUTA_LOGO, **kwargs)
    else:
        st.warning("No se encontró el logo junto a app.py")


# ---------- BARRA LATERAL ----------
st.sidebar.title("Mi primera barra lateral de Streamlit")
st.sidebar.header("¡Hola, Barra Lateral!")
st.sidebar.write("Esto es una barra lateral")

with st.sidebar:
    mostrar_logo(use_container_width=True)

if st.sidebar.button("Haz clic pero en la barra lateral"):
    st.sidebar.write("¡Hiciste clic en la barra lateral!")

texto_barra = st.sidebar.text_input("Escribe algo en la barra:")
st.sidebar.write("Escribiste en la barra:", texto_barra)

# ---------- ÁREA PRINCIPAL ----------
st.title("Mi primera aplicación de Streamlit")
st.header("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")

mostrar_logo(width=300)

if st.button("Haz clic"):
    st.write("¡Hiciste clic!")

texto = st.text_input("Escribe algo:")
st.write("Escribiste:", texto)
