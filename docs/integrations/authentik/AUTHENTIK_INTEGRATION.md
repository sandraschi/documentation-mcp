# Authentik Integration Guide

**Status:** Security Layer
**Role:** Identity Provider (IdP) / SSO / Access Control

## Overview

Authentik is the bouncer. It provides a unified identity layer for all our services. Instead of managing 20 different logins, we use one Authentik login.

## Capabilities
- **Single Sign-On (SSO)**: One login for Plex, Grafana, Portainer, Homarr, etc.
- **MFA**: Enforce 2FA/WebAuthn globally.
- **Policy Engine**: "Only access Sonarr if user is in group `Admins` and network is `Home_LAN`".

## Setup Structure
1. **Worker & Server**: The core Authentik stack.
2. **Outpost**: The component that talks to the reverse proxy (Traefik).

## Integration with Traefik (Forward Auth)

We use Authentik as a "middleware" in Traefik.

**Traefik Config:**
```yaml
http:
  middlewares:
    authentik:
      forwardAuth:
        address: http://authentik-server:9000/outpost.goauthentik.io/auth/traefik
        trustForwardHeader: true
        authResponseHeaders:
          - X-authentik-username
          - X-authentik-groups
```

**Service Label:**
```yaml
      - "traefik.http.routers.sonarr.middlewares=authentik"
```

## User Management
- **Sandra**: Admin / Superuser
- **Family**: Read-access to Plex/Overseerr requests only. No touchy the Arrs.

*Security without friction.*
