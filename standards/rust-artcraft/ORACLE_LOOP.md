---
title: "Oracle loop: original app, artifact, diff, iterate"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-18
---

# Oracle loop

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)

One of the patterns behind the Crafting Apps. The original program is the oracle. The clone is not done while its output still differs.

## The loop

1. Start the original app.
2. Click and drag. Make one artifact. Begin small: one shape, one layer, one paragraph, one cell.
3. Write it out. Save the native file. When the claim is about looks, also write the rendered picture.
4. Open that file in the clone under development. Render it, or write it out again.
5. Diff. Structure against structure. Pixels against pixels. The pass bar is a difference of nil, or one quantization step (1/255) where the format forces it.
6. If the diff is not nil, fix the clone and add the file to the corpus. A published floor only rises.
7. Grow the same gesture. Tens of objects, then thousands, then millions. A nil diff on a toy file that explodes on a million objects is a failed pass.
8. Iterate.

The original app is an oracle for output. It is not a source of code, shaders, or assets. Clean-room still holds.

## The same loop for UI and UX

When the claim is about the screen, the artifact is a screenshot of the gesture, not a saved document.

1. Start the original app. Click and drag the control under test: a crop handle, a slider, a selection, a panel resize.
2. Screenshot that frame. One gesture, one frame. Then the same gesture with the window full of objects.
3. Do the identical clicks in the clone. Screenshot that frame.
4. Diff the two images. Pass is nil, or a known difference you wrote down (font hinting, one-pixel antialiasing). An unexplained shift of a handle, a wrong cursor, or a panel that lands in a different place is a fail.
5. Fix the clone. Keep the pair. Raise the floor. Iterate.

A golden PNG of our window alone is not this loop. The oracle frame is the original app, taken after the same click and drag. `egui_kittest` keeps our frame from drifting after the pair already matches.

## What "nil" means in practice

PhotoCraft publishes the loop as numbers, not a vibe. `max_diff` is the largest per-channel distance between two RGBA buffers, ignoring pixels that are fully transparent on both sides. Their own files round-trip (169/169 in the io corpus at one published check). Photoshop-authored files are the harder oracle: on 2026-10-10 they reported 133/256 rendering as Photoshop does, and about 65% of a 170-file corpus pixel-matching. Those floors are the point. The loop is finished for a case only when the diff is nil. The product is not finished because the loop exists.

VectorCraft states the other half of the rule: a real user's file may be used locally and must not be committed. PhotoCraft keeps the authored corpus in a separate repo (`storytold/photocraft-corpus`).

## Fleet use

For a `repconv` repo, run both loops against the legacy app or the Craft engine being wrapped. File diffs cover exports. Screenshot pairs cover the gesture. A golden of our window alone covers neither.

- Small artifact first, committed only if it contains no private library data.
- Then a generated artifact at thousands of objects (books, tracks, pages, cells).
- Then the largest set the machine can hold, when the claim is "the library does not fall over."
- Record the diff command and the floor in `docs/CONVERSION_LOG.md`. Do not lower the floor to go green.
