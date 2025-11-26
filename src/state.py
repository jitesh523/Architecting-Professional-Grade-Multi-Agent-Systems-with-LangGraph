import operator
from typing import Annotated, List, TypedDict, Optional

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    next_step: Optional[str]
    error_count: int
