from PyPDF2 import PdfReader
from docx import Document

class Extractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_pdf(self):
        try:
            reader = PdfReader(self.file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return None

    def extract_docx(self):
        try:
            doc = Document(self.file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return None