from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import dotenv
from uuid import uuid4

dotenv.load_dotenv()
class VectorDB:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.db = Chroma(collection_name="collection",persist_directory=self.persist_directory, embedding_function=self.embeddings)

    def add_documents(self, documents):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.db.add_documents(documents=documents,  ids=uuids)
    

    def query(self, query_text: str, k: int = 5):
        return self.db.similarity_search(query_text, k=k)

    def delete_collection(self):
        self.db.delete_collection()

    def get_collection_info(self):
        return self.db.get_collection_info()