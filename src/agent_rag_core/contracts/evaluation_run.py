"""Reproducible evaluation run for models, retrieval, and agents."""

from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from pydantic import AwareDatetime, Field, FiniteFloat, model_validator

from agent_rag_core.contracts._base import ContractModel, utc_now


class EvaluationStatus(StrEnum):
    """Lifecycle state of an evaluation run."""

    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


class EvaluationRun(ContractModel):
    """Versioned metrics and counts needed to reproduce an evaluation."""

    evaluation_id: UUID = Field(default_factory=uuid4)
    system_name: str = Field(min_length=1, max_length=100)
    system_version: str = Field(min_length=1, max_length=100)
    dataset_name: str = Field(min_length=1, max_length=100)
    dataset_version: str = Field(min_length=1, max_length=100)
    git_sha: str = Field(pattern=r"^[0-9a-f]{7,40}$")
    status: EvaluationStatus = EvaluationStatus.RUNNING
    started_at: AwareDatetime = Field(default_factory=utc_now)
    finished_at: AwareDatetime | None = None
    sample_count: int = Field(ge=0)
    passed_count: int = Field(default=0, ge=0)
    failed_count: int = Field(default=0, ge=0)
    metrics: dict[str, FiniteFloat] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_lifecycle_and_counts(self) -> Self:
        """Reject impossible run states before metrics are published."""
        if self.finished_at is not None and self.finished_at < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at")
        if self.status is EvaluationStatus.RUNNING and self.finished_at is not None:
            raise ValueError("a running evaluation cannot have finished_at")
        if self.status is not EvaluationStatus.RUNNING and self.finished_at is None:
            raise ValueError("a completed evaluation requires finished_at")
        if self.passed_count + self.failed_count > self.sample_count:
            raise ValueError("passed_count + failed_count cannot exceed sample_count")
        if self.status is EvaluationStatus.PASSED and self.failed_count:
            raise ValueError("a passed evaluation cannot contain failed cases")
        return self
