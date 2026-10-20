"""Resolve module bases and offset tables for REANIMAL."""
from __future__ import annotations

from loguru import logger

from src.bootstrap.runtime import TrainerRuntime


class OffsetService:
    def __init__(self, runtime: TrainerRuntime) -> None:
        self.runtime = runtime
        self.modules: dict[str, int] = {}

    def resolve_modules(self) -> None:
        pm = self.runtime.memory
        if pm is None:
            raise RuntimeError("runtime not attached")
        for mod_name in ("GameAssembly.dll", "UnityPlayer.dll"):
            try:
                module = pm.pm.get_module(mod_name)
                self.modules[mod_name] = module.lpBaseOfDll
                logger.debug(f"{mod_name} @ {module.lpBaseOfDll:#x}")
            except Exception:
                logger.debug(f"{mod_name} not loaded")

    def module_base(self, name: str) -> int:
        if name not in self.modules:
            raise KeyError(f"module '{name}' not resolved")
        return self.modules[name]