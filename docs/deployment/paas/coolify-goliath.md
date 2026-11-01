# Coolify on Goliath — Build Guide (friends / family / testing)

**Last Updated:** 2026-10-22
**Status:** active
**Premise:** Goliath (Win11, Ryzen 9 5900X, 64GB, RTX 4090) always up. Very low traffic. You report a stable public IP (verify below, never commit the literal IP to git — use `<YOUR_PUBLIC_IP>` / DNS names in code).
**Result:** your own Railway on your own watts. Env stays home. €0 marginal.

Parent: [README.md](README.md). Breach context: [oct-2026-breach-runbook.md](oct-2026-breach-runbook.md). Alternatives: [alternatives.md](alternatives.md).

## 0. Verify the public IP first (2 min, do not skip)

Your router IP can look stable until it isn't (Magenta/A1 re-assign, CGNAT, DS-Lite).

```powershell
# what the internet sees right now
curl.exe -4 ifconfig.me
nslookup myip.opendns.com resolver1.opendns.com
# from phone (LTE, NOT wifi): http://<YOUR_PUBLIC_IP> should hit your router, not timeout
```

If `ifconfig.me` matches what you think (you reported 213.47.34.131) on 2 different days + reboot, treat as stable. Still: create a DynDNS name (desec.io, afraid.org, or router vendor) pointing at it — one CNAME change saves you later. In this doc: `<YOUR_PUBLIC_IP>` and `demo.yourdomain.at`.

Reverse check (optional): `nslookup 213.47.34.131` usually shows `*.upc.at / *.magenta.at` on this range — normal for AT cable.

## 1. Architecture (what we build)

```
Internet (<YOUR_PUBLIC_IP> :80/:443)
  └─ Router port-forward 80/443 → 192.168.1.50 (coolify VM)
Goliath Win11 (always up)
  ├── Ollama :11434, NSSM fleet 10700-15000 (unchanged, RTX 4090 stays here)
  └── Hyper-V VM "coolify" Ubuntu 24.04 LTS
       ├── Docker + Coolify :8000 (ADMIN, Tailscale-only, never public)
       ├── app :80/:443 → demo.yourdomain.at (static or backend+frontend)
       └── postgres/redis (Coolify one-click, volumes on VHDX)
Friends/family → https://demo.yourdomain.at (public) OR Tailscale share (private)
Apps in VM → http://<GOLIATH_LAN_IP>:11434 for LLM (no GPU in VM, by design)
```

Why a VM, not Docker Desktop / WSL2: Coolify install script targets Debian-based Linux + systemd + Docker Engine. WSL2 has no systemd by default, restarts oddly, networking NATs twice. A Gen2 Hyper-V VM is isolated, snapshottable, static-IP-able, and survives Docker Desktop updates.

## 2. Hyper-V VM spec (exact)

| Item | Value |
|------|-------|
| Name | `coolify` |
| Generation | Gen2, Secure Boot = Microsoft UEFI Certificate Authority (Ubuntu template) |
| vCPU | 4 (reserve 2 minimum if Goliath loaded) |
| RAM | 8192 MB static (not dynamic for Docker stability; you have 64GB) |
| Disk | 80 GB dynamic VHDX (`C:\VMs\coolify\coolify.vhdx`), ext4 inside |
| Switch | External vSwitch bound to the physical NIC that has internet (not Default Switch) |
| Network | Static LAN IP `192.168.1.50/24`, gateway = router, DNS = router or 1.1.1.1. DHCP reservation in router by VM MAC |
| OS | Ubuntu Server 24.04 LTS, OpenSSH server, no snaps you don't need |
| Checkpoints | Production checkpoints on before updates, off during normal ops |
| Auto-start | Automatic Start Action = Always start, delay 60s (so host NIC is ready) |

PowerShell (admin, adjust switch name + paths):

```powershell
# one-time: external switch if missing
# New-VMSwitch -Name "External" -NetAdapterName "Ethernet" -AllowManagementOS $true

New-VM -Name "coolify" -Generation 2 -MemoryStartupBytes 8GB `
  -NewVHDPath "C:\VMs\coolify\coolify.vhdx" -NewVHDSizeBytes 80GB `
  -SwitchName "External"
Set-VM -Name "coolify" -ProcessorCount 4 -AutomaticStartAction Start -AutomaticStartDelay 60
Set-VMFirmware -VMName "coolify" -EnableSecureBoot On -SecureBootTemplate "MicrosoftUEFICertificateAuthority"
# install Ubuntu 24.04 ISO via Hyper-V Manager → Connect → Start, then:
# sudo apt update && sudo apt install -y openssh-server, set static netplan to 192.168.1.50
```

Netplan snippet (VM, `/etc/netplan/01-netcfg.yaml`, then `sudo netplan apply`):

```yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses: [192.168.1.50/24]
      routes: [{to: default, via: 192.168.1.1}]
      nameservers: {addresses: [192.168.1.1, 1.1.1.1]}
```

## 3. Coolify install (VM, 10 min)

```bash
# Ubuntu 24.04 as root / sudo
sudo apt update && sudo apt upgrade -y
curl -fsSL https://cdn.coollabs.io/coolify/install.sh | bash
# verify against https://coolify.io/docs/start-with-self-hosted before running
# first login: http://192.168.1.50:8000 → create admin → connect GitHub (sandraschi, fine-grained, repos: test repos only at first)
# Settings → Auto-update ON (tagged), Backups → local + test restore
```

Lockdown immediately:
- Coolify UI `:8000` = LAN + Tailscale only. Do NOT port-forward 8000. Ever.
- `sudo ufw allow 80,443/tcp && sudo ufw allow from 192.168.1.0/24 to any port 8000 && sudo ufw enable`
- Tailscale in VM: `curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up` → admin UI via `http://coolify.tail-scale:8000`.

## 4. Networking: direct (you have public IP) vs Tailscale vs Tunnel

You have a stable public IP, so use **direct** for public demos. Keep Tailscale as admin + private path.

### A. Direct (recommended for you) — port 80/443 → VM

1. Router → Port Forwarding: `<YOUR_PUBLIC_IP>:80 → 192.168.1.50:80`, `:443 → 192.168.1.50:443` (TCP). No forward for 8000.
2. DNS: `A demo.yourdomain.at → <YOUR_PUBLIC_IP>` (TTL 300 while testing). Apex or subdomain, your call.
3. Coolify → Project → Service → Domains → add `https://demo.yourdomain.at` → enable Let's Encrypt (HTTP-01 uses :80, already forwarded). Wait for green cert.
4. Test: `curl -v https://demo.yourdomain.at/health`, phone on LTE (not wifi), `https://www.ssllabs.com/ssltest/` once.

Pros: real public URL for anyone, no client install. Cons: you own patching + fail2ban. Fine at your traffic.

### B. Tailscale (private friends/family/testing, zero router changes)

- VM + your laptop + Steve's machine on same tailnet. Coolify → Share via `tailscale serve` or Tailscale Funnel for ephemeral `https://*.ts.net`.
- Use for: Coolify admin, pre-public staging, anything with dummy-but-sensitive env.
- No DNS, no certs to manage, CGNAT-proof.

### C. Cloudflare Tunnel (optional later)

- `cloudflared` in VM → outbound-only to Cloudflare, no inbound ports. Good if you lose the stable IP or want CDN/WAF.
- Not needed day 1 with your IP. Keep as fallback.

Rule: admin always via Tailscale/LAN. Public only via :80/:443 app domains. Never expose :8000.

## 5. Fleet Dockerfile pattern (what Coolify builds)

Coolify accepts Nixpacks or Dockerfile. Use Dockerfile — deterministic, matches fleet `uv` standard.

Backend (FastMCP Python, example `demo-app` port 11140 → container 8000):

```dockerfile
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 UV_LINK_MODE=copy
WORKDIR /app
COPY requirements.txt* pyproject.toml* uv.lock* ./
RUN pip install --no-cache-dir uv && \
    (uv sync --frozen --no-dev || pip install --no-cache-dir -r requirements.txt)
COPY src/ ./src/
COPY run_server.py ./
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uv", "run", "python", "run_server.py", "--host", "0.0.0.0", "--port", "8000"]
```

Notes: listen on `0.0.0.0`, read `PORT` from env if you prefer (`int(os.getenv("PORT","8000"))`), `/health` must exist (fleet standard). SQLite/LanceDB → Coolify Volume mounted at `/app/data`, never in container layer.

Frontend (Vite React static, example `demo-app/webapp`):

```dockerfile
FROM node:22-alpine AS build
WORKDIR /webapp
COPY package.json bun.lock* ./
RUN npm ci || npm install
COPY . .
RUN npm run build
FROM caddy:2-alpine
COPY --from=build /webapp/dist /srv
COPY Caddyfile /etc/caddy/Caddyfile
EXPOSE 80
```

```caddyfile
:80 {
  root * /srv
  file_server
  try_files {path} /index.html
}
```

Coolify layout for fullstack: two Resources in one Project + private network (`backend:8000`), frontend proxies `/api/* → http://backend:8000`. Env vars set in Coolify UI, never in git. `.env.example` with NAMES only stays in repo (already fleet rule).

## 6. Deploy clicks (first app, 15 min)

1. Coolify → Project `friends` → Environment `prod` → + Resource → Public Repository → `sandraschi/sandras-com` (branch main, build pack Dockerfile, domain `https://demo.yourdomain.at` for test).
2. Build → Deploy → Logs green → open domain. Static first = proves DNS + cert + forwarding with zero secrets.
3. Next: same Project → + Resource → `sandraschi/demo-app` backend (env `PORT=8000`, volume `demo-data:/app/data`, healthcheck `/health`) + frontend (proxy to backend). Internal URL `http://backend:8000` never leaves Coolify network.
4. Git push to main → auto-redeploy (or manual Deploy). Preview per-PR optional; keep off for low traffic.

## 7. Backups + updates (10 min/month)

- Coolify → Backups → schedule DB/volume dump → local `/backups` + copy to external (USB or Hetzner Storage Box). Test restore once.
- Hyper-V checkpoint before Coolify/host upgrade, delete checkpoint after green week.
- Ubuntu: `sudo apt update && sudo apt upgrade -y` monthly. Coolify: in-UI update button.
- Provider keys: dummy for tests; when real keys needed, scoped + spend caps + rotation log in `operations/session-log/` (no values).

## 8. Troubleshooting

| Symptom | Check |
|---------|-------|
| Domain timeout publicly, works on LAN | Router forward to .50? ISP CGNAT? `curl -4 ifconfig.me` changed? Firewall `ufw status`? |
| Cert stays pending | :80 reachable publicly? DNS A propagated? (`nslookup demo.yourdomain.at 1.1.1.1`). HTTP-01 needs :80. |
| Build fails, runs locally | Coolify uses Linux + Dockerfile — Windows paths, `D:/`, `pwsh` in build scripts break. Keep build Linux-pure. |
| App can't reach Ollama | From VM: `curl http://<GOLIATH_LAN_IP>:11434/api/tags`. Host firewall must allow 11434 from 192.168.1.50. No GPU in VM by design. |
| Coolify UI unreachable | Use Tailscale/LAN IP, not public. `tailscale status`, `docker ps`, `systemctl status coolify`. |
| Disk full | `docker system df`, `docker system prune -a --volumes` (careful with volumes), VHDX compact after. |

## 9. Test plan for you

1. **Today:** VM + Coolify + Tailscale admin. No public yet.
2. **Tomorrow:** `sandras-com` static → `https://demo.yourdomain.at` via direct forward. Phone-on-LTE test.
3. **Next:** `demo-app` backend+frontend with dummy env. Proves fullstack pattern every other fleet repo will copy.
4. **Then:** decide keep/sleep. Sleep = stop Resource (no burn, you own watts). No per-second bill to fear.
