from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.planner_output import PlannerOutput
from app.prompts import get_system_instruction

planner_agent = Agent(
    name="planner_agent",
    model=get_secure_model("gemini-2.5-flash"),
    instruction=get_system_instruction("planner"),
    output_schema=PlannerOutput,
)
