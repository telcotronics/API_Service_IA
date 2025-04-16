import pytesseract
import cv2
import numpy as np


class OCRProcessor:
    def __init__(self, tesseract_path=None, idioma='spa'):
        """
        Inicializa el procesador OCR

        Args:
            tesseract_path: Ruta al ejecutable de Tesseract (opcional)
            idioma: Idioma para el reconocimiento (default: español)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.idioma = idioma

    def preprocesar_imagen(self, img_array, nivel_preprocesamiento=1):
        """
        Preprocesa la imagen para mejorar el OCR

        Args:
            img_array: Array de imagen (numpy.ndarray)
            nivel_preprocesamiento:
                0 = sin preprocesamiento
                1 = escala de grises
                2 = reducción de ruido
                3 = umbral adaptativo

        Returns:
            Imagen preprocesada
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

    def extraer_texto(self, imagen, nivel_preprocesamiento=3, config=''):
        """
        Extrae texto de una imagen

        Args:
            imagen: Ruta a la imagen o array de imagen
            nivel_preprocesamiento: Nivel de preprocesamiento (0-3)
            config: Configuración adicional para pytesseract

        Returns:
            Texto extraído de la imagen
        """
        # Cargar imagen si se proporciona una ruta
        if isinstance(imagen, str):
            img_array = cv2.imread(imagen)
            if img_array is None:
                raise ValueError(f"No se pudo cargar la imagen: {imagen}")
        else:
            img_array = imagen

        # Preprocesar imagen
        img_procesada = self.preprocesar_imagen(img_array, nivel_preprocesamiento)

        # Extraer texto
        texto = pytesseract.image_to_string(img_procesada, lang=self.idioma, config=config)

        return texto

    def extraer_datos_estructurados(self, imagen, nivel_preprocesamiento=3):
        """
        Extrae datos estructurados de la imagen (cajas de texto, datos, etc.)

        Args:
            imagen: Ruta a la imagen o array de imagen
            nivel_preprocesamiento: Nivel de preprocesamiento (0-3)

        Returns:
            DataFrame con los datos extraídos
        """
        # Cargar imagen si se proporciona una ruta
        if isinstance(imagen, str):
            img_array = cv2.imread(imagen)
            if img_array is None:
                raise ValueError(f"No se pudo cargar la imagen: {imagen}")
        else:
            img_array = imagen

        # Preprocesar imagen
        img_procesada = self.preprocesar_imagen(img_array, nivel_preprocesamiento)

        # Extraer datos
        datos = pytesseract.image_to_data(img_procesada, lang=self.idioma, output_type=pytesseract.Output.DATAFRAME)

        # Filtrar filas con texto
        datos_filtrados = datos[datos['text'].str.strip() != '']

        return datos_filtrados

