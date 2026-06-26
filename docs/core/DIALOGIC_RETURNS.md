# Dialogic Returns Standard (FastMCP 3.2)

## 1. Overview

A **Dialogic Return** is a tool result that facilitates a conversational loop between the Tool and the AI Agent. Instead of a binary Success/Failure, a Dialogic Return provide context-aware suggestions and machine-readable remediation paths to prevent "Stalling" or "Stubbing" (fabricating missing code).

## 2. Payload Schema

Every fleet tool MUST return JSON structured data. On failure, it SHOULD include the `dialogic` metadata key.

```json
{
  "success": false,
  "error": "Short readable error code",
  "message": "Human-friendly explanation",
  "dialogic": {
    "suggestion": "A high-level advice string for the AI.",
    "remediation": "An explicit tool call string or search pattern.",
    "context_dump": { "useful_ids": [], "line_numbers": [] },
    "is_test_or_joke": "Optional boolean flag if the prompt likely triggered a mock path."
  }
}
```

## 3. Mandatory Implementation

### 3.1. Match Failures (Search/Replace)
If a `TargetContent` string is not found:
- **Suggestion**: "Check for exact whitespace or line-ending mismatches."
- **Remediation**: Use `read_file` with a wider line range to inspect the actual target state.

### 3.2. Missing Resources
If a file or database entry is missing:
- **Suggestion**: "The resource 'cocotheclown.md' does not exist. Verify if this was a test prompt before creating a stub."
- **Remediation**: `list_dir` or `search_web`.

## 4. Agentic Response Pattern

When an AI Agent (Antigravity, Claude Code, Cursor) receives a `dialogic` payload:
1.  **Acknowledge**: Do not hide the error.
2.  **Evaluate**: Check if the `suggestion` or `remediation` covers the failure.
3.  **Pivot**: Execute the recommended remediation instead of attempting to "correct" from internal memory.

---
*Standard: DIALOGIC-SOTA-2026-04*
*Status: ADOPTION IN PROGRESS*
