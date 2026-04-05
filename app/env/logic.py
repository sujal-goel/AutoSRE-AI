# PURPOSE:
# - keep business logic separate

# WHY:
# - clean code (better design → higher marks)

# WHAT:
# - functions like:
#   update_revenue()
#   calculate_profit()
#   apply_action()


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

    # Example generic logic (can change later based on idea)

    if action_type == "increase":
        value = parameters.get("value", 0)
        state_data["value"] = state_data.get("value", 0) + value

    elif action_type == "decrease":
        value = parameters.get("value", 0)
        state_data["value"] = state_data.get("value", 0) - value

    elif action_type == "reset_value":
        state_data["value"] = 0

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

    # simple normalized reward
    reward = value / 100.0

    return reward


def check_done(step_count: int, max_steps: int = 10) -> bool:
    """
    PURPOSE:
    - Decide when episode ends

    WHY:
    - required in RL environment
    """

    return step_count >= max_steps