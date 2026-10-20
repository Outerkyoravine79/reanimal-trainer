"""Trainer profile model."""
from __future__ import annotations

from pydantic import BaseModel, Field


class OffsetTable(BaseModel):
    base_pointer: int = Field(..., description="Base pointer for entity enumeration")
    health_offset: int = 0x48
    ammo_offset: int = 0x28
    delta_time_offset: int = 0x8


class TrainerProfile(BaseModel):
    name: str = "default"
    process: str = "REANIMAL.exe"
    offsets: OffsetTable
    hotkeys: dict[str, int] = Field(default_factory=dict)