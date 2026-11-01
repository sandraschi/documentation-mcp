# BUG-056 — Goliath cargo passes split `--cfg values(...)` args; all native builds fail

**Date:** 2026-09-29
**Found during:** raspberrypi-mcp scaffold (assfix-zero gate: `cargo check` on `native/`)
**Severity:** P1 (blocks every Tauri/NSIS build fleet-wide; no repo can produce an installer)
**Class:** Host toolchain environment, not repo code.

## Symptom

`cargo check --manifest-path native/Cargo.toml` (cargo 1.96.0 + rustc 1.96.0,
2026-05-25) compiles registry deps fine until proc-macro/config-heavy crates
(icu_*, strsim, litemap, time-core, ident_case, utf8_iter, writeable), then
dies per-crate with:

```
error: multiple input filenames provided (first two filenames are
`.../registry/src/.../strsim-0.11.1/src/lib.rs` and `values())`)
```

i.e. rustc receives `values(...)` as a separate argv entry instead of part of
a `--cfg`/`--check-cfg` argument — argument splitting happens between cargo's
invocation and rustc's parse (quoting mangled, possibly AV/shell interference
on Windows; no RUSTFLAGS/CFLAGS/CARGO_BUILD_RUSTFLAGS are set).

## Scope

Reproduced on two independent repos: `raspberrypi-mcp/native` (fresh Tauri 2
scaffold) and `jtag-swd-mcp/native` (existing). Same failure mode, different
dependency trees → environmental, not per-repo.

## Impact on this build

`raspberrypi-mcp` ships `native/` uncompiled (sources adapted and constant-checked,
tauri.conf/Cargo/hooks verified by inspection, `frontendDist` built and present)
with no local `cargo check` green and no NSIS artifact. Same standing as every
other fleet repo until the toolchain is fixed.

## Fix (for whoever owns the Rust toolchain)

1. `rustc --print sysroot` sanity + a hello-world `cargo new --bin` check
   outside the fleet (isolates fleet config vs toolchain).
2. Try `cargo check` with `--offline` (done — same failure, rules out network).
3. Inspect exact rustc invocation (`cargo check -v`) to see where `values(...)`
   splits; compare against a known-good 1.96 install.
4. Suspects in order: overzealous AV hooking CreateProcess command lines,
   a `config.toml` rustflags entry upstream (`%CARGO_HOME%/config.toml`),
   sccache/rustc-wrapper interference.

## Fleet rule (proposed)

No new proposal — but `cargo check` on `native/` cannot be a silent skip in
assfix: if it fails identically on two repos, file it here instead of waving
each repo through individually.
