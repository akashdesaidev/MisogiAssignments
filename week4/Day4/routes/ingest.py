from fastapi import APIRouter, UploadFile, File
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import tempfile
import os
from pprint import pprint

router = APIRouter()


def print_documents_nicely(documents):
    for i, doc in enumerate(documents, 1):
        print(f"\n--- Document {i} ---")
        print("Metadata:")
        pprint(doc.metadata)  # prints metadata dict nicely
        print("\nContent Preview:")
        # Print only the first 500 characters to avoid too long output
        print(doc.page_content[:500].replace('\n', '\\n'))
        print("\n" + "-"*40)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save uploaded file to a temp file
    suffix = os.path.splitext(file.filename)[1]
    if suffix != ".pdf":
        return {"error": "Only PDF files are supported for now"}

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    # Load documents from the temp PDF file path
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    # Delete the temp file explicitly after loading
    os.unlink(tmp_path)

    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n", "\n\n", " ", ". "]
    )

    # Split documents into chunks
    chunks = splitter.split_documents(documents)
    # Example usage assuming 'documents' is your list of Document objects
    print_documents_nicely(chunks)

   
    # Here you would embed and store your chunks
    # embeddings = embed_chunks(chunks)
    # store_chunks(chunks, embeddings)

    return {"message": "PDF processed and stored", "num_chunks": len(chunks)}
