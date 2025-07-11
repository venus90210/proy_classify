# Diccionario de datos

## Tabla de Transacciones Consolidadas

**Descripción:** Esta tabla contiene el conjunto de datos consolidado a partir de los cinco archivos JSON de origen. Cada fila representa un registro con sus características asociadas. El objetivo es utilizar estas características para predecir la variable `CODIGO`.

| Variable | Descripción | Tipo de dato | Rango/Valores posibles | Fuente de datos |
| --- | --- | --- | --- | --- |
| `CODIGO` | **Variable Objetivo.** Código que representa la categoría a predecir. | Categórico (String) | Valores discretos que representan las clases. | Archivos JSON de origen |
| `TIPO` | Tipo de registro o transacción. | Categórico (String) | Valores discretos (ej. 'CREDITO', 'DEBITO'). | Archivos JSON de origen |
| `MENSAJE` | Texto o descripción asociado al registro. | Texto (String) | Cadena de caracteres. | Archivos JSON de origen |
| `source` | Identificador del archivo de origen del cual se extrajo el registro. | Categórico (String) | 'C026', 'C025', 'C001', 'P001', 'P047' | Script `docs/data/data.py` |

### Notas
- **Variable**: Nombre de la columna en el DataFrame de pandas.
- **Descripción**: Explicación del significado de la variable en el contexto del negocio.
- **Tipo de dato**: Tipo de dato esperado en pandas.
- **Rango/Valores posibles**: Ejemplos de los valores que puede tomar la variable.
- **Fuente de datos**: Origen de la columna.
