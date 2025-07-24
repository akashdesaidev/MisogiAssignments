from fastapi import APIRouter, UploadFile, File
from utils.file_parser import extract_text_from_pdf
from services.chunker import chunk_text
# from services.embedder import embed_chunks
# from services.vectorstore import store_chunks

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text_from_pdf(contents)

    chunks = chunk_text(text)
    print(chunks)
    # embeddings = embed_chunks(chunks)
    # store_chunks(chunks, embeddings)

    return {"message": "PDF processed and stored", "num_chunks": len(chunks)}