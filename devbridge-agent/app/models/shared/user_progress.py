from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from .base import BaseDevBridgeModel


class ExperienceLevel(StrEnum):
    """
    Represents the developer's overall open-source experience.

    This is NOT tied to a specific repository or workflow.
    It reflects the user's long-term growth as an open-source contributor.
    """

    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    MAINTAINER = "MAINTAINER"


class UserProgress(BaseDevBridgeModel):
    """
    Represents a user's long-term mentoring progress.

    This model captures persistent contribution history across multiple
    repositories and mentoring sessions. It is intended to be stored
    by persistence services and restored whenever the user resumes
    their DevBridge journey.

    It does NOT represent the current workflow state of a repository.
    """

    # Overall experience
    experience_level: ExperienceLevel = ExperienceLevel.BEGINNER

    # Contribution statistics
    repositories_contributed: int = 0
    issues_completed: int = 0
    pull_requests_created: int = 0
    pull_requests_merged: int = 0

    # Learning progress
    completed_milestones: list[str] = Field(default_factory=list)

    # Repository history
    completed_repositories: list[RepositoryProgress]

    # Current learning goals
    learning_goals: list[str] = Field(default_factory=list)


class RepositoryProgress(BaseDevBridgeModel):
    repository_name: str
    repository_url: str
    completed_at: datetime | None = None
