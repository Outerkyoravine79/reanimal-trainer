"""God mode — patches the player health write-back routine."""
from __future__ import annotations

from loguru import logger

from src.cheats.base import BaseCheat


class GodModeCheat(BaseCheat):
    name = "god_mode"
    # Signature for the health-decrement instruction inside REANIMAL's player controller.
    SIGNATURE = bytes.fromhex("F3 0F 10 47 48 F3 0F 5C 47 4C")
    PATCH = bytes.fromhex("F3 0F 10 47 48 90 90 90 90 90")

    def enable(self) -> None:
        mem = self.runtime.memory
        if mem is None:
            raise RuntimeError("not attached")
        addr = mem.scan_signature(self.SIGNATURE)
        if addr is None:
            logger.warning("god_mode signature not found")
            return
        self._original_bytes = mem.read_bytes(addr, len(self.PATCH))
        mem.patch_bytes(addr, self.PATCH, expected=self.SIGNATURE)
        logger.success(f"god_mode enabled @ {addr:#x}")

    def disable(self) -> None:
        if self._original_bytes is None:
            return
        mem = self.runtime.memory
        addr = mem.scan_signature(self.SIGNATURE) or 0
        if addr:
            mem.patch_bytes(addr, self._original_bytes)