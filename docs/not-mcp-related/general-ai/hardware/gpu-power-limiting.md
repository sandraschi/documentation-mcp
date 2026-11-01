# GPU Power Capping: RTX 4090 at 300W

**Status:** Practical reference for reducing local inference heat

**Created:** 2026-08-01
**Context:** Goliath server - RTX 4090 (450W stock TDP), Ollama local inference
**Related:** `robotics/research/COMPUTE_LIMITS_SINGLE_GPU.md`, `integrations/ollama/TECHNICAL.md`

---

## 1. Why Cap Power

The RTX 4090 ships with a 450W power limit. Under sustained load
(LLM inference, rendering), essentially all of that electrical power is
dissipated as heat inside the case and eventually into the room.

Power-in equals heat-out for a GPU: there is no meaningful fraction of
input power that leaves as anything other than heat. One watt of power
is 3.412 BTU/h. A 4090 pegged at 450W is a 1,535 BTU/h space heater
the size of a graphics card.

Capping the limit is the single highest-leverage thermal control on the
card: it is a hard ceiling on heat generation that requires no fan curve
tuning, no case mods, and no undervolting experimentation.

---

## 2. Measured Setup (2026-08-01)

| Item | Value |
|------|-------|
| Card | NVIDIA GeForce RTX 4090 |
| Stock power limit | 450 W (also the max limit) |
| Capped power limit | 300 W (-33%) |
| Idle draw at 450W cap | ~28 W |
| Steady-state heat reduction | -150 W (-33%) |

The cap is applied with the stock `nvidia-smi -pl` mechanism. No
undervolt curve, no BIOS change, no driver hack. The card's boost
algorithm handles the rest: it clocks down just enough to stay under
the cap.

### Files

```
C:\Scripts\set_gpu_power.bat   # nvidia-smi -pl 300
```

### Windows quirk: no persistence

Windows resets `nvidia-smi` power limits on every reboot. GeForce
cards have no native persistence mode, and Nvidia's own persistence
daemon does not survive reboot for consumer cards. The cap MUST be
re-applied at every boot, and it must re-apply with Administrator
rights without a visible window or UAC prompt.

### Scheduled task (the clean automation)

Created with `schtasks` (Task Scheduler GUI equivalent described in
step 3 of the original writeup):

```
schtasks /Create /TN "NVIDIA GPU Power Limit" /TR "C:\Scripts\set_gpu_power.bat" /SC ONLOGON /RL HIGHEST /F
```

- Trigger: At logon (ONLOGON). Runs as the logged-in user, no stored
  password required. ONSTART would need SYSTEM or a stored credential.
- Privileges: `/RL HIGHEST` - mandatory. Without it `nvidia-smi -pl`
  fails silently on boot (the bat runs, the limit never changes).
- No visible window: a .bat via Task Scheduler runs without a console
  flash on modern Windows.

Verify the task is healthy:

```
schtasks /Query /TN "NVIDIA GPU Power Limit" /V /FO LIST
nvidia-smi --query-gpu=power.limit --format=csv
```

Apply immediately without waiting for the next logon:

```
schtasks /Run /TN "NVIDIA GPU Power Limit"
```

---

## 3. What You Give Up: Compute

The key insight is that power is NOT proportional to performance.
GPU power scales roughly as V^2 * f (voltage squared times clock
frequency), while performance scales roughly linearly with clock
frequency in the non-memory-bound regime.

Cutting the power limit by 33% therefore only forces a ~10-15% clock
reduction, which yields:

| Metric | Change |
|--------|--------|
| Power limit | 450 W -> 300 W (-33%) |
| Clock frequency | ~-10 to -15% |
| Compute throughput | ~-5 to -10% (retains ~90-95%) |
| Perf per watt | +~35% |

Real-world ballpark on a 4090 at ~67% power limit: gaming FPS drops
single digits; LLM token generation drops roughly 5-10%. VRAM-bound
phases (prompt processing, large batch decoding) are affected even
less, because they are bandwidth-limited, not power-limited.

The RTX 4090 is one of the best ratio cards for this: its boost
curve has enormous headroom, so it retains efficiency unusually well
at reduced power.

---

## 4. The Energy Nuance: Rate vs. Total

There are two different numbers, and they are easy to confuse:

1. **Heat rate (W)** - steady-state heat while pegged at the cap.
   This drops the full 33%: 450W -> 300W of heat into the room.

2. **Energy per fixed task (Wh)** - total energy for a render,
   a training run, a bulk inference job. This drops LESS than 33%,
   because the task now runs ~5-10% longer:

```
Stock:  450 W x 1.00 h = 450 Wh
Capped: 300 W x 1.09 h = 327 Wh  (task takes ~9% longer)

=> ~27% energy saved per task, not 33%
```

If the workload is instead time-boxed (continuous chat, a game
session of fixed length), then the full 33% heat reduction applies,
because the GPU is simply capped the whole time.

---

## 5. Adjusting and Resetting

Change the target wattage in `C:\Scripts\set_gpu_power.bat` (the
`300` in `nvidia-smi -pl 300`), then re-apply:

```
schtasks /Run /TN "NVIDIA GPU Power Limit"
```

Restore stock behavior at any time:

```
nvidia-smi -pl 450
```

Notes:

- The minimum settable limit on a 4090 is ~100W (driver-enforced).
- 300W is a conservative-but-comfortable point. 350W is a common
  "invisible loss" setting. Below ~280W the clock penalty starts to
  become visible in FPS and token rates.
- The power cap does not reduce idle draw (~28W) - it only limits
  the ceiling.

---

## 6. TL;DR

- 450W -> 300W cuts heat into the room by 150W (-33%) at full load.
- Compute drops only ~5-10% because power scales superlinearly with
  clock.
- Perf-per-watt improves ~35% - the actual reason to do this.
- Per fixed task, total energy drops ~27% (task runs longer).
- Windows forgets the cap on reboot; the ONLOGON scheduled task with
  /RL HIGHEST is the clean fix.
