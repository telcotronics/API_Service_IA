import gradio as gr
from convert import PDFConverter  # Asume que tu clase está en el archivo convert.py

# Instancia de la clase PDFConverter
# Si tu clase necesita una instancia de OCR, asegúrate de pasarla aquí.
converter = PDFConverter()

def procesar_pdf(archivo_pdf):
    """
    Procesa un archivo PDF subido por el usuario.
    Gradio pasa la ruta temporal del archivo.

    Args:
        archivo_pdf: El objeto de archivo de Gradio con la ruta temporal.

    Returns:
        El resultado del procesamiento (texto, ruta de archivo, etc.).
    """
    if archivo_pdf is None:
        return "Error: Por favor, sube un archivo."

    try:
        # Llama a tu método pdf_to_text. Gradio proporciona el archivo
        # como un objeto con un atributo 'name' que es la ruta.
        texto_extraido = converter.pdf_to_text(pdf_path=archivo_pdf.name)
        return texto_extraido
    except Exception as e:
        return f"Error al procesar el PDF: {str(e)}"

# Define la interfaz web
# 'gr.File' es el componente correcto para subir archivos.
web = gr.Interface(
    fn=procesar_pdf,
    inputs=gr.File(label="Sube un archivo PDF"),
    outputs=gr.Textbox(label="Texto extraído"),
    title="Convertidor de PDF",
    description="Sube un archivo PDF para extraer su texto."
)

# Lanza la interfaz
web.launch()