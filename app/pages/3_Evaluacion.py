import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_model_artifact

st.set_page_config(
    page_title="Evaluación | SaaS Churn Intelligence",
    page_icon="📊",
    layout="wide",
)

# Encabezado Principal
st.title("🚀 Evaluación del Modelo")
st.caption("Panel de control para el análisis de rendimiento observado en el conjunto de prueba")

try:
    artifact = load_model_artifact()
except (FileNotFoundError, ValueError, RuntimeError) as exc:
    st.error(f"❌ No se pudo cargar el modelo: {exc}")
    st.stop()

model = artifact["model"]

# Resultados obtenidos en el notebook de entrenamiento.
metrics = {
    "Decision Tree": {
        "Accuracy": 0.7991483321504613,
        "Precision": 0.6318840579710145,
        "Recall": 0.5828877005347594,
        "F1-score": 0.6063977746870653,
        "Falsos positivos": 127,
        "Falsos negativos": 156,
    },
    "Regresión Logística": {
        "Accuracy": 0.8005677785663591,
        "Precision": 0.6495176848874598,
        "Recall": 0.5401069518716578,
        "F1-score": 0.5897810218978102,
        "Falsos positivos": 109,
        "Falsos negativos": 172,
    },
}

st.divider()

# Modelo seleccionado
st.subheader("🤖 Modelo Seleccionado")

model_col1, model_col2, model_col3 = st.columns(3)
model_col1.metric("Modelo Activo", artifact["model_name"])
model_col2.metric(
    "Variables de entrada",
    f"{len(artifact['feature_columns'])}",
)
model_col3.metric(
    "Profundidad del árbol",
    str(model.get_depth()) if hasattr(model, "get_depth") else "No disponible",
)

st.caption(
    "ℹ️ *Nota: El artefacto del modelo contiene el clasificador. "
    "Las métricas de esta página proceden de las salidas guardadas en el notebook de entrenamiento y no se recalculan en tiempo real.*"
)

st.divider()

# Métricas del modelo seleccionado
selected = metrics["Decision Tree"]

st.subheader("📈 Métricas de Rendimiento")

metric_cols = st.columns(4)
metric_cols[0].metric("Accuracy", f"{selected['Accuracy']:.1%}")
metric_cols[1].metric("Precision", f"{selected['Precision']:.1%}")
metric_cols[2].metric("Recall", f"{selected['Recall']:.1%}")
metric_cols[3].metric("F1-score", f"{selected['F1-score']:.1%}")

with st.expander("📖 ¿Qué significa cada métrica?"):
    st.markdown(
        """
        - **Accuracy:** proporción de predicciones correctas entre todos los clientes del conjunto de prueba.
        - **Precision:** proporción de predicciones de churn que correspondieron a clientes que realmente abandonaron.
        - **Recall:** proporción de clientes que realmente abandonaron y fueron detectados por el modelo.
        - **F1-score:** media armónica de precision y recall.
        """
    )

st.divider()

# Matriz de confusión
st.subheader("🧩 Matriz de Confusión")

confusion = pd.DataFrame(
    [[908, 127], [156, 218]],
    index=["Real: No", "Real: Yes"],
    columns=["Predicción: No", "Predicción: Yes"],
)

fig_confusion = go.Figure(
    data=go.Heatmap(
        z=confusion.values,
        x=confusion.columns.tolist(),
        y=confusion.index.tolist(),
        text=confusion.values,
        texttemplate="%{text}",
        colorscale="Blues",
        showscale=False,
    )
)

fig_confusion.update_layout(
    title="Decision Tree — Conjunto de prueba",
    xaxis_title="Clase predicha",
    yaxis_title="Clase real",
)
st.plotly_chart(fig_confusion, width="stretch")

error_col1, error_col2 = st.columns(2)
error_col1.metric("⚠️ Falsos negativos", f"{selected['Falsos negativos']}")
error_col2.metric("⚠️ Falsos positivos", f"{selected['Falsos positivos']}")

st.info(
    "💡 **Nota de errores:** Un falso negativo es un cliente que abandonó pero el modelo "
    "clasificó como No. Un falso positivo es un cliente que permaneció pero el modelo clasificó como Yes."
)

st.divider()

# Comparación de modelos
st.subheader("⚖️ Comparación de Modelos")

comparison_rows = []
for name, values in metrics.items():
    comparison_rows.append({
        "Modelo": name,
        "Accuracy": values["Accuracy"],
        "Precision": values["Precision"],
        "Recall": values["Recall"],
        "F1-score": values["F1-score"],
        "Falsos negativos": values["Falsos negativos"],
        "Falsos positivos": values["Falsos positivos"],
    })

comparison = pd.DataFrame(comparison_rows)

fig_comparison = px.bar(
    comparison.melt(
        id_vars="Modelo",
        value_vars=["Accuracy", "Precision", "Recall", "F1-score"],
        var_name="Métrica",
        value_name="Valor",
    ),
    x="Métrica",
    y="Valor",
    color="Modelo",
    barmode="group",
    title="Comparativa de métricas entre clasificadores",
    labels={"Valor": "Puntuación"},
)
fig_comparison.update_yaxes(tickformat=".0%", range=[0, 1])
st.plotly_chart(fig_comparison, width="stretch")

display_comparison = comparison.copy()
for column in ["Accuracy", "Precision", "Recall", "F1-score"]:
    display_comparison[column] = display_comparison[column].map(
        lambda value: f"{value:.1%}"
    )

st.dataframe(display_comparison, width="stretch", hide_index=True)

st.markdown(
    """
    > 📊 **Lectura del resultado:** El Decision Tree presenta mayor recall y 
    > F1-score en este conjunto de prueba, mientras que la Regresión 
    > Logística obtiene una accuracy y una precision ligeramente superiores. 
    > La elección depende también del coste operativo de los distintos errores.
    """
)

st.divider()

# Limitaciones
st.subheader("⚠️ Limitaciones de la Evaluación")

st.markdown(
    """
    - Los resultados corresponden a un único conjunto de prueba de **1.409 registros**, separado mediante una división estratificada con `random_state=42`.
    - Las métricas no garantizan exactamente el mismo rendimiento operativo con datos productivos nuevos.
    - Los falsos negativos demuestran que el modelo actual todavía no detecta todos los casos de churn observado.
    - Una predicción de churn no constituye una garantía de que un cliente vaya a abandonar de forma inminente.
    - El conjunto de datos utilizado es una muestra Telco adaptada para fines didácticos; no representa datos financieros o de uso reales de una empresa SaaS B2B.
    """
)