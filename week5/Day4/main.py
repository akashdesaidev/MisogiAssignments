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
        file_path = "./output_Dir/sample-report.pdf"
        loader = DoclingLoader(file_path=file_path)
        # docs = loader.load()
       
        Fitdoc = fitz.open("./output_Dir/Attention.pdf")
        for page_num, page in enumerate(Fitdoc):
         imgs = page.get_images(full=True)
         print(f"Page {page_num}: {len(imgs)} images")
        # Loop through docling's unified documents

        image_pattern = re.compile(r'!\[\]\((data:image\/[a-zA-Z]+;base64,[^)]+)\)')

        num_images = 0

        # for doc in docs:
        #     # In Docling, extracted page/image content is often in markdown-style format
        #     for match in image_pattern.findall(doc.page_content):
        #         header, encoded = match.split(',', 1)
        #         ext = header.split('/')[1].split(';')[0]
        #         img_path = os.path.join(output_dir, f"docling_image_{num_images+1}.{ext}")
        #         with open(img_path, "wb") as f:
        #             f.write(base64.b64decode(encoded))
        #         print(f"Saved image: {img_path}")
        #         num_images += 1

        # print(f"Total images extracted: {num_images}")
        # # for doc in docs:
        #     print(doc)
        #     print()
        # for page_num, doc in enumerate(docs):
            # content = doc.page_content
            # base64_images = re.findall(r'!\[\]\((data:image\/[a-zA-Z]+;base64,[^)]+)\)', content)
            # for img_data in base64_images:
            #     header, encoded = img_data.split(',', 1)
            #     img_bytes = base64.b64decode(encoded)
            #     images_bytes.append(img_bytes)
        return {
            "message": "Images extracted successfully (async)",
          
            "note": "You can now process images_bytes asynchronously for LLM input."
        }
    except Exception as e:
        return {"message": "Error extracting images", "error": str(e)}