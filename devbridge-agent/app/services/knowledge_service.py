"""
Knowledge Service layer providing orchestration for deterministic extractors.
"""
from typing import Any

from app.models.state.knowledge_state import KnowledgeState
from app.services.github_service import GitHubService
from app.tools.readme_knowledge.extract_readme import ReadmeKnowledgeExtractor
from app.tools.repository_knowledge.extract_repository import (
    RepositoryKnowledgeExtractor,
)

# TODO: Import IssueKnowledgeExtractor, DependencyKnowledgeExtractor, ContributionKnowledgeExtractor, ArchitectureKnowledgeExtractor when implemented and mapped to proper Pydantic models.


class KnowledgeService:
    """
    Service coordinating the execution of Knowledge Extractors to build DevBridge Context.

    This service delegates to specific Extractor instances to safely fetch and
    transform data into Knowledge Models. It never calls GitHub directly and
    never performs AI reasoning.
    """

    def __init__(
        self,
        github_service: GitHubService,
        repository_extractor: RepositoryKnowledgeExtractor,
        readme_extractor: ReadmeKnowledgeExtractor
    ):
        """
        Initialize the Knowledge Service.

        Args:
            github_service: The orchestrated GitHub service.
            repository_extractor: Extractor for RepositoryKnowledge.
            readme_extractor: Extractor for ReadmeKnowledge.
        """
        self._github = github_service
        self._repo_extractor = repository_extractor
        self._readme_extractor = readme_extractor

    async def build_repository_knowledge(self, owner: str, repo: str) -> Any:
        """Deterministically extract and return the RepositoryKnowledge model."""
        return await self._repo_extractor.extract(owner, repo)

    async def build_readme_knowledge(self, owner: str, repo: str) -> Any:
        """Deterministically extract and return the ReadmeKnowledge model."""
        return await self._readme_extractor.extract(owner, repo)

    async def build_repository_context(self, owner: str, repo: str) -> KnowledgeState:
        """
        Orchestrate all available extractors to produce a comprehensive KnowledgeState.

        This method will expand as new extractors are introduced. Currently, it
        populates the implemented RepositoryKnowledge and ReadmeKnowledge.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            The fully populated KnowledgeState.
        """
        repo_knowledge = await self.build_repository_knowledge(owner, repo)
        readme_knowledge = await self.build_readme_knowledge(owner, repo)

        # TODO: Add ArchitectureKnowledge when implemented.
        # TODO: Add DependencyKnowledge when implemented.
        # TODO: Add IssueKnowledge when implemented.
        # TODO: Add ContributionKnowledge when implemented.

        state = KnowledgeState(
            repository=repo_knowledge,
            readme=readme_knowledge
        )

        return state
