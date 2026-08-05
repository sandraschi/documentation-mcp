from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

_tools_root = Path(__file__).resolve().parents[3] / "tools"
if str(_tools_root) not in sys.path:
    sys.path.insert(0, str(_tools_root))
from fastmcp_version import parse_fastmcp_version_from_pyproject


@dataclass(frozen=True)
class StartEntry:
    file_name: str
    file_path: Path
    shortname: str
    category: str
    title: str
    description: str
    port: int | None
    repo_path: str | None
    # Repo URL when known; else owner profile Repositories tab (?tab=repositories).
    github_url: str
    description_source: str = "default"  # fleet_registry | readme_hero | default
    # Declared in fleet-registry.json ("fastmcp") or scan of repo pyproject.toml (fastmcp>=…).
    fastmcp_version: str | None = None


def _repo_root_from_this_file() -> Path:
    # src/docs_mcp/starts_ui/asgi.py -> repo root
    return Path(__file__).resolve().parents[3]


def _starts_dir(repo_root: Path) -> Path:
    return repo_root / "starts"


def _fleet_registry_path(repo_root: Path) -> Path:
    return repo_root / "operations" / "fleet-registry.json"


def _normalize_shortname(file_name: str) -> str:
    name = file_name.lower()
    for suffix in ("-sota-start.bat", "-start.bat"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    if name.endswith(".bat"):
        return name[: -len(".bat")]
    return name


def _load_fleet_registry(repo_root: Path) -> dict[str, dict[str, Any]]:
    path = _fleet_registry_path(repo_root)
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    fleet = data.get("fleet", [])
    index: dict[str, dict[str, Any]] = {}
    for item in fleet:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            continue
        keys = [item["id"]]
        aliases = item.get("aliases")
        if isinstance(aliases, list):
            keys.extend(a for a in aliases if isinstance(a, str) and a.strip())
        for k in keys:
            index[k] = item
    return index


def _best_registry_match(shortname: str, registry: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    # Common mapping patterns:
    # - virtualdj-sota-start.bat -> virtualdj-mcp
    # - advanced-memory-start.bat -> advanced-memory-mcp
    candidates = [
        shortname,
        f"{shortname}-mcp",
        shortname.replace("_", "-"),
        f"{shortname.replace('_', '-')}-mcp",
    ]
    for key in candidates:
        if key in registry:
            return registry[key]
    return None


def _version_tuple(version: str) -> tuple[int, ...]:
    out: list[int] = []
    for part in version.strip().split("."):
        if part.isdigit():
            out.append(int(part))
        else:
            break
    return tuple(out) if out else (0,)


def _is_fastmcp_31_plus(version: str | None) -> bool:
    if not version:
        return False
    return _version_tuple(version) >= (3, 1)


def _resolve_fastmcp_version(shortname: str, meta: dict[str, Any]) -> str | None:
    raw = meta.get("fastmcp")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    repo = _resolve_repo_path_for_readme(shortname, meta)
    if repo is None:
        return None
    return parse_fastmcp_version_from_pyproject(repo / "pyproject.toml")


# Bat shortname -> repo folder under D:/Dev/repos when it does not match {shortname}-mcp
_SHORTNAME_REPO_ALIASES: dict[str, str] = {
    "federation": "mcp-federation-hub",
    "speech": "speech-mcp",
    "reversing": "reversing-mcp",
    "meta_mcp": "meta_mcp",
    "meta-mcp": "meta_mcp",
}

_DEFAULT_DESCRIPTION = "Start script in mcp-central-docs\\starts"

_readme_hero_cache: dict[str, tuple[float, str | None, str | None]] = {}


def _repos_root() -> Path:
    return Path(os.environ.get("MCP_FLEET_REPOS_ROOT", "D:/Dev/repos"))


def _candidate_repo_dirs(shortname: str) -> list[str]:
    """Ordered repo folder names to try on disk."""
    sn = shortname.lower().strip()
    if sn in _SHORTNAME_REPO_ALIASES:
        return [_SHORTNAME_REPO_ALIASES[sn]]
    out: list[str] = []
    for name in (f"{sn}-mcp", sn, sn.replace("_", "-") + "-mcp", sn.replace("_", "-")):
        if name and name not in out:
            out.append(name)
    return out


def _default_github_owner() -> str:
    return (os.environ.get("MCP_FLEET_GITHUB_OWNER") or "sandraschi").strip() or "sandraschi"


def _github_owner_repositories_url() -> str:
    """Used when no specific repo URL is known: opens the owner’s Repositories tab."""
    return f"https://github.com/{_default_github_owner()}?tab=repositories"


def _normalize_github_url(raw: str) -> str:
    u = raw.strip().rstrip("/")
    if u.startswith("https://github.com/") or u.startswith("http://github.com/"):
        return u.replace("http://", "https://", 1)
    if u.startswith("github.com/"):
        return f"https://{u}"
    if "/" in u and not u.startswith("http") and "\n" not in u and " " not in u:
        return f"https://github.com/{u}"
    return u


def _resolve_github_repo_url(meta: dict[str, Any], shortname: str) -> str | None:
    """Specific repo URL from registry or inferred id/repo name; None if unknown."""
    raw = meta.get("github_url")
    if isinstance(raw, str) and raw.strip():
        return _normalize_github_url(raw)
    rid = meta.get("id")
    if isinstance(rid, str) and rid.strip():
        return f"https://github.com/{_default_github_owner()}/{rid.strip()}"
    for dirname in _candidate_repo_dirs(shortname):
        return f"https://github.com/{_default_github_owner()}/{dirname}"
    return None


def _resolve_repo_path_for_readme(shortname: str, registry_meta: dict[str, Any]) -> Path | None:
    """Best-effort local repo path for README hero (may differ from fleet-registry id)."""
    rp = registry_meta.get("repo_path")
    if isinstance(rp, str) and rp.strip():
        p = Path(rp.replace("\\", "/"))
        if p.is_dir():
            return p
    root = _repos_root()
    for dirname in _candidate_repo_dirs(shortname):
        cand = root / dirname
        if cand.is_dir():
            return cand
    return None


def _readme_hero_module():
    path = Path(__file__).resolve().parents[3] / "tools" / "readme_hero.py"
    spec = importlib.util.spec_from_file_location("mcp_central_readme_hero", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"readme_hero not found: {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_rh = _readme_hero_module()
_extract_readme_hero = _rh.extract_readme_hero


def _read_readme_hero_cached(repo_path: Path) -> tuple[str | None, str | None]:
    for name in ("README.md", "Readme.md", "readme.md"):
        readme = repo_path / name
        if not readme.is_file():
            continue
        try:
            mtime = readme.stat().st_mtime
        except OSError:
            return None, None
        key = str(readme.resolve())
        hit = _readme_hero_cache.get(key)
        if hit and hit[0] == mtime:
            return hit[1], hit[2]
        title, blurb = _extract_readme_hero(readme)
        _readme_hero_cache[key] = (mtime, title, blurb)
        return title, blurb
    return None, None


def _enrich_entries_with_readme(entries: list[StartEntry], registry: dict[str, dict[str, Any]]) -> list[StartEntry]:
    """Prefer README.md hero (H1 + opening blurb) for description when the repo is on disk.

    Fleet registry still supplies category, port, and fallback title/description when README has no hero text.
    """
    out: list[StartEntry] = []
    for e in entries:
        meta = _best_registry_match(e.shortname, registry) or {}
        repo = _resolve_repo_path_for_readme(e.shortname, meta)
        if repo is None:
            out.append(e)
            continue
        hero_title, hero_blurb = _read_readme_hero_cached(repo)
        rp_str = str(repo).replace("\\", "/")
        new_title = e.title
        new_desc = e.description
        new_src = e.description_source
        if hero_blurb:
            new_desc = hero_blurb
            new_src = "readme_hero"
        if hero_title and hero_blurb:
            new_title = hero_title
        elif hero_title and (
            e.title == e.shortname or e.title.replace("-", " ").lower() == e.shortname.replace("-", " ").lower()
        ):
            new_title = hero_title
        out.append(
            replace(
                e,
                title=new_title,
                description=new_desc,
                repo_path=e.repo_path or rp_str,
                description_source=new_src,
            )
        )
    return out


def _scan_start_entries(repo_root: Path) -> list[StartEntry]:
    starts = _starts_dir(repo_root)
    if not starts.exists():
        return []

    registry = _load_fleet_registry(repo_root)
    entries: list[StartEntry] = []

    for p in sorted(starts.glob("*.bat")):
        if not p.is_file():
            continue
        shortname = _normalize_shortname(p.name)
        meta = _best_registry_match(shortname, registry) or {}
        fastmcp_ver = _resolve_fastmcp_version(shortname, meta)

        category = str(meta.get("category") or "Other")
        title = str(meta.get("name") or shortname)
        raw_desc = meta.get("description")
        description = str(raw_desc) if raw_desc else _DEFAULT_DESCRIPTION
        port_val = meta.get("port")
        port = int(port_val) if isinstance(port_val, int) else None
        repo_path_val = meta.get("repo_path")
        repo_path = str(repo_path_val) if isinstance(repo_path_val, str) else None
        desc_src = "fleet_registry" if raw_desc else "default"
        repo_github = _resolve_github_repo_url(meta, shortname)
        github_url = repo_github or _github_owner_repositories_url()

        entries.append(
            StartEntry(
                file_name=p.name,
                file_path=p,
                shortname=shortname,
                category=category,
                title=title,
                description=description,
                port=port,
                repo_path=repo_path,
                github_url=github_url,
                description_source=desc_src,
                fastmcp_version=fastmcp_ver,
            )
        )

    return _enrich_entries_with_readme(entries, registry)


def _render_html(entries: list[StartEntry], started_recently: dict[str, float]) -> str:
    categories: dict[str, list[StartEntry]] = {}
    for e in entries:
        categories.setdefault(e.category, []).append(e)

    category_names = sorted(
        categories.keys(),
        key=lambda s: (s.lower() != "infra", s.lower()),
    )

    def esc(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    now = time.time()

    rows: list[str] = []
    for cat in category_names:
        cat_id = "cat-" + "".join(ch if (ch.isalnum() or ch in "-_") else "-" for ch in cat.lower())
        rows.append(f'<div class="cat" data-cat="{esc(cat)}">')
        rows.append(
            "\n".join(
                [
                    f'  <button class="cat-toggle" type="button" onclick="toggleCat(\'{esc(cat_id)}\')">',
                    f'    <span class="chev" id="{esc(cat_id)}-chev">▶</span>',
                    f'    <span class="cat-title">{esc(cat)}</span>',
                    f'    <span class="cat-count" id="{esc(cat_id)}-count"></span>',
                    "  </button>",
                ]
            )
        )
        rows.append(f'  <div class="grid cat-body" id="{esc(cat_id)}" data-collapsed="true">')
        for e in categories[cat]:
            last = started_recently.get(e.file_name)
            last_text = ""
            if isinstance(last, float):
                age = int(max(0.0, now - last))
                if age < 3600:
                    last_text = f"Started {age}s ago"
                else:
                    last_text = f"Started {age // 60}m ago"

            meta_bits: list[str] = []
            if e.port is not None:
                meta_bits.append(f"port {e.port}")
            if e.repo_path:
                meta_bits.append(e.repo_path)
            if e.fastmcp_version:
                meta_bits.append(f"FastMCP {e.fastmcp_version}+")
            meta_line = " · ".join(meta_bits)

            hay_parts = [
                e.title,
                e.description,
                e.shortname,
                e.file_name,
                cat,
                e.github_url,
                e.fastmcp_version or "",
            ]
            if _is_fastmcp_31_plus(e.fastmcp_version):
                hay_parts.append("3.1 fastmcp31 sota")
            hay = " ".join(p for p in hay_parts if p).lower()
            hay = " ".join(hay.split())
            fm31 = "1" if _is_fastmcp_31_plus(e.fastmcp_version) else "0"

            github_btn = (
                f'    <a class="btn btn-ghost" href="{esc(e.github_url)}" '
                'target="_blank" rel="noopener noreferrer">GitHub</a>'
            )

            rows.append(
                "\n".join(
                    [
                        f'<div class="card" data-haystack="{esc(hay)}" data-fm31="{fm31}">',
                        f'  <div class="title">{esc(e.title)}</div>',
                        f'  <div class="desc">{esc(e.description)}</div>',
                        f'  <div class="meta">{esc(meta_line)}</div>' if meta_line else '  <div class="meta"></div>',
                        '  <div class="actions">',
                        f'    <button class="btn" type="button" onclick="launchScript(\'{esc(e.file_name)}\')">Launch</button>',
                        github_btn,
                        f'    <span class="status" id="st-{esc(e.file_name)}">{esc(last_text)}</span>',
                        "  </div>",
                        "</div>",
                    ]
                )
            )
        rows.append("  </div></div>")

    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Fleet Starts Launcher</title>
    <style>
      :root {{
        --bg: #0b1020;
        --panel: rgba(255,255,255,0.06);
        --panel2: rgba(255,255,255,0.08);
        --text: rgba(255,255,255,0.92);
        --muted: rgba(255,255,255,0.65);
        --muted2: rgba(255,255,255,0.45);
        --border: rgba(255,255,255,0.14);
        --accent: #7c3aed;
        --ok: #22c55e;
        --warn: #f59e0b;
        --bad: #ef4444;
      }}
      body {{
        margin: 0;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial,
                     "Noto Sans", "Liberation Sans", sans-serif;
        background: radial-gradient(1200px 700px at 20% 10%, rgba(124,58,237,0.35), transparent 60%),
                    radial-gradient(900px 600px at 85% 20%, rgba(34,197,94,0.20), transparent 55%),
                    radial-gradient(800px 500px at 60% 90%, rgba(59,130,246,0.18), transparent 55%),
                    var(--bg);
        color: var(--text);
      }}
      .wrap {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 28px 20px 60px;
      }}
      .header {{
        display: flex;
        gap: 16px;
        align-items: flex-end;
        justify-content: space-between;
        margin-bottom: 18px;
      }}
      .h1 {{
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.2px;
      }}
      .subtitle {{
        font-size: 13px;
        color: var(--muted);
        margin-top: 6px;
      }}
      .subtitle2 {{
        font-size: 12px;
        color: var(--muted2);
        margin-top: 10px;
        line-height: 1.45;
        max-width: 820px;
      }}
      .toolbar {{
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
        justify-content: flex-end;
      }}
      .search-row {{
        width: 100%;
        margin: 0 0 14px 0;
        padding: 0;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
      }}
      .search-inp {{
        flex: 1 1 280px;
        min-width: 200px;
        background: rgba(255,255,255,0.06);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px 14px;
        font-size: 13px;
        color: var(--text);
        outline: none;
      }}
      .search-inp::placeholder {{
        color: var(--muted2);
      }}
      .search-inp:focus {{
        border-color: rgba(124,58,237,0.65);
        box-shadow: 0 0 0 2px rgba(124,58,237,0.2);
      }}
      .chk {{
        display: inline-flex;
        gap: 8px;
        align-items: center;
        font-size: 12px;
        color: var(--muted);
        cursor: pointer;
        user-select: none;
      }}
      .chk input {{
        accent-color: var(--accent);
      }}
      .pill {{
        background: var(--panel);
        border: 1px solid var(--border);
        padding: 10px 12px;
        border-radius: 999px;
        font-size: 12px;
        color: var(--muted);
        backdrop-filter: blur(10px);
      }}
      .cat {{
        margin-top: 18px;
      }}
      .cat-toggle {{
        width: 100%;
        display: flex;
        gap: 10px;
        align-items: center;
        justify-content: flex-start;
        background: rgba(255,255,255,0.06);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 10px 12px;
        cursor: pointer;
        backdrop-filter: blur(10px);
      }}
      .cat-toggle:hover {{
        background: rgba(255,255,255,0.09);
      }}
      .chev {{
        font-size: 12px;
        color: rgba(255,255,255,0.80);
        width: 18px;
        text-align: center;
      }}
      .cat-title {{
        font-size: 13px;
        font-weight: 800;
        color: rgba(255,255,255,0.88);
        text-transform: uppercase;
        letter-spacing: 0.12em;
      }}
      .cat-count {{
        margin-left: auto;
        font-size: 12px;
        color: var(--muted);
        letter-spacing: 0.02em;
      }}
      .cat-body {{
        margin-top: 10px;
      }}
      .cat-body[data-collapsed="true"] {{
        display: none;
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
      }}
      @media (max-width: 980px) {{
        .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      }}
      @media (max-width: 640px) {{
        .grid {{ grid-template-columns: repeat(1, minmax(0, 1fr)); }}
      }}
      .card {{
        background: linear-gradient(180deg, var(--panel2), var(--panel));
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px 14px 12px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.28);
      }}
      .title {{
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 6px;
      }}
      .desc {{
        font-size: 12px;
        line-height: 1.35;
        color: var(--muted);
        min-height: 32px;
      }}
      .meta {{
        font-size: 11px;
        color: var(--muted2);
        margin-top: 10px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      .actions {{
        display: flex;
        gap: 8px;
        align-items: center;
        margin-top: 12px;
        flex-wrap: wrap;
      }}
      .btn {{
        background: rgba(124,58,237,0.18);
        border: 1px solid rgba(124,58,237,0.55);
        color: rgba(255,255,255,0.92);
        padding: 8px 10px;
        border-radius: 10px;
        font-size: 12px;
        cursor: pointer;
      }}
      a.btn {{
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
      }}
      .btn:hover {{
        background: rgba(124,58,237,0.28);
      }}
      .btn-ghost {{
        background: rgba(255,255,255,0.06);
        border: 1px solid var(--border);
      }}
      .btn-ghost:hover {{
        background: rgba(255,255,255,0.10);
      }}
      .status {{
        font-size: 11px;
        color: var(--muted2);
        margin-left: auto;
      }}
      .toast {{
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0,0,0,0.55);
        border: 1px solid rgba(255,255,255,0.15);
        color: rgba(255,255,255,0.90);
        padding: 10px 12px;
        border-radius: 12px;
        font-size: 12px;
        display: none;
        backdrop-filter: blur(10px);
        max-width: 90vw;
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="header">
        <div>
          <div class="h1">Fleet Starts Launcher</div>
          <div class="subtitle">Runs entries from <code>mcp-central-docs\\starts</code> (bat launchers).</div>
          <div class="subtitle2">
            Launchers map to <code>operations/fleet-registry.json</code>
            (category, port, path, <code>aliases</code>, optional <code>fastmcp</code>).
            FastMCP version: registry field or scan of <code>pyproject.toml</code>.
            Card copy comes from each repo's <code>README.md</code> hero when present;
            otherwise the registry description is shown.
          </div>
        </div>
        <div class="toolbar">
          <div class="pill" id="countPill">Loading…</div>
          <button class="btn btn-ghost" onclick="setAllCats(true)">Expand all</button>
          <button class="btn btn-ghost" onclick="setAllCats(false)">Collapse all</button>
          <button class="btn btn-ghost" onclick="location.reload()">Refresh</button>
        </div>
      </div>
      <div class="search-row">
        <input type="search" id="searchQ" class="search-inp"
               placeholder="Search title, repo, category… (type 3.1 for FastMCP 3.1+ tier)"
               autocomplete="off" />
        <label class="chk" title="Show only repos with FastMCP 3.1+ (registry or pyproject)">
          <input type="checkbox" id="filterFm31" />
          FastMCP 3.1+ only
        </label>
      </div>
      {"".join(rows)}
    </div>
    <div class="toast" id="toast"></div>
    <script>
      function toast(msg) {{
        var t = document.getElementById("toast");
        t.textContent = msg;
        t.style.display = "block";
        clearTimeout(window.__toastTimer);
        window.__toastTimer = setTimeout(function() {{
          t.style.display = "none";
        }}, 2400);
      }}

      function setStatus(fileName, msg) {{
        var el = document.getElementById("st-" + fileName);
        if (el) el.textContent = msg;
      }}

      function setCatCollapsed(catId, collapsed) {{
        var body = document.getElementById(catId);
        var chev = document.getElementById(catId + "-chev");
        if (!body) return;
        body.dataset.collapsed = collapsed ? "true" : "false";
        if (chev) chev.textContent = collapsed ? "▶" : "▼";
      }}

      function toggleCat(catId) {{
        var body = document.getElementById(catId);
        if (!body) return;
        var collapsed = (body.dataset.collapsed === "true");
        setCatCollapsed(catId, !collapsed);
      }}

      function setAllCats(expand) {{
        var bodies = document.querySelectorAll(".cat-body");
        for (var i = 0; i < bodies.length; i++) {{
          var id = bodies[i].id;
          setCatCollapsed(id, !expand);
        }}
      }}

      async function launchScript(fileName) {{
        setStatus(fileName, "Launching…");
        try {{
          var r = await fetch("/api/launch", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ file_name: fileName }})
          }});
          var data = await r.json();
          if (!r.ok || !data.success) {{
            setStatus(fileName, "Launch failed");
            toast("Launch failed: " + (data.error || "unknown error"));
            return;
          }}
          setStatus(fileName, "Started");
          toast("Started " + fileName);
        }} catch (e) {{
          setStatus(fileName, "Launch error");
          toast("Launch error: " + String(e));
        }}
      }}

      function applyFilters() {{
        var q = (document.getElementById("searchQ").value || "").trim().toLowerCase();
        var fm31only = document.getElementById("filterFm31").checked;
        var cards = document.querySelectorAll(".card");
        var visible = 0;
        for (var i = 0; i < cards.length; i++) {{
          var c = cards[i];
          var hay = (c.getAttribute("data-haystack") || "").toLowerCase();
          var okQ = !q || hay.indexOf(q) !== -1;
          var okFm = !fm31only || c.getAttribute("data-fm31") === "1";
          var show = okQ && okFm;
          c.style.display = show ? "" : "none";
          if (show) visible++;
        }}
        var cats = document.querySelectorAll(".cat");
        for (var j = 0; j < cats.length; j++) {{
          var cat = cats[j];
          var body = cat.querySelector(".cat-body");
          if (!body) continue;
          var cc = body.querySelectorAll(".card");
          var any = false;
          for (var k = 0; k < cc.length; k++) {{
            if (cc[k].style.display !== "none") {{ any = true; break; }}
          }}
          cat.style.display = any ? "" : "none";
          var countEl = document.getElementById(body.id + "-count");
          if (countEl) {{
            var vis = 0;
            for (var m = 0; m < cc.length; m++) {{
              if (cc[m].style.display !== "none") vis++;
            }}
            countEl.textContent = vis + " shown";
          }}
        }}
        var total = window.__fleetStartsTotal || document.querySelectorAll(".card").length;
        var pill = document.getElementById("countPill");
        if (pill) pill.textContent = visible + " shown · " + total + " total";
      }}

      (function initCount() {{
        var total = document.querySelectorAll(".card").length;
        window.__fleetStartsTotal = total;
        var pill = document.getElementById("countPill");
        if (pill) pill.textContent = total + " start scripts";

        var cats = document.querySelectorAll(".cat-body");
        for (var i = 0; i < cats.length; i++) {{
          var catBody = cats[i];
          setCatCollapsed(catBody.id, true);
          var countEl = document.getElementById(catBody.id + "-count");
          if (countEl) {{
            var n = catBody.querySelectorAll(".card").length;
            countEl.textContent = n + " scripts";
          }}
        }}

        var sq = document.getElementById("searchQ");
        var f31 = document.getElementById("filterFm31");
        if (sq) sq.addEventListener("input", applyFilters);
        if (f31) f31.addEventListener("change", applyFilters);
        applyFilters();
      }})();
    </script>
  </body>
</html>
"""


def _safe_bat_name(file_name: str) -> str:
    if not file_name:
        raise ValueError("Missing file_name")
    if "/" in file_name or "\\" in file_name:
        raise ValueError("file_name must be a base name (no path separators)")
    if not file_name.lower().endswith(".bat"):
        raise ValueError("Only .bat entries are allowed")
    return file_name


def _windows_creationflags_new_console() -> int:
    if os.name != "nt":
        return 0
    return getattr(subprocess, "CREATE_NEW_CONSOLE", 0)


def create_app() -> FastAPI:
    repo_root = _repo_root_from_this_file()
    starts_dir = _starts_dir(repo_root)
    started_recently: dict[str, float] = {}

    app = FastAPI(title="Fleet Starts Launcher", version="1.0.0")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> HTMLResponse:
        entries = _scan_start_entries(repo_root)
        html = _render_html(entries, started_recently)
        return HTMLResponse(content=html)

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {"success": True, "status": "ok"}

    @app.get("/api/starts")
    async def list_starts() -> JSONResponse:
        entries = _scan_start_entries(repo_root)
        result = [
            {
                "file_name": e.file_name,
                "shortname": e.shortname,
                "category": e.category,
                "title": e.title,
                "description": e.description,
                "port": e.port,
                "repo_path": e.repo_path,
                "description_source": e.description_source,
                "github_url": e.github_url,
                "fastmcp_version": e.fastmcp_version,
                "fastmcp_31_plus": _is_fastmcp_31_plus(e.fastmcp_version),
            }
            for e in entries
        ]
        return JSONResponse({"success": True, "result": result})

    @app.post("/api/launch")
    async def launch(payload: dict[str, Any]) -> JSONResponse:
        try:
            file_name = _safe_bat_name(str(payload.get("file_name") or ""))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

        target = starts_dir / file_name
        if not target.exists():
            raise HTTPException(status_code=404, detail="Start script not found")

        # Resolve symlinks: many entries in starts/ are .bat symlinks to repo
        # webapp/web_sota/start.bat. Running cmd on the symlink path leaves %~dp0
        # as starts\, so "start.ps1" is missing and the window exits instantly.
        resolved = target.resolve()
        try:
            # S607: Use absolute path for cmd.exe to prevent path injection
            # S603: input 'resolved' is from the local 'starts' dir, which is audited
            subprocess.Popen(
                ["C:\\Windows\\System32\\cmd.exe", "/c", str(resolved)],
                cwd=str(resolved.parent),
                creationflags=_windows_creationflags_new_console(),
            )
            started_recently[file_name] = time.time()
        except Exception as e:
            return JSONResponse(
                {
                    "success": False,
                    "error": f"Failed to launch: {e}",
                    "recovery_options": [
                        "Run the .bat directly from Explorer",
                        "Verify the repo exists and the target start.ps1 exists",
                    ],
                },
                status_code=500,
            )

        return JSONResponse({"success": True, "result": {"started": file_name}})

    return app


app = create_app()
