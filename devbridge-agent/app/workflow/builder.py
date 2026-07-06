from collections.abc import AsyncGenerator
from typing import Any
from google.adk.workflow import Workflow, node, Edge

from app.models.state.devbridge_state import DevBridgeState
from app.models.state.workflow_state import UserIntent
from app.workflow.nodes.contribution_node import ContributionNode
from app.workflow.nodes.issue_recommendation import IssueRecommendationNode
from app.workflow.nodes.merge_node import MergeNode
from app.workflow.nodes.planner_node import PlannerNode
from app.workflow.nodes.repository_analysis import RepositoryAnalysisNode
from app.workflow.nodes.repository_discovery_node import RepositoryDiscoveryNode
from app.workflow.nodes.response_node import ResponseNode
from app.workflow.nodes.security_guard_node import SecurityGuardNode


def build_workflow(
    planner_agent=None,
    discovery_agent=None,
    analysis_agent=None,
    contribution_agent=None,
    issue_agent=None,
    response_agent=None,
    security_agent=None
) -> Workflow:
    """
    Build and compile the complete GraphFlow Workflow for DevBridge.
    """
    if planner_agent is None:
        from app.agents import planner_agent
    if discovery_agent is None:
        from app.agents import repository_discovery_agent as discovery_agent
    if analysis_agent is None:
        from app.agents import repository_analysis_agent as analysis_agent
    if contribution_agent is None:
        from app.agents import contribution_agent
    if issue_agent is None:
        from app.agents import issue_recommendation_agent as issue_agent
    if response_agent is None:
        from app.agents import response_composer_agent as response_agent
    if security_agent is None:
        from app.agents import security_guard_agent as security_agent

    # Instantiate the node class instances
    security_node_inst = SecurityGuardNode(security_agent)
    planner_node_inst = PlannerNode(planner_agent)
    discovery_node_inst = RepositoryDiscoveryNode(discovery_agent)
    analysis_node_inst = RepositoryAnalysisNode(analysis_agent)
    contribution_node_inst = ContributionNode(contribution_agent)
    issue_node_inst = IssueRecommendationNode(issue_agent)
    response_node_inst = ResponseNode(response_agent)

    # Wrap them in plain functions so ADK detects their async/sync nature correctly
    async def run_security(ctx: Any) -> Any:
        return await security_node_inst(ctx)

    async def run_planner(ctx: Any) -> Any:
        return await planner_node_inst(ctx)

    async def run_discovery(ctx: Any) -> Any:
        return await discovery_node_inst(ctx)

    async def run_analysis(ctx: Any) -> Any:
        return await analysis_node_inst(ctx)

    async def run_contribution(ctx: Any) -> Any:
        return await contribution_node_inst(ctx)

    async def run_issue(ctx: Any) -> Any:
        return await issue_node_inst(ctx)

    async def run_response(ctx: Any) -> AsyncGenerator[Any, None]:
        async for event in response_node_inst(ctx):
            yield event

    # Wrap the functions using ADK node helper to specify names
    security_node = node(run_security, name="security_guard_node", rerun_on_resume=True)
    planner_node = node(run_planner, name="planner_node", rerun_on_resume=True)
    discovery_node = node(run_discovery, name="discovery_node", rerun_on_resume=True)
    analysis_node = node(run_analysis, name="analysis_node", rerun_on_resume=True)
    contribution_node = node(run_contribution, name="contribution_node", rerun_on_resume=True)
    issue_node = node(run_issue, name="issue_node", rerun_on_resume=True)
    merge_node = MergeNode(name="merge_node")
    response_node = node(run_response, name="response_composer_node", rerun_on_resume=True)

    # Define the graph execution paths
    edges = [
        # Entry point to SecurityGuardNode
        ("START", security_node),

        # Routing based on Safety determination
        Edge(from_node=security_node, to_node=planner_node, route="SAFE"),
        Edge(from_node=security_node, to_node=response_node, route="UNSAFE"),

        # Routing based on Planner intent determination
        Edge(from_node=planner_node, to_node=discovery_node, route=UserIntent.DISCOVER_REPOSITORIES.value),

        # Route all other repository-scoped intents to Analysis Node
        Edge(from_node=planner_node, to_node=analysis_node, route=[
            UserIntent.EXPLORE_REPOSITORY.value,
            UserIntent.UNDERSTAND_ARCHITECTURE.value,
            UserIntent.FIND_BEGINNER_ISSUES.value,
            UserIntent.CONTRIBUTE.value,
            UserIntent.LEARN_PROJECT.value,
        ]),

        # Direct route for general follow-up questions to response node
        Edge(from_node=planner_node, to_node=response_node, route=UserIntent.ASK_QUESTION.value),

        # Discovery flows directly to codebase analysis
        (discovery_node, analysis_node),

        # Analysis forks into parallel contribution and issue recommendation tasks
        (analysis_node, (contribution_node, issue_node)),

        # Fan-in from parallel branches into MergeNode
        (contribution_node, merge_node),
        (issue_node, merge_node),

        # MergeNode connects to ResponseNode
        (merge_node, response_node),
    ]

    # Instantiate and return the compiled Workflow
    return Workflow(
        name="devbridge_workflow",
        description="GraphFlow workflow for open-source developer mentoring.",
        state_schema=DevBridgeState,
        edges=edges
    )
