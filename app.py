import base64
import os
from datetime import datetime

import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# ------------------------------------------------------------------
st.set_page_config(page_title="Portal Estudiantil USS", page_icon="🎓", layout="wide")

# El logo debe estar en la MISMA carpeta que este archivo
CARPETA = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGO = os.path.join(CARPETA, "logo-vector-universidad-san-sebastian.jpg")

# Imagen de fondo (marca de agua). Para usar otra, sube la imagen a GitHub
# y cambia el nombre entre comillas (por ejemplo "campus.jpg" o "fondo.png").
RUTA_FONDO = os.path.join(CARPETA, "logo-vector-universidad-san-sebastian.jpg")

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


def css_fondo(datos, mime, visibilidad):
    """Pone una imagen de fondo difuminada (marca de agua) detrás de toda la app."""
    b64 = base64.b64encode(datos).decode()
    velo = round(1 - visibilidad / 100, 2)  # capa blanca que "apaga" la imagen
    return (
        "<style>"
        ".stApp {"
        f"background-image: linear-gradient(rgba(255,255,255,{velo}), rgba(255,255,255,{velo})), "
        f"url('data:{mime};base64,{b64}');"
        "background-repeat: no-repeat, no-repeat;"
        "background-position: center, center;"
        "background-size: 100% 100%, 55%;"
        "background-attachment: fixed, fixed;"
        "}"
        "</style>"
    )


def clasificar(texto):
    t = texto.lower()
    if any(p in t for p in ["nota", "solemne", "examen", "promedio", "evaluaci"]):
        return "Evaluaciones"
    if any(p in t for p in ["horario", "sala", "clase", "asistencia", "toma de ramos"]):
        return "Horarios y asistencia"
    if any(p in t for p in ["pago", "arancel", "matrícula", "matricula", "beca", "cuota"]):
        return "Finanzas estudiantiles"
    if any(p in t for p in ["certificado", "constancia", "documento"]):
        return "Certificados y documentos"
    return "Consulta general"


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
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# ESTADO DE LA SESIÓN
# ------------------------------------------------------------------
if "asistencias" not in st.session_state:
    st.session_state.asistencias = []
if "consultas" not in st.session_state:
    st.session_state.consultas = []

# ------------------------------------------------------------------
# BARRA LATERAL
# ------------------------------------------------------------------
with st.sidebar:
    mostrar_logo(width=240)

    st.title("Menú del estudiante")

    st.header("Mi perfil")
    st.caption("Completa tus datos para personalizar el portal.")
    nombre = st.text_input("Nombre", placeholder="Ej: Camila Rojas")
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
    st.header("Asistencia")
    if st.button("Registrar asistencia de hoy"):
        st.session_state.asistencias.append(AHORA.strftime("%H:%M"))
        st.toast("Asistencia registrada correctamente", icon="✅")
    if st.session_state.asistencias:
        st.success(
            f"Asistencias registradas: {len(st.session_state.asistencias)} "
            f"(última a las {st.session_state.asistencias[-1]})"
        )
    else:
        st.caption("Aún no registras asistencia en esta sesión.")

    st.divider()
    st.header("Recordatorios")
    recordatorio = st.text_input("Anota algo pendiente", placeholder="Ej: Entregar informe de finanzas")
    if recordatorio.strip():
        st.info(f"📌 Pendiente: {recordatorio.strip()}")
    else:
        st.caption("No tienes recordatorios anotados.")

    st.divider()
    st.header("Apariencia")
    usar_fondo = st.checkbox("Mostrar imagen de fondo", value=True)
    fondo_subido = st.file_uploader("Cambiar imagen de fondo (opcional)", type=["png", "jpg", "jpeg"])
    visibilidad = st.slider("Visibilidad del fondo (%)", 5, 40, 12)

# ------------------------------------------------------------------
# IMAGEN DE FONDO
# ------------------------------------------------------------------
if usar_fondo:
    if fondo_subido is not None:
        st.markdown(css_fondo(fondo_subido.getvalue(), fondo_subido.type or "image/png", visibilidad), unsafe_allow_html=True)
    elif os.path.exists(RUTA_FONDO):
        mime_fondo = "image/png" if RUTA_FONDO.lower().endswith(".png") else "image/jpeg"
        with open(RUTA_FONDO, "rb") as f:
            st.markdown(css_fondo(f.read(), mime_fondo, visibilidad), unsafe_allow_html=True)

# ------------------------------------------------------------------
# ENCABEZADO
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
            <h1>Portal Estudiantil USS</h1>
            <p>{saludo}, {nombre_mostrar} · {carrera} · Semestre {semestre}</p>
            <p>📅 {fecha_txt} · Segundo semestre 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Resumen académico")
st.write("Revisa tus notas, calcula la nota que necesitas en el examen, consulta tu horario y envía consultas a coordinación.")

# ------------------------------------------------------------------
# PESTAÑAS
# ------------------------------------------------------------------
tab_notas, tab_calc, tab_horario, tab_consultas = st.tabs(
    ["📊 Mis notas", "🎯 Meta del examen", "🗓️ Horario", "💬 Consultas"]
)

# ================= TAB 1: NOTAS =================
with tab_notas:
    st.subheader("Seguimiento de notas del semestre")
    st.caption("Edita las notas directamente en la tabla (escala 1,0 a 7,0). Puedes agregar o quitar ramos.")

    st.markdown("**Ponderaciones de la evaluación**")
    c1, c2, c3, c4 = st.columns(4)
    p1 = c1.slider("Solemne 1 (%)", 10, 30, 20, step=5)
    p2 = c2.slider("Solemne 2 (%)", 10, 30, 20, step=5)
    p3 = c3.slider("Solemne 3 (%)", 10, 30, 30, step=5)
    pe = 100 - p1 - p2 - p3
    c4.metric("Examen (%)", pe)

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
            "Solemne 3": [5.5, 4.4, 6.1, 4.0, 5.2],
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
            "Solemne 3": formato_nota,
            "Examen": formato_nota,
        },
        key="tabla_notas",
    )

    # --- Procesamiento ---
    df = editado.copy()
    df["Asignatura"] = df["Asignatura"].fillna("Sin nombre")
    columnas_notas = ["Solemne 1", "Solemne 2", "Solemne 3", "Examen"]
    for col in columnas_notas:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Nota final"] = (
        (df["Solemne 1"] * p1 + df["Solemne 2"] * p2 + df["Solemne 3"] * p3 + df["Examen"] * pe) / 100
    ).round(1)


    def estado(nota):
        if pd.isna(nota):
            return "—"
        if nota >= 4.0:
            return "✅ Aprobado"
        if nota >= 3.5:
            return "⚠️ En riesgo"
        return "❌ Reprobado"


    df["Estado"] = df["Nota final"].apply(estado)
    validos = df.dropna(subset=["Nota final"])

    # --- Salida ---
    st.markdown("#### Resultados del semestre")
    if validos.empty:
        st.info("Completa las cuatro notas de al menos un ramo para ver tus resultados.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Promedio general", f"{validos['Nota final'].mean():.1f}")
        mejor = validos.loc[validos["Nota final"].idxmax()]
        m2.metric("Mejor ramo", f"{mejor['Nota final']:.1f}", mejor["Asignatura"], delta_color="off")
        en_riesgo = int((validos["Nota final"] < 4.0).sum())
        m3.metric("Ramos bajo 4,0", en_riesgo)

        izq, der = st.columns([3, 2])
        with izq:
            st.dataframe(df[["Asignatura", "Nota final", "Estado"]], hide_index=True)
        with der:
            st.bar_chart(validos.set_index("Asignatura")["Nota final"], color="#C9A96A")

# ================= TAB 2: META DEL EXAMEN =================
with tab_calc:
    st.subheader("¿Qué nota necesito en el examen?")
    st.caption(f"Ponderaciones actuales: S1 {p1}% · S2 {p2}% · S3 {p3}% · Examen {pe}%")

    a, b, c, d = st.columns(4)
    s1 = a.number_input("Nota Solemne 1", 1.0, 7.0, 4.5, 0.1)
    s2 = b.number_input("Nota Solemne 2", 1.0, 7.0, 4.0, 0.1)
    s3 = c.number_input("Nota Solemne 3", 1.0, 7.0, 4.8, 0.1)
    meta = d.number_input("Nota final deseada", 1.0, 7.0, 4.0, 0.1)

    acumulado = (s1 * p1 + s2 * p2 + s3 * p3) / 100
    necesaria = (meta * 100 - s1 * p1 - s2 * p2 - s3 * p3) / pe

    r1, r2 = st.columns(2)
    r1.metric("Puntaje acumulado antes del examen", f"{acumulado:.2f}")
    r2.metric("Nota necesaria en el examen", f"{min(max(necesaria, 1.0), 7.0):.1f}")

    if necesaria <= 1.0:
        st.success("Ya alcanzaste tu meta: aprobarías incluso con un 1,0 en el examen.")
    elif necesaria > 7.0:
        st.error(f"Con tus notas actuales necesitarías un {necesaria:.1f} en el examen, lo que supera el 7,0. Conviene ajustar la meta.")
    else:
        st.progress((necesaria - 1.0) / 6.0, text=f"Nota requerida en el examen: {necesaria:.1f}")
        if necesaria <= 4.0:
            st.info("La meta es alcanzable con una preparación normal del examen.")
        elif necesaria <= 5.5:
            st.warning("Necesitarás una buena preparación para lograr tu meta.")
        else:
            st.warning("El examen será exigente: conviene planificar tus horas de estudio con anticipación.")

    st.markdown("#### Nota final según tu resultado en el examen")
    notas_examen = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    escenarios = pd.DataFrame(
        {"Nota final": [(s1 * p1 + s2 * p2 + s3 * p3 + n * pe) / 100 for n in notas_examen]},
        index=pd.Index(notas_examen, name="Nota del examen"),
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
    dia = st.selectbox("Selecciona el día", DIAS[:5], index=dia_defecto)
    clases_dia = horario[horario["Día"] == dia][["Bloque", "Asignatura", "Sala"]]

    if AHORA.weekday() >= 5:
        st.info("Hoy es fin de semana. Se muestra el horario del día que seleccionaste.")
    if clases_dia.empty:
        st.success(f"No tienes clases el {dia.lower()}.")
    else:
        st.write(f"**Tienes {len(clases_dia)} clase(s) el {dia.lower()}:**")
        st.dataframe(clases_dia, hide_index=True)

    with st.expander("Ver horario de la semana completa"):
        st.dataframe(horario, hide_index=True)

# ================= TAB 4: CONSULTAS =================
with tab_consultas:
    st.subheader("Consultas a coordinación académica")
    st.caption("Escribe tu consulta y recibirás un folio para hacerle seguimiento.")

    texto = st.text_area(
        "Describe tu consulta",
        placeholder="Ejemplo: Quisiera revisar la nota de mi Solemne 2 de Finanzas Corporativas.",
        height=120,
    )

    if st.button("Enviar consulta"):
        if texto.strip():
            numero = len(st.session_state.consultas) + 1
            folio = f"USS-{AHORA.strftime('%Y%m%d')}-{numero:04d}"
            st.session_state.consultas.append(
                {
                    "Folio": folio,
                    "Fecha": AHORA.strftime("%d/%m/%Y %H:%M"),
                    "Categoría": clasificar(texto),
                    "Palabras": len(texto.split()),
                    "Consulta": texto.strip(),
                }
            )
            st.success(f"Consulta recibida. Tu folio de seguimiento es {folio}.")
        else:
            st.warning("Escribe tu consulta antes de enviarla.")

    if st.session_state.consultas:
        st.markdown("#### Consultas enviadas")
        k1, k2 = st.columns(2)
        k1.metric("Consultas enviadas", len(st.session_state.consultas))
        k2.metric("Última categoría", st.session_state.consultas[-1]["Categoría"])
        st.dataframe(pd.DataFrame(st.session_state.consultas), hide_index=True)
    else:
        st.info("Todavía no has enviado consultas en esta sesión.")

# ------------------------------------------------------------------
# PIE DE PÁGINA
# ------------------------------------------------------------------
st.divider()
st.caption("Universidad San Sebastián · Proyecto académico desarrollado con Streamlit")
