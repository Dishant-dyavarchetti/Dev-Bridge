from typing import Any
from app.models.state.output_state import OutputState

class RepositoryAnalysisNode:
    """
    Analyze and explain an unfamiliar repository.
    Runs the repository analysis agent and updates the state.
    """
    def __init__(self, analysis_agent: Any = None):
        self.analysis_agent = analysis_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state
        user_request = state.get("user_request", "")

        if self.analysis_agent:
            agent_output = await ctx.run_node(self.analysis_agent, node_input=user_request)
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
            workflow.stage = WorkflowStage.REPOSITORY_ANALYZED
            state["workflow"] = workflow.model_dump()
