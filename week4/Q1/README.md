# Document Analyzer

A comprehensive document analysis tool that provides sentiment analysis, keyword extraction, readability scoring, and document management capabilities using Google Gemini AI.

## Features

- **Document Storage**: 16 sample technology/AI articles with metadata
- **Sentiment Analysis**: Analyze text sentiment (positive/negative/neutral) with confidence scores
- **Keyword Extraction**: Extract top keywords with relevance scores
- **Readability Analysis**: Calculate readability scores and reading levels
- **Document Search**: Fuzzy text matching for document discovery
- **Document Management**: Add new documents to the knowledge base

## Requirements

- Python 3.7+
- Google Gemini API key

## Installation

1. Clone or download the project files
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project directory
   - Add your API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

### Available Functions

#### 1. `analyze_document(document_id)`
Performs comprehensive analysis of a document by ID.

```python
from main import analyze_document

# Analyze a specific document
result = analyze_document("doc_001")
print(result)
```

#### 2. `get_sentiment(text)`
Analyzes sentiment of any text.

```python
from main import get_sentiment

# Analyze sentiment
result = get_sentiment("This AI technology is amazing!")
print(result)
```

#### 3. `extract_keywords(text, limit=10)`
Extracts top keywords from text.

```python
from main import extract_keywords

# Extract keywords
result = extract_keywords("Machine learning and artificial intelligence", limit=5)
print(result)
```

#### 4. `add_document(document_data)`
Adds a new document to the knowledge base.

```python
from main import add_document

# Add new document
new_doc = add_document({
    "title": "New AI Article",
    "content": "Content of the article...",
    "createdby": "Author Name",
    "category": "AI Technology"
})
print(new_doc)
```

#### 5. `search_documents(query, limit=10)`
Searches documents using fuzzy text matching.

```python
from main import search_documents

# Search documents
results = search_documents("neural networks", limit=5)
print(results)
```

### Running the Example

Run the main script to see all functions in action:

```bash
python main.py
```

## Sample Data

The knowledge base (`kb.json`) contains 16 technology/AI articles covering topics like:
- Machine Learning
- Deep Learning
- Generative AI
- Natural Language Processing
- Computer Vision
- AI Ethics
- Quantum Computing
- Robotics
- And more...

## Data Structure

### Document Structure
```json
{
  "id": "doc_001",
  "title": "Document Title",
  "content": "Document content...",
  "metadata": {
    "createdby": "Author Name",
    "time": "2024-01-15T10:30:00Z",
    "category": "Technology",
    "word_count": 150,
    "created_at": "2024-01-15"
  }
}
```

### Analysis Output Structure
```json
{
  "document_id": "doc_001",
  "title": "Document Title",
  "basic_stats": {
    "word_count": 150,
    "sentence_count": 8,
    "character_count": 900,
    "paragraph_count": 3
  },
  "sentiment_analysis": {
    "sentiment": "positive",
    "confidence": 0.85,
    "reasoning": "Analysis explanation"
  },
  "keyword_analysis": {
    "keywords": ["keyword1", "keyword2"],
    "keyword_scores": [0.9, 0.8],
    "total_words": 150
  },
  "readability_analysis": {
    "readability_score": 75,
    "reading_level": "high_school",
    "avg_sentence_length": 15.2,
    "avg_word_length": 5.1
  }
}
```

## Error Handling

The application includes comprehensive error handling:
- Missing API key detection
- Fallback analysis methods when API calls fail
- JSON parsing error recovery
- File I/O error handling

## Notes

- All functions return JSON-formatted results
- Results are also printed to console for immediate feedback
- The knowledge base is automatically saved when documents are added
- Fuzzy search uses a minimum 30% similarity threshold
- Keyword extraction and sentiment analysis use AI when available, with fallback methods

