import http.server
import os
import socketserver
import sys
from datetime import datetime
from pathlib import Path

# --- Configuration ---
REPOS_ROOT = "D:/Dev/repos"
MD_OUTPUT = "D:/Dev/repos/mcp-central-docs/projects/fleet.md"
HTML_OUTPUT = "D:/Dev/repos/mcp-central-docs/projects/fleet.html"

# --- Logic ---


def get_category(item):
    name = item.name.lower()

    # Flagship detection (high priority)
    if name.startswith("my") or "core" in name or "sota" in name:
        return "Flagship"

    # MCP Server detection
    has_mcp_indicators = False

    # Check for direct mcp indicators in file contents
    for ext in ["**/*.py", "**/*.ts", "**/*.js", "mcpb.json"]:
        for file_path in item.glob(ext):
            if "node_modules" in str(file_path) or ".venv" in str(file_path):
                continue
            if file_path.name == "mcpb.json":
                has_mcp_indicators = True
                break
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if (
                    "FastMCP" in content
                    or "@mcp.tool" in content
                    or "mcp_server" in content.lower()
                    or "from mcp" in content.lower()
                ):
                    has_mcp_indicators = True
                    break
            except Exception:
                continue
        if has_mcp_indicators:
            break

    if has_mcp_indicators or "mcp" in name:
        return "MCPServer"

    # Junk detection (refined)
    # If it's an MCP server or has flagship vibes, it's NOT junk even without .git
    is_important = has_mcp_indicators or name.startswith("my") or "sota" in name

    junk_patterns = ["junk", "test", "temp", "adn-", "tomfoolery", "mirror", "external"]
    if not is_important:
        if any(p in name for p in junk_patterns) or not (item / ".git").exists():
            return "Junk"

    return "Other"


def get_description(repo_path):
    # Try mcpb.json first
    mcpb = repo_path / "mcpb.json"
    if mcpb.exists():
        try:
            import json

            data = json.loads(mcpb.read_text(encoding="utf-8"))
            if "description" in data:
                return data["description"]
        except Exception:
            pass

    # Try package.json
    pkg = repo_path / "package.json"
    if pkg.exists():
        try:
            import json

            data = json.loads(pkg.read_text(encoding="utf-8"))
            if "description" in data:
                return data["description"]
        except Exception:
            pass

    # Fallback to README
    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        readme_path = repo_path / "readme.md"

    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding="utf-8", errors="ignore")
            # Look for the first paragraph that isn't a header or badge
            lines = content.split("\n")
            desc_lines = []
            found_h1 = False
            for line in lines:
                line = line.strip()
                if not line or line.startswith("[!") or line.startswith("<") or "![" in line:
                    continue
                if line.startswith("# "):
                    found_h1 = True
                    continue
                if found_h1:
                    desc_lines.append(line)
                    if len(desc_lines) >= 2:
                        break

            if desc_lines:
                return " ".join(desc_lines)
        except Exception:
            pass
    return "No description available."


def discover_fleet(root_dir):
    root = Path(root_dir)
    fleet = {"Flagship": [], "MCPServer": [], "Other": [], "Junk": []}

    for item in sorted(root.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            cat = get_category(item)
            info = {
                "name": item.name,
                "path": str(item),
                "description": get_description(item),
                "updated": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d"),
            }
            fleet[cat].append(info)

    return fleet


def generate_markdown(fleet):
    with open(MD_OUTPUT, "w", encoding="utf-8") as f:
        f.write("# Repository Fleet Dashboard\n\n")
        f.write(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for cat in ["Flagship", "MCPServer", "Other", "Junk"]:
            f.write(f"## {cat} ({len(fleet[cat])})\n\n")
            f.write("| Repository | Description | Last Modified |\n")
            f.write("|------------|-------------|---------------|\n")
            for repo in fleet[cat]:
                # Remove backslashes for URL compatibility
                clean_path = repo["path"].replace("\\", "/")
                f.write(
                    f"| [{repo['name']}](file:///{clean_path}) | {repo['description']} | {repo['updated']} |\n"
                )
            f.write("\n")


def generate_html(fleet):
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fleet Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #030712;
            --card-bg: rgba(17, 24, 39, 0.6);
            --accent: #6366f1; /* Indigo */
            --text: #f9fafb;
            --text-dim: #9ca3af;
            --mcp: #0ea5e9; /* Sky */
            --other: #8b5cf6; /* Violet */
            --junk: #4b5563; /* Gray */
            --flagship: #f43f5e; /* Rose */
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-shine: rgba(255, 255, 255, 0.03);
        }}

        body {{
            background: radial-gradient(circle at top left, #111827, #030712);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 2rem;
            line-height: 1.6;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: left;
            margin-bottom: 4rem;
            padding: 3rem;
            border-radius: 24px;
            background: linear-gradient(135deg, var(--glass-shine), transparent);
            border: 1px solid var(--glass-border);
            backdrop-filter: blur(20px);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }}

        h1 {{
            font-weight: 800;
            font-size: 3.5rem;
            margin: 0;
            letter-spacing: -0.04em;
            background: linear-gradient(to right, #ffffff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-top: 1.5rem;
            font-size: 0.85rem;
        }}

        .stat-item {{
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 99px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .dot {{ width: 8px; height: 8px; border-radius: 50%; }}
        .dot.flagship {{ background: var(--flagship); }}
        .dot.mcp {{ background: var(--mcp); }}
        .dot.other {{ background: var(--other); }}
        .dot.junk {{ background: var(--junk); }}

        .search-box {{
            width: 100%;
            padding: 1.25rem 2rem;
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            color: white;
            font-size: 1.1rem;
            margin-bottom: 3rem;
            outline: none;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        .search-box:focus {{
            border-color: var(--accent);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
            gap: 2rem;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .card:hover {{
            transform: translateY(-8px) scale(1.02);
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(31, 41, 55, 0.8);
            box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.6);
        }}

        .card-header {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }}

        .badge {{
            align-self: flex-start;
            font-size: 0.65rem;
            text-transform: uppercase;
            font-weight: 700;
            padding: 0.35rem 0.75rem;
            border-radius: 6px;
            letter-spacing: 0.1em;
        }}

        .badge.MCPServer {{ background: rgba(14, 165, 233, 0.1); color: var(--mcp); border: 1px solid rgba(14, 165, 233, 0.2); }}
        .badge.Other {{ background: rgba(139, 92, 246, 0.1); color: var(--other); border: 1px solid rgba(139, 92, 246, 0.2); }}
        .badge.Junk {{ background: rgba(75, 85, 99, 0.1); color: var(--junk); border: 1px solid rgba(75, 85, 99, 0.2); }}
        .badge.Flagship {{ background: rgba(244, 63, 94, 0.1); color: var(--flagship); border: 1px solid rgba(244, 63, 94, 0.2); }}

        .repo-name {{
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0;
            color: white;
            text-decoration: none;
            letter-spacing: -0.02em;
        }}

        .description {{
            color: var(--text-dim);
            font-size: 0.95rem;
            margin-bottom: 2rem;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.6;
        }}

        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #6b7280;
            font-family: 'JetBrains Mono', monospace;
            padding-top: 1.5rem;
            border-top: 1px solid var(--glass-border);
        }}

        #no-results {{
            text-align: center;
            padding: 8rem;
            grid-column: 1 / -1;
            font-size: 1.5rem;
            color: var(--text-dim);
            display: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Fleet Dashboard</h1>
            <div class="stats">
                <div class="stat-item"><div class="dot flagship"></div> Flagship: {flagship_count}</div>
                <div class="stat-item"><div class="dot mcp"></div> MCP: {mcp_count}</div>
                <div class="stat-item"><div class="dot other"></div> Other: {other_count}</div>
                <div class="stat-item"><div class="dot junk"></div> Junk: {junk_count}</div>
                <div class="stat-item">Total: {total}</div>
            </div>
            <p style="color: #6b7280; font-size: 0.8rem; margin-top: 2rem;">SOTA Snapshot: {last_updated}</p>
        </header>

        <input type="text" class="search-box" placeholder="Search repositories..." id="search">

        <div class="grid" id="grid">
            {cards}
            <div id="no-results">No repositories matching your search.</div>
        </div>
    </div>

    <script>
        const search = document.getElementById('search');
        const cards = document.querySelectorAll('.card');
        const noResults = document.getElementById('no-results');

        search.addEventListener('input', (e) => {{
            const term = e.target.value.toLowerCase();
            let hasVisible = false;

            cards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if(text.includes(term)) {{
                    card.style.display = 'flex';
                    hasVisible = true;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            noResults.style.display = hasVisible ? 'none' : 'block';
        }});
    </script>
</body>
</html>
    """

    cards = []
    all_repos = []
    for cat in ["Flagship", "MCPServer", "Other", "Junk"]:
        for repo in fleet[cat]:
            clean_path = repo["path"].replace("\\", "/")
            card = f"""
            <div class="card" data-category="{cat}">
                <div>
                    <div class="card-header">
                        <a href="file:///{clean_path}" class="repo-name">{repo["name"]}</a>
                        <span class="badge {cat}">{cat}</span>
                    </div>
                    <p class="description">{repo["description"]}</p>
                </div>
                <div class="footer">
                    <span>{repo["updated"]}</span>
                </div>
            </div>
            """
            cards.append(card)
            all_repos.append(repo)

    mcp_count = len(fleet["MCPServer"])
    other_count = len(fleet["Other"])
    junk_count = len(fleet["Junk"])
    flagship_count = len(fleet["Flagship"])
    total = mcp_count + other_count + junk_count + flagship_count

    final_html = html_template.format(
        total=total,
        flagship_count=flagship_count,
        mcp_count=mcp_count,
        other_count=other_count,
        junk_count=junk_count,
        last_updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
        cards="\n".join(cards),
    )

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(final_html)


def serve_dashboard(port=10794):
    os.chdir(Path(HTML_OUTPUT).parent)
    handler = http.server.SimpleHTTPRequestHandler

    # Enable reuse of address to avoid "Address already in use" errors on restart
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(
            f"\n[SOTA] Fleet Dashboard serving at: http://localhost:{port}/{Path(HTML_OUTPUT).name}"
        )
        httpd.serve_forever()


if __name__ == "__main__":
    print(f"Scanning {REPOS_ROOT}...")
    fleet_data = discover_fleet(REPOS_ROOT)

    print("Generating Markdown...")
    generate_markdown(fleet_data)

    print("Generating HTML...")
    generate_html(fleet_data)

    print("Dashboard generation complete.")

    # Start server in a background thread or just run it directly if that's the end of the script
    if "--no-serve" not in sys.argv:
        serve_dashboard()
