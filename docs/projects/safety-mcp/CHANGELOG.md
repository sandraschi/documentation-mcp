# Changelog

## [0.1.0] - 2026-08-04

### Added
- Initial release: threat forensics and verdict engine
- Collectors: Defender detections/status/threat_info, security event
  channels (4688/4624/4104/Sysmon/custom), network evidence
  (firewall blocks/connections/sniff trigger)
- Verdict engine: evidence gathering + triage chain (ctx.sample ->
  Ollama -> deterministic classifier)
- Deterministic classifier reproduces the PowhidSubExec false-positive
  verdict (cmdline-only dev detections -> benign)
- Bidirectional aiwatcher integration (push verdicts, pull intel)
- SQLite verdict persistence + collector health
- Webapp (11147): graded alert banner, verdict history, event channels,
  chat, logs, settings, help
- Prefab chat cards: show_verdict_prefab, show_health_prefab
- pytest suite (19 tests incl. PowhidSubExec regression) + Playwright e2e
