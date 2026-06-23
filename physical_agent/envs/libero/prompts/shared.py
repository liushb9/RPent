"""Shared LIBERO prompt fragments."""

from __future__ import annotations

from physical_agent.envs.libero.prompts.env_calibration import ENV_CALIBRATION
from physical_agent.envs.libero.prompts.pro_hybrid_guide import PRO_HYBRID_GUIDE
from physical_agent.envs.libero.prompts.strict_hybrid_guide import (
    STRICT_HYBRID_GUIDE,
)

LIBERO_GUIDES = f"""
GUIDES :

## physical_agent/envs/libero/prompts/strict_hybrid_guide.py

{STRICT_HYBRID_GUIDE}

## physical_agent/envs/libero/prompts/pro_hybrid_guide.py

{PRO_HYBRID_GUIDE}

## physical_agent/envs/libero/prompts/env_calibration.py

{ENV_CALIBRATION}
"""
