import fitz  # PyMuPDF
from typing import Union

def extract_text_from_pdf(file_bytes: Union[bytes, bytearray]) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text