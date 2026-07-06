"""
Progress Service layer managing logic for mentoring states.
"""
from datetime import datetime
from typing import Any

from app.models.shared.user_progress import RepositoryProgress, UserProgress


class ProgressService:
    """
    Service responsible for encapsulating all mutations to the UserProgress model.

    It updates mentoring stages, completes milestones, increments stats, and
    manages repository histories without allowing AI agents to directly mutate
    the state variables.
    """

    def __init__(self, memory_service: Any = None):
        """
        Initialize the Progress Service.

        Args:
            memory_service: Optional backend for saving after mutations.
        """
        self._memory = memory_service

    def increment_contribution_count(self, progress: UserProgress) -> UserProgress:
        """
        Increment the overall completed issues count.

        Args:
            progress: The user's current progress object.

        Returns:
            The mutated UserProgress object.
        """
        progress.issues_completed += 1
        return progress

    def mark_milestone_complete(self, progress: UserProgress, milestone_name: str) -> UserProgress:
        """
        Add a milestone to the user's completed milestones.

        Args:
            progress: The user's current progress object.
            milestone_name: The name of the completed milestone.

        Returns:
            The mutated UserProgress object.
        """
        if milestone_name not in progress.completed_milestones:
            progress.completed_milestones.append(milestone_name)
        return progress

    def mark_repository_complete(self, progress: UserProgress, repo_name: str, repo_url: str) -> UserProgress:
        """
        Mark a repository as completed and log the history.

        Args:
            progress: The user's current progress object.
            repo_name: Name of the repository.
            repo_url: URL of the repository.

        Returns:
            The mutated UserProgress object.
        """
        # Check if already completed to avoid duplication
        for rp in progress.completed_repositories:
            if rp.repository_name == repo_name:
                return progress

        repo_progress = RepositoryProgress(
            repository_name=repo_name,
            repository_url=repo_url,
            # completed_at accepts the datetime value
            completed_at=datetime.utcnow()
        )
        progress.completed_repositories.append(repo_progress)
        progress.repositories_contributed += 1
        return progress

    def update_mentoring_stage(self, progress: UserProgress, new_goals: list[str]) -> UserProgress:
        """
        Update learning goals for the user.

        Args:
            progress: The user's current progress object.
            new_goals: The new active learning goals.

        Returns:
            The mutated UserProgress object.
        """
        progress.learning_goals = new_goals
        return progress
