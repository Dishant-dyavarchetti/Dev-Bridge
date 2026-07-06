from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.repository_output import RepositoryAnalysisOutput
from app.prompts import get_system_instruction

repository_analysis_agent = Agent(
    name="repository_analysis_agent",
    model=get_secure_model("gemini-3.1-flash-lite"),
    instruction=get_system_instruction("repository_analysis"),
    output_schema=RepositoryAnalysisOutput,
)
