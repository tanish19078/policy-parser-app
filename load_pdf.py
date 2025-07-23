# load_pdf.py
import fitz  # PyMuPDF

def load_pdf_text(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()
