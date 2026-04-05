---
title: AutoSRE Agent
emoji: 📈
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
short_description: 'An OpenEnv environment where an AI/LLM agent acts as a Site '
---

# AutoSRE-AI: OpenEnv SRE Simulation

An OpenEnv environment where an AI/LLM agent acts as a Site Reliability Engineer (SRE).
The agent perceives system health, forecasts overloads, diagnoses system crashes, and executes safe remediation actions to keep services highly available under dynamic loads.

## The Perceive-Think-Act Loop
- **Perceive**: Read simulated synthetic infrastructure metrics (CPU saturation, DB active connections, queue depth, query latency, app error rates).
- **Think**: Forecast impending traffic spikes, diagnose memory leaks, or identify failing components (caching outage).
- **Act**: Scale up nodes, kill zombie DB transactions, reroute traffic from overloaded instances, or restart faulty microservices securely.

## Observation Space
The agent receives a full-state JSON metric burst each step:
- `cpu_usage`: Dictionary of servers mapping to float utilization %.
- `db_connections`: Current active DB connection threads.
- `queue_depth`: Accumulated unprocessed task queue integers.
- `latency`: Current sub-second request response time.
- `error_rate`: Percentage of HTTP 5xx responses out of total traffic.
- `traffic_level`: Active inbound API request levels.
- `active_alerts`: Live cluster-level PagerDuty style alert feeds.
- `cache_status`: Heartbeat enum (healthy/failed).

## Action Space
The agent can execute explicit operational remediation functions via JSON payloads:
```json
{
  "action_type": "<action>",
  "target": "<target>"
}
```
Available operations: `scale_up`, `scale_down`, `kill_zombies`, `route_traffic`, `clear_cache`, `restart_service`.

## Scenarios (3 Graded Tasks)
The environment dynamically evaluates recovery speed, avoidance of over-scaling/useless commands, error stabilization, and workflow sequence natively across three tasks:
1. **Easy (`sre-easy-cpu-spike`)**: Inbound traffic rapidly saturates standard compute thresholds.
2. **Medium (`sre-medium-db-zombie`)**: Subtle, non-traffic-bound memory/connection leak flooding database thresholds dynamically, causing escalating query latency. 
3. **Hard (`sre-hard-cache-failure`)**: Complete Cache subsystem crash driving explosive un-cached fallback load onto the database/compute layers. Agents MUST isolate traffic -> dump corruption -> reboot caches securely.

## How to Test

### 1. Requirements Setup
First, install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Deterministic Logic Demo (No Keys Required)
If you just want to evaluate the underlying environment physics, graders, and state transitions without configuring an LLM, run the hardcoded proof-of-concept demo:
```bash
python demo.py
```

### 3. Run LLM Agent Simulation
To run the automated `inference.py` grader loop and watch the LLM solve the environments organically, configure your API keys on the CLI:

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="your_openai_api_key_here"
$env:MODEL_NAME="gpt-4o"
python inference.py
```

**Linux/Mac:**
```bash
export HF_TOKEN="your_openai_or_hf_api_key_here"
export MODEL_NAME="gpt-4o"
python inference.py
```

*(Note: The script defaults to `gpt-4o`, but respects the `$MODEL_NAME` flag if you want to swap the AI engine dynamically).*

### 3. Deploy via Docker (HuggingFace Validator)
The environment ships pre-configured with a direct HTTP API compliant with the standard containerized configurations expected in the OpenEnv platform:
```bash
docker build -t sre-agent .
docker run -p 7860:7860 sre-agent
```