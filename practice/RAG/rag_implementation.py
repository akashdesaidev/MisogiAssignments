import os
from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import json

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, continue without it
class RAGSystem:
    def __init__(self, openai_api_key: str, collection_name: str = "rag_collection"):
        """
        Initialize the RAG system with OpenAI API key and collection name.
        
        Args:
            openai_api_key (str): OpenAI API key
            collection_name (str): Name for the Chroma collection
        """
        self.openai_api_key = openai_api_key
        self.collection_name = collection_name
        
        # Set OpenAI API key
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize embeddings and LLM
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.1,
            max_tokens=1000
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Initialize vector store
        self.vector_store = None
        self.retriever = None
        self.qa_chain = None
        
    def add_documents(self, documents: List[str], metadata: List[Dict[str, Any]] = None):
        """
        Add documents to the vector store.
        
        Args:
            documents (List[str]): List of document texts
            metadata (List[Dict[str, Any]], optional): List of metadata for each document
        """
        # Create Document objects
        docs = []
        for i, doc_text in enumerate(documents):
            doc_metadata = metadata[i] if metadata and i < len(metadata) else {"source": f"document_{i}"}
            docs.append(Document(page_content=doc_text, metadata=doc_metadata))
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(docs)
        
        # Create or get vector store
        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=split_docs,
                embedding=self.embeddings,
                collection_name=self.collection_name
            )
        else:
            self.vector_store.add_documents(split_docs)
        
        # Initialize retriever and QA chain
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create custom prompt template
        prompt_template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )
        
        print(f"Added {len(split_docs)} document chunks to the vector store.")
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        Args:
            question (str): The question to ask
            
        Returns:
            Dict[str, Any]: Dictionary containing answer and source documents
        """
        if self.qa_chain is None:
            raise ValueError("No documents have been added to the system yet.")
        
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }
    
    def search_similar(self, query: str, k: int = 4) -> List[Dict[str, Any]]:
        """
        Search for similar documents without generating an answer.
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of similar documents
        """
        if self.retriever is None:
            raise ValueError("No documents have been added to the system yet.")
        
        docs = self.retriever.get_relevant_documents(query)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": doc.metadata.get("score", 0.0)
            }
            for doc in docs
        ]
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the current collection.
        
        Returns:
            Dict[str, Any]: Collection information
        """
        if self.vector_store is None:
            return {"status": "No collection initialized"}
        
        try:
            collection = self.vector_store._collection
            count = collection.count()
            
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "embedding_dimension": "cosine"  # Default for OpenAI embeddings
            }
        except Exception as e:
            return {
                "collection_name": self.collection_name,
                "document_count": "Unknown",
                "error": str(e)
            }

def main():
    """
    Example usage of the RAG system.
    """
    # Get API key from environment variable
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        print("❌ Error: No valid OpenAI API key found!")
        print("\nTo fix this, please:")
        print("1. Get your API key from: https://platform.openai.com/account/api-keys")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='your-actual-api-key'")
        print("   # or on Windows:")
        print("   set OPENAI_API_KEY=your-actual-api-key")
        print("\n3. Or create a .env file in this directory with:")
        print("   OPENAI_API_KEY=your-actual-api-key")
        return
    
    # Initialize RAG system
    rag = RAGSystem(OPENAI_API_KEY)
    
    # Sample documents
    sample_documents = [
        """
        Artificial Intelligence (AI) is a branch of computer science that aims to create intelligent machines 
        that work and react like humans. Some of the activities computers with artificial intelligence are 
        designed for include speech recognition, learning, planning, and problem solving.
        """,
        """
        Machine Learning is a subset of AI that provides systems the ability to automatically learn and 
        improve from experience without being explicitly programmed. Machine learning focuses on the 
        development of computer programs that can access data and use it to learn for themselves.
        """,
        """
        Deep Learning is a subset of machine learning that uses neural networks with multiple layers 
        to model and understand complex patterns. It has been particularly successful in areas like 
        image recognition, natural language processing, and speech recognition.
        """,
        """
        Natural Language Processing (NLP) is a field of AI that gives machines the ability to read, 
        understand, and derive meaning from human languages. It combines computational linguistics 
        with statistical, machine learning, and deep learning models.
        """
    ]
    
    # Add documents to the system
    print("Adding documents to the RAG system...")
    rag.add_documents(sample_documents)
    
    # Get collection info
    print("\nCollection Information:")
    print(json.dumps(rag.get_collection_info(), indent=2))
    
    # Example queries
    queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "What is the relationship between deep learning and neural networks?",
        "What are the applications of natural language processing?"
    ]
    
    print("\n" + "="*50)
    print("RAG SYSTEM QUERIES")
    print("="*50)
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 30)
        
        try:
            result = rag.query(query)
            print(f"Answer: {result['answer']}")
            print(f"Sources: {len(result['source_documents'])} documents retrieved")
        except Exception as e:
            print(f"Error: {e}")
    
    # Example similarity search
    print("\n" + "="*50)
    print("SIMILARITY SEARCH")
    print("="*50)
    
    search_query = "neural networks and learning"
    print(f"\nSearching for: {search_query}")
    
    try:
        similar_docs = rag.search_similar(search_query)
        print(f"Found {len(similar_docs)} similar documents:")
        
        for i, doc in enumerate(similar_docs, 1):
            print(f"\nDocument {i}:")
            print(f"Content: {doc['content'][:200]}...")
            print(f"Metadata: {doc['metadata']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Check if OpenAI API key is provided
    if os.getenv("OPENAI_API_KEY"):
        main()
    else:
        print("Please set your OpenAI API key before running the script.")
        print("You can either:")
        print("1. Set the OPENAI_API_KEY environment variable")
        print("2. Replace 'your-openai-api-key-here' in the main() function")
        print("3. Pass your API key directly to the RAGSystem constructor") 