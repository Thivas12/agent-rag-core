"""Behavioural tests for the public contracts."""

from datetime import UTC, datetime, timedelta
from hashlib import sha256
from uuid import uuid4

import pytest
from pydantic import ValidationError

from agent_rag_core import (
    ActionStatus,
    AgentAction,
    EvaluationRun,
    EvaluationStatus,
    Event,
    Evidence,
    GeoPoint,
)

NOW = datetime(2026, 9, 12, 12, 0, tzinfo=UTC)


def test_event_has_stable_deduplication_key_and_json_round_trip() -> None:
    event = Event(
        event_id="us7000abcd",
        event_type="earthquake",
        source="usgs",
        occurred_at=NOW,
        location=GeoPoint(latitude=34.2, longitude=-117.4, altitude_km=-8.1),
        payload={"magnitude": 4.3, "reviewed": True},
    )

    assert event.deduplication_key == "usgs:us7000abcd"
    assert Event.model_validate_json(event.model_dump_json()) == event
    assert event.ingested_at.tzinfo is not None


@pytest.mark.parametrize(
    ("field", "value"),
    [("latitude", 90.01), ("longitude", -180.01)],
)
def test_geo_point_rejects_invalid_coordinates(field: str, value: float) -> None:
    coordinates = {"latitude": 0.0, "longitude": 0.0, field: value}

    with pytest.raises(ValidationError):
        GeoPoint.model_validate(coordinates)


def test_event_requires_timezone_and_forbids_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        Event.model_validate(
            {
                "event_id": "1",
                "event_type": "earthquake",
                "source": "usgs",
                "occurred_at": datetime(2026, 9, 12),
                "unexpected": True,
            }
        )


def test_evidence_generates_and_verifies_content_hash() -> None:
    content = "USGS reviewed earthquake bulletin"
    expected_hash = sha256(content.encode("utf-8")).hexdigest()

    generated = Evidence(
        evidence_id="evidence-1",
        source_uri="https://earthquake.usgs.gov/example",
        content=content,
    )
    supplied = Evidence(
        evidence_id="evidence-2",
        source_uri="fixture://usgs/example.json",
        content=content,
        content_sha256=expected_hash,
    )

    assert generated.content_sha256 == expected_hash
    assert supplied.content_sha256 == expected_hash


def test_evidence_rejects_changed_content() -> None:
    with pytest.raises(ValidationError, match="does not match"):
        Evidence(
            evidence_id="evidence-1",
            source_uri="https://example.com",
            content="changed",
            content_sha256="0" * 64,
        )


def test_evidence_rejects_non_mapping_or_missing_content() -> None:
    with pytest.raises(ValidationError):
        Evidence.model_validate("not-a-mapping")
    with pytest.raises(ValidationError):
        Evidence.model_validate({"evidence_id": "evidence-1", "source_uri": "https://example.com"})


def test_agent_action_accepts_valid_running_and_completed_states() -> None:
    run_id = uuid4()
    running = AgentAction(run_id=run_id, agent_name="triage", action_type="retrieve")
    completed = AgentAction(
        run_id=run_id,
        agent_name="triage",
        action_type="retrieve",
        status=ActionStatus.SUCCEEDED,
        started_at=NOW,
        finished_at=NOW + timedelta(seconds=2),
        evidence_ids=("evidence-1",),
    )

    assert running.status is ActionStatus.RUNNING
    assert completed.finished_at is not None


@pytest.mark.parametrize(
    "values",
    [
        {
            "status": ActionStatus.SUCCEEDED,
            "started_at": NOW,
            "finished_at": NOW - timedelta(seconds=1),
        },
        {"status": ActionStatus.RUNNING, "started_at": NOW, "finished_at": NOW},
        {"status": ActionStatus.SUCCEEDED, "started_at": NOW},
        {"status": ActionStatus.FAILED, "started_at": NOW, "finished_at": NOW},
    ],
)
def test_agent_action_rejects_impossible_lifecycle(values: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        AgentAction(
            run_id=uuid4(),
            agent_name="triage",
            action_type="retrieve",
            **values,
        )


def test_failed_agent_action_records_error() -> None:
    action = AgentAction(
        run_id=uuid4(),
        agent_name="triage",
        action_type="retrieve",
        status=ActionStatus.FAILED,
        started_at=NOW,
        finished_at=NOW + timedelta(seconds=1),
        error="source timed out",
    )

    assert action.error == "source timed out"


def test_evaluation_run_accepts_reproducible_completed_run() -> None:
    evaluation = EvaluationRun(
        system_name="atlas-pulse",
        system_version="0.1.0",
        dataset_name="usgs-frozen-fixture",
        dataset_version="2026-09-12",
        git_sha="abcdef1",
        status=EvaluationStatus.PASSED,
        started_at=NOW,
        finished_at=NOW + timedelta(seconds=3),
        sample_count=10,
        passed_count=10,
        metrics={"duplicate_rate": 0.0},
    )

    assert evaluation.metrics["duplicate_rate"] == 0.0


@pytest.mark.parametrize(
    "values",
    [
        {
            "status": EvaluationStatus.FAILED,
            "started_at": NOW,
            "finished_at": NOW - timedelta(seconds=1),
        },
        {"status": EvaluationStatus.RUNNING, "started_at": NOW, "finished_at": NOW},
        {"status": EvaluationStatus.FAILED, "started_at": NOW},
        {"sample_count": 1, "passed_count": 1, "failed_count": 1},
        {
            "status": EvaluationStatus.PASSED,
            "started_at": NOW,
            "finished_at": NOW,
            "sample_count": 1,
            "failed_count": 1,
        },
    ],
)
def test_evaluation_run_rejects_impossible_state(values: dict[str, object]) -> None:
    defaults: dict[str, object] = {
        "system_name": "atlas-pulse",
        "system_version": "0.1.0",
        "dataset_name": "fixture",
        "dataset_version": "v1",
        "git_sha": "abcdef1",
        "sample_count": 1,
    }

    with pytest.raises(ValidationError):
        EvaluationRun(**(defaults | values))


def test_evaluation_run_rejects_non_finite_metric() -> None:
    with pytest.raises(ValidationError):
        EvaluationRun(
            system_name="atlas-pulse",
            system_version="0.1.0",
            dataset_name="fixture",
            dataset_version="v1",
            git_sha="abcdef1",
            sample_count=1,
            metrics={"accuracy": float("nan")},
        )
