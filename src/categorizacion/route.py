from fastapi import FastAPI
from pydantic import BaseModel
import random

# --------------------------------------------------------------------------
# 1. Definición de los modelos de datos con Pydantic
# --------------------------------------------------------------------------
# Pydantic se encarga de la validación y serialización de datos.
# FastAPI lo usa para validar las solicitudes entrantes y formatear las respuestas.

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
# 2. Lógica del Modelo de Clasificación (Simulado)
# --------------------------------------------------------------------------
# En un caso real, aquí cargarías tu modelo (ej. desde un archivo .pkl o .h5)
# y realizarías la predicción. Para este ejemplo, simularemos la lógica.

def get_model_prediction(text: str) -> dict:
    """
    Función que simula la predicción de un modelo de machine learning.

    Args:
        text (str): El texto de entrada a clasificar.

    Returns:
        dict: Un diccionario con la clasificación y la confianza.
    """
    # Lógica de clasificación simple basada en palabras clave
    positive_keywords = ["bueno", "excelente", "genial", "increíble", "fantástico", "amo"]
    negative_keywords = ["malo", "terrible", "odio", "decepcionante", "pésimo"]

    text_lower = text.lower()
    
    # Asignar clasificación por defecto
    classification = "neutral"
    
    if any(keyword in text_lower for keyword in positive_keywords):
        classification = "positivo"
    elif any(keyword in text_lower for keyword in negative_keywords):
        classification = "negativo"

    # Simular una puntuación de confianza
    confidence = random.uniform(0.75, 0.99)

    return {
        "classification": classification,
        "confidence": confidence
    }

# --------------------------------------------------------------------------
# 3. Creación de la Aplicación FastAPI y sus Endpoints
# --------------------------------------------------------------------------

# Inicializa la aplicación FastAPI con metadatos para la documentación
app = FastAPI(
    title="API de Clasificación de Texto",
    description="Una API simple para recibir texto en formato JSON, pasarlo a un modelo y devolver una clasificación.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Bienvenido a la API de Clasificación"}


@app.post("/classify/", response_model=ClassificationOutput)
async def classify_text_endpoint(item: TextInput):
    """
    Endpoint para clasificar texto.
    
    Recibe un objeto JSON con un campo 'text', lo procesa y devuelve 
    la clasificación y una puntuación de confianza.
    """
    # 1. Llama a la función del modelo para obtener la predicción
    prediction_result = get_model_prediction(item.text)

    # 2. Construye el objeto de respuesta usando el modelo Pydantic
    # FastAPI se encargará de convertirlo a JSON.
    response = ClassificationOutput(
        original_text=item.text,
        classification=prediction_result["classification"],
        confidence=prediction_result["confidence"]
    )
    
    return response

