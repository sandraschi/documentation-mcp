---
title: "Release Standard (formerly Release Tiers)"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-10-06
---
# Release Standard

**Status:** Active (2026-10-06). **Supersedes** the T1/T2/T3 tier model of 2026-07-11 and the
"Infrastructure MCP Tier" exception in `tauri_nsis_building.md` for any repo with a webapp.
**Gate:** `scripts/check-release-gate.ps1` (see [The gate](#the-gate)).
**References:** [MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md),
[tauri_nsis_building.md](./rules/tauri_nsis_building.md),
[cua_nsis_smoke_testing.md](./rules/cua_nsis_smoke_testing.md),
[README_STRUCTURE.md](./README_STRUCTURE.md).

---

## The rule

There are no tiers. A repo is in one of two classes, decided by whether it has a webapp
(a `package.json` under `webapp/`, `web_sota/`, `webapp/frontend/`, `frontend/` or `web/`).

| Class | Every published release MUST carry | Default install for users |
|-------|------------------------------------|---------------------------|
| **A - has a webapp** | `{repo}-{version}.mcpb` **and** `{repo}-{version}-setup.exe` (Tauri NSIS) | The NSIS installer |
| **B - no webapp** (headless / infrastructure) | `{repo}-{version}.mcpb` | The `.mcpb` |

- "Published release" means any non-draft GitHub release, pre-releases included. A tag with no
  assets is not a release, it is a bookmark. Do not create the GitHub release before both
  artifacts exist.
- Both artifacts are **mandatory, not optional and not "when we get round to it"**. A repo that
  cannot yet produce its installer does not get a release.
- The NSIS installer is the default for end users because it installs the whole product: webapp
  plus embedded backend, one download, one shortcut. A `.mcpb` registers the MCP server in
  Claude Desktop only; it does **not** install the webapp.
- Installers are built locally and uploaded with `gh release upload` (no private CI). They are
  unsigned: README and INSTALL must say so and mention the SmartScreen "More info > Run anyway" step.

## Artifact contract

| Item | Requirement |
|------|-------------|
| Names | `{repo}-{version}.mcpb`, `{repo}-{version}-setup.exe`. Rename the Tauri output (`Product_1.2.3_x64-setup.exe`) and the manifest-named `.mcpb` on upload so users can predict them. |
| Version | `{version}` equals the Git tag without the leading `v`, `tauri.conf.json` `version`, and `mcpb/manifest.json` `version`. |
| Tag | The release tag points at the commit the artifacts were built from, built from a clean tree. |
| Sizes | `.mcpb` > 10 KB. Installer >= 5 MB (a runt installer means the embedded backend is missing). |
| Embedded backend | `bundle.resources`, not `externalBin`; never bundle `.env` (`.env.example` only). |
| Operator port | A dedicated claimed port (`{repo}-native`), never the dev ports. |
| Transport | Dual transport on the sidecar: HTTP by default, `--stdio` / `MCP_TRANSPORT=stdio` for IDEs. Stdout carries JSON-RPC only; logs go to stderr. Stateful servers also proxy to a running daemon ([SOTA_REQUIREMENTS.md](./SOTA_REQUIREMENTS.md) 2.3). |

## Release prerequisites (all of them, every release)

1. **Hooks:** `.pre-commit-config.yaml` runs `ruff` and `ruff-format`; Class A repos also run Biome
   (`biome-web`, see `templates/pre-commit-config.yaml.template`).
2. **Build gates pass** (`just build-native`): ruff, tsc, biome, frozen-backend HTTP smoke, frozen-backend
   **stdio MCP handshake** (`scripts/smoke_stdio.py`: `initialize` + `tools/list`, fails on any
   non-JSON-RPC stdout).
3. **MCPB gates pass** (`just mcpb-pack`): import isolation, AST, pollution, launch check; handshake
   verified from a clean unpack.
4. **CUA smoke test passes on the exact installer being shipped** (Class A). Below.
5. **Docs:** README leads with the installer download; `INSTALL.md` and `docs/DEVELOPMENT.md` exist;
   build recipes (`just ...`) appear only in `docs/DEVELOPMENT.md`. See [README_STRUCTURE.md](./README_STRUCTURE.md).
6. **`BUILD_LOG.md`** has an entry for this build (problems found, fixes).

### CUA smoke test is a release prerequisite

`just cua-nsis-test` installs the real installer, launches it, walks the UI, proves the backend
received the requests, and uninstalls. It drives a real desktop session, so it **cannot run in CI**;
it is run by a person (or agent) at an interactive Windows session before the release is created.

Because this test has produced false passes before (missing `pywinauto`; an OCR nav-walk that passed
while every fetch failed), a log line or a screenshot folder is **not evidence**. The run must write
`cua-reports/cua-result.json` (template `CUA_SMOKE_VERSION >= 15`) and the gate accepts it only if:

| Field | Required |
|-------|----------|
| `all_passed` | `true` |
| `pywinauto` | `true` (GUI phases really ran) |
| `backend_receipt_proof` | `true` (the backend saw the requests the UI claims to have made) |
| `installer_sha256` | equals the SHA-256 of the `-setup.exe` that will be / was uploaded |
| `finished_at` | present (ISO-8601 UTC) |

The SHA-256 binding means any rebuild invalidates the previous CUA result: change one byte of the
installer and the test must be run again. A repo whose CUA result is missing, failed, or for a
different installer does not get a release.

## Procedure

```powershell
# 1. clean tree, versions aligned (tag == tauri.conf.json == mcpb/manifest.json)
# 2. build installer (full gate chain, embedded backend, stdio+HTTP smoke)
just build-native
# 3. build the bundle (isolation, launch, handshake)
just mcpb-pack
# 4. CUA smoke on the installer you are about to ship; writes cua-reports/cua-result.json
just cua-nsis-test
# 5. rename to the contract names, verify BEFORE publishing
pwsh mcp-central-docs/scripts/check-release-gate.ps1 -Repo . -Local -Version 1.2.3
# 6. tag at HEAD, create the release with both assets in one command
gh release create v1.2.3 dist/{repo}-1.2.3.mcpb dist/{repo}-1.2.3-setup.exe --title "..." --notes "..."
# 7. verify what is actually published
pwsh mcp-central-docs/scripts/check-release-gate.ps1 -Repo . -Version 1.2.3
```

Dev pushes do not need installers. Only releases do. Heavy builds can run in the background
([async-worktree-agent.md](../patterns/async-worktree-agent.md)).

## The gate

`scripts/check-release-gate.ps1` fails (exit 1) unless every applicable check passes:

| Check | Applies to |
|-------|-----------|
| Class detection (webapp or not) | all |
| Release exists, is not a draft, and its assets include `{repo}-{version}.mcpb` (size > 10 KB) | all |
| Release includes `{repo}-{version}-setup.exe` (size >= 5 MB) | Class A |
| Tag commit equals `HEAD` and the working tree is clean | all (published mode) |
| `cua-reports/cua-result.json` passes every field above and its `installer_sha256` matches the installer | Class A |
| `.pre-commit-config.yaml` contains `ruff`, and `biome` for Class A | all |
| README has no `just mcpb-pack` / `just build-native` outside a developer section | all |

`-Local` checks the files in `dist/` instead of the published release, so the gate can run before
`gh release create`. The `ship` skill must call the gate and refuse to publish on a non-zero exit.

**Known follow-ups (not yet done):** `scripts/release-template.ps1` still has `-SkipNsis`, `-SkipMcpb` and
`-SkipSidecar` switches that skip steps this standard makes mandatory. They are for dev dry runs only; a
release created with them fails the gate. They should be removed or made to refuse `gh release create`,
and the template should call the gate and `just cua-nsis-test` itself. The `ship` skill (outside this
repo) needs the same gate call.

## Current state and rollout

Measured 2026-10-06 across the 196 repos with `native/` or `mcpb/`: 37 had a release with assets,
28 had an empty release, 131 had no release. Reference implementation: `docker-mcp`. The fleet sweep
(retrofitting hooks, installers, CUA results, README) is done repo by repo, never in bulk
([GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md) batch limits apply).

## Migrating a repo

- **No webapp, no installer:** nothing to do except releases carrying the `.mcpb`.
- **Webapp, no `native/`:** add the Tauri wrapper from `templates/tauri-native/` (about 2 h the first
  time, about 10 min per build afterwards). Until `native/` exists the repo may not publish a release.
- **Downgrading** (removing the webapp) moves the repo to Class B; delete `native/` and `BUILD_LOG.md`.
