from __future__ import annotations

from datetime import datetime

from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel


class RepositoryKnowledge(BaseDevBridgeModel):
    """
    Represents repository metadata extracted from GitHub.

    This model is produced exclusively by deterministic extraction tools.
    It contains factual metadata about a repository and does NOT contain
    any AI reasoning, summaries, recommendations, or interpretations.
    """

    repository_name: str
    owner: RepositoryOwner
    repository_url: str
    homepage_url: str | None = None

    description: str | None = None
    primary_language: str | None = None
    topics: list[str] = Field(default_factory=list)
    license: str | None = None
    default_branch: str
    stars: int = 0
    forks: int = 0
    open_issues: int = 0

    is_archived: bool = False

    created_at: datetime | None = None
    updated_at: datetime | None = None


class RepositoryOwner(BaseDevBridgeModel):
    username: str
    profile_url: str | None = None
    owner_type: str | None = None   # User or Organization
