from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from app.models.shared.base import BaseDevBridgeModel


class ExecutionStatus(StrEnum):
    """
    Represents the current execution status of the GraphFlow workflow.
    """

    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ExecutionError(BaseDevBridgeModel):
    """
    Represents an error encountered while executing a GraphFlow node.

    This model enables structured execution logging and recovery without
    exposing implementation details to higher layers.
    """

    node: str
    agent: str | None = None
    message: str
    recoverable: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ParallelTask(BaseDevBridgeModel):
    """
    Represents the execution status of a node participating in
    parallel GraphFlow execution.
    """

    node_name: str
    completed: bool = False
    started_at: datetime | None = None
    completed_at: datetime | None = None


class ExecutionState(BaseDevBridgeModel):
    """
    Stores execution metadata for a single GraphFlow execution.

    This model tracks how the workflow is progressing rather than
    what the workflow is about.

    It is exclusively owned by GraphFlow and should never contain
    repository knowledge, mentoring state, or AI reasoning outputs.
    """

    status: ExecutionStatus = ExecutionStatus.NOT_STARTED

    current_node: str | None = None
    previous_node: str | None = None

    executed_nodes: list[str] = Field(default_factory=list)
    executed_agents: list[str] = Field(default_factory=list)

    pending_nodes: list[str] = Field(default_factory=list)
    failed_nodes: list[str] = Field(default_factory=list)

    execution_errors: list[ExecutionError] = Field(default_factory=list)

    parallel_tasks: list[ParallelTask] = Field(default_factory=list)

    started_at: datetime | None = None
    completed_at: datetime | None = None
