"""
Semantic Mapping Layer
Maps user queries to intent categories using keyword-based classification
"""

from typing import Dict, List, Tuple
import re


class SemanticMapper:
    """
    Simple keyword-based semantic mapper.
    Maps user queries into predefined categories/intents.
    
    This is where SEMANTIC MAPPING happens - converting natural language
    into structured intent categories.
    """
    
    def __init__(self):
        # Define intent patterns with keywords
        # ORDER MATTERS: More specific intents first to avoid false positives
        self.intent_patterns = {
            "debugging": [
                r"\b(debug|fix|error|bug|issue|problem|wrong|broken|not working|throwing|exception|traceback|fails?|crash)\b",
                r"\b(typeerror|keyerror|valueerror|attributeerror|indexerror|nameerror)\b",
                r"\b(why.*not|what.*wrong|help.*fix)\b"
            ],
            "optimization": [
                r"\b(optimize|optimiz|faster|speed|performance|efficient|efficiency|slow)\b",
                r"\b(speed up|make.*faster|improve.*performance|run.*faster)\b",
                r"\b(reduce|minimize).*\b(time|memory|latency)\b"
            ],
            "documentation": [
                r"\b(document|docs|documentation|readme|guide|tutorial|manual)\b",
                r"\b(how to use|usage|instructions|reference)\b",
                r"\bshow.*documentation\b"
            ],
            "general_question": [
                r"\b(what is|what are|what's|explain|describe|tell me about|how does|how do)\b",
                r"\b(difference between|compare|versus|vs\.?)\b",
                r"\b(why|when|where|who|which)\b"
            ],
            "code_generation": [
                r"\b(write|create|generate|build|implement|develop|code)\b.*\b(function|class|method|script|program|app|api|endpoint)\b",
                r"\b(show me|give me).*\b(code|example|implementation)\b",
                r"\bwrite.*\b(code|function|class|script)\b",
                r"\bcreate.*\b(function|class|api)\b",
                r"\b(function|code).*\b(to|for).*\b(sort|reverse|calculate|find|search|filter)\b",
                r"\b(add|subtract|multiply|divide|sum|calculate|find|sort|reverse|filter)\b.*(number|list|array|string|value)",
                r"\b(number|list|array|string).*\b(add|subtract|multiply|divide|sum|calculate|find|sort|reverse|filter)\b"
            ]
        }
        
        # Default intent if no match
        self.default_intent = "general_question"
    
    def map_query(self, query: str) -> Tuple[str, float]:
        """
        Map a user query to an intent category.
        
        Args:
            query: User's input query
            
        Returns:
            Tuple of (intent, confidence_score)
        """
        query_lower = query.lower()
        
        # Score each intent
        intent_scores: Dict[str, float] = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    score += 1.0
            
            if score > 0:
                intent_scores[intent] = score
        
        # Return intent with highest score
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            # Normalize confidence (simple approach)
            confidence = min(best_intent[1] / len(self.intent_patterns[best_intent[0]]), 1.0)
            return best_intent[0], confidence
        
        # Default fallback
        return self.default_intent, 0.5
    
    def get_intent_metadata(self, intent: str) -> Dict[str, str]:
        """
        Get metadata about an intent category.
        
        Args:
            intent: Intent category
            
        Returns:
            Dictionary with intent description and handling strategy
        """
        metadata = {
            "code_generation": {
                "description": "User wants to generate or create code",
                "strategy": "Generate code with explanations"
            },
            "debugging": {
                "description": "User needs help fixing an issue",
                "strategy": "Analyze problem and suggest fixes"
            },
            "general_question": {
                "description": "User has a general question",
                "strategy": "Provide informative answer"
            },
            "documentation": {
                "description": "User needs documentation or guides",
                "strategy": "Provide structured documentation"
            },
            "optimization": {
                "description": "User wants to optimize code or process",
                "strategy": "Suggest improvements and best practices"
            }
        }
        
        return metadata.get(intent, {
            "description": "General query",
            "strategy": "Provide helpful response"
        })
