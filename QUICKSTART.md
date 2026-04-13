# 🚀 Quick Start Guide

Get the AI Pipeline POC running in 3 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run the Server

```bash
python main.py
```

You should see:
```
============================================================
AI Pipeline POC - Starting Server
============================================================

Endpoints:
  - POST /query          - Submit queries
  - GET  /context        - View context
  - POST /context/clear  - Clear context
  - GET  /pipeline/info  - Pipeline info
  - GET  /health         - Health check

Access API docs at: http://localhost:8000/docs
============================================================
```

## Step 3: Test It

### Option A: Use the Interactive Docs (Easiest)

1. Open browser: http://localhost:8000/docs
2. Click on `POST /query`
3. Click "Try it out"
4. Enter a query like: `"How do I write a Python function?"`
5. Click "Execute"

### Option B: Use cURL

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Write a function to reverse a string", "use_mock_llm": true}'
```

### Option C: Run Test Suite

```bash
python test_examples.py
```

This will run all test examples and show you the pipeline in action.

## What You'll See

The API returns structured JSON with:

```json
{
  "input": "your query",
  "intent": "code_generation",
  "confidence": 0.75,
  "response": "Generated response...",
  "steps": ["receive", "map", "route", "generate", "finalize"],
  "metadata": {
    "processing_time_ms": 12.5,
    "intent_metadata": {...}
  },
  "success": true
}
```

## Try Different Query Types

### Code Generation
```
"Write a Python function to calculate factorial"
```

### Debugging
```
"My code is throwing a TypeError, how do I fix it?"
```

### General Question
```
"What is the difference between async and sync in Python?"
```

### Documentation
```
"Show me how to use FastAPI"
```

### Optimization
```
"How can I make my database queries faster?"
```

## Understanding the Flow

Each query goes through 5 steps:

1. **RECEIVE** - Validates input
2. **MAP** - Classifies intent (semantic mapping)
3. **ROUTE** - Routes to appropriate handler
4. **GENERATE** - Calls LLM (mock or real)
5. **FINALIZE** - Prepares output

## Context Continuity

The system remembers your last 5 interactions:

```bash
# First query
curl -X POST "http://localhost:8000/query" \
  -d '{"query": "Explain Python decorators"}'

# Second query - will have context from first
curl -X POST "http://localhost:8000/query" \
  -d '{"query": "Show me an example"}'

# Check what context is stored
curl "http://localhost:8000/context"
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the code - it's well-commented
- Customize intents in `mapper.py`
- Add your own pipeline steps in `pipeline.py`
- Integrate a real LLM in `llm.py`

## Troubleshooting

### Port already in use?
Change the port in `main.py`:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8001)  # Use 8001 instead
```

### Dependencies not installing?
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Need help?
Check the comments in the code - every major function is documented.

---

**That's it! You're ready to explore the AI Pipeline POC.** 🎉
