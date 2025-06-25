#!/usr/bin/env python3
"""
Medical Q&A Assistant - CLI Application
Uses Ollama Qwen3:0.6b with different prompt engineering strategies
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
import requests
from utils import (
    load_prompts, load_queries, evaluate_response, 
    log_hallucination, save_results, OllamaClient
)

class MedicalQAAssistant:
    def __init__(self, model_name: str = "qwen:0.5b"):
        """Initialize the Medical Q&A Assistant"""
        self.model_name = model_name
        self.ollama_client = OllamaClient(model_name)
        self.prompts = load_prompts()
        self.results = {
            'zero_shot': {'query_results': [], 'performance_metrics': {}},
            'few_shot': {'query_results': [], 'performance_metrics': {}},
            'cot': {'query_results': [], 'performance_metrics': {}},
            'meta_prompt': {'query_results': [], 'performance_metrics': {}}
        }
        
    def run_single_query(self, query: str, prompt_type: str) -> Dict[str, Any]:
        """Run a single query with specified prompt type"""
        try:
            # Format the prompt with the query
            formatted_prompt = self.prompts[prompt_type].format(query=query)
            
            # Get response from Ollama
            start_time = time.time()
            response = self.ollama_client.generate(formatted_prompt)
            response_time = time.time() - start_time
            
            return {
                'query': query,
                'prompt_type': prompt_type,
                'response': response,
                'response_time': response_time,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error processing query with {prompt_type}: {str(e)}")
            return {
                'query': query,
                'prompt_type': prompt_type,
                'response': f"Error: {str(e)}",
                'response_time': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    def evaluate_all_prompts(self, queries: List[Dict]) -> None:
        """Evaluate all prompt types against all queries"""
        print("🏥 Starting Medical Q&A Assistant Evaluation...")
        print(f"📊 Model: {self.model_name}")
        print(f"🧪 Testing {len(queries)} queries with 4 prompt strategies\n")
        
        prompt_types = ['zero_shot', 'few_shot', 'cot', 'meta_prompt']
        
        for i, query_data in enumerate(queries):
            query = query_data['query']
            print(f"Query {i+1}/{len(queries)}: {query[:80]}...")
            
            for prompt_type in prompt_types:
                print(f"  Testing {prompt_type}...", end=' ')
                
                # Run the query
                result = self.run_single_query(query, prompt_type)
                
                # Evaluate the response
                evaluation = evaluate_response(
                    result['response'], 
                    query_data.get('expected_considerations', []),
                    query_data.get('safety_requirements', [])
                )
                
                # Add evaluation to result
                result.update(evaluation)
                
                # Store result
                self.results[prompt_type]['query_results'].append(result)
                
                # Check for hallucinations
                if evaluation.get('hallucination_detected', False):
                    log_hallucination(result, evaluation['hallucination_details'])
                
                print(f"✓ (Accuracy: {evaluation['accuracy_score']:.1f})")
            
            print()  # Add space between queries
    
    def calculate_performance_metrics(self) -> None:
        """Calculate overall performance metrics for each prompt type"""
        for prompt_type in self.results:
            results = self.results[prompt_type]['query_results']
            
            if not results:
                continue
                
            # Calculate averages
            accuracy_scores = [r.get('accuracy_score', 0) for r in results]
            reasoning_scores = [r.get('reasoning_clarity', 0) for r in results]
            hallucination_scores = [r.get('hallucination_score', 0) for r in results]
            consistency_scores = [r.get('consistency_score', 0) for r in results]
            safety_scores = [r.get('safety_compliance', 0) for r in results]
            
            self.results[prompt_type]['performance_metrics'] = {
                'accuracy_score': sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0,
                'reasoning_clarity': sum(reasoning_scores) / len(reasoning_scores) if reasoning_scores else 0,
                'hallucination_score': sum(hallucination_scores) / len(hallucination_scores) if hallucination_scores else 0,
                'consistency_score': sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0,
                'safety_compliance': sum(safety_scores) / len(safety_scores) if safety_scores else 0
            }
    
    def print_results_summary(self) -> None:
        """Print a summary of the evaluation results"""
        print("\n" + "="*60)
        print("📊 EVALUATION RESULTS SUMMARY")
        print("="*60)
        
        for prompt_type in self.results:
            metrics = self.results[prompt_type]['performance_metrics']
            if metrics:
                print(f"\n{prompt_type.upper().replace('_', '-')} PROMPTING:")
                print(f"  Accuracy:       {metrics['accuracy_score']:.1f}%")
                print(f"  Reasoning:      {metrics['reasoning_clarity']:.1f}/5")
                print(f"  Hallucinations: {metrics['hallucination_score']:.1f}/5")
                print(f"  Consistency:    {metrics['consistency_score']:.1f}%")
                print(f"  Safety:         {metrics['safety_compliance']:.1f}%")
        
        # Find best performing prompt
        best_prompt = max(self.results.keys(), 
                         key=lambda x: self.results[x]['performance_metrics'].get('accuracy_score', 0))
        
        print(f"\n🏆 BEST PERFORMING: {best_prompt.upper().replace('_', '-')}")
        print("="*60)
    
    def interactive_mode(self) -> None:
        """Run the assistant in interactive mode"""
        print("\n🏥 Medical Q&A Assistant - Interactive Mode")
        print("Choose a prompt strategy:")
        print("1. Zero-shot")
        print("2. Few-shot")
        print("3. Chain-of-Thought")
        print("4. Meta-prompting")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                choice = input("Select prompt type (1-4) or 'quit': ").strip()
                
                if choice.lower() == 'quit':
                    break
                
                prompt_map = {
                    '1': 'zero_shot',
                    '2': 'few_shot', 
                    '3': 'cot',
                    '4': 'meta_prompt'
                }
                
                if choice not in prompt_map:
                    print("Invalid choice. Please select 1-4 or 'quit'.")
                    continue
                
                query = input("\nEnter your medical question: ").strip()
                if not query:
                    print("Please enter a valid question.")
                    continue
                
                print("\n🤔 Processing your question...")
                result = self.run_single_query(query, prompt_map[choice])
                
                print("\n" + "="*60)
                print("🏥 MEDICAL ASSISTANT RESPONSE:")
                print("="*60)
                print(result['response'])
                print("\n" + "="*60)
                print(f"Response time: {result['response_time']:.2f} seconds")
                print("="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

def main():
    """Main application entry point"""
    assistant = MedicalQAAssistant()
    
    print("🏥 Medical Q&A Assistant")
    print("Choose mode:")
    print("1. Run full evaluation")
    print("2. Interactive mode")
    
    try:
        mode = input("Select mode (1-2): ").strip()
        
        if mode == '1':
            # Load test queries
            queries = load_queries()
            
            # Run evaluation
            assistant.evaluate_all_prompts(queries)
            
            # Calculate metrics
            assistant.calculate_performance_metrics()
            
            # Print results
            assistant.print_results_summary()
            
            # Save results
            save_results(assistant.results)
            print("\n💾 Results saved to evaluation/output_logs.json")
            
        elif mode == '2':
            assistant.interactive_mode()
            
        else:
            print("Invalid selection. Please choose 1 or 2.")
            
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()