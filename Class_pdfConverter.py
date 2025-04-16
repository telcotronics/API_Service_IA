import fitz
import pandas as pd
import docx
import tabula

# Para PDFs escaneados (usando tu OCR existente)
from Class_ocr import OCRProcessor  # Tu clase OCR existente

class PDFConverter:
    def __init__(self, ocr_processor=None):
        """
        Inicializa el convertidor de PDF

        Args:
            ocr_processor: Instancia de OCRProcessor para PDFs escaneados (opcional)
        """
        self.ocr = ocr_processor

    def pdf_to_text(self, pdf_path, output_path=None, ocr_if_needed=True):
        """
        Convierte un PDF a texto plano

        Args:
            pdf_path: Ruta al archivo PDF
            output_path: Ruta para guardar el archivo de texto (opcional)
            ocr_if_needed: Utilizar OCR si no se encuentra texto en el PDF

        Returns:
            Texto extraído del PDF
        """
        try:
            # Abrir el PDF
            pdf_document = fitz.open(pdf_path)
            text = ""

            # Extraer texto de cada página
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                page_text = page.get_text()
                text += page_text

            # Si no hay texto y está habilitado OCR, usar OCR
            if not text.strip() and ocr_if_needed and self.ocr:
                text = self._extract_with_ocr(pdf_document)

            # Guardar resultado si se especificó una ruta
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)

            return text

        except Exception as e:
            raise Exception(f"Error al convertir PDF a texto: {str(e)}")

    def pdf_to_docx(self, pdf_path, output_path, ocr_if_needed=True):
        """
        Convierte un PDF a documento Word (.docx)

        Args:
            pdf_path: Ruta al archivo PDF
            output_path: Ruta para guardar el archivo Word
            ocr_if_needed: Utilizar OCR si no se encuentra texto en el PDF

        Returns:
            Ruta al archivo Word generado
        """
        try:
            # Extraer texto (con OCR si es necesario)
            text = self.pdf_to_text(pdf_path, ocr_if_needed=ocr_if_needed)

            # Crear documento Word
            doc = docx.Document()

            # Dividir por párrafos y añadir al documento
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    doc.add_paragraph(para)

            # Guardar documento
            doc.save(output_path)
            return output_path

        except Exception as e:
            raise Exception(f"Error al convertir PDF a Word: {str(e)}")

    def pdf_to_excel(self, pdf_path, output_path, method='tabula', pages='all'):
        """
        Convierte tablas de un PDF a Excel (versión sin Camelot)

        Args:
            pdf_path: Ruta al archivo PDF
            output_path: Ruta para guardar el archivo Excel
            method: Método de extracción ('tabula', 'ocr')
            pages: Páginas a procesar ('all' o lista de números)

        Returns:
            Ruta al archivo Excel generado
        """
        try:
            if method == 'tabula':
                # Usar tabula-py para PDFs con tablas nativas
                tables = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)

                with pd.ExcelWriter(output_path) as writer:
                    for i, table in enumerate(tables):
                        table.to_excel(writer, sheet_name=f'Tabla_{i + 1}', index=False)

            elif method == 'ocr' and self.ocr:
                # Usar OCR para PDFs escaneados
                self._extract_tables_with_ocr(pdf_path, output_path)

            else:
                raise ValueError(f"Método '{method}' no soportado o OCR no disponible")

            return output_path

        except Exception as e:
            raise Exception(f"Error al convertir PDF a Excel: {str(e)}")
