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
from routes import ingest_router,testrouter
load_dotenv()
# from langchain_community.document_loaders import PyMuPDFLoader
# from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from unstructured.partition.pdf import partition_pdf
# os.environ["PATH"] += os.pathsep + r"C:\poppler\poppler-24.08.0\Library\bin"
# os.environ["PATH"] += os.pathsep + r"C:\Program Files\Tesseract-OCR"

app = FastAPI()

app.include_router(ingest_router)
app.include_router(testrouter)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

