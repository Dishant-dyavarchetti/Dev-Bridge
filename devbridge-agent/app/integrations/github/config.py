"""
Configuration management for the GitHub integration layer.
"""
import os


class GitHubConfig:
    """Configuration for the GitHub API integration layer."""

    @classmethod
    def get_token(cls) -> str | None:
        """Retrieve the GitHub token from the environment."""
        return os.environ.get("GITHUB_TOKEN")

    @classmethod
    def get_api_url(cls) -> str:
        """Retrieve the GitHub API base URL from the environment or use the default."""
        return os.environ.get("GITHUB_API_URL", "https://api.github.com")
