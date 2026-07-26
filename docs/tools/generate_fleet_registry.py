"""Rebuild operations/fleet-registry.json from webapp-registry + starts + existing fleet.

Run:
  uv run python tools/generate_fleet_registry.py
  just fleet-registry
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from readme_hero import read_readme_from_repo
from sync_fleet_fastmcp import apply_fastmcp_to_fleet_items

REPO_ROOT = Path(__file__).resolve().parents[1]
OPS = REPO_ROOT / "operations"
STARTS = REPO_ROOT / "starts"

# Repo folder name (under D:/Dev/repos) -> canonical fleet id (when id != folder name)
REPO_BASENAME_TO_ID: dict[str, str] = {
    "mcp-central-docs": "docs-mcp",
}

# Bat shortname -> fleet id (when {shortname}-mcp is wrong)
SHORTNAME_TO_ID: dict[str, str] = {
    "federation": "mcp-federation-hub",
    "mcp-central-docs": "docs-mcp",
    "vienna-life": "vienna-life-assistant",
    "meta-mcp": "meta_mcp",
}

# Fleet id -> extra registry index keys
ID_EXTRA_ALIASES: dict[str, list[str]] = {
    "docs-mcp": ["mcp-central-docs"],
    "mcp-federation-hub": ["federation"],
    "vienna-life-assistant": ["vienna-life"],
}


def _normalize_shortname(file_name: str) -> str:
    name = file_name.lower()
    for suffix in ("-sota-start.bat", "-start.bat"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    if name.endswith(".bat"):
        return name[: -len(".bat")]
    return name


def _normalize_repo_path(path: str) -> str:
    """Group webapp rows by repo root (strip trailing /web, /webapp, /web_sota)."""
    p = path.replace("\\", "/").rstrip("/")
    for suffix in ("/web", "/webapp", "/web_sota"):
        while p.lower().endswith(suffix):
            p = str(Path(p).parent).replace("\\", "/")
    return p


def _repo_norm(path: str) -> str:
    return _normalize_repo_path(path).lower()


def _basename(path: str) -> str:
    return Path(_normalize_repo_path(path)).name


def _canonical_id_for_repo(repo_path: str, ids: list[str]) -> str:
    b = _basename(repo_path)
    if b in REPO_BASENAME_TO_ID:
        return REPO_BASENAME_TO_ID[b]
    if b in ids:
        return b
    # Repo folder name is usually the canonical fleet id (discord-mcp, not discord-mcp-backend)
    if b.endswith("-mcp") or b in (
        "meta_mcp",
        "robofang",
        "myai",
        "teleconference-mcp",
        "games-app",
        "dark-app-factory",
        "mcp-federation-hub",
        "mcp-central-docs",
    ):
        return b
    plain = [i for i in ids if i.endswith("-mcp") and "-backend" not in i and "-frontend" not in i]
    if plain:
        return sorted(plain, key=len)[0]
    no_bf = [i for i in ids if "-backend" not in i and "-frontend" not in i]
    if len(no_bf) == 1:
        return no_bf[0]
    return sorted(ids, key=len)[0]


def _infer_category(fid: str, label: str) -> str:
    t = (fid + " " + label).lower()
    if any(x in t for x in ("transit", "vienna", "wiener", "gtfs")):
        return "Transit"
    if any(x in t for x in ("robot", "yahboom", "dreame", "bumi")):
        return "Robotics"
    if any(
        x in t
        for x in (
            "blender",
            "gimp",
            "inkscape",
            "davinci",
            "resolume",
            "vroid",
            "avatar",
            "unity",
            "resonite",
            "worldlabs",
            "audiotool",
        )
    ):
        return "Creative"
    if any(
        x in t
        for x in ("obs", "reaper", "plex", "handbrake", "virtualdj", "songgeneration", "suno")
    ):
        return "Media"
    if any(x in t for x in ("discord", "email", "tailscale", "readly")):
        return "Comms"
    if any(x in t for x in ("memory", "obsidian", "notion", "docs", "calibre", "llm-txt", "arxiv")):
        return "Knowledge"
    if any(x in t for x in ("local-llm", "ocr", "speech", "myai", "sakana", "kyutai")):
        return "AI"
    if any(
        x in t
        for x in (
            "docker",
            "rustdesk",
            "virtualization",
            "windows-operations",
            "system-admin",
            "backup",
            "monitoring",
            "filesystem",
            "netatmo",
        )
    ):
        return "Infra"
    if any(x in t for x in ("ring", "nest", "devices", "home-assistant", "osc")):
        return "Control"
    if any(x in t for x in ("federation", "meta_mcp", "robofang", "games-app", "moltbot")):
        return "Command"
    return "Dev"


def main() -> None:
    fleet_by_id: dict[str, dict[str, object]] = {}

    existing_path = OPS / "fleet-registry.json"
    if existing_path.exists():
        old = json.loads(existing_path.read_text(encoding="utf-8"))
        for item in old.get("fleet", []):
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                fleet_by_id[item["id"]] = dict(item)

    webapps = json.loads((OPS / "webapp-registry.json").read_text(encoding="utf-8")).get(
        "webapps", []
    )
    by_repo: dict[str, list[dict[str, object]]] = defaultdict(list)
    for w in webapps:
        rp = w.get("repo_path")
        if isinstance(rp, str):
            by_repo[_repo_norm(rp)].append(w)

    def _prune_transport_suffix_ids() -> None:
        """Drop *-backend / *-frontend rows when the canonical *-mcp id exists."""
        for fid in list(fleet_by_id.keys()):
            for suffix in ("-backend", "-frontend"):
                if fid.endswith(suffix):
                    base = fid[: -len(suffix)]
                    if base in fleet_by_id:
                        del fleet_by_id[fid]
                    break

    for _rk, rows in by_repo.items():
        sample = str(rows[0].get("repo_path", ""))
        norm = _normalize_repo_path(sample)
        ids = [str(r["id"]) for r in rows if isinstance(r.get("id"), str)]
        cid = _canonical_id_for_repo(norm, ids)
        labels = [str(r.get("label", "")) for r in rows]
        label = next((L for L in labels if L), cid)
        ports = [int(r["port"]) for r in rows if isinstance(r.get("port"), int)]
        port = min(ports) if ports else 0
        desc = f"Fleet webapp / MCP ({label.split('—')[0].strip()})."
        cat = _infer_category(cid, label)
        repo_folder = _basename(norm)
        entry = {
            "id": cid,
            "name": (label[:120] if label else cid),
            "description": desc,
            "port": port,
            "repo_path": f"D:/Dev/repos/{repo_folder}",
            "category": cat,
        }
        if cid in fleet_by_id:
            prev = dict(fleet_by_id[cid])
            # Webapp wins for paths/ports; README enrichment pass fills description/name later
            merged = {**prev, **entry}
            if prev.get("icon"):
                merged["icon"] = prev["icon"]
            if prev.get("priority"):
                merged["priority"] = prev["priority"]
            fleet_by_id[cid] = merged
        else:
            fleet_by_id[cid] = entry

    _prune_transport_suffix_ids()

    # Every starts/*.bat must resolve
    for p in sorted(STARTS.glob("*.bat")):
        sn = _normalize_shortname(p.name)
        fid = SHORTNAME_TO_ID.get(sn)
        if fid is None:
            cand = f"{sn.replace('_', '-')}-mcp"
            if cand in fleet_by_id:
                fid = cand
            elif sn in fleet_by_id:
                fid = sn
            else:
                fid = f"{sn.replace('_', '-')}-mcp"
        if fid not in fleet_by_id:
            repo_folder = fid
            if repo_folder == "meta-mcp":
                repo_folder = "meta_mcp"
            fleet_by_id[fid] = {
                "id": fid,
                "name": fid.replace("-", " ").replace("_", " ").title()[:80],
                "description": f"MCP fleet member ({fid}).",
                "port": 0,
                "repo_path": f"D:/Dev/repos/{repo_folder}",
                "category": _infer_category(fid, fid),
            }

    for fid, extras in ID_EXTRA_ALIASES.items():
        if fid not in fleet_by_id:
            continue
        cur = dict(fleet_by_id[fid])
        aliases = (
            [str(x) for x in cur.get("aliases", [])] if isinstance(cur.get("aliases"), list) else []
        )
        for e in extras:
            if e not in aliases:
                aliases.append(e)
        cur["aliases"] = aliases
        fleet_by_id[fid] = cur

    if "speech-mcp" in fleet_by_id:
        sp = dict(fleet_by_id["speech-mcp"])
        sp["repo_path"] = "D:/Dev/repos/speech-mcp"
        fleet_by_id["speech-mcp"] = sp

    def _enrich_from_readme(entry: dict[str, object]) -> dict[str, object]:
        """Prefer README.md hero (H1 + opening blurb) when repo exists on disk."""
        rp = entry.get("repo_path")
        if not isinstance(rp, str) or not rp.strip():
            return entry
        root = Path(rp.replace("\\", "/"))
        if not root.is_dir():
            return entry
        title, blurb = read_readme_from_repo(root)
        out = dict(entry)
        if blurb:
            out["description"] = blurb
        if title:
            out["name"] = str(title)[:120]
        return out

    fleet_by_id = {fid: _enrich_from_readme(dict(e)) for fid, e in fleet_by_id.items()}

    fleet_list = sorted(
        fleet_by_id.values(), key=lambda x: (str(x.get("category", "")), str(x.get("id", "")))
    )
    fleet_list, fm_stats = apply_fastmcp_to_fleet_items(fleet_list)
    print(
        "fastmcp scan: "
        f"set={fm_stats['found']}, "
        f"no_repo={fm_stats['missing_repo']}, "
        f"no_pyproject={fm_stats['no_pyproject']}, "
        f"no_fastmcp_dep={fm_stats['no_fastmcp']}"
    )
    existing_path.write_text(
        json.dumps({"fleet": fleet_list}, indent=4, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(fleet_list)} fleet entries to {existing_path}")


if __name__ == "__main__":
    main()
