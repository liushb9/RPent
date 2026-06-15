"""Agent tool declarations, handlers, and result serialization."""
from __future__ import annotations

from physical_agent.envs.base import EnvSpec
from physical_agent.envs.registry import get_env_spec
from physical_agent.tools import common
from physical_agent.tools.common import tool_result_to_content_blocks

_ACTIVE_ENV_SPEC: EnvSpec | None = None


def configure_env(env_name: str | None = None) -> EnvSpec:
    """Select the environment-specific tool extension for this process."""
    global _ACTIVE_ENV_SPEC
    _ACTIVE_ENV_SPEC = get_env_spec(env_name)
    return _ACTIVE_ENV_SPEC


def get_active_env_spec() -> EnvSpec:
    global _ACTIVE_ENV_SPEC
    if _ACTIVE_ENV_SPEC is None:
        _ACTIVE_ENV_SPEC = get_env_spec("libero")
    return _ACTIVE_ENV_SPEC


def get_tools_spec(env_spec: EnvSpec | None = None) -> list[dict]:
    spec = env_spec or get_active_env_spec()
    return common.bind_output_dir_descriptions([
        *common.TOOLS_SPEC,
        *spec.tools_spec,
    ])


def execute_tool(name: str, input_dict: dict) -> dict:
    handler = common.TOOL_HANDLERS.get(name)
    if handler is None:
        handler = get_active_env_spec().tool_handlers.get(name)
    if handler is None:
        return {"error": f"unknown tool: {name}"}
    try:
        return handler(**input_dict)
    except TypeError as e:
        return {"error": f"bad arguments for {name}: {e}", "got": input_dict}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}


__all__ = [
    "configure_env",
    "execute_tool",
    "get_active_env_spec",
    "get_tools_spec",
    "tool_result_to_content_blocks",
]
