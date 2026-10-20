"""Handles attaching to the REANIMAL game process and bootstrapping runtime state."""
from __future__ import annotations

import time

import pymem
from loguru import logger

from src.bootstrap.runtime import TrainerRuntime
from src.services.offset_service import OffsetService


class AttachService:
    def __init__(self, runtime: TrainerRuntime) -> None:
        self.runtime = runtime

    def attach(self, process_name: str, timeout: float = 10.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                pm = pymem.Pymem(process_name)
                self.runtime.bind(pm)
                OffsetService(self.runtime).resolve_modules()
                logger.debug(f"Base module {pm.base_address:#x}")
                return True
            except pymem.exception.ProcessNotFound:
                time.sleep(0.5)
            except Exception as exc:
                logger.error(f"attach error: {exc}")
                return False
        return False