import json
import os
import tomllib

REPOS_DIR = r"D:\Dev\repos"
EXISTING_CONFIG_PATH = r"C:\Users\sandr\.gemini\antigravity\mcp_config.json"
OUTPUT_PATH = r"D:\Dev\repos\mcp-central-docs\operations\MASTER_MCP_CONFIG.json"


def get_existing_config():
    if os.path.exists(EXISTING_CONFIG_PATH):
        try:
            with open(EXISTING_CONFIG_PATH, encoding="utf-8") as f:
                return json.load(f).get("mcpServers", {})
        except Exception as e:
            print(f"Error loading existing config: {e}")
    return {}


def scan_repos():
    master_config = {}

    # Preload existing envs to carry them over
    existing_servers = get_existing_config()
    existing_envs_by_dir = {}
    for _name, s_config in existing_servers.items():
        if "args" in s_config and "--directory" in s_config["args"]:
            idx = s_config["args"].index("--directory")
            if idx + 1 < len(s_config["args"]):
                dir_path = s_config["args"][idx + 1].replace("\\", "/")
                existing_envs_by_dir[dir_path] = s_config.get("env", {})

    # Loop over all repos
    for entry in os.scandir(REPOS_DIR):
        if not entry.is_dir():
            continue

        repo_name = entry.name
        repo_path = entry.path.replace("\\", "/")

        # Check for Python MCP (pyproject.toml)
        pyproject_path = os.path.join(entry.path, "pyproject.toml")
        package_json_path = os.path.join(entry.path, "package.json")

        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)

                deps = data.get("project", {}).get("dependencies", [])
                is_mcp = any("fastmcp" in d.lower() or "mcp" in d.lower() for d in deps)

                if not is_mcp and "mcp" not in repo_name.lower():
                    continue

                scripts = data.get("project", {}).get("scripts", {})
                if not scripts and not is_mcp:
                    continue

                # Determine the correct script
                script_name = None
                for key in scripts:
                    if "server" in key.lower() or "mcp" in key.lower():
                        script_name = key
                        break
                if not script_name and scripts:
                    script_name = next(iter(scripts.keys()))

                if not script_name:
                    script_name = repo_name  # Fallback

                env = existing_envs_by_dir.get(repo_path, {})
                if "PYTHONPATH" not in env and os.path.exists(os.path.join(entry.path, "src")):
                    env["PYTHONPATH"] = f"{repo_path}/src"
                if "PYTHONUNBUFFERED" not in env:
                    env["PYTHONUNBUFFERED"] = "1"

                server_key = repo_name
                master_config[server_key] = {
                    "command": "uv",
                    "args": ["--directory", repo_path, "run", script_name],
                    "env": env,
                    "disabled": True,  # Default to disabled to let workflow choose
                }

                # Special cases overrides
                if repo_name == "advanced-memory-mcp":
                    master_config[server_key]["args"] = [
                        "--directory",
                        repo_path,
                        "run",
                        "advanced-memory",
                        "mcp",
                    ]
                elif repo_name == "pywinauto-mcp":
                    master_config[server_key]["args"] = [
                        "--directory",
                        repo_path,
                        "run",
                        "python",
                        "-m",
                        "pywinauto_mcp.main",
                        "--stdio",
                    ]
                elif repo_name == "openclaw-molt-mcp":
                    master_config[server_key]["args"] = [
                        "--directory",
                        repo_path,
                        "run",
                        "python",
                        "-m",
                        "openclaw_molt_mcp",
                    ]

            except Exception as e:
                print(f"Error parsing Python repo {repo_name}: {e}")

        # Check for Node.js MCP (package.json)
        elif os.path.exists(package_json_path):
            try:
                with open(package_json_path, encoding="utf-8") as f:
                    data = json.load(f)

                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                all_deps = list(deps.keys()) + list(dev_deps.keys())

                is_mcp = any("@modelcontextprotocol" in d for d in all_deps)
                if not is_mcp and "mcp" not in repo_name.lower():
                    continue

                # Usually node based MCPs run via node build/index.js or dist/index.js
                index_path = f"{repo_path}/dist/index.js"
                if not os.path.exists(index_path.replace("/", "\\")):
                    index_path = f"{repo_path}/build/index.js"

                server_key = repo_name

                master_config[server_key] = {
                    "command": "node",
                    "args": [index_path],
                    "env": existing_envs_by_dir.get(repo_path, {}),
                    "disabled": True,
                }
            except Exception as e:
                print(f"Error parsing Node repo {repo_name}: {e}")

    # Merge existing ones not in repos (like brightdata, firebase, mcp-playwright)
    for name, config in existing_servers.items():
        if name not in master_config and "npx" in config.get("command", ""):
            config["disabled"] = True  # disable by default
            master_config[name] = config

    final_json = {"mcpServers": master_config}

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=2)

    print(f"Generated master config at {OUTPUT_PATH} with {len(master_config)} servers.")


if __name__ == "__main__":
    scan_repos()
