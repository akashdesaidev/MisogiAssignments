import numpy as np
from difflib import SequenceMatcher
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PlagiarismDetector:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)

    def compute_similarity(self, texts: list, model_type: str = "difflib"):
        if not texts or len(texts) < 2:
            raise ValueError("At least two texts are required for comparison")

        if model_type == "difflib":
            return self._compute_similarity_difflib(texts)
        elif model_type == "openai":
            return self._compute_similarity_openai(texts)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

    def _compute_similarity_difflib(self, texts: list):
        n = len(texts)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                similarity = SequenceMatcher(None, texts[i], texts[j]).ratio()
                similarity_matrix[i][j] = similarity
        
        return similarity_matrix

    def _compute_similarity_openai(self, texts: list):
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found")

        # Generate embeddings using OpenAI
        embeddings = []
        for text in texts:
            response = self.openai_client.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embeddings.append(response.data[0].embedding)

        # Convert to numpy array and compute similarity
        embeddings_array = np.array(embeddings)
        similarity_matrix = np.dot(embeddings_array, embeddings_array.T)
        
        # Normalize to [0, 1] range
        norms = np.linalg.norm(embeddings_array, axis=1)
        similarity_matrix = similarity_matrix / np.outer(norms, norms)
        
        return similarity_matrix 