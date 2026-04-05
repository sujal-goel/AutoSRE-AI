# PURPOSE:
# - easy level task

# WHY:
# - problem requires 3 tasks (easy → hard)

# WHAT:
# - simple scenario

# EXAMPLE:
# stable company → increase profit by 10%


"""
PURPOSE:
- Define EASY level task

WHY (problem requirement):
- Must have minimum 3 tasks (easy → hard)

CHARACTERISTICS:
- simple goal
- low difficulty
- predictable environment

EXAMPLE IDEA:
- increase value to a target

SUCCESS CONDITION:
- value >= target
"""

from typing import Dict, Any


def get_easy_task() -> Dict[str, Any]:
    return {
        "task_name": "easy",
        "description": "Increase the value to at least 50",
        "target_value": 50,
        "max_steps": 5
    }


def check_easy_success(state_data: Dict[str, Any]) -> float:
    """
    RETURNS:
    - score (0 → 1)
    """

    value = state_data.get("value", 0)

    # normalized score
    score = value / 50.0

    return max(0.0, min(score, 1.0))