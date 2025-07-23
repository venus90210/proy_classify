# Despliegue de modelos

## Infraestructura
 
- **Nombre del modelo:** Clasificador de Transacciones
- **Plataforma de despliegue:** Google Cloud Platform (GCP) - AI Platform / Cloud Run
- **Requisitos técnicos:** 
    - Python 3.9 o superior.
    - Bibliotecas: scikit-learn, pandas, numpy, Flask/FastAPI (para el endpoint de API).
    - Hardware: Instancia de cómputo estándar (ej. n1-standard-2 en GCP) con al menos 2 vCPU y 4 GB de RAM.
- **Requisitos de seguridad:** 
    - Autenticación mediante claves de API o tokens OAuth 2.0 para el acceso al endpoint.
    - Uso de roles y permisos de IAM (Identity and Access Management) para restringir el acceso a los recursos de la nube.
    - Gestión de secretos (secrets management) para credenciales y claves de API.
- **Diagrama de arquitectura:** (Se recomienda incluir un diagrama que muestre el flujo de datos, por ejemplo: Usuario -> API Gateway -> Cloud Function/Cloud Run (con el modelo) -> Base de datos/Almacenamiento)

## Código de despliegue

- **Archivo principal:** `app.py` (Contiene la API de Flask/FastAPI para servir el modelo).
- **Rutas de acceso a los archivos:**
    - `app.py`: El script de la aplicación web.
    - `models/clasificador_proyectos.joblib`: El modelo entrenado y serializado.
    - `requirements.txt`: Lista de dependencias de Python.
    - `Dockerfile`: Archivo para construir la imagen del contenedor para Cloud Run.
- **Variables de entorno:**
    - `MODEL_PATH`: Ruta al archivo del modelo (ej. `models/model.joblib`).
    - `PORT`: Puerto en el que se ejecutará la aplicación (usualmente gestionado por Cloud Run, por defecto 8080).

## Documentación del despliegue

- **Instrucciones de instalación:**
    1.  **Prerrequisitos:**
        - Instalar y configurar [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
        - Instalar [Docker](https://docs.docker.com/get-docker/).
    2.  **Autenticación:**
        - Autenticarse con gcloud: `gcloud auth login`
        - Configurar el proyecto: `gcloud config set project [PROJECT_ID]`
    3.  **Construir y Subir la Imagen del Contenedor:**
        - Habilitar el servicio de Artifact Registry: `gcloud services enable artifactregistry.googleapis.com`
        - Crear un repositorio (si no existe): `gcloud artifacts repositories create [REPO_NAME] --repository-format=docker --location=[REGION]`
        - Construir la imagen de Docker: `docker build -t [REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/clasificador-proyectos:v1 .`
        - Autenticar Docker con gcloud: `gcloud auth configure-docker [REGION]-docker.pkg.dev`
        - Subir la imagen al repositorio: `docker push [REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/clasificador-proyectos:v1`
    4.  **Desplegar en Cloud Run:**
        - Ejecutar el comando de despliegue. Para permitir el acceso público, se usa `--allow-unauthenticated`.
          ```bash
          gcloud run deploy clasificador-proyectos \
            --image [REGION]-docker.pkg.dev/[PROJECT_ID]/[REPO_NAME]/clasificador-proyectos:v1 \
            --platform managed \
            --region [REGION] \
            --allow-unauthenticated
          ```

- **Instrucciones de configuración:**
    - Las variables de entorno se pueden configurar durante el despliegue usando el flag `--set-env-vars`.
    - Ejemplo: `--set-env-vars MODEL_PATH="models/clasificador_proyectos.joblib"`
    - Se pueden ajustar los recursos de la instancia (CPU, memoria) con los flags `--cpu` y `--memory`.

- **Instrucciones de uso:**
    - Una vez desplegado, el servicio tendrá una URL de endpoint.
    - Para realizar una predicción, se debe enviar una petición POST a la ruta `/predict` con un cuerpo JSON que contenga los datos del proyecto.
    - Ejemplo usando `curl`:
      ```bash
      curl -X POST [URL_DEL_SERVICIO]/predict \
      -H "Content-Type: application/json" \
      -d '{"titulo": "Nuevo proyecto de IA", "descripcion": "Desarrollo de un sistema de recomendación."}'
      ```

- **Instrucciones de mantenimiento:**
    - **Actualización del modelo:** Para desplegar una nueva versión del modelo, se debe reemplazar el archivo `.joblib`, construir una nueva imagen de Docker con una nueva etiqueta (ej. `v2`), subirla y volver a desplegar el servicio. Cloud Run gestionará el tráfico hacia la nueva revisión automáticamente.
    - **Monitoreo y Logs:** Utilizar la suite de operaciones de Google Cloud (Logging y Monitoring) para visualizar los logs de la aplicación, monitorear métricas como la latencia, el número de peticiones y configurar alertas.
    - **Escalado:** Cloud Run escala automáticamente el número de instancias según el tráfico de entrada. Los límites de escalado (mínimo y máximo de instancias) se pueden configurar en los ajustes del servicio.
