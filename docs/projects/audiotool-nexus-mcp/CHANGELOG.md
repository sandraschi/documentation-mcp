# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-04-14

### SOTA 14.1 Industrialization
- **Biome Migration**: Replaced legacy ESLint and Prettier with **Biome** for high-performance, Rust-powered linting and formatting. Achieved sub-50ms quality checks across the codebase.
- **Tiered Testing Scaffold**: Established a robust testing architecture using **Vitest**.
    - **Unit Tests**: Implemented `src/nexus-bridge.test.ts` using mocked Audiotool SDK to allow offline, credential-free logic verification.
    - **Integration Tests**: Hardened authenticated connectivity tests with environment isolation.
- **Documentation Restructuring**: Overhauled documentation for industrial clarity. Moved technical setup and architecture details into specialized sub-docs in `docs/`.

### Added
- **Industrial Grid UI**: Upgraded the webapp dashboard to a high-fidelity "Industrial Grid" aesthetic, featuring glassmorphism, zinc-base palette, and amber-500 accents.
- **Premium Branding**: Integrated the premium "Audiotool Nexus" industrial logo.
- **Vitest integration tests**: Skips automatically in non-authenticated environments while providing deep coverage for PAT-based sessions.

### Fixed
- **SDK Mocking**: Resolved module-level mocking conflicts in `NexusBridge` unit tests.
- **Environment Isolation**: Hardened tests to ignore local `.env` interference using `vi.stubEnv`.
- **`.env` loading**: Fixed path-based environment loading to support headless launchers and varied working directories.

### Removed
- **Legacy Tooling**: Purged all `node_modules` and configurations related to ESLint and Prettier.

## [0.1.0] - 2026-03-16

### Added
- **Specialized DAW Views**: Implemented `MixerView`, `SamplerView`, and `MasteringView`.
- **Mixer Board**: High-res peak meters (color-graded) and vertical channel strips.
- **Sampler**: Real-time waveform visualization and ADSR parameter controls.
- **Mastering**: FFT spectral analysis and RMS/Peak precision gauges.
- **Connection Handshake**: Implemented secure session establishment flow in the webapp.
