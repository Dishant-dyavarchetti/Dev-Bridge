from enum import StrEnum

from pydantic import Field

from .base import BaseDevBridgeModel
from .confidence import Confidence
from .evidence import Evidence


class RecommendationType(StrEnum):
    """
    Represents the category of recommendation produced by an AI agent.
    """

    REPOSITORY = "REPOSITORY"
    ISSUE = "ISSUE"
    CONTRIBUTION = "CONTRIBUTION"
    LEARNING = "LEARNING"
    NEXT_ACTION = "NEXT_ACTION"


class RecommendationPriority(StrEnum):
    """
    Indicates how important a recommendation is.

    The frontend can use this value to visually prioritize recommendations.
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Recommendation(BaseDevBridgeModel):
    """
    Represents a recommendation produced by any DevBridge reasoning agent.

    Recommendations are intentionally generic so they can be reused across
    repository discovery, issue recommendation, contribution mentoring,
    learning guidance, and future agents.

    This model is designed to be directly consumable by the frontend,
    allowing recommendations to be rendered as reusable UI cards without
    additional transformation.
    """

    # Recommendation classification
    type: RecommendationType
    priority: RecommendationPriority = RecommendationPriority.MEDIUM

    # Display information
    title: str
    reason: str

    # User action
    action: str

    # Optional reference
    target_url: str | None = None

    # Suggested execution steps
    next_steps: list[str] = Field(default_factory=list)

    # Explainability
    evidence: list[Evidence] = Field(default_factory=list)

    # AI confidence
    confidence: Confidence | None = None
