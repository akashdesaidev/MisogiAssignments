from fastapi import APIRouter, Depends, HTTPException,UploadFile, File
from pydantic import BaseModel
from typing import List

from DB.VectorDB import VectorDB
from utils.PdfProcessing import extract_text_from_pdf

ingestRouter = APIRouter( tags=["Ingest"] ,prefix="/ingest")


@ingestRouter.post("/")
async def ingest_data(data: UploadFile = File(...)):
    """
    Endpoint to ingest data to vector DB.
    """
    try:

        vector_db = VectorDB(persist_directory="../DB/vector_db")
        if data.content_type == "application/pdf":
            file = await data.read()
            documents = extract_text_from_pdf(file)
            vector_db.add_documents(documents)
        elif data.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # process DOCX file
            pass
        elif data.content_type == "text/html":
                # process HTML file
                pass
        return {"status": "success", "message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))