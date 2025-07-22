# RAG Chunking Strategy Visualizer

A web application that allows users to upload PDF documents and visualize different chunking strategies for RAG (Retrieval-Augmented Generation) systems.

## Features

- PDF Upload & Text Extraction
- Multiple Chunking Strategies:
  - Fixed Size: Split text into chunks of fixed size with overlap
  - Sentence-based: Split text by sentences, maintaining semantic coherence
  - Paragraph-based: Split text by paragraphs, combining small ones and splitting large ones
  - Sliding Window: Split text using a sliding window approach with fixed overlap
- Interactive Chunk Visualization
- Configurable Chunk Size and Overlap
- Metadata Display for Each Chunk

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   └── text_chunker.py  # Text chunking implementations
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── src/
    │   ├── app/
    │   │   └── page.tsx     # Main application page
    │   └── components/      # React components
    └── package.json         # Node.js dependencies
```

## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Upload a PDF document using the drag & drop interface
3. Select a chunking strategy from the dropdown
4. Adjust chunk size and overlap using the sliders
5. View the resulting chunks and their metadata
6. Click on individual chunks to see detailed information

## Chunking Strategies

### Fixed Size
- Splits text into chunks of exactly the specified size
- Good for maintaining consistent chunk sizes
- May break semantic units (sentences/paragraphs)

### Sentence-based
- Splits text at sentence boundaries
- Maintains semantic coherence at sentence level
- Chunk sizes may vary significantly

### Paragraph-based
- Splits text at paragraph boundaries
- Combines small paragraphs and splits large ones
- Best for documents with clear paragraph structure

### Sliding Window
- Uses a moving window with fixed overlap
- Good for capturing context across chunk boundaries
- Consistent overlap between chunks

## Trade-offs

Each chunking strategy offers different trade-offs:

- **Semantic Coherence vs. Size Consistency**: Fixed-size chunking ensures consistent sizes but may break semantic units. Sentence and paragraph-based chunking preserve meaning but produce variable-sized chunks.

- **Context Preservation vs. Storage Efficiency**: Higher overlap between chunks helps preserve context but increases storage requirements and processing time.

- **Processing Speed vs. Quality**: Simple strategies like fixed-size chunking are faster but may produce lower quality chunks. Semantic-aware strategies provide better chunks but require more processing.

## API Endpoints

- `POST /upload`: Upload PDF file
  - Input: PDF file
  - Output: Extracted text

- `POST /chunk`: Chunk text using specified strategy
  - Input: 
    ```json
    {
      "text": "text to chunk",
      "strategy": "fixed|sentence|paragraph|sliding",
      "chunk_size": 500,
      "overlap": 50
    }
    ```
  - Output: Chunks and metadata

## Frontend Setup (To be completed)

The frontend setup is pending due to Node.js installation issues. Once Node.js is properly installed, we'll add React-based frontend implementation. 