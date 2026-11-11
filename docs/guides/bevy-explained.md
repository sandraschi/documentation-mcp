# Bevy explained, from zero, using the GameCraft code

Audience: a full-stack developer who finds Bevy alien. That reaction is normal and has a
cause: Bevy is not object-oriented, and almost everything you know about "a game object
with methods" has to be set down for a while. This guide rebuilds the picture using ideas
you already have (tables, queries, request handlers), then walks the real code in
`D:\Dev\repos\gamecraft\crates\gamecraft-bevy`.

Verified against Bevy 0.20.1 as used there. Snippets marked *shape* show the pattern, not
copy-paste code; snippets marked *repo* are taken from the repo.

---

## 1. The one idea: a game is an in-memory database plus functions that run on it

Forget classes. Think of the running game as a small database in RAM:

| Database idea | Bevy name | Example in GameCraft |
|---|---|---|
| A row id | **Entity** | one wall, the player, the goal, one starling |
| A column, a typed fact attached to a row | **Component** | `GridPos(3, 5)`, `Player`, `Transform` |
| A table of one-of-a-kind settings or state | **Resource** | `MazeRun` (moves, bumps, won), `FlockWorld` (the whole flock) |
| A stored procedure that runs on a schedule | **System** | `step_flock`, `apply_move`, `announce` |
| The SQL `SELECT ... WHERE` a system runs | **Query** | "every entity that has `GridPos` and `Player`" |
| A module you register | **Plugin** | `MazeLogicPlugin`, `MurmurationRenderPlugin` |
| The scheduler | **Schedule** | `Startup`, `Update`, `FixedUpdate` |

This whole style is called **ECS** (entity-component-system). The payoff is not elegance,
it is speed and decoupling: Bevy knows exactly which data each function touches, so it can
run independent functions on different CPU cores by itself, and it can store same-shaped
data contiguously in memory.

What feels alien, and why:

- **Data and behaviour are separate.** A `Player` is not an object with a `move()` method.
  It is a row carrying a `Player` tag and a `GridPos`; a *system* elsewhere moves every row
  that has both.
- **You never call your own functions.** You register systems; Bevy calls them, every frame
  or tick, in an order it works out (or you pin).
- **Function parameters are the dependency declaration.** The signature of a system is how
  you ask for data (section 5). Nothing is passed in by you.

---

## 2. The smallest complete program

*shape*

```rust
use bevy::prelude::*;

#[derive(Component)]            // a column
struct Name(String);

#[derive(Resource)]             // a one-row table
struct Score(u32);

fn setup(mut commands: Commands) {          // a system: runs once at Startup
    commands.spawn(Name("first".into()));   // insert a row with one column
    commands.insert_resource(Score(0));
}

fn greet(query: Query<&Name>, mut score: ResMut<Score>) {   // runs every Update
    for name in &query {                    // SELECT name FROM everything_with_Name
        println!("hello {}", name.0);
        score.0 += 1;
    }
}

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)        // window, renderer, input, audio, time...
        .add_systems(Startup, setup)
        .add_systems(Update, greet)
        .run();                             // the loop: Bevy now owns the program
}
```

`App::new()` builds an empty world. `add_plugins` and `add_systems` fill it. `run()` hands
control to Bevy, which loops forever: poll input, run schedules, render, repeat. Your
`main` only describes the world; it does not drive it. That inversion is the second thing
that feels alien.

---

## 3. Entities and components

An entity is just an integer id (with a generation counter). It has no data by itself. You
give it data by attaching components when you spawn it:

*shape (the maze does this for the player)*

```rust
commands.spawn((Player, GridPos(1, 1)));       // a tuple of components is a "bundle"
```

Components are plain structs, usually tiny. A marker component with no fields (`Player`,
`Goal`, `Wall`) is a *tag*: it exists only so queries can find the entity. In the repo:

```rust
// repo: crates/gamecraft-bevy/src/maze.rs
pub struct GridPos(pub i32, pub i32);   // where in the grid
pub struct Player;                      // tag
pub struct Goal;                        // tag
pub struct Wall;                        // tag
```

The rendering plugin later adds more columns to the same rows (a mesh, a `Transform`), and
the logic plugin never knows. That is the design goal: columns added by different plugins
to the same row.

Rule of thumb: if you reach for inheritance ("a Wizard is a Player that..."), instead add or
remove components ("this entity also has `Wizard`").

---

## 4. Resources: the singletons

Some state is not about any one entity: the current run's score, the loaded level, a timer.
Those are **resources**, one value per type, fetched by type:

```rust
// repo: crates/gamecraft-bevy/src/murmuration.rs
#[derive(Resource, Debug, Clone)]
pub struct FlockWorld(pub Flock);        // the entire simulated flock, one value

#[derive(Resource, Default)]
pub struct Steer { pub target: Option<(f32, f32)>, pub flare: bool }  // what the player wants
```

Look at how Murmuration is built: 20 000 starlings are **not** 20 000 entities in the
logic. They are plain arrays inside one resource (`FlockWorld`), stepped by the std-only sim
in `gamecraft-sim`. Why: the simulation must be deterministic and fast, and plain arrays
with a fixed update order give exactly that. ECS is great for "many different things with
overlapping traits"; a tight numeric simulation is better as one function over arrays. The
*render* plugin then spawns one entity per boid purely to draw it and copies positions in
each frame. Use ECS where it helps and step outside it where it does not.

---

## 5. Systems and their parameters

A system is an ordinary function. Its parameters tell Bevy what it needs:

| Parameter | Meaning | SQL-ish |
|---|---|---|
| `Res<T>` | read resource `T` | SELECT from a one-row table |
| `ResMut<T>` | read and write resource `T` | UPDATE that row |
| `Query<&A>` | iterate every entity with component `A` | SELECT a FROM ... |
| `Query<(&A, &mut B), With<C>>` | read A, write B, only where tag C exists | SELECT ... JOIN ... WHERE has C |
| `Commands` | queue structural changes (spawn, despawn, add or remove a component) | INSERT / DELETE, applied later |
| `Local<T>` | private state of this one system between runs | a static variable |
| `Time` | the clock | |
| `MessageWriter<M>` / `MessageReader<M>` | send or receive one-way notifications | an event bus (called Events before 0.17, Messages now) |

A real one from the repo:

```rust
// repo: crates/gamecraft-bevy/src/murmuration.rs
fn step_flock(
    mut world: ResMut<FlockWorld>,        // I will change the flock
    mut steer: ResMut<Steer>,             // and consume the player's input
    auto: Option<Res<FlockAutoplay>>,     // is the scripted pilot flying? (may not exist)
) {
    let orders = if auto.is_some() {
        autopilot(&world.0)               // scripted
    } else {
        let orders = Orders { target: steer.target.unwrap_or(world.0.lure), flare: steer.flare };
        steer.flare = false;              // the flare is a one-shot
        orders
    };
    world.0.step(orders);                 // one 1/60 s step of the pure simulation
}
```

Why the repo has `#![allow(clippy::needless_pass_by_value)]`: Clippy sees `Res<T>` taken by
value and complains it could be a reference. But taking it by value is the API; the type
carries the access declaration. It is not a smell here.

**Why parameters matter beyond style.** Bevy reads the signatures before running anything.
Two systems that only read the same data can run in parallel. A system that writes
`ResMut<FlockWorld>` cannot overlap another that touches `FlockWorld`. You get safe
parallelism for free, and the cost is that you must declare honestly. If two parameters in
one system could alias the same data mutably (two `Query<&mut Transform>` that might hit the
same entity), Bevy panics at startup with a conflict error (code B0001). The fix is a
`With`/`Without` filter that proves they are disjoint, or `ParamSet`.

---

## 6. Schedules: when things run

| Schedule | Runs | Use for |
|---|---|---|
| `Startup` | once, first | build the level, load assets, spawn the camera |
| `Update` | once per rendered frame (rate varies, 144 Hz, 30 Hz...) | input reading, drawing, sound reactions, anything visual |
| `FixedUpdate` | a fixed number of times per second, possibly several times or zero times in one frame | **game rules**, physics, simulations |

GameCraft pins `FixedUpdate` to 60 Hz:

```rust
// repo
app.insert_resource(Time::<Fixed>::from_hz(60.0))
   .add_systems(FixedUpdate, (step_flock, announce).chain());
```

Why rules live in `FixedUpdate`: the simulation must give identical results on a slow
laptop and on Goliath, in a test with no window, and in a replay. If rules ran per frame, a
faster monitor would make the game run faster. With a fixed step, Bevy accumulates real
time and runs the rules as many times as needed to catch up (or skips if ahead), always in
the same 1/60 s increments.

`.chain()` means "in this order, one after the other". Without it, Bevy may run two systems
in either order or in parallel. For the flock, `announce` must see the state *after*
`step_flock`, so they are chained. Ordering you do not state is ordering you do not get,
which is why the deterministic sim keeps its whole state in one resource and one function.

---

## 7. Commands are deferred (this surprises everyone once)

`commands.spawn(...)` does not spawn immediately. It records "spawn this" in a queue that is
applied at a sync point after the system finishes. Why: while systems run in parallel, the
table layout cannot change under them. Practical consequences:

- you cannot spawn an entity and query for it in the same system call;
- a system that spawns in `Startup` has its entities visible to `Update` systems, not to
  later lines of the same function.

Direct changes to existing data (`ResMut`, `&mut Component`) are immediate; only *structural*
changes (adding or removing entities and components) are deferred.

---

## 8. Plugins: how a game is assembled, and the two-plugin split

A plugin is anything with a `build(&self, app: &mut App)` that registers resources and
systems. `DefaultPlugins` is a big bundle of them: window, GPU renderer, input, audio, time.
Your game is plugins on top.

```rust
// repo (abridged): crates/gamecraft-bevy/src/murmuration.rs
impl Plugin for MurmurationLogicPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(Time::<Fixed>::from_hz(60.0))
            .insert_resource(FlockWorld(Flock::new(self.cfg)))
            .init_resource::<Steer>()
            .init_resource::<Announced>()
            .add_systems(FixedUpdate, (step_flock, announce).chain());
        if self.autoplay { app.insert_resource(FlockAutoplay); }
    }
}
```

**The most important design choice in this repo: every game is two plugins.**

1. A **logic** plugin: components, resources, fixed-step rules, the win check. It needs no
   window and no GPU.
2. A **render** plugin (and an **audio** plugin): meshes, camera, light, keyboard, sound.

Because logic is separate, `cargo test` runs the game to its win with no window
(section 9), the gates are deterministic, and the compile of the logic crate is fast. It
also means "the game" can be reused with a different front end (a replay viewer, a server).

---

## 9. Testing without a window

Bevy's `MinimalPlugins` gives the app loop and time without any window or GPU.
`TimeUpdateStrategy::ManualDuration` replaces the real clock with a fake one that advances
exactly 1/60 s per `app.update()`, so each `update()` is exactly one fixed tick:

```rust
// repo: crates/gamecraft-bevy/src/murmuration.rs (tests)
fn headless(cfg: FlockConfig, autoplay: bool) -> App {
    let mut app = App::new();
    app.add_plugins(MinimalPlugins)
        .insert_resource(bevy::time::TimeUpdateStrategy::ManualDuration(
            Duration::from_secs_f64(1.0 / 60.0),
        ))
        .add_plugins(MurmurationLogicPlugin { cfg, autoplay });
    app
}
// then: loop { app.update(); read FlockWorld; stop when won or lost }
```

This is how "autoplay wins the maze in 272 moves" and "autoplay settles the flock at tick
2564" are asserted in plain `cargo test`. The windowed gates (`just bevy-gate`,
`just murmuration-gate`) then prove the *real* binary reaches the same result and draws a
frame that is not blank.

---

## 10. What you see: meshes, materials, transforms, the camera

Drawing is also just components on an entity. *shape*:

```rust
commands.spawn((
    Mesh3d(meshes.add(Cuboid::new(1.0, 1.0, 1.0))),        // what shape (a handle into Assets<Mesh>)
    MeshMaterial3d(materials.add(Color::srgb(0.8, 0.2, 0.1))), // what surface
    Transform::from_xyz(3.0, 0.5, 5.0),                    // where, how rotated, how big
));
commands.spawn((Camera3d::default(), Transform::from_xyz(0.0, 40.0, 30.0).looking_at(Vec3::ZERO, Vec3::Y)));
commands.spawn((PointLight::default(), Transform::from_xyz(0.0, 20.0, 0.0)));
```

Three ideas:

- **Handles.** `meshes.add(...)` stores the mesh once in `Assets<Mesh>` and returns a cheap
  `Handle`. Many entities can point at the same handle. Murmuration relies on this: all
  boids of one colour share one mesh and one material, so the GPU draws them in a handful of
  batched calls instead of 20 000 separate ones. That is why 20 000 boids run at 60 fps.
- **`Transform`** is position, rotation, scale. Moving a thing means writing its
  `Transform` from a system (the render plugin copies sim positions into transforms every
  frame).
- **The camera is an entity.** Nothing special: an entity with `Camera3d` and a
  `Transform`. Our follow camera is a system that edits that transform each frame.

Coordinate note from the repo: sim (x, y) maps to world (x, z), with the camera above and
behind looking down, so "up" on the keyboard means y minus 1.

---

## 11. Input, notifications and sound

- **Input**: a system takes `Res<ButtonInput<KeyCode>>` and asks `just_pressed(KeyCode::Space)`
  or `pressed(...)`. In GameCraft the render plugin turns keys into the `Steer` resource and
  the fixed-step logic reads it. Input in `Update`, rules in `FixedUpdate`: the two are
  connected only through a resource.
- **Messages** (called Events in older tutorials; renamed in Bevy 0.17): fire-and-forget
  broadcasts. The binaries use one to quit: `MessageWriter<AppExit>` then
  `exit.write(AppExit::Success)`.
- **Sound** uses the same ECS idea: playing a sound is spawning an entity.

  ```rust
  // repo: crates/gamecraft-bevy/src/audio.rs (abridged)
  commands.spawn((
      AudioPlayer::new(clip.clone()),                          // which clip
      PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)), // play once, then remove the entity
  ));
  ```

  GameCraft's clips are synthesised by formulas (`synth.rs`) and handed to Bevy as WAV bytes.
  A separate pure module, `cues.rs`, decides *when* a sound happens (hawk ate something,
  flare fired, game won) from game state, so the rules are unit-tested without a sound card.
  `audio.rs` only maps each cue to a clip. The same logic/presentation split as everywhere
  else.

---

## 12. Walk through one tick of the maze

1. Real time passes; Bevy's fixed-timestep accumulator decides a tick is due.
2. `FixedUpdate` runs the maze rules: read the `Intent` resource (set by the keyboard
   system, or by the autoplay driver), check `MazeLevel::open` for the target cell, and if
   open update the player's `GridPos` and `MazeRun.moves`, otherwise bump `MazeRun.bumps`.
   If the player is on the goal cell set `MazeRun.won` and print the win marker.
3. `Update` runs once per frame: the render plugin reads `GridPos` and glides the player's
   `Transform` toward the cell, so movement looks smooth while rules still move one whole
   cell per tick; the audio plugin compares `MazeRun` with what it last heard and plays a
   blip, a thump or the win chime.
4. Bevy renders the frame.

Nothing in step 2 knows steps 3 and 4 exist. That is the point.

## 13. Walk through one tick of Murmuration

1. `FixedUpdate`: `step_flock` builds `Orders` (lure target, flare) from `Steer` or the
   autopilot and calls `Flock::step`. Inside, steering is computed on up to 8 threads over
   fixed chunks and merged in a fixed order, so the result is bit-identical regardless of
   thread count (that is what makes the headless test and the real window agree).
2. `announce` checks `won` or `lost` once and prints the marker.
3. `Update`: `sync_boids` copies each boid's position and heading into its entity's
   `Transform`; `camera_rig` follows the flock; `hud` writes stats into the window title;
   `react_murmuration` asks `FlockEars` what is new and plays cues.
4. Bevy draws about 20 000 instanced meshes.

---

## 14. Where each concept lives in this repo

| Concept | File |
|---|---|
| Pure simulations (no Bevy at all) | `crates/gamecraft-sim/src/flock.rs`, maze generator and solver |
| Maze logic plugin, components, resources | `crates/gamecraft-bevy/src/maze.rs` |
| Maze meshes, camera, keyboard | `crates/gamecraft-bevy/src/render.rs` |
| Murmuration logic plugin | `crates/gamecraft-bevy/src/murmuration.rs` |
| Murmuration rendering, camera, HUD | `crates/gamecraft-bevy/src/render_murmuration.rs` |
| Sound formulas | `crates/gamecraft-bevy/src/synth.rs` |
| When to play which sound | `crates/gamecraft-bevy/src/cues.rs` |
| Playing sounds with Bevy | `crates/gamecraft-bevy/src/audio.rs` |
| Spectrograms and WAV dump | `crates/gamecraft-bevy/src/analysis.rs`, `src/bin/synth_dump.rs` |
| The playable programs (`main`) | `crates/gamecraft-bevy/src/bin/maze.rs`, `murmuration.rs` |
| Catalog entries | `bevy/games/<slug>/game.json` |

Reading order for a first pass: `murmuration.rs` (small, no rendering), then the tests at its
bottom, then `render_murmuration.rs`.

---

## 15. Build, features and why it is slow

- Bevy is huge (hundreds of crates). The repo keeps it in one workspace member
  (`gamecraft-bevy`) so everything else builds fast, and turns **default features off**,
  adding back only what each game needs: `3d_bevy_render`, `default_app`, `multi_threaded`,
  `bevy_winit`, `keyboard`, plus `bevy_audio` and `wav` for sound. Cargo features are how
  you ask Bevy not to compile the parts you do not use.
- `cargo test -p gamecraft-bevy` compiles only the logic (no renderer): fast.
- A windowed build uses the `render` feature. The custom Cargo profile `play` compiles
  dependencies at optimisation level 3 and our own code at 1; the first build took about 12
  to 15 minutes, later ones are fast. Run with `-j 6` so Windows does not run out of paging
  file (error 1455).
- While iterating you can add the `dev` feature (dynamic linking) for seconds-long relinks.

## 16. Reading Bevy errors

| You see | Usually means |
|---|---|
| Panic at startup mentioning B0001 or "conflicts with a previous access" | two parameters in one system could mutably alias; add `With`/`Without` filters or `ParamSet` |
| Panic "Resource ... requested by system does not exist" | the plugin that inserts it was not added, or the system runs before `Startup` created it; use `Option<Res<T>>` if it may be absent |
| Nothing draws | missing camera, light, or `Visibility`; or the entity has a mesh but no `Transform` in view |
| A system never runs | not added with `add_systems`, or it is in the wrong schedule, or a `run_if` condition is false |
| Wrong ordering, flaky results | systems unordered; add `.chain()` or `.before()` / `.after()` |
| Type has no `Component` impl | forgot `#[derive(Component)]` |
| Compile error after a Bevy upgrade | the API moved (it is pre-1.0); read the migration guide for that version |

## 17. Exercises (each changes one concept)

1. In `MazeLevel::challenge`, change the seed and watch `autoplay` still win: proves the
   solver, not the level, is trusted.
2. Add a `Component` tag `Visited` to cells the player has stepped on, and a system that
   tints them. You touch components, queries, `Commands` and materials.
3. Change `Time::<Fixed>::from_hz(60.0)` to 30 in a headless test and see tick counts
   change but outcomes not (fixed step means rules are frame-rate independent).
4. Make `Cue::Step` quieter in `audio.rs`, then run `just sounds` and compare the report.
5. Add a second hawk cry sound: new `synth` function, new `Cue`, new `FlockEars` rule with a
   test, new entry in `audio.rs`. Four files, each one concept.

## 18. Vocabulary

**ECS** entity-component-system. **World** the whole in-memory database. **Archetype**
the set of entities sharing the same component set (stored together; why queries are fast).
**Bundle** a tuple of components spawned together. **Marker/tag** a field-less component.
**Handle** a cheap reference to an asset. **Observer** a callback triggered by an event on
an entity (used for saving screenshots). **Run condition** a boolean function that gates a
system. **State** Bevy's enum-based game phases (menu, playing); GameCraft does not use it
yet.

## 19. Further reading

- The official book and examples at bevy.org and the `examples/` folder in the Bevy
  repository (the best source; copy small examples and mutate them).
- docs.rs/bevy for the exact 0.20 API. Third-party tutorials, including the popular
  community cheat book, are often written for older versions; check the version first.
- Fleet standard for when Bevy is justified: `standards/rust-crates/BEVY.md`.
- GameCraft's own plan and decisions: `D:\Dev\repos\gamecraft\docs\TARGETS_PLAN.md`.