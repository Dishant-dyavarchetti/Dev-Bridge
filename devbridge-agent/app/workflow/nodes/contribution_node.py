from typing import Any
from app.models.state.output_state import OutputState

class ContributionNode:
    """
    Guides users through the repository's contribution process.
    Runs the contribution mentor agent and updates the state.
    """
    def __init__(self, contribution_agent: Any = None):
        self.contribution_agent = contribution_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state
        user_request = state.get("user_request", "")

        if self.contribution_agent:
            agent_output = await ctx.run_node(self.contribution_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                from app.models.agent_outputs.contribution_output import ContributionOutput
                agent_output = ContributionOutput.model_validate(agent_output)

            outputs = state.get("outputs")
            if outputs is None:
                outputs = OutputState()
            elif isinstance(outputs, dict):
                outputs = OutputState.model_validate(outputs)
            
            outputs.contribution_output = agent_output
            state["outputs"] = outputs.model_dump()

        workflow = state.get("workflow")
        if workflow is not None:
            if isinstance(workflow, dict):
                from app.models.state.workflow_state import WorkflowState
                workflow = WorkflowState.model_validate(workflow)
            from app.models.state.workflow_state import WorkflowStage
            workflow.stage = WorkflowStage.IMPLEMENTATION
            state["workflow"] = workflow.model_dump()
