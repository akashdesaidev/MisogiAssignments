import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from rapidfuzz import fuzz, process
import google.generativeai as genai
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

mcp =  FastMCP("My Mcp Server")

class DocumentAnalyzer:
    def __init__(self, kb_file: str = None):
        """Initialize the Document Analyzer with knowledge base"""
        if kb_file is None:
            kb_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "doc_data.json")
        
        self.kb_file = kb_file
        self.documents = self.load_knowledge_base()
        
        # Configure Google Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            print("Please set your Google API key in a .env file")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def load_knowledge_base(self) -> List[Dict]:
        """Load documents from knowledge base JSON file"""
        try:
            with open(self.kb_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('documents', [])
        except FileNotFoundError:
            print(f"Knowledge base file '{self.kb_file}' not found")
            return []
        except json.JSONDecodeError:
            print(f"Error parsing JSON from '{self.kb_file}'")
            return []
    
    def save_knowledge_base(self):
        """Save documents to knowledge base JSON file"""
        try:
            with open(self.kb_file, 'w', encoding='utf-8') as f:
                json.dump({"documents": self.documents}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    def get_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of given text using Google Gemini
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict containing sentiment analysis results
        """
        try:
            prompt = f"""
            Analyze the sentiment of the following text and provide a JSON response with:
            1. sentiment: "positive", "negative", or "neutral"
            2. confidence: a score from 0.0 to 1.0
            3. reasoning: brief explanation of the sentiment
            
            Text: "{text}"
            
            Response format:
            {{
                "sentiment": "positive/negative/neutral",
                "confidence": 0.85,
                "reasoning": "Brief explanation here"
            }}
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Try to extract JSON from response
            try:
                # Find JSON part in response
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = result_text[start:end]
                    result = json.loads(json_str)
                else:
                    # Fallback parsing
                    raise ValueError("No JSON found")
            except:
                # Fallback: simple sentiment analysis
                text_lower = text.lower()
                if any(word in text_lower for word in ['good', 'great', 'excellent', 'amazing', 'positive', 'success', 'wonderful']):
                    sentiment = "positive"
                elif any(word in text_lower for word in ['bad', 'terrible', 'awful', 'negative', 'failure', 'problem', 'issue']):
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                result = {
                    "sentiment": sentiment,
                    "confidence": 0.7,
                    "reasoning": "Fallback analysis based on keyword detection"
                }
            
            # Print to console
            print(f"Sentiment Analysis Results:")
            print(f"Text: {text[:100]}...")
            print(f"Sentiment: {result['sentiment']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Reasoning: {result['reasoning']}")
            print("-" * 50)
            
            return result
            
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "reasoning": f"Error occurred: {str(e)}"
            }
    
    def extract_keywords(self, text: str, limit: int = 10) -> Dict[str, Any]:
        """
        Extract top keywords from text using Google Gemini
        
        Args:
            text (str): Text to analyze
            limit (int): Maximum number of keywords to return
            
        Returns:
            Dict containing keyword extraction results
        """
        try:
            prompt = f"""
            Extract the top {limit} most important keywords from the following text.
            Provide a JSON response with:
            1. keywords: list of keywords
            2. keyword_scores: list of relevance scores (0.0 to 1.0) for each keyword
            3. total_words: total word count in the text
            
            Text: "{text}"
            
            Response format:
            {{
                "keywords": ["keyword1", "keyword2", "keyword3"],
                "keyword_scores": [0.9, 0.8, 0.7],
                "total_words": 150
            }}
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Try to extract JSON from response
            try:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = result_text[start:end]
                    result = json.loads(json_str)
                else:
                    raise ValueError("No JSON found")
            except:
                # Fallback: simple keyword extraction
                words = text.lower().split()
                word_freq = {}
                for word in words:
                    word = word.strip('.,!?;:"()[]{}')
                    if len(word) > 3:  # Only words longer than 3 characters
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                # Get top keywords
                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
                keywords = [word for word, _ in top_words]
                scores = [min(1.0, freq / max(word_freq.values())) for _, freq in top_words]
                
                result = {
                    "keywords": keywords,
                    "keyword_scores": scores,
                    "total_words": len(words)
                }
            
            # Print to console
            print(f"Keyword Extraction Results:")
            print(f"Text: {text[:100]}...")
            print(f"Keywords: {result['keywords']}")
            print(f"Scores: {result['keyword_scores']}")
            print(f"Total words: {result['total_words']}")
            print("-" * 50)
            
            return result
            
        except Exception as e:
            print(f"Error in keyword extraction: {e}")
            return {
                "keywords": [],
                "keyword_scores": [],
                "total_words": len(text.split())
            }
    
    def analyze_document(self, document_id: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a document
        
        Args:
            document_id (str): ID of the document to analyze
            
        Returns:
            Dict containing complete document analysis
        """
        # Find document
        doc = None
        for document in self.documents:
            if document['id'] == document_id:
                doc = document
                break
        
        if not doc:
            print(f"Document with ID '{document_id}' not found")
            return {"error": f"Document with ID '{document_id}' not found"}
        
        text = doc['content']
        
        # Perform all analyses
        sentiment_result = self.get_sentiment(text)
        keywords_result = self.extract_keywords(text, limit=10)
        
        # Basic statistics
        words = text.split()
        sentences = text.split('.')
        
        # Readability analysis using Gemini
        try:
            readability_prompt = f"""
            Analyze the readability of the following text and provide a JSON response with:
            1. readability_score: score from 0-100 (higher = more readable)
            2. reading_level: "elementary", "middle_school", "high_school", "college", "graduate"
            3. avg_sentence_length: average words per sentence
            4. avg_word_length: average characters per word
            
            Text: "{text}"
            
            Response format:
            {{
                "readability_score": 75,
                "reading_level": "high_school",
                "avg_sentence_length": 15.2,
                "avg_word_length": 5.1
            }}
            """
            
            response = self.model.generate_content(readability_prompt)
            result_text = response.text.strip()
            
            # Try to extract JSON
            try:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = result_text[start:end]
                    readability_result = json.loads(json_str)
                else:
                    raise ValueError("No JSON found")
            except:
                # Fallback readability calculation
                avg_sentence_length = len(words) / max(1, len([s for s in sentences if s.strip()]))
                avg_word_length = sum(len(word) for word in words) / len(words)
                
                readability_result = {
                    "readability_score": min(100, max(0, 100 - avg_sentence_length * 2)),
                    "reading_level": "high_school",
                    "avg_sentence_length": round(avg_sentence_length, 2),
                    "avg_word_length": round(avg_word_length, 2)
                }
                
        except Exception as e:
            print(f"Error in readability analysis: {e}")
            readability_result = {
                "readability_score": 50,
                "reading_level": "unknown",
                "avg_sentence_length": 0,
                "avg_word_length": 0
            }
        
        # Compile complete analysis
        analysis = {
            "document_id": document_id,
            "title": doc['title'],
            "metadata": doc['metadata'],
            "basic_stats": {
                "word_count": len(words),
                "sentence_count": len([s for s in sentences if s.strip()]),
                "character_count": len(text),
                "paragraph_count": len(text.split('\n\n'))
            },
            "sentiment_analysis": sentiment_result,
            "keyword_analysis": keywords_result,
            "readability_analysis": readability_result,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Print comprehensive results
        print(f"Complete Document Analysis for '{doc['title']}':")
        print(f"Document ID: {document_id}")
        print(f"Category: {doc['metadata']['category']}")
        print(f"Author: {doc['metadata']['createdby']}")
        print(f"Word Count: {analysis['basic_stats']['word_count']}")
        print(f"Sentence Count: {analysis['basic_stats']['sentence_count']}")
        print(f"Sentiment: {sentiment_result['sentiment']} (confidence: {sentiment_result['confidence']})")
        print(f"Top Keywords: {', '.join(keywords_result['keywords'][:5])}")
        print(f"Readability Score: {readability_result['readability_score']}")
        print(f"Reading Level: {readability_result['reading_level']}")
        print("=" * 60)
        
        return analysis
    
    def add_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new document to the knowledge base
        
        Args:
            document_data (Dict): Document data with title, content, and metadata
            
        Returns:
            Dict containing the added document with generated ID
        """
        # Generate new ID
        existing_ids = [doc['id'] for doc in self.documents]
        new_id = f"doc_{len(existing_ids) + 1:03d}"
        
        # Ensure no ID conflicts
        while new_id in existing_ids:
            new_id = f"doc_{len(existing_ids) + len([i for i in existing_ids if i.startswith('doc_')]) + 1:03d}"
        
        # Create new document
        new_doc = {
            "id": new_id,
            "title": document_data.get('title', 'Untitled Document'),
            "content": document_data.get('content', ''),
            "metadata": {
                "createdby": document_data.get('createdby', 'Unknown'),
                "time": datetime.now().isoformat(),
                "category": document_data.get('category', 'General'),
                "word_count": len(document_data.get('content', '').split()),
                "created_at": datetime.now().strftime('%Y-%m-%d')
            }
        }
        
        # Add to documents
        self.documents.append(new_doc)
        
        # Save to file
        self.save_knowledge_base()
        
        # Print confirmation
        print(f"Document Added Successfully:")
        print(f"ID: {new_doc['id']}")
        print(f"Title: {new_doc['title']}")
        print(f"Author: {new_doc['metadata']['createdby']}")
        print(f"Category: {new_doc['metadata']['category']}")
        print(f"Word Count: {new_doc['metadata']['word_count']}")
        print("-" * 50)
        
        return new_doc
    
    def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search documents using fuzzy text matching
        
        Args:
            query (str): Search query
            limit (int): Maximum number of results to return
            
        Returns:
            List of matching documents with similarity scores
        """
        if not query.strip():
            print("Empty query provided")
            return []
        
        results = []
        
        for doc in self.documents:
            # Calculate similarity scores for different fields
            title_score = fuzz.partial_ratio(query.lower(), doc['title'].lower())
            content_score = fuzz.partial_ratio(query.lower(), doc['content'].lower())
            category_score = fuzz.partial_ratio(query.lower(), doc['metadata']['category'].lower())
            
            # Weighted average (title and category get higher weight)
            combined_score = (title_score * 0.4 + content_score * 0.4 + category_score * 0.2)
            
            if combined_score > 30:  # Minimum similarity threshold
                results.append({
                    "document": doc,
                    "similarity_score": combined_score,
                    "match_details": {
                        "title_match": title_score,
                        "content_match": content_score,
                        "category_match": category_score
                    }
                })
        
        # Sort by similarity score
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Limit results
        results = results[:limit]
        
        # Print search results
        print(f"Search Results for '{query}':")
        print(f"Found {len(results)} matching documents")
        print("-" * 50)
        
        for i, result in enumerate(results, 1):
            doc = result['document']
            score = result['similarity_score']
            print(f"{i}. {doc['title']} (ID: {doc['id']})")
            print(f"   Category: {doc['metadata']['category']}")
            print(f"   Author: {doc['metadata']['createdby']}")
            print(f"   Similarity: {score:.1f}%")
            print(f"   Content preview: {doc['content'][:100]}...")
            print()
        
        return results

# Initialize the analyzer
analyzer = DocumentAnalyzer()

# Register MCP tools
@mcp.tool()
def analyze_document_tool(document_id: str) -> Dict[str, Any]:
    """Analyze a document by ID and return comprehensive analysis"""
    return analyzer.analyze_document(document_id)

@mcp.tool()
def get_sentiment_tool(text: str) -> Dict[str, Any]:
    """Get sentiment analysis for the provided text"""
    return analyzer.get_sentiment(text)

@mcp.tool()
def extract_keywords_tool(text: str, limit: int = 10) -> Dict[str, Any]:
    """Extract keywords from the provided text"""
    return analyzer.extract_keywords(text, limit)

@mcp.tool()
def add_document_tool(title: str, content: str, createdby: str = "Unknown", category: str = "General") -> Dict[str, Any]:
    """Add a new document to the knowledge base"""
    document_data = {
        "title": title,
        "content": content,
        "createdby": createdby,
        "category": category
    }
    return analyzer.add_document(document_data)

@mcp.tool()
def search_documents_tool(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search documents using fuzzy text matching"""
    return analyzer.search_documents(query, limit)

# Start the MCP server
if __name__ == "__main__":
    mcp.run()