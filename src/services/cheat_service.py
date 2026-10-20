"""Cheat feature dispatch for the REANIMAL Trainer."""
from __future__ import annotations

from dataclasses import dataclass

from loguru import logger

from src.bootstrap.runtime import TrainerRuntime
from src.cheats.god_mode import GodModeCheat
from src.cheats.infinite_ammo import InfiniteAmmoCheat
from src.cheats.speed_hack import SpeedHackCheat
from src.cheats.esp_overlay import EspOverlayCheat
from src.models.feature import FeatureState


_CHEATS = {
    "god_mode": GodModeCheat,
    "infinite_ammo": InfiniteAmmoCheat,
    "speed_hack": SpeedHackCheat,
    "esp": EspOverlayCheat,
}


@dataclass
class CheatResult:
    feature: str
    state: FeatureState


class CheatService:
    def __init__(self, runtime: TrainerRuntime) -> None:
        self.runtime = runtime
        self._instances: dict[str, object] = {}

    def toggle(self, feature: str, enable: bool) -> CheatResult:
        cls = _CHEATS.get(feature)
        if cls is None:
            logger.warning(f"unknown feature '{feature}'")
            return CheatResult(feature, FeatureState.UNKNOWN)
        inst = self._instances.setdefault(feature, cls(self.runtime))
        inst.set_enabled(enable)  # type: ignore[attr-defined]
        return CheatResult(feature, inst.state)  # type: ignore[attr-defined]