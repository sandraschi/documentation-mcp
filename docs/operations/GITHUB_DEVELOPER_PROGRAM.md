# GitHub Developer Program - Decision (2026-09-22)

## Trigger
Banner seen on `github.com/sandraschi` profile:
"Building an application, service, or tool that integrates with GitHub? Join the GitHub Developer Program"

Question: should we join, given `git-github-mcp` (breakfast run, star stats for fleet, etc.)?

## What it is
Source: https://docs.github.com/en/developers/overview/github-developer-program

- Free program for individual developers and companies building tools that integrate with GitHub APIs.
- Registration: https://github.com/developer/register (must be logged in).
- Requirements:
  1. An integration in production or development using the GitHub API.
  2. An email address where GitHub users can contact you for support.
- What you get:
  - API change / preview news.
  - Right to use Octocat / GitHub logo ("works with GitHub").
  - Place to post video/blog about integration.
  - Credibility prerequisite for later Marketplace / Partner / OAuth App steps.
- What you do NOT get: traffic, stars, rate-limit increase, money, review, promotion. Not Marketplace, not Sponsors, not Partners.

## Does git-github-mcp qualify?
Yes.

- Wraps `git` + GitHub via `gh` CLI (REST + GraphQL via `gh api`) — history, branches, PRs, issues, releases, workflows, secrets, code search, discussions. That is GitHub API usage.
- Differentiating fleet features: `/breakfast` morning digest + 15 fleet ops + full suite, `/stars` received-vs-given + trajectory, `/ci` monitor + rerun + AI diagnose, 73-op `github_ops` portmanteau.
- In production: `D:\Dev\repos\git-github-mcp`, MIT, `.mcpb` Releases, `INSTALL.md`, `docs/ONBOARDING.md` (`gh auth login`).
- Auth model: user's own `gh` PAT, local-first, no OAuth App, no hosted secrets — no security review needed. Joining changes nothing in code.
- Support contact: `https://github.com/sandraschi/git-github-mcp/issues` counts; add contact email at registration.

## Decision
JOIN as `sandraschi` (individual). Cost ~5 min, free, no obligations.

Expectation: badge + API news + logo rights, not growth. Distribution for git-github-mcp comes from repo topics (`mcp`, `github`, `claude-desktop`, `gh-cli`), `.mcpb` Releases, Glama/MCP directories, and demo hook ("morning digest across fleet") — not from this program.

If later converted to hosted GitHub App / Marketplace listing, revisit Partner track.

## How to join (for Sandra)
1. Log in as `sandraschi` at https://github.com/developer/register
2. Fill: display name `sandraschi`, integration URL `https://github.com/sandraschi/git-github-mcp`, description: "Local-first git + GitHub MCP server (gh CLI): fleet morning digest, star intelligence, CI monitor, 73 GitHub ops for AI agents", support email (your contact email), integration status: production.
3. Submit, confirm email if asked.
4. Optional: add "Built with GitHub" / Octocat logo to `git-github-mcp/README.md` per https://github.com/logos.
5. Record date + screenshot in `projects/git-github-mcp/` and session-log.

## Related
- Repo: `D:\Dev\repos\git-github-mcp` + `mcp-central-docs/projects/git-github-mcp/`
- Standards: `operations/github-workflows.md`
- Patterns: `patterns/GITHUB_MAINTAINER_HEARTBEAT.md`
- Previous analysis: 2026-09-22 chat (should-we-join verdict: yes, low-cost, no growth expectations).
