from typing import Any
from app.models.state.output_state import OutputState

class RepositoryDiscoveryNode:
    """
    Help users discover suitable open-source repositories.
    Runs the discovery agent to suggest matching repositories.
    """
    def __init__(self, discovery_agent: Any = None):
        self.discovery_agent = discovery_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state
        user_request = state.get("user_request", "")

        if self.discovery_agent:
            agent_output = await ctx.run_node(self.discovery_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                from app.models.agent_outputs.repository_output import RepositoryAnalysisOutput
                agent_output = RepositoryAnalysisOutput.model_validate(agent_output)

            outputs = state.get("outputs")
            if outputs is None:
                outputs = OutputState()
            elif isinstance(outputs, dict):
                outputs = OutputState.model_validate(outputs)
            
            outputs.repository_output = agent_output
            state["outputs"] = outputs.model_dump()

        workflow = state.get("workflow")
        if workflow is not None:
            if isinstance(workflow, dict):
                from app.models.state.workflow_state import WorkflowState
                workflow = WorkflowState.model_validate(workflow)
            from app.models.state.workflow_state import WorkflowStage
            workflow.stage = WorkflowStage.DISCOVERY
            state["workflow"] = workflow.model_dump()
