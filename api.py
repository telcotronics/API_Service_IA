from http.client import HTTPException
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, Security, status, File, UploadFile, Form
from fastapi.security.api_key import APIKeyHeader, APIKey

import tempfile
import os

from pyxnat.core.errors import catch_error
#para usar en el removedor de fondos
from rembg import remove
from PIL import Image
import io

#imagen a texto
import pytesseract
import cv2
import numpy as np

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, FileResponse

from Class_audio_aTexto import Audio_aTexto
from Class_consulta_apikey import ApiKeyManager
from Class_ocr import OCRProcessor

#from dotenv import dotenv_values
#config = dotenv_values(".env")
#model = whisper.load_model("small")

# Configuración de la base de datos
DB_CONFIG = {
    "host": "192.168.10.150",
    "user": "admin",
    "password": "Dx.1706%",
    "database": "webControl",
    "auth_plugin":"mysql_native_password"
}
# Creamos una instancia del gestor de API keys
api_key_manager = ApiKeyManager(DB_CONFIG)
# Definimos el esquema de seguridad para las API keys
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Definimos nuestra aplicación FastAPI
app = FastAPI(title="API de IA", description="API para extraer DATOS de imágenes,audio,PDFs")

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para verificar la API key
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no proporcionada"
        )
    # Verificamos la API key usando nuestro gestor
    api_key_info = api_key_manager.verify_api_key(api_key_header)
    if not api_key_info:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida o expirada"
        )
    return api_key_info

# Verificación adicional para endpoints de administración
async def get_admin_api_key(api_key_info: dict = Depends(get_api_key)):
    if not api_key_info.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador"
        )
    return api_key_info



@app.get("/items/", tags=["Items"])
async def read_items(api_key_info: dict = Depends(get_api_key)):
    return {
        "message": "Has accedido correctamente a un endpoint protegido",
        "user_id": api_key_info.get("user_id"),
        "key_name": api_key_info.get("key_name")
    }


@app.post("/audio_aTexto", tags=["Convertir Audio a texto"])
async def prueba(upload_file: UploadFile = File, api_key_info: dict = Depends(get_api_key)):
    # return {"resp": audio_a_text(upload_file.read())}
    return {"resp": Audio_aTexto(upload_file.read())}

@app.post("/convertir_audio_aTexto/", tags=["Convertir Audio a texto"])
async def create_upload_file(upload_file: UploadFile = File(...), api_key_info: dict = Depends(get_api_key)):
    res = await upload_file.read()
    if not res:
        return {"message": "No upload file sent"}
    # Guardar el archivo en un temporal para Whisper
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(res)
        temp_audio_path = temp_audio.name
    try:
        # response = audio_a_text(temp_audio_path)
        transcriptor = Audio_aTexto(modelo="small")
        response = transcriptor.audio_aText_convert(temp_audio_path)
    finally:
        os.remove(temp_audio_path)  # Limpiar archivo temporal
    return {"filename": upload_file.filename, "size": len(res), "respuesta": response}

@app.post("/removerFondo_img/", tags=["Remover Fondo de una Imagen"])
async def quitar_fondo(file: UploadFile = File(...), api_key_info: dict = Depends(get_api_key)):
    try:
        # Leer el archivo de imagen
        input_image = await file.read()
        # Usar rembg para eliminar el fondo
        output_image = remove(input_image)
        # Convertir a imagen PIL
        image = Image.open(io.BytesIO(output_image)).convert("RGBA")
        # Guardar imagen en memoria
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        return StreamingResponse(img_bytes, media_type="image/png")
    except Exception as e:
        return  {"Error": "error al procesar imagen", "respuesta": "Formato desconocido"}

@app.post("/convertir_img_aTexto/", response_class=JSONResponse, tags=["Convertir Imagen a texto"])
async def convertir_img_a_texto(file: UploadFile = File(...), api_key_info: dict = Depends(get_api_key)):
    # Obtener contenido del archivo y convertirlo a un array de numpy
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Crear instancia del OCRProcessor
    ocr = OCRProcessor(idioma='spa')

    # Procesar la imagen para extraer texto
    texto = ocr.extraer_texto(img, nivel_preprocesamiento=3)

    # Devolver el resultado como JSON
    return {
        "success": True,
        "texto": texto,
        "nombre_archivo": file.filename
    }

@app.post("/ocr/", response_class=JSONResponse, tags=["Convertir Imagen a texto"])
async def realizar_ocr(
        imagen: UploadFile = File(...),
        idioma: str = Form("spa"),
        nivel_preprocesamiento: int = Form(1)
        , api_key_info: dict = Depends(get_api_key)
):
    """
    Extrae texto de una imagen usando OCR
    - **imagen**: archivo de imagen
    - **idioma**: código de idioma (spa, eng, fra, etc.)
    - **nivel_preprocesamiento**: nivel de preprocesamiento (0-3)
    """
    try:
        # Validar nivel de preprocesamiento
        if nivel_preprocesamiento not in [0, 1, 2, 3]:
            raise HTTPException(status_code=400, detail="Nivel de preprocesamiento debe ser 0, 1, 2 o 3")

        # Validar idioma
        idiomas_validos = ["spa", "eng", "fra", "deu", "por", "ita"]
        if idioma not in idiomas_validos:
            raise HTTPException(
                status_code=400,
                detail=f"Idioma no soportado. Use uno de: {', '.join(idiomas_validos)}"
            )

        # Leer la imagen
        contenido = await imagen.read()
        img = Image.open(io.BytesIO(contenido))

        # Convertir a formato numpy para OpenCV
        img_array = np.array(img)

        # Preprocesar la imagen
        img_procesada = preprocesar_imagen(img_array, nivel_preprocesamiento)

        # Convertir de nuevo a formato PIL para pytesseract
        img_pil = Image.fromarray(img_procesada)

        # Realizar OCR
        texto = pytesseract.image_to_string(img_pil, lang=idioma)

        # Devolver resultado
        return {
            "estado": "éxito",
            "texto_extraido": texto,
            "idioma": idioma,
            "preprocesamiento": nivel_preprocesamiento
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el procesamiento: {str(e)}")

def preprocesar_imagen(img_array, nivel_preprocesamiento=1):
    """
    Preprocesa la imagen para mejorar el OCR
    nivel_preprocesamiento:
        0 = sin preprocesamiento
        1 = escala de grises
        2 = reducción de ruido
        3 = umbral adaptativo
    """
    if nivel_preprocesamiento == 0:
        return img_array

    # Convertir a escala de grises
    if len(img_array.shape) == 3:
        gris = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    else:
        gris = img_array

    if nivel_preprocesamiento == 1:
        return gris

    # Reducir ruido
    gris = cv2.medianBlur(gris, 3)

    if nivel_preprocesamiento == 2:
        return gris

    # Umbral adaptativo
    umbral = cv2.adaptiveThreshold(
        gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    return umbral

@app.get("/idiomas")
def obtener_idiomas():
    """Devuelve la lista de idiomas soportados"""
    return {
        "idiomas": [
            {"codigo": "spa", "nombre": "Español"},
            {"codigo": "eng", "nombre": "Inglés"},
            {"codigo": "fra", "nombre": "Francés"},
            {"codigo": "deu", "nombre": "Alemán"},
            {"codigo": "por", "nombre": "Portugués"},
            {"codigo": "ita", "nombre": "Italiano"}
        ]
    }
