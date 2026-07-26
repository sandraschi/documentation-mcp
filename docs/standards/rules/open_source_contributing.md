# FOSS Contribution Etiquette for AI-Assisted Development

**Scope**: Opening issues and PRs against third-party open-source projects (NOT our own repos).

## Core Principle

We are guests in other people's projects. Our advantage (AI speed) does not entitle us to skip their process. Every issue and PR costs a human maintainer time and attention. Spend that currency wisely.

## Before You Open

- **Search first**. Duplicate issues annoy maintainers more than anything. Search the tracker for existing issues/PRs covering the same thing.
- **Check the contribution guidelines** (`CONTRIBUTING.md`, `README`). Some projects want an issue before a PR. Some want a PR directly. Some want a discussion first. Follow their rules.
- **Check the code of conduct** if present.
- **Small ask = one issue**. A single issue covering two unrelated features forces maintainers to track two conversations. Split them.

## Issue Etiquette

- **One issue, one request**. Two features = two issues. Keeps discussion focused and allows independent accept/reject.
- **Title**: descriptive, includes the project name if cross-posting. "Feature request: --load <path> CLI flag" not "wouldnt it be nice if".
- **Body**: context → what → why → implementation sketch. No essays. 3-5 paragraphs max.
- **Implementation sketch**: reference existing code patterns (e.g. "--config was added in 3.17 in GOApp.cpp, same pattern"). Shows you've done your homework.
- **Tag**: use the project's issue labels (enhancement, feature, etc.).
- **Don't ask "when will this be done"**. It's open source. It'll be done when a maintainer has time and interest.
- **Don't mention AI in the issue**. The maintainer doesn't need to know how the code was written. The code stands on its own merits.

## PR Etiquette

- **Open an issue first unless the project explicitly allows PRs without one**. The issue is where you gauge interest before spending time on code.
- **Keep diffs small**. A 10-line PR is reviewed in 30 seconds. A 200-line PR takes an hour and may be ignored. Prefer incremental PRs.
- **Follow the project's code style**. Don't reformat existing code. Match their naming, brace style, comment style.
- **Include tests if the project has a test suite**.
- **Don't force-push after review comments**. Add fixup commits. The reviewer needs to see what changed since their last review.
- **Respond to feedback within a reasonable timeframe** (1-2 weeks). If you can't, say so and someone else may pick it up.
- **Don't close and re-PR to bypass review**. Squash and rebase if needed, but keep the PR thread intact.

## AI-Specific Rules

- **Review every line the AI generates before submission**. AI code can be subtly wrong, miss edge cases, or not match the project's style. You are responsible for every line.
- **Do not attribute the code to AI in the PR description**. The code is yours. It should stand on technical merit.
- **If asked about AI use, be honest but brief**: "I used an LLM as a coding assistant. I reviewed every line." This is only credible for small PRs. See below.
- **Small PRs only**. The "I reviewed every line" claim is believable for a 6-line `--load` flag. It is not believable for a 1000-line feature add, and asserting it damages trust. If a change is too large for a human to reasonably review line-by-line, it's too large for AI-assisted contribution. Split it.
- **AI speed does not imply maintainer speed**. A feature that took us 30 seconds to implement may take a maintainer 30 minutes to review, test, and merge. Respect that asymmetry.
- **Never apply fleet standards to foreign repos**. Do not run fleet tooling (ruff, just, SOTA standardization, CI config) on a third-party repo. The clone must be left exactly as-is except for the intended fix. Adding linter reformatting, config files, or infrastructure changes clutters the diff and wastes the maintainer's time. The diff should contain **only the fix**.
- **Issue before PR**. Always file an issue first to gauge interest. Only open a PR after the issue is acknowledged.
- **Do not merge your own PRs on foreign repos**. The maintainer merges — or doesn't. Pushing directly to their branch or auto-merging disrespects their ownership. Our job ends at the PR.

## When in Doubt

- **Watch the project's community first**. Read existing issues and PRs to gauge the maintainer's communication style and responsiveness before submitting anything.
- **A maintainer saying "no" is not a failure**. Respect their vision for their project. Fork if you must.
- **If ignored after 2 weeks, a polite ping is acceptable**. If ignored after 4 weeks, assume it's not a priority for them.
- **The project owes you nothing**. You chose to use their software. You chose to contribute. They didn't ask for either.
