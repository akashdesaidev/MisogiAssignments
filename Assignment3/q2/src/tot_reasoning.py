"""
Tree-of-Thought reasoning implementation for multi-path problem solving.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import asdict
import random

from utils import (
    ReasoningPath, ProblemInstance, FileManager, TextProcessor, 
    generate_id, format_prompt, PerformanceTracker
)

logger = logging.getLogger(__name__)

class TreeOfThoughtReasoner:
    """
    Implements Tree-of-Thought reasoning with branch generation,
    path evaluation, pruning, and synthesis.
    """
    
    def __init__(self, llm_client, config: Dict[str, Any]):
        self.llm_client = llm_client
        self.config = config
        self.file_manager = FileManager()
        self.performance_tracker = PerformanceTracker()
        
        # Load prompts
        self.prompts = self._load_prompts()
        
        # Configuration parameters
        self.num_initial_branches = config.get('num_initial_branches', 3)
        self.max_depth = config.get('max_depth', 5)
        self.pruning_threshold = config.get('pruning_threshold', 0.3)
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompt templates."""
        try:
            base_prompts = self.file_manager.load_json('prompts/base_prompts.json')
            tot_prompts = self.file_manager.load_json('prompts/tot_prompts.json')
            return {**base_prompts, **tot_prompts}
        except FileNotFoundError as e:
            logger.error(f"Could not load prompts: {e}")
            return {}
    
    async def solve_problem(self, problem: ProblemInstance) -> Dict[str, Any]:
        """
        Solve a problem using Tree-of-Thought reasoning.
        
        Args:
            problem: The problem instance to solve
            
        Returns:
            Dict containing solution, reasoning paths, and metadata
        """
        logger.info(f"Starting ToT reasoning for problem: {problem.id}")
        
        start_time = asyncio.get_event_loop().time()
        
        # Step 1: Generate initial reasoning branches
        initial_paths = await self._generate_initial_branches(problem)
        
        # Step 2: Expand and evaluate paths iteratively
        expanded_paths = await self._expand_and_evaluate_paths(problem, initial_paths)
        
        # Step 3: Prune low-quality paths
        viable_paths = await self._prune_paths(problem, expanded_paths)
        
        # Step 4: Synthesize final solution
        final_solution = await self._synthesize_solution(problem, viable_paths)
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        # Log the reasoning session
        self._log_reasoning_session(problem, viable_paths, final_solution, processing_time)
        
        return {
            'problem_id': problem.id,
            'final_answer': final_solution['answer'],
            'confidence': final_solution['confidence'],
            'reasoning_paths': [asdict(path) for path in viable_paths],
            'synthesis_reasoning': final_solution['reasoning'],
            'processing_time': processing_time,
            'num_paths_explored': len(expanded_paths),
            'num_viable_paths': len(viable_paths)
        }
    
    async def _generate_initial_branches(self, problem: ProblemInstance) -> List[ReasoningPath]:
        """Generate initial reasoning branches for the problem."""
        logger.info(f"Generating {self.num_initial_branches} initial branches")
        
        # Get the appropriate prompt template
        task_type = problem.task_type
        if task_type in self.prompts.get('task_prompts', {}):
            base_prompt = self.prompts['task_prompts'][task_type]['base']
        else:
            base_prompt = "Solve this problem step by step: {problem}"
        
        # Generate branch generation prompt
        branch_prompt = self.prompts.get('tree_of_thought_prompts', {}).get('branch_generation', {}).get('user_template', '')
        
        if branch_prompt:
            prompt = format_prompt(
                branch_prompt,
                num_branches=self.num_initial_branches,
                problem=problem.problem
            )
        else:
            prompt = format_prompt(base_prompt, problem=problem.problem)
        
        # Get LLM response
        response = await self._call_llm(prompt, system_prompt=self.prompts.get('system_prompt', ''))
        
        # Parse response into separate reasoning paths
        branches = self._parse_branches_response(response, problem)
        
        logger.info(f"Generated {len(branches)} initial branches")
        return branches
    
    async def _expand_and_evaluate_paths(self, problem: ProblemInstance, 
                                       initial_paths: List[ReasoningPath]) -> List[ReasoningPath]:
        """Expand reasoning paths and evaluate their quality."""
        logger.info("Expanding and evaluating reasoning paths")
        
        expanded_paths = []
        
        for path in initial_paths:
            if path.status == 'active':
                # Expand this path
                expanded_path = await self._expand_path(problem, path)
                
                # Evaluate the expanded path
                evaluation = await self._evaluate_path(problem, expanded_path)
                expanded_path.evaluation_scores = evaluation
                
                # Update path status based on evaluation
                if evaluation.get('overall_score', 0) >= self.confidence_threshold:
                    expanded_path.status = 'completed'
                elif evaluation.get('overall_score', 0) >= self.pruning_threshold:
                    expanded_path.status = 'active'
                else:
                    expanded_path.status = 'pruned'
                
                expanded_paths.append(expanded_path)
        
        return expanded_paths
    
    async def _expand_path(self, problem: ProblemInstance, path: ReasoningPath) -> ReasoningPath:
        """Expand a single reasoning path with additional steps."""
        
        # Create expansion prompt
        expansion_prompt = self.prompts.get('tree_of_thought_prompts', {}).get('path_expansion', {}).get('user_template', '')
        
        if expansion_prompt:
            current_path_text = "\n".join(path.steps)
            prompt = format_prompt(
                expansion_prompt,
                problem=problem.problem,
                current_path=current_path_text
            )
        else:
            # Fallback expansion approach
            prompt = f"Continue solving this problem from where we left off:\n\nProblem: {problem.problem}\n\nCurrent progress:\n" + "\n".join(path.steps) + "\n\nNext steps:"
        
        response = await self._call_llm(prompt)
        
        # Parse additional steps from response
        new_steps = self._parse_expansion_response(response)
        
        # Create expanded path
        expanded_path = ReasoningPath(
            id=generate_id("path", problem.problem),
            problem=problem.problem,
            approach=path.approach,
            steps=path.steps + new_steps,
            confidence=path.confidence,
            status=path.status
        )
        
        return expanded_path
    
    async def _evaluate_path(self, problem: ProblemInstance, path: ReasoningPath) -> Dict[str, float]:
        """Evaluate the quality of a reasoning path."""
        
        # Get evaluation prompt
        eval_prompt = self.prompts.get('tree_of_thought_prompts', {}).get('path_evaluation', {}).get('user_template', '')
        
        if eval_prompt:
            path_text = "\n".join(path.steps)
            prompt = format_prompt(
                eval_prompt,
                problem=problem.problem,
                path=path_text
            )
        else:
            # Fallback evaluation
            path_text = "\n".join(path.steps)
            prompt = f"Evaluate this solution approach:\n\nProblem: {problem.problem}\n\nSolution: {path_text}\n\nRate on scale 1-10 for correctness, completeness, efficiency, clarity."
        
        response = await self._call_llm(prompt)
        
        # Parse evaluation scores
        scores = self._parse_evaluation_response(response)
        
        # Calculate overall score
        weights = {
            'correctness': 0.4,
            'completeness': 0.3,
            'efficiency': 0.2,
            'clarity': 0.1
        }
        
        overall_score = sum(scores.get(key, 5.0) * weight for key, weight in weights.items()) / 10.0
        scores['overall_score'] = overall_score
        
        return scores
    
    async def _prune_paths(self, problem: ProblemInstance, paths: List[ReasoningPath]) -> List[ReasoningPath]:
        """Prune low-quality reasoning paths."""
        logger.info(f"Pruning paths from {len(paths)} candidates")
        
        # Filter out pruned paths
        viable_paths = [path for path in paths if path.status != 'pruned']
        
        # If we have too many viable paths, keep only the best ones
        max_paths = self.config.get('max_viable_paths', 5)
        if len(viable_paths) > max_paths:
            # Sort by overall evaluation score
            viable_paths.sort(key=lambda p: p.evaluation_scores.get('overall_score', 0), reverse=True)
            viable_paths = viable_paths[:max_paths]
            
            # Mark the rest as pruned
            for path in viable_paths[max_paths:]:
                path.status = 'pruned'
        
        logger.info(f"Kept {len(viable_paths)} viable paths after pruning")
        return viable_paths
    
    async def _synthesize_solution(self, problem: ProblemInstance, 
                                 paths: List[ReasoningPath]) -> Dict[str, Any]:
        """Synthesize final solution from multiple reasoning paths."""
        logger.info("Synthesizing final solution from viable paths")
        
        if not paths:
            return {
                'answer': 'No viable solution found',
                'confidence': 0.0,
                'reasoning': 'All reasoning paths were pruned due to low quality'
            }
        
        # Get synthesis prompt
        synthesis_prompt = self.prompts.get('tree_of_thought_prompts', {}).get('synthesis', {}).get('user_template', '')
        
        if synthesis_prompt:
            paths_text = ""
            for i, path in enumerate(paths, 1):
                paths_text += f"\nPath {i} ({path.approach}):\n" + "\n".join(path.steps) + "\n"
            
            prompt = format_prompt(
                synthesis_prompt,
                problem=problem.problem,
                paths=paths_text
            )
        else:
            # Fallback synthesis
            paths_text = ""
            for i, path in enumerate(paths, 1):
                paths_text += f"\n\nApproach {i}: {path.approach}\n" + "\n".join(path.steps)
            
            prompt = f"Synthesize the best solution from these approaches:\n\nProblem: {problem.problem}\n\nApproaches:{paths_text}\n\nFinal answer:"
        
        response = await self._call_llm(prompt)
        
        # Parse synthesis response
        synthesis_result = self._parse_synthesis_response(response)
        
        return synthesis_result
    
    def _parse_branches_response(self, response: str, problem: ProblemInstance) -> List[ReasoningPath]:
        """Parse LLM response into separate reasoning branches."""
        branches = []
        
        # Simple parsing - look for approach markers
        sections = response.split('Approach')
        
        for i, section in enumerate(sections[1:], 1):  # Skip first empty section
            lines = section.strip().split('\n')
            if lines:
                approach_name = f"Approach {i}"
                steps = [line.strip() for line in lines if line.strip()]
                
                if steps:
                    branch = ReasoningPath(
                        id=generate_id("branch", problem.problem),
                        problem=problem.problem,
                        approach=approach_name,
                        steps=steps[:3],  # Initial steps only
                        confidence=0.5,  # Initial confidence
                        status='active'
                    )
                    branches.append(branch)
        
        # If parsing failed, create default branches
        if not branches:
            for i in range(self.num_initial_branches):
                branch = ReasoningPath(
                    id=generate_id("branch", problem.problem),
                    problem=problem.problem,
                    approach=f"Standard approach {i+1}",
                    steps=[f"Step 1: Analyze the problem", f"Step 2: Identify key information"],
                    confidence=0.5,
                    status='active'
                )
                branches.append(branch)
        
        return branches
    
    def _parse_expansion_response(self, response: str) -> List[str]:
        """Parse expansion response into additional reasoning steps."""
        lines = response.strip().split('\n')
        steps = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                steps.append(line)
        
        return steps[:3]  # Limit to 3 additional steps
    
    def _parse_evaluation_response(self, response: str) -> Dict[str, float]:
        """Parse evaluation response into numerical scores."""
        scores = {
            'correctness': 5.0,
            'completeness': 5.0,
            'efficiency': 5.0,
            'clarity': 5.0
        }
        
        # Look for numerical scores in the response
        import re
        for key in scores.keys():
            pattern = rf'{key}[:\s]+(\d+(?:\.\d+)?)'
            match = re.search(pattern, response.lower())
            if match:
                scores[key] = min(float(match.group(1)), 10.0)
        
        return scores
    
    def _parse_synthesis_response(self, response: str) -> Dict[str, Any]:
        """Parse synthesis response into final answer and reasoning."""
        
        # Extract final answer
        final_answer = TextProcessor.extract_final_answer(response)
        
        # Extract confidence
        confidence = TextProcessor.extract_confidence_score(response)
        
        return {
            'answer': final_answer,
            'confidence': confidence,
            'reasoning': response
        }
    
    async def _call_llm(self, prompt: str, system_prompt: str = "") -> str:
        """Make a call to the LLM."""
        try:
            # This is a placeholder - actual implementation would depend on the LLM client
            if hasattr(self.llm_client, 'chat_completion'):
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = await self.llm_client.chat_completion(messages)
                return response.get('content', '')
            else:
                # Fallback for simple completion
                return await self.llm_client.complete(prompt)
                
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"Error: Could not get LLM response - {str(e)}"
    
    def _log_reasoning_session(self, problem: ProblemInstance, paths: List[ReasoningPath], 
                             solution: Dict[str, Any], processing_time: float):
        """Log the complete reasoning session."""
        session_data = {
            'problem_id': problem.id,
            'problem': problem.problem,
            'task_type': problem.task_type,
            'reasoning_paths': [asdict(path) for path in paths],
            'final_solution': solution,
            'processing_time': processing_time,
            'timestamp': generate_id("session")
        }
        
        self.file_manager.append_log(session_data, 'logs/reasoning_paths/sessions.jsonl')

# Mock LLM client for testing
class MockLLMClient:
    """Mock LLM client for testing purposes."""
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> Dict[str, str]:
        """Mock chat completion."""
        # Simple mock responses based on prompt content
        user_message = messages[-1].get('content', '').lower()
        
        if 'generate' in user_message and 'approaches' in user_message:
            return {
                'content': """Approach 1: Direct calculation
1. Identify the given values
2. Set up the equation
3. Solve step by step

Approach 2: Working backwards
1. Start with the desired result
2. Reverse engineer the steps
3. Verify the solution

Approach 3: Visual/graphical method
1. Draw a diagram or graph
2. Use visual reasoning
3. Extract the numerical answer"""
            }
        elif 'evaluate' in user_message:
            return {
                'content': """Correctness: 8
Completeness: 7
Efficiency: 6
Clarity: 8
Overall: This is a solid approach with good logical flow."""
            }
        elif 'synthesize' in user_message:
            return {
                'content': """After comparing all approaches, the direct calculation method provides the most reliable solution.

Final answer: 42

Confidence: 8/10

The solution is well-supported by multiple reasoning paths."""
            }
        else:
            return {
                'content': """Step 1: Analyze the problem components
Step 2: Apply relevant principles
Step 3: Calculate the result
Step 4: Verify the answer

Final answer: Based on the analysis, the solution is 42."""
            }
    
    async def complete(self, prompt: str) -> str:
        """Mock completion."""
        return "This is a mock response to: " + prompt[:50] + "..." 