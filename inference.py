# 🔥 VERY VERY IMPORTANT

# PURPOSE:
# - run agent on environment

# WHY:
# - mandatory (else disqualified)

# MUST FOLLOW FORMAT:

# [START]
# [STEP]
# [END]

# RULE:
# - strict format (no change allowed)

# WHAT IT DOES:
# - call reset()
# - loop step()
# - log output


"""
🔥 PURPOSE:
- Run agent inside environment
- Generate reproducible baseline score

⚠️ VERY IMPORTANT (from problem):
- MUST print:
    [START]
    [STEP]
    [END]

- Format must NOT change
"""

import asyncio
import os
from typing import List, Optional

from app.env.environment import Environment
from app.models.action import Action
from app.llm.router import get_llm
from app.config.settings import settings


# CONFIG
TASK_NAME = "generic-task"
BENCHMARK = "ai-env"
MAX_STEPS = 10


# ---------------- LOG FUNCTIONS ---------------- #

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True
    )


def log_end(success: bool, steps: int, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True
    )


# ---------------- AGENT LOGIC ---------------- #

def get_action_from_llm(llm, observation_text: str) -> str:
    """
    PURPOSE:
    - Ask LLM what action to take

    OUTPUT:
    - simple action string
    """

    prompt = f"""
    You are an agent in an environment.

    Current state:
    {observation_text}

    Choose next action:
    - increase value
    - decrease value

    Reply ONLY with:
    increase or decrease
    """

    try:
        response = llm.generate(prompt)
        return response.strip().lower()
    except:
        return "increase"


# ---------------- MAIN FUNCTION ---------------- #

async def main():

    # initialize environment + llm
    env = Environment()
    llm = get_llm()

    rewards = []
    steps_taken = 0

    log_start(TASK_NAME, BENCHMARK, settings.MODEL_NAME)

    try:
        # RESET
        observation = env.reset()

        for step in range(1, MAX_STEPS + 1):

            if env.state.done:
                break

            # convert observation to text
            obs_text = str(observation.data)

            # get action from LLM
            action_str = get_action_from_llm(llm, obs_text)

            # map to Action model
            if "decrease" in action_str:
                action = Action(action_type="decrease", parameters={"value": 10})
            else:
                action = Action(action_type="increase", parameters={"value": 10})

            # STEP
            observation, reward, done, _ = env.step(action)

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=action.action_type,
                reward=reward,
                done=done,
                error=None
            )

            if done:
                break

        # SUCCESS CONDITION
        total_reward = sum(rewards)
        success = total_reward > 0.1

    except Exception as e:
        success = False
        print(f"[DEBUG] Error: {e}")

    finally:
        log_end(success, steps_taken, rewards)


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    asyncio.run(main())