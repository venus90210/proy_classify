# Definición de los datos

## Origen de los datos

- Los datos se obtienen de repositorios privados y contienen un historial de transacciones financieras realizadas por usuarios.

## Especificación de los scripts para la carga de datos

Los datos se encuentran alojados en un bucket de AWS S3, distribuidos en varios archivos en formato JSON. Se ha desarrollado un script en Python, ubicado en `docs/data/data.py`, que automatiza la descarga y consolidación de estos archivos en un único DataFrame de pandas, facilitando así su posterior análisis y procesamiento.

## Especificación de los scripts para la carga de datos

- **Ubicación y Rutas:** Los datos de origen son cinco archivos en formato JSON, alojados públicamente en un bucket de AWS S3. Las URLs específicas están definidas dentro del script `docs/data/data.py` y son las siguientes:
  - `https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100005.json`
  - `https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100004.json`
  - `https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100003.json`
  - `https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100002.json`
  - `https://dataanaliticaunal.s3.us-east-2.amazonaws.com/deeplearning/100001.json`
- **Estructura y Transformación:** Cada archivo contiene registros de transacciones. El script de carga los consolida en un único DataFrame y añade una columna `source` para identificar el origen de cada registro.

### Archivos y Base de datos de destino

- **Base de Datos de Destino:** El alcance actual del proyecto, centrado en la creación de un modelo de machine learning, no contempla la carga de los datos a una base de datos de destino. El entregable principal es el modelo entrenado.


