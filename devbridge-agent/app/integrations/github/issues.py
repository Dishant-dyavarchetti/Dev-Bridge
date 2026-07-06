"""
Issue API endpoints for the GitHub integration layer.
"""
from typing import Any

from app.integrations.github.client import GitHubClient


class IssueAPI:
    """
    API client for GitHub issue operations.
    """

    def __init__(self, client: GitHubClient):
        self.client = client

    async def list_open_issues(self, owner: str, repo: str, per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        """
        List open issues for a repository.

        Args:
            owner: The repository owner.
            repo: The repository name.
            per_page: Number of items per page.
            page: Page number.

        Returns:
            A list of raw JSON issue objects.
        """
        params = {"state": "open", "per_page": per_page, "page": page}
        response = await self.client.get(f"/repos/{owner}/{repo}/issues", params=params)
        return response.json()

    async def get_issue(self, owner: str, repo: str, issue_number: int) -> dict[str, Any]:
        """
        Get a specific issue.

        Args:
            owner: The repository owner.
            repo: The repository name.
            issue_number: The issue number.

        Returns:
            The raw JSON issue object.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
        return response.json()

    async def list_good_first_issues(self, owner: str, repo: str, per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        """
        List open issues labeled 'good first issue'.

        Args:
            owner: The repository owner.
            repo: The repository name.
            per_page: Number of items per page.
            page: Page number.

        Returns:
            A list of raw JSON issue objects.
        """
        params = {"state": "open", "labels": "good first issue", "per_page": per_page, "page": page}
        response = await self.client.get(f"/repos/{owner}/{repo}/issues", params=params)
        return response.json()
