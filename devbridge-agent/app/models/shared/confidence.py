from enum import StrEnum

from pydantic import Field

from .base import BaseDevBridgeModel


class ConfidenceLevel(StrEnum):
    """Standardized confidence levels for AI reasoning."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Confidence(BaseDevBridgeModel):
    """
    Represents the confidence level associated with AI reasoning.

    Requires agents to explicitly state their confidence and reasoning,
    enabling safer and more transparent mentorship. Supports future extension.
    """
    level: ConfidenceLevel
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    reasoning: str
