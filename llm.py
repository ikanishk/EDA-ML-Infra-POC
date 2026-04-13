"""
LLM Integration Layer
Handles interaction with Language Models (mock or real)
"""

from typing import Dict, Any, Optional
import os


class LLMHandler:
    """
    LLM integration handler.
    This is where LLM INTERACTION happens.
    
    Can use real LLM APIs (OpenAI, Anthropic, etc.) or mock responses.
    """
    
    def __init__(self, use_mock: bool = True):
        """
        Initialize LLM handler.
        
        Args:
            use_mock: If True, use mock responses. If False, use real LLM API.
        """
        self.use_mock = use_mock
        self.api_key = os.getenv("OPENAI_API_KEY")  # Example for OpenAI
        
        # Mock response templates by intent
        self.mock_responses = {
            "code_generation": "Here's a code example that addresses your request:\n\n```python\ndef example_function():\n    # Implementation based on your query\n    pass\n```\n\nThis code demonstrates the concept you asked about.",
            
            "debugging": "I've analyzed the issue. Here are potential solutions:\n\n1. Check for null/undefined values\n2. Verify data types match expected format\n3. Review error logs for specific error messages\n\nTry adding error handling and logging to identify the root cause.",
            
            "general_question": "Based on your question, here's a comprehensive explanation:\n\nThe concept you're asking about involves multiple components working together. The key points to understand are:\n\n1. Core functionality and purpose\n2. How different parts interact\n3. Best practices for implementation\n\nLet me know if you need more specific details.",
            
            "documentation": "Here's the documentation you requested:\n\n## Overview\nThis section covers the main concepts and usage patterns.\n\n## Getting Started\n1. Installation steps\n2. Basic configuration\n3. First example\n\n## API Reference\nDetailed information about available methods and parameters.",
            
            "optimization": "Here are optimization recommendations:\n\n1. **Performance**: Consider caching frequently accessed data\n2. **Efficiency**: Use appropriate data structures (e.g., sets for lookups)\n3. **Scalability**: Implement async operations where applicable\n4. **Best Practices**: Follow language-specific optimization patterns\n\nThese changes should improve overall performance."
        }
    
    def generate_response(
        self, 
        query: str, 
        intent: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a response using LLM.
        
        Args:
            query: User's input query
            intent: Detected intent category
            context: Optional context from previous interactions
            
        Returns:
            Generated response string
        """
        if self.use_mock:
            return self._generate_mock_response(query, intent, context)
        else:
            return self._generate_real_response(query, intent, context)
    
    def _generate_mock_response(
        self, 
        query: str, 
        intent: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate mock response based on intent and query content.
        
        Args:
            query: User's query
            intent: Detected intent
            context: Optional context
            
        Returns:
            Mock response string
        """
        # Generate contextual response based on query content
        response = self._generate_contextual_response(query, intent)
        
        # Add context awareness if available
        if context and context.get("has_context"):
            response += f"\n\n💡 *Building on your previous question about: '{context.get('last_query', 'N/A')}'*"
        
        return response
    
    def _generate_contextual_response(self, query: str, intent: str) -> str:
        """
        Generate a contextual response based on query keywords.
        
        Args:
            query: User's query
            intent: Detected intent
            
        Returns:
            Contextual response string
        """
        query_lower = query.lower()
        
        if intent == "code_generation":
            return self._generate_code_response(query_lower)
        elif intent == "debugging":
            return self._generate_debug_response(query_lower)
        elif intent == "general_question":
            return self._generate_explanation_response(query_lower)
        elif intent == "documentation":
            return self._generate_docs_response(query_lower)
        elif intent == "optimization":
            return self._generate_optimization_response(query_lower)
        else:
            return f"I understand you're asking about: '{query}'\n\nLet me help you with that. Could you provide more specific details about what you need?"
    
    def _generate_code_response(self, query: str) -> str:
        """Generate code based on query keywords"""
        
        # Check for specific operations (order matters - check specific before general)
        if "add" in query or "sum" in query or "addition" in query:
            return """Here's a function to add two numbers:

```python
def add_numbers(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

# Example:
result = add_numbers(5, 3)
print(result)  # Output: 8
```"""
        
        elif "subtract" in query or "subtraction" in query:
            return """Here's a function to subtract two numbers:

```python
def subtract_numbers(a, b):
    \"\"\"Subtract b from a and return the result.\"\"\"
    return a - b

# Example:
result = subtract_numbers(10, 4)
print(result)  # Output: 6
```"""
        
        elif "multiply" in query or "multiplication" in query:
            return """Here's a function to multiply two numbers:

```python
def multiply_numbers(a, b):
    \"\"\"Multiply two numbers and return the result.\"\"\"
    return a * b

# Example:
result = multiply_numbers(6, 7)
print(result)  # Output: 42
```"""
        
        elif "divide" in query or "division" in query:
            return """Here's a function to divide two numbers:

```python
def divide_numbers(a, b):
    \"\"\"Divide a by b and return the result.\"\"\"
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

# Example:
result = divide_numbers(20, 4)
print(result)  # Output: 5.0
```"""
        
        elif "sort" in query:
            return """Here's a function to sort a list:

```python
def sort_list(numbers):
    \"\"\"Sort a list of numbers in ascending order.\"\"\"
    return sorted(numbers)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
sorted_numbers = sort_list(numbers)
print(sorted_numbers)  # Output: [1, 2, 3, 5, 8, 9]
```"""
        
        elif "reverse" in query:
            return """Here's a function to reverse a list:

```python
def reverse_list(items):
    \"\"\"Reverse the order of items in a list.\"\"\"
    return items[::-1]

# Example:
numbers = [1, 2, 3, 4, 5]
reversed_numbers = reverse_list(numbers)
print(reversed_numbers)  # Output: [5, 4, 3, 2, 1]
```"""
        
        elif "max" in query or "maximum" in query or "largest" in query:
            return """Here's a function to find the maximum value:

```python
def find_max(numbers):
    \"\"\"Find the maximum value in a list.\"\"\"
    return max(numbers)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
maximum = find_max(numbers)
print(maximum)  # Output: 9
```"""
        
        elif "min" in query or "minimum" in query or "smallest" in query:
            return """Here's a function to find the minimum value:

```python
def find_min(numbers):
    \"\"\"Find the minimum value in a list.\"\"\"
    return min(numbers)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
minimum = find_min(numbers)
print(minimum)  # Output: 1
```"""
        
        elif "average" in query or "mean" in query:
            return """Here's a function to calculate the average:

```python
def calculate_average(numbers):
    \"\"\"Calculate the average of a list of numbers.\"\"\"
    return sum(numbers) / len(numbers)

# Example:
numbers = [10, 20, 30, 40, 50]
average = calculate_average(numbers)
print(average)  # Output: 30.0
```"""
        
        elif "filter" in query or "even" in query:
            return """Here's a function to filter even numbers:

```python
def filter_even(numbers):
    \"\"\"Filter and return only even numbers from a list.\"\"\"
    return [n for n in numbers if n % 2 == 0]

# Example:
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = filter_even(numbers)
print(even_numbers)  # Output: [2, 4, 6, 8]
```"""
        
        # Default
        else:
            return """Here's a basic Python function template:

```python
def my_function(data):
    \"\"\"Process the input data.\"\"\"
    # Add your logic here
    return data

# Example:
result = my_function("input")
print(result)
```

**Tip:** Try asking for:
- "add two numbers"
- "sort a list"
- "find maximum value"
- "calculate average"
"""
    
    def _detect_language(self, query: str) -> str:
        """Detect language - simplified to just return python"""
        return "python"
    
    def _generate_debug_response(self, query: str) -> str:
        """Generate simple debugging help"""
        
        query_lower = query.lower()
        
        if "error" in query_lower or "bug" in query_lower or "fix" in query_lower:
            return """**Basic Debugging Steps:**

1. **Read the error message carefully**
   - Look at the line number
   - Understand what went wrong

2. **Check common issues:**
   - Typos in variable names
   - Missing parentheses or brackets
   - Indentation errors (Python)
   - Data type mismatches

3. **Add print statements:**
```python
print("Debug: variable value =", my_variable)
```

4. **Test with simple inputs first**

5. **Check if variables are None/null**
"""
        
        elif "min" in query_lower or "minimum" in query_lower or "smallest" in query_lower:
            return """**Basic Debugging Steps:**

1. **Read the error message carefully**
   - Look at the line number
   - Understand what went wrong

2. **Check common issues:**
   - Typos in variable names
   - Missing parentheses or brackets
   - Indentation errors (Python)
   - Data type mismatches

3. **Add print statements:**
```python
print("Debug: variable value =", my_variable)
```

4. **Test with simple inputs first**

5. **Check if variables are None/null**
"""
        
        return """**Debugging Help:**

Common issues to check:
- Syntax errors (missing colons, brackets)
- Variable not defined
- Wrong data type
- Division by zero
- Index out of range

Add print statements to see what's happening:
```python
print("Value:", my_var)
```"""
    
    def _generate_explanation_response(self, query: str) -> str:
        """Generate simple explanations"""
        
        if "list" in query or "array" in query:
            return """**Lists in Python:**

A list is a collection of items in a specific order.

```python
# Creating a list
my_list = [1, 2, 3, 4, 5]

# Accessing items
first = my_list[0]  # Gets 1

# Adding items
my_list.append(6)

# Removing items
my_list.remove(3)

# Length
length = len(my_list)
```

**Common operations:**
- `append()` - add item
- `remove()` - remove item
- `sort()` - sort the list
- `reverse()` - reverse order
"""
        
        elif "function" in query:
            return """**Functions in Python:**

A function is a reusable block of code.

```python
def greet(name):
    \"\"\"Greet a person by name.\"\"\"
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

**Key parts:**
- `def` - defines a function
- Parameters - inputs to the function
- `return` - sends back a result
"""
        
        return f"""**About: {query}**

This is a common programming concept. Here's a simple explanation:

**What it is:**
A fundamental building block in programming.

**How to use it:**
```python
# Example code
result = process_data(input)
```

**When to use it:**
When you need this specific functionality in your program.
"""
    
    def _generate_docs_response(self, query: str) -> str:
        """Generate simple documentation"""
        return """**Quick Reference:**

## Basic Python Syntax

### Variables
```python
x = 10
name = "Alice"
```

### Lists
```python
numbers = [1, 2, 3]
numbers.append(4)
```

### Functions
```python
def my_function(param):
    return param * 2
```

### Loops
```python
for item in my_list:
    print(item)
```

### Conditionals
```python
if x > 5:
    print("Greater than 5")
```
"""
    
    def _generate_optimization_response(self, query: str) -> str:
        """Generate simple optimization tips"""
        return """**Simple Optimization Tips:**

1. **Use built-in functions**
   - They're faster than custom loops
   ```python
   # Fast
   total = sum(numbers)
   
   # Slower
   total = 0
   for n in numbers:
       total += n
   ```

2. **Use list comprehensions**
   ```python
   # Fast
   squares = [x**2 for x in range(10)]
   
   # Slower
   squares = []
   for x in range(10):
       squares.append(x**2)
   ```

3. **Avoid repeated calculations**
   ```python
   # Calculate once
   length = len(my_list)
   for i in range(length):
       # use i
   ```

4. **Use appropriate data structures**
   - Lists for ordered data
   - Sets for unique items (faster lookups)
   - Dictionaries for key-value pairs
"""
    
    # Remove all the complex helper methods
    def _generate_real_response(
        self, 
        query: str, 
        intent: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate response using real LLM API.
        
        This is a placeholder for actual LLM integration.
        You would implement OpenAI, Anthropic, or other LLM API calls here.
        
        Args:
            query: User's query
            intent: Detected intent
            context: Optional context
            
        Returns:
            LLM-generated response
        """
        # Example structure for OpenAI API call (commented out)
        """
        import openai
        
        openai.api_key = self.api_key
        
        # Build prompt with intent and context
        system_prompt = f"You are a helpful assistant. The user's intent is: {intent}"
        
        if context and context.get("has_context"):
            system_prompt += f"\n\nPrevious context: {context.get('last_query')}"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]
        )
        
        return response.choices[0].message.content
        """
        
        # Fallback to mock if API not configured
        if not self.api_key:
            return self._generate_mock_response(query, intent, context)
        
        return "Real LLM integration not implemented. Set use_mock=True or implement API calls."
