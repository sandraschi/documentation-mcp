# Autodesk Fusion: the reference SolidCraft was built against, and what that means for us

**Status:** Research and Analysis Doc | **Date:** 2026-10-29
**Subject:** Autodesk Fusion (formerly Fusion 360), the commercial product whose workflow
SolidCraft tracks. Written after forking `tangency-labs/solidcraft` and cross-checking its
geometry against FreeCAD.
**Evidence base:** the SolidCraft 0.26.1 source tree at `_upstream/solidcraft`, its live
command registry (`solidcraft-cli commands`, 528 commands), its docs, and two web
verifications logged in section 9. Claims not re-verified today are marked **[background]**.

**Related documents:**
- `mcp-central-docs/patterns/CRAFT_MULTI_APP_FLOWS.md` - the family the launcher ships
- `mcp-central-docs/reference/COOL_REPOS.md`
- `freecad-mcp/scripts/solidcraft_crosscheck.py` - the two-kernel harness this doc produced
- `~/.config/opencode/skills/solidcraft/SKILL.md` - the operating skill

---

## 1. Why this document exists

Three things happened at once and only make sense together:

1. `solidcraft` was added to the ArtCraft launcher as its first **community app**, so it now
   sits in the same family as CADCraft, FigCraft, DesignCraft and the rest.
2. A reader of its Show HN thread guessed it was copying Inventor, Solid Edge or Fusion
   before anyone guessed SolidWorks. Because it is.
3. We already own `freecad-mcp`, which wraps a *different* engine (OpenCASCADE) under a
   *different* licence (LGPL) with a *different* interface (scripts, not commands).

Fusion is the product both of those are measured against, whether or not anyone says so.
If we build CAD tooling without knowing what Fusion actually is, we will keep rediscovering
its decisions as surprises.

## 2. What Fusion is, in one paragraph

A **cloud-connected, subscription, parametric 3D CAD/CAM/CAE application** from Autodesk.
Desktop app on Windows and macOS, with a limited browser client and mobile viewers. The
differentiator is not the modeller - it is that the document lives in Autodesk's cloud, the
history is server-side, the same file feeds simulation, generative design, CAM and drawings,
and collaboration is a permissions model rather than a shared drive.

**[verified 2026-10-29]** It was rebranded from "Autodesk Fusion 360" to **"Autodesk Fusion"**
in January 2024, when the "360" was dropped alongside a new pricing and packaging structure
announced in November 2023.

That rebrand matters for us: any wrapper, doc or skill that says "Fusion 360" is describing a
product name Autodesk retired two years ago. Use "Fusion".

## 3. The parts that actually shape a clone

### 3.1 Kernel lineage: ShapeManager, which is ACIS with a fork

**[verified 2026-10-29]** Autodesk ShapeManager is Autodesk's own geometric modelling kernel.
It was forked from **ACIS 7.0** (Spatial Corp) in November 2001 and first shipped in
Inventor 5.3 in February 2002. Fusion is built on it.

This is the single most important fact in this document, because it sets the technical bar
for anything claiming to replace Fusion:

- Fusion inherits 25+ years of accumulated boolean, fillet and healing work, plus a
  topological-naming scheme that mostly holds.
- OpenCASCADE (FreeCAD, and therefore `freecad-mcp`) is a contemporary of that lineage, not a
  toy, but its fillet/boolean robustness is widely reported as behind the commercial kernels.
- SolidCraft uses neither. It builds on the Rust `truck` crates, with `truck-shapeops`
  vendored and patched locally. Its own README claims 75 of 76 reference parts match
  analytic or FreeCAD-computed values.

So the kernel landscape is: ShapeManager (Fusion/Inventor) > OpenCASCADE (FreeCAD) >
truck (SolidCraft) in maturity, while Rust/WebAssembly reach runs the other way.

### 3.2 The feature timeline is the product

Fusion's defining interaction is a **linear, editable feature history** across the bottom of
the window: every sketch, extrude, fillet and pattern is a row you can double-click, edit,
suppress, reorder, or roll back past with a drag of the end marker.

Two consequences that clones must reproduce or they feel wrong:

- **Parameters are first-class.** Dimensions are expressions, and a "user parameter" is a
  named value every dimension can reference. Edit one number, the model rebuilds.
- **Design History can be switched off.** Fusion carries both a parametric mode and a direct
  modelling mode in the same document, which is why its timeline is a toggle and not a
  fixture.

SolidCraft mirrors all three: a 22-command `timeline` family (suppress, reorder, rollback),
a 13-command `parameters` family with unit-aware expressions, and 8 `config` commands.

### 3.3 Assemblies use joints, not mates

Fusion's assembly model is **components as occurrences** inside a parent design, positioned
by **joints** (rigid, revolute, slider, cylindrical, pin-slot, planar, ball) rather than by
constraint pairs. Motion links, contact sets and motion studies sit on top.

This is a genuine divergence from SolidWorks' mate-based approach and from FreeCAD's
Assembly workbenches, and it is the thing that most often breaks expectations when someone
moves between tools. SolidCraft ships `joint` (18), `motion` (11), `contact` (7) and
`occurrence` (6) command families - the Fusion model, not the SolidWorks one.

### 3.4 The ribbon and its vocabulary

Fusion's ribbon tabs are, in order: SOLID, SURFACE, MESH, SHEET METAL, PLASTIC, ASSEMBLE,
CONSTRUCT, INSPECT, INSERT, SELECT, EVALUATE. Panels inside carry names like CREATE,
MODIFY, FINISH SKETCH.

SolidCraft's live registry maps onto that almost family for family:

| Fusion ribbon area | SolidCraft command family (count) |
|---|---|
| SOLID / CREATE | `solid` (36), `face` (1), `body` (1) |
| SKETCH | `sketch` (113) |
| SURFACE | `surface` (19) |
| SHEET METAL / PLASTIC | `sheet` (13), `plastic` (7) |
| ASSEMBLE | `component` (27), `joint` (18), `occurrence` (6), `assembly` (1), `motion` (11), `contact` (7), `explode` (4) |
| CONSTRUCT | `construct` (19), `frame` (4) |
| INSPECT | `inspect` (18), `model` (3), `diagnostics` (4) |
| EVALUATE | `render` (57), `appearance` (10), `material` (8) |
| (browser tree) | `browser` (8), `selection` (1), `select` (4) |
| (timeline) | `timeline` (22) |
| (parameters) | `parameters` (13), `expr` (1), `config` (8) |

**This is the strongest single piece of evidence that Fusion, not SolidWorks, is the design
reference.** "SOLID" as a tab name and "FINISH SKETCH" as a panel are Fusion's vocabulary.
SolidWorks calls its tabs Features / Sketch / Evaluate, and its CommandManager is not a
ribbon in the same sense.

### 3.5 Navigation presets name the competitors outright

SolidCraft's default mouse navigation is Fusion's: wheel zooms at cursor, middle button pans,
right-drag orbits. Preferences then offers presets for **SolidWorks, Inventor, Alias, Maya,
Blender, Tinkercad, OpenSCAD, HFSS and Touchpad**.

That is the standard interoperability move every serious CAD app makes, and it is worth
recording accurately: shipping a "SolidWorks" preset is not copying SolidWorks. It is
acknowledging where users' muscle memory comes from.

## 4. Where SolidCraft follows Fusion, and where it deliberately does not

| Paradigm | Fusion | SolidCraft | Verdict |
|---|---|---|---|
| Sketch + constraints + dimensions | yes | own solver (Levenberg-Marquardt + rigid-cluster decomposition), 113 sketch commands | follows |
| Parametric timeline | yes | yes, editable, suppress/reorder/rollback | follows |
| Parameters as expressions | yes | yes, unit-aware | follows |
| Configurations | yes | yes (`config`, 8 commands) | follows |
| Components + joints | yes | yes | follows |
| Sheet metal | yes | yes (flanges, hems, fold/unfold, flat pattern) | follows |
| Direct modelling toggle | yes | via suppressing/rolling the timeline | partial |
| Cloud document store | yes | no - local `.sc` designs | **diverges** |
| Simulation / FEM | yes | **none** | **diverges** |
| CAM / toolpaths | yes (extensive) | **none, explicitly out of scope** | **diverges** |
| Generative design | yes, cloud + credits | none | **diverges** |
| Drawings from model | yes | DXF of the current view only | partial |
| Slicing / 3D printing | no (leaves to slicers) | no, and the author said so on HN | matches |
| File formats | native + STEP/IGES/STL/3MF | STEP/IGES/3MF/STL/OBJ/DXF/URDF, `.sc` native | comparable |
| Kernel | ShapeManager (ACIS lineage) | truck (Rust), vendored patched shapeops | **diverges** |
| Licence | subscription, proprietary | MIT OR Apache-2.0 | **diverges** |

The four "diverges" in bold are not gaps SolidCraft forgot. Cloud storage, simulation, CAM
and generative design are the revenue surface of Fusion. A local, permissively licensed,
scriptable modeller deliberately does not build them.

## 5. What "clone" means here, and what the project itself says

The word needs precision, because the honest answer is narrower than the accusation.

SolidCraft is a **clean-room reimplementation of the Fusion-class workflow**, not a copy of
Fusion. The project states this in enforceable terms, which is unusual and worth quoting
because it is the strongest evidence available to us:

- `skills/solidcraft-ground-rules/SKILL.md`: *"Do not drive, script, automate or extract data
  from commercial CAD products (Fusion, SolidWorks, Onshape, ...) for this project: no test
  data, measurements, command lists, ids or files produced with them."*
- `AGENTS.md`: no GPL/LGPL/AGPL CAD source may be read at all (OpenCASCADE, FreeCAD,
  SolveSpace, CadQuery, LibreCAD, QCAD), enforced by `cargo xtask licences --check`.
- `ATTRIBUTION.md`: **no Autodesk iconography, images, artwork, fonts, templates, materials
  or help text**; no committed screenshots of Autodesk software.
- `NOTICE` / `README`: not affiliated with or endorsed by Autodesk, Dassault, PTC or Siemens;
  the trademarks are named only to describe compatibility.
- What *was* borrowed is disclosed per file: CADCraft and GridCraft code, PhotoCraft's
  packaging.

So the accurate sentence is: **Fusion's interaction model, vocabulary and feature set, rebuilt
from public documentation and convention, with SolidWorks contributing the name and a handful
of parity notes.** The resemblance is the stated design goal; the code and assets are not
derived from Autodesk.

What none of us can rule on is trade dress or the look-and-feel question. Do not assert
either way in fleet prose.

## 6. What this means for the fleet

### 6.1 Do not treat SolidCraft as a FreeCAD replacement

| | freecad-mcp | SolidCraft |
|---|---|---|
| Engine | OpenCASCADE | truck (Rust) |
| Licence | LGPL - real friction inside a shipped `.mcpb`/NSIS product | MIT/Apache - none |
| Interface | FastMCP wrapper, script-oriented | 19 MCP tools over 528 schema-typed commands, batch with checkpoint rollback |
| Analysis | FEM, CFD, FluidX3D, BIM | none |
| Maturity | 20+ years | ~3 weeks as a public project |
| Numbers | exact | planar exact, curved faces ~1.1e-4 low (tessellation) |

They are complements. FreeCAD is the reference and the analysis engine. SolidCraft is the
agent-native, licence-clean modeller and the second opinion.

### 6.2 Use Fusion as the vocabulary, not as the spec

When writing skill prose, docs or UI copy about parametric CAD, Fusion is the mental model
users already hold (sketch, timeline, parameters, components, joints). Borrow the vocabulary.
Do not borrow the pricing model, the cloud dependency or the credits.

### 6.3 Two wedges, and only one of them is about money

An earlier draft of this section said SolidCraft's users are "mostly hobbyists and automation
people". That described its **current adopters**, who are a self-selected Hacker News crowd,
and quietly implied something about its **addressable market**, which is a different and much
larger set. Do not conflate the two. The market is anyone who needs parametric solids and
cannot or will not pay 720 EUR per seat per year in hard currency - which includes working
professionals running small machine shops, product studios, fab labs, parts and repair
businesses, small consultancies and under-funded engineering departments, not just students
and hobbyists.

That is a genuine and permanent gap. It is also older than the gap's usual explanation
suggests, so hold both halves of the picture:

**The gap is real.** A price set in EUR and applied globally excludes most small firms in
lower-income countries outright. One seat is a decision, not a purchase. And the base seat is
not the working configuration: a shop that needs 5-axis needs the Manufacturing extension, one
that needs FEA needs the Simulation extension, and neither price is published - they are
quote-only. The real small-shop cost is a multiple of 720 EUR, by an amount Autodesk does not
tell you publicly.

**But the gap has not converted.** Free alternatives have existed for over twenty years -
FreeCAD since 2002 - and the historical response to price exclusion has been **piracy**, with
FreeCAD a distant second for people who cannot or will not run cracked software. "Unhappy with
the price" has never by itself produced switching. A free price is necessary, not sufficient.

**What actually converts is price plus the things piracy cannot provide.** A cracked Autodesk
seat gets a company a working modeller and a legal liability. It does not get them an
auditable licence for a client contract, an API they can build a business process on, or a
machine that works offline under their own control. That is the buyer who most needs something
like SolidCraft: not the hobbyist who would have pirated it anyway, but the **small commercial
shop in a price-excluded market that cannot legally run cracked software** and therefore
currently either does without parametric CAD or fights FreeCAD.

### 6.4 Reconciliation: small share of Autodesk's revenue, large share of humanity

Both statements are true and they use different denominators, which is why the argument never
converges when only one is stated.

**[background, aggregator-sourced]** Autodesk's fiscal 2026 revenue was about 7.21 billion USD,
roughly 97 percent recurring. Trailing-twelve-month revenue to 30 June 2026 splits
approximately: Americas 3.41bn (44 percent), EMEA 3.06bn (39 percent), APAC 1.32bn (17 percent).

APAC is not a proxy for "Global South" - it is mostly Japan, Korea, Australia, Singapore and
China. So the genuinely price-excluded segment is a low single-digit percentage of Autodesk's
revenue. **Autodesk has little financial reason to react**, and expecting outrage or a takedown
is a category error: their incentives point at enterprise and AEC in high-income markets, which
is precisely why the gap stays open rather than closing.

That is the honest version of both claims:

- Excluded population: very large, and growing.
- Excluded share of Autodesk's revenue: small enough to ignore.
- Which means: the market is real, the incumbent will not fix it, and nobody should expect them
  to notice.

### 6.5 The automation surface is what makes this wedge different from the last twenty years

Fusion's MCP story is thin and account-bound; its scripting is cloud-era and gated. The HN
thread on SolidCraft made the same point twice: what people actually want from these apps is
**being able to drive the whole thing programmatically**, and the incumbents do not allow it
cheaply.

That is the part that is new. FreeCAD has been free since 2002 and did not convert the market.
An agent-drivable engine with 528 schema-typed commands, a batch call with checkpoint rollback,
and no account, is a different offer from "a free version of the same GUI".

So the fleet's lane is not "open-source Fusion". It is **scriptable, local, legally clean,
agent-drivable CAD that does not phone home** - which is priced at zero and costs zero
licence risk. `freecad-mcp` and the SolidCraft MCP are two bets on that, with different engines
and different licences.

## 7. Parity gaps we should expect to hit

Ordered by how soon they will bite a real task:

1. **Curved-surface precision.** SolidCraft's measurements are tessellation-derived. Any
   pipeline that adjudicates tolerances below ~2e-4 on curved parts must not use it as the
   referee.
2. **No FEM / CFD.** Any "model then analyse" loop still needs FreeCAD. This is the most
   likely reason to call both.
3. **Topological naming under edits.** Fusion's persistent-naming scheme is the result of two
   decades; a three-week-old kernel will lose face/edge references when the timeline is
   reordered. Expect repair workflows to be exercised.
4. **Drawings.** DXF of the current view is not a drawing package. TechDraw via FreeCAD
   remains the only option in the fleet.
5. **Fillet robustness.** Historically the hardest kernel problem and the one the HN thread
   flagged unprompted.
6. **Longevity.** CAD documents outlive software. Treat SolidCraft as an optional peer with
   soft degradation, never as a hard dependency, until it has survived a year.

## 8. Commercial reality, briefly

Fusion is sold as a subscription with a free personal-use tier for non-commercial work, plus
paid commercial seats and consumption-based credits for cloud compute (generative design,
simulation, cloud rendering). There is no perpetual licence.

### Verified price snapshot, 2026-10-29

Read from Autodesk's own product pages, not an aggregator. The checkout links on those pages
carry `intendedUsageCode:COM`, `accessModelCode:S`, `termCode:A01` - commercial, single-user,
1-year term - so these are per-seat commercial list prices.

| Region | List price | Per seat, per year |
|---|---|---|
| EU (EUR) - what Austria sees | 60 EUR/month, billed annually | **720 EUR** |
| US (USD) | 57 USD/month, billed annually | **684 USD** |
| Fusion for Manufacturing | not published - quote only | - |
| Fusion for Design | not published - quote only | - |
| Manufacturing / Simulation / Design / Manage extensions | not published - quote only | - |

Notes that matter when quoting this:

- **EU prices are shown excluding VAT.** Austrian VAT is 20 percent, so a Vienna business pays
  roughly 864 EUR gross per seat per year. Confirm the VAT line at checkout; this was not
  verified from the page.
- **A promotion was live on the day of checking** (12-30 October 2026, commercial copies only,
  not on renewals): 25 percent off when buying two new one-year subscriptions, 33 percent off
  for three or more, capped at 20 seats. At three seats that is about 482 EUR per seat per
  year for the first term. Do not treat it as the normal price.
- **These numbers have a shelf life.** They are a dated observation with a source, not a
  standing fact. Re-check before quoting; a stale number in a fleet doc is worse than none.
  Source: `autodesk.com/eu/products/fusion-360/overview` and
  `autodesk.com/products/fusion-360/pricing` (both redirect to the overview page, section
  "Plans and Pricing").

The structural facts that do not change:

- The document lives on Autodesk's servers; offline use is an exception, not the mode.
- Features are gated by tier, so "does it do X" is always "on which plan".
- Extensibility is API- and account-bound.
- Exit cost is real: native format, cloud history, no local-first story.

Every one of those is an argument for the thing we are building, and none of them is a reason
to pretend Fusion is bad. It is very good. That is why cloning it is interesting.

## 9. Verification log

Checked today to avoid writing from memory:

| Claim | Source | Result |
|---|---|---|
| Rebrand Fusion 360 -> Autodesk Fusion, Jan 2024 | productdesignonline.com article on the rebrand | confirmed |
| ShapeManager forked from ACIS 7.0, Nov 2001; Inventor 5.3, Feb 2002 | Wikipedia / HandWiki / Wikiwand ShapeManager | confirmed |
| Timeline warning/error behaviour in Fusion | help.autodesk.com support article | confirmed |
| SolidCraft default navigation is Fusion's model | `_upstream/solidcraft/docs/book/src/guide/ui-tour.md` | confirmed in source |
| SolidCraft ships SolidWorks/Inventor/Alias/Maya/Blender/Tinkercad/OpenSCAD/HFSS presets | same file | confirmed in source |
| SolidCraft clean-room ground rules name Fusion first | `skills/solidcraft-ground-rules/SKILL.md` | confirmed in source |
| SolidCraft command families and counts | `solidcraft-cli commands` on 0.26.1 | measured: 528 total, 417 enabled |
| SolidCraft curved-volume error ~1.128e-4, size-independent | `solidcraft_crosscheck.py` vs analytic | measured |
| Fusion commercial price, EU and US, per seat per year | autodesk.eu + autodesk.com Plans and Pricing | 720 EUR / 684 USD, commercial 1-year |
| Autodesk revenue by region, TTM to Jun 2026 | aggregator (revenue-by-geography table), not the 10-K | Americas 44 / EMEA 39 / APAC 17 percent |

Not re-verified today, and therefore not stated as fact above: Fusion's 2013 launch date,
current tier names, current prices, and the exact scope of the free personal-use tier.

## 10. If we want to go further

- **Capability drift audit.** Run `patterns/WRAPPEE_CAPABILITY_DRIFT_SOP.md` against
  `freecad-mcp` with Fusion as the comparator, explicitly, so the gap list becomes actionable
  rather than anecdotal.
- **Extend the cross-check.** Add the curved cases that exercise the precision floor: loft,
  sweep, drafted pocket, threaded hole. Five green cases prove the harness; they do not prove
  the kernels agree where it is hard.
- **Watch the kernel port.** `bherbruck/solidcore` is a Rust port of NVIDIA's open-sourced
  SMLib. If it matures, the ShapeManager/OpenCASCADE/truck ranking above changes, and the
  tool that benefits most is whichever of ours can swap kernels.
