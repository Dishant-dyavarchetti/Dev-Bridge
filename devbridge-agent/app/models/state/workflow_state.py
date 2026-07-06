from enum import StrEnum

from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel


class UserIntent(StrEnum):
    """
    Represents the primary goal of the user for the current workflow.
    """

    DISCOVER_REPOSITORIES = "DISCOVER_REPOSITORIES"
    EXPLORE_REPOSITORY = "EXPLORE_REPOSITORY"
    UNDERSTAND_ARCHITECTURE = "UNDERSTAND_ARCHITECTURE"
    FIND_BEGINNER_ISSUES = "FIND_BEGINNER_ISSUES"
    CONTRIBUTE = "CONTRIBUTE"
    LEARN_PROJECT = "LEARN_PROJECT"
    ASK_QUESTION = "ASK_QUESTION"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"


class WorkflowStage(StrEnum):
    """
    Represents the current mentoring stage within the active workflow.

    Unlike UserProgress, this stage exists only for the current
    workflow execution and is discarded when the workflow ends.
    """

    DISCOVERY = "DISCOVERY"
    REPOSITORY_SELECTED = "REPOSITORY_SELECTED"
    REPOSITORY_ANALYZED = "REPOSITORY_ANALYZED"
    ISSUE_SELECTED = "ISSUE_SELECTED"
    IMPLEMENTATION = "IMPLEMENTATION"
    PULL_REQUEST = "PULL_REQUEST"
    COMPLETED = "COMPLETED"


class WorkflowState(BaseDevBridgeModel):
    """
    Represents the user's mentoring workflow for the current execution.

    This model tracks where the user currently is in the DevBridge
    mentoring process without storing repository knowledge or
    GraphFlow execution metadata.

    It is reset when a workflow finishes and should not be used
    for long-term persistence.
    """

    # User goal
    intent: UserIntent

    # Current mentoring stage
    stage: WorkflowStage = WorkflowStage.DISCOVERY

    # Selected repository (lightweight identifiers only)
    repository_url: str | None = None
    repository_name: str | None = None

    # Selected issue (lightweight identifiers only)
    current_issue_number: int | None = None
    current_issue_title: str | None = None

    # Guidance for the user
    next_recommended_step: str | None = None

    # Workflow progress
    completed_steps: list[WorkflowStage] = Field(default_factory=list)

    is_completed: bool = False
