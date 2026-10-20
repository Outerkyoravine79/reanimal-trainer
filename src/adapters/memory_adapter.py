"""Thin wrapper around pymem with typed read/write helpers."""
from __future__ import annotations

import struct
from typing import Any

import pymem


class MemoryAdapter:
    def __init__(self, pm: pymem.Pymem) -> None:
        self.pm = pm

    def read_float(self, address: int) -> float:
        return self.pm.read_float(address)

    def write_float(self, address: int, value: float) -> None:
        self.pm.write_float(address, value)

    def read_int(self, address: int) -> int:
        return self.pm.read_int(address)

    def write_int(self, address: int, value: int) -> None:
        self.pm.write_int(address, value)

    def read_bytes(self, address: int, size: int) -> bytes:
        return self.pm.read_bytes(address, size)

    def patch_bytes(self, address: int, payload: bytes, expected: bytes | None = None) -> bool:
        if expected is not None:
            current = self.read_bytes(address, len(expected))
            if current != expected:
                return False
        self.pm.write_bytes(address, payload, len(payload))
        return True

    def resolve_pointer(self, base: int, offsets: list[int]) -> int:
        addr = base
        for off in offsets[:-1]:
            addr = self.pm.read_longlong(addr + off)
        return addr + offsets[-1]

    def scan_signature(self, pattern: bytes) -> int | None:
        return self.pm.pattern_scan_all(pattern)