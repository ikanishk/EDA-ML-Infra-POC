# AI Pipeline POC

A minimal proof-of-concept demonstrating Langraph-style orchestration, semantic mapping, and LLM integration.

## 🎯 Overview

This POC implements a clean, explainable AI pipeline with:

- **Semantic Mapping**: Keyword-based intent classification
- **Langraph-style Orchestration**: Step-by-step state-based flow
- **LLM Integration**: Mock or real LLM responses
- **MCP-style Context**: Conversation context management
- **FastAPI**: RESTful API interface

## 📁 Project Structure

```
POC/
├── main.py          # FastAPI application & endpoints
├── pipeline.py      # Langraph-style orchestrator
├── mapper.py        # Semantic intent mapper
├── llm.py           # LLM integration handler
├── context.py       # MCP-style context manager
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

### 3. Access API Documentation

Open your browser and navigate to:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔧 API Endpoints

### POST /query
Submit a query to the AI pipeline.

**Request:**
```json
{
  "query": "How do I write a Python function to sort a list?",
  "use_mock_llm": true
}
```

**Response:**
```json
{
  "input": "How do I write a Python function to sort a list?",
  "intent": "code_generation",
  "confidence": 0.75,
  "response": "Here's a code example...",
  "steps": ["receive", "map", "route", "generate", "finalize"],
  "metadata": {
    "intent_metadata": {...},
    "processing_time_ms": 12.5
  },
  "success": true
}
```

### GET /context
View current conversation context.

### POST /context/clear
Clear all stored context.

### GET /pipeline/info
Get pipeline graph structure information.

### GET /health
Health check endpoint.

## 📊 Pipeline Flow

The pipeline follows a Langraph-style execution:

```
1. RECEIVE  → Validate and accept query
2. MAP      → Semantic intent classification
3. ROUTE    → Route to appropriate handler
4. GENERATE → LLM response generation
5. FINALIZE → Prepare final output
```

Each step transforms the state object, which flows through the pipeline.

## 🧠 Intent Categories

The semantic mapper classifies queries into:

- **code_generation**: Generate or create code
- **debugging**: Fix errors or issues
- **general_question**: Answer general questions
- **documentation**: Provide docs or guides
- **optimization**: Improve performance

## 🔄 Context Management (MCP-style)

The context manager maintains:
- Last query and response
- Conversation history (last 5 interactions)
- Intent tracking
- Timestamps

Context is automatically passed to subsequent requests for continuity.

## 🤖 LLM Integration

### Mock Mode (Default)
Uses intelligent, query-aware responses based on intent and keywords. No API key required.

**Multi-Language Support:**
The mock LLM automatically detects the programming language from your query and generates code accordingly:

- **Python** (default)
- **Java** - mention "Java" in your query
- **JavaScript** - mention "JavaScript" or "JS"
- **C++** - mention "C++" or "cpp"
- **C#** - mention "C#" or "csharp"
- **Go** - mention "Go" or "golang"
- **TypeScript** - mention "TypeScript" or "ts"

**Examples:**
- "Write a Python function to sort a list" → Python code
- "Write a Java method to reverse a string" → Java code
- "Create a JavaScript function to sort an array" → JavaScript code

### Real LLM Mode
To use a real LLM API:

1. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

2. Update `llm.py` to uncomment and implement the API calls

3. Set `use_mock_llm: false` in your requests

## 📝 Example Usage

### Using cURL

```bash
# Submit a query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Write a function to reverse a string", "use_mock_llm": true}'

# Check context
curl "http://localhost:8000/context"

# Clear context
curl -X POST "http://localhost:8000/context/clear"
```

### Using Python

```python
import requests

# Submit query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "How do I debug a Python error?",
        "use_mock_llm": True
    }
)

print(response.json())
```

### Using the Interactive Docs

1. Go to http://localhost:8000/docs
2. Click on `/query` endpoint
3. Click "Try it out"
4. Enter your query
5. Click "Execute"

## 🎨 Key Features Explained

### 1. Langraph-style Orchestration
- **State Management**: `PipelineState` object flows through nodes
- **Sequential Execution**: Each step transforms the state
- **Clear Flow**: Defined pipeline graph with named steps
- **Error Handling**: Errors stop execution gracefully

### 2. Semantic Mapping
- **Keyword-based**: Uses regex patterns for classification
- **Confidence Scoring**: Returns confidence with each classification
- **Extensible**: Easy to add new intents and patterns

### 3. MCP-style Context
- **Persistent**: Maintains state across requests
- **History**: Stores last 5 interactions
- **Automatic**: Context passed to LLM automatically

## 🛠️ Customization

### Adding New Intents

Edit `mapper.py`:

```python
self.intent_patterns = {
    # ... existing intents ...
    "new_intent": [
        r"\b(keyword1|keyword2)\b",
        r"\bpattern\b"
    ]
}
```

### Modifying Pipeline Steps

Edit `pipeline.py`:

```python
self.pipeline_graph = [
    ("receive", self._receive_query),
    ("custom_step", self._custom_function),  # Add here
    ("map", self._map_intent),
    # ... rest of steps
]
```

### Integrating Real LLM

Edit `llm.py` `_generate_real_response()` method to add your LLM API calls.

## 🧪 Testing

### Test Code Generation Query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Create a Python class for user management"}'
```

### Test Debugging Query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why is my code throwing a null pointer exception?"}'
```

### Test Context Continuity
```bash
# First query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain Python decorators"}'

# Second query (will have context from first)
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me an example"}'
```

## 📚 Architecture Highlights

### Clean Separation of Concerns
- `main.py`: API layer
- `pipeline.py`: Orchestration logic
- `mapper.py`: Intent classification
- `llm.py`: LLM interaction
- `context.py`: State management

### No Over-engineering
- ✅ No database
- ✅ No message queues
- ✅ No authentication
- ✅ Simple, readable code
- ✅ Well-commented

### Production-Ready Patterns
While minimal, this POC demonstrates:
- Proper error handling
- Structured logging potential
- Modular design
- API best practices
- State management

## 🔍 Monitoring & Debugging

The API returns detailed metadata:
- Processing time
- Steps completed
- Confidence scores
- Context usage
- Error messages

Use `/pipeline/info` to understand the execution graph.

## 📈 Next Steps

To extend this POC:

1. **Add Authentication**: Implement API keys or OAuth
2. **Add Database**: Store conversation history persistently
3. **Add Caching**: Cache common queries
4. **Add Monitoring**: Integrate logging and metrics
5. **Add Tests**: Unit and integration tests
6. **Real LLM**: Integrate OpenAI, Anthropic, etc.
7. **Advanced Routing**: Implement complex conditional flows
8. **Streaming**: Add streaming responses

## 🤝 Contributing

This is a POC for demonstration purposes. Feel free to extend and customize for your needs.

## 📄 License

MIT License - feel free to use and modify.

---

**Built with**: Python 3.8+, FastAPI, Pydantic

**Concepts Demonstrated**: Langraph orchestration, Semantic mapping, LLM integration, MCP-style context management
