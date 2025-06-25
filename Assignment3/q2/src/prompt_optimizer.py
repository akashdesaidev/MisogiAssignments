"""
Automated Prompt Optimization using feedback loops similar to OPRO/TextGrad.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
import json
import numpy as np
from dataclasses import asdict, dataclass
import re

from utils import OptimizationResult, FileManager, format_prompt, generate_id, calculate_similarity

logger = logging.getLogger(__name__)

@dataclass
class PromptCandidate:
    """Represents a candidate prompt during optimization."""
    id: str
    prompt: str
    performance_score: float
    feedback: str
    iteration: int
    parent_id: Optional[str] = None
    mutation_type: str = ""

class PromptOptimizer:
    """
    Automated prompt optimization system that iteratively improves prompts
    based on performance feedback.
    """
    
    def __init__(self, llm_client, config: Dict[str, Any]):
        self.llm_client = llm_client
        self.config = config
        self.file_manager = FileManager()
        
        # Optimization parameters
        self.max_iterations = config.get('max_optimization_iterations', 5)
        self.population_size = config.get('optimization_population_size', 4)
        self.mutation_rate = config.get('mutation_rate', 0.7)
        self.improvement_threshold = config.get('improvement_threshold', 0.05)
        
        # Load optimization prompts
        self.optimization_prompts = self._load_optimization_prompts()
        
        # Track optimization history
        self.optimization_history = []
    
    def _load_optimization_prompts(self) -> Dict[str, str]:
        """Load prompts for the optimization process itself."""
        try:
            prompts = self.file_manager.load_json('prompts/optimization_prompts.json')
            return prompts
        except FileNotFoundError:
            # Return default optimization prompts
            return {
                'analyze_failures': """Analyze these failed reasoning attempts and identify what went wrong:

Problem: {problem}

Failed attempts:
{failed_attempts}

For each failure, identify:
1. What specific aspect caused the failure?
2. What information was missing or incorrectly processed?
3. What reasoning errors were made?
4. How could the prompt be improved to avoid this failure?

Provide specific, actionable feedback for prompt improvement.""",

                'improve_prompt': """You are a prompt optimization expert. Improve this prompt based on the feedback provided.

Original prompt:
{original_prompt}

Performance feedback:
{feedback}

Common failure patterns:
{failure_patterns}

Task: Create an improved version of the prompt that addresses the identified issues.

Requirements:
1. Keep the core structure and intent
2. Add specific guidance to avoid identified failures
3. Include examples if they would help
4. Ensure clarity and specificity
5. Maintain appropriate length (not too verbose)

Improved prompt:""",

                'evaluate_improvement': """Evaluate whether this prompt improvement is likely to be effective:

Original prompt:
{original_prompt}

Improved prompt:
{improved_prompt}

Improvement reasoning:
{improvement_reasoning}

Rate the improvement on a scale of 1-10 considering:
1. How well it addresses identified issues
2. Clarity and specificity
3. Likelihood to improve performance
4. Potential for new issues

Score: [1-10]
Reasoning:"""
            }
    
    async def optimize_prompt(self, 
                            original_prompt: str,
                            task_type: str,
                            test_problems: List[Dict[str, Any]],
                            evaluation_function) -> OptimizationResult:
        """
        Optimize a prompt through iterative feedback and improvement.
        
        Args:
            original_prompt: The initial prompt to optimize
            task_type: Type of task (math_problems, logic_puzzles, etc.)
            test_problems: Problems to test prompt performance
            evaluation_function: Function to evaluate prompt performance
            
        Returns:
            OptimizationResult with the best prompt and performance data
        """
        logger.info(f"Starting prompt optimization for {task_type}")
        
        # Initialize optimization tracking
        best_prompt = original_prompt
        best_score = await self._evaluate_prompt_performance(
            original_prompt, test_problems, evaluation_function
        )
        
        optimization_log = {
            'task_type': task_type,
            'original_prompt': original_prompt,
            'original_score': best_score,
            'iterations': []
        }
        
        # Initialize population with original prompt
        population = [PromptCandidate(
            id=generate_id("prompt"),
            prompt=original_prompt,
            performance_score=best_score,
            feedback="Original baseline prompt",
            iteration=0
        )]
        
        # Optimization loop
        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"Optimization iteration {iteration}")
            
            # Analyze failures from current population
            failure_analysis = await self._analyze_current_failures(
                population, test_problems, evaluation_function
            )
            
            # Generate new prompt candidates
            new_candidates = await self._generate_prompt_candidates(
                population, failure_analysis, iteration
            )
            
            # Evaluate new candidates
            evaluated_candidates = []
            for candidate in new_candidates:
                score = await self._evaluate_prompt_performance(
                    candidate.prompt, test_problems, evaluation_function
                )
                candidate.performance_score = score
                evaluated_candidates.append(candidate)
            
            # Update population (keep best performers)
            combined_population = population + evaluated_candidates
            combined_population.sort(key=lambda x: x.performance_score, reverse=True)
            population = combined_population[:self.population_size]
            
            # Check for improvement
            current_best_score = population[0].performance_score
            improvement = current_best_score - best_score
            
            iteration_log = {
                'iteration': iteration,
                'best_score': current_best_score,
                'improvement': improvement,
                'new_candidates': len(new_candidates),
                'failure_analysis': failure_analysis
            }
            optimization_log['iterations'].append(iteration_log)
            
            # Update best if improved
            if current_best_score > best_score:
                best_score = current_best_score
                best_prompt = population[0].prompt
                logger.info(f"New best score: {best_score:.3f} (improvement: {improvement:.3f})")
            
            # Early stopping if improvement is minimal
            if iteration > 1 and improvement < self.improvement_threshold:
                logger.info(f"Early stopping - improvement below threshold")
                break
        
        # Log optimization results
        self._log_optimization_results(optimization_log)
        
        final_improvement = best_score - optimization_log['original_score']
        
        return OptimizationResult(
            iteration=len(optimization_log['iterations']),
            original_prompt=original_prompt,
            optimized_prompt=best_prompt,
            performance_improvement=final_improvement,
            feedback=json.dumps(optimization_log, indent=2)
        )
    
    async def _evaluate_prompt_performance(self, 
                                         prompt: str,
                                         test_problems: List[Dict[str, Any]],
                                         evaluation_function) -> float:
        """Evaluate how well a prompt performs on test problems."""
        
        if not test_problems:
            return 0.0
        
        scores = []
        
        for problem in test_problems:
            try:
                # Use the prompt to solve the problem
                formatted_prompt = format_prompt(prompt, problem=problem.get('problem', ''))
                response = await self._call_llm(formatted_prompt)
                
                # Evaluate the response
                score = await evaluation_function(problem, response)
                scores.append(score)
                
            except Exception as e:
                logger.warning(f"Error evaluating problem: {e}")
                scores.append(0.0)
        
        return np.mean(scores) if scores else 0.0
    
    async def _analyze_current_failures(self, 
                                      population: List[PromptCandidate],
                                      test_problems: List[Dict[str, Any]],
                                      evaluation_function) -> Dict[str, Any]:
        """Analyze failure patterns in current prompt population."""
        
        failure_examples = []
        
        # Test current best prompt on problems
        best_prompt = population[0].prompt
        
        for problem in test_problems[:3]:  # Analyze a few examples
            try:
                formatted_prompt = format_prompt(best_prompt, problem=problem.get('problem', ''))
                response = await self._call_llm(formatted_prompt)
                score = await evaluation_function(problem, response)
                
                if score < 0.7:  # Consider this a failure
                    failure_examples.append({
                        'problem': problem.get('problem', ''),
                        'response': response,
                        'score': score,
                        'expected': problem.get('expected_answer', 'Unknown')
                    })
                    
            except Exception as e:
                logger.warning(f"Error in failure analysis: {e}")
        
        # Analyze failure patterns using LLM
        if failure_examples:
            failure_text = "\n\n".join([
                f"Problem: {ex['problem']}\nResponse: {ex['response']}\nScore: {ex['score']}\nExpected: {ex['expected']}"
                for ex in failure_examples
            ])
            
            analysis_prompt = format_prompt(
                self.optimization_prompts['analyze_failures'],
                problem="Multiple reasoning problems",
                failed_attempts=failure_text
            )
            
            analysis_response = await self._call_llm(analysis_prompt)
            
            return {
                'failure_count': len(failure_examples),
                'failure_examples': failure_examples,
                'analysis_response': analysis_response
            }
        
        return {
            'failure_count': 0,
            'failure_examples': [],
            'analysis_response': "No significant failures detected"
        }
    
    async def _generate_prompt_candidates(self, 
                                        population: List[PromptCandidate],
                                        failure_analysis: Dict[str, Any],
                                        iteration: int) -> List[PromptCandidate]:
        """Generate new prompt candidates based on current population and failure analysis."""
        
        candidates = []
        best_prompt = population[0].prompt
        
        # Strategy 1: Direct improvement based on failure analysis
        if failure_analysis['failure_count'] > 0:
            improvement_prompt = format_prompt(
                self.optimization_prompts['improve_prompt'],
                original_prompt=best_prompt,
                feedback=failure_analysis['analysis_response'],
                failure_patterns=str(failure_analysis['failure_examples'])
            )
            
            improved_prompt = await self._call_llm(improvement_prompt)
            
            candidates.append(PromptCandidate(
                id=generate_id("prompt"),
                prompt=improved_prompt,
                performance_score=0.0,  # Will be evaluated later
                feedback="Improved based on failure analysis",
                iteration=iteration,
                parent_id=population[0].id,
                mutation_type="failure_based_improvement"
            ))
        
        # Strategy 2: Add specificity and examples
        specificity_improvements = [
            "Add more specific step-by-step instructions",
            "Include concrete examples of good reasoning",
            "Add explicit error-checking steps",
            "Emphasize verification of final answers"
        ]
        
        for improvement in specificity_improvements[:2]:  # Limit candidates
            mutation_prompt = f"""Improve this prompt by: {improvement}

Original prompt:
{best_prompt}

Enhanced prompt:"""
            
            mutated_prompt = await self._call_llm(mutation_prompt)
            
            candidates.append(PromptCandidate(
                id=generate_id("prompt"),
                prompt=mutated_prompt,
                performance_score=0.0,
                feedback=f"Mutation: {improvement}",
                iteration=iteration,
                parent_id=population[0].id,
                mutation_type="specificity_enhancement"
            ))
        
        # Strategy 3: Crossover between top performers (if we have multiple)
        if len(population) >= 2:
            crossover_prompt = f"""Create a new prompt that combines the best aspects of these two approaches:

Prompt A:
{population[0].prompt}

Prompt B:
{population[1].prompt}

Combined prompt that takes the strengths of both:"""
            
            crossover_result = await self._call_llm(crossover_prompt)
            
            candidates.append(PromptCandidate(
                id=generate_id("prompt"),
                prompt=crossover_result,
                performance_score=0.0,
                feedback="Crossover of top two performers",
                iteration=iteration,
                parent_id=f"{population[0].id}+{population[1].id}",
                mutation_type="crossover"
            ))
        
        return candidates
    
    def _log_optimization_results(self, optimization_log: Dict[str, Any]):
        """Log the optimization results for analysis."""
        
        log_file = f"logs/optimization_history/optimization_{generate_id()}.json"
        self.file_manager.save_json(optimization_log, log_file)
        
        # Also append to summary log
        summary = {
            'task_type': optimization_log['task_type'],
            'original_score': optimization_log['original_score'],
            'final_score': optimization_log['iterations'][-1]['best_score'] if optimization_log['iterations'] else optimization_log['original_score'],
            'improvement': optimization_log['iterations'][-1]['best_score'] - optimization_log['original_score'] if optimization_log['iterations'] else 0,
            'iterations_run': len(optimization_log['iterations']),
            'timestamp': generate_id("opt")
        }
        
        self.file_manager.append_log(summary, 'logs/optimization_history/summary.jsonl')
    
    async def _call_llm(self, prompt: str, system_prompt: str = "") -> str:
        """Make a call to the LLM for optimization tasks."""
        try:
            if hasattr(self.llm_client, 'chat_completion'):
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await self.llm_client.chat_completion(messages)
                return response.get('content', '')
            else:
                return await self.llm_client.complete(prompt)
                
        except Exception as e:
            logger.error(f"LLM call failed in optimization: {e}")
            return f"Error: Could not get LLM response - {str(e)}"

class PerformanceBasedOptimizer:
    """
    Simplified optimizer that focuses on performance metrics only.
    """
    
    def __init__(self, llm_client, config: Dict[str, Any]):
        self.llm_client = llm_client
        self.config = config
        self.file_manager = FileManager()
    
    async def optimize_for_metric(self, 
                                original_prompt: str,
                                target_metric: str,
                                test_problems: List[Dict[str, Any]],
                                evaluation_function) -> str:
        """Optimize a prompt to improve a specific metric."""
        
        # Simple A/B testing approach
        variations = await self._generate_metric_focused_variations(
            original_prompt, target_metric
        )
        
        best_prompt = original_prompt
        best_score = 0.0
        
        for variation in variations:
            score = await self._evaluate_prompt_performance(
                variation, test_problems, evaluation_function
            )
            
            if score > best_score:
                best_score = score
                best_prompt = variation
        
        return best_prompt
    
    async def _generate_metric_focused_variations(self, 
                                                original_prompt: str,
                                                target_metric: str) -> List[str]:
        """Generate prompt variations focused on improving a specific metric."""
        
        optimization_strategies = {
            'accuracy': [
                "Add explicit verification steps",
                "Include error-checking instructions",
                "Emphasize careful calculation"
            ],
            'consistency': [
                "Add standardized output format",
                "Include systematic approach instructions",
                "Emphasize consistent reasoning patterns"
            ],
            'confidence': [
                "Add confidence assessment instructions",
                "Include uncertainty acknowledgment",
                "Emphasize self-evaluation steps"
            ]
        }
        
        strategies = optimization_strategies.get(target_metric, ["Add more detailed instructions"])
        variations = []
        
        for strategy in strategies:
            variation_prompt = f"""Modify this prompt to improve {target_metric} by: {strategy}

Original prompt:
{original_prompt}

Modified prompt:"""
            
            try:
                variation = await self._call_llm(variation_prompt)
                variations.append(variation)
            except Exception as e:
                logger.warning(f"Failed to generate variation: {e}")
        
        return variations
    
    async def _evaluate_prompt_performance(self, 
                                         prompt: str,
                                         test_problems: List[Dict[str, Any]],
                                         evaluation_function) -> float:
        """Evaluate prompt performance (simplified version)."""
        
        if not test_problems:
            return 0.0
        
        # Sample a few problems for quick evaluation
        sample_problems = test_problems[:min(3, len(test_problems))]
        scores = []
        
        for problem in sample_problems:
            try:
                formatted_prompt = format_prompt(prompt, problem=problem.get('problem', ''))
                response = await self._call_llm(formatted_prompt)
                score = await evaluation_function(problem, response)
                scores.append(score)
            except Exception as e:
                logger.warning(f"Evaluation error: {e}")
                scores.append(0.0)
        
        return np.mean(scores) if scores else 0.0
    
    async def _call_llm(self, prompt: str) -> str:
        """Make LLM call for optimization."""
        try:
            if hasattr(self.llm_client, 'chat_completion'):
                messages = [{"role": "user", "content": prompt}]
                response = await self.llm_client.chat_completion(messages)
                return response.get('content', '')
            else:
                return await self.llm_client.complete(prompt)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return "" 