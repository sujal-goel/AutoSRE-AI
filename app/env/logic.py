

"""
PURPOSE:
- Keep business logic separate from environment

WHY:
- Clean architecture (better marks)
- Easy to modify logic without touching core env

WHAT THIS FILE DOES:
- apply action
- update state
- calculate reward
"""

from typing import Dict, Any


def apply_action(state_data: Dict[str, Any], action_type: str, parameters: Dict[str, Any]):
    """
    PURPOSE:
    - Modify state based on action

    INPUT:
    - state_data → current environment data
    - action_type → what agent wants to do
    - parameters → extra inputs

    OUTPUT:
    - updated state_data
    """

    value = state_data.get("value", 0)
    target = parameters.get("target", "")

    if action_type in {"scale_up", "increase"}:
        state_data["value"] = value + 10

    elif action_type in {"scale_down", "decrease"}:
        state_data["value"] = value - 5

    elif action_type == "kill_zombies":
        state_data["value"] = value + 15

    elif action_type == "route_traffic":
        state_data["value"] = value + 8

    elif action_type == "clear_cache":
        state_data["value"] = value + 12

    elif action_type == "restart_service":
        state_data["value"] = value + 20

    elif action_type == "reset_value":
        state_data["value"] = 0

    if target:
        state_data["last_target"] = target

    # default (no change)
    return state_data


def calculate_reward(state_data: Dict[str, Any]) -> float:
    """
    PURPOSE:
    - Compute reward (VERY IMPORTANT)

    WHY:
    - Problem requires meaningful reward (not binary)

    LOGIC:
    - reward based on improvement
    """

    value = state_data.get("value", 0)

    reward = value / 100.0

    return max(-1.0, min(reward, 1.0))


def check_done(step_count: int, max_steps: int = 10) -> bool:
    """
    PURPOSE:
    - Decide when episode ends

    WHY:
    - required in RL environment
    """

    return step_count >= max_steps