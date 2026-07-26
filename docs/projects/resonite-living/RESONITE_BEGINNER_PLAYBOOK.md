# Resonite Beginner Playbook — for Sandra, tonight

**Written**: 2026-07-18 · **Grounding**: wiki.resonite.com (live-checked this
session, not from training memory alone — Resonite is niche and evolves
fast) plus resonite-mcp's existing `BEGINNERS_GUIDE.md` for basic controls.
**Scope**: exactly the five things asked — leave the welcome area, travel
between worlds, make your own world, add furniture/a living room, open
audio links, and (the actual point) make Nekomimi-chan speak.

---

## 0. Where you are right now

You're in the **Tutorial world** (`Tutorial [en-US]`) — the same session
this whole project has been testing against tonight (ResoniteLink port
11831). That's a stock, disposable practice space. Nothing you do there is
precious — the test objects spawned tonight (house, Boomy chassis,
Nekomimi-chan) live there and vanish if that session closes. That's fine,
it's the point of a tutorial session.

## 1. Basic controls (if you haven't already got these from the tutorial)

```
WASD        = walk
Mouse       = look (hold right-click if not already free-look)
Space       = jump
Tab         = open the Dash (THE most important key — everything routes
              through here: worlds, inventory, settings, create tools)
E           = interact/grab
T           = text chat
Esc         = close menus / cancel
```

Everything below routes through **Tab → Dash**.

## 2. Leaving the welcome area — how to travel to other worlds

Three distinct ways to get somewhere else, worth knowing apart:

1. **World Browser** (Dash → Worlds → Browse): a searchable list of public
   worlds — social hubs, creative spaces, games. This is the "go explore"
   button.
2. **Direct world links** (`resrec://...` links): Resonite worlds can be
   shared as clickable links, the same way a URL works. Someone gives you
   a link (Discord, a wiki page, a friend), you open it in Resonite, you're
   there. You'll see these a lot in community resources — e.g. the
   Kitbasher world (a real, useful one for later — see §4).
3. **Your Home** — every Resonite account automatically gets a **Cloud
   Home** the first time you log in: a personal, customizable world that's
   always there, always yours. Dash → Worlds → Home gets you back to it
   from anywhere, and it's a reasonable default answer to "where do I put
   my stuff" before you've built anything custom.

**Session vs. World** — worth understanding early: a *World* is the actual
place (the file, the design). A *Session* is a live, running instance of
one World, hosted by whoever's running it — it exists while the host is
in it and ends when they leave. Two different Sessions of the same World
don't share what happens in them live.

## 3. Making your own world

Dash → **Create New World**. It'll ask you to pick a starting template —
`Grid` (flat floor with a grid, good for building), `Platform` (a plain
circle), or `Blank` (nothing — advanced). Pick `Grid` to start.

You'll also set, right there in the creation dialog:
- **World Name** — what it's called, shown to others if public.
- **Access Level** — who can join: `Private` (invite-only — **this is what
  you want** for Nekomimi-chan's home, per the project plan's earlier
  etiquette note about not making an AI-companion space publicly
  joinable), `LAN`, `Contacts`, `Contacts+`, `Registered users`, `Anyone`.
- **Port** — leave on `Auto` unless you have a specific reason not to.

**To save it** (important — a created-but-unsaved world can vanish):
go to **Session tab → Settings → Save As...**, saving into a folder in
your own Inventory you can write to. That's what makes it a persistent
thing you can return to, rather than a one-off scratch session like the
Tutorial you're in now.

**This is the actual "home" for the project** — not the automatic Cloud
Home necessarily, though you could use that instead if you'd rather not
juggle two "home" concepts. Either works; pick one and be consistent
about which one Nekomimi-chan actually lives in.

## 4. Furniture and a living room

Two tracks, worth keeping separate:

**A. Fast — use existing community content.** Resonite has an active
building/kitbashing community with free, importable asset packs:
- **Dawn** (and the community-made **Dusk Modular** companion set) —
  furniture/architecture kits, CC0-licensed, matching styles.
- **Kitbasher world** — a real, linkable Resonite world built specifically
  for house-building: import tools plus a large collection of prefabbed
  furniture, ready to grab and place. Worth visiting directly (it'll be
  a `resrec://` link — search "Kitbasher" from the World Browser or ask
  in the Resonite Discord for the current link, since these can move).
- **Softpoint's shop** and similar community worlds — decorative props
  (plushies etc.), same pattern: visit, grab, bring into your world.

The general mechanic, precisely (grabbing alone does NOT save it to your
account — easy to assume it does, it doesn't): walk into a world with
items you like, **grab one** (laser/hand), then **open the context menu
while still holding it** and choose to save it into a folder in your
Inventory — that's the step that actually makes it yours permanently.
From there, in any world, **Tab → Inventory → navigate to that folder →
double-click the item** to spawn it into whatever world you're currently
in.

**Faster one-off alternative — Transfer Grabbing** ("grab smuggling"):
grab an item and, while still holding it, travel directly to another
world — Resonite carries it through the transition automatically, no
separate Inventory-save step. Good for "just get this one sofa over
there right now"; if you'll want to reuse it later, still worth also
saving it to Inventory at some point since Transfer Grabbing alone
doesn't create a permanent copy.

**B. Slower, custom — this project's own pipeline.** Everything built
tonight (`gltf_meshjson.py`, `stl_meshjson.py`, `decimate_meshjson.py`,
live ResoniteLink import) is exactly the mechanism for bringing
Marble-generated or Blender-built furniture in programmatically, per the
master plan's Phase 2 (shell refinery + furniture kit-bash). That's the
path for anything custom-generated rather than hand-picked from the
community — the kotatsu for Phase 5b's lesson scene, for instance.

Use (A) to get a living room *tonight*, cheaply. Use (B) for anything
that needs to be a specific, generated, or programmatically-placed object
later.

## 5. Audio links

This term covers a few genuinely different things in Resonite — worth
being precise about which one you mean, since the mechanisms differ:

- **Ordinary voice chat**: automatic, proximity-based. No setup — people
  near your avatar hear you talk (mic permitting), same as most social VR.
- **Stream Audio** (Dash → **Home tab → "Stream Audio"** button): this is
  the real "audio link" feature — it lets you pick an audio input device
  (your mic, or a virtual audio cable capturing another app's output) and
  broadcast it into the world persistently as a spawned **Audio Stream
  Controller** object, separate from your normal voice. This is how
  people DJ, share a music source, or pipe an external audio pipeline
  into a session. **This is very likely what you actually want** to test
  tonight, and it's also relevant to Nekomimi's voice later (see §6).
- **Video/Audio Player with a URL**: drop a link into a Video Player's
  URL bar and it'll try to play that source directly (works for many
  streamable URLs). Different from Stream Audio — this pulls a stream
  by link rather than broadcasting a local device.
- **AudioClipPlayer + AudioOutput**: for a specific, already-imported
  audio file (not a live stream) — load a clip, play it through an
  Audio Output component. This is the one that matters for Nekomimi.

## 6. Making Nekomimi-chan speak — the real mechanism

This ties directly into what's already scoped in the master plan (Phase
5) and what's now confirmed as real, nameable Resonite components rather
than a guess:

1. **learnbot-mcp** generates her reply text (already live daily).
2. **speech-mcp** (Gemini TTS, already live) turns that text into an
   audio file.
3. That file needs to become a Resonite **AudioClip asset** on her slot.
   ResoniteLink's protocol lists `importAudioClipFile` as a real message
   type (same family as `importMeshJSON`, which this project used
   extensively tonight) — **not yet wrapped as a client method** in
   `resonite_link.py` (same situation `import_mesh_json` was in before
   Phase 0), so this is real, scoped, not-yet-done work, not a guess.
4. Once imported, an **AudioClipPlayer** component (holding that clip) +
   an **AudioOutput** component (set to spatialized, positioned at her
   slot) makes it audible, positionally, from her location — so she
   sounds like she's actually talking from where she's standing.
5. Triggering step 4 on every new conversation turn is the "she speaks"
   loop — chat response → TTS → import → play, repeating.

None of this is built yet. It's the natural next engineering step after
tonight's mesh work, and now has concrete, named components to build
against instead of an open question.

## 7. Procedural objects, mirrors, screens, pictures

All four of these are real, standard Resonite mechanics — grounded via
wiki.resonite.com checks this session, not guessed.

**Rotating / spinning objects — no ProtoFlux needed.** Resonite has a
`Spinner` component (Transform category, alongside `Wiggler`/`Wobbler` for
other built-in procedural motion) — attach it to a slot and it rotates on
its own. This is the fastest path for "something rotating."

**Morphing / pulsing / custom animated properties — ProtoFlux.** The
official tutorial pattern (Tutorial:RGB Cube) is the template for this
whole category: a `World Time Float` node feeds a math node (Sine,
multiply, etc.), whose output drives a property via a `Drive` node —
that tutorial specifically drives a material's color hue over time, but
the identical pattern drives scale, position, or (if the mesh actually
has blend-shape data) a blend-shape weight for true mesh morphing. Grab
the ProtoFlux Tool from your Inventory's Essentials folder to start.

**A mirror.** Underlying mechanism: a `CameraPortal` component (also
called Mirror/Portal/Gateway in Resonite's own terminology) on a flat
surface, paired with a `ReflectionMaterial` component that renders what
the portal sees. Building this from scratch is a real ProtoFlux/component
task — **much easier as a beginner**: grab a ready-made mirror facet from
the community, e.g. **Mirracle** (Enzi's public folder) — just spawn it
from Inventory like any other item, no building required.

**A TV screen playing a Plex video — yes, and it's easier than it sounds
on your setup specifically.** Resonite's `Video Player` has a URL bar:
paste a link and it attempts to stream/download from there (it uses
libVLC under the hood, per the Audio Player docs, so it handles a wide
range of formats/protocols, not just a narrow whitelist). Since **Goliath
runs both Plex and Resonite**, this is same-machine/local-network
playback — the 2025 Plex policy change that requires a paid pass only
affects *remote* playback (off your local network), so it doesn't apply
here at all. Concretely: use `python-plexapi` (`pip install plexapi`) to
get a direct stream URL for a specific item —
```python
from plexapi.server import PlexServer
plex = PlexServer()  # defaults to localhost:32400
item = plex.library.section('Movies').get('Some Movie')
url = item.getStreamUrl()
```
— then paste that URL into the Video Player's URL bar in Resonite. Worth
testing with one file before assuming it always works.

**A picture on the wall.** Simplest version: a flat `Quad` (Shape Tool)
with an image applied as its texture — dragging an image file into
Resonite directly typically spawns a basic textured picture object
already, similar to how dropping in a video spawns a Video Player.


1. Get comfortable with Tab/Dash navigation in the Tutorial world you're
   already in (§1-2) — no rush, this is free practice.
2. Dash → Create New World → Grid template → Private access → **Save As**
   into your Inventory (§3). This is your first real, persistent world.
3. Visit Kitbasher (or search the World Browser for it) and grab a few
   furniture pieces into your Inventory (§4A) — instant living room.
4. Try the **Stream Audio** button (Home tab) once, just to see what it
   does (§5) — good to have used it once before it matters for real.
5. Leave Nekomimi's actual voice (§6) for a build session — it's real
   work (wrapping `importAudioClipFile`, wiring AudioClipPlayer/Output),
   not a tonight task.
