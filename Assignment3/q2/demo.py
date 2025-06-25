#!/usr/bin/env python3
"""
Demonstration script for the Multi-Path Reasoning Pipeline.
This script showcases the key capabilities of the system with example problems.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils import ProblemInstance, FileManager
from tot_reasoning import TreeOfThoughtReasoner, MockLLMClient
from self_consistency import SelfConsistencyAggregator, MajorityVotingAggregator
from prompt_optimizer import PromptOptimizer
from evaluator import PipelineEvaluator
from main import MultiPathReasoningPipeline, create_default_config

def print_banner():
    """Print an attractive banner for the demo."""
    print("=" * 80)
    print("🧠 MULTI-PATH REASONING PIPELINE DEMONSTRATION 🧠")
    print("=" * 80)
    print("Features:")
    print("• Tree-of-Thought (ToT) Multi-Path Reasoning")
    print("• Self-Consistency Answer Aggregation") 
    print("• Automated Prompt Optimization (OPRO/TextGrad style)")
    print("• Comprehensive Evaluation Framework")
    print("=" * 80)
    print()

def create_demo_problems():
    """Create a set of demonstration problems across different domains."""
    
    demo_problems = [
        # Math Problem
        {
            'id': 'demo_math_001',
            'task_type': 'math_problems',
            'problem': 'A store sells notebooks for $3 each and pens for $2 each. If Sarah buys 4 notebooks and 6 pens, and pays with a $50 bill, how much change should she receive?',
            'expected_answer': '$26',
            'difficulty': 'basic'
        },
        
        # Logic Puzzle
        {
            'id': 'demo_logic_001', 
            'task_type': 'logic_puzzles',
            'problem': 'Three friends Alice, Bob, and Carol each have different pets: a cat, a dog, and a bird. We know: (1) Alice does not have the cat, (2) Bob does not have the bird, (3) Carol does not have the dog. Who has which pet?',
            'expected_answer': 'Alice has the dog, Bob has the cat, Carol has the bird',
            'difficulty': 'basic'
        },
        
        # Code Debugging
        {
            'id': 'demo_code_001',
            'task_type': 'code_debugging', 
            'problem': 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n)\n\n# This function causes infinite recursion. What\'s wrong and how to fix it?',
            'expected_answer': 'Missing recursive case reduction: should be factorial(n-1)',
            'difficulty': 'basic'
        }
    ]
    
    return demo_problems

async def demo_tree_of_thought(problem, llm_client, config):
    """Demonstrate Tree-of-Thought reasoning on a single problem."""
    
    print(f"🌳 TREE-OF-THOUGHT REASONING DEMO")
    print(f"Problem: {problem.problem}")
    print("-" * 60)
    
    reasoner = TreeOfThoughtReasoner(llm_client, config)
    result = await reasoner.solve_problem(problem)
    
    print(f"Generated {len(result['reasoning_paths'])} reasoning paths:")
    print()
    
    for i, path in enumerate(result['reasoning_paths'], 1):
        print(f"Path {i}: {path['approach']}")
        print(f"Confidence: {path['confidence']:.2f}")
        print("Steps:")
        for j, step in enumerate(path['steps'], 1):
            print(f"  {j}. {step}")
        print(f"Status: {path['status']}")
        print()
    
    print(f"Final Answer: {result['final_answer']}")
    print(f"Overall Confidence: {result['confidence']:.2f}")
    print(f"Processing Time: {result['processing_time']:.2f}s")
    print()
    
    return result

async def demo_self_consistency(reasoning_paths):
    """Demonstrate Self-Consistency aggregation."""
    
    print(f"🎯 SELF-CONSISTENCY AGGREGATION DEMO")
    print("-" * 60)
    
    from utils import ReasoningPath
    
    # Convert to ReasoningPath objects
    paths = []
    for path_data in reasoning_paths:
        path = ReasoningPath(
            id=path_data['id'],
            problem=path_data['problem'],
            approach=path_data['approach'],
            steps=path_data['steps'],
            confidence=path_data['confidence'],
            status=path_data['status'],
            evaluation_scores=path_data.get('evaluation_scores', {})
        )
        paths.append(path)
    
    # Compare different aggregation methods
    config = create_default_config()
    
    # Self-Consistency
    sc_aggregator = SelfConsistencyAggregator(config)
    sc_result = sc_aggregator.aggregate_paths(paths)
    
    # Simple Majority Voting
    mv_aggregator = MajorityVotingAggregator(config)
    mv_result = mv_aggregator.aggregate_paths(paths)
    
    print("📊 Aggregation Results Comparison:")
    print()
    print("Self-Consistency Method:")
    print(f"  Consensus Answer: {sc_result['consensus_answer']}")
    print(f"  Confidence: {sc_result['confidence']:.2f}")
    print(f"  Consistency Score: {sc_result['consistency_score']:.2f}")
    print(f"  Reasoning Diversity: {sc_result['reasoning_diversity']:.2f}")
    print()
    
    print("Simple Majority Voting:")
    print(f"  Consensus Answer: {mv_result['consensus_answer']}")
    print(f"  Confidence: {mv_result['confidence']:.2f}")
    print(f"  Vote Distribution: {mv_result['vote_distribution']}")
    print()
    
    return sc_result

async def demo_prompt_optimization(problem, llm_client, config):
    """Demonstrate automated prompt optimization."""
    
    print(f"⚡ AUTOMATED PROMPT OPTIMIZATION DEMO")
    print("-" * 60)
    
    # Original prompt
    original_prompt = "Solve this problem step by step: {problem}"
    
    print(f"Original Prompt:")
    print(f"  {original_prompt}")
    print()
    
    # Create simple evaluation function
    async def evaluate_performance(problem_dict, response):
        # Mock evaluation - in reality this would be more sophisticated
        expected = problem_dict.get('expected_answer', '').lower()
        actual = response.lower()
        
        if expected in actual:
            return 0.9
        elif len(set(expected.split()) & set(actual.split())) > 0:
            return 0.6
        else:
            return 0.3
    
    # Run optimization
    test_problems = [{
        'problem': problem.problem,
        'expected_answer': problem.expected_answer,
        'id': problem.id
    }]
    
    optimizer = PromptOptimizer(llm_client, config)
    
    try:
        optimization_result = await optimizer.optimize_prompt(
            original_prompt=original_prompt,
            task_type=problem.task_type,
            test_problems=test_problems,
            evaluation_function=evaluate_performance
        )
        
        print(f"Optimization Results:")
        print(f"  Iterations: {optimization_result.iteration}")
        print(f"  Performance Improvement: {optimization_result.performance_improvement:.3f}")
        print()
        print(f"Optimized Prompt:")
        print(f"  {optimization_result.optimized_prompt}")
        print()
        
        return optimization_result
        
    except Exception as e:
        print(f"Optimization demo encountered an error: {e}")
        print("This is expected with the mock LLM client.")
        return None

async def demo_comprehensive_evaluation(problem, pipeline_result):
    """Demonstrate comprehensive evaluation system."""
    
    print(f"📈 COMPREHENSIVE EVALUATION DEMO")
    print("-" * 60)
    
    config = create_default_config()
    evaluator = PipelineEvaluator(config)
    
    try:
        evaluation = await evaluator.evaluate_pipeline_result(problem, pipeline_result)
        
        print("Evaluation Results:")
        print()
        
        # Correctness
        correctness = evaluation['correctness']
        print(f"✅ Correctness Score: {correctness['score']:.2f}")
        print(f"   Final Answer: {correctness['final_answer']}")
        print(f"   Expected: {correctness['expected_answer']}")
        print(f"   Exact Match: {correctness['exact_match']}")
        print()
        
        # Reasoning Quality
        reasoning = evaluation['reasoning_quality']
        print(f"🧠 Reasoning Quality: {reasoning['score']:.2f}")
        print(f"   Path Count: {reasoning['path_count']}")
        print(f"   Avg Steps per Path: {reasoning['avg_steps_per_path']:.1f}")
        print(f"   Reasoning Coherence: {reasoning['reasoning_coherence']:.2f}")
        print()
        
        # Consistency
        consistency = evaluation['consistency']
        print(f"🎯 Consistency Score: {consistency['score']:.2f}")
        print(f"   Path Agreement: {consistency['path_agreement']:.2f}")
        print(f"   Reasoning Diversity: {consistency['reasoning_diversity']:.2f}")
        print()
        
        # Hallucination
        hallucination = evaluation['hallucination']
        print(f"🚨 Hallucination Score: {hallucination['score']:.2f}")
        print(f"   Hallucination Count: {hallucination['hallucination_count']}")
        print()
        
        # Overall Assessment
        assessment = evaluation['overall_assessment']
        print(f"🏆 Overall Performance: {assessment['performance_level']}")
        print(f"   Description: {assessment['description']}")
        print(f"   Overall Score: {assessment['overall_score']:.2f}")
        if assessment['strengths']:
            print(f"   Strengths: {', '.join(assessment['strengths'])}")
        if assessment['weaknesses']:
            print(f"   Weaknesses: {', '.join(assessment['weaknesses'])}")
        print()
        
        return evaluation
        
    except Exception as e:
        print(f"Evaluation demo encountered an error: {e}")
        return None

async def demo_full_pipeline():
    """Demonstrate the complete pipeline on multiple problems."""
    
    print(f"🚀 FULL PIPELINE DEMONSTRATION")
    print("-" * 60)
    
    # Setup
    config = create_default_config()
    config['verbose'] = True
    llm_client = MockLLMClient()
    pipeline = MultiPathReasoningPipeline(config, llm_client)
    
    # Load demo problems
    demo_problems = create_demo_problems()
    
    print(f"Running pipeline on {len(demo_problems)} demonstration problems...")
    print()
    
    try:
        results = await pipeline.run_pipeline(
            task_type='mixed_demo',
            problems=demo_problems,
            optimize_prompts=False  # Skip optimization for demo speed
        )
        
        print("Pipeline Results Summary:")
        print("-" * 40)
        
        performance = results['performance_summary']
        print(f"Total Problems: {performance['total_problems']}")
        print(f"Overall Accuracy: {performance['accuracy']:.2%}")
        print(f"Average Confidence: {performance['average_confidence']:.2f}")
        print(f"Average Consistency: {performance['average_consistency']:.2f}")
        print()
        
        # Show individual results
        for i, result in enumerate(results['problem_results']):
            prob = demo_problems[i]
            print(f"Problem {i+1} ({prob['task_type']}):")
            print(f"  Question: {prob['problem'][:60]}...")
            print(f"  Answer: {result.get('final_answer', 'Error')}")
            print(f"  Expected: {prob.get('expected_answer', 'N/A')}")
            print(f"  Confidence: {result.get('confidence', 0.0):.2f}")
            print()
        
        return results
        
    except Exception as e:
        print(f"Full pipeline demo encountered an error: {e}")
        return None

async def run_demo():
    """Run the complete demonstration."""
    
    print_banner()
    
    # Setup
    config = create_default_config()
    llm_client = MockLLMClient()
    demo_problems = create_demo_problems()
    
    # Convert first problem to ProblemInstance
    prob_data = demo_problems[0]  # Use math problem for detailed demo
    problem = ProblemInstance(
        id=prob_data['id'],
        task_type=prob_data['task_type'],
        problem=prob_data['problem'],
        expected_answer=prob_data['expected_answer'],
        difficulty=prob_data['difficulty']
    )
    
    try:
        # Demo 1: Tree-of-Thought
        print("DEMO 1: Tree-of-Thought Reasoning")
        print("=" * 80)
        tot_result = await demo_tree_of_thought(problem, llm_client, config)
        input("\nPress Enter to continue to next demo...")
        print()
        
        # Demo 2: Self-Consistency
        print("DEMO 2: Self-Consistency Aggregation")
        print("=" * 80)
        sc_result = await demo_self_consistency(tot_result['reasoning_paths'])
        input("\nPress Enter to continue to next demo...")
        print()
        
        # Demo 3: Prompt Optimization
        print("DEMO 3: Automated Prompt Optimization")
        print("=" * 80)
        opt_result = await demo_prompt_optimization(problem, llm_client, config)
        input("\nPress Enter to continue to next demo...")
        print()
        
        # Demo 4: Comprehensive Evaluation
        print("DEMO 4: Comprehensive Evaluation")
        print("=" * 80)
        eval_result = await demo_comprehensive_evaluation(problem, tot_result)
        input("\nPress Enter to continue to final demo...")
        print()
        
        # Demo 5: Full Pipeline
        print("DEMO 5: Complete Pipeline")
        print("=" * 80)
        pipeline_result = await demo_full_pipeline()
        
        print()
        print("=" * 80)
        print("🎉 DEMONSTRATION COMPLETE! 🎉")
        print("=" * 80)
        print()
        print("Key Takeaways:")
        print("• Multi-path reasoning explores diverse solution approaches")
        print("• Self-consistency provides more reliable answers than single paths")
        print("• Automated optimization can improve prompt performance")
        print("• Comprehensive evaluation reveals multiple quality dimensions")
        print("• The full pipeline integrates all components effectively")
        print()
        print("Next Steps:")
        print("• Try running: python src/main.py --task math_problems --optimize")
        print("• Experiment with different configuration parameters")
        print("• Add your own problems to the task files")
        print("• Explore the evaluation and optimization logs")
        print()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo encountered an error: {e}")
        print("This may be due to missing dependencies or configuration issues.")

if __name__ == "__main__":
    print("🔧 Setting up demonstration environment...")
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Create file manager to ensure directories exist
    file_manager = FileManager()
    
    print("✅ Environment ready!")
    print()
    
    # Run the demo
    asyncio.run(run_demo()) 