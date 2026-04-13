"""
FastAPI Main Application
Entry point for the AI pipeline POC
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uvicorn

from pipeline import LangraphPipeline
from context import context_manager


# Initialize FastAPI app
app = FastAPI(
    title="AI Pipeline POC",
    description="Minimal AI pipeline with Langraph-style orchestration, semantic mapping, and LLM integration",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for the web UI
app.mount("/static", StaticFiles(directory="static"), name="static")


# Request/Response models
class QueryRequest(BaseModel):
    """Request model for /query endpoint"""
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
    """Response model for /query endpoint"""
    input: str
    intent: str
    confidence: float
    response: str
    steps: list
    metadata: Dict[str, Any]
    context_used: Optional[Dict[str, Any]] = None
    success: bool
    error: Optional[str] = None


# Initialize TRUE Langraph pipeline
pipeline = LangraphPipeline()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Pipeline POC API",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Submit a query to the AI pipeline",
            "/context": "GET - View current context",
            "/context/clear": "POST - Clear context",
            "/pipeline/info": "GET - Get pipeline graph information",
            "/health": "GET - Health check"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Main endpoint: Process user query through the AI pipeline.
    
    This endpoint:
    1. Receives the query
    2. Runs it through semantic mapping
    3. Routes to appropriate handler
    4. Generates LLM response
    5. Returns structured output
    
    Args:
        request: QueryRequest with user query
        
    Returns:
        QueryResponse with processing results
    """
    try:
        # Update pipeline LLM setting if needed
        if pipeline.llm_handler.use_mock != request.use_mock_llm:
            pipeline.llm_handler.use_mock = request.use_mock_llm
        
        # Execute pipeline
        result = pipeline.execute(request.query)
        
        return QueryResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")


@app.get("/context")
async def get_context():
    """
    Get current context from the context manager.
    
    Returns:
        Current context information
    """
    return {
        "current_context": context_manager.get_context(),
        "history": context_manager.get_history()
    }


@app.post("/context/clear")
async def clear_context():
    """
    Clear all context from the context manager.
    
    Returns:
        Confirmation message
    """
    context_manager.clear_context()
    return {"message": "Context cleared successfully"}


@app.get("/pipeline/info")
async def get_pipeline_info():
    """
    Get information about the pipeline graph structure.
    
    Returns:
        Pipeline graph information
    """
    return pipeline.get_pipeline_graph_info()


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "pipeline": "operational",
        "context_manager": "operational"
    }


# Run the application
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
