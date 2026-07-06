"""
Exceptions for the GitHub integration layer.
"""

class GitHubError(Exception):
    """Base exception for all GitHub API errors."""
    pass

class GitHubAuthenticationError(GitHubError):
    """Raised when GitHub authentication fails."""
    pass

class GitHubRateLimitError(GitHubError):
    """Raised when GitHub rate limit is exceeded."""
    pass

class GitHubNotFoundError(GitHubError):
    """Raised when a GitHub resource is not found."""
    pass

class GitHubAPIError(GitHubError):
    """Raised when GitHub returns an unexpected error response."""
    pass
