#!/usr/bin/env python3
"""
Simple test script to check Ollama connection and available models
"""

import requests
import json
import sys
import os

# Add src directory to path
sys.path.append('src')
from utils import OllamaClient, MockOllamaClient

def test_ollama_connection():
    """Test connection to Ollama and check available models"""
    print("🔍 Testing Ollama Connection...")
    
    # Test basic connection
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('models', [])
            print(f"✅ Connected to Ollama! Found {len(models)} models:")
            
            if models:
                for model in models:
                    print(f"   - {model.get('name', 'Unknown')}")
                return models[0]['name']  # Return first available model
            else:
                print("❌ No models found. You need to pull a model first!")
                print("💡 Try running in PowerShell: ollama pull llama3:8b")
                return None
        else:
            print(f"❌ HTTP {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama (connection refused)")
        print("💡 Make sure Ollama is running: ollama serve")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_model_generation(model_name):
    """Test model generation"""
    print(f"\n🧪 Testing model generation with {model_name}...")
    
    client = OllamaClient(model_name)
    response = client.generate("What is 2+2?")
    
    print("Response:", response[:100] + "..." if len(response) > 100 else response)
    
    if "Error:" in response:
        print("❌ Model generation failed")
        return False
    else:
        print("✅ Model generation successful")
        return True

def main():
    print("🏥 Ollama Connection Test for Medical Q&A Assistant\n")
    
    # Test connection
    available_model = test_ollama_connection()
    
    if available_model:
        # Test generation
        success = test_model_generation(available_model)
        
        if success:
            print(f"\n🎉 SUCCESS! You can use model: {available_model}")
            print(f"💡 Update your main.py to use: model_name='{available_model}'")
        else:
            print("\n⚠️  Connection OK but generation failed")
    else:
        print("\n🤖 Using Mock Client instead...")
        mock_client = MockOllamaClient("mock")
        response = mock_client.generate("What is 2+2?")
        print("Mock Response:", response[:100] + "..." if len(response) > 100 else response)

if __name__ == "__main__":
    main() 