# Caddy Web Server Evaluation

**Date:** 2026-06-25  
**Status:** Recommended — high value for fleet consolidation  
**Source:** https://github.com/caddyserver/caddy  
**License:** Apache 2.0  

---

## 1. What it is

A **Go-based web server and reverse proxy** that auto-configures HTTPS and exposes a full REST API for live config changes. Think "nginx but with auto-TLS and an API you can drive programmatically."

| Contrast | Caddy | nginx | HAProxy |
|---|---|---|---|
| **TLS** | Auto (Let's Encrypt + ZeroSSL) | Manual (certbot) | Manual |
| **Config API** | Built-in REST (2000+ endpoints) | None | None (socket) |
| **Binary** | ~20 MB, static Go | ~3 MB + libc | ~15 MB |
| **Config format** | Caddyfile (human-friendly) or JSON | nginx.conf DSL | haproxy.cfg |
| **Hot reload** | Via API, zero-downtime | Requires reload | Requires reload |

---

## 2. License

**Apache 2.0** — fully permissive, no restrictions. Core, CertMagic (the ACME/TLS library), and all standard modules.

---

## 3. Stars & activity

62k stars, thousands of commits, hundreds of contributors. Backed by ZeroSSL. Documentation at caddyserver.com is excellent.

---

## 4. Fleet fit — the core pitch

The fleet has 85+ MCP webapps on separate ports in the 10700-11500 range. Currently you need to remember the port number for each one. **Caddy solves this** — it becomes a single entry point for all webapps.

### Strategy A: Subdomain-per-app (recommended)

```caddyfile
# *.fleet.local domains — Caddy's built-in CA auto-generates
# locally-trusted certs. No DNS config needed on LAN.
email.fleet.local       { reverse_proxy localhost:10812 }
pywinauto.fleet.local   { reverse_proxy localhost:10789 }
arr.fleet.local         { reverse_proxy localhost:10939 }
godot.fleet.local       { reverse_proxy localhost:10992 }
# ... add as many as needed — Caddy handles hundreds of thousands of routes
```

Add a new webapp with one API call:

```powershell
curl -X POST "http://localhost:2019/config/apps/http/servers/fleet/routes/..." \
    -H "Content-Type: application/json" \
    -d '{
        "match": [{"host": ["newapp.fleet.local"]}],
        "handle": [{"handler": "reverse_proxy", "upstreams": [{"dial": "localhost:10999"}]}]
    }'
```

### Strategy B: Path-based on single domain

```caddyfile
fleet.local {
    handle_path /email/*     { reverse_proxy localhost:10812 }
    handle_path /pywinauto/* { reverse_proxy localhost:10789 }
    handle_path /arr/*       { reverse_proxy localhost:10939 }
}
```

---

## 5. Key features for fleet use

| Feature | What it gives us |
|---|---|
| **Auto-HTTPS** | Every fleet webapp gets TLS automatically with locally-trusted certs (no self-signed warnings) |
| **REST API** | Add/remove/update webapp routes programmatically from an MCP tool |
| **Tailscale plugin** | Serve fleet apps over Tailscale without public exposure |
| **Health checks** | Active probe of each backend, auto-remove dead backends |
| **Load balancing** | Multiple instances of a service if needed |
| **Templates** | Could generate a fleet landing page with server-side includes |
| **Windows service** | Runs as native Windows service via sc.exe or WinSW |

---

## 6. Resource requirements

- **Binary:** ~20 MB, static Go (no runtime deps)
- **RAM:** ~10-20 MB idle, negligible per-request overhead
- **CPU:** Comparable to nginx for reverse proxy workloads

---

## 7. Limitations

- Slightly heavier than nginx at idle (Go vs C), negligible for fleet use
- No built-in WAF/mod_security equivalent (use a separate layer if needed)
- Must use forward slashes in paths even on Windows
- Service registration on Windows requires sc.exe or WinSW (not systemd)

---

## 8. Verdict

**Strong yes for fleet consolidation.** Single binary, minimal overhead, auto-TLS eliminates certificate pain, REST API enables programmatic fleet management. The win is not needing to remember port numbers — just `http://email.fleet.local`. Deployable in 30 minutes.
