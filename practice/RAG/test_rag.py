#!/usr/bin/env python3
"""
Test script for RAG implementation - demonstrates usage without requiring API key
"""

import os
import sys

def test_rag_structure():
    """Test that the RAG system can be imported and initialized"""
    try:
        from rag_implementation import RAGSystem
        print("✅ RAGSystem class imported successfully")
        
        # Test initialization (this will fail without API key, but we can test the structure)
        try:
            rag = RAGSystem("test-key")
            print("✅ RAGSystem can be instantiated")
        except Exception as e:
            print(f"⚠️  Expected error during initialization: {type(e).__name__}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import RAGSystem: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are installed"""
    required_packages = [
        'langchain',
        'langchain_openai', 
        'langchain_community',
        'chromadb',
        'openai',
        'tiktoken'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required dependencies are installed!")
    return True

def show_usage_example():
    """Show how to use the RAG system"""
    print("\n" + "="*60)
    print("📖 RAG SYSTEM USAGE EXAMPLE")
    print("="*60)
    
    example_code = '''
# 1. Set your OpenAI API key
export OPENAI_API_KEY="your-actual-api-key"

# 2. Run the main script
python rag_implementation.py

# 3. Or use it in your own code:
from rag_implementation import RAGSystem

# Initialize
rag = RAGSystem("your-api-key")

# Add documents
documents = [
    "Your document content here...",
    "More document content..."
]
rag.add_documents(documents)

# Ask questions
result = rag.query("What is the main topic?")
print(result["answer"])

# Search similar documents
similar_docs = rag.search_similar("neural networks")
for doc in similar_docs:
    print(doc["content"])
'''
    
    print(example_code)

def main():
    """Main test function"""
    print("🧪 Testing RAG Implementation")
    print("="*40)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    print("\n" + "-"*40)
    
    # Test RAG structure
    structure_ok = test_rag_structure()
    
    print("\n" + "-"*40)
    
    # Show usage example
    show_usage_example()
    
    print("\n" + "="*40)
    if deps_ok and structure_ok:
        print("✅ RAG system is ready to use!")
        print("📝 Next step: Set your OpenAI API key and run rag_implementation.py")
    else:
        print("❌ Some issues found. Please fix them before using the RAG system.")

if __name__ == "__main__":
    main() 