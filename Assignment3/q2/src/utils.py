"""
Utility functions for the multi-path reasoning pipeline.
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import hashlib
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ReasoningPath:
    """Represents a single reasoning path in the Tree-of-Thought."""
    id: str
    problem: str
    approach: str
    steps: List[str]
    confidence: float
    status: str  # 'active', 'completed', 'pruned'
    evaluation_scores: Dict[str, float] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.evaluation_scores is None:
            self.evaluation_scores = {}

@dataclass
class ProblemInstance:
    """Represents a problem to be solved."""
    id: str
    task_type: str
    problem: str
    expected_answer: Optional[str] = None
    difficulty: str = 'intermediate'
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class OptimizationResult:
    """Represents the result of prompt optimization."""
    iteration: int
    original_prompt: str
    optimized_prompt: str
    performance_improvement: float
    feedback: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class FileManager:
    """Manages file operations for the pipeline."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure all required directories exist."""
        dirs = [
            "logs/reasoning_paths",
            "logs/optimization_history", 
            "logs/performance_metrics",
            "evaluation"
        ]
        for dir_path in dirs:
            full_path = os.path.join(self.base_path, dir_path)
            os.makedirs(full_path, exist_ok=True)
    
    def save_json(self, data: Dict[str, Any], filepath: str) -> None:
        """Save data as JSON file."""
        full_path = os.path.join(self.base_path, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_json(self, filepath: str) -> Dict[str, Any]:
        """Load data from JSON file."""
        full_path = os.path.join(self.base_path, filepath)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def append_log(self, data: Dict[str, Any], log_file: str) -> None:
        """Append data to a log file."""
        full_path = os.path.join(self.base_path, log_file)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        with open(full_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data) + '\n')

class TextProcessor:
    """Processes and analyzes text for various pipeline operations."""
    
    @staticmethod
    def extract_confidence_score(text: str) -> float:
        """Extract confidence score from text."""
        # Look for patterns like "confidence: 8/10", "8 out of 10", "confidence level: 7"
        patterns = [
            r'confidence[:\s]+(\d+(?:\.\d+)?)/10',
            r'confidence[:\s]+(\d+(?:\.\d+)?)\s*out\s*of\s*10',
            r'confidence[:\s]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)/10\s*confidence',
            r'score[:\s]+(\d+(?:\.\d+)?)/10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                score = float(match.group(1))
                return min(score / 10 if score > 10 else score, 1.0)
        
        return 0.5  # Default confidence if none found
    
    @staticmethod
    def extract_final_answer(text: str) -> str:
        """Extract the final answer from reasoning text."""
        # Look for patterns like "Final answer:", "Answer:", "Result:", etc.
        patterns = [
            r'final\s+answer[:\s]+(.+?)(?:\n|$)',
            r'answer[:\s]+(.+?)(?:\n|$)',
            r'result[:\s]+(.+?)(?:\n|$)',
            r'conclusion[:\s]+(.+?)(?:\n|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1).strip()
        
        # If no explicit answer marker, return last line
        lines = text.strip().split('\n')
        return lines[-1].strip() if lines else ""
    
    @staticmethod
    def count_reasoning_steps(text: str) -> int:
        """Count the number of reasoning steps in text."""
        # Look for numbered steps, bullet points, etc.
        step_patterns = [
            r'^\d+\.',  # "1.", "2.", etc.
            r'^step\s+\d+',  # "Step 1", "Step 2", etc.
            r'^\s*[-*]\s',  # Bullet points
        ]
        
        lines = text.split('\n')
        step_count = 0
        
        for line in lines:
            for pattern in step_patterns:
                if re.match(pattern, line.strip().lower()):
                    step_count += 1
                    break
        
        return step_count
    
    @staticmethod
    def assess_reasoning_quality(text: str) -> Dict[str, float]:
        """Assess various aspects of reasoning quality."""
        return {
            'step_count': TextProcessor.count_reasoning_steps(text),
            'confidence': TextProcessor.extract_confidence_score(text),
            'length': len(text.split()),
            'complexity': len(set(text.lower().split())) / len(text.split()) if text else 0
        }

class ConsistencyChecker:
    """Checks consistency across multiple reasoning paths."""
    
    @staticmethod
    def extract_answers(paths: List[ReasoningPath]) -> List[str]:
        """Extract final answers from all paths."""
        answers = []
        for path in paths:
            if path.steps:
                # Get the last step as the final answer
                last_step = path.steps[-1]
                answer = TextProcessor.extract_final_answer(last_step)
                answers.append(answer)
        return answers
    
    @staticmethod
    def calculate_agreement(answers: List[str]) -> float:
        """Calculate agreement level among answers."""
        if not answers:
            return 0.0
        
        # Simple exact match
        unique_answers = list(set(answers))
        if len(unique_answers) == 1:
            return 1.0
        
        # Find most common answer
        answer_counts = {}
        for answer in answers:
            answer_counts[answer] = answer_counts.get(answer, 0) + 1
        
        max_count = max(answer_counts.values())
        return max_count / len(answers)
    
    @staticmethod
    def find_consensus_answer(paths: List[ReasoningPath]) -> str:
        """Find the consensus answer from multiple paths."""
        answers = ConsistencyChecker.extract_answers(paths)
        
        if not answers:
            return ""
        
        # Count occurrences
        answer_counts = {}
        for answer in answers:
            answer_counts[answer] = answer_counts.get(answer, 0) + 1
        
        # Return most common answer
        return max(answer_counts.items(), key=lambda x: x[1])[0]

class PerformanceTracker:
    """Tracks performance metrics across the pipeline."""
    
    def __init__(self):
        self.metrics = {
            'total_problems': 0,
            'correct_answers': 0,
            'average_confidence': 0.0,
            'average_consistency': 0.0,
            'optimization_improvements': [],
            'processing_times': [],
            'reasoning_path_counts': []
        }
    
    def update_problem_result(self, correct: bool, confidence: float, 
                            consistency: float, processing_time: float,
                            path_count: int):
        """Update metrics with a problem result."""
        self.metrics['total_problems'] += 1
        
        if correct:
            self.metrics['correct_answers'] += 1
        
        # Update averages
        n = self.metrics['total_problems']
        self.metrics['average_confidence'] = (
            (self.metrics['average_confidence'] * (n-1) + confidence) / n
        )
        self.metrics['average_consistency'] = (
            (self.metrics['average_consistency'] * (n-1) + consistency) / n
        )
        
        self.metrics['processing_times'].append(processing_time)
        self.metrics['reasoning_path_counts'].append(path_count)
    
    def get_accuracy(self) -> float:
        """Get current accuracy rate."""
        if self.metrics['total_problems'] == 0:
            return 0.0
        return self.metrics['correct_answers'] / self.metrics['total_problems']
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        return {
            'accuracy': self.get_accuracy(),
            'total_problems': self.metrics['total_problems'],
            'average_confidence': self.metrics['average_confidence'],
            'average_consistency': self.metrics['average_consistency'],
            'average_processing_time': sum(self.metrics['processing_times']) / len(self.metrics['processing_times']) if self.metrics['processing_times'] else 0,
            'average_path_count': sum(self.metrics['reasoning_path_counts']) / len(self.metrics['reasoning_path_counts']) if self.metrics['reasoning_path_counts'] else 0
        }

def generate_id(prefix: str = "", content: str = "") -> str:
    """Generate a unique ID for various pipeline components."""
    timestamp = str(int(time.time() * 1000))
    if content:
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{prefix}_{timestamp}_{content_hash}"
    else:
        return f"{prefix}_{timestamp}"

def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with given parameters."""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        logger.warning(f"Missing key in prompt formatting: {e}")
        return template

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts (simple word overlap)."""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0 