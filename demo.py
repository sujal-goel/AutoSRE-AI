"""
SRE Environment Demo Script
A deterministic, API-free demonstration of the AutoSRE-AI environment physics.
Run this script to manually verify the state transitions, reward logic, and graders
without requiring an LLM connection or external API keys!
"""
import time
from app.env.environment import Environment
from app.models.action import Action
from app.grader.grader import grade_easy_task, grade_medium_task, grade_hard_task

def run_demo():
    print("="*60)
    print("AutoSRE-AI: OpenEnv Deterministic Physics Demo")
    print("="*60)
    
    env = Environment()

    tasks = [
        (
            "sre-easy-cpu-spike", 
            grade_easy_task,
            [
                Action(action_type="scale_up", target="server_1"),
                Action(action_type="scale_up", target="server_1"),
                # Agent realizes load is managed, decides not to overscale
                Action(action_type="scale_down", target="server_1"),
            ]
        ),
        (
            "sre-medium-db-zombie", 
            grade_medium_task,
            [
                # Agent precisely purges ghost connections 
                Action(action_type="kill_zombies", target="primary"),
            ]
        ),
        (
            "sre-hard-cache-failure", 
            grade_hard_task,
            [
                # Full cascade isolate and wipe workflow
                Action(action_type="route_traffic", target="backup_zone"),
                Action(action_type="clear_cache", target="global"),
                Action(action_type="restart_service", target="primary"),
            ]
        )
    ]

    for task_name, grader, actions in tasks:
        print(f"\n\n[STARTING TASK]: {task_name}")
        obs = env.reset(task_name=task_name)
        
        print(f"   [!] Initial Alerts: {obs.active_alerts}")
        print(f"   [~] CPU: {obs.cpu_usage} | DB Threads: {obs.db_connections}")
        print("-" * 50)
        
        step_count = 0
        rewards = []
        for action in actions:
            step_count += 1
            print(f"Step {step_count:02} | Action: [ {action.action_type.upper()} ] target -> {action.target}")
            obs, reward, done, _ = env.step(action)
            rewards.append(reward)
            
            print(f"        -> Inst-Reward: {reward:+.2f}")
            print(f"        -> Latency: {obs.latency:.2f}s | App Errors: {obs.error_rate:.2%}")
            if obs.active_alerts:
                print(f"        -> Still active: {obs.active_alerts}")
            time.sleep(0.6)
            if done:
                break
                
        # Fast forward remaining steps doing nothing to hit max states or done
        # This simulates the environment stabilizing or crashing
        print("\n   ... Fast-forwarding remaining environment steps (Agent idle) ...")
        while step_count < env.max_steps and not env._state.done:
             step_count += 1
             obs, reward, done, _ = env.step(Action(action_type="unknown", target=""))
             rewards.append(reward)
             if done: break
             
        score = grader(env.state())
        print("-" * 50)
        print(f"Task '{task_name}' Ended.")
        print(f"Final Grader Score: {score:.2f} / 1.0 (Higher is better)")

if __name__ == "__main__":
    run_demo()
