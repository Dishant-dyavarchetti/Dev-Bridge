"""
Search API endpoints for the GitHub integration layer.
"""
from typing import Any

from app.integrations.github.client import GitHubClient


class SearchAPI:
    """
    API client for GitHub search operations.
    """

    def __init__(self, client: GitHubClient):
        self.client = client

    async def search_repositories(
        self, query: str, sort: str | None = None, order: str | None = None, per_page: int = 30, page: int = 1
    ) -> dict[str, Any]:
        """
        Search for repositories.

        Args:
            query: The search query.
            sort: Sort field (e.g., 'stars', 'forks', 'updated').
            order: Sort order ('asc' or 'desc').
            per_page: Number of items per page.
            page: Page number.

        Returns:
            The raw JSON search results object.
        """
        params: dict[str, Any] = {"q": query, "per_page": per_page, "page": page}
        if sort:
            params["sort"] = sort
        if order:
            params["order"] = order

        response = await self.client.get("/search/repositories", params=params)
        return response.json()
