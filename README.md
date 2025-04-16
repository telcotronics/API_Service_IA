# API DE SERVICIOS con Inteligencia Artificial

## AUDIO A TEXTO IA 
uso: el antiguo audio_aTexto_whisperAPI

### Para instalr WHISPER
```bash
pip install -U openai-whisper
```
Setup
WUsamos Python 3.9.9 y PyTorch 1.10.1 para entrenar y probar nuestros modelos, pero se espera que el código base sea compatible con Python 3.8-3.11 y versiones recientes de PyTorch. El código base también depende de algunos paquetes de Python, en particular de tiktoken de OpenAI para la rápida implementación del tokenizador. Puedes descargar e instalar (o actualizar) la última versión de Whisper con el siguiente comando:

pip install -U openai-whisper
Alternativamente, el siguiente comando extraerá e instalará la última confirmación de este repositorio, junto con sus dependencias de Python:

pip install git+https://github.com/openai/whisper.git
Para actualizar el paquete a la última versión de este repositorio, ejecuta:

pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
También requiere que la herramienta de línea de comandos ffmpeg esté instalada en tu sistema, disponible en la mayoría de los gestores de paquetes.

### on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

### on Arch Linux
sudo pacman -S ffmpeg

### on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

### on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

### on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
Es posible que también necesites instalar Rust, en caso de que TikTok no proporcione una rueda precompilada para tu plataforma. Si ves errores de instalación durante el comando pip install mencionado anteriormente, sigue la página de inicio para instalar el entorno de desarrollo de Rust. Además, puede que necesites configurar la variable de entorno PATH, por ejemplo, export PATH="$HOME/.cargo/bin:$PATH". Si la instalación falla y no aparece el módulo "setuptools_rust", debes instalarlo, por ejemplo, ejecutando:
pip install setuptools-rust
Available models and languages

## OBJETIVO IMPORTATNTES
instalar python
```bash
sudo apt install python3
```
instalar pip
```bash
sudo apt install pip
sudo apt install python3-pip
```

Para actualizar pip
```bash
pip install --upgrade pip
```
instalamos venv
```bash
sudo apt install python3-venv
```
Para crear el entorno virtual de python
```bash
python3 -m venv api_env
```
Para activar el entorno virtual env de python
```bash
source api_env/bin/activate
```
Instalar requerimientos
```bash
pip install -r requirements.txt
```
instalar tmux
```bash
sudo apt install tmux -y
```

## Remover Fondos de imagenes
Para remover fondos de imagens
Instala 
```bash
pip install rembg
```
Instala onnxruntime
```bash
pip install onnxruntime
```
Si planeas usar GPU para acelerar el procesamiento (si tienes una tarjeta gráfica compatible), podrías instalar la versión para GPU:
```bash
pip install onnxruntime-gpu
```

## pasar imagen a texto(OCR)
### Instalar Tesseract OCR en Ubuntu

```bash
sudo apt install tesseract-ocr
```
```bash
sudo apt install tesseract-ocr-spa  # Para español
```

## conversor de pdf a (txt,word,excel)
necesitas instalar las siguientes librerias
```bash
pip install PyMuPDF python-docx pandas tabula-py camelot-py opencv-python Pillow
```


instalar la libreria pytesseract
```bash
pip install pytesseract pillow opencv-python
```

# Instalar paquetes Python
pip install gradio pytesseract pillow opencv-python
## Para usar con fast api

instalamos fast api
```bash
pip install "fastapi[standard]"
```
corrremos fast api
Modo Desarrollo
```bash
fastapi dev api.py #develop
```
Modo produccion
```bash
fastapi run api.py #produccion
```

modo test que verifica codigo sin deterner el servidor
```bash
pip install uvicorn
```
iniciar uvcorn
```bash
uvicorn api:app
```
api la hoja clase o la instacia preincipal de python
```bash
uvicorn api:app --host 192.168.10.3 --port 8000
```# API_Service_IA
