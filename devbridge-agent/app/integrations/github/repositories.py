"""
Repository API endpoints for the GitHub integration layer.
"""
from typing import Any

from app.integrations.github.client import GitHubClient


class RepositoryAPI:
    """
    API client for GitHub repository operations.
    """

    def __init__(self, client: GitHubClient):
        self.client = client

    async def get_repository(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Get details of a specific repository.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            The raw JSON response from GitHub API representing the repository.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}")
        return response.json()

    async def get_languages(self, owner: str, repo: str) -> dict[str, int]:
        """
        Get language statistics for a repository.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            The raw JSON response representing languages and byte counts.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/languages")
        return response.json()

    async def get_topics(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Get topics for a repository.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            The raw JSON response representing topics.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/topics")
        return response.json()
