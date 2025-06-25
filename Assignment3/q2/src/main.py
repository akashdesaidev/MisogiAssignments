"""
Main pipeline orchestrator for the Multi-Path Reasoning + Automated Prompt Optimization system.
"""

import asyncio
import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ProblemInstance, FileManager, PerformanceTracker, generate_id
from tot_reasoning import TreeOfThoughtReasoner, MockLLMClient
from self_consistency import SelfConsistencyAggregator
from prompt_optimizer import PromptOptimizer
from evaluator import PipelineEvaluator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiPathReasoningPipeline:
    """
    Main pipeline that orchestrates Tree-of-Thought reasoning, Self-Consistency,
    and Automated Prompt Optimization.
    """
    
    def __init__(self, config: Dict[str, Any], llm_client=None):
        self.config = config
        self.llm_client = llm_client or MockLLMClient()
        self.file_manager = FileManager()
        self.performance_tracker = PerformanceTracker()
        
        # Initialize components
        self.tot_reasoner = TreeOfThoughtReasoner(self.llm_client, config)
        self.consistency_aggregator = SelfConsistencyAggregator(config)
        self.prompt_optimizer = PromptOptimizer(self.llm_client, config)
        self.evaluator = PipelineEvaluator(config)
        
        # Pipeline settings
        self.enable_optimization = config.get('enable_optimization', True)
        self.save_logs = config.get('save_logs', True)
        self.verbose = config.get('verbose', False)
    
    async def run_pipeline(self, 
                          task_type: str,
                          problems: List[Dict[str, Any]],
                          optimize_prompts: bool = True) -> Dict[str, Any]:
        """
        Run the complete pipeline on a set of problems.
        
        Args:
            task_type: Type of problems (math_problems, logic_puzzles, etc.)
            problems: List of problem dictionaries
            optimize_prompts: Whether to run prompt optimization
            
        Returns:
            Complete pipeline results including optimizations and evaluations
        """
        logger.info(f"Starting pipeline for {task_type} with {len(problems)} problems")
        
        pipeline_session_id = generate_id("pipeline_session")
        results = {
            'session_id': pipeline_session_id,
            'task_type': task_type,
            'total_problems': len(problems),
            'problem_results': [],
            'optimization_results': [],
            'performance_summary': {},
            'config_used': self.config
        }
        
        # Convert problems to ProblemInstance objects
        problem_instances = []
        for i, prob_data in enumerate(problems):
            problem = ProblemInstance(
                id=prob_data.get('id', f"{task_type}_{i}"),
                task_type=task_type,
                problem=prob_data.get('problem', ''),
                expected_answer=prob_data.get('expected_answer'),
                difficulty=prob_data.get('difficulty', 'intermediate'),
                metadata=prob_data.get('metadata', {})
            )
            problem_instances.append(problem)
        
        # Phase 1: Run initial pipeline on problems
        logger.info("Phase 1: Running initial ToT + Self-Consistency pipeline")
        initial_results = []
        
        for problem in problem_instances:
            try:
                result = await self._solve_single_problem(problem)
                initial_results.append(result)
                
                if self.verbose:
                    logger.info(f"Solved {problem.id}: {result['final_answer']}")
                    
            except Exception as e:
                logger.error(f"Error solving problem {problem.id}: {e}")
                initial_results.append({
                    'problem_id': problem.id,
                    'error': str(e),
                    'final_answer': '',
                    'confidence': 0.0
                })
        
        results['problem_results'] = initial_results
        
        # Phase 2: Evaluate initial performance
        logger.info("Phase 2: Evaluating initial performance")
        evaluations = []
        
        for problem, result in zip(problem_instances, initial_results):
            if 'error' not in result:
                try:
                    evaluation = await self.evaluator.evaluate_pipeline_result(problem, result)
                    evaluations.append(evaluation)
                except Exception as e:
                    logger.error(f"Error evaluating {problem.id}: {e}")
        
        # Update performance tracker
        for evaluation in evaluations:
            correctness = evaluation.get('correctness', {}).get('score', 0.0)
            consistency = evaluation.get('consistency', {}).get('score', 0.0)
            confidence = evaluation.get('composite_score', {}).get('overall_score', 0.0)
            
            # Simplified performance tracking
            self.performance_tracker.update_problem_result(
                correct=correctness >= 0.8,
                confidence=confidence,
                consistency=consistency,
                processing_time=1.0,  # Placeholder
                path_count=3  # Placeholder
            )
        
        # Phase 3: Prompt optimization (if enabled)
        if optimize_prompts and self.enable_optimization:
            logger.info("Phase 3: Running prompt optimization")
            
            try:
                optimization_result = await self._optimize_prompts_for_task(
                    task_type, problem_instances, evaluations
                )
                results['optimization_results'].append(optimization_result)
                
                # Phase 4: Re-run with optimized prompts
                if optimization_result.performance_improvement > 0.05:  # Significant improvement
                    logger.info("Phase 4: Re-running with optimized prompts")
                    optimized_results = await self._run_with_optimized_prompts(
                        problem_instances, optimization_result.optimized_prompt
                    )
                    results['optimized_problem_results'] = optimized_results
                    
            except Exception as e:
                logger.error(f"Error in prompt optimization: {e}")
        
        # Phase 5: Generate final performance summary
        results['performance_summary'] = self.performance_tracker.get_summary()
        results['evaluations'] = evaluations
        
        # Save results if enabled
        if self.save_logs:
            self._save_pipeline_results(results)
        
        logger.info(f"Pipeline completed. Overall accuracy: {results['performance_summary'].get('accuracy', 0.0):.2f}")
        return results
    
    async def _solve_single_problem(self, problem: ProblemInstance) -> Dict[str, Any]:
        """Solve a single problem using ToT + Self-Consistency."""
        
        # Step 1: Tree-of-Thought reasoning
        tot_result = await self.tot_reasoner.solve_problem(problem)
        
        # Step 2: Self-Consistency aggregation
        if len(tot_result.get('reasoning_paths', [])) > 1:
            from utils import ReasoningPath
            
            # Convert reasoning paths back to objects for consistency aggregation
            reasoning_paths = []
            for path_data in tot_result['reasoning_paths']:
                path = ReasoningPath(
                    id=path_data['id'],
                    problem=path_data['problem'],
                    approach=path_data['approach'],
                    steps=path_data['steps'],
                    confidence=path_data['confidence'],
                    status=path_data['status'],
                    evaluation_scores=path_data.get('evaluation_scores', {}),
                    timestamp=path_data.get('timestamp')
                )
                reasoning_paths.append(path)
            
            consistency_result = self.consistency_aggregator.aggregate_paths(reasoning_paths)
            
            # Use consensus answer if confidence is high enough
            if consistency_result['confidence'] >= self.config.get('consensus_threshold', 0.7):
                tot_result['final_answer'] = consistency_result['consensus_answer']
                tot_result['confidence'] = consistency_result['confidence']
            
            tot_result['consistency_analysis'] = consistency_result
        
        return tot_result
    
    async def _optimize_prompts_for_task(self, 
                                       task_type: str,
                                       problems: List[ProblemInstance],
                                       evaluations: List[Dict[str, Any]]) -> Any:
        """Optimize prompts based on task performance."""
        
        # Get base prompt for task type
        base_prompts = self.file_manager.load_json('prompts/base_prompts.json')
        task_prompts = base_prompts.get('task_prompts', {})
        
        if task_type not in task_prompts:
            logger.warning(f"No base prompt found for task type: {task_type}")
            return None
        
        original_prompt = task_prompts[task_type]['base']
        
        # Create evaluation function
        async def evaluate_performance(problem_dict, response):
            # Simple evaluation function for optimization
            if problem_dict.get('expected_answer'):
                expected = problem_dict['expected_answer'].lower().strip()
                actual = response.lower().strip()
                
                # Basic similarity check
                if expected in actual or actual in expected:
                    return 0.8
                elif len(set(expected.split()) & set(actual.split())) > 0:
                    return 0.5
                else:
                    return 0.2
            else:
                # Heuristic evaluation
                return 0.6 if len(response.strip()) > 20 else 0.2
        
        # Run optimization
        test_problems = [
            {
                'problem': p.problem,
                'expected_answer': p.expected_answer,
                'id': p.id
            }
            for p in problems[:5]  # Use first 5 problems for optimization
        ]
        
        optimization_result = await self.prompt_optimizer.optimize_prompt(
            original_prompt=original_prompt,
            task_type=task_type,
            test_problems=test_problems,
            evaluation_function=evaluate_performance
        )
        
        return optimization_result
    
    async def _run_with_optimized_prompts(self, 
                                        problems: List[ProblemInstance],
                                        optimized_prompt: str) -> List[Dict[str, Any]]:
        """Re-run problems with optimized prompts."""
        
        # Temporarily update the prompt in the reasoner
        # (In a real implementation, this would be more sophisticated)
        
        optimized_results = []
        for problem in problems:
            try:
                # For this demo, we'll just run the original solver
                # In practice, you'd update the prompts and re-run
                result = await self._solve_single_problem(problem)
                result['used_optimized_prompt'] = True
                optimized_results.append(result)
            except Exception as e:
                logger.error(f"Error with optimized prompt for {problem.id}: {e}")
                optimized_results.append({
                    'problem_id': problem.id,
                    'error': str(e),
                    'used_optimized_prompt': True
                })
        
        return optimized_results
    
    def _save_pipeline_results(self, results: Dict[str, Any]):
        """Save pipeline results to files."""
        
        session_id = results['session_id']
        task_type = results['task_type']
        
        # Save main results
        results_file = f"logs/performance_metrics/pipeline_results_{session_id}.json"
        self.file_manager.save_json(results, results_file)
        
        # Save performance summary
        summary_file = f"logs/performance_metrics/summary_{session_id}.json"
        summary_data = {
            'session_id': session_id,
            'task_type': task_type,
            'performance_summary': results['performance_summary'],
            'total_problems': results['total_problems']
        }
        self.file_manager.save_json(summary_data, summary_file)
        
        logger.info(f"Results saved to {results_file}")

def load_problems(task_type: str, file_manager: FileManager) -> List[Dict[str, Any]]:
    """Load problems for a specific task type."""
    
    task_files = {
        'math_problems': 'tasks/math_problems.json',
        'logic_puzzles': 'tasks/logic_puzzles.json',
        'code_debugging': 'tasks/code_debugging.json'
    }
    
    if task_type not in task_files:
        raise ValueError(f"Unknown task type: {task_type}")
    
    try:
        task_data = file_manager.load_json(task_files[task_type])
        return task_data.get('problems', [])
    except FileNotFoundError:
        logger.error(f"Task file not found: {task_files[task_type]}")
        return []

def create_default_config() -> Dict[str, Any]:
    """Create default configuration for the pipeline."""
    
    return {
        # Tree-of-Thought settings
        'num_initial_branches': 3,
        'max_depth': 5,
        'pruning_threshold': 0.3,
        'confidence_threshold': 0.7,
        'max_viable_paths': 5,
        
        # Self-Consistency settings
        'consistency_threshold': 0.7,
        'min_paths_for_consensus': 2,
        'answer_similarity_threshold': 0.8,
        'consensus_threshold': 0.7,
        
        # Optimization settings
        'enable_optimization': True,
        'max_optimization_iterations': 5,
        'optimization_population_size': 4,
        'mutation_rate': 0.7,
        'improvement_threshold': 0.05,
        
        # Evaluation settings
        'correctness_threshold': 0.8,
        'metric_weights': {
            'correctness': 0.4,
            'consistency': 0.3,
            'confidence': 0.2,
            'efficiency': 0.1
        },
        
        # General settings
        'save_logs': True,
        'verbose': False
    }

async def main():
    """Main entry point for the pipeline."""
    
    parser = argparse.ArgumentParser(description='Multi-Path Reasoning Pipeline')
    parser.add_argument('--task', choices=['math_problems', 'logic_puzzles', 'code_debugging'], 
                       default='math_problems', help='Task type to run')
    parser.add_argument('--optimize', action='store_true', help='Enable prompt optimization')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--num-problems', type=int, default=5, help='Number of problems to run')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = create_default_config()
    
    # Override config with command line arguments
    config['verbose'] = args.verbose
    config['enable_optimization'] = args.optimize
    
    # Initialize pipeline
    file_manager = FileManager()
    llm_client = MockLLMClient()  # Replace with real LLM client
    
    pipeline = MultiPathReasoningPipeline(config, llm_client)
    
    # Load problems
    try:
        all_problems = load_problems(args.task, file_manager)
        problems = all_problems[:args.num_problems]
        
        if not problems:
            logger.error(f"No problems found for task: {args.task}")
            return
        
        logger.info(f"Loaded {len(problems)} problems for {args.task}")
        
    except Exception as e:
        logger.error(f"Error loading problems: {e}")
        return
    
    # Run pipeline
    try:
        results = await pipeline.run_pipeline(
            task_type=args.task,
            problems=problems,
            optimize_prompts=args.optimize
        )
        
        # Print summary
        print("\n" + "="*50)
        print("PIPELINE RESULTS SUMMARY")
        print("="*50)
        print(f"Task Type: {args.task}")
        print(f"Problems Processed: {results['total_problems']}")
        
        performance = results.get('performance_summary', {})
        print(f"Overall Accuracy: {performance.get('accuracy', 0.0):.2%}")
        print(f"Average Confidence: {performance.get('average_confidence', 0.0):.2f}")
        print(f"Average Consistency: {performance.get('average_consistency', 0.0):.2f}")
        
        if results.get('optimization_results'):
            opt_result = results['optimization_results'][0]
            print(f"Prompt Optimization Improvement: {opt_result.performance_improvement:.3f}")
        
        print("="*50)
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 