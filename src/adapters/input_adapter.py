"""Hotkey / input hooks for the REANIMAL Trainer overlay."""
from __future__ import annotations

from typing import Callable

import win32api
import win32con


class InputAdapter:
    def __init__(self) -> None:
        self._bindings: dict[int, Callable[[], None]] = {}

    def bind(self, vk_code: int, callback: Callable[[], None]) -> None:
        self._bindings[vk_code] = callback

    def poll(self) -> None:
        for vk, cb in list(self._bindings.items()):
            if win32api.GetAsyncKeyState(vk) & 0x8000:
                try:
                    cb()
                except Exception:
                    pass

    @staticmethod
    def is_key_down(vk_code: int) -> bool:
        return bool(win32api.GetAsyncKeyState(vk_code) & 0x8000)

    VK = win32con