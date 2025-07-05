from flask import Flask, request, jsonify, send_from_directory
import os
from services.plagiarism_detector import PlagiarismDetector

app = Flask(__name__, static_folder='static')
plagiarism_detector = PlagiarismDetector()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_texts():
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        model_type = data.get('model_type', 'sentence-transformers')

        if not texts or len(texts) < 2:
            return jsonify({'error': 'At least two texts are required'}), 400

        # Get similarity matrix using specified model
        similarity_matrix = plagiarism_detector.compute_similarity(texts, model_type)
        
        # Find potential plagiarism (similarity > 80%)
        plagiarism_pairs = []
        for i in range(len(similarity_matrix)):
            for j in range(i + 1, len(similarity_matrix)):
                if similarity_matrix[i][j] > 0.8:  # 80% threshold
                    plagiarism_pairs.append({
                        'text1_index': i,
                        'text2_index': j,
                        'similarity': float(similarity_matrix[i][j])
                    })

        return jsonify({
            'similarity_matrix': similarity_matrix.tolist(),
            'plagiarism_detected': plagiarism_pairs,
            'model_used': model_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 