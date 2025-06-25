"""
Evaluation system for measuring pipeline performance across different metrics.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
import re
import json
from dataclasses import asdict
import numpy as np
from datetime import datetime

from utils import (
    ReasoningPath, ProblemInstance, TextProcessor, ConsistencyChecker,
    calculate_similarity, FileManager
)

logger = logging.getLogger(__name__)

class PipelineEvaluator:
    """
    Comprehensive evaluator for the multi-path reasoning pipeline.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.file_manager = FileManager()
        
        # Evaluation thresholds
        self.correctness_threshold = config.get('correctness_threshold', 0.8)
        self.consistency_threshold = config.get('consistency_threshold', 0.7)
        self.confidence_threshold = config.get('confidence_threshold', 0.6)
        
        # Weights for composite scoring
        self.metric_weights = config.get('metric_weights', {
            'correctness': 0.4,
            'consistency': 0.3,
            'confidence': 0.2,
            'efficiency': 0.1
        })
    
    async def evaluate_pipeline_result(self, 
                                     problem: ProblemInstance,
                                     pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the complete result from the pipeline.
        
        Args:
            problem: The original problem instance
            pipeline_result: Result from the ToT + Self-Consistency pipeline
            
        Returns:
            Comprehensive evaluation metrics
        """
        logger.info(f"Evaluating pipeline result for problem: {problem.id}")
        
        evaluation = {
            'problem_id': problem.id,
            'task_type': problem.task_type,
            'timestamp': datetime.now().isoformat()
        }
        
        # 1. Correctness Evaluation
        correctness_eval = await self._evaluate_correctness(problem, pipeline_result)
        evaluation['correctness'] = correctness_eval
        
        # 2. Reasoning Quality Evaluation
        reasoning_eval = await self._evaluate_reasoning_quality(pipeline_result)
        evaluation['reasoning_quality'] = reasoning_eval
        
        # 3. Consistency Evaluation
        consistency_eval = await self._evaluate_consistency(pipeline_result)
        evaluation['consistency'] = consistency_eval
        
        # 4. Hallucination Detection
        hallucination_eval = await self._evaluate_hallucinations(problem, pipeline_result)
        evaluation['hallucination'] = hallucination_eval
        
        # 5. Efficiency Evaluation
        efficiency_eval = await self._evaluate_efficiency(pipeline_result)
        evaluation['efficiency'] = efficiency_eval
        
        # 6. Composite Score
        composite_score = self._calculate_composite_score(evaluation)
        evaluation['composite_score'] = composite_score
        
        # 7. Overall Assessment
        overall_assessment = self._generate_overall_assessment(evaluation)
        evaluation['overall_assessment'] = overall_assessment
        
        return evaluation
    
    async def _evaluate_correctness(self, 
                                  problem: ProblemInstance,
                                  pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the correctness of the final answer."""
        
        final_answer = pipeline_result.get('final_answer', '')
        expected_answer = problem.expected_answer
        
        if not expected_answer:
            # If no expected answer, use heuristic evaluation
            return await self._heuristic_correctness_evaluation(problem, final_answer)
        
        # Direct comparison
        exact_match = self._normalize_answer(final_answer) == self._normalize_answer(expected_answer)
        
        # Semantic similarity
        semantic_similarity = calculate_similarity(
            self._normalize_answer(final_answer),
            self._normalize_answer(expected_answer)
        )
        
        # Numerical accuracy (for math problems)
        numerical_accuracy = self._evaluate_numerical_accuracy(final_answer, expected_answer)
        
        correctness_score = 0.0
        if exact_match:
            correctness_score = 1.0
        elif semantic_similarity >= 0.9:
            correctness_score = 0.9
        elif numerical_accuracy >= 0.95:
            correctness_score = 0.8
        elif semantic_similarity >= 0.7:
            correctness_score = 0.6
        else:
            correctness_score = semantic_similarity * 0.5
        
        return {
            'score': correctness_score,
            'exact_match': exact_match,
            'semantic_similarity': semantic_similarity,
            'numerical_accuracy': numerical_accuracy,
            'final_answer': final_answer,
            'expected_answer': expected_answer
        }
    
    async def _heuristic_correctness_evaluation(self, 
                                              problem: ProblemInstance,
                                              final_answer: str) -> Dict[str, Any]:
        """Evaluate correctness using heuristics when no expected answer is available."""
        
        # Basic checks
        has_answer = bool(final_answer.strip())
        answer_length_appropriate = 5 <= len(final_answer) <= 500
        
        # Domain-specific checks
        domain_score = 0.5
        
        if problem.task_type == 'math_problems':
            domain_score = self._evaluate_math_answer_plausibility(problem.problem, final_answer)
        elif problem.task_type == 'logic_puzzles':
            domain_score = self._evaluate_logic_answer_completeness(problem.problem, final_answer)
        elif problem.task_type == 'code_debugging':
            domain_score = self._evaluate_code_answer_quality(problem.problem, final_answer)
        
        # Combine heuristics
        heuristic_score = 0.0
        if has_answer and answer_length_appropriate:
            heuristic_score = domain_score
        
        return {
            'score': heuristic_score,
            'exact_match': False,
            'heuristic_evaluation': True,
            'has_answer': has_answer,
            'answer_length_appropriate': answer_length_appropriate,
            'domain_score': domain_score,
            'final_answer': final_answer,
            'expected_answer': None
        }
    
    def _evaluate_math_answer_plausibility(self, problem: str, answer: str) -> float:
        """Evaluate if a math answer seems plausible."""
        
        # Check if answer contains numerical values
        numbers_in_answer = re.findall(r'-?\d+(?:\.\d+)?', answer)
        if not numbers_in_answer:
            return 0.2
        
        # Check for currency format if problem mentions money
        if any(word in problem.lower() for word in ['$', 'dollar', 'cost', 'price', 'revenue']):
            if '$' in answer or 'dollar' in answer.lower():
                return 0.8
            return 0.5
        
        # Check for percentage if problem mentions percentages
        if '%' in problem:
            if '%' in answer:
                return 0.8
            return 0.5
        
        return 0.6  # Default for numerical answer
    
    def _evaluate_logic_answer_completeness(self, problem: str, answer: str) -> float:
        """Evaluate if a logic puzzle answer is complete."""
        
        # Count assignations or conclusions
        assignments = len(re.findall(r'\w+\s+(?:has|is|wears|sits)', answer.lower()))
        
        # Check for definitive statements
        definitive_words = ['therefore', 'thus', 'conclusion', 'answer:', 'solution:']
        has_definitive = any(word in answer.lower() for word in definitive_words)
        
        completeness_score = 0.3
        if assignments >= 2:
            completeness_score += 0.3
        if has_definitive:
            completeness_score += 0.4
        
        return min(completeness_score, 1.0)
    
    def _evaluate_code_answer_quality(self, problem: str, answer: str) -> float:
        """Evaluate if a code debugging answer is comprehensive."""
        
        # Check for issue identification
        issue_keywords = ['bug', 'error', 'issue', 'problem', 'fix', 'correction']
        issue_mentions = sum(1 for keyword in issue_keywords if keyword in answer.lower())
        
        # Check for proposed solutions
        solution_keywords = ['should', 'need to', 'fix:', 'solution:', 'change', 'add', 'remove']
        solution_mentions = sum(1 for keyword in solution_keywords if keyword in answer.lower())
        
        # Check for code examples
        has_code = bool(re.search(r'```|def |class |if |for |while ', answer))
        
        quality_score = 0.2
        if issue_mentions >= 2:
            quality_score += 0.3
        if solution_mentions >= 1:
            quality_score += 0.3
        if has_code:
            quality_score += 0.2
        
        return min(quality_score, 1.0)
    
    async def _evaluate_reasoning_quality(self, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of reasoning across all paths."""
        
        reasoning_paths = pipeline_result.get('reasoning_paths', [])
        
        if not reasoning_paths:
            return {
                'score': 0.0,
                'path_count': 0,
                'avg_steps_per_path': 0,
                'reasoning_coherence': 0.0,
                'step_quality': 0.0
            }
        
        # Analyze each path
        path_analyses = []
        for path_data in reasoning_paths:
            steps = path_data.get('steps', [])
            
            analysis = {
                'step_count': len(steps),
                'coherence_score': self._assess_reasoning_coherence(steps),
                'step_quality_score': self._assess_step_quality(steps),
                'confidence': path_data.get('confidence', 0.5)
            }
            path_analyses.append(analysis)
        
        # Aggregate metrics
        avg_coherence = np.mean([a['coherence_score'] for a in path_analyses])
        avg_step_quality = np.mean([a['step_quality_score'] for a in path_analyses])
        avg_steps = np.mean([a['step_count'] for a in path_analyses])
        
        # Overall reasoning quality score
        reasoning_score = (avg_coherence * 0.5 + avg_step_quality * 0.5)
        
        return {
            'score': reasoning_score,
            'path_count': len(reasoning_paths),
            'avg_steps_per_path': avg_steps,
            'reasoning_coherence': avg_coherence,
            'step_quality': avg_step_quality,
            'path_analyses': path_analyses
        }
    
    def _assess_reasoning_coherence(self, steps: List[str]) -> float:
        """Assess how coherent and logical the reasoning steps are."""
        
        if not steps:
            return 0.0
        
        coherence_score = 0.0
        
        # Check for logical connectors
        connectors = ['therefore', 'thus', 'because', 'since', 'so', 'then', 'next']
        connector_count = sum(1 for step in steps 
                            for connector in connectors 
                            if connector in step.lower())
        
        coherence_score += min(connector_count / len(steps), 0.3)
        
        # Check for step progression indicators
        progression_indicators = ['step', 'first', 'second', 'next', 'finally', 'then']
        progression_count = sum(1 for step in steps 
                              for indicator in progression_indicators 
                              if indicator in step.lower())
        
        coherence_score += min(progression_count / len(steps), 0.3)
        
        # Check for consistent terminology
        # (Simple heuristic: repeated key terms indicate consistency)
        all_words = ' '.join(steps).lower().split()
        word_counts = {}
        for word in all_words:
            if len(word) > 4:  # Focus on meaningful words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        repeated_terms = sum(1 for count in word_counts.values() if count > 1)
        consistency_score = min(repeated_terms / max(len(word_counts), 1), 0.4)
        coherence_score += consistency_score
        
        return min(coherence_score, 1.0)
    
    def _assess_step_quality(self, steps: List[str]) -> float:
        """Assess the quality of individual reasoning steps."""
        
        if not steps:
            return 0.0
        
        quality_scores = []
        
        for step in steps:
            step_score = 0.0
            
            # Length appropriateness (not too short, not too long)
            length = len(step.split())
            if 5 <= length <= 50:
                step_score += 0.3
            elif 3 <= length <= 80:
                step_score += 0.2
            else:
                step_score += 0.1
            
            # Contains specific information (numbers, names, etc.)
            if re.search(r'\d+|[A-Z][a-z]+', step):
                step_score += 0.2
            
            # Contains action words (calculate, determine, find, etc.)
            action_words = ['calculate', 'determine', 'find', 'solve', 'check', 'verify', 'analyze']
            if any(word in step.lower() for word in action_words):
                step_score += 0.3
            
            # Not repetitive
            if not any(calculate_similarity(step, other_step) > 0.8 
                      for other_step in steps if other_step != step):
                step_score += 0.2
            
            quality_scores.append(min(step_score, 1.0))
        
        return np.mean(quality_scores)
    
    async def _evaluate_consistency(self, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate consistency across reasoning paths."""
        
        consistency_score = pipeline_result.get('consistency_score', 0.0)
        reasoning_paths = pipeline_result.get('reasoning_paths', [])
        
        if len(reasoning_paths) < 2:
            return {
                'score': 1.0,  # Perfect consistency with only one path
                'path_agreement': 1.0,
                'answer_consistency': 1.0,
                'reasoning_diversity': 0.0
            }
        
        # Extract answers from all paths
        answers = []
        for path_data in reasoning_paths:
            steps = path_data.get('steps', [])
            if steps:
                answer = TextProcessor.extract_final_answer(steps[-1])
                answers.append(answer)
        
        # Calculate answer consistency
        answer_consistency = ConsistencyChecker.calculate_agreement(answers)
        
        # Calculate reasoning diversity (high diversity with high consistency is good)
        reasoning_texts = []
        for path_data in reasoning_paths:
            steps = path_data.get('steps', [])
            reasoning_texts.append(' '.join(steps))
        
        diversity_scores = []
        for i in range(len(reasoning_texts)):
            for j in range(i + 1, len(reasoning_texts)):
                similarity = calculate_similarity(reasoning_texts[i], reasoning_texts[j])
                diversity_scores.append(1.0 - similarity)
        
        reasoning_diversity = np.mean(diversity_scores) if diversity_scores else 0.0
        
        # Overall consistency score
        overall_consistency = (answer_consistency * 0.7 + 
                             (1.0 - abs(reasoning_diversity - 0.5) * 2) * 0.3)  # Moderate diversity is good
        
        return {
            'score': overall_consistency,
            'path_agreement': answer_consistency,
            'answer_consistency': answer_consistency,
            'reasoning_diversity': reasoning_diversity,
            'num_paths': len(reasoning_paths)
        }
    
    async def _evaluate_hallucinations(self, 
                                     problem: ProblemInstance,
                                     pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """Detect potential hallucinations in the reasoning."""
        
        final_answer = pipeline_result.get('final_answer', '')
        reasoning_paths = pipeline_result.get('reasoning_paths', [])
        
        hallucination_indicators = []
        
        # Check for inconsistent numerical values
        problem_numbers = set(re.findall(r'\d+(?:\.\d+)?', problem.problem))
        
        for path_data in reasoning_paths:
            steps = path_data.get('steps', [])
            path_text = ' '.join(steps)
            path_numbers = set(re.findall(r'\d+(?:\.\d+)?', path_text))
            
            # Numbers that appear in reasoning but not in problem (potential hallucination)
            new_numbers = path_numbers - problem_numbers
            if len(new_numbers) > 3:  # Allow some derived numbers
                hallucination_indicators.append({
                    'type': 'excessive_new_numbers',
                    'path_id': path_data.get('id', 'unknown'),
                    'new_numbers': list(new_numbers)
                })
        
        # Check for contradictory statements within paths
        for path_data in reasoning_paths:
            steps = path_data.get('steps', [])
            contradictions = self._detect_contradictions(steps)
            if contradictions:
                hallucination_indicators.append({
                    'type': 'internal_contradiction',
                    'path_id': path_data.get('id', 'unknown'),
                    'contradictions': contradictions
                })
        
        # Check for impossible or unrealistic values (domain-specific)
        if problem.task_type == 'math_problems':
            unrealistic_values = self._detect_unrealistic_math_values(problem.problem, final_answer)
            if unrealistic_values:
                hallucination_indicators.append({
                    'type': 'unrealistic_values',
                    'values': unrealistic_values
                })
        
        # Calculate hallucination score (lower is better)
        hallucination_score = len(hallucination_indicators) / max(len(reasoning_paths), 1)
        hallucination_score = min(hallucination_score, 1.0)
        
        return {
            'score': 1.0 - hallucination_score,  # Invert so higher is better
            'hallucination_count': len(hallucination_indicators),
            'indicators': hallucination_indicators,
            'hallucination_rate': hallucination_score
        }
    
    def _detect_contradictions(self, steps: List[str]) -> List[Dict[str, str]]:
        """Detect contradictory statements within reasoning steps."""
        
        contradictions = []
        
        # Simple contradiction detection (can be enhanced)
        for i, step1 in enumerate(steps):
            for j, step2 in enumerate(steps[i+1:], i+1):
                # Look for numerical contradictions
                numbers1 = re.findall(r'\d+(?:\.\d+)?', step1)
                numbers2 = re.findall(r'\d+(?:\.\d+)?', step2)
                
                # Check if same variable has different values
                if numbers1 and numbers2:
                    # Simple heuristic: if similar sentence structure but different numbers
                    similarity = calculate_similarity(
                        re.sub(r'\d+(?:\.\d+)?', 'NUM', step1),
                        re.sub(r'\d+(?:\.\d+)?', 'NUM', step2)
                    )
                    
                    if similarity > 0.7 and numbers1 != numbers2:
                        contradictions.append({
                            'step1': step1,
                            'step2': step2,
                            'type': 'numerical_contradiction'
                        })
        
        return contradictions
    
    def _detect_unrealistic_math_values(self, problem: str, answer: str) -> List[str]:
        """Detect unrealistic mathematical values."""
        
        unrealistic_values = []
        
        # Extract numbers from answer
        answer_numbers = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', answer)]
        
        for num in answer_numbers:
            # Check for extremely large values (likely calculation errors)
            if abs(num) > 1e10:
                unrealistic_values.append(f"Extremely large value: {num}")
            
            # Check for negative values where they don't make sense
            if num < 0 and any(word in problem.lower() for word in ['cost', 'price', 'age', 'distance', 'time']):
                if 'loss' not in problem.lower() and 'debt' not in problem.lower():
                    unrealistic_values.append(f"Unexpected negative value: {num}")
        
        return unrealistic_values
    
    async def _evaluate_efficiency(self, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate computational efficiency of the pipeline."""
        
        processing_time = pipeline_result.get('processing_time', 0)
        num_paths = pipeline_result.get('num_paths_explored', 1)
        num_viable_paths = pipeline_result.get('num_viable_paths', 1)
        
        # Efficiency metrics
        time_per_path = processing_time / max(num_paths, 1)
        path_pruning_efficiency = 1.0 - (num_viable_paths / max(num_paths, 1))
        
        # Normalize processing time (assuming reasonable baseline)
        time_efficiency = max(0.0, 1.0 - (processing_time / 60.0))  # 60 seconds baseline
        
        efficiency_score = (time_efficiency * 0.4 + 
                          path_pruning_efficiency * 0.3 + 
                          (1.0 - min(time_per_path / 10.0, 1.0)) * 0.3)
        
        return {
            'score': efficiency_score,
            'processing_time': processing_time,
            'time_per_path': time_per_path,
            'path_pruning_efficiency': path_pruning_efficiency,
            'time_efficiency': time_efficiency,
            'paths_explored': num_paths,
            'viable_paths': num_viable_paths
        }
    
    def _calculate_composite_score(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate a composite score from all evaluation metrics."""
        
        # Extract scores from each evaluation category
        correctness_score = evaluation.get('correctness', {}).get('score', 0.0)
        reasoning_score = evaluation.get('reasoning_quality', {}).get('score', 0.0)
        consistency_score = evaluation.get('consistency', {}).get('score', 0.0)
        hallucination_score = evaluation.get('hallucination', {}).get('score', 0.0)
        efficiency_score = evaluation.get('efficiency', {}).get('score', 0.0)
        
        # Apply weights
        composite_score = (
            correctness_score * self.metric_weights['correctness'] +
            (reasoning_score + consistency_score + hallucination_score) / 3 * 0.3 +  # Reasoning quality aggregate
            efficiency_score * self.metric_weights['efficiency']
        )
        
        return {
            'overall_score': composite_score,
            'component_scores': {
                'correctness': correctness_score,
                'reasoning': reasoning_score,
                'consistency': consistency_score,
                'hallucination': hallucination_score,
                'efficiency': efficiency_score
            },
            'weights_used': self.metric_weights
        }
    
    def _generate_overall_assessment(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an overall qualitative assessment."""
        
        composite_score = evaluation['composite_score']['overall_score']
        
        # Performance categories
        if composite_score >= 0.9:
            performance_level = "Excellent"
            description = "Outstanding performance across all metrics"
        elif composite_score >= 0.8:
            performance_level = "Good"
            description = "Strong performance with minor areas for improvement"
        elif composite_score >= 0.7:
            performance_level = "Satisfactory"
            description = "Acceptable performance with some notable weaknesses"
        elif composite_score >= 0.6:
            performance_level = "Needs Improvement"
            description = "Below expectations, requires significant improvement"
        else:
            performance_level = "Poor"
            description = "Substantial issues across multiple metrics"
        
        # Identify strengths and weaknesses
        component_scores = evaluation['composite_score']['component_scores']
        strengths = [key for key, score in component_scores.items() if score >= 0.8]
        weaknesses = [key for key, score in component_scores.items() if score < 0.6]
        
        return {
            'performance_level': performance_level,
            'description': description,
            'overall_score': composite_score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'recommendations': self._generate_recommendations(strengths, weaknesses)
        }
    
    def _generate_recommendations(self, strengths: List[str], weaknesses: List[str]) -> List[str]:
        """Generate recommendations based on evaluation results."""
        
        recommendations = []
        
        if 'correctness' in weaknesses:
            recommendations.append("Improve prompt clarity and add verification steps")
        
        if 'reasoning' in weaknesses:
            recommendations.append("Enhance reasoning structure and step-by-step guidance")
        
        if 'consistency' in weaknesses:
            recommendations.append("Increase number of reasoning paths and improve consensus mechanisms")
        
        if 'hallucination' in weaknesses:
            recommendations.append("Add fact-checking and constraint validation steps")
        
        if 'efficiency' in weaknesses:
            recommendations.append("Optimize path pruning and reduce unnecessary computation")
        
        if not weaknesses:
            recommendations.append("Maintain current high performance standards")
        
        return recommendations
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize answer for comparison."""
        if not answer:
            return ""
        
        # Remove extra whitespace and convert to lowercase
        normalized = re.sub(r'\s+', ' ', answer.strip().lower())
        
        # Standardize number formats
        normalized = re.sub(r'\$\s*(\d+(?:\.\d+)?)', r'$\1', normalized)
        normalized = re.sub(r'(\d+)\s*%', r'\1%', normalized)
        
        return normalized
    
    def _evaluate_numerical_accuracy(self, answer1: str, answer2: str) -> float:
        """Evaluate numerical accuracy between two answers."""
        
        # Extract numbers from both answers
        nums1 = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', answer1)]
        nums2 = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', answer2)]
        
        if not nums1 or not nums2:
            return 0.0
        
        # Compare primary numbers (assume first/largest is primary)
        primary1 = max(nums1, key=abs) if nums1 else 0
        primary2 = max(nums2, key=abs) if nums2 else 0
        
        if primary2 == 0:
            return 1.0 if primary1 == 0 else 0.0
        
        # Calculate relative error
        relative_error = abs(primary1 - primary2) / abs(primary2)
        
        if relative_error <= 0.01:  # 1% error
            return 1.0
        elif relative_error <= 0.05:  # 5% error
            return 0.8
        elif relative_error <= 0.1:  # 10% error
            return 0.6
        elif relative_error <= 0.2:  # 20% error
            return 0.3
        else:
            return 0.0 