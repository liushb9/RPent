"""Environment extension contracts for PhysicalAgent."""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from physical_agent.context.prompt_base import PromptNode, format_prompt
from physical_agent.tools.toolkit import Toolkit

PromptFactory = Callable[..., PromptNode]


@dataclass(frozen=True)
class PromptBundle:
    """Python-defined prompt variants for one environment."""

    api_system: PromptFactory
    api_user: PromptFactory
    cli_system: PromptFactory
    cli_user: PromptFactory

    def render(
        self,
        variant: str,
        *,
        variables: Mapping[str, object] | None = None,
        perception: bool = False,
    ) -> str:
        """Render one prompt variant."""
        prompt = getattr(self, variant)(perception=perception)
        return format_prompt(prompt, variables=variables)


@dataclass(frozen=True)
class EnvSpec:
    """Environment-level (non-tool) extension points for PhysicalAgent.

    Tool schemas, handlers, driver lifecycle, and the MCP allowlist live on
    :class:`physical_agent.tools.toolkit.Toolkit` (and env-specific
    subclasses). ``EnvSpec`` carries only the env identity and prompt bundle.
    """

    name: str
    prompts: PromptBundle


# ``libero`` imports ``EnvSpec`` / ``PromptBundle`` from this module, so it is
# imported below the dataclass definitions to avoid a circular import.
from physical_agent.envs import libero  # noqa: E402

# Registered envs: name -> module exposing get_env_spec() / get_toolkit().
_ENVS = {"libero": libero}


def _resolve_env(name: str | None = None) -> Any:
    env_name = (name or "libero").lower()
    module = _ENVS.get(env_name)
    if module is None:
        known = ", ".join(sorted(_ENVS))
        raise ValueError(f"unknown env: {env_name!r}; known envs: {known}")
    return module


def get_env_spec(name: str | None = None) -> EnvSpec:
    return _resolve_env(name).get_env_spec()


def get_toolkit(name: str | None = None) -> Toolkit:
    """Build the env toolkit (common tools + env-specific tools)."""
    return _resolve_env(name).get_toolkit()
