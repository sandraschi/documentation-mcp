# stockcraft

Local-first inventory & light warehouse management (*Lagerhaltung*) in the Back-Office Craft Suite (`d:\Dev\repos\stockcraft`).

- **L1 (`stockcraft-core`)**: SQLite WAL store, immutable `movements`, integer-cent moving-average valuation, *Inventur*, `pick_lists`, `craft-biz` bus intake/outbox.
- **L2 (`stockcraft-mcp`)**: Dual CLI + MCP `2024-11-05` stdio server (`19` `stock_*` tools).
- **L3 (`stockcraft-app`)**: Native `egui 0.37` desktop workstation over `craft-biz-ui` (`Shell` + `SuiteApp`).
