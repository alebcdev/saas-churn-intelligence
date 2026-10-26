import streamlit as st
from data_loader import load_dataframe

st.set_page_config(
    page_title="SaaS Churn Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("🚀 SaaS Churn Intelligence")
st.caption("Panel de control y análisis descriptivo de abandono de clientes")

# Carga de Datos
try:
    df = load_dataframe("cleaned")
except (FileNotFoundError, ValueError, RuntimeError) as exc:
    st.error(f"❌ No se pudieron cargar los datos: {exc}")
    st.stop()

# Cálculo de Métricas
total_customers = len(df)
churn_count = int((df["Churn"] == "Yes").sum())
churn_rate = churn_count / total_customers if total_customers else 0
retention_rate = 1 - churn_rate

st.divider()

# Sección de Métricas en Tarjetas
st.subheader("📈 Resumen General")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Clientes", f"{total_customers:,}")
col2.metric("⚠️ Clientes con Churn", f"{churn_count:,}")
col3.metric("📊 Tasa de Churn", f"{churn_rate:.2%}")
col4.metric("🛡️ Tasa de Retención", f"{retention_rate:.2%}")

st.caption("ℹ️ *Nota: La proporción mostrada corresponde a los clientes de la muestra analizada; no representa una tasa mensual de churn.*")

st.divider()

# Vista Previa de los Datos
st.subheader("🔍 Vista Previa de los Datos Limpios")
st.markdown("A continuación se muestran los primeros registros del conjunto de datos analizado:")

st.dataframe(df.head(10), width="stretch")