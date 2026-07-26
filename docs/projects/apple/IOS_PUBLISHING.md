# iOS Development Setup & Publishing

**Status**: PLANNING  
**Date**: 2026-05-29  
**App**: CalFolio (working title ÔÇö see [CALFOLIO.md](./CALFOLIO.md#naming))  
**Fleet backend**: calibreops MCP (port 10750)

---

## Repo Location

The Xcode project lives on the **Mac** ÔÇö not D:\\Dev\\repos.

| Location | What lives there |
|----------|-----------------|
| `~/Developer/calfolio/` (Mac) | Xcode project, Swift sources, derived data |
| `sandraschi/calfolio` (GitHub) | Remote ÔÇö same fleet GitHub as all other repos |
| `D:\\Dev\\repos\\calfolio\\` (Windows, optional) | Clone for doc editing only ÔÇö cannot build from here |

Xcode's build system, simulators, code signing, and derived data are Mac-local
infrastructure. The GitHub remote is the canonical source; clone wherever useful.

Add to fleet index: `D:\\Dev\\repos\\mcp-central-docs\\projects\\FLEET_INDEX.md`
when repo is created.

### Dev loop

```
Mac (Xcode) ÔöÇÔöÇTailscaleÔöÇÔöÇÔû║ Fleet server ÔöÇÔöÇÔû║ calibreops :10750
     Ôöé
     Ôû╝
iPad (TestFlight / cable sideload)
```

Tailscale is already on Mac and PC ÔÇö iPad connects to fleet server the same way
in development as in production. No special test config needed.

---

## Scaffolding ÔÇö Do It Now

Not too early. Creating the repo skeleton now:
- Captures architecture decisions before context fades
- Gets CLAUDE.md / AGENTS.md in place so any AI coding session starts with context
- Forces the name decision (required for App Store Connect later)
- Costs nothing to have an empty Xcode project placeholder

### What to scaffold now (before opening Xcode)

```
calfolio/                       ÔåÉ repo root
Ôö£ÔöÇÔöÇ README.md                   ÔåÉ concept + status
Ôö£ÔöÇÔöÇ CLAUDE.md                   ÔåÉ Claude Code context
Ôö£ÔöÇÔöÇ AGENTS.md                   ÔåÉ Codex / agent context
Ôö£ÔöÇÔöÇ INSTALL.md                  ÔåÉ "how to build from source" (for contributors)
Ôö£ÔöÇÔöÇ .gitignore                  ÔåÉ Swift/Xcode gitignore
Ôö£ÔöÇÔöÇ docs/
Ôöé   Ôö£ÔöÇÔöÇ ARCHITECTURE.md         ÔåÉ fleet connectivity, data flow
Ôöé   Ôö£ÔöÇÔöÇ CALIBREOPS_API.md       ÔåÉ which endpoints the app uses
Ôöé   Ôö£ÔöÇÔöÇ EPUB_READER.md          ÔåÉ copy from mcd projects/apple/EPUB_READER.md
Ôöé   ÔööÔöÇÔöÇ PUBLISHING.md           ÔåÉ link to this doc
ÔööÔöÇÔöÇ CalFolio/                   ÔåÉ Xcode project (created on Mac in Xcode)
    ÔööÔöÇÔöÇ (Xcode generates this)
```

### Xcode project creation (on Mac, one-time)

```
Xcode ÔåÆ New Project ÔåÆ App
  Product Name: CalFolio (or chosen store name ÔÇö see CALFOLIO.md naming)
  Team: your Apple Developer account
  Bundle ID: at.schipal.calfolio (or chosen)
  Interface: SwiftUI
  Language: Swift
  Storage: None (use SwiftData later if needed)
Save to: ~/Developer/calfolio/  (the cloned repo root)
```

Then push the generated Xcode project files to GitHub.

---

## Apple Developer Program

**Cost**: $99 USD/year ÔÇö no way around it for TestFlight or App Store.  
**Enrol**: [developer.apple.com/programs/enroll](https://developer.apple.com/programs/enroll/)  
**Time**: Usually approved same day with existing Apple ID in good standing.

Required before: uploading any build, TestFlight, or App Store submission.  
Not required for: Simulator testing, cable sideload to your own device (free provisioning).

---

## Beta Publishing via TestFlight

### Internal testing (up to 25 devices)

- Available **immediately** after upload ÔÇö no Apple review
- Add testers by Apple ID in App Store Connect
- Good for: your own iPad, trusted friends
- Limit: 25 devices, must be named in your developer account

### External testing (up to 10,000 testers)

- Requires **TestFlight review** ÔÇö lightweight, typically 1ÔÇô2 days
- Share via public link or email invitation
- Testers install **TestFlight app** (free, App Store), tap your link ÔÇö done
- Good for: MobileRead community post, wider beta

**This is the target for the first public beta.**

### The upload flow

```
Xcode
  ÔåÆ Product ÔåÆ Archive
  ÔåÆ Distribute App ÔåÆ App Store Connect
  ÔåÆ Upload

App Store Connect (appstoreconnect.apple.com)
  ÔåÆ Your app ÔåÆ TestFlight tab
  ÔåÆ Create group (e.g. "MobileRead Beta")
  ÔåÆ Add build
  ÔåÆ External Testing ÔåÆ Submit for review
  ÔåÆ Share public link when approved
```

---

## App Store Connect Setup (do when enrolling)

1. Create app record: Apps ÔåÆ (+) ÔåÆ New App
2. Bundle ID must match Xcode project exactly
3. Set **Primary Language**, **Category** (Books), **SKU** (internal reference)
4. Pricing: set to paid ($4.99) or free later ÔÇö can change before release

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
| **Tome** | Heavy book ÔÇö clear meaning | Check App Store |

Search the App Store before committing ÔÇö names aren't unique but close matches cause confusion.

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

From calibreops documentation ÔÇö these cover the core Calibre Companion feature set:

| Feature | calibreops tool | Operation |
|---------|----------------|-----------|
| Book list / grid | `query_books` | list, filter by author/series/tag |
| Book detail | `query_books` | get single book metadata |
| Series browser | `manage_series` | list series, books in series |
| Author browser | `manage_authors` | list authors |
| Tag browser | `manage_tags` | list tags, filter |
| Download file | `manage_files` | get file path ÔåÆ serve via HTTP |
| Search | `calibre_metadata_search` | full-text + metadata search |
| "What to read next" | `rag_retrieve` | semantic recommendation |
| Reading stats | `reading_statistics` | pages read, time, history |
| Library switch | `manage_libraries` | list + switch libraries |

The calibreops FastAPI bridge already exposes these ÔÇö define the Swift API client
against the actual endpoint responses (probe with curl first).

---

## Timeline Sketch

| Phase | Scope | When |
|-------|-------|------|
| Scaffold | Repo, name decision, Xcode project created on Mac | This week |
| Prototype | Book grid over Tailscale, one calibreops endpoint | Weekend |
| Alpha | Browse + download working on own iPad | 2ÔÇô3 weeks |
| Beta | TestFlight external, MobileRead post | 4ÔÇô6 weeks |
| App Store | Submission after beta feedback | 2ÔÇô3 months |

Realistic AI-assisted solo dev timeline ÔÇö days not weeks for each phase.
