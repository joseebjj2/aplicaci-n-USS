import os
from datetime import datetime

import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------------
st.set_page_config(page_title="Portal Estudiantil USS", page_icon="🎓", layout="wide")

# El logo debe estar en la MISMA carpeta que este archivo
RUTA_LOGO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "logo-vector-universidad-san-sebastian.jpg",
)

try:
    from zoneinfo import ZoneInfo

    AHORA = datetime.now(ZoneInfo("America/Santiago"))
except Exception:
    AHORA = datetime.now()

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
MESES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def mostrar_logo(**kwargs):
    if os.path.exists(RUTA_LOGO):
        st.image(RUTA_LOGO, **kwargs)
    else:
        st.warning("No se encontró el logo junto a app.py")


# ------------------------------------------------------------------
# ESTILO (colores institucionales: azul marino y dorado)
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    .banner {
        background: linear-gradient(120deg, #0B2545 0%, #13315C 60%, #1D4E89 100%);
        border-radius: 16px;
        padding: 1.6rem 2rem;
        border-bottom: 5px solid #C9A96A;
        box-shadow: 0 6px 18px rgba(11, 37, 69, 0.25);
    }
    .banner h1 { color: #FFFFFF; margin: 0; padding: 0; font-size: 2.1rem; }
    .banner p  { color: #E6D5B0; margin: .4rem 0 0 0; font-size: 1.05rem; }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E3E6EC;
        border-left: 5px solid #C9A96A;
        border-radius: 12px;
        padding: .8rem 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    .tarjeta {
        background: #F4F6FA;
        border: 1px solid #D9DEE8;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: .6rem;
    }
    .tarjeta b { color: #0B2545; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# ESTADO DE LA SESIÓN (contadores de clics)
# ------------------------------------------------------------------
if "clics_barra" not in st.session_state:
    st.session_state.clics_barra = 0
if "clics_main" not in st.session_state:
    st.session_state.clics_main = 0

# ------------------------------------------------------------------
# BARRA LATERAL
# ------------------------------------------------------------------
st.sidebar.title("Mi primera barra lateral de Streamlit")
st.sidebar.header("¡Hola, Barra Lateral!")
st.sidebar.write("Esto es una barra lateral")

with st.sidebar:
    mostrar_logo(width=240)

    st.divider()
    st.subheader("👤 Perfil del estudiante")
    nombre = st.text_input("¿Cómo te llamas?", placeholder="Tu nombre")
    carrera = st.selectbox(
        "Carrera",
        [
            "Ingeniería Civil Industrial",
            "Ingeniería Comercial",
            "Ingeniería Civil en Informática",
            "Derecho",
            "Psicología",
            "Medicina Veterinaria",
        ],
    )
    semestre = st.slider("Semestre que cursas", 1, 12, 9)

    st.divider()
    if st.button("Haz clic pero en la barra lateral"):
        st.session_state.clics_barra += 1
        st.toast("¡Clic registrado desde la barra lateral!", icon="👈")
    st.caption(f"Clics en la barra lateral: {st.session_state.clics_barra}")

    texto_barra = st.text_input("Escribe algo en la barra:")
    st.write("Escribiste en la barra:", texto_barra)

# ------------------------------------------------------------------
# ÁREA PRINCIPAL: ENCABEZADO
# ------------------------------------------------------------------
hora = AHORA.hour
saludo = "Buenos días" if hora < 12 else ("Buenas tardes" if hora < 20 else "Buenas noches")
nombre_mostrar = nombre.strip().title() if nombre.strip() else "estudiante"
fecha_txt = f"{DIAS[AHORA.weekday()]} {AHORA.day} de {MESES[AHORA.month - 1]} de {AHORA.year}"

col_logo, col_banner = st.columns([1, 3])
with col_logo:
    mostrar_logo(width=260)
with col_banner:
    st.markdown(
        f"""
        <div class="banner">
            <h1>Mi primera aplicación de Streamlit</h1>
            <p>{saludo}, {nombre_mostrar} 👋 · {carrera} · Semestre {semestre}</p>
            <p>📅 {fecha_txt}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.header("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")

# ------------------------------------------------------------------
# PESTAÑAS
# ------------------------------------------------------------------
tab_notas, tab_calc, tab_horario, tab_mensajero = st.tabs(
    ["📊 Mis notas", "🎯 ¿Cuánto necesito?", "🗓️ Horario", "💬 Mensajero"]
)

# ================= TAB 1: NOTAS =================
with tab_notas:
    st.subheader("Simulador de notas del semestre")
    st.caption("Edita las notas directamente en la tabla (escala chilena 1,0 a 7,0). Puedes agregar filas.")

    c1, c2, c3 = st.columns(3)
    p1 = c1.slider("Peso Solemne 1 (%)", 10, 45, 30)
    p2 = c2.slider("Peso Solemne 2 (%)", 10, 45, 30)
    pe = 100 - p1 - p2
    c3.metric("Peso del Examen (%)", pe)

    base = pd.DataFrame(
        {
            "Asignatura": [
                "Taller de Programación",
                "Finanzas Corporativas",
                "Gestión de Operaciones",
                "Evaluación de Proyectos",
                "Estadística Aplicada",
            ],
            "Solemne 1": [5.2, 4.1, 6.0, 3.8, 5.5],
            "Solemne 2": [4.8, 3.5, 6.3, 4.2, 5.0],
            "Examen": [5.0, 4.0, 6.5, 3.5, 5.8],
        }
    )

    formato_nota = st.column_config.NumberColumn(min_value=1.0, max_value=7.0, step=0.1, format="%.1f")
    editado = st.data_editor(
        base,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "Solemne 1": formato_nota,
            "Solemne 2": formato_nota,
            "Examen": formato_nota,
        },
        key="tabla_notas",
    )

    # --- Procesamiento ---
    df = editado.copy()
    df["Asignatura"] = df["Asignatura"].fillna("Sin nombre")
    for col in ["Solemne 1", "Solemne 2", "Examen"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Promedio"] = ((df["Solemne 1"] * p1 + df["Solemne 2"] * p2 + df["Examen"] * pe) / 100).round(1)


    def estado(nota):
        if pd.isna(nota):
            return "—"
        if nota >= 4.0:
            return "✅ Aprobado"
        if nota >= 3.5:
            return "⚠️ En riesgo"
        return "❌ Reprobado"


    df["Estado"] = df["Promedio"].apply(estado)
    validos = df.dropna(subset=["Promedio"])

    # --- Salida ---
    st.markdown("#### Resultados")
    if validos.empty:
        st.info("Completa al menos una fila con sus tres notas para ver los resultados.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Promedio general", f"{validos['Promedio'].mean():.1f}")
        mejor = validos.loc[validos["Promedio"].idxmax()]
        m2.metric("Mejor ramo", f"{mejor['Promedio']:.1f}", mejor["Asignatura"], delta_color="off")
        en_riesgo = int((validos["Promedio"] < 4.0).sum())
        m3.metric("Ramos bajo 4,0", en_riesgo)

        izq, der = st.columns([3, 2])
        with izq:
            st.dataframe(df[["Asignatura", "Promedio", "Estado"]], hide_index=True)
        with der:
            st.bar_chart(validos.set_index("Asignatura")["Promedio"], color="#C9A96A")

# ================= TAB 2: CALCULADORA =================
with tab_calc:
    st.subheader("¿Qué nota necesito en el examen?")
    st.caption(f"Usa los pesos configurados en la pestaña anterior: S1 {p1}% · S2 {p2}% · Examen {pe}%")

    a, b, c = st.columns(3)
    s1 = a.number_input("Nota Solemne 1", 1.0, 7.0, 4.5, 0.1)
    s2 = b.number_input("Nota Solemne 2", 1.0, 7.0, 4.0, 0.1)
    meta = c.number_input("Nota final que quieres", 1.0, 7.0, 4.0, 0.1)

    necesaria = (meta * 100 - s1 * p1 - s2 * p2) / pe
    avance = (s1 * p1 + s2 * p2) / 100

    r1, r2 = st.columns(2)
    r1.metric("Puntos acumulados antes del examen", f"{avance:.2f}")
    r2.metric("Nota necesaria en el examen", f"{min(max(necesaria, 1.0), 7.0):.1f}")

    if necesaria <= 1.0:
        st.success("🎉 ¡Ya alcanzaste tu meta, incluso con un 1,0 en el examen!")
    elif necesaria > 7.0:
        st.error(f"😟 Con estas notas necesitarías un {necesaria:.1f}, lo que supera el 7,0. Conviene replantear la meta.")
    else:
        st.progress((necesaria - 1.0) / 6.0, text=f"Dificultad del examen: necesitas un {necesaria:.1f}")
        if necesaria <= 4.0:
            st.info("Se ve bastante alcanzable. ¡A repasar con calma!")
        elif necesaria <= 5.5:
            st.warning("Requiere buena preparación. ¡Tú puedes!")
        else:
            st.warning("Será un examen exigente: a estudiar fuerte.")

    st.markdown("#### Escenarios: nota final según tu nota de examen")
    escenarios = pd.DataFrame(
        {"Nota final": [(s1 * p1 + s2 * p2 + n * pe) / 100 for n in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]]},
        index=pd.Index([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], name="Nota examen"),
    )
    st.line_chart(escenarios, color="#13315C")

# ================= TAB 3: HORARIO =================
with tab_horario:
    st.subheader("Horario semanal")

    horario = pd.DataFrame(
        {
            "Día": ["Lunes", "Lunes", "Martes", "Martes", "Miércoles", "Miércoles", "Jueves", "Jueves", "Viernes"],
            "Bloque": [
                "08:30 - 10:00", "10:10 - 11:40", "08:30 - 10:00", "14:30 - 16:00",
                "10:10 - 11:40", "16:10 - 17:40", "08:30 - 10:00", "14:30 - 16:00", "10:10 - 11:40",
            ],
            "Asignatura": [
                "Finanzas Corporativas", "Estadística Aplicada", "Gestión de Operaciones",
                "Taller de Programación", "Evaluación de Proyectos", "Estadística Aplicada",
                "Finanzas Corporativas", "Taller de Programación", "Gestión de Operaciones",
            ],
            "Sala": ["B-204", "A-101", "C-305", "Lab 2", "B-110", "A-101", "B-204", "Lab 2", "C-305"],
        }
    )

    dia_defecto = AHORA.weekday() if AHORA.weekday() < 5 else 0
    dia = st.selectbox("Ver el día:", DIAS[:5], index=dia_defecto)
    clases_dia = horario[horario["Día"] == dia][["Bloque", "Asignatura", "Sala"]]

    if AHORA.weekday() >= 5:
        st.info("Hoy es fin de semana 🎉 Aquí tienes el horario del día que elegiste.")
    if clases_dia.empty:
        st.success(f"Sin clases el {dia.lower()} 😎")
    else:
        st.write(f"**{len(clases_dia)} clase(s) el {dia.lower()}:**")
        st.dataframe(clases_dia, hide_index=True)

    with st.expander("Ver semana completa"):
        st.dataframe(horario, hide_index=True)

# ================= TAB 4: MENSAJERO =================
with tab_mensajero:
    st.subheader("Recibir una entrada, procesarla y presentar una salida")

    if st.button("Haz clic"):
        st.session_state.clics_main += 1
        st.toast("¡Clic registrado en el área principal!", icon="🖱️")
    st.caption(f"Clics en el área principal: {st.session_state.clics_main}")

    texto = st.text_input("Escribe algo:")
    st.write("Escribiste:", texto)

    if texto.strip():
        palabras = len(texto.split())
        caracteres = len(texto)
        vocales = sum(1 for ch in texto.lower() if ch in "aeiouáéíóú")

        k1, k2, k3 = st.columns(3)
        k1.metric("Palabras", palabras)
        k2.metric("Caracteres", caracteres)
        k3.metric("Vocales", vocales)

        st.markdown(
            f"""
            <div class="tarjeta">
                <b>En mayúsculas:</b> {texto.upper()}<br>
                <b>Al revés:</b> {texto[::-1]}<br>
                <b>Procesado a las:</b> {AHORA.strftime('%H:%M:%S')}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("Escribe un mensaje para ver cómo la app lo procesa.")

# ------------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------------
st.divider()
st.caption("Aplicación desarrollada con Streamlit · Universidad San Sebastián · Tarea evaluativa")
