# Reporte del Modelo Final

## Resumen Ejecutivo

El modelo final, basado en una arquitectura Transformer, ha demostrado un rendimiento general robusto, alcanzando una precisión (accuracy) del **90.9%** en el conjunto de prueba. Este resultado indica una alta capacidad para clasificar correctamente los movimientos contables en las categorías definidas.

El análisis detallado de las métricas revela las fortalezas y debilidades del modelo:
- **Rendimiento Excepcional:** Para las clases **2, 3 y 4**, el modelo logró una precisión y recall perfectos (1.0), lo que significa que identifica estas categorías sin errores.
- **Fortalezas y Debilidades:**
  - Para la **clase 1**, el modelo presenta un recall muy alto (98.8%), identificando casi todos los casos positivos, aunque a costa de una precisión menor (69.1%), lo que indica una tendencia a generar falsos positivos.
  - La principal área de mejora se encuentra en la **clase 0**, que, a pesar de tener una alta precisión (97.9%), muestra un recall bajo (55.8%). Esto significa que, si bien las predicciones para esta clase son muy confiables, el modelo no logra identificar un número significativo de casos reales, generando falsos negativos.

En conclusión, el modelo es altamente efectivo para la mayoría de las clases y establece una base sólida. Las futuras mejoras deberían centrarse en aumentar la capacidad de detección (recall) de la clase 0, manteniendo al mismo tiempo la alta precisión lograda.


## Descripción del Problema

El manejo de transacciones contables en empresas medianas y grandes es un proceso fundamental que tradicionalmente se ha realizado de forma manual. Este enfoque es ineficiente, consume una cantidad considerable de tiempo y es altamente propenso a errores humanos. Una clasificación incorrecta de un movimiento bancario puede llevar a inconsistencias en los libros contables, informes financieros imprecisos y, en última instancia, a una toma de decisiones de negocio deficiente.

**Contexto:** En el marco de la transformación digital que está revolucionando el sector financiero y contable, surge la necesidad de automatizar y optimizar estos procesos críticos. Este proyecto se enfoca en la clasificación de movimientos bancarios, donde cada transacción, descrita en un objeto JSON (`MENSAJE`), debe ser asignada a una cuenta contable específica, representada por un `CODIGO`.

**Objetivos:** El objetivo principal de este proyecto es desarrollar un modelo de Deep Learning capaz de automatizar la clasificación de transacciones contables. Se busca:
- **Minimizar errores:** Reducir la tasa de error humano en la categorización de movimientos.
- **Optimizar la eficiencia:** Acelerar el proceso de contabilidad, permitiendo un manejo más ágil de un gran volumen de datos.
- **Mejorar la toma de decisiones:** Proporcionar datos financieros más precisos y confiables para la gerencia.

**Justificación del Modelo:** Se seleccionó un modelo basado en la arquitectura **Transformer** debido a su probada eficacia en el procesamiento de secuencias y la comprensión del lenguaje natural. Dado que los datos de entrada son objetos JSON con información textual y contextual, la capacidad del Transformer para ponderar la importancia de diferentes partes del mensaje a través de mecanismos de atención lo convierte en el candidato ideal para interpretar los detalles de cada transacción y asignarla al `CODIGO` contable correcto con alta precisión.

## Descripción del Modelo

El modelo final es una red neuronal profunda basada en la arquitectura **Transformer**, diseñada específicamente para la clasificación de texto. Esta arquitectura fue seleccionada por su capacidad superior para capturar relaciones contextuales complejas en datos secuenciales.

### Arquitectura del Modelo

El modelo se compone de las siguientes capas principales:
1.  **Capa de Entrada y Embedding:**
    -   Recibe secuencias de texto tokenizadas y normalizadas a una longitud fija (`maxlen=125`).
    -   Utiliza una capa personalizada `TokenAndPositionEmbedding` que combina dos tipos de embeddings:
        -   **Token Embeddings:** Convierte cada token (palabra) en un vector denso de una dimensión (`embed_dim`) definida.
        -   **Positional Embeddings:** Añade información sobre la posición de cada token en la secuencia, lo cual es crucial para que el modelo entienda el orden de las palabras.
2.  **Bloques Transformer:**
    -   El núcleo del modelo está formado por dos `TransformerBlock` apilados. Cada bloque contiene:
        -   Una capa de **Atención Multi-Cabeza (Multi-Head Attention)**, que permite al modelo ponderar la importancia de diferentes palabras al procesar una palabra específica.
        -   Una **Red Neuronal Feed-Forward** para un procesamiento adicional.
        -   Capas de **Normalización (LayerNormalization)** y **Dropout** para estabilizar el entrenamiento y prevenir el sobreajuste.
3.  **Cabezal de Clasificación:**
    -   La salida del primer token de la secuencia (token `[CLS]`) se extrae y se utiliza como una representación agregada de toda la secuencia.
    -   Esta representación pasa a través de dos capas `Dense` con activación ReLU y capas de `Dropout` intermedias para una clasificación final.
    -   La capa de salida es una capa `Dense` con una función de activación **softmax**, que produce una distribución de probabilidad sobre las 5 clases de cuentas contables.

### Metodología y Técnicas

-   **Preprocesamiento y Tokenización:** Los datos de entrada en formato JSON se limpiaron y tokenizaron, convirtiendo cada mensaje en una secuencia de enteros. Las secuencias se rellenaron (padding) para asegurar una longitud uniforme.
-   **Optimización de Hiperparámetros:** Se utilizó **KerasTuner** con una estrategia de `RandomSearch` para encontrar la combinación óptima de hiperparámetros, incluyendo la dimensión del embedding, el número de cabezas de atención, la tasa de dropout, la tasa de aprendizaje y la fuerza de la regularización.
-   **Entrenamiento y Regularización:** El modelo se entrenó utilizando el optimizador `Adam` y la función de pérdida `categorical_crossentropy`. Para combatir el sobreajuste, se implementaron técnicas de regularización como:
    -   **Dropout:** Se aplicaron varias capas de Dropout en diferentes puntos de la red.
    -   **Regularización L1/L2:** Se añadió a las capas densas para penalizar pesos grandes y promover un modelo más simple.
    -   **Callbacks:** Se usó `EarlyStopping` para detener el entrenamiento si la pérdida de validación no mejoraba, y `ReduceLROnPlateau` para ajustar dinámicamente la tasa de aprendizaje.

## Evaluación del Modelo

El modelo final, basado en una arquitectura Transformer, ha demostrado un rendimiento general robusto, alcanzando una precisión (accuracy) del **90.9%** en el conjunto de prueba. Este resultado indica una alta capacidad para clasificar correctamente los movimientos contables en las categorías definidas.

El análisis detallado de las métricas revela las fortalezas y debilidades del modelo:
- **Rendimiento Excepcional:** Para las clases **2, 3 y 4**, el modelo logró una precisión y recall perfectos (1.0), lo que significa que identifica estas categorías sin errores.
- **Fortalezas y Debilidades:**
  - Para la **clase 1**, el modelo presenta un recall muy alto (98.8%), identificando casi todos los casos positivos, aunque a costa de una precisión menor (69.1%), lo que indica una tendencia a generar falsos positivos.
  - La principal área de mejora se encuentra en la **clase 0**, que, a pesar de tener una alta precisión (97.9%), muestra un recall bajo (55.8%). Esto significa que, si bien las predicciones para esta clase son muy confiables, el modelo no logra identificar un número significativo de casos reales, generando falsos negativos.

En conclusión, el modelo es altamente efectivo para la mayoría de las clases y establece una base sólida. Las futuras mejoras deberían centrarse en aumentar la capacidad de detección (recall) de la clase 0, manteniendo al mismo tiempo la alta precisión lograda.

## Conclusiones y Recomendaciones

A partir de los resultados obtenidos con el modelo Transformer, se concluye lo siguiente:

**Puntos Fuertes:**
- El modelo presenta un alto rendimiento general, evidenciado por una precisión del 90.9%.
- Destaca en la clasificación de las clases 2, 3 y 4, con precisión y recall perfectos, lo que indica una identificación muy fiable de estos tipos de movimientos.
- El modelo ha demostrado ser viable y efectivo en la automatización de la clasificación de transacciones contables, cumpliendo con los objetivos iniciales del proyecto.

**Puntos Débiles y Limitaciones:**
- Existe una debilidad en la clasificación de la clase 0, con un recall relativamente bajo, lo que implica que el modelo tiene dificultades para identificar todos los movimientos bancarios que pertenecen a esta clase, generando falsos negativos.
- La precisión para la clase 1 es menor en comparación con el recall, lo que sugiere una tendencia a generar falsos positivos.

**Recomendaciones:**
- Se recomienda enfocar los esfuerzos futuros en mejorar la identificación de movimientos bancarios de la clase 0 (aumentar el recall), sin comprometer la alta precisión ya lograda en esta y otras clases.  
- Se sugiere investigar por qué el modelo distingue tan bien las clases 2, 3 y 4, para aplicar esos aprendizajes a la clase 0.
- Explorar técnicas de aumento de datos o ajuste de pesos para mitigar el desbalance de clases y mejorar el rendimiento general del modelo.

## Referencias

En esta sección se deben incluir las referencias bibliográficas y fuentes de información utilizadas en el desarrollo del modelo.
