# FakeFind Audit SOP (SOTA 2026)

**Purpose**: Systematically audit a webapp for hardcoded mock data, dead UI, fake stats, placeholder content, and "gaslights" — things that pretend to work but don't.

**Established**: 2026-07-25
**Updated**: 2026-07-26 — Cross-linked to new-repo gate: **no undeclared mocks** (`TESTING_GUIDE.md` § Declared doubles). FakeFind is the webapp audit; the gate also covers pytest/API silent fakes.

**Reference fix**: `advanced-memory-mcp` — 18 files, 49 issues (ControlRoom, SkillStudio, Dashboard, Settings, Skills, etc.)

## Severity Classification

| Level | Definition | Examples |
|-------|------------|----------|
| **CRITICAL** | Misleads user into thinking a feature exists | Fake progress bars, mocked API responses with fabricated data, fake save dialogs |
| **HIGH** | Dead UI that wastes user time | Buttons with no onClick, panels that always show "processing" with setTimeout, fake stats displayed as real |
| **MEDIUM** | Placeholder content with no data source | Hardcoded version strings, empty panels with no API integration, default values that are never persisted |
| **LOW** | Cosmetic/decorative fakery | Marketing text, decorative badges, always-green status indicators |

## Audit Phases

### Phase 1: API Service Scan

Check `src/services/api.ts` (or equivalent) for:

- **Mock returns**: Methods that return `{ success: true, data: [] }` without making any HTTP request
- **Fake success**: Catch blocks that return `{ success: true, data: {...} }` with fabricated data when the API is actually down
- **Simulated delays**: `await new Promise(r => setTimeout(r, N))` pretending to be an API call
- **Hardcoded provider lists**: Methods that return hardcoded config without probing the backend

### Phase 2: Page Component Scan

For every page in `src/pages/` (or equivalent), check:

- **`useState` initialized with mock data**: e.g. `const [data, setData] = useState([{id: "1", ...}])` with fabricated entries
- **`setTimeout` simulating API calls**: `setTimeout(() => { setData([...fake...]); setLoading(false); }, 1500)`
- **`setInterval` for fake progress**: `setInterval(() => { setProgress(p => Math.min(p+2, 100)) }, 50)` without any backend work
- **`defaultValue` / `defaultChecked` without persistence**: Form fields with hardcoded defaults that are never saved to any backend
- **Hardcoded version strings**: `"v1.3.0"`, `"2.14.3 Compatible"` in rendered JSX
- **Fake stats**: `"1247 Notes Integrated"`, `"84%"`, `"98.4% Integrated"` that don't come from any API
- **Marketing fluff**: `"Zero Crash"`, `"Bulletproof Design"`, `"System Online"` badges

### Phase 3: Button/Interaction Audit

For every `<button>` and clickable element:

- **Dead buttons**: `<button>` with no `onClick`, or `onClick={() => {}}`, or `onClick={() => console.log(...)}`
- **Dead links**: `<Link to="">` with empty or `#` target
- **Dead toggles**: Filter/sort controls that update local state but never actually filter or sort data
- **Fake navigation**: Buttons that look like links but aren't wrapped in `<Link>` or don't have `onClick`

### Phase 4: Data Flow Audit

Trace data sources for all rendered dynamic content:

- If a value comes from `useState` initialized inline, it's fake
- If a value has a hardcoded `|| "fallback"` that's shown instead of an error state, flag it
- If a component shows content before any API call completes, flag it

## Remediation Rules

| Severity | Action |
|----------|--------|
| CRITICAL | Remove fake data. Replace with honest empty state or wire to real API. Must fix. |
| HIGH | Wire dead buttons to real routes, remove fake progress animations, replace with simple loading or disabled state. Must fix. |
| MEDIUM | Replace hardcoded fallbacks with `"—"` or honest empty states. Fix if trivial. |
| LOW | Report but do not fix unless the fix is a one-line change. |

### Honest Empty State Template

```tsx
<div className="text-center opacity-40">
  <Icon className="h-12 w-12 mx-auto mb-4" />
  <h3 className="text-lg font-bold mb-2">Not Yet Available</h3>
  <p className="text-sm text-muted-foreground">
    This feature requires a backend API that has not been connected yet.
  </p>
</div>
```

### Wiring Dead Buttons

If the target page exists:
```tsx
import { Link } from "react-router-dom";
<Link to="/notes" className="btn">Go to Notes</Link>
```

If the target doesn't exist, remove the button.

## Report Format

Write to `reports/fakefind-{repo}-{date}.md`:

```markdown
# FakeFind Audit: {repo}
**Date**: {date}

## Summary
- Total issues: N
- CRITICAL: N, HIGH: N, MEDIUM: N, LOW: N
- Files affected: N

## Findings

### {severity}: {file}:{line} — {description}
**What**: {what it shows/does}
**Fix**: {what was done}

...

## Fixed Items
- [ ] {file}: {description}

## Remaining Items (not fixed)
- {file}: {description} (reason: {why not fixed})
```

## Reference Implementation

The first fleet-wide FakeFind was run against `advanced-memory-mcp` on 2026-07-25:

| File | Finding | Severity | Fix |
|------|---------|----------|-----|
| ControlRoom.tsx | Entirely fake mock data with setTimeout(1500) | CRITICAL | Replaced with honest empty state |
| SkillStudio.tsx | Fake progress interval, fake "356 lines generated" | CRITICAL | Replaced with "not available" state |
| Settings.tsx | Fake save via setTimeout(1000) | CRITICAL | Removed save button, saved settings wiring |
| Skills.tsx | 750+ lines of hardcoded mock skills | CRITICAL | Removed mock fallback, shows empty state |
| Dashboard.tsx | Fake "GPT-4o", "1247 Notes", dead buttons | HIGH | Replaced with "—", wired buttons to routes |
| api.ts | getRecentResearch/getRecentSkills return fake data | MEDIUM | Removed try/catch noise |
| ResearchLab.tsx | Hardcoded gap analysis scores | MEDIUM | Replaced with empty state |
| Apps.tsx | Wrong port numbers | MEDIUM | Fixed to correct fleet ports |

## Verification

After fixing, run:
```bash
npx tsc --noEmit  # TypeScript check
# Also check for remaining patterns
rg -n "className=\"[^\"]*\binput\b[^\"]*\"" src/  # No bare input class
rg -n "setTimeout|setInterval" src/pages/  # Review timers
rg -n "mock|fake|placeholder" src/ --include="*.tsx" -i  # Review suspicious naming
```
