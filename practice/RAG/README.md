# Basic RAG Implementation with Langchain

This is a complete Retrieval-Augmented Generation (RAG) system implemented using Langchain, OpenAI, and Chroma DB. The implementation is contained in a single file for simplicity and ease of use.

## Features

- **Document Ingestion**: Add documents to the vector store with automatic text chunking
- **Semantic Search**: Find similar documents using vector similarity
- **Question Answering**: Generate answers based on retrieved context
- **Metadata Support**: Track document sources and metadata
- **Collection Management**: Get information about your vector store collections

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Internet connection for API calls

## Installation

1. **Clone or download the files**:

   - `rag_implementation.py` - Main RAG implementation
   - `requirements.txt` - Python dependencies
   - `README.md` - This documentation

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:

   **Option A: Environment variable**

   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

   **Option B: .env file (recommended)**

   ```bash
   # Copy the template
   cp env_template.txt .env
   # Edit .env and add your actual API key
   ```

   **Option C: Direct in code**

   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
   ```

## Quick Start

```python
from rag_implementation import RAGSystem

# Initialize the RAG system
rag = RAGSystem("your-openai-api-key")

# Add some documents
documents = [
    "Your first document content here...",
    "Your second document content here...",
    "More document content..."
]

rag.add_documents(documents)

# Ask questions
result = rag.query("What is the main topic?")
print(result["answer"])

# Search for similar documents
similar_docs = rag.search_similar("neural networks")
for doc in similar_docs:
    print(doc["content"])
```

## Usage Examples

### 1. Basic Document Addition and Querying

```python
from rag_implementation import RAGSystem

# Initialize system
rag = RAGSystem("your-api-key")

# Add documents with metadata
documents = [
    "Machine learning is a subset of artificial intelligence...",
    "Deep learning uses neural networks with multiple layers...",
    "Natural language processing enables computers to understand text..."
]

metadata = [
    {"source": "ml_intro", "topic": "machine_learning"},
    {"source": "dl_basics", "topic": "deep_learning"},
    {"source": "nlp_overview", "topic": "nlp"}
]

rag.add_documents(documents, metadata)

# Query the system
result = rag.query("What is machine learning?")
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['source_documents'])} documents")
```

### 2. Similarity Search

```python
# Search for similar documents without generating an answer
similar_docs = rag.search_similar("neural networks and AI", k=3)

for i, doc in enumerate(similar_docs, 1):
    print(f"Document {i}:")
    print(f"Content: {doc['content'][:100]}...")
    print(f"Metadata: {doc['metadata']}")
    print()
```

### 3. Collection Information

```python
# Get information about your vector store
info = rag.get_collection_info()
print(f"Collection: {info['collection_name']}")
print(f"Documents: {info['document_count']}")
```

## API Reference

### RAGSystem Class

#### Constructor

```python
RAGSystem(openai_api_key: str, collection_name: str = "rag_collection")
```

#### Methods

- **`add_documents(documents, metadata=None)`**: Add documents to the vector store
- **`query(question)`**: Ask a question and get an answer with sources
- **`search_similar(query, k=4)`**: Find similar documents
- **`get_collection_info()`**: Get collection statistics

## Configuration Options

### Text Splitting

The system uses `RecursiveCharacterTextSplitter` with these default settings:

- Chunk size: 1000 characters
- Chunk overlap: 200 characters

### LLM Settings

- Model: `gpt-3.5-turbo`
- Temperature: 0.1 (for consistent answers)
- Max tokens: 1000

### Retrieval Settings

- Search type: Similarity
- Number of retrieved documents: 4

## Running the Example

To run the included example:

```bash
python rag_implementation.py
```

This will:

1. Add sample AI/ML documents to the system
2. Demonstrate querying capabilities
3. Show similarity search functionality
4. Display collection information

## Customization

### Changing the LLM Model

```python
self.llm = ChatOpenAI(
    model_name="gpt-4",  # Change to gpt-4 for better performance
    temperature=0.1,
    max_tokens=1000
)
```

### Adjusting Text Chunking

```python
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Smaller chunks for more precise retrieval
    chunk_overlap=100,   # Less overlap
    length_function=len,
)
```

### Modifying Retrieval Parameters

```python
self.retriever = self.vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6}  # Retrieve more documents
)
```

## Error Handling

The system includes error handling for common issues:

- Missing OpenAI API key
- No documents added to the system
- API rate limits
- Network connectivity issues

## Performance Considerations

- **Chunk Size**: Smaller chunks (500-1000 chars) work well for precise retrieval
- **Overlap**: 10-20% overlap helps maintain context across chunks
- **Retrieval Count**: 3-6 documents typically provide good context
- **Model Choice**: GPT-4 provides better answers but costs more

## Troubleshooting

### Common Issues

1. **"No documents added" error**: Make sure to call `add_documents()` before querying
2. **API key errors**: Verify your OpenAI API key is correct and has sufficient credits
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
4. **Chroma DB issues**: The system creates a local Chroma database automatically

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed correctly
2. Verify your OpenAI API key is valid
3. Ensure you have an internet connection for API calls
4. Check the error messages for specific guidance

## License

This implementation is provided as-is for educational and development purposes.
