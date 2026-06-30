"""Shared LIBERO prompt fragments."""

from __future__ import annotations

from physical_agent.envs.libero.prompts.env_calibration import ENV_CALIBRATION
from physical_agent.envs.libero.prompts.pro_hybrid_guide import PRO_HYBRID_GUIDE
from physical_agent.envs.libero.prompts.strict_hybrid_guide import (
    STRICT_HYBRID_GUIDE,
)

MCP_RUNTIME_ADAPTER = """
CURRENT MCP RUNTIME ADAPTER:
- The environment server is already running and managed by the runner.
- Do not start, stop, restart, or otherwise manage `env_server.py`.
- Do not write `command.json` or any file-based driver command.
- Do not emit plain-text pseudo tool calls such as `<tool_call>`, `[tool_use:]`,
  or JSON action commands.
- For images, use Claude Code's structured `Read` tool.
- For physical actions, call the real `physical_agent` MCP tools exposed by the
  runtime.
- If an embedded guide mentions file-driver commands, action dictionaries, or
  legacy command files, translate the intended primitive into structured MCP
  tool calls. Preserve the guide's strategy, constraints, parameters, and
  recovery advice; only the command format is legacy.
- Only call `finish` with success status after the latest
  state has `libero_terminated == true`.
"""

LIBERO_GUIDES = f"""
GUIDES :

## physical_agent/envs/libero/prompts/strict_hybrid_guide.py

{STRICT_HYBRID_GUIDE}

## physical_agent/envs/libero/prompts/pro_hybrid_guide.py

{PRO_HYBRID_GUIDE}

## physical_agent/envs/libero/prompts/env_calibration.py

{ENV_CALIBRATION}
"""
