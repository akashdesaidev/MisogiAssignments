from fastapi import FastAPI, UploadFile, File,HTTPException
from langchain_community.document_loaders import TextLoader
from langchain_docling import DoclingLoader
from typing import Union
from pprint import pprint
from tabulate import tabulate
import os
import re
import base64 
import fitz
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.parsers import LLMImageBlobParser
from dotenv import load_dotenv 

load_dotenv()
# from langchain_community.document_loaders import PyMuPDFLoader
# from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from unstructured.partition.pdf import partition_pdf
# os.environ["PATH"] += os.pathsep + r"C:\poppler\poppler-24.08.0\Library\bin"
# os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/extract-images-async")
def extract_images_async():
    try:
        output_dir="./output_Dir/"
        file_path = "./output_Dir/Attention.pdf"
        loader = PyMuPDFLoader(
            file_path=file_path,
            mode="page",                        # Split PDF into per-page documents
            extract_images=True,                 # Enable image extraction
            images_inner_format="markdown-img"   # Embed images as markdown base64 in page content
        )

        docs = loader.load()  # docs is a list: one Document object per page

        Fitdoc = fitz.open(filename=file_path)
        for page_num, page in enumerate(Fitdoc):
         imgs = page.get_images(full=True)
         print(f"Page {page_num}: {len(imgs)} images")
        # Loop through docling's unified documents

        for idx, doc in enumerate(docs):
            if idx == 2 or idx==3:
                print(f"Page {idx} Metadata:", doc.metadata)
                print(f"Page {idx} Content Sample:", doc.page_content[:400])
                images = re.findall(r'!\[\]\((data:image\/[a-zA-Z]+;base64,[^)]+)\)', doc.page_content)
                print("Images in page using langchain pymupdf", idx, "are", images)
                
  
        return {
            "message": "Images extracted successfully (async)",
          
            "note": "You can now process images_bytes asynchronously for LLM input."
        }
    except Exception as e:
        return {"message": "Error extracting images", "error": str(e)}