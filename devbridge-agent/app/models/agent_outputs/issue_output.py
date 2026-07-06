from pydantic import Field

from app.models.agent_outputs.base_output import BaseAgentOutput
from app.models.shared.recommendation import Recommendation


class IssueRecommendationOutput(BaseAgentOutput):
    """
    Output produced by the Issue Recommendation Agent.

    Recommends issues that best match the user's experience level and
    learning goals.
    """

    recommended_issues: list[Recommendation] = Field(default_factory=list)
