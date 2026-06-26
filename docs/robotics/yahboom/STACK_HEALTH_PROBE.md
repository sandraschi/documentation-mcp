# Stack health probe (`GET /api/v1/health` → `stack`)

**MCP Central Docs (RAG):** this page is the **full reference** for the stack snapshot and container diagnostics so the docs webapp can retrieve it without opening the **yahboom-mcp** repo. Implementation source code: **`yahboom-mcp`** → `src/yahboom_mcp/stack_probe.py`, `src/yahboom_mcp/server.py` (health payload). When behavior or JSON fields change, update **this file** and the parallel **`yahboom-mcp/docs/ops/STACK_HEALTH_PROBE.md`**.

**Operator context:** Goliath runs **yahboom-mcp**; the **Dashboard** (`/dashboard`) and **Diagnostic Hub** (`/diagnostics`) render **`StackStatusTable`** when **`health.stack`** is present. Boot order and webapp roles: **[STARTUP_AND_BRINGUP.md](STARTUP_AND_BRINGUP.md)**.

---

## API

- **HTTP:** `GET /api/v1/health` on the MCP gateway (default **10892** when running dual mode).  
- **JSON path:** root **`stack`** (object). Omitted or partial only if the server cannot assemble probes (e.g. no robot target); normally present when the health handler runs stack assembly.  
- **TypeScript (dashboard):** `webapp/src/lib/api.ts` → **`StackOverview`**, **`Health.stack`**.

---

## Top-level `stack` object (semantic index)

| Key | Meaning |
|-----|--------|
| **`probed_at`** | ISO8601 UTC timestamp of this snapshot. |
| **`cache_ttl_sec`** | Seconds the server may reuse cached SSH-heavy probes (from **`YAHBOOM_STACK_PROBE_SECS`**). |
| **`goliath_to_robot`** | TCP probes from this PC to robot **SSH :22** and **rosbridge** port; robot IP and port echoed; human **`summary`**. |
| **`ssh_session`** | Whether Paramiko session is up; target host; **`summary`**. |
| **`pi_host`** | Hostname, primary IP, optional **`all_ips`**, **`interfaces_preview`**, **`wifi`** (`state`, `ssid`, `raw_preview`), **`summary`**. |
| **`docker_engine`** | **`systemd_active`** for Docker daemon, optional **`server_version`**, **`summary`**. |
| **`ros_container`** | Docker **`inspect`**-derived state for **`YAHBOOM_ROS2_CONTAINER`**, lifecycle, logs preview, remediation — see next section. |
| **`ros_graph_in_container`** | Cached **`ros2 node list`** inside the container (driver stack / rosbridge presence); **`status`**, **`detail`**, **`matched_nodes`**, **`rosbridge_node_seen`**, etc. |
| **`rosbridge_from_pc`** | WebSocket/cmd_vel readiness from the bridge client’s point of view; **`summary`**. |
| **`video`** | VideoBridge active flag and **`summary`**. |
| **`layers`** | Array of **`{ id, title, ok, detail }`** for the stack table UI (order bottom-up narrative). |

---

## Stack table `layers[].id` values (fixed order)

Use these strings when searching logs or writing UI automation:

1. **`goliath_tcp`** — This PC → robot TCP (**:22**, rosbridge port).  
2. **`ssh_session`** — SSH control session.  
3. **`pi_network`** — Pi hostname, IP, Wi‑Fi.  
4. **`docker_engine`** — Pi Docker daemon.  
5. **`ros_container`** — Named ROS container; title may append **`— RESTART LOOP`** when **`restart_loop`** is true.  
6. **`ros_graph_docker`** — ROS 2 graph inside the container.  
7. **`rosbridge_graph`** — Whether **rosbridge_websocket** appears in that graph.  
8. **`rosbridge_pc`** — This PC → rosbridge WebSocket.  
9. **`cmd_vel`** — Bridge **`/cmd_vel`** advertised.  
10. **`video`** — Video pipeline.

---

## `ros_container` fields (full list for RAG)

| Field | Type / role |
|-------|-------------|
| **`name`** | Container name probed (from **`YAHBOOM_ROS2_CONTAINER`**). |
| **`running`** | Boolean or null from Docker **`State.Running`**. |
| **`docker_state`** | Lowercased Docker **`State.Status`** string (e.g. contains **`exited`**, **`restarting`**, **`running`**). |
| **`started_at`**, **`finished_at`** | Docker State timestamps (API zero dates treated as “no time”). |
| **`exit_code`**, **`oom_killed`**, **`error`** | Exit code, OOM flag, engine error string when present. |
| **`docker_ps_preview`** | Short **`docker ps -a`** text (names + status) for context. |
| **`alternate_running_container`** | Another **`yahboom*`** container name that is **Up** if the configured name is wrong. |
| **`restart_loop`** | **true** when lifecycle phase is **`restart_loop`** (Docker restart crash loop). |
| **`lifecycle`** | **`{ phase, label, detail }`** — see **Lifecycle phases** below. |
| **`remediation_steps`** | String array of operator hints (**`docker logs`**, **`docker start`**, **`YAHBOOM_ROS2_CONTAINER`**, OOM 137, etc.). |
| **`docker_logs_preview`** | Redacted tail of **`docker logs`** when unhealthy; null when skipped. |
| **`docker_logs_error`** | Short error if log fetch failed. |
| **`docker_logs_truncated`** | Boolean if preview was cut for **`YAHBOOM_DOCKER_LOGS_MAX_CHARS`**. |
| **`docker_logs_lines_fetched`** | Line count after sanitization (approximate). |
| **`summary`** | One-line human summary for tables. |

---

## Environment variables (Goliath / `yahboom-mcp` process)

| Variable | Default | Meaning |
|----------|---------|--------|
| **`YAHBOOM_ROS2_CONTAINER`** | `yahboom_ros2_final` | Passed to **`docker inspect`**, **`docker logs`**, and **`docker exec … ros2 node list`**. Must match **`docker ps`** on the Pi. Factory **`setup-autostart.sh`** may use **`yahboom_ros2`**. |
| **`YAHBOOM_STACK_PROBE_SECS`** | `5` | TTL for recomputing cached stack / driver probes (seconds). |
| **`YAHBOOM_DOCKER_LOGS_TAIL`** | `80` | Lines for **`docker logs`** (clamped **10–200** in code). |
| **`YAHBOOM_DOCKER_LOGS_MAX_CHARS`** | `16000` | Max characters for log preview after redaction (clamped **2000–64000**). |

Container names must match **`^[a-zA-Z0-9][a-zA-Z0-9_.-]*$`** and length ≤ **128** for log fetch; otherwise **`docker_logs_error`** is set and logs are not retrieved.

---

## Lifecycle phases (`lifecycle.phase`)

Derived from **`docker inspect`** JSON **`.State`**: **`Running`**, **`Status`**, **`StartedAt`**, **`FinishedAt`**, **`ExitCode`**, **`OOMKilled`**, **`Error`**.

| **`phase`** | **`label`** (typical) | Meaning |
|---------------|------------------------|--------|
| **`running`** | Running now | Main process up at probe time. |
| **`never_started`** | Never run to completion | **`created`** or no meaningful start time; often needs **`docker start`**. |
| **`ran_then_stopped`** | Started, then exited | Process ran and stopped; use exit code and **`docker_logs_preview`**. |
| **`restart_loop`** | Restart loop (crash loop) | **`restarting`** in status — Docker repeatedly starts then loses the process. |
| **`paused`** | Paused | **`docker pause`** state. |
| **`removing`** | Removing | Transient teardown. |
| **`not_found`** | Wrong or missing name | No container with configured name. |
| **`no_ssh`** | SSH offline | Cannot read Pi Docker state. |
| **`unknown`** / **`unavailable`** | Could not classify / State unreadable | Parse or inspect errors. |

**UI:** **Run history** shows **`label`** and **`detail`**. **Restart loop:** amber banner, highlighted **`ros_container`** table row, **Loop** badge instead of red **FAIL**, **`ROS container`** remediation header suffix **`· restart loop`**.

---

## Docker log preview (when it runs)

Fetched over SSH when SSH is connected, container is **not** **`not_found`**, and **not** the case (**`running` === true** and **not** **`restart_loop`**). Skipped for steady healthy containers to limit load and payload size.

**Redaction (best effort):** `password=` / `token=` / `api_key`-style pairs, **`Authorization: Bearer …`**, simple AWS-style key env patterns, PEM **private key** lines; per-line length cap then global **`YAHBOOM_DOCKER_LOGS_MAX_CHARS`**. **Not a security boundary** for highly sensitive deployments — restrict network access to **`/api/v1/health`**.

---

## Agent mission planner (embodied goals)

- **HTTP:** `POST /api/v1/agent/mission` on the MCP gateway (same host/port as health).  
- **Body:** `{ "goal": "string", "provider": "auto" | "ollama" | "gemini", "publish_to_ros": true, "speak": false }`.  
- **Response:** `{ "success", "provider", "plan", "published_to_ros", "mission_topic", "publish_error?", "spoke?" }` where **`plan`** matches **`MissionPlanV1`** (version, intent, behavior, target_description, suggested_ros_topics, voice_feedback, safety_notes, estimated_duration_sec).  
- **ROS:** When **`publish_to_ros`** is true and the bridge is **ROS2Bridge**, the plan JSON is published once on **`std_msgs/String`** (default topic **`/boomy/mission`**, override with **`YAHBOOM_MISSION_TOPIC`**). **Shipped executor:** in **yahboom-mcp** clone **`ros2/boomy_mission_executor`** — `colcon build --packages-select boomy_mission_executor`, `ros2 run boomy_mission_executor mission_executor` (or `ros2 launch boomy_mission_executor mission_executor.launch.py`). Extend that node for Nav2, PTZ, or detectors (e.g. “find Benny”).  
- **LLM backends:** **Ollama** uses the dashboard-selected model (`GET/PUT /api/v1/settings/llm`). **Gemini** uses **`YAHBOOM_GEMINI_API_KEY`** and **`YAHBOOM_GEMINI_MISSION_MODEL`** (default **`gemini-2.0-flash`**; set a **Gemini Robotics‑ER** model id when your Google AI project exposes it). **`provider`: `auto`** picks Gemini if the API key is set, otherwise Ollama.  
- **`speak`:** If true, **`voice_feedback`** is sent to the Yahboom voice module over **SSH** (truncated).

---

## RAG keywords (synonyms)

stack health, health.stack, StackOverview, StackStatusTable, docker inspect, docker logs, restart loop, crash loop, exited container, YAHBOOM_ROS2_CONTAINER, ros2 node list, driver stack, rosbridge graph, Goliath TCP, Pi Wi‑Fi, docker ps preview, remediation, OOM 137, never started, created container, YAHBOOM_STACK_PROBE_SECS, diagnostics dashboard layers.
