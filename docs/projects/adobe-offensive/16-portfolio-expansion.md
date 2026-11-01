# 16 - Portfolio Expansion: Office Batch, Fit Matrix, Shared Engines, CAD Bridge

Date: 2026-10-11 (gh api read 10:20 UTC). Companion to 13 (business model),
15 (trajectories). Items marked VERIFY are from memory and must be checked
before anyone cites them.

## 1. What happened: the second batch

| Batch | Repo creation | Targets | Stars per repo (2026-10-11) |
|---|---|---|---|
| Adobe | 2026-09-30 to 10-01 | Photoshop, Illustrator, Premiere, Lightroom, Acrobat, After Effects, InDesign | 2,724 to 44,204 |
| Office + others | **2026-10-07, all same day** | Word (wordcraft), Excel (gridcraft), PowerPoint (deckcraft), AutoCAD (cadcraft), Pro Tools (soundcraft) | 1,464 to 3,777 |
| Infrastructure | 2026-10-09 | craft-launcher, **craft-libs** (shared Rust libs), craft-repo-status-app | 44 to 747 |

Reading:
- **Attention decays per batch.** Batch 2 got roughly a tenth of batch 1 per
  repo. "Free Photoshop" was news; free Word has existed since 2000
  (OpenOffice, LibreOffice, OnlyOffice, Collabora). The Office clones can only
  differentiate on familiar-by-design + native Rust + agent CLI/MCP, not price.
- **craft-libs on 10-09** is the first sign of the shared-engine move (section 4).
- cadcraft is moving fastest of batch 2: v0.4.0 on 10-10, v0.5.0 on 10-11,
  241 open issues.

Baseline for the 2026-10-15 weekly delta: wordcraft 3,777 / soundcraft 1,464 /
deckcraft 1,586 / cadcraft 2,104 / gridcraft 2,099 / craft-launcher 747 /
craft-libs 69 / photocraft 44,204.

## 2. "Excel is primitive": half true

Easy: grid, formula parser, documented formats. ECMA-376 (OOXML) is an open
standard, and Microsoft publishes the binary/legacy format specs ([MS-XLS],
[MS-XLSX], [MS-DOC] etc.) under its Open Specification Promise (VERIFY current
scope). If so, the legal footing for Office is BETTER than for Adobe: the
vendor has publicly covenanted not to sue implementers of the formats.

Hard (what LibreOffice still misses after 25 years):
- Exact semantics of 500+ functions, including deliberate legacy bugs (1900
  leap year), floating-point display rules, recalc order, volatile functions.
- Dynamic arrays/spill, LAMBDA, LET, structured references, pivot tables,
  charts, conditional formatting, data validation.
- VBA, Power Query, external links, add-ins.
- Round-tripping real corporate workbooks with zero diff.

Excel's moat is not the UI, it is the installed base of business workbooks
that must open identically. 90 percent fidelity is unusable for exactly the
people who would switch. Gridcraft lives or dies on a round-trip corpus (cf.
photocraft-corpus and the 134/135 PSD claim). Watch for a `gridcraft-corpus`.

## 3. Fit matrix: what the CUA-reversal method can and cannot take

### Good fit (local desktop app, observable UI, documented or reversed formats, rent-extracting vendor)
Visio, Microsoft Project, **Access** (millions of orphaned business DBs,
underrated), SketchUp, CorelDRAW, SPSS/Stata, Tableau/Power BI Desktop,
Publisher (discontinued by Microsoft, VERIFY date), OneNote (local notebook
format), QuickBooks-class accounting (but per-country tax liability).

### Weak fit (value is not the desktop UI)
- Network/server apps: Teams, Outlook-as-Exchange-client, Slack, Dropbox. The
  client is cloneable; the value is the network or the server.
  - **2026-10-14 override — LookCraft:** the Outlook rating is appealed in
    `18-lookcraft-prd.md` §3 (EWS death 2026-10-01, PST lock-in is client-side,
    mail is standards-heavy). Appeal stands only while those three facts hold;
    re-score on the 15 monthly cadence. Teams/Slack/Dropbox ratings unchanged.
- Math-kernel apps: SolidWorks/Parasolid, MATLAB toolboxes, Mathematica, ANSYS.
  Behavior is observable; numerical kernels take decades. FreeCAD (OCCT) and
  Octave show where behavioral parity stalls.
- OS-level: ReactOS has been "almost there" for 25+ years for good reasons.

### Bad fit (do not, and say so)
- **"safetycraft" (antivirus/EDR)**: value is threat intel, signature feeds,
  signed kernel drivers, incident response. A vibe-coded AV that misses
  detections is worse than none; liability lands on users.
- **"gamescraft"**: games are mostly expression (art, levels, music, story),
  exactly what copyright protects. Functional cloning does not help; engines
  are covered (Godot, Bevy).
- Regulated (tax filing, medical, payroll), DRM- or anti-cheat-dependent,
  anything whose value lives behind circumvention (reversal-targets Tier 3).

## 4. Shared-engine thesis: suites, not apps

Every new app that does not reuse an engine is linear maintenance debt. Five
engines carry the whole portfolio:

| Engine | Apps |
|---|---|
| Text layout + typesetting (shaping, hyphenation, flow, fonts) | wordcraft, deckcraft, designcraft, pdfcraft |
| Raster/vector canvas (GPU compositor, color management) | photocraft, vectorcraft, effectcraft, lightcraft |
| Timeline + media (decode, sync, effects graph) | filmcraft, soundcraft, effectcraft |
| Calculation graph (dependencies, recalc, formulas) | gridcraft, a future Project/Access clone |
| 2D/3D geometry (snaps, constraints, kernels) | cadcraft, vectorcraft, future SketchUp-class |

That is how Microsoft built Office. craft-libs (and craft-fonts) are the start.
Recommendation to watch for in their repos: engine crates with their own test
corpora, and apps shrinking to UI shells. If instead each app keeps its own
text/canvas stack, expect scenario G (fizzle) in 15.

Weekly new-clone drops make sense as a community vote ("tell us what to
rebuild next"), not as a release cadence. One app at professional daily-driver
quality converts stars into users; twelve alphas do not.

## 5. The "-craft" suffix: strong brand, mined namespace

Strength: craftsmanship, honest tools, productive people, the drudge-work of
the office mines dignified as craft. Works for any work tool.

Collisions (ALL VERIFY before citing):
- **Soundcraft**: long-established pro audio mixing-console brand (Harman,
  owned by Samsung). Identical name, same audio market as the DAW clone.
  The clearest trademark exposure in the portfolio, worse than anything
  Adobe holds.
- **Lightcraft**: Lightcraft Technology makes virtual-production tools for film
  (same industry as ArtCraft).
- **Minecraft / Warcraft / StarCraft**: all Microsoft-owned (Mojang, Activision
  Blizzard). A "gamescraft" next to an Office-clone campaign opens a second
  front with the same legal department.
- Also occupied: Craft Docs (craft.do), Craft CMS, Google's Wordcraft (AI
  writing research).

NOTICE protects his marks; it does not clear him against prior marks.
Every new -craft name needs a trademark search per jurisdiction and class.

## 6. CAD: the fleet already holds the other half

cadcraft (read 2026-10-11, v0.5.0) is a **2D AutoCAD-workflow clone**:
command line with keywords and `@d<a` entry, snaps, polar/ortho, layers,
dimensions, hatches with islands, blocks/attributes, paper space + PLOT to PDF.
Files: DXF read R12-2018 / write R2000; DWG read via the `acadrust` library,
write R2000; SVG/PNG export. Entities it does not model are dropped on save.
Crate layering: ui-egui front end, `mcp` crate, apps cadcraft / cadcraft-cli /
cadcraft-web. **It ships its own MCP server**: `cadcraft-cli mcp` (stdio,
headless, or `--connect 127.0.0.1:7979` to a running desktop app) with tools
including `command_line`, `execute` (any command as JSON), `screenshot`,
`ui_click`. No 3D solids, no BIM/IFC, no FEM/CFD.

Fleet components (read 2026-10-11):

| | cadcraft (upstream) | qcad-mcp (fleet) | freecad-mcp (fleet) |
|---|---|---|---|
| Scope | 2D drafting UI, interactive | 2D DXF depot + analysis, headless | 3D, BIM/Arch/IFC, FEM (CalculiX), CFD (OpenFOAM, FluidX3D), 3D print |
| Engine | Rust, acadrust for DWG | ezdxf (MIT), optional QCAD Pro | FreeCAD 1.1.x (OCCT) |
| Agent surface | own MCP: command_line/execute/screenshot/ui_click | 42 plan_* tools incl. plan_analyse (rooms, doors, windows, areas), plan_wall_data (BIM-ready JSON), plan_extrude (walls to STL), plan_beam_analysis (2D FEM), plan_convert DXF/DWG | 46+ tools incl. step_to_stl, cfd_run_solver, Arch/IFC |
| Unique | the familiar drafting UX | depot + room/wall semantics | physics, BIM, ML surrogate pipeline |

Conclusion: **do not build a fleet cadcraft. Compose.** The overlap is only
qcad-mcp's drawing-creation tools vs cadcraft's drafting; everything
downstream of a drawing is fleet-only.

### Pipeline (DXF as the interchange, no code sharing needed)

```text
cadcraft (human or agent drafts; cadcraft-cli mcp)
  -> DXF R2000 into qcad-mcp depot
     -> plan_analyse / plan_wall_data  (rooms, areas, walls as JSON)
        -> plan_extrude (quick STL)  or  freecad-mcp Arch/IFC (real BIM)
           -> freecad-mcp FEM (CalculiX) / CFD (OpenFOAM, FluidX3D on the 4090)
              -> blender / godot / resonite / unity for visualization
```

The pitch nobody else can make: "AutoCAD workflow, free, with structural and
airflow simulation of the floor plan you just drew, driven by one agent."

### Concrete steps (none started)

1. Smoke-test `cadcraft-cli mcp` in Claude Desktop/Code: draw, save DXF,
   export PNG. Record tool list and stability. Third-party alpha install needs
   Sandra's go (same rule as 0.2 in HANDOVER).
2. Round-trip test: cadcraft DXF R2000 -> qcad-mcp `plan_info` / `plan_analyse`
   on `examples/apartment.dxf` from the cadcraft repo. Log which entities
   survive (MTEXT, TABLE, MULTILEADER, hatches, dimensions) in both directions.
3. qcad-mcp: add cadcraft as an optional drafting backend next to QCAD Pro,
   or simply document the pairing in its README (prefer docs first).
4. freecad-mcp: confirm Arch import path for qcad `plan_wall_data` JSON.
5. Copy cadcraft's trademark disclaimer pattern ("Autodesk, AutoCAD and DWG are
   trademarks of ... not affiliated ... used only to describe compatible
   workflows and file formats") into fleet READMEs that name vendors.
6. Licensing note: no code moves between projects (DXF only). FreeCAD is LGPL,
   QCAD community is GPLv3, ezdxf MIT, Crafts MIT/Apache. Keep it that way;
   pipe files, do not vendor code.

### Doc drift found while reading

`projects/CAD_FLEET_COMPETITIVE.md` (2026-05-28) lists qcad-mcp ports
10966/10967 and 7 tools; qcad-mcp README says 11966/11967 and 42 tools.
Check `operations/WEBAPP_PORTS.md` for the truth and fix the stale doc. NOT
fixed in this session.

## 7. What next for him (opinion, ranked)

1. Finish one: photocraft to pro daily-driver, with corpus-backed parity
   numbers. Converts attention into users before it decays further.
2. Engines: craft-libs as real shared crates (section 4).
3. Office fidelity corpora (gridcraft/wordcraft round-trip suites); publish
   numbers like 134/135.
4. Access and Visio before more creative apps: orphaned business data, weak
   FOSS incumbents, enterprise interest (feeds the migration story in 15 sec 5).
5. Trademark clean-up (soundcraft first).
6. Not: security, games, regulated software.
