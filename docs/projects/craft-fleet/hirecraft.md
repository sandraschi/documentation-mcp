# HireCraft — Assessment

**Repo:** `D:\Dev\repos\hirecraft` · **Date:** 2026-11-12 · **Grade:** C · **Origin:** fleet-owned

## What it is

Local-first sovereign Applicant Tracking System (ATS), blind scorecard interview pipeline, and automated employee onboarding engine. Replaces commercial recruiting SaaS (Greenhouse, Lever, Ashby) with a local SQLite workstation and automated onboarding cascades across the fleet. Part of the Back-Office Craft Suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`).

## Architecture & Verbs

- **Crates:**
  - `crates/hirecraft-store`: Pure SQLite database layer (`JobRequisitions`, `Candidates`, `Scorecards`).
  - `crates/hirecraft-core`: Structured recruiting stage pipeline (`applied` → `screening` → `interview` → `offer` → `hired`), blind scorecard aggregation, onboarding cascade dispatcher.
  - `crates/hirecraft-mcp`: Stdio JSON-RPC FastMCP server & CLI binary (`hirecraft`).
  - `crates/hirecraft-app`: Native desktop GUI workstation (`hirecraft-app`) via `egui 0.37`.
- **MCP Tools / CLI Verbs:**
  - `hire_status`, `hire_req_create`, `hire_req_list`, `hire_candidate_create`, `hire_candidate_show`, `hire_candidate_stage`, `hire_candidate_hire`, `hire_scorecard_add`.
- **Bus Integration:**
  - Outbound: Transitioning a candidate to `hired` simultaneously emits `candidate.hired` to:
    1. `contractcraft\inbox` (drafts Austrian employment contract)
    2. `teamcraft\inbox` (creates 38.5h AZG employee profile and statutory leave entitlement)
    3. `assetcraft\inbox` (reserves primary hardware workstation)

## Strengths

- Pure Rust with strict `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
- Blind quantitative scorecards (1–5 ratings across technical skills and cultural alignment) to eliminate bias.
- Fully automated cross-fleet onboarding handshake eliminating multi-day HR onboarding delays.
- Tri-modal: L1 CLI, L2 FastMCP, L3 native desktop egui 0.37 with live smoke tests.

## Gaps & Non-Goals

- Non-goal: Direct scraping of LinkedIn / Indeed job boards (resumes/candidates are ingested via local JSON/CLI or agent tools).
- Non-goal: Automated video interview recording (handled via local OBS/teleconference tools).

## Verdict

Grade C: Stages, scorecards, and a three-event hire cascade. Downstream apps do not consume the event. It does not replace Greenhouse. PRD: `D:\Dev\repos\hirecraft\docs\PRD.md`.
