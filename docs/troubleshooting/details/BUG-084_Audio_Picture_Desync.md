# BUG-084 - Voiceover drifts ahead of the picture when page dwell is variable

**Severity**: P2 (output is wrong but valid; every narrated video from the old pipeline was affected)
**First seen**: 2026-10-21, `demo-vid-mcp` japanophile-mcp tour
**Affects**: any pipeline that lays narration over scenes with per-scene dwell times

## Symptom

The voice reaches each page's line before the page appears, and the error accumulates.
Measured on the japanophile tour:

```
video 263.8 s   voiceover 156.3 s   23 cues
cue 2   SRT 10.100   audio  7.144   -2.956 s
cue 10  SRT 100.100  audio 42.208  -57.892 s
cue 23  SRT 251.100  audio 103.689 -147.411 s
```

Subtitles looked plausible (they were generated from the same waits as the video), which is
why this survived review: every artifact was internally consistent except the audio.

## Root cause

Two timelines, one silence constant.

1. Video page boundaries advanced on cumulative `wait` values, including authored `hold`
   steps (e.g. a 10 s page, then a 3 s hold).
2. The voiceover was concatenated with a **fixed 0.8 s** inter-segment silence.
3. `align_script_waits` set `wait = max(authored, narration + pad)`. Authored dwell (10 s)
   usually exceeded narration + pad (~6.8 s), so waits stayed at 10 s while the audio moved
   on at 6.8 s. Every such page pushed the next line earlier.

The code comment asserted `wait[i] = duration[i] + gap` "by construction". It was only true
if the script's authored waits happened to equal narration + pad, which they never do.

## Fix (`demo-vid-mcp` `8816fcd`, `ee61173`)

One timeline, derived from the same waits the picture uses:

- `narration_timeline(steps, durations)` returns each segment's start (cumulative waits,
  hold steps included) plus the gap to the next page.
- `assemble_voiceover()` places segments **absolutely** into a silent bed of the picture
  length, instead of concatenating with a constant. It reports `overrun` if a line exceeds
  its page rather than shifting everything after it.
- `PAGE_GAP_S = 2.0` is both the pad alignment adds and the minimum tail, so a page always
  holds 2 s past end-of-speech.

Verified end-to-end on a re-recorded tour:

```
worst drift +0.121 s across 23 cues (tolerance 0.35)
audio bed 276.0 s vs picture 281.6 s (5.6 s outro hold, allowed)
```

## Gate

`demo-vid-mcp` now ships `scripts/check_sync.py`:

- compares every SRT cue start against real speech onsets (`ffmpeg silencedetect`),
- compares the audio bed length with the video length,
- fails on drift above 0.35 s or speech outrunning the picture.

Run it after any narration change: `just verify-sync <repo>`.

## Lesson

If the picture and the sound are both laid out from a dwell table, they must be laid out
from the *same table*, and the invariant must be checkable from the artifacts. A constant
that "should be equal" is not a timeline. This class of bug is invisible in subtitles and in
file sizes, and obvious the moment you compare a cue time to an audio onset.
