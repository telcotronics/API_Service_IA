import gradio as gr
import pytesseract
from PIL import Image
import cv2
import numpy as np


def preprocesar_imagen(imagen, aplicar_preprocesamiento):
    """Preprocesa la imagen para mejorar el reconocimiento de texto"""
    if aplicar_preprocesamiento:
        # Convertir a escala de grises
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        gris = cv2.cvtColor(gris, cv2.COLOR_RGB2GRAY)

        # Reducir ruido
        gris = cv2.medianBlur(gris, 3)

        # Aplicar umbral adaptativo
        umbral = cv2.adaptiveThreshold(
            gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        return umbral
    return imagen


def ocr(imagen, idioma, aplicar_preprocesamiento):
    """Realiza OCR en la imagen proporcionada"""
    if imagen is None:
        return "Por favor, sube una imagen"

    # Convertir de formato Gradio a formato numpy/OpenCV
    img_array = np.array(imagen)

    # Preprocesar si es necesario
    if aplicar_preprocesamiento:
        img_procesada = preprocesar_imagen(img_array, aplicar_preprocesamiento)
        # Convertir a PIL Image para pytesseract
        img_pil = Image.fromarray(img_procesada)
    else:
        # Usar la imagen original
        img_pil = Image.fromarray(img_array)

    # Realizar OCR
    texto = pytesseract.image_to_string(img_pil, lang=idioma)

    # Si no hay texto reconocido
    if not texto.strip():
        return "No se pudo detectar texto en la imagen"

    return texto


# Crear la interfaz Gradio
web = gr.Interface(
    fn=ocr,
    inputs=[
        gr.Image(type="pil", label="Imagen con texto"),
        gr.Dropdown(
            choices=["eng", "spa", "fra", "deu"],
            value="spa",
            label="Idioma del texto"
        ),
        gr.Checkbox(label="Aplicar preprocesamiento")
    ],
    outputs=gr.Textbox(label="Texto extraído"),
    title="OCR - Reconocimiento Óptico de Caracteres",
    description="Sube una imagen con texto y se extraerá el contenido textual",
    examples=[
        ["imagen_ejemplo.jpg", "spa", True],
    ],
    flagging_mode="never"
)
web.launch()