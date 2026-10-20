"""REANIMAL Trainer — CLI entrypoint."""
from __future__ import annotations

import click
from loguru import logger

from src.bootstrap.runtime import TrainerRuntime
from src.services.attach_service import AttachService
from src.services.cheat_service import CheatService
from src.config.loader import load_profile


@click.group()
def cli() -> None:
    """REANIMAL Trainer command line interface."""


@cli.command()
@click.option("--process", default="REANIMAL.exe", help="Target game process")
@click.option("--profile", default="default", help="Trainer profile name")
def attach(process: str, profile: str) -> None:
    profile_cfg = load_profile(profile)
    runtime = TrainerRuntime(profile_cfg)
    svc = AttachService(runtime)
    if svc.attach(process):
        logger.success(f"Attached to {process} (pid={runtime.process_id})")
    else:
        logger.error(f"Failed to attach to {process}")


@cli.command()
@click.argument("feature")
@click.option("--enable/--disable", default=True)
def cheat(feature: str, enable: bool) -> None:
    runtime = TrainerRuntime.from_last_attach()
    svc = CheatService(runtime)
    result = svc.toggle(feature, enable)
    logger.info(f"{feature} -> {result.state}")


if __name__ == "__main__":
    cli()