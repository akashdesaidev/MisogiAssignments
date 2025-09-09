import os
from typing import List
from  langchain.schema import Document  
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file) -> List[Document]:
    """
    Extract langchain Document from pdf file sent to this function containing text image and table data, for image call llm to generate summary for the content.
    """
   
    data = []
    with open("temp.pdf", "wb") as f:
        f.write(file)

    loader = PyMuPDFLoader("temp.pdf" ,extract_images=True, extract_tables="html")
    documents = loader.load()
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documents = chunks.split_documents(documents)
    os.remove("temp.pdf")
    for doc in documents:
        print(doc)
        print("\n\n")
    return documents