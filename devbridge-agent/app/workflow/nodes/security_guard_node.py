from typing import Any
from app.models.agent_outputs.security_output import SecurityOutput
from app.models.state.workflow_state import WorkflowState, UserIntent

class SecurityGuardNode:
    """
    Acts as the first line of defense. Evaluates user input for malicious
    intents (e.g., prompt injections) and sensitive credentials (e.g., API keys)
    before allowing the graph to proceed to domain reasoning.
    """
    def __init__(self, security_agent: Any = None):
        self.security_agent = security_agent

    async def __call__(self, ctx: Any) -> Any:
        state = ctx.state

        # Initialize workflow state if missing
        workflow = state.get("workflow")
        if workflow is None:
            workflow = WorkflowState(intent=UserIntent.DISCOVER_REPOSITORIES)
        elif isinstance(workflow, dict):
            workflow = WorkflowState.model_validate(workflow)

        # Read the user's request
        user_request = state.get("user_request", "")

        # Evaluate the request
        if self.security_agent:
            agent_output = await ctx.run_node(self.security_agent, node_input=user_request)
            if isinstance(agent_output, dict):
                agent_output = SecurityOutput.model_validate(agent_output)
        else:
            # Fallback if no agent is injected (fail open for development)
            from app.models.shared.confidence import Confidence, ConfidenceLevel
            agent_output = SecurityOutput(
                summary="Fallback security check (no agent).",
                confidence=Confidence(level=ConfidenceLevel.LOW, score=0.0, reasoning="No agent injected"),
                next_actions=[],
                is_safe=True
            )

        # Store output in OutputState (under 'outputs' key)
        from app.models.state.output_state import OutputState
        outputs = state.get("outputs")
        if outputs is None:
            outputs = OutputState()
        elif isinstance(outputs, dict):
            outputs = OutputState.model_validate(outputs)

        outputs.security_output = agent_output
        state["outputs"] = outputs.model_dump()

        # Route based on safety
        if not agent_output.is_safe:
            workflow.intent = UserIntent.SECURITY_VIOLATION
            workflow.next_recommended_step = agent_output.violation_reason
            ctx.route = "UNSAFE"
        else:
            ctx.route = "SAFE"

        state["workflow"] = workflow.model_dump()
