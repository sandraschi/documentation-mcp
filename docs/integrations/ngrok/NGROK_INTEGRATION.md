# Ngrok Integration Guide

**Status:** Surgical Tunneling
**Role:** External Access / Webhook Ingress

## Overview

While Tailscale is our primary VPN for full mesh access, **Ngrok** is the surgical tool for exposing specific ports or webhooks to the public internet temporarily or for services that require a fixed public callback URL (like GitHub webhooks or Plex authentication callbacks during dev).

## Use Cases
1. **Dev Testing**: Exposing `localhost:3000` to a client or mobile device for testing.
2. **Webhooks**: Receiving webhooks from external APIs (Stripe, GitHub) into our local development environment.
3. **Emergency Access**: Backdoor access if Tailscale negotiation fails (rare, but possible).

## Configuration

**Command Line:**
```powershell
ngrok http 8989  # Expose Sonarr
ngrok http 32400 # Expose Plex
```

**Config File (`ngrok.yml`):**
```yaml
tunnels:
  plex:
    proto: http
    addr: 32400
    subdomain: sandra-plex-dev # usage requires paid plan usually
  sonarr:
    proto: http
    addr: 8989
```

## Security Warning ⚠️
Ngrok exposes local services to the open internet.
- **Always** use `nginx` or `authentik` behind it if exposing sensitive apps permanently.
- **Prefer Tailscale** for private access.
- Use Ngrok Inspect (`http://localhost:4040`) to debug traffic.

*Tunneling through the firewall walls.*
