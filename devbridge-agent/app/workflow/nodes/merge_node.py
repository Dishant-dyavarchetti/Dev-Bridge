from google.adk.workflow import JoinNode


class MergeNode(JoinNode):
    """
    Join node that synchronizes the outputs of ContributionNode and IssueRecommendationNode.
    It inherits from JoinNode to ensure the orchestrator waits for both parallel branches.
    """
    pass
