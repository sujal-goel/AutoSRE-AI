# PURPOSE:
# - What agent sees after each step

# WHY:
# - step() must return observation (mandatory)

# WHAT TO INCLUDE:
# - revenue
# - expenses
# - cash
# - message

# EXAMPLE:
# revenue=2000, expenses=1000


"""
PURPOSE:
- What agent sees after each step

WHY:
- step() must return observation (mandatory)

DESIGN:
- generic structure
- supports any domain

EXAMPLE:
{
    "data": {
        "revenue": 2000,
        "expenses": 1000
    },
    "message": "current state"
}
"""

from pydantic import BaseModel
from typing import Dict, Any


class Observation(BaseModel):
    # main environment data
    data: Dict[str, Any]

    # optional message (helps LLM understanding)
    message: str = ""