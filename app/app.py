import streamlit as st

st.set_page_config(
    page_title="SaaS Churn Intelligence",
    page_icon="📊",
    layout="wide",
)

pagina_inicio = st.Page(
    "pages/0_Principal.py",
    title="Inicio",
    icon="🚀",
    default=True
)

pagina_exploracion = st.Page(
    "pages/1_Exploracion.py",
    title="Exploración",
    icon="📊"
)

pagina_segmentacion = st.Page(
    "pages/2_Segmentacion.py",
    title="Segmentación",
    icon="🧩"
)

pagina_evaluacion = st.Page(
    "pages/3_Evaluacion.py",
    title="Evaluación",
    icon="📈"
)

pagina_limitaciones = st.Page(
    "pages/4_Limitaciones.py",
    title="Limitaciones y Conclusiones",
    icon="🧭"
)

# menú lateral agrupado por secciones
navegacion = st.navigation(
    {
        "Principal": [pagina_inicio],
        "Análisis": [pagina_exploracion, pagina_segmentacion],
        "Modelado": [pagina_evaluacion, pagina_limitaciones],
    }
)

# 3. Ejecutar la navegación
navegacion.run()