"""Base class shared by all REANIMAL Trainer cheats."""
from __future__ import annotations

from abc import ABC, abstractmethod

from src.bootstrap.runtime import TrainerRuntime
from src.models.feature import FeatureState


class BaseCheat(ABC):
    name: str = "base"

    def __init__(self, runtime: TrainerRuntime) -> None:
        self.runtime = runtime
        self.state: FeatureState = FeatureState.DISABLED
        self._original_bytes: bytes | None = None

    def set_enabled(self, enabled: bool) -> None:
        if enabled and self.state is not FeatureState.ENABLED:
            self.enable()
            self.state = FeatureState.ENABLED
        elif not enabled and self.state is FeatureState.ENABLED:
            self.disable()
            self.state = FeatureState.DISABLED

    @abstractmethod
    def enable(self) -> None: ...

    @abstractmethod
    def disable(self) -> None: ...