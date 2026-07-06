from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel


class ReadmeKnowledge(BaseDevBridgeModel):
    """
    Represents structured information extracted from a repository's README.md.

    This model stores categorized sections of the README to avoid passing raw,
    unstructured markdown into the agent context. It is produced solely by
    deterministic extraction tools and contains only factual information.
    """

    title: str
    overview: str | None = None
    installation: str | None = None
    usage: str | None = None
    features: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    documentation_links: list[str] = Field(default_factory=list)
