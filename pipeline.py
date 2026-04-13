"""
TRUE Langraph Implementation - Multi-Agent Graph Orchestration

This module implements REAL Langraph concepts:
- Multiple specialized agents (nodes)
- Conditional routing based on state
- Graph-based execution flow
- State management through the graph
- Agent coordination and handoffs
"""

from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import time

from mapper import SemanticMapper
from agents import get_agent, BaseAgent
from context import context_manager


@dataclass
class GraphState:
    """
    State object that flows through the Langraph.
    
    This is the TRUE Langraph State:
    - Carries all information through the graph
    - Modified by each agent (node)
    - Tracks routing decisions
    - Maintains execution history
    """
    # Input
    query: str
    
    # Semantic mapping results
    intent: str = ""
    confidence: float = 0.0
    
    # Agent execution
    current_agent: str = ""
    agent_response: str = ""
    agents_visited: List[str] = field(default_factory=list)
    
    # Graph execution
    graph_path: List[str] = field(default_factory=list)
    routing_decisions: List[Dict[str, str]] = field(default_factory=list)
    
    # Context (MCP)
    context: List[Dict[str, Any]] = field(default_factory=list)
    
    # Output
    final_response: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Error handling
    error: str = ""
    
    # Timing
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    execution_time: float = 0.0


class LangraphPipeline:
    """
    TRUE Langraph Multi-Agent Orchestrator.
    
    This implements REAL Langraph with:
    - Multiple specialized agents (nodes)
    - Conditional routing based on intent
    - Graph-based execution flow
    - Agent coordination
    """
    
    def __init__(self):
        """
        Initialize Langraph with semantic mapper and agent registry.
        """
        self.mapper = SemanticMapper()
        
        # Define the Langraph execution graph
        # This is the TRUE Langraph structure with conditional routing
        self.graph_nodes = {
            "entry": self._entry_node,
            "semantic_classifier": self._semantic_classifier_node,
            "router": self._router_node,
            "code_agent": self._code_agent_node,
            "debug_agent": self._debug_agent_node,
            "docs_agent": self._docs_agent_node,
            "optimization_agent": self._optimization_agent_node,
            "validator": self._validator_node,
            "exit": self._exit_node
        }
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute the Langraph with multi-agent routing.
        
        This is TRUE Langraph execution:
        - Starts at entry node
        - Routes through semantic classifier
        - Conditionally routes to specialized agents
        - All agents converge at validator
        - Exits with final response
        
        Args:
            query: User's input query
            
        Returns:
            Dictionary with execution results
        """
        start_time = time.time()
        
        # Initialize graph state
        state = GraphState(query=query)
        
        # Get MCP context from previous interactions
        state.context = context_manager.get_context()
        
        # Execute graph: entry → classifier → router → agent → validator → exit
        try:
            # Node 1: Entry
            state = self.graph_nodes["entry"](state)
            state.graph_path.append("entry")
            
            # Node 2: Semantic Classifier
            state = self.graph_nodes["semantic_classifier"](state)
            state.graph_path.append("semantic_classifier")
            
            # Node 3: Router (conditional routing happens here)
            state = self.graph_nodes["router"](state)
            state.graph_path.append("router")
            
            # Node 4: Agent execution (determined by router)
            agent_node = self._get_agent_node(state.intent)
            state = self.graph_nodes[agent_node](state)
            state.graph_path.append(agent_node)
            
            # Node 5: Validator
            state = self.graph_nodes["validator"](state)
            state.graph_path.append("validator")
            
            # Node 6: Exit
            state = self.graph_nodes["exit"](state)
            state.graph_path.append("exit")
            
        except Exception as e:
            state.error = f"Graph execution error: {str(e)}"
        
        # Calculate execution time
        state.execution_time = time.time() - start_time
        
        # Update MCP context with results
        if not state.error:
            context_manager.update_context(
                query=state.query,
                intent=state.intent,
                response={"text": state.final_response, "agent": state.current_agent}
            )
        
        # Return formatted output
        return self._format_output(state)
    
    def _entry_node(self, state: GraphState) -> GraphState:
        """
        Entry node: Validate and prepare query.
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state
        """
        if not state.query or not state.query.strip():
            state.error = "Empty query provided"
            return state
        
        state.metadata["query_length"] = len(state.query)
        state.metadata["graph_type"] = "multi_agent_langraph"
        
        return state
    
    def _semantic_classifier_node(self, state: GraphState) -> GraphState:
        """
        Semantic Classifier Node: Detect user intent.
        
        This is where SEMANTIC MAPPING happens.
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with intent classification
        """
        # Use semantic mapper to classify intent
        intent, confidence = self.mapper.map_query(state.query)
        
        state.intent = intent
        state.confidence = confidence
        
        # Get intent metadata
        intent_metadata = self.mapper.get_intent_metadata(intent)
        state.metadata["intent_metadata"] = intent_metadata
        state.metadata["semantic_confidence"] = confidence
        
        return state
    
    def _router_node(self, state: GraphState) -> GraphState:
        """
        Router Node: Conditional routing to specialized agents.
        
        This is TRUE Langraph CONDITIONAL ROUTING.
        Based on intent, routes to different agent nodes.
        
        Args:
            state: Current graph state
            
        Returns:
            Updated state with routing decision
        """
        # Determine which agent to route to
        agent_mapping = {
            "code_generation": "code_agent",
            "debugging": "debug_agent",
            "general_question": "docs_agent",
            "documentation": "docs_agent",
            "optimization": "optimization_agent"
        }
        
        target_agent = agent_mapping.get(state.intent, "docs_agent")
        
        # Record routing decision
        state.routing_decisions.append({
            "from": "router",
            "to": target_agent,
            "reason": f"Intent: {state.intent}",
            "confidence": state.confidence
        })
        
        state.metadata["routed_to_agent"] = target_agent
        
        return state
    
    def _get_agent_node(self, intent: str) -> str:
        """Get the agent node name for an intent"""
        mapping = {
            "code_generation": "code_agent",
            "debugging": "debug_agent",
            "general_question": "docs_agent",
            "documentation": "docs_agent",
            "optimization": "optimization_agent"
        }
        return mapping.get(intent, "docs_agent")
    
    def _code_agent_node(self, state: GraphState) -> GraphState:
        """Code Generation Agent Node"""
        agent = get_agent("code_generation")
        response = agent.process(state.query, state.context)
        
        state.current_agent = response.agent_name
        state.agent_response = response.content
        state.agents_visited.append(response.agent_name)
        state.metadata["agent_metadata"] = response.metadata
        
        return state
    
    def _debug_agent_node(self, state: GraphState) -> GraphState:
        """Debugging Agent Node"""
        agent = get_agent("debugging")
        response = agent.process(state.query, state.context)
        
        state.current_agent = response.agent_name
        state.agent_response = response.content
        state.agents_visited.append(response.agent_name)
        state.metadata["agent_metadata"] = response.metadata
        
        return state
    
    def _docs_agent_node(self, state: GraphState) -> GraphState:
        """Documentation Agent Node"""
        agent = get_agent("general_question")
        response = agent.process(state.query, state.context)
        
        state.current_agent = response.agent_name
        state.agent_response = response.content
        state.agents_visited.append(response.agent_name)
        state.metadata["agent_metadata"] = response.metadata
        
        return state
    
    def _optimization_agent_node(self, state: GraphState) -> GraphState:
        """Optimization Agent Node"""
        agent = get_agent("optimization")
        response = agent.process(state.query, state.context)
        
        state.current_agent = response.agent_name
        state.agent_response = response.content
        state.agents_visited.append(response.agent_name)
        state.metadata["agent_metadata"] = response.metadata
        
        return state
    
    def _validator_node(self, state: GraphState) -> GraphState:
        """
        Validator Node: Validate agent response.
        
        All agents converge here for validation.
        
        Args:
            state: Current graph state
            
        Returns:
            Validated state
        """
        # Validate response exists
        if not state.agent_response:
            state.error = "No response from agent"
            return state
        
        # Add validation metadata
        state.metadata["validated"] = True
        state.metadata["response_length"] = len(state.agent_response)
        
        return state
    
    def _exit_node(self, state: GraphState) -> GraphState:
        """
        Exit Node: Prepare final output.
        
        Args:
            state: Current graph state
            
        Returns:
            Final state
        """
        # Set final response
        state.final_response = state.agent_response
        
        # Add execution summary
        state.metadata["total_agents_visited"] = len(state.agents_visited)
        state.metadata["graph_path_length"] = len(state.graph_path)
        
        return state
    
    def _format_output(self, state: GraphState) -> Dict[str, Any]:
        """
        Format graph state into output JSON.
        
        Args:
            state: Final graph state
            
        Returns:
            Formatted output dictionary
        """
        output = {
            "input": state.query,
            "intent": state.intent,
            "confidence": state.confidence,
            "response": state.final_response,
            "agent": state.current_agent,
            "graph_execution": {
                "path": state.graph_path,
                "agents_visited": state.agents_visited,
                "routing_decisions": state.routing_decisions
            },
            "execution_time_ms": round(state.execution_time * 1000, 2),
            "metadata": state.metadata
        }
        
        # Add MCP context info if available
        if state.context.get("has_context"):
            output["context_used"] = {
                "previous_query": state.context.get("last_query"),
                "previous_intent": state.context.get("last_intent")
            }
        
        # Add error if present
        if state.error:
            output["error"] = state.error
            output["success"] = False
        else:
            output["success"] = True
        
        return output
    
    def get_graph_info(self) -> Dict[str, Any]:
        """
        Get information about the Langraph structure.
        Useful for visualization and debugging.
        
        Returns:
            Graph structure information
        """
        return {
            "graph_type": "Multi-Agent Langraph",
            "nodes": list(self.graph_nodes.keys()),
            "total_nodes": len(self.graph_nodes),
            "agent_nodes": [
                "code_agent",
                "debug_agent",
                "docs_agent",
                "optimization_agent"
            ],
            "execution_flow": [
                "entry",
                "semantic_classifier",
                "router",
                "[conditional: agent]",
                "validator",
                "exit"
            ],
            "description": "TRUE Langraph with multi-agent conditional routing"
        }
