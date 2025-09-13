from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from db import get_db
import os

def create_vector_store():
    db = get_db()
    embeddings = OpenAIEmbeddings()
    vectore_store = Chroma.from_sql_database(db, embeddings, collection_name="my_collection", persist_directory="./chroma_db")
    return vectore_store