
"""
🔥 CORE FILE (MOST IMPORTANT)

PURPOSE:
- Implement OpenEnv environment

REQUIRED (from problem):
- reset()
- step(action)
- state()

FLOW:
reset() → initial state
step() → apply action → update → reward → done
state() → return full state
"""

from app.models.action import Action
from app.models.observation import Observation
from app.models.state import State

from app.env.logic import apply_action, calculate_reward, check_done
from dotenv import load_dotenv
load_dotenv()

class Environment:

    def __init__(self):
        self.max_steps = 10
        self.reset()

    def reset(self):
        """
        PURPOSE:
        - Initialize environment

        RETURNS:
        - initial observation
        """

        self._state = State(
            step_count=0,
            done=False,
            data={
                "value": 0  # generic starting variable
            }
        )

        return self._get_observation()

    def step(self, action: Action):
        """
        PURPOSE:
        - Apply action and move environment forward

        INPUT:
        - action (from agent)

        RETURNS:
        - observation, reward, done, info
        """

        if self._state.done:
            return self._get_observation(), 0.0, True, {}

        # increment step
        self._state.step_count += 1

        # apply action using logic.py
        self._state.data = apply_action(
            self._state.data,
            action.action_type,
            action.parameters or {}
        )

        # calculate reward
        reward = calculate_reward(self._state.data)

        # check done condition
        self._state.done = check_done(self._state.step_count, self.max_steps)

        return self._get_observation(), reward, self._state.done, {}

    def state(self):
        """
        PURPOSE:
        - Return full internal state
        """

        return self._state

    def state_fn(self):
        """
        PURPOSE:
        - Return full internal state
        """

        return self.state()

    async def close(self):
        return None

    def _get_observation(self):
        """
        PURPOSE:
        - Convert state → observation
        """

        return Observation(
            data=self._state.data,
            message="Current environment state"
        )