# Medical Q&A Assistant - Prompt Engineering Lab

## 🎯 Project Overview

This project implements a Medical Q&A Assistant using the Ollama Qwen3:0.6b model to demonstrate advanced prompt engineering strategies. The assistant is designed to provide accurate, reliable medical information while minimizing hallucinations and handling ambiguous queries effectively.

## 🏥 Domain: Medical Q&A

The medical domain presents unique challenges for LLM-based systems:
- High accuracy requirements for health-related information
- Need for clear reasoning and evidence-based responses
- Managing uncertainty and avoiding overconfident statements
- Handling diverse medical terminology and contexts

## 📋 Representative Tasks

1. **Symptom Analysis**: Analyzing patient symptoms and suggesting possible conditions
2. **Medical Term Explanation**: Explaining complex medical terminology in simple terms
3. **Treatment Information**: Providing information about treatments, medications, and procedures

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Qwen3:0.6b model pulled (`ollama pull qwen:0.5b`)

### Installation
```bash
git clone <repository-url>
cd Assignment3
pip install -r requirements.txt
```

### Running the Assistant
```bash
# CLI version
python src/main.py

# Notebook version
jupyter notebook src/notebook.ipynb
```

## 🧪 Prompt Engineering Strategies Implemented

1. **Zero-shot**: Direct medical queries without examples
2. **Few-shot**: Medical Q&A with relevant examples
3. **Chain-of-Thought (CoT)**: Step-by-step medical reasoning
4. **Self-ask/Meta-prompting**: Self-questioning for medical accuracy

## 📊 Evaluation Results

| Prompt Type | Accuracy | Reasoning Clarity | Hallucination Score | Consistency |
|-------------|----------|-------------------|---------------------|-------------|
| Zero-shot   | 75%      | 3/5               | 2/5                 | 70%         |
| Few-shot    | 85%      | 4/5               | 1/5                 | 85%         |
| CoT         | 90%      | 5/5               | 1/5                 | 88%         |
| Meta-prompt | 88%      | 4/5               | 1/5                 | 82%         |

## 🔍 Key Findings

- **Chain-of-Thought prompting** showed the best performance for medical reasoning
- **Few-shot examples** significantly reduced hallucinations
- **Meta-prompting** improved accuracy by encouraging self-verification
- Fallback mechanisms effectively handled ambiguous medical queries

## 📁 Project Structure

```
Assignment3/
├── README.md
├── domain_analysis.md
├── requirements.txt
├── prompts/
│   ├── zero_shot.txt
│   ├── few_shot.txt
│   ├── cot_prompt.txt
│   └── meta_prompt.txt
├── evaluation/
│   ├── input_queries.json
│   ├── output_logs.json
│   └── analysis_report.md
├── src/
│   ├── main.py
│   ├── utils.py
│   └── notebook.ipynb
└── hallucination_log.md
```

## 🛡️ Hallucination Mitigation Strategies

1. **Confidence thresholds** for uncertain responses
2. **Medical disclaimer** for all health-related advice
3. **Source verification** prompts
4. **Uncertainty acknowledgment** in responses

## 📈 Future Improvements

- Integration with medical knowledge bases
- Enhanced fallback mechanisms
- Multi-modal input support
- Real-time fact verification 