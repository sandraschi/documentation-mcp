# Virtual twins fleet — teleoperator + robotics + Resonite + LeRobot

**Last updated:** 2026-06-04

Cross-repo index for **embodied VR teleop → virtual robot → imitation-learning dataset**. Physical hardware optional.

## One-line flow

```
Pico WebXR  →  teleoperator-mcp  →  robotics-mcp  →  OSC :9000  →  Resonite vBot
                    ↓ JSONL
              export-lerobot.ps1  →  parquet  →  lerobot-train
```

## Repos

| Repo | Role | Key docs |
|------|------|----------|
| [teleoperator-mcp](https://github.com/sandraschi/teleoperator-mcp) | WebXR pose, adapters (`boomy`, `bumi`, `vboomy`), JSONL + parquet export | [VIRTUAL_TWINS.md](https://github.com/sandraschi/teleoperator-mcp/blob/master/docs/VIRTUAL_TWINS.md), [LEROBOT.md](https://github.com/sandraschi/teleoperator-mcp/blob/master/docs/LEROBOT.md), [VBOT_CREATIVE_TWINS.md](https://github.com/sandraschi/teleoperator-mcp/blob/master/docs/VBOT_CREATIVE_TWINS.md) |
| [robotics-mcp](https://github.com/sandraschi/robotics-mcp) | vbot registry, UDP OSC bridge, `platform=resonite` auto-spawn | CHANGELOG · port **12230** |
| [resonite-mcp](https://github.com/sandraschi/resonite-mcp) | ProtoFlux receiver spec, test OSC API | [VBOT_OSC_RECEIVER.md](https://github.com/sandraschi/resonite-mcp/blob/master/docs/VBOT_OSC_RECEIVER.md) |
| [bumi-mcp](https://github.com/sandraschi/bumi-mcp) | Physical Bumi bridge (when hardware arrives) | INTEGRATION.md |

## Ports

| Port | Service |
|------|---------|
| 10900 / 10901 | teleoperator webapp / backend |
| 12230 | robotics-mcp HTTP |
| 9000 | Resonite OSC **input** (world receiver) |
| 15580 | LiveKit (headset video return) |

## Bring-up checklist

1. Resonite running, OSC input **9000**, ProtoFlux receiver on `vBotRoot` ([resonite-mcp doc](https://github.com/sandraschi/resonite-mcp/blob/master/docs/VBOT_OSC_RECEIVER.md)).
2. `robotics-mcp` on `:12230`.
3. `teleoperator-mcp\scripts\start-vboomy-loop.ps1` — register `vbot_yahboom_01`.
4. Pico → `https://<tailnet>/#/?robot=vboomy` → Enter VR.
5. After sessions: `teleoperator-mcp\scripts\export-lerobot.ps1`.

## Creative vBots (Mechazilla, kaiju, …)

**Same OSC contract and LeRobot schema** for utilitarian and fictional morphologies. Resonite supports **Godzilla-scale** rigs — set spawn `scale` to 50+ (`robot_type=godzilla`).

Examples: vBoomy (training), vMechazilla (scale 2.5), vGodzilla (city block). See upstream [VBOT_CREATIVE_TWINS.md](https://github.com/sandraschi/teleoperator-mcp/blob/master/docs/VBOT_CREATIVE_TWINS.md).

## LeRobot status (2026-06)

| Step | Status |
|------|--------|
| JSONL capture on teleop WS | **Shipped** |
| Parquet export (`export-lerobot.ps1`, `POST /api/v1/recording/export`) | **Shipped** |
| Video in parquet | **Not yet** (LiveKit egress sync — M5) |
| HF Hub push | Manual / your CI |

## Pico hub

Headset path: [pico/WEBXR.md](../../pico/WEBXR.md) · [projects/teleoperator-mcp/README.md](README.md)

## Paper angle

- Same producer/arbiter/recording for **virtual and physical**
- Fleet MCP composition (not monolithic sim)
- Embodied VR with video return
- Creative morphology ablation without code forks
