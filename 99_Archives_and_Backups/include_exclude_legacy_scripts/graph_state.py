from typing import TypedDict, Optional, Dict

class AgentState(TypedDict):
    """
    The state of the graph. It holds the data that is passed between nodes.
    """
    article_id: str
    pdf_text: str
    
    # Reviewer's output
    verdict_json: Optional[Dict[str, str]]
    
    # Auditor's feedback
    auditor_feedback: Optional[str]
    is_approved: bool
    
    # Loop counter to prevent infinite ping-pong between Reviewer and Auditor
    iteration_count: int
    
    # Status message
    status_msg: str
