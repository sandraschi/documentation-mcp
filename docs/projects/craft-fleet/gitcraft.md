# GitCraft — Assessment (Retired)

**Status:** Retired / Deleted from `D:\Dev\repos` (2026-11-09) · **Grade:** Retired · **Superseded by:** `git-github-mcp` + [codercraft](codercraft.md)

## Why it was retired

Code audit on 2026-11-09 showed `sandraschi/gitcraft` (`451 LOC` Python) consisted of 6 basic `subprocess.run(["git" / "gh", ...])` wrappers (`status`, `log`, `diff`, `pr-list`, `pr-view`, `fleet-dirty`). Repository and GitHub workflows live in `git-github-mcp` and [codercraft](codercraft.md).
