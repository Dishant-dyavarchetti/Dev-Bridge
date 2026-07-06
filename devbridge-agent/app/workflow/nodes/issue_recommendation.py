from typing import Any
from app.models.state.output_state import OutputState

class IssueRecommendationNode:
    """
    Recommend suitable issues for contribution.
    Runs the issue recommendation agent and updates the state.
    """
    def __init__(self, issue_agent: Any = None):
        self.issue_agent = issue_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state
        user_request = state.get("user_request", "")

        if self.issue_agent:
            import asyncio
            # Space out parallel executions to prevent concurrent rate limit triggers
            await asyncio.sleep(5.0)
            agent_output = await ctx.run_node(self.issue_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                from app.models.agent_outputs.issue_output import IssueRecommendationOutput
                agent_output = IssueRecommendationOutput.model_validate(agent_output)

            outputs = state.get("outputs")
            if outputs is None:
                outputs = OutputState()
            elif isinstance(outputs, dict):
                outputs = OutputState.model_validate(outputs)
            
            outputs.issue_output = agent_output
            state["outputs"] = outputs.model_dump()

        workflow = state.get("workflow")
        if workflow is not None:
            if isinstance(workflow, dict):
                from app.models.state.workflow_state import WorkflowState
                workflow = WorkflowState.model_validate(workflow)
            from app.models.state.workflow_state import WorkflowStage
            workflow.stage = WorkflowStage.ISSUE_SELECTED
            state["workflow"] = workflow.model_dump()
