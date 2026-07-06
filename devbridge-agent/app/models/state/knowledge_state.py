from typing import Any

from app.models.knowledge.readme import ReadmeKnowledge
from app.models.knowledge.repository import RepositoryKnowledge
from app.models.shared.base import BaseDevBridgeModel


class KnowledgeState(BaseDevBridgeModel):
    """
    Aggregates every Knowledge Model produced by the deterministic extraction layer.

    This state model serves as a centralized container for all factual knowledge
    extracted from external sources (e.g., GitHub, repositories) during a session.
    It exists strictly to organize knowledge for passing through GraphFlow and
    contains no business logic, reasoning, or interpretations.

    Since extraction tools run incrementally at different stages of the workflow,
    all knowledge models are fully optional.
    """

    repository: RepositoryKnowledge | None = None
    readme: ReadmeKnowledge | None = None

    # The following knowledge models will be added as they are implemented
    # in the app.models.knowledge package.
    dependency: Any | None = None
    architecture: Any | None = None
    contribution: Any | None = None
    issue: Any | None = None
