"""LIBERO environment extension."""
from __future__ import annotations

from physical_agent.envs.base import EnvSpec, PromptBundle
from physical_agent.envs.libero.prompt_bundle import (
    api_system,
    api_user,
    cli_system,
    cli_user,
)


def get_env_spec() -> EnvSpec:
    """Return the LIBERO env identity + prompt bundle.

    Tool schemas, handlers, driver lifecycle, and the MCP allowlist live on
    the LIBERO toolkit (see :func:`get_toolkit`).
    """
    return EnvSpec(
        name="libero",
        prompts=PromptBundle(
            api_system=api_system,
            api_user=api_user,
            cli_system=cli_system,
            cli_user=cli_user,
        ),
    )


def get_toolkit():
    """Return the LIBERO toolkit (common tools + LIBERO primitives)."""
    from physical_agent.envs.libero.toolkit import LiberoToolkit

    return LiberoToolkit()
