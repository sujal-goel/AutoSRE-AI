# PURPOSE:
# - expose API endpoints

# WHY:
# - OpenEnv works via HTTP

# ENDPOINTS:

# POST /reset
# → start environment

# POST /step
# → send action → get result

# GET /state
# → get current state

# NOTE:
# - required for validation


"""
PURPOSE:
- Expose API endpoints for environment

WHY (from problem):
- OpenEnv environment must be accessible via API
- Required endpoints:
    1. /reset
    2. /step
    3. /state

FLOW:
Client → API → Environment → Response

IMPORTANT:
- This file connects frontend / Postman / inference script to env
"""

from fastapi import FastAPI
from app.env.environment import Environment
from app.models.action import Action

# create FastAPI app
app = FastAPI()

# create global environment instance
env = Environment()


@app.post("/reset")
def reset():
    """
    PURPOSE:
    - Start new episode

    RETURNS:
    - initial observation
    """

    observation = env.reset()

    return {
        "observation": observation
    }


@app.post("/step")
def step(action: Action):
    """
    PURPOSE:
    - Take action in environment

    INPUT:
    - action (from agent / user)

    RETURNS:
    - observation
    - reward
    - done
    """

    observation, reward, done, info = env.step(action)

    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
def get_state():
    """
    PURPOSE:
    - Get full internal state

    RETURNS:
    - state object
    """

    state = env.state_fn()

    return {
        "state": state
    }


@app.get("/")
def root():
    """
    PURPOSE:
    - Health check endpoint

    WHY:
    - required for deployment testing
    """

    return {
        "message": "AI Environment Running 🚀"
    }