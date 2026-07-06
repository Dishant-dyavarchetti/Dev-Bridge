import os
import logging
import json
from typing import Any, AsyncGenerator
from app.models.state.workflow_state import WorkflowStage
from app.models.state.output_state import OutputState
from google.adk.events.event import Event
from google.genai import types

logger = logging.getLogger("devbridge." + __name__)

class ResponseNode:
    """
    Generate the final mentoring response.
    Runs the response composer agent and updates the state.
    """
    def __init__(self, response_agent: Any = None):
        self.response_agent = response_agent

    async def __call__(self, ctx: Any) -> AsyncGenerator[Any, None]:
        state = ctx.state
        user_request = state.get("user_request", "")

        outputs = state.get("outputs")
        if outputs is None:
            outputs = OutputState()
        elif isinstance(outputs, dict):
            outputs = OutputState.model_validate(outputs)

        workflow = state.get("workflow")
        if workflow is not None:
            if isinstance(workflow, dict):
                from app.models.state.workflow_state import WorkflowState
                workflow = WorkflowState.model_validate(workflow)

        # Detect if this is an ASK_QUESTION (conversational follow-up)
        from app.models.state.workflow_state import UserIntent
        is_question = workflow and workflow.intent == UserIntent.ASK_QUESTION

        # Compile repository and guidelines context collected from preceding agents
        repo_data = outputs.repository_output.model_dump() if outputs.repository_output else {}
        contrib_data = outputs.contribution_output.model_dump() if outputs.contribution_output else {}
        issue_data = outputs.issue_output.model_dump() if outputs.issue_output else {}

        if is_question:
            # Tell ResponseComposerAgent to act as a conversational mentor answering the specific question
            context_prompt = f"""[USER QUESTION]
"{user_request}"

[CONVERSATION CONTEXT]
Use the following codebase and issues details from previous analysis to answer the user's question directly. Do NOT output a new onboarding guide template. Just reply to their question.

Repository Analysis:
{json.dumps(repo_data, indent=2)}

Contribution Guidelines:
{json.dumps(contrib_data, indent=2)}

Curated Recommended Issues:
{json.dumps(issue_data, indent=2)}
"""
        else:
            # Tell ResponseComposerAgent to synthesize a complete mentoring guide
            context_prompt = f"""[USER REQUEST]
"{user_request}"

[COLLECTED FINDINGS]
Repository Analysis:
{json.dumps(repo_data, indent=2)}

Contribution Guidelines:
{json.dumps(contrib_data, indent=2)}

Curated Recommended Issues:
{json.dumps(issue_data, indent=2)}
"""

        use_gemma = os.environ.get("USE_GEMMA_FOR_RESPONSE", "False").lower() in ("true", "1")

        if use_gemma:
            from app.agents.response_composer.agent import gemma_response_composer_agent
            from app.models.agent_outputs.response_output import ResponseComposerOutput
            from app.models.shared.confidence import Confidence, ConfidenceLevel
            
            # Execute gemma response composer (which has no output_schema and returns a string)
            agent_output_text = await ctx.run_node(gemma_response_composer_agent, node_input=context_prompt)
            
            # Wrap the raw text output inside a ResponseComposerOutput object
            agent_output = ResponseComposerOutput(
                summary="Composed mentoring guide using Gemma 4." if not is_question else "Answered follow-up question using Gemma 4.",
                confidence=Confidence(
                    level=ConfidenceLevel.HIGH,
                    score=0.95,
                    reasoning="Successfully generated response details via gemma-4-31b-it."
                ),
                agent_id="gemma_response_composer_agent",
                sections=[agent_output_text]
            )
        elif self.response_agent:
            agent_output = await ctx.run_node(self.response_agent, node_input=context_prompt)
            if isinstance(agent_output, dict):
                from app.models.agent_outputs.response_output import ResponseComposerOutput
                agent_output = ResponseComposerOutput.model_validate(agent_output)
        else:
            # Fallback response
            from app.models.agent_outputs.response_output import ResponseComposerOutput
            from app.models.shared.confidence import Confidence, ConfidenceLevel
            agent_output = ResponseComposerOutput(
                summary="Fallback response composed.",
                confidence=Confidence(
                    level=ConfidenceLevel.LOW,
                    score=0.0,
                    reasoning="No agent was injected."
                ),
                agent_id="response_composer_agent",
                sections=["Fallback Response Section"]
            )

        outputs.response_output = agent_output
        state["outputs"] = outputs.model_dump()

        if workflow is not None:
            workflow.next_recommended_step = agent_output.summary
            workflow.is_completed = True
            workflow.stage = WorkflowStage.COMPLETED
            state["workflow"] = workflow.model_dump()

        # Persist final session state and outputs to Neon Postgres
        try:
            from app.app_utils.db import save_session_history
            wf_dict = workflow.model_dump() if hasattr(workflow, "model_dump") else workflow
            out_dict = outputs.model_dump() if hasattr(outputs, "model_dump") else outputs
            
            save_session_history(
                session_id=state.get("session_id", "playground_session"),
                user_request=user_request,
                workflow_state=json.dumps(wf_dict),
                outputs=json.dumps(out_dict)
            )
        except Exception as e:
            logger.warning(f"Failed to persist session history to Neon: {e}")

        # Yield the final compiled response text to the user
        if agent_output.sections:
            response_text = "\n\n".join(agent_output.sections)
        else:
            response_text = agent_output.summary
        yield Event(content=types.Content(parts=[types.Part.from_text(text=response_text)]))
