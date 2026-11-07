---
title: "Design Review - 80 Item Visual Audit and Repair Loop"
category: pattern
status: active
audience: mcp-dev
last_updated: 2026-11-04
---

# Design Review - 80 Item Visual Audit and Repair Loop

A structured visual audit for a running page, followed by a bounded repair loop
with visual proof. Ten categories, roughly eighty checks, a dual headline score
(Design + AI Slop), and a fix budget.

**Adapted** from `garrytan/gstack` `design-review/SKILL.md` at commit
`622e8b1f76d293b647eca7b33d9dd060ab618b21` (MIT). Provenance and the decision to
port rather than install: `GSTACK_METHODOLOGY_ADOPTION.md`.

---

## 1. Why this exists in the fleet

`FAKEFIND_AUDIT_SOP.md` and `GAPFIND_AUDIT_SOP.md` are read-only. They tell you
what is wrong and stop. `WEBAPP_SOTA_STANDARDS.md` states what good looks like but
does not audit a running page.

This adds the missing half: audit the rendered page, then fix, then prove the fix
with before and after evidence.

Use it when a fleet webapp is going into a demo, a release, or a first
screenshot set - or when a page "looks off" and nobody can say why.

---

## 2. Hard rules before you start

1. **Audit the rendered page, not the source.** Reading JSX to guess how it looks
   is exactly the failure this pattern exists to prevent.
2. **Screenshots are the evidence.** Every finding that changes a grade needs a
   before screenshot. Every fix needs a before and after. A finding without a
   picture is an opinion.
3. **One commit per fix**, message `style(design): FINDING-NNN <what changed>`.
   Bisectable, revertable, reviewable.
4. **Never audit a page you are not authorized to load.** Fleet webapps run on
   localhost ports from `operations/WEBAPP_PORTS.md`. Auditing a third-party site
   against this checklist is fine for study, but do not drive its forms or mutate
   anything on a non-local origin without explicit approval for the exact actions.
5. **Stop at 30 fixes.** The audit finds more than anyone should change in one
   pass. Cap it, report the rest, and let a human schedule them.
6. **A grade is not a score to maximize.** Grade honestly; a D that is true is
   worth more than a B that is flattered.

---

## 3. Scope modes

| Mode | Scope | Use |
|---|---|---|
| Full (default) | 5-8 pages reachable from home, full checklist, responsive captures | Normal pre-release pass |
| Quick | Home + 2 key pages, First Impression + design system extraction | Fast gut check |
| Deep | 10-15 pages, every interaction flow, exhaustive | Pre-launch or redesign |
| Diff-aware | Only pages touched by the current branch | PR review on a webapp change |
| Regression | Full run plus comparison against the previous `design-baseline.json` | Verify a fix campaign worked |

For diff-aware runs, determine the base branch explicitly. Do not assume `main`.

```powershell
gh pr view --json baseRefName -q .baseRefName
gh repo view --json defaultBranchRef -q .defaultBranchRef.name
git diff <base>...HEAD --name-only
```

---

## 4. Phase 1 - First Impression

Do this before analyzing anything. A gut reaction is data; once you start
measuring, you cannot get it back.

Take a full-page desktop screenshot, then write this exact shape:

```
The site communicates __[what]__.
I notice __[specific observation, positive or negative]__.
The first 3 things my eye goes to are: [1], [2], [3].
If I had to describe this in one word: __[word]__.
```

The hierarchy check is the useful part. If your eye lands on something the
designer did not intend to be primary, the visual hierarchy is lying, regardless
of how polished the page looks.

**Page Area Test:** name the purpose of each clearly defined region in two
seconds. List the regions you cannot name. Those are poorly defined.

---

## 5. Trunk Test (run on every page)

Dropped onto this page with no context, can you answer at once:

1. What site is this?
2. What page am I on?
3. What are the major sections?
4. What are my options here?
5. Where am I (breadcrumb, "you are here")?
6. How do I search?

**PASS** = all 6. **PARTIAL** = 4-5. **FAIL** = 3 or fewer.

A FAIL is a **high-impact** finding no matter how beautiful the page is.

---

## 6. Phase 2 - Design System Extraction

Extract what the page actually renders, not what a design doc claims.

Collect and count:

- **Font families** with usage counts. Flag if more than 3.
- **Colors** in use. Flag if more than 12 unique non-gray colors. Note whether
  the neutral range is warm or cool, and whether it is mixed.
- **Heading scale** h1-h6. Flag skipped levels and non-systematic jumps.
- **Spacing samples**. Flag values off the declared scale.
- **Touch targets** under 44px on interactive elements.

If the extracted system is coherent, offer to record it as the project's
`DESIGN.md` baseline. If it is not coherent, that is finding 1.

---

## 7. The checklist - 10 categories

Rate each finding **high**, **medium**, or **polish**, and assign a category.
Polish findings are noted and do not affect the grade.

### 7.1 Visual Hierarchy and Composition (8)

- Clear focal point? One primary CTA per view?
- Eye flows naturally top-left to bottom-right?
- Visual noise - competing elements fighting for attention?
- Information density appropriate for the content type?
- Z-index clarity - nothing unexpectedly overlapping?
- Above-the-fold content communicates purpose in 3 seconds?
- Squint test: hierarchy still visible when blurred?
- White space intentional, not leftover?

### 7.2 Typography (15)

- Font count <= 3 (flag if more)
- Scale follows a ratio (1.25 major third or 1.333 perfect fourth)
- Line-height 1.5x body, 1.15-1.25x headings
- Measure 45-75 characters per line (66 ideal)
- Heading hierarchy has no skipped levels (h1 to h3 without h2)
- Weight contrast: at least 2 weights used for hierarchy
- No banned fonts: Papyrus, Comic Sans, Lobster, Impact, Jokerman,
  Bleeding Cowboys, Permanent Marker, Bradley Hand, Brush Script, Hobo, Trajan,
  Raleway, Clash Display, Courier New
- Display face on the overused list (Inter, Roboto, Arial, Helvetica, Open Sans,
  Lato, and similar) - flag `[overused-font]`; as body or UI on an Operate or
  Read surface it passes when `DESIGN.md` says so deliberately
- `text-wrap: balance` or `text-pretty` on headings
- Curly quotes, not straight quotes
- Ellipsis character, not three dots
- `font-variant-numeric: tabular-nums` on number columns
- Body text >= 16px
- Caption and label text >= 12px
- No letter-spacing on lowercase text

### 7.3 Color and Contrast (10)

- Palette coherent (<= 12 unique non-gray colors)
- WCAG AA: body 4.5:1, large text (18px+) 3:1, UI components 3:1
- Semantic colors consistent (success green, error red, warning amber)
- No color-only encoding (add labels, icons, or patterns)
- Dark mode: surfaces use elevation, not just inverted lightness
- Dark mode: text off-white (around #E0E0E0), not pure white
- Primary accent desaturated 10-20 percent in dark mode
- `color-scheme: dark` on the html element when dark mode exists
- No red/green-only combinations (about 8 percent of men have red-green deficiency)
- Neutral palette is consistently warm or cool, not mixed

### 7.4 Spacing and Layout (11)

- Grid consistent at all breakpoints
- Spacing uses a scale (4px or 8px base), not arbitrary values
- Alignment consistent - nothing floating outside the grid
- Rhythm: related items closer, distinct sections further apart
- Border-radius hierarchy, not one uniform bubbly radius on everything
- Nested radius: inner radius = outer radius minus gap
- Max content width set (no full-bleed body text)
- `env(safe-area-inset-*)` for notch devices
- URL reflects state (filters, tabs, pagination in query params)
- Flex or grid used for layout, not JS measurement
- Breakpoints at mobile 375, tablet 768, desktop 1024, wide 1440

### 7.5 Interaction States (12)

- Hover state on all interactive elements
- `focus-visible` ring present (never `outline: none` without a replacement)
- Active/pressed state with depth or color shift
- Disabled state: reduced opacity plus `cursor: not-allowed`
- Loading: skeleton shapes match the real content layout
- Empty states: warm message plus a primary action plus a visual, not just
  "No items."
- Error messages specific and include the fix or next step
- Success: confirmation animation or color, auto-dismissing
- Touch targets >= 44px on all interactive elements
- `cursor: pointer` on all clickable elements
- **Mindless choice audit:** every decision point (button, link, dropdown, modal
  choice) is an obvious click. If a click requires thought about whether it is
  the right choice, that is **high** impact.
- **Browser surfaces themed from the palette:** selection color, caret, scrollbars,
  focus ring, underline offset, tabular numerals. Left at defaults, the page reads
  as assembled rather than designed.

### 7.6 Responsive Design (6)

- Mobile layout makes design sense, not just stacked desktop columns
- No horizontal scroll at any viewport
- Images responsive (srcset, sizes, or CSS containment)
- Navigation collapses appropriately
- Forms usable on mobile (correct input types, no autofocus on mobile)
- No `user-scalable=no` or `maximum-scale=1` in the viewport meta

### 7.7 Motion and Animation (7)

- Easing: ease-out to enter and exit, ease-in-out to move; flag plain ease-in
- Duration in the 50-700ms range (nothing slower unless a page transition)
- Purpose: every animation communicates something
- `prefers-reduced-motion` respected
- No `transition: all` - properties listed explicitly
- Only `transform` and `opacity` animated, not layout properties
- One authored motion moment per page. Not the same entrance on every section,
  not a hover effect on everything. Content never hides behind animation timing.

### 7.8 Content and Microcopy (8)

- Button labels specific ("Save API Key", not "Continue" or "Submit")
- No placeholder or lorem ipsum text in production
- Truncation handled (ellipsis, line-clamp, or break-words)
- Active voice ("Install the CLI", not "The CLI will be installed")
- Loading states end with an ellipsis character ("Saving...", not "Saving")
- Destructive actions have a confirmation or an undo window
- **Happy talk:** welcome paragraphs and self-praise. Report
  "this page has X words, Y (Z percent) are happy talk."
- **Instructions longer than one sentence mean the design failed.** Flag the
  instructions and the interaction they compensate for.

### 7.9 AI Slop Detection

The test: would a human designer at a respected studio ever ship this?

**Blacklist patterns (11):**

- Purple/violet/indigo gradient backgrounds or blue-to-purple schemes
- **The 3-column feature grid:** icon in colored circle + bold title + 2-line
  description, repeated 3x symmetrically. The most recognizable AI layout.
- Icons in colored circles as section decoration
- Centered everything (`text-align: center` on all headings, descriptions, cards)
- Uniform bubbly border-radius on every element
- Decorative blobs, floating circles, wavy SVG dividers (if a section feels empty
  it needs better content, not decoration)
- Emoji as design elements (rockets in headings, emoji as bullets)
- Colored left border on cards
- Generic hero copy ("Welcome to X", "Unlock the power of...",
  "Your all-in-one solution for...")
- Cookie-cutter section rhythm (hero, 3 features, testimonials, pricing, CTA,
  every section the same height)
- `system-ui` or `-apple-system` as the primary display/body font - the
  "gave up on typography" signal

**Detector rule ids** (a mechanical scanner's name for the same pattern; a scan
hit and a judgement hit on one element are one finding): `border-accent-on-rounded`,
`overused-font`, `flat-type-hierarchy`, `gradient-text`, `cream-palette`,
`nested-cards`, `shape-assembled-illustration`, `dark-glow`, `radial-halo`,
`radial-spotlight-glow`, `marquee`, `icon-tile-stack`, `italic-serif-display`,
`hero-eyebrow-chip`, `kicker-above-heading`, `marketing-buzzword`,
`aphoristic-cadence`, `oversized-h1`, `theater-slop-phrase`.

**Judgement tells (you are the detector):**

- Gradient buttons as the primary CTA. One solid color the palette owns.
- A generic stock-photo hero, or a gray placeholder div standing in for one.
- Rounded cards with drop shadows as the container for everything. App UI made
  of stacked cards is not layout.
- A testimonial row with avatars, five stars, and quotes nobody said.
- The cookie-cutter hero: headline left, screenshot right, two buttons.
- "Get Started" and "Learn More" as the only CTAs.
- Three big numbers with tiny labels under the hero.
- A grid of cards with the same shape and the same icon slot. Content of unequal
  weight given equal boxes.
- Frosted-glass panels with blurred backdrops as the default surface.
- Generated SVG doodles and mascots in place of art direction.
- Every secondary action in a modal.
- Sparklines, progress rings, and fake avatars filling space.
- Dark because it is a dev tool, light because it is health. The use scene
  decides, not the category.
- Only the happy path is designed. Empty, loading, error, and long-content states
  are part of the component.

**Polish-level tells, note but do not grade:** monotonous spacing, bounce easing,
pulsing dot, blinking cursor, numbered section labels, em-dash overuse,
extreme negative tracking, thin border with wide shadow, repeating-stripe
gradient, grid background costume, image hover transform, monospace as costume,
unthemed browser surfaces.

### 7.10 Performance as Design (6)

- LCP under 2.0s for web apps, under 1.5s for informational sites
- CLS under 0.1 (no visible layout shift during load)
- Skeleton quality: shapes match real content, shimmer
- Images: lazy loading, width and height set, WebP or AVIF
- Fonts: `font-display: swap`, preconnect to CDN origins
- No visible font swap flash on critical fonts

---

## 8. Phase 4 - Interaction Flow Review

Walk 2-3 key flows and judge the feel, not only the function. For each:

- **Response feel:** does the click feel responsive? Any delay with no loading state?
- **Transition quality:** intentional, generic, or absent?
- **Feedback clarity:** did the action clearly succeed or fail, immediately?
- **Form polish:** focus states visible, validation timing correct, errors near
  the source?

Narrate in first person ("I click Sign Up... still spinning after 3 seconds"),
naming each element, position, and visual weight.

### Goodwill Reservoir

Start at 70/100. The number is a heuristic; the drains and fills are the finding.

| Drain | Delta |
|---|---|
| Hidden information the user wants (pricing, contact, shipping) | -15 |
| Interstitial, splash screen, or forced tour | -15 |
| Format punishment (rejecting dashes in a phone number) | -10 |
| Unnecessary information request | -10 |
| Sloppy appearance | -10 |
| Each ambiguous choice | -5 |

| Fill | Delta |
|---|---|
| Top tasks obvious | +10 |
| Graceful error recovery with a specific fix | +10 |
| Upfront about costs and limits | +5 |
| Each saved step (direct link, smart default, autofill) | +5 |
| Apologizes when something goes wrong | +5 |

Below 30 = critical UX debt. 30-60 = needs work. Above 60 = healthy. File the
biggest drains and fills as findings.

---

## 9. Phase 5 - Cross-Page Consistency

- Navigation bar consistent across pages?
- Footer consistent?
- Component reuse, or the same button styled differently on two pages?
- Tone consistent (one page playful, another corporate)?
- Spacing rhythm carries across pages?

---

## 10. Scoring

### Dual headline

- **Design Score A-F** - weighted average of the ten categories
- **AI Slop Score A-F** - standalone grade with a one-line verdict

### Per-category grades

| Grade | Meaning |
|---|---|
| A | Intentional and polished |
| B | Solid, minor inconsistencies |
| C | Functional but generic, no point of view |
| D | Noticeable problems, feels careless |
| F | Actively hurts the user |

### Computation

Each category starts at A. Each **high** finding drops one letter grade. Each
**medium** finding drops half a letter grade. **Polish** findings are noted and do
not change the grade. Floor is F.

### Weights for Design Score

| Category | Weight |
|---|---|
| Visual Hierarchy | 15% |
| Typography | 15% |
| Spacing and Layout | 15% |
| Color and Contrast | 10% |
| Interaction States | 10% |
| Responsive | 10% |
| Content Quality | 10% |
| AI Slop | 5% |
| Motion | 5% |
| Performance Feel | 5% |

AI Slop is 5 percent of the Design Score and is also graded independently as a
headline metric. Report both; do not average them into one number.

### Regression output

When a previous baseline exists, compare per-category deltas, new findings, and
resolved findings. A detector delta is only meaningful when the scan mode and the
scanned target set both match; otherwise say "modes differ, no delta" rather than
reporting a false improvement.

Live pages jitter. Treat detector counts as advisory; the signal is rule ids
appearing and disappearing, not the raw total.

---

## 11. Repair loop (Phase 8)

Bounded, one concern per commit.

1. **Locate source.** Find the file responsible for the finding.
2. **Fix minimally.** Smallest change that resolves the finding. CSS-only changes
   are low risk and reversible; component code counts against the risk budget.
3. **Commit.** `style(design): FINDING-NNN <what changed>`.
4. **Re-verify.** Reload, re-screenshot, confirm the finding is gone and nothing
   adjacent broke.
5. **Classify.** Fixed and verified, fixed best-effort, or deferred.
6. **Self-regulate.** Hard cap 30 fixes. If the accumulated risk exceeds a
   sensible threshold, stop and report.

### What never happens in the repair loop

- No refactors smuggled in as design fixes.
- No behavior changes under a `style(design)` commit.
- No weakening of tests, snapshots, or assertions to make a visual change pass.
  That is a gate edit and it needs a human (see `REVIEW_GATE_INTEGRITY.md`).
- No fix without a before and after screenshot.

---

## 12. Report shape

```
Design Score: C   AI Slop Score: D
Findings: 12 (4 high, 5 medium, 3 polish)
Fixed: 9 (8 verified, 1 best-effort)   Deferred: 3

Per category: hierarchy C, typography D, spacing B, color B, states C, ...
Top drains: [FINDING-001], [FINDING-004], [FINDING-007]
Evidence: <report dir>/screenshots/ (before/after per fix)
```

Keep the report dir out of git (gitignored), or put it under a dated report path
that is already ignored. Screenshots are evidence, not source.

---

## 13. Fleet adaptation notes

What was changed from upstream, and why:

| Change | Reason |
|---|---|
| Dropped `aside repl` script blocks and `$B` command tables | Host-specific drivers. Use whatever browser MCP the session has; the checklist is driver-agnostic. |
| Dropped the `impeccable` detector install flow | No third-party binary download over project files. Run the detector rules as judgement, or wire a local scanner if one exists. |
| Dropped `gbrain` context and telemetry calls | No fleet equivalent; would be dead calls. |
| Added hard rules on authorization, commit discipline, and gate edits | Fleet safety standards apply regardless of the source pattern. |
| Kept every checklist item and the full scoring model | This is the actual IP; trimming it would defeat the port. |

---

## 14. Related

- `GSTACK_METHODOLOGY_ADOPTION.md` - why this was ported and not installed
- `FAKEFIND_AUDIT_SOP.md` - find mocks and dead buttons (read-only)
- `GAPFIND_AUDIT_SOP.md` - find unsurfaced backend capability (read-only)
- `WEBAPP_COVERAGE_AUDIT_SOP.md` - coverage of tools and routes
- `../standards/WEBAPP_SOTA_STANDARDS.md` - the standard the grades refer to
- `../standards/REACT_HARDENING.md` - frontend hardening requirements
- `REVIEW_GATE_INTEGRITY.md` - what to do when a fix would weaken a gate
