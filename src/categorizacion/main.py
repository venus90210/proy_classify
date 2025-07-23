import logging
import os

import numpy as np
import joblib
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras import layers
from tensorflow.keras.utils import custom_object_scope

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

  

# --------------------------------------------------------------------------
# 1. Definición de los modelos de datos con Pydantic
# --------------------------------------------------------------------------

class TextInput(BaseModel):
    """
    Define la estructura del JSON que esperamos en la solicitud (request).
    Debe tener una clave "text" con un valor de tipo string.
    """
    text: str

class ClassificationOutput(BaseModel):
    """
    Define la estructura del JSON que nuestra API devolverá (response).
    """
    original_text: str
    classification: str
    confidence: float

# --------------------------------------------------------------------------
# 2. Definición de la Capa Personalizada de Keras
# --------------------------------------------------------------------------
# Para que `joblib.load()` (o cualquier método de carga de Keras) pueda
# reconstruir el modelo, necesita la definición de cualquier clase personalizada
# que se haya utilizado, como 'TokenAndPositionEmbedding'.
# El decorador `@keras.saving.register_keras_serializable()` es crucial.

@tf.keras.utils.register_keras_serializable()
class TokenAndPositionEmbedding(layers.Layer):
    """
    Capa de embedding que combina embeddings de tokens y de posición.
    Esta clase es necesaria para que Keras pueda cargar el modelo correctamente.
    """
    def __init__(self, maxlen, vocab_size, embed_dim, **kwargs):
        super().__init__(**kwargs)
        self.maxlen = maxlen
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        # Capa de embedding para los tokens
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        # Capa de embedding para las posiciones
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions

    def get_config(self):
        # Permite que Keras guarde la configuración de la capa para recrearla
        config = super().get_config()
        config.update({
            "maxlen": self.maxlen,
            "vocab_size": self.vocab_size,
            "embed_dim": self.embed_dim,
        })
        return config

@tf.keras.utils.register_keras_serializable()
class TransformerBlock(layers.Layer):
    """
    Capa de Transformer que combina Multi-Head Attention y una red Feed-Forward.
    Esta clase es necesaria para que Keras pueda cargar el modelo correctamente.
    """
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.rate = rate
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential(
            [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training=False):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "rate": self.rate,
        })
        return config

# --------------------------------------------------------------------------
# 3. Carga del Modelo de Clasificación
# --------------------------------------------------------------------------
# Cargamos el modelo una sola vez cuando se inicia la aplicación para
# mayor eficiencia.
# Asegúrate de que el archivo 'model.joblib' se encuentre en la carpeta 'models'.

# El error 'TypeError: 'Functional' object is not subscriptable' indica que
# 'model.joblib' contiene solo el objeto del modelo, no un diccionario.
# Por lo tanto, cargamos cada componente desde su propio archivo.
MODELS_DIR = "models"
MODEL_PATH = os.path.join(MODELS_DIR, "model.joblib")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.joblib")
CLASS_NAMES_PATH = os.path.join(MODELS_DIR, "class_names.joblib")

# Al cargar un modelo que contiene objetos personalizados (como capas),
# es más robusto usar un 'custom_object_scope' para asegurar que Keras
# sepa cómo deserializarlos, especialmente cuando se usa con joblib.
with custom_object_scope({
    'TokenAndPositionEmbedding': TokenAndPositionEmbedding,
    'TransformerBlock': TransformerBlock
}):
    # Cargar el modelo Keras.
    logging.info(f"Cargando modelo desde: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

# Cargar los otros componentes por separado.
# Asegúrate de que estos archivos existan en la carpeta 'models'.
logging.info(f"Cargando vectorizador desde: {VECTORIZER_PATH}")
vectorizer = joblib.load(VECTORIZER_PATH)
logging.info(f"Cargando nombres de clases desde: {CLASS_NAMES_PATH}")
class_names = joblib.load(CLASS_NAMES_PATH)

# 'maxlen' se puede inferir de la forma de entrada del modelo.
# La forma de entrada es (batch_size, maxlen), por lo que tomamos el segundo elemento.
maxlen = model.input_shape[1]

logging.info("Modelo y componentes cargados correctamente.")

def get_model_prediction(text: str) -> dict:
    """
    Utiliza el modelo Keras cargado para predecir la clasificación del texto.
    Realiza los pasos de preprocesamiento necesarios: tokenización y padding.

    Args:
        text (str): El texto de entrada a clasificar.

    Returns:
        dict: Un diccionario con la clasificación y la confianza.
    """
    logging.info(f"Procesando texto para predicción: '{text}'")

    # 1. Vectorizar el texto de entrada usando el Tokenizer.
    # El Tokenizer convierte el texto en una secuencia de enteros.
    vectorized_text = vectorizer.texts_to_sequences([text])
    logging.info(f"Secuencia vectorizada (antes del padding): {vectorized_text}")

    # 2. Aplicar padding para que la secuencia tenga la longitud `maxlen`.
    padded_text = pad_sequences(vectorized_text, maxlen=maxlen, padding='post')
    logging.info(f"Secuencia con padding (lista para el modelo): {padded_text}")

    # 3. Realizar la predicción con el modelo Keras
    predictions = model.predict(padded_text)
    probabilities = predictions[0] # Obtenemos las probabilidades para la única entrada
    logging.info(f"Probabilidades predichas: {probabilities}")

    # 4. Obtener la clase y la confianza
    predicted_index = np.argmax(probabilities)
    confidence = float(probabilities[predicted_index])
    predicted_class_label = class_names[predicted_index]

    return {
        "classification": str(predicted_class_label),
        "confidence": confidence
    }

# --------------------------------------------------------------------------
# 4. Creación de la Aplicación FastAPI y sus Endpoints
# --------------------------------------------------------------------------

# Inicializa la aplicación FastAPI con metadatos para la documentación
app = FastAPI(
    title="API de Clasificación de Texto con Modelo",
    description="Una API que usa un modelo de ML (cargado con Joblib) para clasificar texto.",
    version="1.1.0",
)

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Bienvenido a la API de Clasificación con Modelo"}

@app.post("/classify/", response_model=ClassificationOutput)
async def classify_text_endpoint(item: TextInput):
    """
    Endpoint para clasificar texto.
    
    Recibe un objeto JSON con un campo 'text', lo procesa y devuelve 
    la clasificación y una puntuación de confianza.
    """
    logging.info(f"Recibido texto para clasificar: '{item.text}'")
    
    # Simplemente llama a la función que ya tiene la lógica correcta
    prediction_result = get_model_prediction(item.text)

    response = ClassificationOutput(
        original_text=item.text,
        classification=prediction_result["classification"],
        confidence=prediction_result["confidence"]
    )

    logging.info(f"Respuesta enviada: {response.model_dump_json()}")
    
    return response
 