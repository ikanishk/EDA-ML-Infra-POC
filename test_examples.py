"""
Test Examples for AI Pipeline POC
Run these to test the pipeline locally without starting the server
"""

from pipeline import Pipeline
from context import context_manager
import json


def print_result(result: dict, title: str):
    """Pretty print test results"""
    print("\n" + "=" * 60)
    print(f"TEST: {title}")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)


def test_code_generation():
    """Test code generation intent"""
    pipeline = Pipeline(use_mock_llm=True)
    result = pipeline.execute("Write a Python function to calculate fibonacci numbers")
    print_result(result, "Code Generation Query")


def test_debugging():
    """Test debugging intent"""
    pipeline = Pipeline(use_mock_llm=True)
    result = pipeline.execute("My code is throwing a KeyError, how do I fix it?")
    print_result(result, "Debugging Query")


def test_general_question():
    """Test general question intent"""
    pipeline = Pipeline(use_mock_llm=True)
    result = pipeline.execute("What is the difference between a list and a tuple in Python?")
    print_result(result, "General Question")


def test_documentation():
    """Test documentation intent"""
    pipeline = Pipeline(use_mock_llm=True)
    result = pipeline.execute("Show me the documentation for FastAPI")
    print_result(result, "Documentation Request")


def test_optimization():
    """Test optimization intent"""
    pipeline = Pipeline(use_mock_llm=True)
    result = pipeline.execute("How can I make my Python code run faster?")
    print_result(result, "Optimization Query")


def test_context_continuity():
    """Test context management across multiple queries"""
    pipeline = Pipeline(use_mock_llm=True)
    
    # Clear context first
    context_manager.clear_context()
    
    # First query
    result1 = pipeline.execute("Explain Python decorators")
    print_result(result1, "First Query (No Context)")
    
    # Second query (should have context from first)
    result2 = pipeline.execute("Can you show me an example?")
    print_result(result2, "Second Query (With Context)")
    
    # Check context
    context = context_manager.get_context()
    print("\n" + "=" * 60)
    print("CONTEXT STATE")
    print("=" * 60)
    print(json.dumps(context, indent=2, default=str))
    print("=" * 60)


def test_pipeline_info():
    """Test pipeline graph information"""
    pipeline = Pipeline(use_mock_llm=True)
    info = pipeline.get_pipeline_graph_info()
    print("\n" + "=" * 60)
    print("PIPELINE GRAPH INFO")
    print("=" * 60)
    print(json.dumps(info, indent=2))
    print("=" * 60)


def run_all_tests():
    """Run all test examples"""
    print("\n" + "#" * 60)
    print("# AI Pipeline POC - Test Suite")
    print("#" * 60)
    
    test_code_generation()
    test_debugging()
    test_general_question()
    test_documentation()
    test_optimization()
    test_context_continuity()
    test_pipeline_info()
    
    print("\n" + "#" * 60)
    print("# All Tests Completed")
    print("#" * 60)


if __name__ == "__main__":
    run_all_tests()
