# ReveCraft — Assessment (Retired)

**Status:** Retired / Deleted from `D:\Dev\repos` (2026-11-09) · **Grade:** Retired · **Superseded by:** `D:\Dev\repos\reversing-mcp` (`v2.3.0`)

## Why it was retired

Code audit on 2026-11-09 confirmed that `sandraschi/revecraft` (`933 LOC` Python) was a watered-down copy-paste subset of `reversing-mcp`:
- `ghidra_extensions.py` was a literal copy of `reversing-mcp`'s SNES/65816 Ghidra extension catalog.
- `cli.py` (521 lines) only implemented basic regex string extraction, Shannon entropy, a 30-line `struct.unpack` PE header reader, and subprocess calls to `diec`/`capa`.

Meanwhile, **`D:\Dev\repos\reversing-mcp` (`v2.3.0`, 27 tools across 10 domains)** is already a mature, SOTA reverse-engineering platform unifying:
- Interactive Ghidra decompilation via **ReVa**, **REA** sidecar, **IDA Pro**, **Frida**, **radare2**, **Detect It Easy**, and **capa**
- **ClickerLab (`gym`)**: CUA clickthrough + OCR correlated with static disassembly to produce feature-to-code maps
- Directmedia `.DKI` decompression toolkit and Hercules DJ Console MK1 hardware reverse engineering
- Full React 19 + FastAPI workbench on ports `10750` / `10751`

Because `reversing-mcp`'s core value is orchestrating Python/JVM/CUA engines (PyGhidra, Frida, pywinauto), rewriting it as a Rust craft app or maintaining a duplicate Python toy (`revecraft`) is counterproductive. **`reversing-mcp` is the canonical fleet reversing system.**
