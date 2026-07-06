from app.models.agent_outputs.contribution_output import ContributionOutput
from app.models.agent_outputs.issue_output import IssueRecommendationOutput
from app.models.agent_outputs.planner_output import PlannerOutput
from app.models.agent_outputs.repository_output import RepositoryAnalysisOutput
from app.models.agent_outputs.response_output import ResponseComposerOutput
from app.models.agent_outputs.security_output import SecurityOutput
from app.models.shared.base import BaseDevBridgeModel


class OutputState(BaseDevBridgeModel):
    """
    Stores the semantic output payloads produced by DevBridge AI reasoning agents.

    Following Clean Architecture principles, this state strictly separates the
    domain-specific outputs (e.g., recommendations, explanations, next steps)
    from the mechanical execution metadata tracked by GraphFlow's ExecutionState.

    All fields are optional as they are populated incrementally throughout
    the GraphFlow execution lifecycle by specialized agents.
    """

    security_output: SecurityOutput | None = None
    planner_output: PlannerOutput | None = None
    repository_output: RepositoryAnalysisOutput | None = None
    contribution_output: ContributionOutput | None = None
    issue_output: IssueRecommendationOutput | None = None
    response_output: ResponseComposerOutput | None = None
