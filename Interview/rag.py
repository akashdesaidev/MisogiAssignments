
import os
import fitz  # PyMuPDF
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text().strip()
    return text

def recursive_character_text_splitter(text, max_chunk_size, overlap):
    """Splits text into chunks of a maximum size with a specified overlap."""
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        chunks.append(text[start:end])
        start += max_chunk_size - overlap
    return chunks

def main():
    """
    Main function to run the RAG pipeline.
    """
    # 1. Document Loading
    pdf_path = "pokemon_4page_info.pdf"  # Create a dummy PDF for testing
    if not os.path.exists(pdf_path):
        # Create a dummy PDF for demonstration
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "This is a test document for the RAG pipeline.")
        doc.save(pdf_path)
        doc.close()

    document_text = get_pdf_text(pdf_path)

    # 2. Text Splitting
    text_chunks = recursive_character_text_splitter(document_text, 1000, 200)

    # 3. Vector Store
    chroma_client = chromadb.Client()
    collection = chroma_client.get_or_create_collection(name="rag_collection")

    # 4. Embedding and Storage
    for i, chunk in enumerate(text_chunks):
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        collection.add(
            embeddings=[embedding],
            documents=[chunk],
            ids=[str(i)]
        )

    # 5. Query from Terminal
    query = input("Enter your query: ")

    # 6. Retrieval
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = response.data[0].embedding
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    retrieved_chunks = results['documents'][0]

    # 7. Generation
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. make sure to answer the question in the same language as the question."},
            {"role": "user", "content": f"Context:\n{''.join(retrieved_chunks)}\n\nQuestion: {query}"}
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
