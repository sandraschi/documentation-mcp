# Comms in Pure Rust (HTTP, WebSocket, MQTT, Serial)

Match the wire protocol with the smallest crate that speaks it. Everything
below is verified on crates.io 2026-10-17 and fits the Tokio workspaces.

| Protocol | Crate (version) | Notes |
|---|---|---|
| HTTPS/REST/OAuth | `reqwest` 0.12, `features = ["json"]` | Fleet default (proven: Ring/Tapo/Netatmo/Hue/ONVIF). Default-tls is Schannel on Windows — no OpenSSL pain. Timeouts on every client (`Builder::timeout`), logs on stderr. |
| WebSocket | `tokio-tungstenite` 0.30 | Tokio-native WS client/server (Tungstenite core). First choice for streaming endpoints, live telemetry sockets, MCP-over-WS experiments. |
| MQTT (IoT) | `rumqttc` 0.25 | Efficient, robust async MQTT client — the obvious next driver transport for Shelly/Tasmota/ESPHome fleets (all speak MQTT natively). Pair with `rumqttd` for a local broker in tests. |
| Serial/UART/USB | `serialport` 4.10 | Cross-platform serial (Wien Energie M-Bus meters, Arduinos, GPS pucks, 3D printers). Enumerate ports, set timeouts, never block the Tokio runtime (use `spawn_blocking`). |

Rules: one client per vendor module (no shared global client with mixed
timeouts); every call wrapped in `tokio::time::timeout` mapped to the typed
`DeviceError::Timeout`; hosts/ports from args → env → fleet import, never
hardcoded; secrets never logged (see the Ring 406/User-Agent bounty — when
a cloud API rejects you with an empty body, suspect headers first).
