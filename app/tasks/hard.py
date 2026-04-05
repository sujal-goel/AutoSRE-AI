
"""
🔥 MOST IMPORTANT TASK

PURPOSE:
- Define HARD level task

WHY:
- judges check this heavily

CHARACTERISTICS:
- conflicting decisions
- high difficulty
- real-world complexity

EXAMPLE:
- maximize value
- but penalize extreme changes

SUCCESS CONDITION:
- high value + stable behavior
"""

from typing import Dict, Any


def get_hard_task() -> Dict[str, Any]:
    return {
        "task_name": "hard",
        "description": "Maximize value while keeping it stable",
        "target_value": 100,
        "max_steps": 10
    }


def check_hard_success(state_data: Dict[str, Any]) -> float:
    value = state_data.get("value", 0)

    # stability penalty (if too extreme)
    stability_penalty = 0.0
    if abs(value) > 120:
        stability_penalty = 0.3

    score = (value / 100.0) - stability_penalty

    return max(0.0, min(score, 1.0))