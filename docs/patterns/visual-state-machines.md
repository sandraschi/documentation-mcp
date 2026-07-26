# Visual State Machines (VSM)

**Status:** Research / Proposed
**Date:** 2026-07-21
**Fleet hooks:** `devices-mcp`, `OCR-MCP`, `monitoring-mcp`, `health-mcp`

## The Insight

A cheap USB camera + motion detection can turn any *dumb physical device* into a
smart event source. No IoT, no API, no sensor — just watch what happens and infer.

## Examples

| What happens | Camera sees | Inferred event | Action |
|-------------|-------------|---------------|--------|
| Fridge door opens | Motion in fridge region, temperature plume | "Someone's getting food" | "What will you cook today?" |
| Toaster lever pushed down | Object enters toaster | "Toast started" | Start 3 min timer |
| Toast pops up | Motion burst above toaster | "Toast done" | "Ding!" (TTS to living room) |
| Step on body scale | Blob of person-shape appears on scale region | "Weigh-in" | Read weight from OCR on display, log to health DB |
| Hamster enters tube | Motion + blob in specific region | "Hamster in tube" | Record event, webcam snapshot |
| Washing machine stops vibrating | Optical flow drops to zero after period of vibration | "Wash cycle done" | "Laundry's ready" |
| Mailbox flag goes up | Color change in mailbox region | "Mail arrived" | Snapshot, OCR address |
| Cat at back door | Motion + blob at specific region at specific time | "Cat wants in" | Unlock cat flap, send snapshot |
| Scanner lid closes | Object enters + motion stops in scanner region | "Document ready to scan" | Trigger flatbed scan + OCR |
| **Dog food bowl empty** | Bowl region: empty (no color/texture change for 30 min after eating) → food surface drops below threshold | "Benny's bowl is empty" | "Refill Benny's bowl!" (TTS) or auto-order food |
| **Dog scratches door** | Door region: repetitive motion pattern (scratching, not knocking) at specific height | "Benny wants out/in" | "Benny wants a walk!" or open door |
| **Human wakes up** | Bedroom door opens + motion in kitchen within 5 min, or no motion in bedroom past 11am | "Sandra is awake" | "Good morning! Should I read the morning report?" |
| **Coffee machine done** | Drip stops + mug in place 30s later | "Coffee's ready" | "Your coffee is waiting" |
| **Mail delivered** | Front door opens briefly + object placed in mailbox region | "Mail arrived" | Snapshot + OCR any visible text |
| **Plant needs water** | Soil region in pot: color shifts from dark (wet) to light (dry) over days | "Plant thirsty" | "Time to water the monstera" |
| **Package delivered** | Front door region: delivery person blob + object left on ground | "Package dropped" | Snapshot + notification |
| **Someone at door** | Door region: blob stationary >3s (not a passerby) | "Visitor" | "Someone's at the door" + snapshot |
| **Garage door open** | Garage door region: color/texture change (door up vs down) | "Garage open" | "Garage door is still open" (after 15 min) |
| **Child comes home** | Front door opens + small blob enters, backpack region visible | "Kid's home" | "Welcome home!" TTS |

## Architecture

```
┌─────────────┐   video   ┌──────────────────┐   events    ┌──────────────┐
│ USB Camera   │─────────►│ visual-watcher    │────────────►│ fleet MCP    │
│ (Logitech    │  frames  │ OpenCV state      │  webhook    │ servers      │
│  C270, $20)  │          │ machine           │  JSON       │              │
└─────────────┘           └──────────────────┘             └──────────────┘
                                  │                              │
                           ┌──────┴──────┐                ┌──────┴──────┐
                           │ Region masks │                │ TTS / Notif │
                           │ Per-device   │                │ DB / Log    │
                           │ ROI configs  │                │ Trigger     │
                           └─────────────┘                └─────────────┘
```

### Components

**1. Camera feed** (via `devices-mcp`)
- Exposes USB camera frames as MCP resources (`camera://{id}/frame`)
- Configurable resolution (640x480 is enough for motion detection)
- One camera can watch multiple devices if positioned right

**2. Visual watcher** (new service, or extension of `scanner_watcher.py`)
- Per-device region of interest (ROI) masks — drawn once during setup
- Per-device state machine: `{states, transitions, triggers}`
- OpenCV pipeline: background subtraction → contour detection → state transition
- Emits JSON events: `{device, event, confidence, timestamp, snapshot_url}`

**3. Action routing** (via fleet MCP servers)
- `speech-mcp` for TTS ("Ding! Toast is ready")
- `monitoring-mcp` for logging and dashboards
- `OCR-MCP` for scanner trigger and display OCR
- `health-mcp` (or equivalent) for body scale weight logging
- `home-assistant-mcp` for smart home actions

## State Machine Pattern

Each device has a simple state machine:

```
IDLE ──► ACTIVE ──► DONE ──► IDLE
```

Example — Toaster:

```
state: IDLE
  on: object enters toaster region → transition to HEATING, start timer

state: HEATING
  on: timer hits 3 min → "Toast should be done" (low confidence)
  on: motion burst above toaster → transition to POPPED

state: POPPED  
  on: no motion for 10s → "Toast retrieved"
  on: motion burst above toaster → "Ding!" (high confidence)
  transition to IDLE
```

Example — Body scale:

```
state: IDLE
  on: person-shape blob in scale region → transition to STEPPED_ON

state: STEPPED_ON
  on: blob stable for 3s → capture frame, OCR the display
  on: blob leaves region → transition to READ_DONE

state: READ_DONE
  if OCR got a number: log weight to health DB
  else: "Couldn't read display — try again"
  transition to IDLE
```

## Implementation Notes

- **Hardware:** Logitech C270 ($20-30) or any UVC-compatible USB camera.
  One camera per room can watch multiple devices.
- **Resolution:** 640x480 at 10fps is more than enough. Higher res = more CPU.
- **Lighting:** IR camera for dark environments (fridge, mailbox at night).
  IR LED ring for consistent illumination.
- **Region setup:** One-time calibration. Show the camera the scene, draw
  rectangles on the frame for each device. Save as JSON config.
- **False positives:** Cooldown timers prevent re-triggering. Confidence
  scoring: single motion event = low, multi-frame consistent state = high.
- **Privacy:** All processing local. No video leaves the machine. Snapshots
  for debugging are opt-in and expire.

## Relationship to Existing Fleet

| Fleet server | Role |
|-------------|------|
| `devices-mcp` | Camera feed source, USB device enumeration |
| `OCR-MCP` | Display OCR (scale, meter), scanner trigger |
| `speech-mcp` | TTS announcements |
| `monitoring-mcp` | Event logging, dashboard |
| `aiwatcher-mcp` | Digest of notable household events |

## Open Questions

- Should the visual watcher be a new MCP server or a plugin for `devices-mcp`?
- One camera per room or one camera per device? (Tradeoff: cost vs coverage)
- How to handle multiple people in frame? (Person tracking needed for fridge/scale)
- Confidence thresholds: what's the false-positive rate that's acceptable per device?

## State Machine Examples

### Dog Food Bowl

```
state: FULL
  on: dog enters bowl region → transition to EATING
  on: no dog near bowl for 4 hours → transition to EMPTY (slow depletion)

state: EATING
  on: dog leaves bowl region → transition to JUST_FED
  on: bowl empty detected (food surface dropped below threshold) → EMPTY

state: JUST_FED
  on: 30 min timer expires → transition to FULL
  on: bowl still empty after 30 min → EMPTY (dog ate everything)

state: EMPTY
  on: food poured (motion above bowl, then color change in bowl) → transition to FULL
  → emit: "Benny's bowl is empty — time to refill!"
```

Detection: A camera aimed at the bowl area. Empty bowl = see the bottom (color change
from kibble brown to stainless steel silver). Motion above bowl = dog eating or human
refilling. No expensive smart bowl needed, just a $20 camera.

### Dog Scratching Door

```
state: IDLE
  on: repetitive vertical motion in door region at dog-head height → transition to SCRATCHING

state: SCRATCHING
  on: 3+ scratch cycles within 10s → emit "Benny wants out/in!"
  on: door opens → transition to IDLE (request fulfilled)
  on: 60s no motion → transition to IDLE (gave up)
```

Detection: Scratch pattern is distinctive — rapid vertical motion, at a specific height
(dog-head level, not human-handle level). Different from knocking (which is horizontal
at human height) or leaning (which is static).

### Wake-Up Detection

```
state: ASLEEP
  on: bedroom door opens (motion + door angle change) → transition to WAKING
  on: 11:00 and no motion in bedroom for 2+ hours → transition to WAKING (late sleeper)

state: WAKING
  on: motion detected in kitchen or bathroom within 10 min → transition to AWAKE
  on: no follow-up motion for 20 min → back to ASLEEP (went back to bed)

state: AWAKE
  → emit: "Good morning! Should I read the morning report?"
  → one shot per day (flag in DB, resets at 4am)
```

No wearable, no phone sensor, just a camera watching the bedroom door and kitchen.
The "11am late sleeper" branch catches weekends and sick days.

## See Also

- `OCR-MCP/docs/BOOK_SCANNING.md` — Camera-based auto-scan trigger for flatbed scanner
- `devices-mcp` — USB camera feed as MCP resource
- `speech-mcp` — TTS for voice announcements
