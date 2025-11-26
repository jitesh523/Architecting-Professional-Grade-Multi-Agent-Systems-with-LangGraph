from typing import Dict, Any, Literal
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from .state import AgentState
import os

# Initialize tools and models
# Note: In a real production app, these should be initialized once or passed via config
try:
    search_tool = TavilySearchResults(max_results=3)
    llm = ChatOpenAI(model="gpt-4o")
except Exception:
    # Fallback for testing without keys if needed, but the plan requires keys
    search_tool = None
    llm = None

def supervisor_node(state: AgentState) -> Dict[str, Any]:
    """
    Supervisor that routes based on LLM decision.
    """
    messages = state['messages']
    
    if not llm:
        # Fallback if LLM not initialized
        last_message = messages[-1] if messages else ""
        
        # Check if the last message is from a worker to avoid loops
        if last_message.startswith("Researcher") or last_message.startswith("Coder"):
             return {"next_step": "FINISH"}

        if "research" in last_message.lower():
            return {"next_step": "researcher"}
        elif "code" in last_message.lower():
            return {"next_step": "coder"}
        return {"next_step": "FINISH"}

    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        " following workers: Researcher, Coder.\n"
        "Given the following user request, respond with the worker to act next.\n"
        "Each worker will perform a task and respond with their results and status.\n"
        "When finished, respond with FINISH."
    )
    
    # Token Optimization: Trim messages to keep context window manageable
    # We keep the last 10 messages, but always ensure the system prompt is included via the invoke call below
    trimmed_messages = trim_messages(
        messages,
        max_tokens=2000, # Approximate token limit for history
        strategy="last",
        token_counter=llm.get_num_tokens_from_messages, # Use the LLM's tokenizer method
        include_system=False, # System prompt is added separately
        allow_partial=False
    )
    
    # Simple structured output for routing
    class Router(Dict):
        next: Literal["researcher", "coder", "FINISH"]

    try:
        # In a real app we'd use with_structured_output, but for simplicity/compatibility:
        response = llm.with_structured_output(Router).invoke(
            [SystemMessage(content=system_prompt)] + trimmed_messages
        )
        return {"next_step": response["next"]}
    except Exception as e:
        print(f"Supervisor Error: {e}")
        # Fallback routing on error
        return {"next_step": "FINISH", "error_count": state.get("error_count", 0) + 1}

def research_node(state: AgentState) -> Dict[str, Any]:
    """
    Researcher node using Tavily.
    """
    try:
        messages = state['messages']
        last_message = messages[-1]
        
        if not search_tool:
            return {"messages": ["Researcher (Mock): Search tool not available."], "error_count": 0}

        # Extract query (simplistic for now)
        query = last_message
        results = search_tool.invoke(query)
        
        return {"messages": [f"Researcher: Found {len(results)} results. {results}"]}
    except Exception as e:
        return {
            "messages": [f"Researcher Error: {str(e)}"],
            "error_count": state.get("error_count", 0) + 1
        }

def code_node(state: AgentState) -> Dict[str, Any]:
    """
    Coder node using LLM to generate code.
    """
    try:
        messages = state['messages']
        
        if not llm:
            return {"messages": ["Coder (Mock): LLM not available."], "error_count": 0}

        prompt = (
            "You are an expert coder. Write python code to solve the user's request.\n"
            "Return ONLY the code block."
        )
        
        response = llm.invoke(
            [SystemMessage(content=prompt)] + [HumanMessage(content=m) for m in messages]
        )
        
        return {"messages": [f"Coder: {response.content}"]}
    except Exception as e:
        return {
            "messages": [f"Coder Error: {str(e)}"],
            "error_count": state.get("error_count", 0) + 1
        }
