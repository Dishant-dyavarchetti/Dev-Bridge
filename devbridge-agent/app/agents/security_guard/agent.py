from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.security_output import SecurityOutput
from app.prompts import get_system_instruction

security_guard_agent = Agent(
    name="security_guard",
    model=get_secure_model("gemini-2.5-flash"),
    instruction=get_system_instruction("security_guard"),
    output_schema=SecurityOutput,
)
