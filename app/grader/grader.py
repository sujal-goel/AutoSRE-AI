
"""
PURPOSE:
- Evaluate agent performance
- Return score between 0.0 and 1.0

WHY (from problem):
- Mandatory requirement
- Used to judge agent success
- Must be deterministic (same input → same score)

WHAT THIS FILE DOES:
- Takes final state
- Calculates score based on:
    - progress
    - stability
    - efficiency

IMPORTANT RULES:
- Score must be between 0.0 and 1.0
- Should NOT be random
- Should reflect real performance
"""

from typing import Dict, Any


def compute_score(state_data: Dict[str, Any]) -> float:
    """
    PURPOSE:
    - Calculate final score

    INPUT:
    - state_data (final environment state)

    OUTPUT:
    - score (0.0 → 1.0)
    """

    # Example generic metric
    value = state_data.get("value", 0)

    # Normalize score (0 to 1)
    score = value / 100.0

    # Clamp between 0 and 1
    score = max(0.0, min(score, 1.0))

    return score


def evaluate_performance(state_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    PURPOSE:
    - Detailed evaluation (optional but useful)

    RETURNS:
    - score
    - breakdown (for debugging)
    """

    value = state_data.get("value", 0)

    # individual components (you can expand later)
    progress_score = value / 100.0
    stability_score = 1.0 if value >= 0 else 0.0

    final_score = compute_score(state_data)

    return {
        "score": final_score,
        "details": {
            "progress": progress_score,
            "stability": stability_score
        }
    }