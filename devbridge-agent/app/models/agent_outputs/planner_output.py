from pydantic import Field

from app.models.agent_outputs.base_output import BaseAgentOutput


class PlannerOutput(BaseAgentOutput):
    """
    Output produced by the Planner Agent.

    The planner determines how the user's request should be handled by
    selecting the appropriate specialized agents and defining the execution
    order for the GraphFlow workflow.
    """

    required_agents: list[str] = Field(default_factory=list)
    execution_plan: list[str] = Field(default_factory=list)
