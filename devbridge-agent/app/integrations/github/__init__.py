"""
GitHub Integration Layer.

This package provides a deterministic, dependency-free wrapper around the GitHub REST API.
It returns raw data mapping to DevBridge knowledge models without any AI reasoning.
"""

from app.integrations.github.client import GitHubClient
from app.integrations.github.config import GitHubConfig
from app.integrations.github.contents import ContentAPI
from app.integrations.github.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)
from app.integrations.github.issues import IssueAPI
from app.integrations.github.models import (
    GitHubContent,
    GitHubIssue,
    GitHubRepository,
)
from app.integrations.github.rate_limit import GitHubRateLimit
from app.integrations.github.repositories import RepositoryAPI
from app.integrations.github.search import SearchAPI
from app.integrations.github.utils import parse_repository_url

__all__ = [
    "ContentAPI",
    "GitHubAPIError",
    "GitHubAuthenticationError",
    "GitHubClient",
    "GitHubConfig",
    "GitHubContent",
    "GitHubError",
    "GitHubIssue",
    "GitHubNotFoundError",
    "GitHubRateLimit",
    "GitHubRateLimitError",
    "GitHubRepository",
    "IssueAPI",
    "RepositoryAPI",
    "SearchAPI",
    "parse_repository_url",
]
