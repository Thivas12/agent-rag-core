"""Shared behaviour for every public contract."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict


def utc_now() -> datetime:
    """Return an aware UTC timestamp for auditable defaults."""
    return datetime.now(UTC)


class ContractModel(BaseModel):
    """Immutable, strict base model used at service boundaries."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)
