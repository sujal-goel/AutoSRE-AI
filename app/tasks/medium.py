
"""
PURPOSE:
- Define MEDIUM level task

CHARACTERISTICS:
- moderate difficulty
- multiple conditions

EXAMPLE:
- increase value but avoid going negative

SUCCESS CONDITION:
- value high AND not negative
"""

from typing import Dict, Any


def get_medium_task() -> Dict[str, Any]:
    return {
        "task_name": "medium",
        "description": "Increase value above 70 without going negative",
        "target_value": 70,
        "max_steps": 7
    }


def check_medium_success(state_data: Dict[str, Any]) -> float:
    value = state_data.get("value", 0)

    # penalty if negative
    if value < 0:
        return 0.0

    score = value / 70.0

    return max(0.0, min(score, 1.0))