"""
Self-Consistency implementation for aggregating multiple reasoning paths
and finding consensus answers.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter, defaultdict
import re
import numpy as np
from dataclasses import asdict

from utils import ReasoningPath, TextProcessor, ConsistencyChecker, calculate_similarity

logger = logging.getLogger(__name__)

class SelfConsistencyAggregator:
    """
    Implements self-consistency for aggregating multiple reasoning paths
    to find the most reliable answer.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.consistency_threshold = config.get('consistency_threshold', 0.7)
        self.min_paths_for_consensus = config.get('min_paths_for_consensus', 2)
        self.answer_similarity_threshold = config.get('answer_similarity_threshold', 0.8)
    
    def aggregate_paths(self, paths: List[ReasoningPath]) -> Dict[str, Any]:
        """
        Aggregate multiple reasoning paths using self-consistency.
        
        Args:
            paths: List of completed reasoning paths
            
        Returns:
            Dict containing consensus answer, confidence, and analysis
        """
        logger.info(f"Aggregating {len(paths)} reasoning paths using self-consistency")
        
        if not paths:
            return {
                'consensus_answer': '',
                'confidence': 0.0,
                'consistency_score': 0.0,
                'agreement_analysis': {},
                'path_analysis': []
            }
        
        # Extract answers and analyze them
        answers = self._extract_answers_from_paths(paths)
        
        # Group similar answers
        answer_groups = self._group_similar_answers(answers)
        
        # Calculate consensus
        consensus_result = self._calculate_consensus(answer_groups, paths)
        
        # Analyze path quality and consistency
        path_analysis = self._analyze_path_consistency(paths, consensus_result['consensus_answer'])
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(
            paths, consensus_result, path_analysis
        )
        
        return {
            'consensus_answer': consensus_result['consensus_answer'],
            'confidence': overall_confidence,
            'consistency_score': consensus_result['consistency_score'],
            'agreement_analysis': consensus_result['agreement_analysis'],
            'path_analysis': path_analysis,
            'reasoning_diversity': self._calculate_reasoning_diversity(paths),
            'quality_metrics': self._calculate_quality_metrics(paths)
        }
    
    def _extract_answers_from_paths(self, paths: List[ReasoningPath]) -> List[Dict[str, Any]]:
        """Extract and normalize answers from reasoning paths."""
        answers = []
        
        for path in paths:
            if not path.steps:
                continue
            
            # Extract answer from the last step
            last_step = path.steps[-1]
            raw_answer = TextProcessor.extract_final_answer(last_step)
            
            # Normalize the answer
            normalized_answer = self._normalize_answer(raw_answer)
            
            answers.append({
                'path_id': path.id,
                'raw_answer': raw_answer,
                'normalized_answer': normalized_answer,
                'confidence': path.confidence,
                'evaluation_scores': path.evaluation_scores or {},
                'approach': path.approach
            })
        
        return answers
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize an answer for comparison."""
        if not answer:
            return ""
        
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', answer.strip())
        
        # Standardize currency formats
        normalized = re.sub(r'\$\s*(\d+(?:\.\d+)?)', r'$\1', normalized)
        
        # Standardize number formats
        normalized = re.sub(r'(\d+)\s*%', r'\1%', normalized)
        
        # Convert to lowercase for comparison (but preserve original case in final answer)
        return normalized
    
    def _group_similar_answers(self, answers: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group similar answers together."""
        groups = defaultdict(list)
        processed_indices = set()
        
        for i, answer1 in enumerate(answers):
            if i in processed_indices:
                continue
            
            # Start a new group with this answer
            group_key = answer1['normalized_answer']
            groups[group_key].append(answer1)
            processed_indices.add(i)
            
            # Find similar answers
            for j, answer2 in enumerate(answers[i+1:], i+1):
                if j in processed_indices:
                    continue
                
                similarity = calculate_similarity(
                    answer1['normalized_answer'], 
                    answer2['normalized_answer']
                )
                
                if similarity >= self.answer_similarity_threshold:
                    groups[group_key].append(answer2)
                    processed_indices.add(j)
        
        return dict(groups)
    
    def _calculate_consensus(self, answer_groups: Dict[str, List[Dict[str, Any]]], 
                           paths: List[ReasoningPath]) -> Dict[str, Any]:
        """Calculate consensus answer from grouped answers."""
        
        if not answer_groups:
            return {
                'consensus_answer': '',
                'consistency_score': 0.0,
                'agreement_analysis': {}
            }
        
        # Score each group based on size, confidence, and path quality
        group_scores = {}
        
        for group_key, group_answers in answer_groups.items():
            # Base score from group size
            size_score = len(group_answers) / len(paths)
            
            # Average confidence of answers in this group
            avg_confidence = np.mean([ans['confidence'] for ans in group_answers])
            
            # Average evaluation scores
            eval_scores = []
            for ans in group_answers:
                if ans['evaluation_scores']:
                    eval_scores.append(ans['evaluation_scores'].get('overall_score', 0.5))
            avg_eval_score = np.mean(eval_scores) if eval_scores else 0.5
            
            # Combined score
            combined_score = (size_score * 0.5 + avg_confidence * 0.3 + avg_eval_score * 0.2)
            
            group_scores[group_key] = {
                'score': combined_score,
                'count': len(group_answers),
                'avg_confidence': avg_confidence,
                'avg_eval_score': avg_eval_score,
                'answers': group_answers
            }
        
        # Find the best group
        best_group_key = max(group_scores.keys(), key=lambda k: group_scores[k]['score'])
        best_group = group_scores[best_group_key]
        
        # Use the most confident answer from the best group as consensus
        best_answer_data = max(best_group['answers'], key=lambda x: x['confidence'])
        consensus_answer = best_answer_data['raw_answer']
        
        # Calculate consistency score
        consistency_score = best_group['count'] / len(paths)
        
        # Create agreement analysis
        agreement_analysis = {
            'total_paths': len(paths),
            'consensus_group_size': best_group['count'],
            'consensus_ratio': consistency_score,
            'num_answer_groups': len(answer_groups),
            'group_breakdown': {k: v['count'] for k, v in group_scores.items()}
        }
        
        return {
            'consensus_answer': consensus_answer,
            'consistency_score': consistency_score,
            'agreement_analysis': agreement_analysis
        }
    
    def _analyze_path_consistency(self, paths: List[ReasoningPath], 
                                consensus_answer: str) -> List[Dict[str, Any]]:
        """Analyze how each path aligns with the consensus."""
        path_analysis = []
        
        for path in paths:
            if not path.steps:
                continue
            
            last_step = path.steps[-1]
            path_answer = TextProcessor.extract_final_answer(last_step)
            
            # Check alignment with consensus
            alignment_score = calculate_similarity(
                self._normalize_answer(path_answer),
                self._normalize_answer(consensus_answer)
            )
            
            # Analyze reasoning quality
            reasoning_quality = TextProcessor.assess_reasoning_quality('\n'.join(path.steps))
            
            analysis = {
                'path_id': path.id,
                'approach': path.approach,
                'answer': path_answer,
                'alignment_with_consensus': alignment_score,
                'supports_consensus': alignment_score >= self.answer_similarity_threshold,
                'confidence': path.confidence,
                'reasoning_quality': reasoning_quality,
                'evaluation_scores': path.evaluation_scores or {},
                'step_count': len(path.steps)
            }
            
            path_analysis.append(analysis)
        
        return path_analysis
    
    def _calculate_overall_confidence(self, paths: List[ReasoningPath], 
                                    consensus_result: Dict[str, Any],
                                    path_analysis: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in the consensus answer."""
        
        if not paths:
            return 0.0
        
        # Base confidence from consistency score
        consistency_confidence = consensus_result['consistency_score']
        
        # Average confidence of supporting paths
        supporting_paths = [p for p in path_analysis if p['supports_consensus']]
        if supporting_paths:
            avg_supporting_confidence = np.mean([p['confidence'] for p in supporting_paths])
        else:
            avg_supporting_confidence = 0.5
        
        # Quality factor based on evaluation scores
        quality_scores = []
        for path in paths:
            if path.evaluation_scores:
                quality_scores.append(path.evaluation_scores.get('overall_score', 0.5))
        avg_quality = np.mean(quality_scores) if quality_scores else 0.5
        
        # Reasoning diversity factor (lower is better for consistency)
        diversity = self._calculate_reasoning_diversity(paths)
        diversity_factor = max(0.5, 1.0 - diversity * 0.5)  # Penalize high diversity
        
        # Combined confidence
        overall_confidence = (
            consistency_confidence * 0.4 +
            avg_supporting_confidence * 0.3 +
            avg_quality * 0.2 +
            diversity_factor * 0.1
        )
        
        return min(overall_confidence, 1.0)
    
    def _calculate_reasoning_diversity(self, paths: List[ReasoningPath]) -> float:
        """Calculate diversity of reasoning approaches."""
        if len(paths) <= 1:
            return 0.0
        
        # Compare reasoning steps across paths
        all_steps = []
        for path in paths:
            path_text = ' '.join(path.steps).lower()
            all_steps.append(path_text)
        
        # Calculate pairwise similarities
        similarities = []
        for i in range(len(all_steps)):
            for j in range(i + 1, len(all_steps)):
                sim = calculate_similarity(all_steps[i], all_steps[j])
                similarities.append(sim)
        
        # Diversity is inverse of average similarity
        avg_similarity = np.mean(similarities) if similarities else 0.0
        return 1.0 - avg_similarity
    
    def _calculate_quality_metrics(self, paths: List[ReasoningPath]) -> Dict[str, float]:
        """Calculate overall quality metrics for the reasoning paths."""
        if not paths:
            return {}
        
        # Aggregate evaluation scores
        all_scores = defaultdict(list)
        for path in paths:
            if path.evaluation_scores:
                for key, value in path.evaluation_scores.items():
                    all_scores[key].append(value)
        
        quality_metrics = {}
        for key, values in all_scores.items():
            quality_metrics[f'avg_{key}'] = np.mean(values)
            quality_metrics[f'std_{key}'] = np.std(values)
        
        # Additional metrics
        quality_metrics['avg_confidence'] = np.mean([p.confidence for p in paths])
        quality_metrics['avg_step_count'] = np.mean([len(p.steps) for p in paths])
        quality_metrics['path_completion_rate'] = sum(1 for p in paths if p.status == 'completed') / len(paths)
        
        return quality_metrics

class MajorityVotingAggregator:
    """
    Simple majority voting aggregator for comparison with self-consistency.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def aggregate_paths(self, paths: List[ReasoningPath]) -> Dict[str, Any]:
        """Aggregate paths using simple majority voting."""
        
        if not paths:
            return {
                'consensus_answer': '',
                'confidence': 0.0,
                'vote_distribution': {}
            }
        
        # Extract answers
        answers = []
        for path in paths:
            if path.steps:
                answer = TextProcessor.extract_final_answer(path.steps[-1])
                answers.append(answer)
        
        # Count votes
        vote_counts = Counter(answers)
        
        if not vote_counts:
            return {
                'consensus_answer': '',
                'confidence': 0.0,
                'vote_distribution': {}
            }
        
        # Find majority answer
        majority_answer = vote_counts.most_common(1)[0][0]
        majority_count = vote_counts[majority_answer]
        
        # Calculate confidence as majority ratio
        confidence = majority_count / len(answers)
        
        return {
            'consensus_answer': majority_answer,
            'confidence': confidence,
            'vote_distribution': dict(vote_counts),
            'total_votes': len(answers)
        }

class WeightedAggregator:
    """
    Weighted aggregator that considers path quality and confidence.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def aggregate_paths(self, paths: List[ReasoningPath]) -> Dict[str, Any]:
        """Aggregate paths using weighted voting based on quality."""
        
        if not paths:
            return {
                'consensus_answer': '',
                'confidence': 0.0,
                'weighted_scores': {}
            }
        
        # Calculate weights for each path
        answer_weights = defaultdict(float)
        answer_details = defaultdict(list)
        
        for path in paths:
            if not path.steps:
                continue
            
            answer = TextProcessor.extract_final_answer(path.steps[-1])
            
            # Calculate weight based on confidence and evaluation scores
            weight = path.confidence
            if path.evaluation_scores:
                eval_weight = path.evaluation_scores.get('overall_score', 0.5)
                weight = (weight + eval_weight) / 2
            
            answer_weights[answer] += weight
            answer_details[answer].append({
                'path_id': path.id,
                'weight': weight,
                'confidence': path.confidence,
                'evaluation_scores': path.evaluation_scores
            })
        
        if not answer_weights:
            return {
                'consensus_answer': '',
                'confidence': 0.0,
                'weighted_scores': {}
            }
        
        # Find highest weighted answer
        consensus_answer = max(answer_weights.items(), key=lambda x: x[1])[0]
        total_weight = sum(answer_weights.values())
        consensus_weight = answer_weights[consensus_answer]
        
        confidence = consensus_weight / total_weight if total_weight > 0 else 0.0
        
        return {
            'consensus_answer': consensus_answer,
            'confidence': confidence,
            'weighted_scores': dict(answer_weights),
            'answer_details': dict(answer_details),
            'total_weight': total_weight
        } 