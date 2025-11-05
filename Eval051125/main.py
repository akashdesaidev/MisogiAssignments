'''
Build an AI-powered Product Research System that allows users to input product page URLs and e-commerce product listings.

Your system should:

Crawl and extract relevant data from the given product page(s).

Store the textual and metadata information in a Vector Database using embeddings.

Enable hybrid retrieval — combining semantic similarity search (via embeddings) with metadata filtering.

Support natural language queries like:

“Find all products that have a price less than $50”

Generate summarized and relevant results using an LLM-powered RAG pipeline.

System Architecture Overview
Your pipeline should include the following layers: 

Input Layer – Accept URLs from users.
Crawler Layer – Crawl each URL, extract meaningful text and metadata.
Preprocessing Layer – Clean, chunk, and prepare text.
Embedding + Storage Layer – Generate embeddings and store them in a vector database (e.g., Chroma or Pinecone).
Retrieval + Generation Layer – Perform hybrid search and respond to user queries using an LLM.

'''
import requests
from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import getpass
# Crawler Layer
def crawl_product_page(url):    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract product title
    title = soup.find('h1').get_text() if soup.find('h1') else 'No Title Found'
    
    # Extract product price
    price = soup.find(class_='price').get_text() if soup.find(class_='price') else 'No Price Found'
      

      
    # Extract product description
    description = soup.find(class_='description').get_text() if soup.find(class_='description') else 'No Description Found'
    
    return {
        'title': title,
        'price': price,
        'description': description,
        'url': url
    }
# Preprocessing Layer
def preprocess_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    chunks = text_splitter.split_text(text)
    return chunks
# Embedding + Storage Layer
def store_in_vector_db(docs, metadatas):
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_texts(docs, embeddings, metadatas=metadatas)
    return vector_store
# Retrieval + Generation Layer
def create_qa_chain(vector_store):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Create a prompt template for the RAG chain
    prompt = ChatPromptTemplate.from_template("""
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {input}

Answer:""")
    
    # Create the document chain
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(vector_store.as_retriever(), document_chain)
    
    return retrieval_chain
def main():
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
    
    try:
        # Input Layer
        url = input("Enter the product page URL: ")
        
        # Crawl the product page
        print("Crawling product page...")
        product_data = crawl_product_page(url)
        
        # Preprocess the text
        combined_text = f"Title: {product_data['title']}\nPrice: {product_data['price']}\nDescription: {product_data['description']}"
        text_chunks = preprocess_text(combined_text)
        
        # Prepare metadata
        metadatas = [{'url': product_data['url'], 'title': product_data['title'], 'price': product_data['price']} for _ in text_chunks]
        
        # Store in vector database
        print("Creating vector embeddings and storing in database...")
        vector_store = store_in_vector_db(text_chunks, metadatas)
        
        # Create QA chain
        qa_chain = create_qa_chain(vector_store)
        
        # User query
        query = input("Enter your query (e.g., 'Find all products that have a price less than $50'): ")
        
        # Get answer
        print("Generating answer...")
        answer = qa_chain.invoke({"input": query})
        print("Answer:", answer["answer"])
        print("Sources:", [doc.metadata.get('url', 'Unknown') for doc in answer.get("context", [])])
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your inputs and try again.")

if __name__ == "__main__":
    main()