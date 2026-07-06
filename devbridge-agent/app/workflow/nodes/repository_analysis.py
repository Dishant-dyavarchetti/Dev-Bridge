import logging
import json
import re
from typing import Any
from app.models.state.output_state import OutputState

logger = logging.getLogger("devbridge." + __name__)

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

        outputs = state.get("outputs")
        if outputs is None:
            outputs = OutputState()
        elif isinstance(outputs, dict):
            outputs = OutputState.model_validate(outputs)

        repo_name = None
        if outputs.repository_output:
            repo_name = outputs.repository_output.repository_name

        # Fallback parsing repository name from user request if needed
        if not repo_name and user_request:
            match = re.search(r"github\.com/([\w\-.]+/[\w\-.]+)", user_request)
            if match:
                repo_name = match.group(1)

        # 1. Try to retrieve analysis from Neon DB cache
        cached_data = None
        agent_output = None
        if repo_name:
            from app.app_utils.db import get_repository_from_cache
            cached_data = get_repository_from_cache(repo_name)

        if cached_data:
            from app.models.agent_outputs.repository_output import RepositoryAnalysisOutput
            try:
                struct_data = json.loads(cached_data["structure"])
                agent_output = RepositoryAnalysisOutput(
                    repository_name=repo_name,
                    primary_language=cached_data["language"],
                    architecture_summary=struct_data.get("architecture"),
                    technologies=json.loads(cached_data["frameworks"])
                )
                logger.info(f"Loaded codebase analysis for '{repo_name}' from Neon DB cache.")
            except Exception as e:
                logger.warning(f"Error parsing Neon DB cache for '{repo_name}': {e}")
                cached_data = None  # Fallback to LLM run

        if not cached_data and self.analysis_agent:
            agent_output = await ctx.run_node(self.analysis_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                from app.models.agent_outputs.repository_output import RepositoryAnalysisOutput
                agent_output = RepositoryAnalysisOutput.model_validate(agent_output)

            # 2. Save compiled analysis to Neon DB cache
            if agent_output and agent_output.repository_name:
                from app.app_utils.db import save_repository_to_cache
                save_repository_to_cache(
                    repo_name=agent_output.repository_name,
                    language=agent_output.primary_language or "Python",
                    structure=json.dumps({
                        "architecture": agent_output.architecture_summary, 
                        "entry_points": agent_output.entry_points,
                        "readme_summary": agent_output.readme_summary
                    }),
                    frameworks=json.dumps(agent_output.technologies)
                )

        if agent_output:
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
