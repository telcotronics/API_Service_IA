import fitz
import pandas as pd
import docx
import tabula

from Class_ocr import OCRProcessor

class PDFConverter:
    def __init__(self, ocr_processor=None):
        self.ocr = ocr_processor

    def pdf_to_text(self, pdf_path, output_path=None, ocr_if_needed=True):
        try:
            with fitz.open(pdf_path) as pdf_document:
                text = ""
                # Utiliza la propiedad 'page_count' en lugar de 'len'
                for page_num in range(pdf_document.page_count):
                    page = pdf_document[page_num]
                    page_text = page.get_text()
                    text += page_text

                if not text.strip() and ocr_if_needed and self.ocr:
                    # Llama a tu lógica OCR aquí
                    pass

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)

            return text

        except Exception as e:
            raise Exception(f"Error al convertir PDF a texto: {str(e)}")

    def pdf_to_docx(self, pdf_path, output_path, ocr_if_needed=True):
        try:
            text = self.pdf_to_text(pdf_path, ocr_if_needed=ocr_if_needed)
            doc = docx.Document()
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    doc.add_paragraph(para)

            doc.save(output_path)
            return output_path

        except Exception as e:
            raise Exception(f"Error al convertir PDF a Word: {str(e)}")

    def pdf_to_excel(self, pdf_path, output_path, method='tabula', pages='all'):
        try:
            if method == 'tabula':
                tables = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)

                with pd.ExcelWriter(output_path) as writer:
                    for i, table in enumerate(tables):
                        table.to_excel(writer, sheet_name=f'Tabla_{i + 1}', index=False)

            else:
                raise ValueError(f"Método '{method}' no soportado")

            return output_path

        except Exception as e:
            raise Exception(f"Error al convertir PDF a Excel: {str(e)}")