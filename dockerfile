# Usa una imagen base con Python 3.10
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias al contenedor
COPY requirements.txt .

# Instala las dependencias desde el archivo
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo tu código al contenedor
COPY . .

# Expone el puerto 80 para que sea accesible desde fuera del contenedor
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]