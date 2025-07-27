# Informe de salida

## Resumen Ejecutivo

Este informe detalla la finalización exitosa del proyecto de despliegue para el servicio de clasificación de transacciones. El objetivo principal fue diseñar e implementar una arquitectura escalable, resiliente y costo-efectiva en AWS para servir un modelo de Machine Learning.

El logro clave es una infraestructura serverless completamente funcional basada en **AWS ECS con Fargate**, que expone el modelo de clasificación a través de una API segura y con balanceo de carga. Esta solución elimina la necesidad de gestionar servidores, permitiendo que el sistema escale automáticamente según la demanda y garantizando alta disponibilidad.

## Resultados del proyecto

- **Entregables y logros alcanzados:**
  - **API de Clasificación Containerizada:** Se desarrolló una API en Python (usando Flask/FastAPI) que encapsula la lógica de predicción. La API, junto con el modelo, el vectorizador y los nombres de las clases (archivos `.joblib`), fue empaquetada en una imagen Docker ligera y eficiente.
  - **Infraestructura como Código (Diagrama):** Se creó un diagrama de arquitectura detallado (`architecture.puml`) que sirve como documentación y plano para la infraestructura en AWS.
  - **Arquitectura Serverless y Escalable:** Se implementó una solución en AWS ECS utilizando el modo de lanzamiento Fargate, lo que permite ejecutar contenedores sin gestionar la infraestructura subyacente.
  - **Alta Disponibilidad y Balanceo de Carga:** La integración con un Application Load Balancer (ALB) distribuye el tráfico de manera eficiente entre las tareas de ECS, asegurando que el servicio sea resiliente y pueda manejar picos de demanda.
  - **Configuración de Red Segura:** El servicio opera dentro de una VPC personalizada con grupos de seguridad específicos para el ALB y las tareas de ECS, garantizando que solo el tráfico autorizado pueda acceder a la aplicación.

- **Evaluación del modelo final:** El modelo de clasificación, compuesto por un vectorizador de texto y un clasificador, fue empaquetado exitosamente. La arquitectura de despliegue se validó como una plataforma robusta capaz de servir este modelo de manera eficiente. Las métricas de rendimiento del modelo (precisión, F1-score) deben ser evaluadas en una fase posterior de monitoreo continuo.

- **Relevancia para el negocio:** El servicio automatiza la categorización de transacciones financieras. Esto reduce drásticamente el tiempo de procesamiento manual, minimiza errores y habilita la generación de análisis y reportes financieros en tiempo real, aportando un valor estratégico directo.

## Lecciones aprendidas

- **Principales desafíos y obstáculos:**
  - **Configuración de Red:** Asegurar la correcta comunicación entre el ALB y las tareas de Fargate a través de los grupos de seguridad y las subredes de la VPC requirió una configuración meticulosa.
  - **Empaquetado de Dependencias:** La creación de una imagen Docker optimizada que incluyera todas las dependencias del modelo (`scikit-learn`, `pandas`, etc.) y los artefactos `.joblib` fue un paso crítico para asegurar un despliegue rápido y consistente.
  - **Visualización de la Arquitectura:** La sintaxis inicial de PlantUML presentó errores que necesitaron ser depurados para generar una visualización correcta y clara de la infraestructura.

- **Lecciones aprendidas:**
  - **Modelamiento:** La modularización del pipeline de inferencia (separando vectorizador, modelo y mapeo de clases) es una práctica recomendada que facilita las actualizaciones y el mantenimiento del modelo.
  - **Implementación:** ECS Fargate es una excelente opción para despliegues de microservicios y modelos de ML, ya que abstrae la complejidad de la gestión de servidores y simplifica el autoescalado.
  - **Documentación:** Mantener un diagrama de arquitectura actualizado (como el archivo `.puml`) es invaluable para la comprensión del sistema por parte de todo el equipo y para futuras iteraciones.

- **Recomendaciones para futuros proyectos:**
  - **Implementar un pipeline de CI/CD:** Automatizar la construcción de la imagen de Docker y el despliegue en ECS (usando herramientas como AWS CodePipeline o GitHub Actions) para agilizar la entrega de nuevas versiones.
  - **Establecer Monitoreo y Alertas:** Configurar Amazon CloudWatch para monitorear métricas clave de la API (latencia, tasa de errores, uso de CPU/memoria de las tareas) y crear alarmas para notificar sobre posibles problemas.
  - **Centralizar la Gestión de Modelos:** Considerar el uso de un registro de modelos como MLflow o Amazon SageMaker Model Registry para versionar y gestionar los artefactos del modelo de forma más robusta.

## Impacto del proyecto

- **Impacto en el negocio:** Este proyecto establece una plataforma tecnológica sólida para la inteligencia de negocio. Permite a la empresa escalar sus operaciones de análisis de datos y abre la puerta a la creación de nuevos productos o servicios basados en la categorización automática de datos.

- **Áreas de mejora y oportunidades futuras:**
  - **Pipeline de Reentrenamiento:** Crear un flujo de trabajo automatizado para reentrenar el modelo periódicamente con nuevos datos y desplegar la mejor versión sin tiempo de inactividad.
  - **A/B Testing de Modelos:** Extender la arquitectura para permitir despliegues tipo "canary" o "blue/green", facilitando la prueba de nuevos modelos con un subconjunto del tráfico antes de un lanzamiento completo.
  - **Base de Datos de Predicciones:** Integrar una base de datos (como Amazon RDS o DynamoDB) para almacenar las transacciones y sus predicciones, permitiendo análisis históricos y auditorías.

## Conclusiones

- **Resumen de logros:** El proyecto cumplió con su objetivo de desplegar un servicio de Machine Learning de manera exitosa, utilizando las mejores prácticas de arquitecturas nativas de la nube. La solución es segura, escalable y de fácil mantenimiento.
- **Conclusiones finales:** La arquitectura basada en contenedores y orquestación serverless (ECS Fargate) se valida como un patrón de diseño moderno y eficaz para la puesta en producción de modelos de ML. El proyecto está en una posición ideal para ser extendido con automatización y capacidades de MLOps.

## Agradecimientos

- Agradecimientos a todo el equipo de desarrollo por su compromiso y excelencia técnica.
- Agradecimientos especiales a los stakeholders y patrocinadores del proyecto por su confianza y apoyo continuo.
