import os
from typing import Any, AsyncGenerator
from app.models.state.workflow_state import WorkflowStage
from app.models.state.output_state import OutputState
from google.adk.events.event import Event
from google.genai import types

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

        use_gemma = os.environ.get("USE_GEMMA_FOR_RESPONSE", "False").lower() in ("true", "1")

        if use_gemma:
            from app.agents.response_composer.agent import gemma_response_composer_agent
            from app.models.agent_outputs.response_output import ResponseComposerOutput
            from app.models.shared.confidence import Confidence, ConfidenceLevel
            
            # Execute gemma response composer (which has no output_schema and returns a string)
            agent_output_text = await ctx.run_node(gemma_response_composer_agent, node_input=user_request)
            
            # Wrap the raw text output inside a ResponseComposerOutput object
            agent_output = ResponseComposerOutput(
                summary="Composed mentoring guide using Gemma 4.",
                confidence=Confidence(
                    level=ConfidenceLevel.HIGH,
                    score=0.95,
                    reasoning="Successfully generated complete mentoring details via gemma-4-31b-it."
                ),
                agent_id="gemma_response_composer_agent",
                sections=[agent_output_text]
            )
        elif self.response_agent:
            agent_output = await ctx.run_node(self.response_agent, node_input=user_request)
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

        outputs = state.get("outputs")
        if outputs is None:
            outputs = OutputState()
        elif isinstance(outputs, dict):
            outputs = OutputState.model_validate(outputs)
        
        outputs.response_output = agent_output
        state["outputs"] = outputs.model_dump()

        workflow = state.get("workflow")
        if workflow is not None:
            if isinstance(workflow, dict):
                from app.models.state.workflow_state import WorkflowState
                workflow = WorkflowState.model_validate(workflow)
            workflow.next_recommended_step = agent_output.summary
            workflow.is_completed = True
            workflow.stage = WorkflowStage.COMPLETED
            state["workflow"] = workflow.model_dump()

        # Yield the final compiled response text to the user
        if agent_output.sections:
            response_text = "\n\n".join(agent_output.sections)
        else:
            response_text = agent_output.summary
        yield Event(content=types.Content(parts=[types.Part.from_text(text=response_text)]))
