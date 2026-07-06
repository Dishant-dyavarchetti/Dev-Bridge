from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.issue_output import IssueRecommendationOutput
from app.prompts import get_system_instruction

issue_recommendation_agent = Agent(
    name="issue_recommendation_agent",
    model=get_secure_model("gemini-3.1-flash-lite"),
    instruction=get_system_instruction("issue_recommendation"),
    output_schema=IssueRecommendationOutput,
)
