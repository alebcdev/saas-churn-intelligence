import streamlit as st
import plotly.express as px

from data_loader import load_dataframe

st.set_page_config(
    page_title="Segmentación | SaaS Churn Intelligence",
    page_icon="📊",
    layout="wide",
)

# Encabezado Principal
st.title("🚀 Segmentación de Clientes")
st.caption("Panel interactivo para la comparación descriptiva de perfiles de clientes")

# Carga de Datos
try:
    df = load_dataframe("segments")
except (FileNotFoundError, ValueError, RuntimeError) as exc:
    st.error(f"❌ No se pudieron cargar los datos: {exc}")
    st.stop()

# Preparación de datos
df = df.copy()
df["segment"] = df["segment"].astype(str)

segment_summary = (
    df.groupby("segment", dropna=False)
    .agg(
        clientes=("customerID", "size"),
        clientes_con_churn=("churn_target", "sum"),
        antiguedad_media=("tenure", "mean"),
        cargo_mensual_medio=("MonthlyCharges", "mean"),
        servicios_medios=("num_services_contracted", "mean"),
    )
    .reset_index()
)

segment_summary["proporcion_churn"] = (
    segment_summary["clientes_con_churn"]
    / segment_summary["clientes"]
)

contract_modes = (
    df.groupby("segment")["Contract"]
    .agg(lambda values: (
        values.mode().iloc[0] if not values.mode().empty else "Sin dato"
    ))
    .rename("contrato_predominante")
    .reset_index()
)

segment_summary = segment_summary.merge(
    contract_modes,
    on="segment",
    how="left",
)

# Indicadores generales
total_customers = len(df)
total_segments = df["segment"].nunique()
total_churn_count = int(segment_summary["clientes_con_churn"].sum())
global_churn_rate = total_churn_count / total_customers if total_customers else 0

highest_churn_segment = segment_summary.loc[
    segment_summary["proporcion_churn"].idxmax()
]

st.divider()

# Sección de Métricas en Tarjetas
st.subheader("📈 Resumen General")

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Clientes", f"{total_customers:,}")
col2.metric("🧩 Segmentos", f"{total_segments}")
col3.metric("📊 Churn Global", f"{global_churn_rate:.2%}")
col4.metric(
    "⚠️ Mayor Churn",
    f"{highest_churn_segment['proporcion_churn']:.1%}",
    help=f"Segmento {highest_churn_segment['segment']}. Es una proporción observada, no una predicción.",
)

st.caption(
    "ℹ️ *Nota: Los segmentos describen grupos de clientes de esta muestra. "
    "El churn mostrado es observado y no representa una probabilidad individual de abandono futuro.*"
)

st.divider()

# Distribución de clientes
st.subheader("📊 Distribución de Clientes por Segmento")

fig_size = px.bar(
    segment_summary,
    x="segment",
    y="clientes",
    text="clientes",
    labels={
        "segment": "Segmento",
        "clientes": "Número de clientes",
    },
    title="Número de clientes en cada segmento",
)
fig_size.update_layout(showlegend=False)
st.plotly_chart(fig_size, width="stretch")

st.divider()

# Comparación de churn
st.subheader("📉 Proporción de Churn Observado")

fig_churn = px.bar(
    segment_summary,
    x="segment",
    y="proporcion_churn",
    text=segment_summary["proporcion_churn"].map(lambda value: f"{value:.1%}"),
    labels={
        "segment": "Segmento",
        "proporcion_churn": "Proporción de churn",
    },
    title="Porcentaje de clientes con churn en cada segmento",
)
fig_churn.update_yaxes(tickformat=".0%", rangemode="tozero")
fig_churn.update_layout(showlegend=False)
st.plotly_chart(fig_churn, width="stretch")

st.divider()

# --- Perfil detallado ---
st.subheader("🔍 Perfil de Cada Segmento")

segment_options = sorted(segment_summary["segment"].unique())
selected_segment = st.selectbox(
    "Selecciona un segmento para ver su detalle",
    options=segment_options,
)

selected_profile = segment_summary[
    segment_summary["segment"] == selected_segment
].iloc[0]

profile_col1, profile_col2, profile_col3 = st.columns(3)
profile_col1.metric("Clientes del segmento", f"{int(selected_profile['clientes']):,}")
profile_col2.metric(
    "Churn observado",
    f"{selected_profile['proporcion_churn']:.1%}",
)
profile_col3.metric(
    "Antigüedad media",
    f"{selected_profile['antiguedad_media']:.1f} meses",
)

st.write(
    f"🔹 **Contrato predominante:** "
    f"{selected_profile['contrato_predominante']}"
)

st.write(
    f"💵 **Cargo mensual medio:** "
    f"${selected_profile['cargo_mensual_medio']:.2f}"
)

st.write(
    f"🛠️ **Número medio de servicios contratados:** "
    f"{selected_profile['servicios_medios']:.2f}"
)

st.divider()

st.subheader("📋 Resumen Comparativo de Segmentos")

display_summary = segment_summary.rename(
    columns={
        "segment": "Segmento",
        "clientes": "Clientes",
        "clientes_con_churn": "Clientes con churn",
        "proporcion_churn": "Proporción de churn",
        "antiguedad_media": "Antigüedad media (meses)",
        "cargo_mensual_medio": "Cargo mensual medio",
        "servicios_medios": "Servicios medios",
        "contrato_predominante": "Contrato predominante",
    }
).copy()

display_summary["Proporción de churn"] = (
    display_summary["Proporción de churn"].map(lambda value: f"{value:.1%}")
)

for column in [
    "Antigüedad media (meses)",
    "Cargo mensual medio",
    "Servicios medios",
]:
    display_summary[column] = display_summary[column].round(2)

st.dataframe(
    display_summary,
    width="stretch",
    hide_index=True,
)