# Safety Protocols: Atomic Writes & Dual-Backups

## 1. Overview

To prevent "Stubbing" (corrupting files with partial or placeholder content) and allow instant recovery from accidental fleet-wide changes, all SOTA-compliant tools that modify the filesystem MUST adhere to this protocol.

**Git rollback (mandatory for agents):** Before any batch change under `src/`, `tests/`, or `webapp/src/`, follow [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md) — dedicated repo `.git`, initial commit, GitHub remote, and a **checkpoint commit** so `git checkout` can recover from zero-byte or mass truncates.

## 2. The Atomic Write Pattern

All writes MUST be atomic to ensure no partial files are left on disk after a crash or tool failure.

1.  **Stage**: Write the new content to a temporary "buddy file" (e.g., `.filename.tmp`).
2.  **Verify**: Perform a basic validation on the temp file (e.g., checksum or length check).
3.  **Replace**: Atomic `os.replace` or `Move-Item -Replace` to the target path.

## 3. Dual-Backup Mandate

Before the Atomic Write procedure begins, the tool MUST generate two backup artifacts:

### 3.1. Local Snapshot (Side-car)
- **Path**: `.backups/YYYY-MM-DD_HHMMSS_{filename}.bak`
- **Purpose**: Quick local diffing and manual rollback during development.
- **Retention**: Local `.backups/` directories should be `.gitignore`'d but persisted long enough for session recovery.

### 3.2. Central Fleet Archive
- **Path**: `D:\Dev\fleet_archive\backups.jsonl` (or equivalent central log)
- **Purpose**: Global traceability and recovery for cross-repository "mass-mod" operations.
- **Data**: Include the full file content (diff or snapshot), author, and the tool call that triggered it.

## 4. Remediation guidance

If any stage of the Safety Protocol fails (e.g., disk full, permission denied):
- The tool MUST NOT attempt the write.
- The tool MUST return a **Dialogic Error** (§ DIALOGIC_RETURNS.md) with explicit instructions on how to clear the lock or free space.

---
*Standard: SAFETY-SOTA-2026-04*
*Status: MANDATORY*
