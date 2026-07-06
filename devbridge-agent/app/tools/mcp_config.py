from google.adk.tools import McpToolset, StdioServerParameters
import os

# Define a standard Notion MCP toolset configuration that agents can use for document caching
notion_mcp_headers = {
    "Authorization": f"Bearer {os.environ.get('NOTION_API_KEY', '')}",
    "Notion-Version": "2022-06-28",
}

notion_mcp_toolset = McpToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env={"OPENAPI_MCP_HEADERS": str(notion_mcp_headers)},
    )
)

# Example: To equip an agent with this MCP server toolset:
#
# from app.agents.utils import get_secure_model
# from google.adk.agents import Agent
#
# notion_agent = Agent(
#     name="notion_agent",
#     model=get_secure_model("gemini-2.5-flash"),
#     tools=[notion_mcp_toolset]
# )
