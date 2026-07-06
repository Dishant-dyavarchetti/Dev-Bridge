"""
Helper classes for GitHub rate limit headers.
"""
from typing import Optional

from httpx import Response


class GitHubRateLimit:
    """Helper class to parse and store GitHub rate limit information from headers."""

    def __init__(self, limit: int, remaining: int, reset: int, used: int, resource: str):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.used = used
        self.resource = resource

    @classmethod
    def from_headers(cls, response: Response) -> Optional['GitHubRateLimit']:
        """
        Extract rate limit information from a GitHub API response.

        Args:
            response: An httpx Response object.

        Returns:
            A GitHubRateLimit instance or None if headers are not present.
        """
        limit = response.headers.get("x-ratelimit-limit")
        remaining = response.headers.get("x-ratelimit-remaining")
        reset = response.headers.get("x-ratelimit-reset")
        used = response.headers.get("x-ratelimit-used")
        resource = response.headers.get("x-ratelimit-resource")

        if limit is None or remaining is None or reset is None:
            return None

        return cls(
            limit=int(limit),
            remaining=int(remaining),
            reset=int(reset),
            used=int(used) if used else 0,
            resource=resource or "core"
        )
