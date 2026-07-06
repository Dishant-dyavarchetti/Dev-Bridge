from pydantic import Field

from app.models.agent_outputs.base_output import BaseAgentOutput


class ContributionOutput(BaseAgentOutput):
    """
    Output produced by the Contribution Mentor Agent.

    Guides users through the repository-specific contribution workflow
    and explains how to successfully contribute.
    """

    contribution_workflow: list[str] = Field(default_factory=list)

    setup_steps: list[str] = Field(default_factory=list)

    repository_rules: list[str] = Field(default_factory=list)
