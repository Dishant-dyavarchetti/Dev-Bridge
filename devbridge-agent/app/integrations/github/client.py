"""
Core HTTP client for the GitHub integration layer.
"""
import asyncio
import logging
from typing import Any

import httpx

from app.integrations.github.config import GitHubConfig
from app.integrations.github.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubError,
    GitHubNotFoundError,
    GitHubRateLimitError,
)

logger = logging.getLogger(__name__)

class GitHubClient:
    """
    HTTP client wrapper for the GitHub REST API.

    Provides authentication, error handling, retries, and timeouts for asynchronous requests.
    """

    def __init__(self, max_retries: int = 3, timeout: float = 10.0):
        self.max_retries = max_retries
        self.timeout = timeout
        self.base_url = GitHubConfig.get_api_url()
        self.token = GitHubConfig.get_token()

    def _build_headers(self) -> dict[str, str]:
        """Build the required headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _handle_response_errors(self, response: httpx.Response) -> None:
        """
        Check the response for errors and raise the appropriate custom exception.

        Args:
            response: The httpx.Response object.

        Raises:
            GitHubAuthenticationError: For 401 Unauthorized.
            GitHubRateLimitError: For 403 or 429 related to rate limits.
            GitHubNotFoundError: For 404 Not Found.
            GitHubAPIError: For other 4xx or 5xx errors.
        """
        if response.is_success:
            return

        status_code = response.status_code

        if status_code in (403, 429) and "x-ratelimit-remaining" in response.headers:
            if response.headers.get("x-ratelimit-remaining") == "0":
                raise GitHubRateLimitError(f"GitHub API rate limit exceeded: {response.text}")

        if status_code == 401:
            raise GitHubAuthenticationError(f"GitHub authentication failed: {response.text}")
        elif status_code == 404:
            raise GitHubNotFoundError(f"GitHub resource not found: {response.text}")

        raise GitHubAPIError(f"GitHub API error ({status_code}): {response.text}")

    async def get(self, path: str, params: dict[str, Any] | None = None) -> httpx.Response:
        """
        Execute an asynchronous GET request to the GitHub API with retry logic.

        Args:
            path: The API endpoint path (e.g., '/repos/owner/repo').
            params: Optional query parameters.

        Returns:
            The successful httpx.Response object.

        Raises:
            GitHubError: When max retries are exceeded or request fails.
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        headers = self._build_headers()

        attempt = 0
        while attempt < self.max_retries:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, headers=headers, params=params)

                    if response.status_code >= 500:
                        logger.warning(f"GitHub API server error ({response.status_code}). Retrying...")
                        attempt += 1
                        await asyncio.sleep(2 ** attempt)
                        continue

                    self._handle_response_errors(response)
                    return response

            except httpx.RequestError as e:
                logger.warning(f"Request to GitHub API failed: {e}. Retrying...")
                attempt += 1
                if attempt >= self.max_retries:
                    raise GitHubError(f"Request failed after {self.max_retries} attempts: {e}") from e
                await asyncio.sleep(2 ** attempt)

        raise GitHubError("Max retries exceeded without a successful response or terminal error.")
