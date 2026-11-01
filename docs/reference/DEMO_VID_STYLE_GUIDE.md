# Repo Demo Video Guide — what to show and how

A good demo video answers one question in 60-90 seconds: *"What does this thing do and why should I care?"* It's not a feature list, not a tutorial, not a talking-head monologue. It's a **walkthrough that builds desire**.

## Structure (60-90 seconds)

| Time | Phase | What happens |
|------|-------|-------------|
| 0-5s | **Title card** | Repo name, one-line value prop. No "welcome to my tutorial" intros. |
| 5-35s | **The hook** | Show the webapp in its most impressive state — dashboard with live data, tool running, output visible. Don't start at an empty login screen or a blank editor. |
| 35-65s | **The flow** | Click through 2-3 core interactions. Show the cause and effect: click button → see result. This proves it actually works. |
| 65-85s | **The closing** | Final state showing the value (a completed task, a rendered asset, a populated list). Call to action: "Install in one command," "Star on GitHub." |
| 85-90s | **End card** | Repo name, one command install, link. |

### The "sandwich" rule

Open with the most impressive thing the repo can do. Close with it too. The middle is the proof that it wasn't staged.

- **Bad:** Start at `localhost:3000` empty page → click around for 45s → show a half-working feature → end abruptly.
- **Good:** Start with the dashboard showing real KPIs → explain what they mean → click into a detail view → show the result → end on the same dashboard with updated data.

## Choreography principles

### Pacing

| Step type | Recommended duration | What to avoid |
|-----------|---------------------|---------------|
| Title card | 4-5s | Text that takes longer to read than the card lasts |
| Page load transition | 2-3s wait | Cutting before the page renders (Vite SPA needs a moment) |
| Narration per step | 3-6s per say: | Droning on — keep it to one sentence per step |
| Click/then show result | 2s wait after click | Clicking and immediately narrating the next thing — show the effect |
| End card | 4-5s | Ending abruptly at the last click |

### Narration voice

- **Factual, not salesy.** "Blender MCP gives Claude tool control over your 3D scenes" not "Revolutionize your 3D workflow with AI-powered magic."
- **One idea per say: segment.** If a step needs two sentences, split into two steps with the same action but different narration.
- **Read the screen.** Narrate what's visible. Don't describe something the viewer can't see yet.

### Step sequence anti-patterns

| Anti-pattern | Why it fails | Fix |
|-------------|--------------|-----|
| 6x `goto` steps in a row | Shows page navigation, not product value. Looks like clicking through a sitemap. | Replace 3 of the `goto`s with clicks that trigger actions. |
| Narrating the sidebar | "Here we have the navigation panel with 8 options" | Show the content, not the furniture. |
| Blank/error page visible | Destroys trust instantly — viewer assumes the repo doesn't work. | Add content-gate detection that aborts the recording. |
| 120-second video of typing | Nobody wants to watch someone type. | Skip to the result. Use `pre_steps` for "type this, then show." |
| Voiceover that doesn't match the screen | Confusing — viewer can't map audio to visual. | Record the steps first, add narration afterward, sync to timestamps. |

## What to show per repo type

### Webapp dashboards (arxiv-mcp, email-mcp, depot-mcp)

1. Dashboard with live KPIs (backend connected, tool count, status dots)
2. Click into a detail view (paper detail, email thread, file entry)
3. Show a tool result (search query returning results, action completed)
4. End on the same dashboard — data should be updated

### Host app wrappers (blender-mcp, resonite-mcp, vroidstudio-mcp)

1. Show the webapp dashboard first (proves the MCP bridge works)
2. Capture the desktop host app showing the effect of an MCP tool call
3. Back to the webapp showing the result logged
4. The contrast between complex host UI and simple webapp is your value

### Developer tools (git-github-mcp, filesystem-mcp, docker-mcp)

1. Show a terminal/CLI or webapp executing a complex operation
2. Show the result (diff output, file tree after operation, container running)
3. The value is "one command instead of 15 clicks" — prove it in 2 steps

### AI/ML tools (local-llm-mcp, google-ai-mcp, comfyops-mcp)

1. Show the chat or generation interface
2. Submit a prompt
3. Show the streaming result coming in (the most impressive part)
4. Show the final output (image, text, analysis)

## Visual style

| Aspect | Recommendation |
|--------|---------------|
| Resolution | 1280×720 (not 4K — larger files, no benefit for UI recording) |
| Background | Dark theme (the webapp is dark, the recording should be too) |
| Title card | White text on dark, repo name + one-line value prop. Blender-mcp 3D title is premium; plain text is fine. |
| Subtitles | Always on — 50% of viewers watch on mute. White text with dark outline, bottom-third position. |
| Cursor | Hide it if not clicking. Show a highlight ring on clicks. |
| Transitions | None or crossfade. No star wipes, no flashy animations. |

## Technical checklist

- [ ] Target webapp is running (auto-start handles this)
- [ ] First URL is the actual frontend, not a JSON API response
- [ ] Wait times are long enough for React SPAs to hydrate (3s for initial load, 2s for navigations)
- [ ] Content gate passes (page has actual text, not blank or error)
- [ ] Voiceover exists (speech-mcp running and returning WAV, not JSON)
- [ ] Subtitles are burned in (optional, but recommended)
- [ ] Video plays from start to finish without buffering
- [ ] Final MP4 is under 5 MB for 90s at 1280×720

## Making the script

Use the [Choreography page](http://127.0.0.1:11135/?page=choreography) in demo-vid-mcp's webapp — it's a visual builder with 11 step types, global options (voiceover, music, subtitles, title card), and live YAML preview. Build your sequence, pick a target repo, and generate in one click.

## References

- [demo-vid-mcp](https://github.com/sandraschi/demo-vid-mcp) — the pipeline that makes these videos
- [Choreography page](http://127.0.0.1:11135/?page=choreography) — visual script builder
- [SCREENSHOT_CONTENT_QUALITY_PLAN.md](../operations/planning/SCREENSHOT_CONTENT_QUALITY_PLAN.md) — same principles apply to video
- [README_WEBAPP_SCREENSHOTS.md](../standards/README_WEBAPP_SCREENSHOTS.md) — screenshot standards (video extends these)
- GitHub videos worth studying: `n8n-io/n8n` (workflow automation), `sanity-io/sanity` (CMS), `calcom/cal.com` (scheduling) — all have 60s demo videos on their READMEs
