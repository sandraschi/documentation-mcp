# Digibib5.exe — reversing status (mirror)

**Mirrored from:** `D:\Dev\repos\reversing-mcp\docs\status.md` (source of truth).  
**Program:** `Digibib5.exe` (Ghidra `/Digibib5.exe`).  
**Companion (upstream repo):** [DIGIBIB_DECOMPILE_PLAN.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIGIBIB_DECOMPILE_PLAN.md) · [GHIDRA.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/GHIDRA.md)

**Reference volumes (local):** `L:\Multimedia Files\Written Word\Digitale Bibliothek\` — per-volume `Data\` holds `TEXT.DKI` / `Text.dki`, `TREE.DKI`, etc.

Last mirrored: 2026-03-23.

---

## Fleet notes (high level)

- Zlib is **embedded** (no zlib DLL in IAT by name). **`FUN_0050b524`** → **`FUN_0051467c`** for zlib init/error strings; PNG/zlib paths use **`FUN_0050c338`** etc.
- **`FUN_0061c0f4`** registers `data\…` paths and accumulates **64-bit total file size**; **`FUN_00616af0`** is the **`Text.dki` loader** that **reads bytes**.
- Registrar object at **`obj+0x60`**: VMT **`~0x0041b6a4`**; **`+0x88`/`+0x8c`** = sorted string list **insert** / **binary search** (not file I/O).

---

## Text.dki format (draft)

- **Hex sample (confirmed magic path):** `L:\...\DB006\Data\Text.dki` — first **16** bytes: **`CC 24 19 00  04 00 00 00  74 DF 00 00`** → LE dwords **`0x001924CC`**, **`0x00000004`**, **`0x0000DF74`**. Matches **`FUN_004c6f88`** magic check. After **`Seek(0)`** + **`Read` 0xC**, code maps **dword0 → `*(obj+0x20)`** (same magic) and **dword1 → `*(obj+4)`**; on this file **`*(obj+4)==4`** drives the **immediate** follow-on **`Read`** of **`4×4=16`** bytes (payload starts at file offset **0x0C** with **`84 FC 0A 00 …`**).
- **Third header dword (`0xDF74` on DB006):** present in the **12-byte** post-rewind read but **not** assigned to **`obj+4`** in **`FUN_00616af0`** decompilation — treat as **parallel metadata** (e.g. total index slots / section size) until a consumer xref names it; it is **not** the length passed to the **second `Read`** in that function.
- **Other on-disk families:** **`DB008\Data\TEXT.DKI`** begins **`56 17 00 00 …`**; **`DB002\Data\TEXT.DKI`** begins **`95 0D 01 00 …`** — **not** **`0x001924CC`**; likely **older or alternate `text.dki` layout** (still **LE dword tables**). Digibib5 may branch on magic or volume revision.
- **Magic:** First **4** bytes **`0x001924CC`** (LE **`CC 24 19 00`**) when using the **`FUN_00616af0`** / **`FUN_004c6f88`** path.
- **Seek:** **`FUN_00420598`** → **`TStream::Seek` at VMT `+0x18`** (rewind before the **12-byte** header read).
- **Payload buffer:** **`obj+0xc`**, **`Read`** length **`*(obj+4) << 2`** for the **first** bulk slice right after header parse; interpreted as **`uint32_t[*(obj+4)]`** for that slice. Larger index data may be loaded in **other routines** (e.g. **`FUN_00616cdc`** / view refresh).
- **Checksum:** no validation in **`FUN_00616af0`** after read; flags only **`obj+0x1c`**, **`obj+0x10`**.

---

## Consumers of `Text.dki` loader / `obj+0xc` table

**`FUN_0061a880`** (sole incoming xref **`FUN_0072af44`**, also from **`entry`** via app shell): builds the **main document / library shell**. It calls **`FUN_00616af0`** and stores the returned object pointer at **`host+0xcc`**. That value is the **Delphi “text index” object** holding stream handle, **`obj+0xc`** dword table pointer, **`obj+0x4` / `obj+0x20` header fields**, and flags; downstream **UI** and **layout** code (e.g. **`FUN_00613458`** → **`FUN_00616dc0`**) use it to **resize line buffers** and **`Read`** **word-count / dimension** data from the same **`TStream`**, not to reinterpret **`obj+0xc`** as strings.

**`FUN_00616dc0`** (incoming **`FUN_00613458`** only): **pagination / line-layout** when the user changes position. It takes **`*(view+0x210)+0xcc`** (same **`Text.dki` loader object**), rewinds the stream when loaded, and either reads **6 bytes** into **ushort** metadata or calls **`FUN_004c6f9c`** for a **single-word** metric when **`obj+0x20==1`**, then **reallocates** a **host buffer** (`*param_3`) sized **`count + 0x5dc`** and **`Read`**s **`count`** bytes into it — so it **consumes the binary index stream** for **geometry / run lengths**, while the **`uint32[]`** at **`obj+0xc`** remains the **in-memory offset table** from the **first** **`FUN_00616af0`** slice for other readers.

---

## Sorted-table compare (VMT `+0x34`)

- Slot **`+0x34`** on the same VMT as **`FUN_0042013c`** resolves to **`0x00420544`**: delegates to **`FUN_0040beb8`** or **`FUN_0040bf08`** → **`CompareStringA`** on **Delphi string contents** (flag **`*(obj+0x1e)`** picks **case-sensitive vs case-insensitive** sort). Keys are **string identity**, not a separate hash column.

---

## Open

- Map **`FUN_00614bb4` / `FUN_006154e4`** and friends to **which fields** of **`obj+0xc`** they index for hit-testing / search.
- Label **`0x001924CC`** vs **`0x00001756`** families (version field at **dword@4** vs different file type).
