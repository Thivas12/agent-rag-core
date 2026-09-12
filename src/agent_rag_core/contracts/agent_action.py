"""Auditable action performed by an AI agent."""

from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from pydantic import AwareDatetime, Field, JsonValue, model_validator

from agent_rag_core.contracts._base import ContractModel, utc_now


class ActionStatus(StrEnum):
    """Lifecycle state of an agent action."""

    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    SKIPPED = "skipped"


class AgentAction(ContractModel):
    """Immutable audit record for a single tool call or reasoning action."""

    action_id: UUID = Field(default_factory=uuid4)
    run_id: UUID
    agent_name: str = Field(min_length=1, max_length=100)
    action_type: str = Field(min_length=1, max_length=100)
    status: ActionStatus = ActionStatus.RUNNING
    started_at: AwareDatetime = Field(default_factory=utc_now)
    finished_at: AwareDatetime | None = None
    input_data: dict[str, JsonValue] = Field(default_factory=dict)
    output_data: dict[str, JsonValue] = Field(default_factory=dict)
    evidence_ids: tuple[str, ...] = ()
    model_name: str | None = None
    prompt_version: str | None = None
    error: str | None = None

    @model_validator(mode="after")
    def validate_lifecycle(self) -> Self:
        """Keep timestamps, status, and failure information consistent."""
        if self.finished_at is not None and self.finished_at < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at")
        if self.status is ActionStatus.RUNNING and self.finished_at is not None:
            raise ValueError("a running action cannot have finished_at")
        if self.status is not ActionStatus.RUNNING and self.finished_at is None:
            raise ValueError("a completed action requires finished_at")
        if self.status is ActionStatus.FAILED and not self.error:
            raise ValueError("a failed action requires an error message")
        return self
