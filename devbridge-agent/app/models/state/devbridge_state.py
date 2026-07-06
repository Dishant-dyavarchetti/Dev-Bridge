from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel
from app.models.shared.user_progress import UserProgress
from app.models.state.execution_state import ExecutionState
from app.models.state.knowledge_state import KnowledgeState
from app.models.state.output_state import OutputState
from app.models.state.workflow_state import WorkflowState


class DevBridgeState(BaseDevBridgeModel):
    """
    The shared aggregate state model for DevBridge.
    Exchanged across all workflow nodes, agents, and services.
    """
    user_id: str
    user_request: str
    workflow: WorkflowState
    execution: ExecutionState = Field(default_factory=ExecutionState)
    knowledge: KnowledgeState = Field(default_factory=KnowledgeState)
    outputs: OutputState = Field(default_factory=OutputState)
    user_progress: UserProgress | None = None
