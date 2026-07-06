"""
GitHub Service layer providing orchestration for the GitHub Integration APIs.
"""
from typing import Any

from app.integrations.github.client import GitHubClient
from app.integrations.github.contents import ContentAPI
from app.integrations.github.issues import IssueAPI
from app.integrations.github.repositories import RepositoryAPI
from app.integrations.github.search import SearchAPI


class GitHubService:
    """
    Service coordinating operations across all GitHub Integration Layer APIs.

    This service acts as a single abstraction point over the raw HTTP clients,
    preventing higher-level tools and agents from manually instantiating
    multiple endpoints. It exposes methods that return raw GitHub DTOs.
    """

    def __init__(self, client: GitHubClient):
        """
        Initialize the GitHub service.

        Args:
            client: The authenticated GitHub HTTP client.
        """
        self._repository_api = RepositoryAPI(client)
        self._content_api = ContentAPI(client)
        self._issue_api = IssueAPI(client)
        self._search_api = SearchAPI(client)

    async def get_repository(self, owner: str, repo: str) -> dict[str, Any]:
        """Fetch a specific repository."""
        return await self._repository_api.get_repository(owner, repo)

    async def search_repositories(self, query: str, sort: str | None = None, order: str | None = None, limit: int = 30) -> dict[str, Any]:
        """Search repositories based on a query."""
        return await self._search_api.search_repositories(query=query, sort=sort, order=order, per_page=limit)

    async def get_readme(self, owner: str, repo: str) -> dict[str, Any]:
        """Fetch the README for a repository."""
        return await self._content_api.get_readme(owner, repo)

    async def get_file(self, owner: str, repo: str, path: str) -> dict[str, Any]:
        """Fetch file contents from a repository."""
        return await self._content_api.get_file(owner, repo, path)

    async def list_issues(self, owner: str, repo: str, limit: int = 30) -> list[dict[str, Any]]:
        """List open issues for a repository."""
        return await self._issue_api.list_open_issues(owner, repo, per_page=limit)

    async def list_good_first_issues(self, owner: str, repo: str, limit: int = 30) -> list[dict[str, Any]]:
        """List open issues tagged as good first issues."""
        return await self._issue_api.list_good_first_issues(owner, repo, per_page=limit)
