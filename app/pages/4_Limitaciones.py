import streamlit as st

st.set_page_config(
    page_title="Limitaciones y conclusiones | SaaS Churn Intelligence",
    page_icon="🧭",
    layout="wide",
)

# Encabezado Principal
st.title("🧭 Limitaciones y Conclusiones")
st.caption("Alcance del análisis, riesgos de interpretación y siguientes pasos estratégicos")

st.divider()

# Alcance de los datos
st.header("1. Alcance de los Datos")

st.markdown(
    """
    El análisis utiliza un dataset de clientes de telecomunicaciones (Telco) adaptado con fines didácticos a un caso ficticio de SaaS B2B. 
    Por tanto, los resultados permiten demostrar un flujo analítico completo de churn, pero no representan evidencia directa sobre clientes reales de una empresa SaaS.
    """
)

scope_col1, scope_col2, scope_col3 = st.columns(3)
scope_col1.metric("👥 Registros analizados", "7.043")
scope_col2.metric("⚠️ Churn observado", "26,54 %")
scope_col3.metric("🧩 Segmentos", "4")

st.caption(
    "ℹ️ *Nota: El 26,54 % es la proporción de clientes con churn en este dataset, no una tasa mensual recurrente ni una previsión futura.*"
)

st.divider()

# Limitaciones del modelo
st.header("2. Limitaciones del Modelo")

st.markdown(
    """
    La evaluación documentada corresponde a un conjunto de prueba aislado de 1.409 registros. El rendimiento medido puede variar notablemente al aplicar el modelo sobre datos nuevos o periodos temporales distintos.
    """
)

model_col1, model_col2, model_col3 = st.columns(3)
model_col1.metric("🎯 Recall", "58,3 %")
model_col2.metric("❌ Falsos negativos", "156")
model_col3.metric("⚠️ Falsos positivos", "127")

st.warning(
    "⚠️ **Atención operativa:** El modelo no detectó 156 de los 374 clientes que realmente presentaron churn en el conjunto de prueba. "
    "Por este motivo, no debe utilizarse como el único mecanismo automatizado para decidir qué clientes necesitan atención prioritaria."
)

with st.expander("📖 Otras limitaciones técnicas del modelo"):
    st.markdown(
        """
        - Las métricas expuestas proceden de las salidas guardadas del notebook de entrenamiento.
        - La evaluación presentada no garantiza que el rendimiento se mantenga estable de forma indefinida en producción.
        - Una predicción de churn es una estimación estadística del clasificador, no una certeza absoluta.
        - No se ha demostrado formalmente que las variables asociadas al churn funcionen como causas directas del mismo.
        """
    )

st.divider()

# Interpretación de segmentos
st.header("3. Interpretación de Segmentos")

st.markdown(
    """
    La segmentación permite resumir de forma efectiva características compartidas por grupos de clientes. Las etiquetas numéricas de los segmentos actúan como identificadores descriptivos, no como categorías comerciales inherentes.
    """
)

st.info(
    "💡 **Hallazgo clave:** El segmento 1 presenta el mayor churn observado (54,2 %), seguido de cerca por el segmento 3 (29,7 %). "
    "Estas diferencias son estrictamente descriptivas y no demuestran que pertenecer a un segmento provoque de forma causal el abandono."
)

st.markdown(
    """
    > 📌 **Recomendación analítica:** Investigar a profundidad las necesidades reales de los segmentos con mayor tasa de churn observada antes de implementar intervenciones comerciales masivas. 
    > Cualquier plan de acción debería validarse previamente mediante datos adicionales y pruebas controladas.
    """
)

st.divider()

# Recomendaciones de negocio
st.header("4. Recomendaciones de Negocio")

recommendations = [
    (
        "🤝 Validar con usuarios y negocio",
        "Contrastar los patrones detectados con el conocimiento experto de los equipos comerciales y de éxito de cliente que operan en el día a día.",
    ),
    (
        "🔍 Priorizar la investigación",
        "Examinar detenidamente los perfiles de los segmentos con mayor churn observado sin asumir que todos sus integrantes corren el mismo riesgo exacto.",
    ),
    (
        "⚖️ Evaluar el coste de los errores",
        "Definir con precisión el impacto financiero y operativo de los falsos negativos frente a los falsos positivos antes de fijar políticas de retención.",
    ),
    (
        "📈 Medir las intervenciones",
        "Comprobar rigurosamente con datos si las acciones de retención implementadas producen mejoras reales, evitando asumir que una correlación implica causalidad directa.",
    ),
]

for title, description in recommendations:
    with st.container(border=True):
        st.subheader(title)
        st.write(description)

st.divider()

# Conclusión Principal
st.subheader("🎯 Conclusión Principal")

st.markdown(
    """
    Este proyecto demuestra un flujo analítico robusto que combina la exploración de datos, la segmentación y la evaluación técnica de modelos predictivos de churn.

    **Conclusión general:** Los resultados obtenidos son útiles como punto de partida estratégico para formular hipótesis de negocio y guiar futuras líneas de investigación. 
    Antes de utilizarlos para tomar decisiones operativas de alto impacto en una compañía real, es imprescindible validarlos con datos SaaS específicos del negocio.
    """
)

st.caption(
    "ℹ️ *Proyecto didáctico: las conclusiones expuestas no deben interpretarse como resultados corporativos validados de una empresa SaaS real.*"
)