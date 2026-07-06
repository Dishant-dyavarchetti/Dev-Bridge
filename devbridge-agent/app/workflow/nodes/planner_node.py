from typing import Any
from app.models.agent_outputs.planner_output import PlannerOutput
from app.models.state.workflow_state import WorkflowState, UserIntent

class PlannerNode:
    """
    Orchestrates user request analysis and classification.
    Runs the planner agent to determine user intent.
    """
    def __init__(self, planner_agent: Any = None):
        self.planner_agent = planner_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state

        # Ensure workflow state exists in the aggregate state
        workflow = state.get("workflow")
        if workflow is None:
            workflow = WorkflowState(intent=UserIntent.DISCOVER_REPOSITORIES)
        elif isinstance(workflow, dict):
            workflow = WorkflowState.model_validate(workflow)

        # Read the user's latest request from the state
        user_request = state.get("user_request", "")

        # Delegate reasoning to the injected AI agent using ADK dynamic run_node
        if self.planner_agent:
            agent_output = await ctx.run_node(self.planner_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                agent_output = PlannerOutput.model_validate(agent_output)
        else:
            # Return a fallback PlannerOutput if no agent is injected
            from app.models.shared.confidence import Confidence, ConfidenceLevel
            agent_output = PlannerOutput(
                summary="Default fallback planner execution.",
                confidence=Confidence(
                    level=ConfidenceLevel.LOW,
                    score=0.0,
                    reasoning="No agent was injected."
                ),
                required_agents=[],
                execution_plan=[],
                agent_id="planner_agent"
            )

        # Update WorkflowState based on the determined output
        workflow.next_recommended_step = agent_output.summary

        # Set the routing path for the orchestrator
        intent = getattr(agent_output, "intent", workflow.intent)
        if intent:
            workflow.intent = intent
            ctx.route = intent.value if hasattr(intent, "value") else str(intent)
        else:
            ctx.route = UserIntent.DISCOVER_REPOSITORIES.value

        state["workflow"] = workflow.model_dump()
