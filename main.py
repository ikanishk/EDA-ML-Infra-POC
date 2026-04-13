from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn
import os

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

app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>AI Pipeline POC</h1><p>UI not found. Use /docs for API documentation.</p>", status_code=200)


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


if __name__ == "__main__":
    print("=" * 60)
    print("AI Pipeline POC - Langraph Multi-Agent System")
    print("=" * 60)
    print("\nWeb UI:")
    print("  http://localhost:8000/static/index.html")
    print("\nAPI Documentation:")
    print("  http://localhost:8000/docs")
    print("\nAPI Endpoints:")
    print("  - POST /query          - Submit queries")
    print("  - GET  /context        - View MCP context")
    print("  - POST /context/clear  - Clear context")
    print("  - GET  /graph          - Langraph structure")
    print("  - GET  /health         - Health check")
    print("\nFeatures:")
    print("  - TRUE Langraph with 4 specialized agents")
    print("  - Semantic intent mapping")
    print("  - MCP-style context management")
    print("  - Conditional agent routing")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
