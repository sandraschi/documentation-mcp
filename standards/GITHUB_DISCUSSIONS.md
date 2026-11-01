---
title: "GitHub Discussions — Fleet Standard"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-09-22
# status: active -- piloted on freecad-mcp 2026-09-22 (enable + 4 seed posts
# [Welcome/FAQ/Architecture/Ideas] + README pointer via API; pin/delete-category
# confirmed API-inaccessible, see section 6).
---

# GitHub Discussions — Fleet Standard

**Scope:** running Discussions on OUR repos (announcements, Q&A, community).
Posting to UPSTREAM wrappee repos is covered separately in
`standards/FLEET_PROMOTION.md` section B — this file does not duplicate it.

**Rule of thumb:** Releases are the announcement source of truth.
Discussions Announcements mirror them. Q&A absorbs support so Issues stay
actionable. Never enable Discussions fleet-wide as a sweep.

---

## 1. When to enable

Enable Discussions on a repo only when at least one is true:

- 10+ stars or steady external traffic (issues/PRs from non-maintainers)
- Users already ask support questions as Issues (misfiled Q&A is the signal)
- A release or promotion wave is imminent and questions will follow

Otherwise leave it off. An empty Discussions tab on 190 repos reads as
abandonment and creates moderation surface with no community behind it.
Pilot repo: `freecad-mcp` (27 stars, 3 forks — highest visibility in fleet).

Audit signal (see `patterns/GHAUDIT_SOP.md`): genuine community repos show
issues/discussions activity; scraper-fork repos show forks with no
conversation. Enabling Discussions does not create community — it only
hosts one that already exists.

## 2. Category set

Keep the GitHub defaults minus Polls unless you have a real vote to run:

| Category | Format | Who posts | Purpose |
|----------|--------|-----------|---------|
| Announcements | Announcement | Maintainers only | Release mirrors, roadmap notes |
| Q&A | Q&A (answered/unanswered) | Anyone | Install help, how-do-I questions |
| Ideas | Open discussion | Anyone | Feature brainstorming before it becomes an Issue |
| Show and tell | Open discussion | Anyone | User builds, demos |
| General | Open discussion | Anyone | Everything else |

Delete Polls at setup unless needed — a dead category is worse than a
missing one. Do not invent custom categories until a default one overflows.

## 3. Announcements discipline

- **Mirror, don't originate.** Write the Release first, then post the
  Announcement as a 3-5 line summary + link to the release page.
- **Template:**

```markdown
## {repo} {version} — {one-line headline}

What changed (concrete, 2-4 bullets):
- ...
- ...

Install / upgrade: {link to INSTALL.md or release assets}
Full notes: {link to release page}

Questions go to Q&A; bugs go to Issues.
```

- **Frequency:** releases and major roadmap notes only. No welcome
  placeholders, no weekly noise. One real first post beats a pinned
  "welcome!" template (the `?category=announcements&welcome_text=true`
  prefill is a starting point — replace the body before posting).
- Maintainers-only posting is enforced by the Announcement format.

## 4. Q&A vs Issues split

| Goes to | Examples |
|---------|----------|
| Q&A discussion | Install help, config questions, "does it support X", usage errors |
| Issue | Reproducible bug, missing file, crash with traceback, actionable task |
| Idea discussion | Feature brainstorming, open-ended design |
| Issue (feature) | Scoped, agreed work item promoted out of an Idea |

**Convert, don't scold.** Maintainers can convert Issue to Discussion
(and back) from the sidebar. Misfiled support Issue → convert to Q&A
with a one-line note, then mark the answer. Takes 30 seconds and keeps
the Issues list as the actionable backlog (the `#1/#2` closeout on
freecad-mcp is the model: verify, cite the fix commit, close).

## 5. Moderation minimum

- Mark correct answers on Q&A (drives the Answered/Unanswered filter).
- Lock resolved Announcements to keep them as clean broadcast threads.
- Point at the docs first: `CODE_OF_CONDUCT.md` / `CONTRIBUTING.md`
  if the repo has them; otherwise the repo README + install docs.
- Spam or off-topic: delete discussion, block only for repeat abuse.
- Review cadence: check unanswered Q&A when doing the morning digest
  (`gitops:fleet_morning_digest`) — no separate rota until volume demands it.
- **Open TODO**: `fleet_morning_digest` currently pulls Issues/PRs, not
  Discussions. The value case for Discussions is capturing low-friction
  contributions — a small improv idea someone won't file an Issue or PR
  for but will drop into a Discussion — which only pays off if the
  maintainer actually sees new activity without manually checking every
  repo's tab. Extending the digest to surface new/unanswered Discussion
  activity fleet-wide (not just unanswered Q&A) is unbuilt as of
  2026-09-22 — flagged here, not yet implemented.

## 6. How to enable

1. `gh api -X PATCH repos/{owner}/{repo} -f has_discussions=true` (or Settings → General → Features → check **Discussions**).
2. Delete the Polls category **manually** — GitHub's public GraphQL API has no
   `deleteDiscussionCategory` mutation (confirmed 2026-09-22 on the freecad-mcp
   pilot). Repo Settings → Features → Discussions → category management.
3. Write and post all three seed discussions (Welcome/Announcement, FAQ/Q&A,
   Technical-Architecture/General — see section 6a) **before** telling anyone
   the tab exists. An enabled-but-empty Discussions tab is the thing this
   standard exists to prevent (section 1) — enable and seed are one atomic
   step, never enable-then-seed-later.
4. Pin the FAQ and Architecture discussions **manually** — no `pinDiscussion`
   mutation exists either (same finding). Use the "..." menu on each
   discussion → Pin discussion.
5. Link it once: one line in README **near the top, right after the
   badges/intro, above the first content section** — not buried at the
   bottom. Point to Q&A for support and Ideas/General for the low-friction
   case: a small improvement idea someone won't bother filing an Issue or PR
   for, but will drop into a Discussion where the maintainer actually reads
   it. No badges, no hype. Example (from the freecad-mcp pilot):
   `**Questions, improv ideas, "what if it also did X"?** → [Discussions](...)
   — Q&A for support, Ideas for anything you'd improve but wouldn't file a
   whole Issue for. Bugs still go to [Issues](...).`

### 6a. Seed content (all four required before going live)

Beyond the Announcements template in section 3, every repo enabling
Discussions needs three more seed posts, all written from that repo's own
README/docs/closed-issues — never generic boilerplate:

| Post | Category | Content |
|---|---|---|
| Welcome | Announcements | What the repo does (pulled from README), current version, install link — not a placeholder "welcome!" |
| FAQ | Q&A, pinned | 5-8 real Q&A pairs sourced from the repo's actual closed Issues, README gotchas, and architecture docs — self-answered and marked Answered |
| Architecture | General, pinned | Short writeup of the real design decisions (why this approach, not that one), sourced from the repo's own architecture doc if it has one |
| Ideas & suggestions | Ideas | Seeded from whatever TODO/roadmap content already exists in the repo (PRD.md "Future" section, ROADMAP.md, TODO.md, HANDOVER.md — check the README stack, most fleet repos already have one of these). This is the standard's answer to the low-friction-contribution gap: a small improvement idea someone won't file a whole Issue or PR for, but will drop into a Discussion the maintainer actually reads. If the roadmap doc is stale (planned item shipped differently, or not at all), say so explicitly in the post — don't let a seed post repeat information that's already wrong. |

A repo with no real closed issues, architecture doc, or roadmap/TODO content yet doesn't get Discussions enabled — there's nothing genuine to seed with, which is itself a signal the repo isn't ready (circle back to section 1). If a repo has some but not all four sources (e.g. no PRD/roadmap doc at all), skip only that one post rather than blocking the whole rollout — note the gap in the tracking list instead.

**ASCII hygiene applies to seed posts too** (fleet-wide rule, not new here): no em dashes, en dashes, or smart quotes in titles or bodies — plain `-` only. Caught and fixed after the fact on the freecad-mcp pilot (11+6 em-dash occurrences across two posts, both titles and bodies) — check before posting next time, not after.

**Before enabling on a repo, check for existing discussions first.** `gh api graphql -f query='query{repository(owner:"X",name:"Y"){discussions(first:20){totalCount nodes{number title}}}}'` — a prior session (human or agent) may have already seeded some. Posting a duplicate Welcome/Roadmap/FAQ on top of an existing one is wasted work and clutters the tab, which is exactly what this standard exists to prevent. Confirmed on freecad-mcp 2026-09-22: two of four posts were unrecognized duplicates of the maintainer's own posts from three days earlier, caught only by chance during unrelated smoke-testing — should have been a pre-check, not a post-hoc catch.

## 7. Related docs

- `standards/FLEET_PROMOTION.md` sec B — posting to upstream wrappee
  repos (their Discussions "Community tools / Show and tell").
- `patterns/GHAUDIT_SOP.md` — community-signal audit (issues/discussions
  vs fork noise).
- `patterns/repo-assess-and-fix.md` — assess phase checks community
  surfaces; do not auto-enable Discussions as a fix.
