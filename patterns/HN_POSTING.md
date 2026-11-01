# HN posting - lifecycle, hand-post rule, discuss links, comment strategy

**Status:** Playbook v1 2026-10-05 - execution companion to [standards/FLEET_PROMOTION.md](../standards/FLEET_PROMOTION.md) (policy: useful pointer, not spam) and [patterns/PROMOTION_PLAYBOOK.md](./PROMOTION_PLAYBOOK.md) (general order)
**Tags:** [fleet, promotion, hacker-news, lobsters, runbook]
**Source:** distilled from the sandraschipal-com launch thread (SPEC Phase 6, Nolan Lawson reference) - the durable parts, not the post-specific parts.

## 1. Principle: human posts, agent never submits

HN has no write API. Submission is login + form + anti-bot heuristics, and automation risks the account. Same for Lobsters. Rule:

- Agents may draft, lint, and record links. Only Sandra submits, from her own account, by hand.
- Never brigade: no asking the fleet, Discord, or friends to upvote or seed comments. HN detects velocity anomalies and kills the post or flags the account. Organic or nothing. One account, no sockpuppets.
- No "Show HN" on essays (that prefix means a thing to try, not a thing to read). Plain self-describing title.

## 2. Lifecycle: spike then invisible (normal)

- `/newest` -> front page in 1-3h on velocity -> top 3-5 means hundreds of comments day one -> decay wins within 12-24h -> page 3+ by day 2 -> reachable only via direct link, search, or `/past` by day 7.
- HN has no native "best of all time / this year" section. Just `/front`, `/past` (date picker), `/ask`/`/show`, and permanent `item?id=` links. The "best of" layer is third-party: hn.algolia.com search, yearly roundup blog posts, and long-tail referral traffic.
- Consequence: the durable asset is the essay on our domain plus the discuss link proving it survived HN. The thread is rented, the post is owned. Reposts of the same link within weeks are discouraged; a new angle years later is fine.

## 3. Submission workflow (Phase 6 pattern)

1. Draft merged with empty `discuss:` frontmatter. Post live, RSS fires.
2. Sandra hand-submits to HN (and Lobsters if wanted) with a plain title. Stays for the first 2-3 hours.
3. Follow-up commit fills in the URLs. Agents may record links, never submit. See section 4.

## 4. Discuss links (Nolan pattern + GitHub 4th link)

Frontmatter schema (all optional, render only what exists):

```md
discuss:
  hn: "https://news.ycombinator.com/item?id=..."
  lobsters: "https://lobste.rs/s/..."
  mastodon: "https://toot.cafe/@user/..."
  github: "https://github.com/sandraschi/sandraschipal-com/discussions/42"
```

- Rendered as one line at the post bottom: "Discuss on HN / Lobsters / the fediverse / GitHub." No embeds, no comment JS, no spam queue.
- `github` points at one thread in the site repo Discussions "Posts" category (creatable via `gh` API with Sandra's auth - legitimate automation, unlike HN submission). Link out, never embed Giscus - keeps the zero-JS budget.
- Most posts get 2 links; the big one gets 3-4. Feed GUIDs/URLs must stay stable across rebuilds or followers get re-dumped (CI check: rebuild twice, diff GUIDs).

## 5. Comment strategy: host, not main act

- Windows: first 2-3h after front page, one evening check, one next morning. After 48h let it go.
- Volume: ~10-20 substantive replies on a 200-comment thread. Batch every 30-45 min, not instant per-comment (a wall of OP replies reads as bot-or-desperate).
- Answer: factual corrections (take gracefully, edit post with "corrected" note), genuine mechanics questions (the stuff only we know), smart pushback (steelman, concede what holds), people sharing their own incidents (acknowledge, one follow-up).
- One polite reply max to: AI-doom threads, framework wars, "just use X" drive-bys. Never feed trolls. Pure praise gets "thanks" or an upvote, not an essay.
- Corrections that improve the piece get folded back into the essay with a note. That edit history turns a one-day spike into a link cited for years.

## 6. Editorial rule: AI drafts, human revises, human posts

- Drafts stay `draft: true`, ASCII-hygiene normalized, until human rewrite. LLMs never touch final prose, not even spellcheck.
- Agent quotes fenced in blockquote/details so readers know human vs robo words.
- Revision strips LLM tells: em-dash chains, "It's not X, it's Y" pivots, triplets, crucial/critical/paramount stacking, loanwords ("load-bearing", "belt-and-suspenders"), "tapestry"/"delve"/"in today's fast-paced", hedged corporate mush, neat wrap-up conclusions.
- No faked typos or performed imperfection. Human texture comes from specifics (dates, counts with snapshot dates, errors admitted) and open problems, not jitter.

## 7. Parallel boards (Asia, phase 2 - not launch day)

Neither takes English posts well; machine translation backfires. Launch English-only, translate by a human later, same hand-post + stay-for-comments rule (V2EX and Hatena both punish bots and brigading).

- China: V2EX (v2ex.com) is the HN equivalent (dev-heavy, curated, self-promo policed, Chinese required). Juejin (juejin.cn) for long-form reach. Avoid CSDN. Note: GitHub is slow from China - a Gitee mirror link (fleet has gitee-mcp) doubles credibility.
- Japan: Hatena Bookmark (b.hatena.ne.jp) is the functional HN (link aggregation, discussion in bookmark comments). Zenn (zenn.dev) is the best article home (Markdown-native, GitHub-synced, matches our Astro workflow). Qiita as either/or with Zenn.
