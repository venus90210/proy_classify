# Project Charter - Entendimiento del Negocio

## Nombre del Proyecto

Modelo Clasificador de Transacciones

## Objetivo del Proyecto

Con este proyecto se busca desarrollar un modelo de machine learning capaz de clasificar transacciones financieras ( por ejemplo: compras o pagos) de forma automática. El objetivo es mejorar la eficiencia operativa, reducir el riesgo de fraude y/o proporcionar a los usuarios una mejor comprensión de sus patrones de gasto.

## Alcance del Proyecto

### Incluye:

- **Fuente de Datos:** Se utilizará un dataset histórico de transacciones en formato CSV,
- **Entregables del Proyecto:**
  - Un modelo de clasificación entrenado y serializado.
  - Código fuente en Python (notebooks o scripts), el preprocesamiento y el entrenamiento del modelo.
.
- **Criterios de Éxito Medibles:**
  - **Técnicos:** El modelo final debe alcanzar una métrica F1-score superior a 0.90 en el conjunto de datos de prueba. La latencia de respuesta de la API no debe superar los 200ms por predicción.
  - **De Negocio:** Lograr una automatización del 95% en la categorización de transacciones, reduciendo el tiempo de procesamiento manual, o identificar correctamente al menos el 85% de las transacciones fraudulentas (recall).



## Metodología

Se utilizará una metodología ágil e iterativa, inspirada en CRISP-DM (Cross-Industry Standard Process for Data Mining). El proyecto se dividirá en ciclos cortos (sprints). Al final de cada ciclo, se entregará un incremento funcional del modelo, permitiendo una validación y retroalimentación continua por parte de los stakeholders. Esto asegura que el producto final esté alineado con las necesidades del negocio y permite ajustar el rumbo del proyecto de manera flexible.

## Cronograma

| Iteración (Sprint) | Objetivo Principal | Entregable Clave | Duración Estimada |
|--------------------|----------------------------------------------------------------|---------------------------------------------------|-------------------|
| Sprint 0: Setup    | Definición, setup de entorno y carga de datos inicial.         | Project Charter finalizado, repositorio y entorno listos. | 1 semana          |
| Sprint 1: MVP      | Primer modelo base (baseline) con preprocesamiento simple.     | Modelo funcional con performance inicial.         | 2 semanas         |
| Sprint 2: Feature Eng. | Mejorar el modelo con ingeniería de características avanzada.    | Modelo con métricas de rendimiento mejoradas.     | 2 semanas         |
| Sprint 3: Tuning   | Optimización de hiperparámetros y evaluación de otros algoritmos. | Versión candidata a producción del modelo.        | 2 semanas         |
| Sprint 4: Despliegue | Empaquetado del modelo y despliegue en un entorno de pruebas.  | API del modelo desplegada para validación.        | 2 semanas         |

El cronograma es una estimación inicial. La naturaleza iterativa del proyecto permite ajustar las prioridades y objetivos de cada sprint según los hallazgos y la retroalimentación recibida.

## Equipo del Proyecto

- Angélica María Amaya Giraldo

## Presupuesto

N/A

## Stakeholders

- Empresas pequeñas y medianas

