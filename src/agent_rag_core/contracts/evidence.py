"""Evidence used by retrieval and reasoning components."""

from collections.abc import Mapping
from hashlib import sha256

from pydantic import AwareDatetime, Field, JsonValue, model_validator

from agent_rag_core.contracts._base import ContractModel, utc_now


class Evidence(ContractModel):
    """A provenance-preserving evidence unit that an answer can cite."""

    evidence_id: str = Field(min_length=1, max_length=200)
    source_uri: str = Field(min_length=1)
    content: str = Field(min_length=1)
    content_sha256: str = Field(default="", pattern=r"^[0-9a-f]{64}$", validate_default=True)
    retrieved_at: AwareDatetime = Field(default_factory=utc_now)
    observed_at: AwareDatetime | None = None
    event_id: str | None = None
    title: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def populate_and_verify_hash(cls, value: object) -> object:
        """Generate the hash when absent and reject altered evidence."""
        if not isinstance(value, Mapping):
            return value

        data = {str(key): item for key, item in value.items()}
        content = data.get("content")
        if not isinstance(content, str):
            return data

        expected_hash = sha256(content.encode("utf-8")).hexdigest()
        supplied_hash = data.get("content_sha256")
        if supplied_hash is not None and supplied_hash != expected_hash:
            raise ValueError("content_sha256 does not match content")

        data["content_sha256"] = expected_hash
        return data
