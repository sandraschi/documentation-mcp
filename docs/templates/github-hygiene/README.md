# GitHub hygiene kit (fleet-wide issue/PR standard)

Canonical templates for how **our own** fleet repos receive issues and PRs.
Pioneered in `vcv-rack-mcp` (2026-10-22) after inbound user mail showed the
alternative is chaos. For how we behave in *other people's* projects, see
`standards/rules/open_source_contributing.md` instead.

## Contents

- `ISSUE_TEMPLATE/bug_report.yml` — version/commit, repro steps, expected vs actual, **artifact attached** (patch file, log, screenshot — whatever reproduces it)
- `ISSUE_TEMPLATE/feature_request.yml` — one-line summary, persona dropdown, what/why/sketch
- `ISSUE_TEMPLATE/config.yml` — blank issues allowed, no fake contact links
- `pull_request_template.md` — linked issue, checklist (tests, lint, catalog validator, changelog)
- `CONTRIBUTING.md` — issues-first, small tested PRs, maintainer merges

## Adopt in a repo (5 minutes)

```powershell
New-Item -ItemType Directory -Path ".github\ISSUE_TEMPLATE" -Force
Copy-Item mcp-central-docs\templates\github-hygiene\ISSUE_TEMPLATE\* .github\ISSUE_TEMPLATE\
Copy-Item mcp-central-docs\templates\github-hygiene\pull_request_template.md .github\
Copy-Item mcp-central-docs\templates\github-hygiene\CONTRIBUTING.md .
```

Then adapt the `ADAPT:` markers to the repo (they are comments — invisible in rendered forms):

- `CONTRIBUTING.md` carries vcv-rack-mcp specifics (catalog verification rule,
  no-DSP, free-modules-only). Keep the shape, swap the domain rules.
- `bug_report.yml` asks for a `.vcv` patch — replace with whatever artifact
  reproduces bugs in *your* repo (config file, log excerpt, screenshot).
- `config.yml`: add `contact_links` only for channels that actually exist
  (discussions, docs). Never link email unless you want the mail.
- PR template checklist: drop lines that don't apply (e.g. no webapp → no
  biome/tsc), keep tests + lint + changelog unconditionally.

Commit message: `GitHub hygiene: issue forms, PR template, contributing guide`.
