---
title: "MCP Registry Publishing - Why, Cost, and How"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# MCP Registry Publishing - Why, Cost, and How

**Status:** Official Fleet Standard (adopted 2026-08-27)
**Registry:** https://registry.modelcontextprotocol.io (preview, API frozen at v0.1)

---

## 1. Why publish here

This is the **discovery layer the fleet has been missing**. Before this, discoverability
effort went to LobeHub, punkpeye/awesome-mcp-servers, and glama.ai submissions - all
third-party, unofficial, long-tail directories. None of them is the channel MCP clients
themselves are converging on.

The official MCP Registry is:

- **Backed by the ecosystem's actual stakeholders**, not a community list: Anthropic,
  GitHub, PulseMCP, and Microsoft are named as trusted contributors, not third parties
  scraping GitHub.
- **The upstream source GitHub's own MCP directory pulls from.** GitHub's blog
  (2026, "How to find, install, and manage MCP servers with the GitHub MCP Registry")
  describes publishing once here and having it "automatically" appear in downstream
  registries including GitHub's, replacing the old pattern of notifying a dozen
  directories per release.
- **A metaregistry, not a code host** - same relationship npm/PyPI/Docker Hub have to
  actual package registries. It stores *metadata that points at* the artifact (a GitHub
  release asset, an npm package, a PyPI package), never the code itself. This fleet
  already publishes MCPB bundles as GitHub release assets; the registry entry is a thin
  pointer to something that already exists.
- **Namespace-authenticated**, not first-come-first-served squatting: publishing under
  `io.github.sandraschi/*` requires proving control of the `sandraschi` GitHub account,
  via OAuth login or (for CI) GitHub Actions OIDC. Nobody else can publish under that
  namespace.
- **Where downstream aggregators actually look.** The registry's stated design is to be
  polled by marketplaces and aggregators on an hourly-ish cadence - publishing once here
  is expected to propagate outward automatically, not something the fleet has to repeat
  per directory.

Net effect for a 128-public-repo fleet: one publish step per release replaces N ad hoc
directory submissions, and lands in the channel MCP host applications are actually
starting to consume.

### Expected impact - honest quantification (2026-08-27)

Be clear-eyed about what publishing does and does not buy, or expectations will be wrong.

**Findability: a qualitative shift, not a percentage gain.** The honest, defensible claim
is that for a 128-public-repo fleet, directed discovery moves from "essentially zero"
(someone searching for an MCP server to solve a problem will not find you on GitHub among
millions of repos) to "present in the exact index MCP host applications query" (GitHub's
MCP directory, Claude and other hosts, hourly-polled aggregators). That is the delta that
matters - moving from invisible-in-the-discovery-layer to present-in-it - not a measurable
percent lift on an existing channel. What cannot be promised: traffic numbers. The
registry is still in preview and does not yet have npm/PyPI volume; being indexed is
necessary but not sufficient, because someone still has to actually search and pick your
server.

**Stars/reactions: ~zero from publishing alone.** `server.json` points *at* the repo's
GitHub release; it does not surface the repo in a way that converts to stars. Stars move
only when the few qualified visitors landing on a repo find it worth starring - driven by
README quality, the `docs/` stack, real screenshots, and a working `.mcpb`, not by the
registry entry itself. Correct mental model: **publish → findability lift (discovery),
not star lift (conversion).** The registry is a funnel top, not a star source.

**Prioritization - publish the strong, maintained servers first.** The registry entry
represents the `io.github.sandraschi/*` namespace, so the servers published first should
be the ones that still work when a stranger installs them and that build credibility.
Decision made 2026-08-27: lead with **meta_mcp** (meta-hypertools - actively maintained,
the fleet's real meta-layer), plus **kicad-mcp** and **docker-mcp**. **mcp-studio is
deferred** - it is schema-validated (so listing it costs nothing) but is a low-strategic-
priority repo, not a namespace flag-bearer. Dry-run test order must not dictate release
order.

## 2. Cost: zero

Every part of this pipeline is free, and nothing new needs to be paid for or hosted:

| Component | Cost |
|---|---|
| `server.json` | A git-committed text file. No hosting cost - lives in the repo. |
| `mcp-publisher` CLI | Free, open-source, MIT-licensed binary from `modelcontextprotocol/registry`. |
| Registry hosting | The registry hosts *metadata only* - no storage cost passed to publishers. Publishing is free; there is no publisher tier or paid plan. |
| Namespace auth (GitHub OIDC) | Free. No secrets to provision, rotate, or pay for - `id-token: write` is a permission grant, not a credential. |
| Artifact hosting | Already free: GitHub Releases on public repos, already the fleet's existing MCPB distribution mechanism. Nothing new to host. |
| CI | GitHub Actions minutes on public repos are free (unlimited, per GitHub's public-repo policy). The publish workflow adds one job, seconds of runtime, per tagged release. |

There is no plan tier, no per-server fee, and no artifact-storage fee anywhere in this
flow. The only real cost paid so far this session was engineering time - fixing the
three genuine packaging bugs (flattening, BOM in manifest.json/examples.json, mojibake in
the generator) that were blocking a *correct* bundle from existing in the first place.
Registry publishing itself adds nothing further to build or run.

## 3. Is this actually the industry standard now?

As of 2026-08-27, checked directly against the live docs rather than assumed from
training data:

- The registry is still formally in **preview** - the maintainers' own site says so, and
  breaking changes are possible before general availability. It is not a stable v1 API
  yet (API frozen at v0.1 since 2025-10-24).
- It is nonetheless the **canonical, ecosystem-endorsed** answer to "how do I make my MCP
  server discoverable," not one option among equals. GitHub's own registry integration
  consumes it directly. The MCP spec's own site (modelcontextprotocol.io) hosts the
  publishing quickstart, package-types guide, and GitHub Actions automation guide as
  first-party documentation, not a third-party add-on.
- Every major package ecosystem it federates with (npm, PyPI, NuGet, Cargo, OCI, and
  MCPB/GitHub-releases for bundles) is already supported, which is the actual bar for
  "the registry that matters" rather than a registry that only covers one packaging
  style.

Verdict: preview-stage in maturity, but already the de facto standard in the sense that
matters for a publisher - it's where the ecosystem's own tooling looks first, and every
day spent publishing only to the long-tail directories is a day of foregone
discoverability through the channel that's actually converging.

## 4. How - the fleet's actual pipeline

1. **Build a correct `.mcpb`.** `mcp-central-docs/scripts/make-mcpb.ps1 -RepoName <repo>`
   (or, for multi-package repos where the generic script would guess wrong - see
   `docker-mcp` - pack directly from an already-correct `mcpb/` via
   `mcpb pack <mcpb-dir> <output.mcpb>`). Verify the *actual* archive contents with
   `Expand-Archive` on a renamed `.zip` copy before trusting any CLI summary output -
   the `mcpb pack` summary line has shown misleading noise (a `C:/Windows/System32/`
   line that was cwd-context display, not a packed file) at least twice this session.

2. **Generate `server.json`.**
   `mcp-central-docs/scripts/generate-server-json.ps1 -RepoName <repo>`. Derives
   `name` (`io.github.sandraschi/<repo-dir>`), `description` (truncated to the
   registry's 100-char hard limit), `version`, and `repository.url`/`source` from the
   repo's own `pyproject.toml` and git remote. Computes a **real** `fileSha256` from the
   local `dist/*.mcpb` - refuses (exits 1) rather than writing a placeholder that looks
   confident but isn't, if no build exists yet.

3. **Validate before publishing.**
   `mcp-publisher validate` (installed at
   `C:\Users\sandr\AppData\Roaming\npm\mcp-publisher.exe`) checks `server.json` against
   the live schema without touching the registry. Zero risk, do this every time.

### Description quality gate (added 2026-08-27)

The registry entry's `description` is **the `pyproject.toml` `description` truncated to 100
chars** - NOT the GitHub repo description. It now surfaces publicly (registry search, and it
would also show on PyPI), so internal fleet jargon ships to strangers verbatim.

**Rule (HARD):** before generating `server.json`, the `pyproject.toml` `description` must be
**user-facing marketing copy, ≤ 100 chars**, written for someone who has never heard of the
repo. If it contains fleet jargon, "SOTA", internal version tags, or is longer than 100 chars
(so it truncates awkwardly), rewrite it first. Then regenerate `server.json`.

Checklist per repo:
- Plain-language, outsider-readable (what it does + who it's for), not fleet-speak.
- `≤ 100 chars` so the registry does not cut it mid-phrase.
- ASCII only (no em/en dashes, no smart quotes - see ASCII hygiene; mojibake em dashes have
  recurred in several `pyproject.toml` descriptions).
- The GitHub repo description is often already-good copy - use it as the starting point.

**Propagation caveat:** honing the description only takes effect on the registry when a
**new version** is published. The registry rejects re-publishing the same version
("duplicate version"), so an already-registered server keeps its old description until its
next version bump. Set the description right *before* first publish; plan version bumps for
already-registered repos to refresh stale copy.

4. **Tag and let CI publish.** `mcp-central-docs/templates/publish-mcp-registry.yml`
   copied into a repo's `.github/workflows/`, triggered by `git tag v<version>` +
   `git push origin v<version>`. Uses GitHub Actions OIDC - no secrets to manage. The
   template pre-flight-checks that `server.json` exists and has no placeholder hash
   before attempting anything.

### Known residual issues (do not treat the pipeline as flawless)

- `make-mcpb.ps1`'s own `mcpb` CLI detection (via `npx`) reports "not available" even
  when `mcpb.cmd` is genuinely installed and working - a PATH-resolution bug in that
  script, worked around this session by invoking `mcpb.cmd` directly. Not fixed.
- `.mcpbignore` for at least one repo (`docker-mcp`) let a stray `.ruff_cache/` directory
  into the packed bundle. Cosmetic, not functionally broken, not swept fleet-wide.
- Three of `make-mcpb.ps1`'s six template writes (`system.md`, `user.md`, `README.md`)
  still write with a UTF-8 BOM. Low-priority - markdown renders fine with a BOM, unlike
  JSON, which hard-fails. Not fixed in this pass.
- The dry-run batch so far is 3 repos (`kicad-mcp`, `docker-mcp`, `mcp-studio`), each
  individually live-import-verified *and* schema-validated. This is not yet a
  fleet-wide guarantee - see `2026-08-27 14:10 mcp-studio fix and fleet-wide live-import
  sampling pass` for why the structural mcpb audit alone is known to miss real bugs.
- **Prioritization (2026-08-27):** `mcp-studio` is now **deferred** as a lead publisher -
  it is not a star performer. The first real publish should lead with **meta_mcp**
  (meta-hypertools), which is *not* yet in the dry-run batch and therefore needs its own
  build + `server.json` + `validate` pass before it can publish.

## 5. Reading the registry (search & verification)

To search the registry (competitor scans, verifying our servers are findable, feature
diffing) use the **v0.1 servers endpoint with the `search` param**:

```
GET https://registry.modelcontextprotocol.io/v0.1/servers?search=<substring>
```

- `search` = **substring match on the server name** (verified 2026-08-27).
- Returns JSON: `{ "servers": [ { "server": { "name", "description", "version",
  "repository", "packages"/"remotes" }, "_meta": {...} } ], "metadata": { "cursor", "count" } }`.
- Use `?search=resonite` to see whether a niche is owned; e.g. `resonite` returns only
  `io.github.sandraschi/resonite-mcp` today, while `godot` returns 5 competitors.

**Known footguns (checked live 2026-08-27):**
- The path is **`/v0.1/servers`**, NOT `/v0/servers` (which 404s or ignores filters).
- The filter param is **`search`**, NOT `query`/`q`/`name` (those return the same unfiltered
  page-1 list, silently ignoring the query).
- **Do not query the registry through a web-fetch proxy**: the Anthropic `web_fetch` proxy
  silently strips query strings on `registry.modelcontextprotocol.io`, and other fetch MCPs
  fail on the JSON endpoint. **Use `Invoke-RestMethod` / `curl.exe` on the local machine**
  (direct HTTP) - that is the reliable path for registry API queries.
- The per-server deep URL (`/v0.1/servers/<id>`) is not a stable lookup; use search or the
  `metadata.cursor` pagination instead.

## 6. Explicitly not done yet

Actual publication to the live registry (`mcp-publisher publish` for real, or a real
`git tag` + push triggering the CI workflow) has not been executed for any repo. That is
a genuine public, hard-to-fully-reverse action and is being treated as requiring its own
explicit go-ahead, separate from generating and validating `server.json` locally.

---

*Sources checked live on 2026-08-27, not from training data: registry.modelcontextprotocol.io
schema, modelcontextprotocol.io/registry/{about,package-types,github-actions}, GitHub's
own MCP registry blog post, and a third-party package manifest (glama.ai mise.lock)
confirming the current `mcp-publisher` release version and per-platform checksums.*
