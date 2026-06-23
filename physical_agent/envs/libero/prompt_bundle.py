"""LIBERO prompt bundle assembly."""
from __future__ import annotations

from physical_agent.context.prompt_base import PromptNode
from physical_agent.context.prompts import prompt as base_prompt
from physical_agent.envs.libero import prompts as libero_prompt


def api_system(*, perception: bool) -> dict[str, PromptNode]:
    """Return the API system prompt tree."""
    sections = {
        "Intro": libero_prompt.API_PREAMBLE,
        "Goal": libero_prompt.API_GOAL,
        "Rules": libero_prompt.API_RULES,
        "Workflow": libero_prompt.API_WORKFLOW,
        "Environment": libero_prompt.API_ENVIRONMENT,
        "Output": base_prompt.API_OUTPUT,
    }
    if perception:
        return {"Perception": libero_prompt.PERCEPTION, **sections}
    return sections


def cli_system(*, perception: bool) -> dict[str, PromptNode]:
    """Return the CLI system prompt tree."""
    if perception:
        return {
            "Intro": libero_prompt.CLI_PERCEPTION_PREAMBLE,
            "Goal": libero_prompt.CLI_GOAL,
            "Rules": libero_prompt.CLI_PERCEPTION_RULES,
            "Localization": libero_prompt.CLI_PERCEPTION_LOCALIZATION,
            "Workflow": libero_prompt.CLI_PERCEPTION_WORKFLOW,
            "Environment": libero_prompt.CLI_PERCEPTION_ENVIRONMENT,
            "Output Discipline": base_prompt.CLI_OUTPUT,
            "Next": libero_prompt.CLI_PERCEPTION_NEXT,
        }
    return {
        "Intro": libero_prompt.CLI_PREAMBLE,
        "Goal": libero_prompt.CLI_GOAL,
        "Rules": libero_prompt.CLI_RULES,
        "Workflow": libero_prompt.CLI_WORKFLOW,
        "Environment": libero_prompt.CLI_ENVIRONMENT,
        "Output": base_prompt.CLI_OUTPUT,
        "Next": libero_prompt.CLI_NEXT,
    }


def api_user(*, perception: bool) -> dict[str, PromptNode]:
    """Return the API user prompt tree."""
    if perception:
        return {
            **base_prompt.API_USER,
            "Context": libero_prompt.API_PERCEPTION_USER_CONTEXT,
            "Output": libero_prompt.API_USER_OUTPUT,
        }
    return {
        **base_prompt.API_USER,
        "Context": libero_prompt.API_USER_CONTEXT,
        "Output": libero_prompt.API_USER_OUTPUT,
    }


def cli_user(*, perception: bool) -> dict[str, PromptNode]:
    """Return the CLI user prompt tree."""
    sections = dict(base_prompt.CLI_USER)
    if perception:
        sections["Mode"] = libero_prompt.CLI_PERCEPTION_USER_MODE
    return sections
