# Voice Command Bus (fleet project index)

**Standard:** [../standards/VOICE_COMMAND_BUS.md](../standards/VOICE_COMMAND_BUS.md)  
**Registry:** [../config/voice_command_bus.yaml](../config/voice_command_bus.yaml)

| Role | Repo | Doc |
|------|------|-----|
| Ingress (wake + STT) | speech-mcp | [speech-mcp/docs/VOICE_COMMAND_BUS.md](file:///D:/Dev/repos/speech-mcp/docs/VOICE_COMMAND_BUS.md) |
| Router | fleet-agent-mcp | `POST /api/voice/intent`, `route_voice_command` |
| Alexa acoustic | alexa-mcp | [alexa-mcp/docs/VOICE_COMMAND_BUS.md](file:///D:/Dev/repos/alexa-mcp/docs/VOICE_COMMAND_BUS.md) |
| Boomy robot | yahboom-mcp | [yahboom-mcp/docs/VOICE_COMMAND_BUS.md](file:///D:/Dev/repos/yahboom-mcp/docs/VOICE_COMMAND_BUS.md) |

**Example:** wakeywakey → *"boomy go on patrol and report what you found"* → `yahboom_agent_mission`.
