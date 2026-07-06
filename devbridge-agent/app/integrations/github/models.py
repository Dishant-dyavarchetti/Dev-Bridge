"""
Pydantic models representing raw GitHub API responses.
"""
from typing import Any

from pydantic import BaseModel, Field


class GitHubRepository(BaseModel):
    """Lightweight representation of a GitHub repository from the API."""
    name: str
    owner: dict[str, Any]
    html_url: str
    description: str | None = None
    language: str | None = None
    stargazers_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0
    archived: bool = False
    topics: list[str] = Field(default_factory=list)

class GitHubIssue(BaseModel):
    """Lightweight representation of a GitHub issue from the API."""
    number: int
    title: str
    state: str
    html_url: str
    user: dict[str, Any]
    body: str | None = None
    labels: list[dict[str, Any]] = Field(default_factory=list)

class GitHubContent(BaseModel):
    """Lightweight representation of GitHub content (file or directory)."""
    type: str
    encoding: str | None = None
    size: int
    name: str
    path: str
    content: str | None = None
    sha: str
