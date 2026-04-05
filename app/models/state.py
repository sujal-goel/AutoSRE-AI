# PURPOSE:
# - internal full environment data

# WHY:
# - required for state() function

# WHAT TO INCLUDE:
# - step_count
# - current financial values
# - done flag

# USED FOR:
# - debugging
# - tracking progress


"""
PURPOSE:
- internal full environment state

WHY:
- required for state() function
- used for debugging + tracking

DESIGN:
- includes system-level info
- includes environment data

EXAMPLE:
{
    "step_count": 1,
    "done": False,
    "data": {...}
}
"""

from pydantic import BaseModel
from typing import Dict, Any


class State(BaseModel):
    # step number
    step_count: int = 0

    # environment finished or not
    done: bool = False

    # internal data
    data: Dict[str, Any] = {}