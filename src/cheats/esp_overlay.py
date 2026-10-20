"""ESP / wallhack — collects entity positions for the external overlay renderer."""
from __future__ import annotations

from dataclasses import dataclass

from src.cheats.base import BaseCheat


@dataclass
class EntityMarker:
    name: str
    x: float
    y: float
    z: float
    distance: float


class EspOverlayCheat(BaseCheat):
    name = "esp"

    def enable(self) -> None:
        # The overlay renderer polls entities each frame; enabling just flips the flag.
        self._enabled = True

    def disable(self) -> None:
        self._enabled = False

    def collect(self) -> list[EntityMarker]:
        mem = self.runtime.memory
        if mem is None or not getattr(self, "_enabled", False):
            return []
        markers: list[EntityMarker] = []
        base = mem.pm.base_address + 0x02A5C000
        count = mem.read_int(base + 0x18)
        for i in range(min(count, 256)):
            entry = base + 0x20 + i * 0x40
            pos_x = mem.read_float(entry + 0x10)
            pos_y = mem.read_float(entry + 0x14)
            pos_z = mem.read_float(entry + 0x18)
            markers.append(EntityMarker("actor", pos_x, pos_y, pos_z, 0.0))
        return markers