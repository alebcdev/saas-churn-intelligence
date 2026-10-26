
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEANED_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned.parquet"
FEATURES_PATH = PROJECT_ROOT / "data" / "processed" / "features.parquet"
SEGMENTS_PATH = PROJECT_ROOT / "data" / "processed" / "customer_segments.parquet"
MODEL_PATH = PROJECT_ROOT / "models" / "churn_model.joblib"


REQUIRED_COLUMNS = {
    "cleaned": {
        "customerID",
        "Churn",
        "tenure",
        "Contract",
        "MonthlyCharges",
        "TotalCharges",
    },
    "features": {
        "customerID",
        "Churn",
        "churn_target",
        "tenure_group",
        "monthly_charge_group",
    },
    "segments": {
        "customerID",
        "Churn",
        "segment",
    },
}


@st.cache_data(show_spinner=False)
def _read_parquet(path_string: str) -> pd.DataFrame:
    """Lee un Parquet y almacena en caché el resultado."""
    return pd.read_parquet(path_string)


def load_dataframe(dataset_name: str) -> pd.DataFrame:
    """Carga y valida uno de los conjuntos de datos permitidos."""
    paths = {
        "cleaned": CLEANED_PATH,
        "features": FEATURES_PATH,
        "segments": SEGMENTS_PATH,
    }

    if dataset_name not in paths:
        raise ValueError(
            f"Conjunto desconocido: {dataset_name!r}. "
            f"Opciones válidas: {', '.join(paths)}."
        )

    path = paths[dataset_name]

    if not path.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo necesario: {path}"
        )

    try:
        df = _read_parquet(str(path))
    except Exception as exc:
        raise RuntimeError(
            f"No se pudo leer el archivo {path.name}: {exc}"
        ) from exc

    missing_columns = REQUIRED_COLUMNS[dataset_name] - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"El archivo {path.name} no contiene las columnas "
            f"requeridas: {missing}"
        )

    if df["customerID"].isna().any():
        raise ValueError(
            f"El archivo {path.name} contiene customerID nulos."
        )

    if df["customerID"].duplicated().any():
        raise ValueError(
            f"El archivo {path.name} contiene customerID duplicados."
        )

    return df


@st.cache_resource(show_spinner=False)
def load_model_artifact() -> dict:
    """Carga y valida el artefacto local del modelo."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"No se encontró el modelo: {MODEL_PATH}"
        )

    try:
        artifact = joblib.load(MODEL_PATH)
    except Exception as exc:
        raise RuntimeError(
            f"No se pudo cargar el artefacto del modelo: {exc}"
        ) from exc

    if not isinstance(artifact, dict):
        raise ValueError(
            "El artefacto del modelo debe ser un diccionario."
        )

    required_keys = {
        "model",
        "model_name",
        "feature_columns",
        "categorical_columns",
        "monthly_charge_q1",
        "monthly_charge_q2",
    }

    missing_keys = required_keys - set(artifact.keys())

    if missing_keys:
        raise ValueError(
            "Faltan claves en el artefacto del modelo: "
            + ", ".join(sorted(missing_keys))
        )

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    if not isinstance(feature_columns, list) or not feature_columns:
        raise ValueError(
            "feature_columns debe ser una lista no vacía."
        )

    if len(feature_columns) != len(set(feature_columns)):
        raise ValueError(
            "feature_columns contiene columnas duplicadas."
        )

    if not hasattr(model, "predict"):
        raise ValueError(
            "El objeto model no dispone del método predict()."
        )

    if getattr(model, "n_features_in_", None) != len(feature_columns):
        raise ValueError(
            "El número de columnas del modelo no coincide "
            "con feature_columns."
        )

    return artifact
