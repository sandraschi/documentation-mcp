# Traefik Integration Guide

**Status:** Infrastructure Backbone
**Role:** Edge Router / Reverse Proxy / SSL Terminator

## Overview

Traefik is the gatekeeper. It manages all incoming traffic to our dockerized services, handles automatic SSL certificate generation (Let's Encrypt), and routes requests based on subdomains (e.g., `plex.sandra.local`, `sonarr.sandra.local`).

## Why Traefik?
- **Dynamic Discovery**: It watches the Docker socket. Spin up a container with a label, and Traefik automatically routes to it. No config file edits needed.
- **Middlewares**: Secure headers, basic auth, rate limiting in one place.
- **Let's Encrypt**: Zero-touch HTTPS.

## Configuration (Sandra Standard)

We use `docker-compose` labels to configure Traefik.

### The Traefik Container
```yaml
  traefik:
    image: traefik:v3.1.1+
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080" # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

### Service Labels (Example: Sonarr)
Add these to your Arr/Plex/Homarr containers:

```yaml
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.sonarr.rule=Host(`sonarr.local`)"
      - "traefik.http.routers.sonarr.entrypoints=web"
```

## Integration with Authentik
Traefik acts as the enforcer for Authentik.
1. Request hits Traefik.
2. Traefik sends "ForwardAuth" request to Authentik.
3. Authentik says "Nay" -> Redirect to login.
4. Authentik says "Aye" -> Traefik allows traffic to service.

*Traffic control with precision.*

