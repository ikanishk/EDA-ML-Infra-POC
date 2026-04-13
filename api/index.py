from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import LangraphPipeline
from context import context_manager

app = FastAPI(
    title="AI Pipeline POC",
    description="Minimal AI pipeline with Langraph-style orchestration, semantic mapping, and LLM integration",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

class QueryRequest(BaseModel):
    query: str = Field(..., description="User's input query", min_length=1)
    use_mock_llm: bool = Field(True, description="Whether to use mock LLM responses")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How do I write a Python function to sort a list?",
                "use_mock_llm": True
            }
        }

class QueryResponse(BaseModel):
    input: str
    intent: str
    confidence: float
    response: str
    agent: Optional[str] = None
    graph_execution: Optional[Dict[str, Any]] = None
    execution_time_ms: Optional[float] = None
    metadata: Dict[str, Any]
    context_used: Optional[Dict[str, Any]] = None
    success: bool
    error: Optional[str] = None

pipeline = LangraphPipeline()

@app.get("/")
async def root():
    return {
        "message": "AI Pipeline POC API",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Submit a query to the AI pipeline",
            "/context": "GET - View current context",
            "/context/clear": "POST - Clear context",
            "/graph": "GET - Get pipeline graph information",
            "/health": "GET - Health check"
        }
    }

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    try:
        result = pipeline.execute(request.query)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")

@app.get("/context")
async def get_context():
    return {
        "current_context": context_manager.get_context(),
        "history": context_manager.get_history()
    }

@app.post("/context/clear")
async def clear_context():
    context_manager.clear_context()
    return {"message": "Context cleared successfully"}

@app.get("/graph")
async def get_graph_info():
    return pipeline.get_graph_info()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "pipeline": "operational",
        "context_manager": "operational"
    }

handler = app
