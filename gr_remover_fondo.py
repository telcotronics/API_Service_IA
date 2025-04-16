import gradio as gr
from rembg import remove
from PIL import Image
import numpy as np
import io

def remover_fondo(imagen):
    # Convertir imagen a bytes
    img_bytes = io.BytesIO()
    imagen.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    # Quitar fondo
    resultado = remove(img_bytes)

    # Convertir resultado a imagen PIL
    img_salida = Image.open(io.BytesIO(resultado)).convert("RGBA")
    return img_salida

#generar interface web
web = gr.Interface(
    fn=remover_fondo,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="Quitar Fondo con Rembg",
    description="Sube una imagen y quitaré el fondo usando rembg."
)

web.launch()