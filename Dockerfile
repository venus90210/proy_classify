# 1. Imagen Base: Usa una imagen de Python ligera y oficial.
# 'slim' es una buena opción para mantener el tamaño de la imagen reducido.
FROM python:3.10-slim

# 2. Establece el directorio de trabajo dentro del contenedor.
# Todos los comandos siguientes se ejecutarán desde /app.
WORKDIR /app

# 3. Copia el archivo de dependencias y las instala.
# Copiarlo por separado aprovecha el cache de Docker, acelerando builds futuros
# si las dependencias no cambian.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia el código de tu aplicación y los modelos al contenedor.
# Copia el contenido de 'src' a '/app'
COPY ./src/ .
# Copia la carpeta 'models' a '/app/models'
COPY models /app/models


# 5. Expone el puerto en el que se ejecutará la aplicación.
EXPOSE 8080

# 6. Comando para ejecutar la aplicación con Uvicorn.
# Uvicorn buscará el objeto 'app' en el archivo 'main.py' dentro del módulo 'categorizacion'.
CMD ["uvicorn", "categorizacion.main:app", "--host", "0.0.0.0", "--port", "80"]