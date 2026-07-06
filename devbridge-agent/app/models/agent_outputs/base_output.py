from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel
from app.models.shared.confidence import Confidence
from app.models.shared.evidence import Evidence
from app.models.shared.recommendation import Recommendation


class BaseAgentOutput(BaseDevBridgeModel):
    """
    Common output contract shared by every reasoning agent in DevBridge.

    This model enforces a consistent, structured output format across all AI agents.
    It ensures that agents produce explainable, actionable responses without exposing
    their internal chain-of-thought or reasoning directly to the user.

    Every specialized agent output model should inherit from this class.
    """

    summary: str
    recommendations: list[Recommendation] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: Confidence
    next_actions: list[str] = Field(default_factory=list)
    agent_id: str
