"""
Content API endpoints for the GitHub integration layer.
"""
import base64
from typing import Any

from app.integrations.github.client import GitHubClient


class ContentAPI:
    """
    API client for GitHub repository content operations.
    """

    def __init__(self, client: GitHubClient):
        self.client = client

    def _decode_content(self, data: dict[str, Any]) -> dict[str, Any]:
        """Decode base64 encoded content from the API."""
        if data.get("encoding") == "base64" and "content" in data:
            data["content"] = base64.b64decode(data["content"]).decode("utf-8")
        return data

    async def get_readme(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Get the README of a repository.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            The raw JSON response from GitHub API, with base64 content decoded to plain text.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/readme")
        return self._decode_content(response.json())

    async def get_file(self, owner: str, repo: str, path: str) -> dict[str, Any]:
        """
        Get the contents of a specific file.

        Args:
            owner: The repository owner.
            repo: The repository name.
            path: The file path.

        Returns:
            The raw JSON response, with base64 content decoded to plain text.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/contents/{path}")
        data = response.json()
        if isinstance(data, list):
            raise ValueError(f"Path '{path}' is a directory, not a file.")
        return self._decode_content(data)

    async def get_directory(self, owner: str, repo: str, path: str) -> list[dict[str, Any]]:
        """
        Get the contents of a specific directory.

        Args:
            owner: The repository owner.
            repo: The repository name.
            path: The directory path.

        Returns:
            A list of raw JSON objects representing the contents of the directory.
        """
        response = await self.client.get(f"/repos/{owner}/{repo}/contents/{path}")
        data = response.json()
        if not isinstance(data, list):
            raise ValueError(f"Path '{path}' is a file, not a directory.")
        return data
