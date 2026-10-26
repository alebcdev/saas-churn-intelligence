# SaaS Churn Intelligence

**Análisis de abandono de clientes, segmentación y Machine Learning aplicado a un caso de negocio B2B SaaS.**

SaaS Churn Intelligence es un proyecto de análisis de datos que estudia los patrones asociados al abandono de clientes (*customer churn*) mediante análisis exploratorio, ingeniería de variables, clasificación y segmentación.

El proyecto incorpora una aplicación interactiva desarrollada con Streamlit para explorar los datos, consultar los segmentos de clientes y revisar los resultados y las limitaciones del modelo.

> **Importante:** este proyecto utiliza el dataset IBM Telco Customer Churn como base para un caso de negocio ficticio B2B SaaS. Los datos originales corresponden al sector de las telecomunicaciones y no representan clientes reales de una empresa SaaS.

## Índice

- [Objetivos](#objetivos)
- [Funcionalidades](#funcionalidades)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Datos y metodología](#datos-y-metodología)
- [Resultados del modelo](#resultados-del-modelo)
- [Limitaciones](#limitaciones)
- [Posibles mejoras](#posibles-mejoras)
- [Fuente de los datos](#fuente-de-los-datos)
- [Autoría](#autoría)

## Objetivos

- Analizar las características de los clientes y su relación descriptiva con el abandono.
- Realizar un análisis exploratorio para identificar patrones relevantes.
- Preparar y transformar variables para el entrenamiento de modelos de Machine Learning.
- Entrenar y evaluar un modelo de clasificación para estudiar el abandono.
- Identificar y analizar segmentos de clientes.
- Comunicar los resultados de forma visual e interactiva.
- Documentar las limitaciones del análisis y evitar interpretaciones que no estén respaldadas por los datos.

## Funcionalidades

La aplicación está organizada en cinco páginas:

| Página | Descripción |
|---|---|
| **Principal** | Presentación, contexto y objetivos del proyecto. |
| **Exploración** | Análisis exploratorio y visualización de las características de los clientes. |
| **Segmentación** | Consulta de segmentos y análisis de sus características. |
| **Evaluación** | Visualización de las métricas y la matriz de confusión del modelo. |
| **Limitaciones** | Explicación del alcance, las restricciones y las precauciones de interpretación. |

La navegación se realiza mediante el sistema multipágina de Streamlit.

## Tecnologías

Las principales herramientas y librerías utilizadas son:

- **Python:** lenguaje principal del proyecto.
- **Pandas y NumPy:** manipulación y análisis de datos.
- **Scikit-learn:** entrenamiento y evaluación del modelo de clasificación.
- **Joblib:** almacenamiento y carga del modelo entrenado.
- **PyArrow:** lectura y escritura de archivos Parquet.
- **Matplotlib y Seaborn:** visualización de datos.
- **Plotly:** gráficos interactivos.
- **Streamlit:** desarrollo de la aplicación web.
- **Jupyter Notebook e IPykernel:** exploración y desarrollo del análisis.

Las versiones de las dependencias se encuentran especificadas en `requirements.txt`.

## Estructura del proyecto

```text
saas-churn-intelligence/
├── app/
│   ├── pages/
│   │   ├── 0_Principal.py
│   │   ├── 1_Exploracion.py
│   │   ├── 2_Segmentacion.py
│   │   ├── 3_Evaluacion.py
│   │   └── 4_Limitaciones.py
│   ├── app.py
│   └── data_loader.py
├── data/
│   ├── processed/
│   │   ├── cleaned.parquet
│   │   ├── customer_segments.parquet
│   │   └── features.parquet
│   └── raw/
│       └── telco_customer_churn.csv
├── models/
│   └── churn_model.joblib
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_segmentation.ipynb
├── reports/
│   └── executive_summary.md
├── .gitignore
├── README.md
└── requirements.txt
```

### Organización de los componentes

- `app/`: contiene la aplicación Streamlit, el módulo de carga de datos y las páginas de navegación.
- `data/raw/`: contiene el dataset original.
- `data/processed/`: contiene los conjuntos de datos procesados utilizados en el análisis y la aplicación.
- `models/`: almacena el modelo de clasificación entrenado.
- `notebooks/`: contiene los notebooks del análisis exploratorio, la ingeniería de variables, el entrenamiento y la segmentación.
- `reports/`: contiene el resumen ejecutivo del proyecto.
- `requirements.txt`: define las dependencias de Python necesarias para ejecutar el proyecto.
- `.gitignore`: especifica los archivos y directorios que Git debe excluir del control de versiones.

## Instalación y ejecución

### Requisitos previos

- Python 3.12.
- Git, si se desea clonar el repositorio.
- Los archivos de datos procesados y el modelo incluidos en el proyecto.

### 1. Clonar el repositorio

Una vez publicado en GitHub, ejecuta:

```bash
git clone https://github.com/alebcdev/saas-churn-intelligence.git
cd saas-churn-intelligence
```

Sustituye `TU_USUARIO` por tu nombre de usuario de GitHub.

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
py -3.12 -m venv .venv
```

Activa el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

Con el entorno virtual activado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

Desde la raíz del proyecto, ejecuta:

```bash
streamlit run app/app.py
```

Streamlit mostrará la dirección local de la aplicación. Normalmente se podrá abrir en:

`http://localhost:8501`

La aplicación necesita que los archivos de datos procesados y el artefacto del modelo estén disponibles en las rutas esperadas por el código.

## Datos y metodología

El proyecto sigue un flujo de trabajo organizado en cuatro notebooks:

1. **Análisis exploratorio (`01_eda.ipynb`):** exploración de las variables, revisión de la distribución de los datos e identificación de patrones descriptivos.
2. **Ingeniería de variables (`02_feature_engineering.ipynb`):** preparación de los datos y transformación de las variables para el modelado.
3. **Entrenamiento del modelo (`03_model_training.ipynb`):** entrenamiento y evaluación de modelos de clasificación.
4. **Segmentación (`04_segmentation.ipynb`):** análisis de grupos de clientes con características compartidas.

Los datos procesados se guardan en formato Parquet y el modelo entrenado se almacena mediante Joblib.

Esta separación permite distinguir entre los datos originales, los conjuntos preparados para el análisis y los artefactos empleados por la aplicación.

## Resultados del modelo

El modelo de clasificación evaluado en el proyecto es un **Decision Tree** (*árbol de decisión*).

En la ejecución reproducida del notebook de entrenamiento se obtuvieron las siguientes métricas:

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.7991 |
| Precision | 0.6319 |
| Recall | 0.5829 |
| F1-score | 0.6064 |

La matriz de confusión obtenida fue:

| Clase real | Predicción: no churn | Predicción: churn |
|---|---:|---:|
| No churn | 908 | 127 |
| Churn | 156 | 218 |

Interpretación de las métricas:

- **Accuracy:** proporción total de predicciones correctas.
- **Precision:** proporción de predicciones positivas de churn que fueron correctas.
- **Recall:** proporción de los casos reales de churn identificados por el modelo.
- **F1-score:** media armónica entre precision y recall.

Los resultados muestran el rendimiento obtenido durante la evaluación realizada. No garantizan el mismo comportamiento en otros conjuntos de datos o en un entorno productivo.

## Limitaciones

Es importante considerar las siguientes limitaciones antes de interpretar los resultados:

- **Naturaleza de los datos:** el dataset original pertenece al sector de las telecomunicaciones. Su uso como caso B2B SaaS es una adaptación didáctica, no una validación en datos reales de una empresa SaaS.
- **Proporción de churn:** el 26,54 % corresponde a la proporción de clientes que abandonan dentro de la muestra analizada. No debe interpretarse como una tasa mensual de churn de una empresa.
- **Análisis descriptivo:** las asociaciones observadas entre variables y abandono no demuestran causalidad.
- **Segmentación:** los segmentos representan grupos con características compartidas. No equivalen a probabilidades individuales de abandono.
- **Generalización:** las métricas de evaluación no garantizan que el modelo funcione igual en otros periodos, empresas o poblaciones.
- **Inferencia individual:** la versión actual de la aplicación muestra métricas de evaluación precomputadas y no implementa un flujo completo de predicción para introducir nuevos clientes y obtener predicciones individuales.
- **Uso empresarial:** antes de utilizar el modelo para tomar decisiones de retención, sería necesario validarlo con datos representativos del negocio y evaluar sus implicaciones operativas.

## Posibles mejoras

Como evolución del proyecto, se podrían implementar las siguientes mejoras:

- Incorporar un flujo de inferencia para evaluar nuevos registros de clientes.
- Añadir pruebas automatizadas para validar los datos, las transformaciones y las predicciones.
- Mejorar la trazabilidad entre el entrenamiento, el modelo almacenado y las métricas mostradas.
- Evaluar el modelo con datos temporales o externos para estudiar su capacidad de generalización.
- Definir métricas de negocio que permitan valorar el impacto de las estrategias de retención.
- Incorporar mecanismos de seguimiento del rendimiento del modelo si se desplegara en un entorno productivo.

## Fuente de los datos

El proyecto utiliza el dataset **Telco Customer Churn IBM Dataset**, publicado en Kaggle:

[https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset)

El conjunto de datos contiene 7.043 registros de clientes de telecomunicaciones. La variable objetivo identifica si un cliente abandonó el servicio.

Los datos se emplean con fines educativos y de portfolio para demostrar un flujo de análisis de datos, clasificación y segmentación.

**Licencia y redistribución:** antes de distribuir públicamente el dataset original junto con el código, deben comprobarse las condiciones de uso y redistribución aplicables en la fuente. La publicación de este proyecto no implica que los datos originales sean propiedad del autor del proyecto.

## Autoría

Proyecto de portfolio de Data Analytics centrado en el análisis de abandono de clientes, segmentación y Machine Learning.

