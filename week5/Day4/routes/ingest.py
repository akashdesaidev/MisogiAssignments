from fastapi import APIRouter, HTTPException    
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
router=APIRouter(prefix="/ingest")

@router.get("/")
def ingest_pdf():
    try:
        file_path = "./output_Dir/Attention.pdf"   
        loader = PyMuPDFLoader(file_path)
        docs =loader.load()
        # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        # chunks=splitter.create_documents(docs)       
        embeddings=OpenAIEmbeddings(model="text-embedding-3-small")
        # Invoke the chain (no arguments needed for loaders)
        
        vector_store = Chroma(embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),collection_name="my_collection",  persist_directory="./chroma_langchain_db",)
        vector_store.add_documents(documents=docs)
        results = vector_store.similarity_search_by_vector(
        embedding=embeddings.embed_query("Attention"), k=1
        )
        for doc in results:
            print(f"* {doc.page_content} [{doc.metadata}]")
        return results[0]     
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
