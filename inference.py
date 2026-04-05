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
    prompt = f"""You are an Autonomous SRE Agent monitoring a live production cluster.

Current system observation (JSON):
{obs_text}

Your job: diagnose the incident and pick ONE remediation action.

INCIDENT GUIDE:
- High CPU usage (>80%) + active alerts -> use "scale_up" on that server
- DB connections > 4500 -> use "kill_zombies" on "primary"
- cache_status="failed" -> first "route_traffic" to "backup_zone", then "clear_cache", then "restart_service" on "primary"
- System is stable -> use "scale_down" to avoid over-provisioning costs

ACTION TYPES: scale_up, scale_down, kill_zombies, route_traffic, clear_cache, restart_service
TARGET: the server or zone name from the observation (e.g. "server_1", "primary", "backup_zone")

Respond ONLY with valid JSON, no extra text:
{{"action_type": "type", "target": "target_name"}}"""

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content

        # Strip thinking tags from reasoning models (e.g. Qwen3, DeepSeek-R1)
        import re
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # Extract first JSON block if extra text exists
        json_match = re.search(r"\{.*?\}", content, re.DOTALL)
        if json_match:
            content = json_match.group(0)

        data = json.loads(content)
        return Action(action_type=data.get("action_type", ""), target=data.get("target", ""))
    except Exception as e:
        print(f"LLM Exception: {str(e)}", flush=True)
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