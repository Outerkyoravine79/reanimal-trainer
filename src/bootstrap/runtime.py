"""Runtime wiring for the REANIMAL Trainer."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pymem

from src.adapters.memory_adapter import MemoryAdapter
from src.adapters.input_adapter import InputAdapter
from src.models.profile import TrainerProfile


@dataclass
class TrainerRuntime:
    profile: TrainerProfile
    process_id: Optional[int] = None
    memory: Optional[MemoryAdapter] = None
    input: InputAdapter = field(default_factory=InputAdapter)

    def bind(self, pm: pymem.Pymem) -> None:
        self.process_id = pm.process_id
        self.memory = MemoryAdapter(pm)

    @classmethod
    def from_last_attach(cls) -> "TrainerRuntime":
        from src.config.loader import load_profile
        return cls(profile=load_profile("default"))