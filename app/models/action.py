# PURPOSE:
# - Define what actions agent can take

# WHY (problem statement):
# - step(action) required → agent interacts using action

# WHAT TO WRITE:
# - action_type (string)
# - amount (number)

# EXAMPLE:
# "invest", 1000
# "cut_cost", 500


"""
PURPOSE:
- Define actions agent can take

WHY (from problem):
- step(action) → agent interacts using actions

DESIGN:
- generic (works for ANY project)
- flexible parameters

EXAMPLE:
{
    "action_type": "invest",
    "parameters": {"amount": 1000}
}
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional


class Action(BaseModel):
    # type of action
    action_type: str

    # extra parameters (flexible)
    parameters: Optional[Dict[str, Any]] = {}