from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.contribution_output import ContributionOutput
from app.prompts import get_system_instruction

contribution_agent = Agent(
    name="contribution_agent",
    model=get_secure_model("gemini-3.1-flash-lite"),
    instruction=get_system_instruction("contribution"),
    output_schema=ContributionOutput,
)
