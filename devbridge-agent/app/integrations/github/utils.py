"""
Utility functions for the GitHub integration layer.
"""
import re


def parse_repository_url(url: str) -> tuple[str, str]:
    """
    Parse a GitHub repository URL and extract the owner and repository name.

    Args:
        url: The full GitHub URL (e.g., https://github.com/owner/repo)

    Returns:
        A tuple of (owner, repo)

    Raises:
        ValueError: If the URL is not a valid GitHub repository URL.
    """
    pattern = r"^(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$"
    match = re.match(pattern, url.strip())

    if not match:
        raise ValueError(f"Invalid GitHub repository URL: {url}")

    owner, repo = match.groups()
    return owner, repo
