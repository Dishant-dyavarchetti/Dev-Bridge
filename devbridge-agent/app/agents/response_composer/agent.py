from google.adk.agents import Agent
from app.agents.utils import get_secure_model
from app.models.agent_outputs.response_output import ResponseComposerOutput
from app.prompts import get_system_instruction

response_composer_agent = Agent(
    name="response_composer_agent",
    model=get_secure_model("gemini-2.5-flash"),
    instruction=get_system_instruction("response_composer"),
    output_schema=ResponseComposerOutput,
)

gemma_response_composer_agent = Agent(
    name="gemma_response_composer_agent",
    model=get_secure_model("gemma-4-31b-it"),
    instruction=get_system_instruction("response_composer") + "\n\nFormat your response as a beautiful, comprehensive Markdown mentoring guide with appropriate headers and sections.",
)
