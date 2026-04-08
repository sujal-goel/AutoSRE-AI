
"""
OpenEnv Inference Script: Runs SRE tasks sequentially.
"""
import os
import asyncio
from openai import AsyncOpenAI
import json
from dotenv import load_dotenv

from app.env.environment import Environment
from app.models.action import Action
from app.tasks.easy import check_easy_success
from app.tasks.medium import check_medium_success
from app.tasks.hard import check_hard_success

load_dotenv()

# CONFIG
BENCHMARK = "sre-benchmark"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise RuntimeError("Missing API key. Set HF_TOKEN or OPENAI_API_KEY in your environment or .env file.")

TASKS = [
    ("sre-easy-cpu-spike", check_easy_success),
("sre-medium-db-zombie", check_medium_success),
("sre-hard-cache-failure", check_hard_success)
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
        return Action(action_type=data.get("action_type", ""), parameters={"target": data.get("target", "")})
    except Exception as e:
        print(f"LLM Exception: {str(e)}", flush=True)
        return Action(action_type="unknown", parameters={})

async def run_task(task_name: str, grader_func, client: AsyncOpenAI):
    env = Environment()
    rewards = []
    step_count = 0
    score = 0.0
    success = False

    log_start(task_name, BENCHMARK, MODEL_NAME)
    try:
        observation = env.reset()
        done = False

        while step_count < env.max_steps and not done:
            step_count += 1
            action = await get_action_from_llm(client, json.dumps(observation.model_dump()))

            if action.action_type == "unknown":
                error_val = "json parse error"
                reward = 0.0
                done = True
            else:
                observation, reward, done, _ = env.step(action)
                error_val = None

            rewards.append(reward)
            target = (action.parameters or {}).get("target", "")
            log_step(
                step=step_count,
                action=f"{action.action_type}_{target}",
                reward=reward,
                done=done,
                error=error_val,
            )

        score = grader_func(env.state().data)
        success = score > 0.5
    finally:
        try:
            close_result = env.close()
            if asyncio.iscoroutine(close_result):
                await close_result
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)

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