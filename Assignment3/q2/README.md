# Prompt Engineering Pipeline: Multi-Path Reasoning + Automated Prompt Optimization

## 🎯 Objective
This project implements a sophisticated prompt engineering pipeline that combines:
- **Tree-of-Thought (ToT)** reasoning for multi-path exploration
- **Self-Consistency** for robust answer aggregation
- **Automated Prompt Optimization** using feedback loops

## 🏗️ Architecture

```
Pipeline Flow:
Query → ToT Reasoning → Self-Consistency → Automated Optimization → Refined Results
```

### Components:
1. **Multi-Path Reasoning**: Generate N reasoning paths using Tree-of-Thought
2. **Self-Consistency**: Aggregate answers through majority voting/consensus
3. **Automated Optimization**: OPRO/TextGrad-style prompt refinement
4. **Evaluation**: Comprehensive metrics and reflection analysis

## 📁 Project Structure

```
q2/
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── tasks/                       # Problem definitions
│   ├── math_problems.json
│   ├── logic_puzzles.json
│   ├── code_debugging.json
│   └── task_definitions.md
├── prompts/                     # Prompt templates
│   ├── base_prompts.json
│   ├── tot_prompts.json
│   ├── optimization_prompts.json
│   └── prompt_history.json
├── src/                         # Core pipeline code
│   ├── main.py                  # Main pipeline orchestrator
│   ├── tot_reasoning.py         # Tree-of-Thought implementation
│   ├── self_consistency.py     # Self-consistency aggregation
│   ├── prompt_optimizer.py     # Automated prompt optimization
│   ├── evaluator.py             # Evaluation metrics
│   └── utils.py                 # Utility functions
├── logs/                        # Execution logs
│   ├── reasoning_paths/
│   ├── optimization_history/
│   └── performance_metrics/
└── evaluation/                  # Results and analysis
    ├── metrics_report.md
    ├── reflection_analysis.md
    └── performance_data.json
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- OpenAI API key (or local LLM setup)
- Required Python packages

### Installation
```bash
cd Assignment3/q2
pip install -r requirements.txt
```

### Configuration
1. Set up your LLM API credentials in environment variables
2. Configure pipeline parameters in `src/config.py`

## 🎮 Usage

### Basic Pipeline Execution
```bash
python src/main.py --task math_problems --optimize --verbose
```

### Advanced Options
```bash
# Run with specific parameters
python src/main.py \
    --task logic_puzzles \
    --tot-paths 5 \
    --consistency-threshold 0.7 \
    --optimization-rounds 3 \
    --save-logs
```

### Available Tasks
- `math_problems`: Multi-step mathematical reasoning
- `logic_puzzles`: Logical deduction problems
- `code_debugging`: Code analysis and debugging
- `planning_tasks`: Sequential planning problems
- `causal_reasoning`: Cause-and-effect analysis

## 📊 Key Features

### Tree-of-Thought Reasoning
- Generates multiple reasoning branches
- Evaluates and prunes paths dynamically
- Maintains reasoning coherence

### Self-Consistency
- Aggregates multiple reasoning paths
- Uses majority voting and consensus mechanisms
- Handles confidence scoring

### Automated Optimization
- Detects reasoning failures and inconsistencies
- Refines prompts using feedback loops
- Tracks optimization history and performance

## 📈 Evaluation Metrics

- **Task Accuracy**: Correctness of final answers
- **Reasoning Coherence**: Quality of reasoning paths
- **Hallucination Rate**: Frequency of factual errors
- **Optimization Improvement**: Performance gains from prompt refinement
- **Consistency Score**: Agreement across reasoning paths

## 🔍 Results & Insights

See `evaluation/` directory for:
- Detailed performance analysis
- Optimization effectiveness studies
- Trade-off analysis (cost vs. quality)
- Reflection on methodology

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Tasks
1. Define task in `tasks/` directory
2. Add task-specific prompts in `prompts/`
3. Update task registry in `src/main.py`

## 📝 License
This project is part of an academic assignment and is for educational purposes. 