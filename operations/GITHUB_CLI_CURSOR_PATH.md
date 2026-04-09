# GITHUB_CLI_CURSOR_PATH.md

Manual fallback for `gh` when the system `PATH` is broken or restricted.

## Hardened Solution (v0.4.0+)

As of **`git-github-mcp` v0.4.0**, the server **automatically discovers** the GitHub CLI in common Windows paths (`C:\Program Files\GitHub CLI`, `scoop`, `winget`). No manual `PATH` configuration is required for tool use.

## Manual fallback

If you are using `gh` directly in the terminal and it fails, call the binary explicitly with the fully qualified path:

```powershell
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

---

## git-github-mcp / `github_ops` and **repository topics**

The fleet **git-github** MCP server exposes **`github_ops`** with operations such as `repo_list`, `repo_create`, issues, PRs, releases, workflows, labels, secrets, etc. It does **not** currently expose a dedicated **`repo_edit`** / **`set_topics`** action in the tool schema (see MCP descriptor: topics are not listed under REPOS).

**Workaround:** use `gh` (full path if needed):

```powershell
gh repo edit OWNER/REPO --add-topic topic-one --add-topic topic-two
```

Or GitHub REST API: `PATCH /repos/{owner}/{repo}` with body `{"names":["topic1","topic2"]}` (replaces **all** topic names — merge client-side first).

**Enhancement (server maintainers):** add `repo_edit` with flags for `--add-topic` / `--remove-topic` mapped to `gh repo edit` or the Repositories API.
