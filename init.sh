#!/bin/bash

# Define el directorio del entorno virtual
VENV_DIR="venv"

echo "Iniciando servicio WHISPER API..."

# 1. Verificar y crear el entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv "$VENV_DIR"
fi

# 2. Activar el entorno virtual
source "$VENV_DIR/bin/activate"

# 3. Instalar dependencias si no están instaladas
# Se usa 'pip list -o' para verificar si hay dependencias pendientes de instalar.
echo "Instalando dependencias (si es necesario)..."
pip list -o > /dev/null || pip install -r requirements.txt

# 4. Iniciar la API
echo "Iniciando la API..."
fastapi run api.py

# El script se mantendrá en ejecución mientras la API esté activa.