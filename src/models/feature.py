"""Feature state model."""
from __future__ import annotations

from enum import Enum


class FeatureState(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return self.value