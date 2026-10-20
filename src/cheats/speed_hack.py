"""Speed hack — scales the game's delta-time accumulator."""
from __future__ import annotations

from loguru import logger

from src.cheats.base import BaseCheat


class SpeedHackCheat(BaseCheat):
    name = "speed_hack"
    MULTIPLIER = 2.5

    def enable(self) -> None:
        mem = self.runtime.memory
        if mem is None:
            raise RuntimeError("not attached")
        dt_addr = mem.resolve_pointer(
            mem.pm.base_address + 0x02A3B010,
            [0x8, 0x0],
        )
        mem.write_float(dt_addr, self.MULTIPLIER)
        logger.success(f"speed_hack enabled x{self.MULTIPLIER}")

    def disable(self) -> None:
        mem = self.runtime.memory
        if mem is None:
            return
        dt_addr = mem.resolve_pointer(
            mem.pm.base_address + 0x02A3B010,
            [0x8, 0x0],
        )
        mem.write_float(dt_addr, 1.0)