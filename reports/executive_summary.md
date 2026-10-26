# SaaS Customer Churn Intelligence
## Informe ejecutivo

## 1. Resumen ejecutivo

Este proyecto explora cómo los datos pueden ayudar a identificar patrones de abandono (*churn*), detectar clientes que podrían irse y describir perfiles útiles para orientar futuras acciones de retención.

Se utilizó el dataset público **IBM Telco Customer Churn** como ejemplo para un caso ficticio de SaaS B2B. Contiene **7.043 clientes**; **1.869 (26,54 %)** tienen `Churn = Yes`. Este porcentaje describe el conjunto analizado, no una tasa mensual.

Los principales hallazgos son:

- El churn observado es mayor entre clientes con contrato mensual (**42,71 %**), pago mediante `Electronic check` (**45,29 %**) y servicio `Fiber optic` (**41,89 %**).
- Se compararon Logistic Regression y Decision Tree. Se eligió **Decision Tree** por su mejor Recall (**0,583**) y F1 (**0,606**), aunque no detectó **156** casos de churn en el conjunto de prueba.
- La segmentación en cuatro grupos identificó un segmento de clientes mensuales con churn observado del **54,25 %**, el más alto de los grupos.

Estos resultados sirven para formular hipótesis y priorizar investigaciones, pero no demuestran causas ni el efecto de una intervención. 

## 2. Alcance y metodología

El trabajo combina tres enfoques:

1. **Análisis exploratorio (EDA):** revisión de calidad de los datos y comparación del churn entre características de clientes.
2. **Modelo predictivo:** comparación de Logistic Regression y Decision Tree con una división estratificada de entrenamiento y prueba del 80/20.
3. **Segmentación:** aplicación de K-Means para describir cuatro perfiles según antigüedad, cargos, contrato, Internet, método de pago y número de servicios adicionales.

En la preparación se detectaron **11 valores vacíos en `TotalCharges`**, todos asociados a clientes con `tenure = 0`. Se convirtieron a valores ausentes y se trataron durante la preparación para el modelado. No se encontraron filas duplicadas ni identificadores repetidos.

Se crearon variables derivadas como `tenure_group`, `monthly_charge_group`, `is_monthly_contract`, `num_services_contracted` y `uses_electronic_check`. Para el modelo se excluyeron identificadores y variables objetivo; también se descartaron indicadores redundantes con variables categóricas originales. Los puntos de corte de `monthly_charge_group` se calcularon con los datos de entrenamiento.

Para K-Means se codificaron las variables categóricas y se estandarizaron las variables. `Churn` no se usó para formar los grupos, sino después para describir el churn observado en cada segmento. Se eligió **K = 4** tras revisar valores entre 2 y 6 con el método del codo y considerar la interpretabilidad.

## 3. Hallazgos principales del EDA

La mediana de antigüedad (`tenure`) es de **10 meses** entre quienes abandonan y de **38 meses** entre quienes permanecen. Esto señala que conviene investigar la experiencia durante los primeros meses de relación.

La mediana de `MonthlyCharges` es **79,65** para clientes con churn y **64,43** para quienes permanecen. En cambio, la mediana de `TotalCharges` es **703,55** y **1.683,60**, respectivamente; esta diferencia debe leerse junto con la antigüedad, porque el total acumulado depende del tiempo como cliente.

| Variable | Categoría | Churn observado |
|---|---|---:|
| Contrato | `Month-to-month` | 42,71 % |
| Contrato | `One year` | 11,27 % |
| Contrato | `Two year` | 2,83 % |
| Método de pago | `Electronic check` | 45,29 % |
| Método de pago | `Bank transfer (automatic)` | 16,71 % |
| Método de pago | `Credit card (automatic)` | 15,24 % |
| Método de pago | `Mailed check` | 19,11 % |
| Internet | `Fiber optic` | 41,89 % |
| Internet | `DSL` | 18,96 % |
| Internet | `No` | 7,40 % |

Las diferencias son descriptivas: las variables pueden estar relacionadas entre sí y no se ha medido el efecto aislado de cada una. En particular, no puede concluirse que el contrato, el método de pago o el tipo de Internet causen el abandono.

## 4. Modelo predictivo

Se evaluaron ambos modelos con Accuracy, Precision, Recall, F1 y matriz de confusión. En este caso, Recall es relevante porque mide qué proporción de los clientes que abandonan detecta el modelo.

| Modelo | Accuracy | Precision | Recall | F1 | Falsos positivos | Falsos negativos |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0,801 | 0,650 | 0,540 | 0,590 | 109 | 172 |
| Decision Tree | 0,799 | 0,632 | 0,583 | 0,606 | 127 | 156 |

Se seleccionó **Decision Tree** porque mejora Recall y F1 respecto al modelo de referencia, a costa de más falsos positivos y una Accuracy ligeramente inferior. En el conjunto de prueba identificó 218 clientes con churn y dejó sin detectar 156.

Entre las variables con mayor peso en el árbol aparecen `is_monthly_contract`, `tenure` e `InternetService_Fiber optic`. Estas importancias describen cómo el modelo realiza sus predicciones; no prueban que esas variables sean causas del churn.

La evaluación es inicial: se utilizó una única división train/test, sin validación cruzada ni validación temporal independiente.

## 5. Segmentación de clientes

K-Means agrupó la cartera en cuatro perfiles. Las tasas de churn que aparecen en la tabla se calcularon después de crear los grupos y son descriptivas, no probabilidades individuales.

| Segmento | Clientes | % de la cartera | Antigüedad media | Cargo mensual medio | Churn observado |
|---|---:|---:|---:|---:|---:|
| Clientes consolidados | 1.993 | 28,30 % | 56,40 meses | 84,15 | 9,08 % |
| Clientes mensuales de alto riesgo | 2.155 | 30,60 % | 21,60 meses | 87,02 | 54,25 % |
| Clientes de bajo gasto y baja adopción | 1.526 | 21,67 % | 30,55 meses | 21,08 | 7,40 % |
| Clientes recientes con DSL | 1.369 | 19,44 % | 16,38 meses | 50,19 | 29,66 % |

El segmento de **clientes mensuales de alto riesgo** combina contratos mensuales, fibra óptica y una proporción alta de pagos con `Electronic check`. **Clientes recientes con DSL** presenta menor antigüedad y un churn observado del 29,66 %. Estos perfiles permiten formular seguimientos distintos, pero su utilidad práctica aún debe comprobarse.

## 6. Recomendaciones y medición

| Acción propuesta | A quién dirigirla | Qué comprobar | Indicadores posibles |
|---|---|---|---|
| Seguimiento preventivo | Clientes señalados por el modelo, priorizando los perfiles con mayor churn observado | Si el contacto permite detectar problemas antes de una baja | Churn posterior, contactos efectivos y rendimiento del modelo |
| Revisar contratos mensuales | Clientes `Month-to-month` | Motivos de baja y aceptación de opciones de fidelización | Aceptación y retención frente a un grupo comparable |
| Mejorar onboarding | Clientes recientes, especialmente el segmento con DSL | Dificultades iniciales, incidencias y adopción del servicio | Retención a un periodo definido e incidencias resueltas |
| Investigar pago e Internet | Clientes con `Electronic check` o `Fiber optic` | Si existen problemas de facturación, expectativas o experiencia | Incidencias, satisfacción —si se recoge— y churn posterior |
| Entender necesidades de baja adopción | Clientes de bajo gasto y sin servicios adicionales | Si hay necesidades no cubiertas antes de ofrecer servicios adicionales | Adopción, satisfacción y retención |

Para evaluar las acciones, primero habría que establecer una línea base y definir un periodo de seguimiento. Cuando sea viable, conviene comparar clientes que reciben una intervención con un grupo comparable que no la recibe. Un cambio en el churn tras una campaña no demuestra por sí solo que la campaña lo haya causado.

Ya se han calculado métricas del modelo sobre el conjunto de prueba: Recall, Precision y falsos negativos. Para una futura implantación también serían útiles el churn por periodo, la retención por cohorte, la aceptación de acciones y el coste por cliente retenido. Estos últimos requieren datos operativos que el dataset actual no contiene.

## 7. Limitaciones y siguientes pasos

- **Datos:** el origen es telecomunicaciones, no una empresa SaaS real. El 26,54 % es una proporción de la muestra y no una tasa mensual.
- **Explicación:** los resultados muestran asociaciones, no causalidad. Faltan motivos de baja, incidencias, satisfacción y resultados de campañas.
- **Modelo:** Decision Tree mantiene falsos negativos y falsos positivos; la evaluación se basa en una única división de los datos. Debe probarse con nuevas muestras antes de cualquier uso operativo.
- **Segmentación:** los grupos dependen de las variables, la codificación, la estandarización y la elección de K. Sus nombres son descripciones interpretativas.
- **Impacto:** no se han medido costes, ingresos perdidos, retorno de campañas ni cambios reales en retención.

**Conclusión:** el proyecto identifica patrones útiles para investigar y ofrece un primer modelo y una segmentación interpretable. Todavía no demuestra que pueda reducir el churn. El paso siguiente es validar los resultados y comprobar, mediante pruebas controladas, si las acciones propuestas mejoran la detección o la retención.
