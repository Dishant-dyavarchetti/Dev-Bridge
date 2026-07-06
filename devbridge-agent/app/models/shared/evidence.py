from enum import StrEnum

from .base import BaseDevBridgeModel


class EvidenceType(StrEnum):
    """Types of evidence that can support reasoning."""
    FILE = "FILE"
    ISSUE = "ISSUE"
    PULL_REQUEST = "PULL_REQUEST"
    METADATA = "METADATA"
    EXTERNAL_DOC = "EXTERNAL_DOC"


class Evidence(BaseDevBridgeModel):
    """
    Represents evidence supporting an AI-generated explanation.

    Captures the origin of a piece of information, such as a file path
    (e.g., README.md, package.json), issue URL, or repository metadata,
    enabling agents to cite their sources and provide explainable responses.
    """
    type: EvidenceType
    artifact: str
    context: str
    excerpt: str | None = None
    reference_url: str | None = None
