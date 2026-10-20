"""Infinite ammo — freezes the mag counter and skips reload."""
from __future__ import annotations

from loguru import logger

from src.cheats.base import BaseCheat


class InfiniteAmmoCheat(BaseCheat):
    name = "infinite_ammo"

    def enable(self) -> None:
        mem = self.runtime.memory
        if mem is None:
            raise RuntimeError("not attached")
        weapon_ptr = mem.resolve_pointer(
            mem.pm.base_address + 0x02A1F480,
            [0x10, 0x38, 0x0],
        )
        mem.write_int(weapon_ptr + 0x28, 9999)
        mem.write_int(weapon_ptr + 0x2C, 9999)
        logger.success(f"infinite_ammo enabled (weapon @ {weapon_ptr:#x})")

    def disable(self) -> None:
        mem = self.runtime.memory
        if mem is None:
            return
        weapon_ptr = mem.resolve_pointer(
            mem.pm.base_address + 0x02A1F480,
            [0x10, 0x38, 0x0],
        )
        mem.write_int(weapon_ptr + 0x28, 30)