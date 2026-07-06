from pydantic import Field

from app.models.agent_outputs.base_output import BaseAgentOutput
from app.models.shared.recommendation import Recommendation


class RepositoryAnalysisOutput(BaseAgentOutput):
    """
    Output produced by the Repository Analysis Agent or Repository Discovery Agent.
    """
    repository_name: str | None = None
    repository_url: str | None = None
    description: str | None = None
    primary_language: str | None = None
    technologies: list[str] = Field(default_factory=list)
    architecture_summary: str | None = None
    important_directories: list[str] = Field(default_factory=list)
    entry_points: list[str] = Field(default_factory=list)
    readme_summary: str | None = None
    discovered_repositories: list[Recommendation] = Field(default_factory=list)
