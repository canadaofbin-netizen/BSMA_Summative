from langgraph.graph import StateGraph, END
from graph_state import AgentState
from nodes import reviewer_node, auditor_node, injector_node

def route_auditor(state: AgentState) -> str:
    """
    Conditional routing logic based on Auditor's verdict and iteration limit.
    """
    if state["is_approved"]:
        return "injector"
    
    # If not approved, check iteration limit to prevent infinite loops (Max 3 retries)
    if state["iteration_count"] >= 3:
        print(f"⚠️ [System Alert] Max iterations reached for {state['article_id']}. Routing to Human-in-the-Loop.")
        return "human_review"
    
    print("🔁 Routing back to Reviewer for correction...")
    return "reviewer"

def human_review_node(state: AgentState) -> AgentState:
    print(f"[HITL] Paper {state['article_id']} placed in pending state. Requires manual intervention.")
    state["status_msg"] = "PENDING HUMAN REVIEW"
    return state

def build_graph():
    # Initialize the Graph with our TypedDict State
    workflow = StateGraph(AgentState)
    
    # Add Nodes
    workflow.add_node("reviewer", reviewer_node)
    workflow.add_node("auditor", auditor_node)
    workflow.add_node("injector", injector_node)
    workflow.add_node("human_review", human_review_node)
    
    # Define Edges (The Pipeline Flow)
    workflow.set_entry_point("reviewer")
    
    # Reviewer always passes data to Auditor
    workflow.add_edge("reviewer", "auditor")
    
    # Auditor uses conditional routing (The Critic Loop)
    workflow.add_conditional_edges(
        "auditor",
        route_auditor,
        {
            "injector": "injector",
            "reviewer": "reviewer",         # Loop back!
            "human_review": "human_review"  # Escape hatch
        }
    )
    
    # Terminal nodes
    workflow.add_edge("injector", END)
    workflow.add_edge("human_review", END)
    
    # Compile Graph
    return workflow.compile()

if __name__ == "__main__":
    print("==================================================")
    print("♾️ Starting BSMA LangGraph Pipeline")
    print("==================================================")
    
    pipeline = build_graph()
    
    # Initial State for a dummy paper
    initial_state = {
        "article_id": "BSMA0500",
        "pdf_text": "Dummy pdf text describing 82 R&D teams.",
        "verdict_json": None,
        "auditor_feedback": None,
        "is_approved": False,
        "iteration_count": 0,
        "status_msg": "Started"
    }
    
    # Execute the Graph
    final_state = pipeline.invoke(initial_state)
    print("\n✅ Final State Result:")
    print(final_state["status_msg"])
