import streamlit as st
import plotly.express as px

from data_loader import load_dataframe

st.set_page_config(
    page_title="Exploración | SaaS Churn Intelligence",
    page_icon="📊",
    layout="wide",
)

# Encabezado Principal
st.title("🚀 Exploración de Clientes")
st.caption("Panel interactivo para el análisis descriptivo de la muestra de clientes")

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

st.caption("ℹ️ *Nota: La proporción de churn corresponde a los clientes de esta muestra; no representa una tasa mensual ni demuestra las causas del abandono.*")

st.divider()

# Distribución del churn
st.subheader("📊 Distribución del Churn")

churn_summary = (
    df["Churn"]
    .value_counts()
    .reindex(["No", "Yes"], fill_value=0)
    .rename_axis("Churn")
    .reset_index(name="Clientes")
)

churn_summary["Estado"] = churn_summary["Churn"].map(
    {"No": "Permanece", "Yes": "Abandonó"}
)

fig_churn = px.bar(
    churn_summary,
    x="Estado",
    y="Clientes",
    text="Clientes",
    title="Clientes según estado de churn",
    labels={"Estado": "Estado del cliente", "Clientes": "Número de clientes"},
)
fig_churn.update_layout(showlegend=False)
st.plotly_chart(fig_churn, width="stretch")

st.divider()

# Churn por tipo de contrato
st.subheader("📋 Churn por Tipo de Contrato")

contract_summary = (
    df.groupby("Contract", dropna=False)
    .agg(
        Clientes=("customerID", "size"),
        Clientes_con_churn=("Churn", lambda s: (s == "Yes").sum()),
    )
    .reset_index()
)

contract_summary["Proporcion_churn"] = (
    contract_summary["Clientes_con_churn"] / contract_summary["Clientes"]
)

fig_contract = px.bar(
    contract_summary,
    x="Contract",
    y="Proporcion_churn",
    text=contract_summary["Proporcion_churn"].map(lambda x: f"{x:.1%}"),
    title="Proporción de churn dentro de cada tipo de contrato",
    labels={
        "Contract": "Tipo de contrato",
        "Proporcion_churn": "Proporción de churn",
    },
)
fig_contract.update_yaxes(tickformat=".0%")
st.plotly_chart(fig_contract, width="stretch")

st.caption(
    "ℹ️ *Nota: Las diferencias entre contratos son asociaciones descriptivas; "
    "no permiten concluir que el contrato cause el abandono.*"
)

st.divider()

# Tabla con filtros
st.subheader("🔍 Explorar Registros")

available_columns = [
    column
    for column in [
        "customerID",
        "Churn",
        "tenure",
        "Contract",
        "MonthlyCharges",
        "TotalCharges",
    ]
    if column in df.columns
]

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    churn_options = ["Todos"] + sorted(
        df["Churn"].dropna().astype(str).unique().tolist()
    )
    selected_churn = st.selectbox("Estado de churn", churn_options)

with filter_col2:
    contract_options = ["Todos"] + sorted(
        df["Contract"].dropna().astype(str).unique().tolist()
    )
    selected_contract = st.selectbox("Tipo de contrato", contract_options)

filtered_df = df.copy()

if selected_churn != "Todos":
    filtered_df = filtered_df[
        filtered_df["Churn"].astype(str) == selected_churn
    ]

if selected_contract != "Todos":
    filtered_df = filtered_df[
        filtered_df["Contract"].astype(str) == selected_contract
    ]

st.caption(f"Registros encontrados: **{len(filtered_df):,}**")

st.dataframe(
    filtered_df[available_columns],
    width="stretch",
    hide_index=True,
)