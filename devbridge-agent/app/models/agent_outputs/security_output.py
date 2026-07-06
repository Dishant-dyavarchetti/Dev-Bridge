from app.models.agent_outputs.base_output import BaseAgentOutput


class SecurityOutput(BaseAgentOutput):
    """
    Output produced by the Security Guard Agent.

    Determines if the user's prompt is safe to process or if it contains
    malicious intent, prompt injections, or sensitive PII.
    """

    is_safe: bool
    violation_reason: str | None = None
