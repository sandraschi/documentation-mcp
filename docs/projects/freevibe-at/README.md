# freevibe.at / paidvibe.at – Coming Soon Landing

Internal testing landing page for freevibe.at and paidvibe.at on server **213.47.34.131**.

## Contents

- `index.html` – Simple "Coming soon" page (minimal)
- `vibe/www/` – **meta_mcp landing page builder** output: full "Coming Soon" site (hero, features, nav, styles). Use this for the live deploy if you want the premium look.
- `nginx.conf` – Nginx server block for both domains

## Preview locally

- **Quick look-see:** run **`start-preview.bat`** or **`start-preview.ps1`** (serves premium `vibe\www` and opens http://127.0.0.1:8765/).
- **Simple page:** open `index.html` in a browser, or serve the repo root on port 8765.
- **Premium page (manual):** `python -m http.server 8765 --directory "vibe\www"` then open **http://127.0.0.1:8765/**.

To regenerate the premium landing with **meta_mcp**: from `d:\Dev\repos\meta_mcp`, use the MCP tool `generate_landing_page` (or the scaffolding API) with `project_name='Vibe'`, `target_path=r'd:\Dev\repos\freevibe-at'`, and your copy (hero_title, features, etc.).

## Deploy on 213.47.34.131

1. Create document root and copy files. For the **premium** landing, copy the contents of `vibe/www/`; for the simple one, copy `index.html` only:
   ```powershell
   # On the server (Linux):
   sudo mkdir -p /var/www/coming-soon
   # Premium: copy vibe/www/* into /var/www/coming-soon
   # Simple:  sudo cp index.html /var/www/coming-soon/
   ```

2. Install Nginx config:
   - Copy `nginx.conf` into a new site file, e.g. `/etc/nginx/sites-available/freevibe-at`
   - Enable: `sudo ln -s /etc/nginx/sites-available/freevibe-at /etc/nginx/sites-enabled/`
   - Test: `sudo nginx -t`
   - Reload: `sudo systemctl reload nginx`

3. DNS: Ensure freevibe.at and paidvibe.at (and www) have A records pointing to **213.47.34.131** (via nic.at or your DNS provider).

## Last updated

2026-02-10
