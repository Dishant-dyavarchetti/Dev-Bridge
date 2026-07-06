"""
Deterministic extraction tool for GitHub repositories.
"""

from app.integrations.github.client import GitHubClient
from app.integrations.github.models import GitHubRepository
from app.integrations.github.repositories import RepositoryAPI
from app.models.knowledge.repository import RepositoryKnowledge, RepositoryOwner
from app.tools.base.base_extractor import BaseExtractor


class RepositoryKnowledgeExtractor(BaseExtractor[RepositoryKnowledge]):
    """
    Extractor for retrieving and mapping repository metadata.

    This extractor communicates with the GitHub REST API to fetch deterministic
    repository data, and transforms it into the DevBridge RepositoryKnowledge
    model without any AI interpretation.
    """

    def __init__(self, client: GitHubClient):
        """
        Initialize the repository extractor.

        Args:
            client: An authenticated GitHubClient instance.
        """
        self.api = RepositoryAPI(client)

    async def extract(self, owner: str, repo: str) -> RepositoryKnowledge:
        """
        Extract repository data and map to RepositoryKnowledge.

        Args:
            owner: The repository owner (user or organization).
            repo: The repository name.

        Returns:
            The deterministically mapped RepositoryKnowledge object.

        Raises:
            ValueError: If the API returns invalid data.
            GitHubError: If the underlying GitHub integration fails.
        """
        # Fetch raw JSON data from GitHub API
        raw_repo_data = await self.api.get_repository(owner, repo)

        # Parse into the GitHub DTO for validation of raw data structure
        try:
            github_repo = GitHubRepository(**raw_repo_data)
        except Exception as e:
            raise ValueError(f"Failed to parse GitHub repository data: {e}") from e

        # Extract owner details
        owner_data = github_repo.owner or {}
        repo_owner = RepositoryOwner(
            username=owner_data.get("login", ""),
            profile_url=owner_data.get("html_url"),
            owner_type=owner_data.get("type")
        )

        # safely extract license and homepage from raw_repo_data
        # (as our lightweight GitHubRepository model doesn't cover all fields explicitly)
        license_data = raw_repo_data.get("license")
        license_name = license_data.get("name") if isinstance(license_data, dict) else None

        # Map to DevBridge Knowledge model
        knowledge = RepositoryKnowledge(
            repository_name=github_repo.name,
            owner=repo_owner,
            repository_url=github_repo.html_url,
            homepage_url=raw_repo_data.get("homepage"),
            description=github_repo.description,
            primary_language=github_repo.language,
            topics=github_repo.topics,
            license=license_name,
            default_branch=raw_repo_data.get("default_branch", "main"),
            stars=github_repo.stargazers_count,
            forks=github_repo.forks_count,
            open_issues=github_repo.open_issues_count,
            is_archived=github_repo.archived,
            created_at=raw_repo_data.get("created_at"),
            updated_at=raw_repo_data.get("updated_at")
        )

        return knowledge
