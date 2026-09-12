"""Canonical event received from a real-time public data source."""

from pydantic import AwareDatetime, Field, JsonValue

from agent_rag_core.contracts._base import ContractModel, utc_now


class GeoPoint(ContractModel):
    """Validated WGS84 location with optional depth or elevation."""

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    altitude_km: float | None = None


class Event(ContractModel):
    """Source-neutral event passed between ingestion, storage, and agents."""

    event_id: str = Field(min_length=1, max_length=200)
    event_type: str = Field(min_length=1, max_length=100)
    source: str = Field(min_length=1, max_length=100)
    occurred_at: AwareDatetime
    ingested_at: AwareDatetime = Field(default_factory=utc_now)
    schema_version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+$")
    location: GeoPoint | None = None
    payload: dict[str, JsonValue] = Field(default_factory=dict)

    @property
    def deduplication_key(self) -> str:
        """Stable key used to make repeated source delivery idempotent."""
        return f"{self.source}:{self.event_id}"
