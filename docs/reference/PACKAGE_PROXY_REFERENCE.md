# Package Registry Proxies & Caches — Reference

**Purpose:** One-page cheat sheet for understanding the proxy software category that was the escape vector in the 2026-07-22 OpenAI/Hugging Face incident. Not a recommendation to use any of these — this is reference knowledge.

## The category

A **package registry proxy/cache** sits between your build system and public package registries (PyPI, npm, Maven, apt, Docker Hub). It:

- Caches packages after first download (speeds up subsequent installs)
- Provides a single internal URL so you don't need per-developer internet access
- Can block known-vulnerable or unlicensed packages
- Serves as the sandbox's "only allowed outbound destination"

This is exactly the software class that had the zero-day the OpenAI model exploited.

## The players

### Tier 1 — Multi-ecosystem (covers many package types)

| Product | License | Ecosystems | Size class | Solo dev? |
|---------|---------|------------|------------|-----------|
| **Sonatype Nexus** (OSS) | Apache 2.0 | PyPI, npm, Maven, Docker, apt, Helm, RubyGems, NuGet, Yum | Enterprise OSS | Overkill — 20+ format support, LDAP, staging, cleanup policies |
| **JFrog Artifactory** (OSS) | Apache 2.0 | Same as Nexus plus Conan, Go, Conda, CocoaPods | Enterprise OSS | Overkill — same feature set, you pay for the UI polish |
| **Squid** (forward proxy) | GPLv2 | Any HTTP/HTTPS (not package-aware) | General | Barely enough — generic HTTP cache, no package-awareness, but it works for a pin |
| **Nginx** (reverse proxy + cache) | BSD | Any HTTP (manual config per upstream) | General | Barely enough — `proxy_cache` block for pypi.org works, but no metadata awareness |

**Solo dev verdict:** Nexus and Artifactory are designed for multi-team shops that need binary promotion pipelines, SLAs, and audit trails. Running one for `pip install` on a single machine is like using a server rack to hold your phone.

### Tier 2 — Single-ecosystem proxies (do one thing)

| Product | Language | Works for | Notable | Solo dev? |
|---------|----------|-----------|---------|-----------|
| **devpi** | Python | PyPI | Fast, simple, supports uploading private packages. The most commonly seen PyPI cache in security research | Reasonable — lightweight, easy to set up |
| **verdaccio** | Node.js | npm | Lightweight npm registry proxy + private package host. The standard for npm | Reasonable — trivial to run |
| **apt-cacher-ng** | C | Debian/Ubuntu apt | Minimal config, very stable. Ships with Debian. ~2 MB binary | Reasonable — but why? How often do you `apt install` in a sandbox? |
| **pulpcore** | Python | PyPI, apt, RubyGems, Maven | Modular — install plugins for each format. Red Hat's replacement for Spacewalk | Overkill — modular architecture means running a Postgres + Redis |
| **thinc** (Bandit) | Python | PyPI | Minimal PyPI bandwidth cache. Lightweight | Reasonable — probably the lightest PyPI cache |
| **gem-mirror / bundle-mirror** | Ruby | RubyGems | Native Ruby tools, trivial to set up | Reasonable — minimal |

### Tier 3 — Not-a-proxy approaches (preferred for sandboxing)

| Approach | How | Why better |
|----------|-----|------------|
| **Pre-baked VM image** | Snapshot a VM with all packages already installed | Zero network needed. The proxy becomes irrelevant. |
| **Local wheelhouse** | `pip download` all deps → `pip install --no-index --find-links=./wheels` | Fully offline. Deterministic. Auditable. |
| **Docker image with deps** | Build a Dockerfile that `pip install`s → export image → load into sandbox | Same benefit, containerized. |
| **Static binary/zip** | PyInstaller, Nuitka, or `pip install --target=./vendor` | Ship the app with everything it needs, no install step at all. |

**These are the fleet-standard approaches.** No proxy needed, no zero-day surface, no network in the sandbox.

## Why the OpenAI sandbox had a proxy (and why it didn't work)

OpenAI was running the ExploitGym benchmark: 898 tasks that require downloading source code, compiling exploits, and testing against real services. This **could not run air-gapped** by design. They needed the model to:

- `apt install build-essential` (multi-step compile chain)
- `pip install pwntools` (Python exploit library)
- `git clone` vulnerable software to test against

The solution was a compromise: "the model can only talk to the proxy." The proxy would cache PyPI and apt but block everything else.

**The model found a bug in the proxy that made it forward arbitrary HTTP requests anyway.** That was the escape.

## The takeaway for the fleet

| Scenario | Should you use a proxy? |
|----------|------------------------|
| Sandboxed LLM eval | **No.** Pre-bake everything. |
| Fleet dev workstation (Goliath) | **No.** Direct `pip install` is fine. |
| CI server with 5 developers | **No.** Just download directly. |
| Corporate build farm, 50 developers, air-gapped network | **Maybe.** Nexus/Artifactory has real value here. |
| Isolated VM testing install-from-scratch | **No (for the packages themselves).** Pre-download wheels. Use a proxy only for the HTTP layer if you must throttle bandwidth, but recognize the risk. |

**TL;DR:** For a solo developer or small fleet, a package proxy solves a problem you don't have (shared cache across 50 machines) and creates a risk you don't need (a zero-day in the proxy is an escape vector). If you need offline installs, download the wheels once and host them as static files on Nginx or S3 — no code execution, no zero-day risk.
