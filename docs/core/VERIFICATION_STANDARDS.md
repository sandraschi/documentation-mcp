# Verification & Testing Standards

## 1. Visual Verification (SOTA)

All UI changes and bug fixes MUST be verified using browser automation tools.

### 1.1. Evidence Requirements
- **Screenshots**: Mandatory "before" and "after" proof for all UI work.
- **Console Logs**: Capture `browser_console_messages()` to detect silent JS errors or network failures.
- **Log Tails**: For any system or server failure, a 20-line log tail MUST be captured and attached to the bug report.
- **Recordings**: Recommended for complex workflows or animations.

### 1.2. Verification Workflow
1.  **Launch**: Open the application in the browser tool.
2.  **Snapshot**: Use `browser_snapshot()` to get an accessible tree of the UI.
3.  **Interact**: Perform actions (click, type, navigate) to exercise the logic.
4.  **Confirm**: Inspect the DOM or capture console logs to verify the result.
5.  **Evidence**: Save a screenshot or recording to the artifacts directory.

---

## 2. Browser Interaction Safety (Anti-Loop Guards)

To prevent credit-wasting loops and subagent hangs (BUG-004), all browser interactions must follow these safety protocols.

### 2.1. DOM Availability Guard (The "Existence Check")
- **Mandatory Pre-check**: Before any `click` or `type` action, the agent MUST verify that the target element exists in the DOM.
- **Crashed State Detection**: If the subagent returns a "no DOM" or "empty page" state (e.g., after a crash), the agent MUST NOT attempt blind interactions.
- **Wait Policy**: Use explicit `wait_for_selector` with a maximum timeout of **5000ms**. If it fails, abort and report the crash rather than retrying indefinitely.

### 2.2. Interactive Debugging Consent
- **Autonomous Limit**: If a page crashes during verification, the agent is allowed **ONE** attempt to refresh the page.
- **Escalation**: If the refresh fails or the page is stuck in a "DOM-less" state, the agent MUST `notify_user` and request explicit permission before attempting complex interactive recovery (e.g., manually resetting state via console).
- **Stupid-Click Prohibition**: Never "click around" on an empty or error-marked page. If the UI is not rendered, diagnostic logging is the only acceptable action.

### 2.3. Timeout Policy
- **Maximum Duration**: No single browser subagent task should exceed **300 seconds**.
- **Iteration Limit**: Limit subagent steps to **10 iterations** per task. If unresolved, return to the user.

### 2.4. Desktop UI tools are not a substitute for browser verification

**Never** use **pywinauto-mcp** or other **OS-level** UI automation MCPs to verify a **webapp** when a **browser** tool (Playwright, MCP browser, CDP) is available. Desktop automation targets **native windows** and **global focus** — wrong window → loops, IDE takeover, unsafe cursor behavior.

Fleet policy: **remove pywinauto from default IDE MCP chains**; keep browser-scoped tools only. See [WEBAPP_STANDARDS.md §7](./WEBAPP_STANDARDS.md#7-mcp-capability-boundaries-web-vs-desktop-ui) and [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md).

---

## 3. Testing Coverage

- **Unit Tests**: 80% minimum coverage using Pytest (Python) or Vitest (TS).
- **Integration Tests**: 70% minimum coverage for tool-to-application communication.
- **E2E Tests**: Mandatory for critical "happy paths" using Playwright or the Browser Tool.

## 4. Manual Verification Fallback

If automated verification is impossible (e.g., hardware-specific), provide:
- Clear, step-by-step instructions for the user.
- Expected vs. actual outcomes.
- Request for user-provided screenshots as proof.
