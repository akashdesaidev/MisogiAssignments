from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from typing import List, Dict
from app.text_chunker import (
    fixed_size_chunker,
    sentence_chunker,
    paragraph_chunker,
    sliding_window_chunker
)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "Only PDF files are allowed"}
    
    try:
        # Read PDF content
        pdf_content = await file.read()
        reader = PdfReader(file.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}

@app.post("/chunk")
async def chunk_text(data: Dict):
    text = data.get("text", "")
    strategy = data.get("strategy", "fixed")
    chunk_size = data.get("chunk_size", 500)
    overlap = data.get("overlap", 50)
    
    if not text:
        return {"error": "No text provided"}
    
    chunkers = {
        "fixed": fixed_size_chunker,
        "sentence": sentence_chunker,
        "paragraph": paragraph_chunker,
        "sliding": sliding_window_chunker
    }
    
    chunker = chunkers.get(strategy)
    if not chunker:
        return {"error": "Invalid chunking strategy"}
    
    try:
        chunks = chunker(text, chunk_size=chunk_size, overlap=overlap)
        return {
            "chunks": chunks,
            "metadata": {
                "total_chunks": len(chunks),
                "average_chunk_size": sum(len(chunk) for chunk in chunks) / len(chunks),
                "strategy": strategy
            }
        }
    except Exception as e:
        return {"error": str(e)} 