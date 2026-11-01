# iOS Development Setup & Publishing

**Private -- Sandra S. + collaborators only. Not for public distribution.**

**Status**: PLANNING
**Date**: 2026-05-29 (reaffirmed 2026-10-28)
**App**: CalFolio (working title -- see [CALFOLIO.md](./CALFOLIO.md#naming))
**Fleet backend**: calibreops MCP (ports 10720/10721)

---

## Repo Location

The Xcode project lives on the **Mac** -- not D:\\Dev\\repos.

| Location | What lives there |
|----------|-----------------|
| `~/Developer/calfolio/` (Mac) | Xcode project, Swift sources, derived data |
| `sandraschi/calfolio` (GitHub) | Remote -- same fleet GitHub as all other repos |
| `D:\\Dev\\repos\\calfolio\\` (Windows, optional) | Clone for doc editing only -- cannot build from here |

Xcode's build system, simulators, code signing, and derived data are Mac-local
infrastructure. The GitHub remote is the canonical source; clone wherever useful.

Add to fleet index: `D:\\Dev\\repos\\mcp-central-docs\\projects\\FLEET_INDEX.md`
when repo is created.

### Dev loop

```
Mac (Xcode) --Tailscale--> Fleet server --> calibreops :10720
     |
     v
iPad (TestFlight / cable sideload)
```

Tailscale is already on Mac and PC -- iPad connects to fleet server the same way
in development as in production. No special test config needed.

---

## Scaffolding -- Do It Now

Not too early. Creating the repo skeleton now:
- Captures architecture decisions before context fades
- Gets CLAUDE.md / AGENTS.md in place so any AI coding session starts with context
- Forces the name decision (required for App Store Connect later)
- Costs nothing to have an empty Xcode project placeholder

### What to scaffold now (before opening Xcode)

```
calfolio/                       : repo root
+-- README.md                   : concept + status
+-- CLAUDE.md                   : Claude Code context
+-- AGENTS.md                   : Codex / agent context
+-- INSTALL.md                  : "how to build from source" (for contributors)
+-- .gitignore                  : Swift/Xcode gitignore
+-- docs/
|   +-- ARCHITECTURE.md         : fleet connectivity, data flow
|   +-- CALIBREOPS_API.md       : which endpoints the app uses
|   +-- EPUB_READER.md          : copy from mcd projects/apple/EPUB_READER.md
|   +-- PUBLISHING.md           : link to this doc
+-- CalFolio/                   : Xcode project (created on Mac in Xcode)
    +-- (Xcode generates this)
```

### Xcode project creation (on Mac, one-time)

```
Xcode -> New Project -> App
  Product Name: CalFolio (or chosen store name -- see CALFOLIO.md naming)
  Team: your Apple Developer account
  Bundle ID: at.s.calfolio (or chosen)
  Interface: SwiftUI
  Language: Swift
  Storage: None (use SwiftData later if needed)
Save to: ~/Developer/calfolio/  (the cloned repo root)
```

Then push the generated Xcode project files to GitHub.

---

## Apple Developer Program

**Cost**: $99 USD/year -- no way around it for TestFlight or App Store.  
**Enrol**: [developer.apple.com/programs/enroll](https://developer.apple.com/programs/enroll/)  
**Time**: Usually approved same day with existing Apple ID in good standing.

Required before: uploading any build, TestFlight, or App Store submission.  
Not required for: Simulator testing, cable sideload to your own device (free provisioning).

---

## Beta Publishing via TestFlight

### Internal testing (up to 100 Apple IDs)

- Available **immediately** after upload -- no Apple review
- Add testers by Apple ID in App Store Connect
- Good for: your own iPad, trusted friends
- Limit: 100 internal testers (named Apple IDs on your team/account)

### External testing (up to 10,000 testers)

- Requires **TestFlight review** -- lightweight, typically 1-2 days
- Share via public link or email invitation
- Testers install **TestFlight app** (free, App Store), tap your link -- done
- Good for: MobileRead community post, wider beta

**This is the target for the first public beta.**

### The upload flow

```
Xcode
  -> Product -> Archive
  -> Distribute App -> App Store Connect
  -> Upload

App Store Connect (appstoreconnect.apple.com)
  -> Your app -> TestFlight tab
  -> Create group (e.g. "MobileRead Beta")
  -> Add build
  -> External Testing -> Submit for review
  -> Share public link when approved
```

---

## App Store Connect Setup (do when enrolling)

1. Create app record: Apps -> (+) -> New App
2. Bundle ID must match Xcode project exactly
3. Set **Primary Language**, **Category** (Books), **SKU** (internal reference)
4. Pricing: set to paid ($4.99) or free later -- can change before release

---

## App Name Options

Avoiding "Calibre" in the title to sidestep trademark friction:

| Name | Vibe | Available? (check) |
|------|------|--------------------|
| **Folio** | Elegant, library-adjacent | Check App Store |
| **Stacks** | Library shelves | Check App Store |
| **Quire** | Bookbinding term, distinctive | Likely clear |
| **Recto** | Right-hand page, bookish | Likely clear |
| **Gauge** | Calibre pun (calibre = bore gauge) | Very clear |
| **Large Bore** | Calibre pun, silly | Too silly |
| **Tome** | Heavy book -- clear meaning | Check App Store |

Search the App Store before committing -- names aren't unique but close matches cause confusion.

---

## .gitignore for Swift/Xcode

Standard entries to include:

```gitignore
# Xcode
*.xcodeproj/xcuserdata/
*.xcworkspace/xcuserdata/
*.xcworkspace/xcshareddata/IDEWorkspaceChecks.plist
build/
DerivedData/
*.ipa
*.dSYM.zip
*.dSYM

# Swift Package Manager
.build/
.swiftpm/

# CocoaPods (if used)
Pods/
Podfile.lock

# macOS
.DS_Store
```

---

## Calibreops Endpoints the App Will Need

From calibreops documentation -- these cover the core Calibre Companion feature set:

| Feature | calibreops tool | Operation |
|---------|----------------|-----------|
| Book list / grid | `query_books` | list, filter by author/series/tag |
| Book detail | `query_books` | get single book metadata |
| Series browser | `manage_series` | list series, books in series |
| Author browser | `manage_authors` | list authors |
| Tag browser | `manage_tags` | list tags, filter |
| Download file | `manage_files` | get file path -> serve via HTTP |
| Search | `calibre_metadata_search` | full-text + metadata search |
| "What to read next" | `rag_retrieve` | semantic recommendation |
| Reading stats | `reading_statistics` | pages read, time, history |
| Library switch | `manage_libraries` | list + switch libraries |

The calibreops FastAPI bridge already exposes these -- define the Swift API client
against the actual endpoint responses (probe with curl first).

---

## Timeline Sketch

| Phase | Scope | When |
|-------|-------|------|
| Scaffold | Repo, name decision, Xcode project created on Mac | First session |
| Prototype | Book grid over Tailscale, one calibreops endpoint | One focused weekend |
| Alpha | Browse + download working on own iPad | 2-3 weeks |
| Beta | TestFlight external, MobileRead post | 4-6 weeks |
| App Store | Submission after beta feedback | 2-3 months |

Realistic AI-assisted solo dev timeline -- days not weeks for each phase.

---
*Last updated: 2026-10-28 (ASCII cleanup, ports 10720/10721, TestFlight limits corrected). Planning doc from 2026-05-29.*
