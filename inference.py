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
OpenEnv Inference Script: Runs SRE tasks sequentially.
"""
import os
import asyncio
from openai import AsyncOpenAI
import json

from app.env.environment import Environment
from app.models.action import Action
from app.grader.grader import grade_easy_task, grade_medium_task, grade_hard_task

# CONFIG
BENCHMARK = "sre-benchmark"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
HF_TOKEN = os.getenv("HF_TOKEN", "")
API_KEY = HF_TOKEN if HF_TOKEN else "sk-fake-key" # fallback for local execution without error

TASKS = [
    ("sre-easy-cpu-spike", grade_easy_task),
    ("sre-medium-db-zombie", grade_medium_task),
    ("sre-hard-cache-failure", grade_hard_task)
]

def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: str):
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: list[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

async def get_action_from_llm(client: AsyncOpenAI, obs_text: str) -> Action:
    prompt = f"""
    You are an Autonomous SRE Agent.
    
    Current state observation:
    {obs_text}
    
    Choose ONE action_type:
    - scale_up
    - scale_down
    - kill_zombies
    - route_traffic
    - clear_cache
    - restart_service

    Choose target (server ID or service name, e.g. "server_1", "primary", "backup_zone").
    
    Respond in STRICT JSON format:
    {{"action_type": "type", "target": "target_name"}}
    """

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return Action(action_type=data.get("action_type", ""), target=data.get("target", ""))
    except Exception as e:
        return Action(action_type="unknown", target="")

async def run_task(task_name: str, grader_func, client: AsyncOpenAI):
    env = Environment()
    rewards = []
    
    log_start(task_name, BENCHMARK, MODEL_NAME)
    
    observation = env.reset(task_name=task_name)
    done = False
    step_count = 0
    
    while step_count < env.max_steps and not done:
        step_count += 1
        
        # LLM Call
        action = await get_action_from_llm(client, json.dumps(observation.model_dump()))
        
        # In case action failed to parse
        if action.action_type == "unknown":
             error_val = "json parse error"
             reward = 0.0
             done = True
        else:
             observation, reward, done, _ = env.step(action)
             error_val = None
             
        rewards.append(reward)
        log_step(step=step_count, action=f"{action.action_type}_{action.target}", reward=reward, done=done, error=error_val)
        
    # Grading
    score = grader_func(env.state())
    success = score > 0.5
    
    log_end(success=success, steps=step_count, score=score, rewards=rewards)

async def main():
    max_retries = 3
    client = AsyncOpenAI(
        api_key=API_KEY,
        base_url=API_BASE_URL,
        max_retries=max_retries
    )
    
    for task_name, grader_func in TASKS:
        await run_task(task_name, grader_func, client)

if __name__ == "__main__":
    asyncio.run(main())