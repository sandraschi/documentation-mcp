# FastMCP 3.1 Skills: Who Provides Them and How They Work

## Who runs the skill provider?

**Not Anthropic.** The **Skills Provider** is a feature of **your MCP server**. When you add `SkillsDirectoryProvider(roots=[path])` to your FastMCP server, that server exposes the folders under `path` (each containing a `SKILL.md`) as MCP **resources** with URIs like `skill://skill-name/SKILL.md`. Clients (Cursor, Claude Desktop, Glama, etc.) that support MCP call `list_resources()` and `read_resource(uri)` on **your** server and get the skill content. There is no central “Anthropic skill repository” in this picture—each server exposes its own bundled or configured skills.

## Is there a big repository to select/download/install skills?

**Not in FastMCP itself.** FastMCP only defines how a server exposes skills as resources. A **separate** concept is a **skill catalog or marketplace** (e.g. a website or app where you browse skills from many sources and “install” them by copying into `~/.claude/skills/` or Cursor’s skills folder). Such catalogs (e.g. ClawHub, or a custom “Skills Hub” app) are built on top of MCP or other distribution mechanisms; they are not part of the FastMCP Skills Provider.

## Skills page in this webapp

This webapp’s **Skills** page is a **UI for this server’s skills only**. It lists the skills that the Docs MCP server exposes (from `src/docs_mcp/skills/`), shows name/description and full content, and provides **Copy** / **Download** and **install instructions** (e.g. “Save to `~/.claude/skills/<name>/SKILL.md`” for Claude, or Cursor’s path). It does not browse a global repository; it helps users see and install the skills that **this** server bundles.

## Summary

| Question | Answer |
|----------|--------|
| Who runs the skill provider? | Your MCP server (this one). Not Anthropic. |
| Central skill repository? | Not part of FastMCP. Catalogs/marketplaces are separate products. |
| What does the Skills page do? | Lists this server’s skills, view/copy/download, and install instructions for Claude/Cursor. |
