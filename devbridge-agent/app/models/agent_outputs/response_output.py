from pydantic import Field

from app.models.agent_outputs.base_output import BaseAgentOutput


class ResponseComposerOutput(BaseAgentOutput):
    """
    Final output returned to the frontend.

    Produced by the Response Composer after combining the outputs of all
    reasoning agents into a single coherent response.
    """

    sections: list[str] = Field(default_factory=list)
