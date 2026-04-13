"""
Specialized AI Agents for Langraph Multi-Agent System

Each agent is a specialized expert that handles specific types of queries.
This demonstrates true multi-agent architecture.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """Response from an agent"""
    content: str
    agent_name: str
    confidence: float
    metadata: Dict[str, Any]


class BaseAgent:
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
    
    def process(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Process a query and return a response"""
        raise NotImplementedError("Subclasses must implement process()")


class CodeGenerationAgent(BaseAgent):
    """
    Specialized agent for code generation tasks.
    Expert in: Writing functions, algorithms, code snippets
    """
    
    def __init__(self):
        super().__init__(
            name="CodeGen Agent",
            specialty="Code Generation & Implementation"
        )
    
    def process(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Generate code based on query"""
        query_lower = query.lower()
        
        # Determine what code to generate
        if "add" in query_lower or "sum" in query_lower:
            code = self._generate_addition_code()
        elif "subtract" in query_lower:
            code = self._generate_subtraction_code()
        elif "multiply" in query_lower:
            code = self._generate_multiplication_code()
        elif "divide" in query_lower:
            code = self._generate_division_code()
        elif "sort" in query_lower:
            code = self._generate_sort_code()
        elif "reverse" in query_lower:
            code = self._generate_reverse_code()
        elif "max" in query_lower or "maximum" in query_lower:
            code = self._generate_max_code()
        elif "min" in query_lower or "minimum" in query_lower:
            code = self._generate_min_code()
        elif "average" in query_lower or "mean" in query_lower:
            code = self._generate_average_code()
        elif "filter" in query_lower or "even" in query_lower:
            code = self._generate_filter_code()
        else:
            code = self._generate_template_code()
        
        return AgentResponse(
            content=code,
            agent_name=self.name,
            confidence=0.95,
            metadata={
                "agent_type": "code_generation",
                "language": "python",
                "has_example": True
            }
        )
    
    def _generate_addition_code(self) -> str:
        return """```python
def add_numbers(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

# Example:
result = add_numbers(5, 3)
print(f"Result: {result}")  # Output: 8
```

**CodeGen Agent**: This function performs addition with type flexibility."""
    
    def _generate_subtraction_code(self) -> str:
        return """```python
def subtract_numbers(a, b):
    \"\"\"Subtract b from a and return the result.\"\"\"
    return a - b

# Example:
result = subtract_numbers(10, 4)
print(f"Result: {result}")  # Output: 6
```

**CodeGen Agent**: Clean subtraction implementation."""
    
    def _generate_multiplication_code(self) -> str:
        return """```python
def multiply_numbers(a, b):
    \"\"\"Multiply two numbers and return the result.\"\"\"
    return a * b

# Example:
result = multiply_numbers(6, 7)
print(f"Result: {result}")  # Output: 42
```

**CodeGen Agent**: Efficient multiplication function."""
    
    def _generate_division_code(self) -> str:
        return """```python
def divide_numbers(a, b):
    \"\"\"Divide a by b with zero-division handling.\"\"\"
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Example:
result = divide_numbers(20, 4)
print(f"Result: {result}")  # Output: 5.0
```

**CodeGen Agent**: Safe division with error handling."""
    
    def _generate_sort_code(self) -> str:
        return """```python
def sort_list(items, reverse=False):
    \"\"\"Sort a list in ascending or descending order.\"\"\"
    return sorted(items, reverse=reverse)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
sorted_asc = sort_list(numbers)
sorted_desc = sort_list(numbers, reverse=True)
print(f"Ascending: {sorted_asc}")   # [1, 2, 3, 5, 8, 9]
print(f"Descending: {sorted_desc}") # [9, 8, 5, 3, 2, 1]
```

**CodeGen Agent**: Flexible sorting with O(n log n) complexity."""
    
    def _generate_reverse_code(self) -> str:
        return """```python
def reverse_list(items):
    \"\"\"Reverse the order of items in a list.\"\"\"
    return items[::-1]

# Example:
numbers = [1, 2, 3, 4, 5]
reversed_nums = reverse_list(numbers)
print(f"Reversed: {reversed_nums}")  # [5, 4, 3, 2, 1]
```

**CodeGen Agent**: Pythonic reversal using slice notation."""
    
    def _generate_max_code(self) -> str:
        return """```python
def find_maximum(numbers):
    \"\"\"Find the maximum value in a list.\"\"\"
    if not numbers:
        raise ValueError("List cannot be empty")
    return max(numbers)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
maximum = find_maximum(numbers)
print(f"Maximum: {maximum}")  # Output: 9
```

**CodeGen Agent**: Robust max finder with validation."""
    
    def _generate_min_code(self) -> str:
        return """```python
def find_minimum(numbers):
    \"\"\"Find the minimum value in a list.\"\"\"
    if not numbers:
        raise ValueError("List cannot be empty")
    return min(numbers)

# Example:
numbers = [5, 2, 8, 1, 9, 3]
minimum = find_minimum(numbers)
print(f"Minimum: {minimum}")  # Output: 1
```

**CodeGen Agent**: Efficient minimum value finder."""
    
    def _generate_average_code(self) -> str:
        return """```python
def calculate_average(numbers):
    \"\"\"Calculate the average of a list of numbers.\"\"\"
    if not numbers:
        raise ValueError("List cannot be empty")
    return sum(numbers) / len(numbers)

# Example:
numbers = [10, 20, 30, 40, 50]
avg = calculate_average(numbers)
print(f"Average: {avg}")  # Output: 30.0
```

**CodeGen Agent**: Statistical average calculation."""
    
    def _generate_filter_code(self) -> str:
        return """```python
def filter_even_numbers(numbers):
    \"\"\"Filter and return only even numbers from a list.\"\"\"
    return [n for n in numbers if n % 2 == 0]

# Example:
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
evens = filter_even_numbers(numbers)
print(f"Even numbers: {evens}")  # [2, 4, 6, 8]
```

**CodeGen Agent**: List comprehension for efficient filtering."""
    
    def _generate_template_code(self) -> str:
        return """```python
def process_data(data):
    \"\"\"Generic data processing function.\"\"\"
    # Add your custom logic here
    result = data
    return result

# Example:
output = process_data("input")
print(output)
```

**CodeGen Agent**: Template for custom implementations.
Try specific queries like: "add two numbers", "sort a list", "find maximum"."""


class DebuggingAgent(BaseAgent):
    """
    Specialized agent for debugging and troubleshooting.
    Expert in: Error analysis, bug fixing, code review
    """
    
    def __init__(self):
        super().__init__(
            name="Debug Agent",
            specialty="Debugging & Troubleshooting"
        )
    
    def process(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Provide debugging assistance"""
        
        response = """**Debug Agent - Systematic Troubleshooting**

🔍 **Step-by-Step Debugging Process:**

1. **Read the Error Message**
   - Identify the error type (TypeError, ValueError, etc.)
   - Note the line number where it occurred
   - Understand what the error is telling you

2. **Check Recent Changes**
   - What did you modify last?
   - Did you add new dependencies?
   - Review your git diff

3. **Isolate the Problem**
   - Comment out sections of code
   - Add print statements to track values
   - Use a debugger (pdb, IDE debugger)

4. **Common Issues & Fixes:**
   ```python
   # Issue: None type error
   if variable is not None:
       result = variable.method()
   
   # Issue: Index out of range
   if index < len(my_list):
       item = my_list[index]
   
   # Issue: Key error in dict
   value = my_dict.get('key', default_value)
   ```

5. **Verify the Fix**
   - Run tests
   - Check edge cases
   - Ensure no regression

**Need specific help?** Share:
- Error message
- Code snippet
- What you expected vs what happened

**Debug Agent** is ready to help you solve this! 🐛
"""
        
        return AgentResponse(
            content=response,
            agent_name=self.name,
            confidence=0.90,
            metadata={
                "agent_type": "debugging",
                "provides_steps": True,
                "interactive": True
            }
        )


class DocumentationAgent(BaseAgent):
    """
    Specialized agent for documentation and explanations.
    Expert in: Concept explanations, API docs, tutorials
    """
    
    def __init__(self):
        super().__init__(
            name="Docs Agent",
            specialty="Documentation & Education"
        )
    
    def process(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Provide documentation and explanations"""
        
        query_lower = query.lower()
        
        if "list" in query_lower and "python" in query_lower:
            response = self._explain_lists()
        elif "function" in query_lower:
            response = self._explain_functions()
        elif "loop" in query_lower:
            response = self._explain_loops()
        else:
            response = self._general_explanation(query)
        
        return AgentResponse(
            content=response,
            agent_name=self.name,
            confidence=0.88,
            metadata={
                "agent_type": "documentation",
                "educational": True,
                "has_examples": True
            }
        )
    
    def _explain_lists(self) -> str:
        return """**Docs Agent - Python Lists Explained**

📚 **What is a List?**
A list is a mutable, ordered collection of items in Python.

**Key Features:**
- ✅ Ordered (maintains insertion order)
- ✅ Mutable (can be changed after creation)
- ✅ Allows duplicates
- ✅ Can contain mixed types

**Examples:**
```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
empty = []

# Common operations
numbers.append(6)        # Add to end
numbers.insert(0, 0)     # Insert at position
numbers.remove(3)        # Remove value
popped = numbers.pop()   # Remove and return last

# Accessing
first = numbers[0]       # First item
last = numbers[-1]       # Last item
slice = numbers[1:4]     # Slice [start:end]

# Iteration
for num in numbers:
    print(num)
```

**Docs Agent**: Lists are fundamental Python data structures!
"""
    
    def _explain_functions(self) -> str:
        return """**Docs Agent - Python Functions Explained**

📚 **What is a Function?**
A reusable block of code that performs a specific task.

**Anatomy:**
```python
def function_name(parameters):
    \"\"\"Docstring: What the function does\"\"\"
    # Function body
    result = parameters * 2
    return result  # Optional return value
```

**Key Concepts:**
- **Parameters**: Input values
- **Return**: Output value
- **Scope**: Variables inside are local
- **Docstring**: Documentation

**Examples:**
```python
# Simple function
def greet(name):
    return f"Hello, {name}!"

# Default parameters
def power(base, exponent=2):
    return base ** exponent

# Multiple returns
def min_max(numbers):
    return min(numbers), max(numbers)

# Usage
message = greet("Alice")
squared = power(5)
minimum, maximum = min_max([1, 2, 3])
```

**Docs Agent**: Functions make code reusable and organized!
"""
    
    def _explain_loops(self) -> str:
        return """**Docs Agent - Python Loops Explained**

📚 **What are Loops?**
Constructs that repeat code multiple times.

**For Loop** (iterate over sequence):
```python
# Iterate over list
for item in [1, 2, 3]:
    print(item)

# Iterate with index
for i, item in enumerate(['a', 'b', 'c']):
    print(f"{i}: {item}")

# Range
for i in range(5):  # 0 to 4
    print(i)
```

**While Loop** (repeat while condition is true):
```python
count = 0
while count < 5:
    print(count)
    count += 1
```

**Loop Control:**
```python
for i in range(10):
    if i == 3:
        continue  # Skip to next iteration
    if i == 7:
        break     # Exit loop
    print(i)
```

**Docs Agent**: Loops automate repetitive tasks!
"""
    
    def _general_explanation(self, query: str) -> str:
        return f"""**Docs Agent - General Information**

📚 You asked about: "{query}"

**How I Can Help:**
- Explain Python concepts (lists, functions, loops, etc.)
- Provide code examples
- Clarify programming terminology
- Offer best practices

**Try asking:**
- "What is a list in Python?"
- "How do functions work?"
- "Explain loops"
- "What are dictionaries?"

**Docs Agent** is here to educate and clarify! 📖
"""


class OptimizationAgent(BaseAgent):
    """
    Specialized agent for performance optimization.
    Expert in: Code efficiency, best practices, performance tuning
    """
    
    def __init__(self):
        super().__init__(
            name="Optimization Agent",
            specialty="Performance & Best Practices"
        )
    
    def process(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Provide optimization advice"""
        
        response = """**Optimization Agent - Performance Tips**

⚡ **Code Optimization Strategies:**

**1. Use Built-in Functions**
```python
# Slow
result = []
for i in range(1000):
    result.append(i * 2)

# Fast
result = [i * 2 for i in range(1000)]

# Faster
result = list(map(lambda x: x * 2, range(1000)))
```

**2. Avoid Repeated Calculations**
```python
# Slow
for i in range(len(data)):
    process(expensive_function())

# Fast
cached = expensive_function()
for i in range(len(data)):
    process(cached)
```

**3. Use Generators for Large Data**
```python
# Memory intensive
def get_numbers():
    return [i for i in range(1000000)]

# Memory efficient
def get_numbers():
    return (i for i in range(1000000))
```

**4. Choose Right Data Structure**
- Lists: Ordered, indexed access
- Sets: Fast membership testing
- Dicts: Fast key-value lookup
- Deque: Fast append/pop from both ends

**5. Profile Before Optimizing**
```python
import time

start = time.time()
# Your code here
end = time.time()
print(f"Execution time: {end - start}s")
```

**Optimization Agent**: Premature optimization is the root of all evil.
Measure first, then optimize! ⚡
"""
        
        return AgentResponse(
            content=response,
            agent_name=self.name,
            confidence=0.85,
            metadata={
                "agent_type": "optimization",
                "provides_examples": True,
                "actionable": True
            }
        )


# Agent registry - maps intent to agent
AGENT_REGISTRY = {
    "code_generation": CodeGenerationAgent(),
    "debugging": DebuggingAgent(),
    "general_question": DocumentationAgent(),
    "documentation": DocumentationAgent(),
    "optimization": OptimizationAgent()
}


def get_agent(intent: str) -> BaseAgent:
    """Get the appropriate agent for an intent"""
    return AGENT_REGISTRY.get(intent, DocumentationAgent())
