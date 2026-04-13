"""
MCP-style Context Manager
Maintains conversation context across requests
"""

from typing import Optional, Dict, Any
from datetime import datetime


class ContextManager:
    """
    Lightweight context manager that stores the last query and response.
    This simulates MCP (Model Context Protocol) by maintaining state across requests.
    """
    
    def __init__(self):
        self.last_query: Optional[str] = None
        self.last_response: Optional[Dict[str, Any]] = None
        self.last_intent: Optional[str] = None
        self.timestamp: Optional[str] = None
        self.history: list = []  # Store last 5 interactions
        self.max_history = 5
    
    def update_context(self, query: str, intent: str, response: Dict[str, Any]):
        """
        Update the context with the latest interaction.
        
        Args:
            query: User's input query
            intent: Detected intent/category
            response: Generated response
        """
        self.last_query = query
        self.last_intent = intent
        self.last_response = response
        self.timestamp = datetime.now().isoformat()
        
        # Add to history
        self.history.append({
            "query": query,
            "intent": intent,
            "response": response,
            "timestamp": self.timestamp
        })
        
        # Keep only last N interactions
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def get_context(self) -> Dict[str, Any]:
        """
        Retrieve current context for the next request.
        
        Returns:
            Dictionary containing context information
        """
        return {
            "last_query": self.last_query,
            "last_intent": self.last_intent,
            "last_response": self.last_response,
            "timestamp": self.timestamp,
            "has_context": self.last_query is not None
        }
    
    def get_history(self) -> list:
        """Get conversation history"""
        return self.history
    
    def clear_context(self):
        """Clear all context"""
        self.last_query = None
        self.last_response = None
        self.last_intent = None
        self.timestamp = None
        self.history = []


# Global context manager instance
context_manager = ContextManager()
