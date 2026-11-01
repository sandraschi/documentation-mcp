# Early Computing Greats & Software Architecture History (1975–1995)

> *"A collection of the foundational platforms, revolutionary paradigms, and legendary software monuments that forged modern personal computing."*

---

## 1. The S-100 Bus & The Genesis of Modular Microcomputing (1975–1981)

Before standard IBM AT buses, PCI, or USB existed, the microcomputer revolution was born on the **S-100 Bus (IEEE 696)**:

* **The Architecture**: Created by Ed Roberts for the **MITS Altair 8800** in 1975, the S-100 bus consisted of a 100-pin passive motherboard backplane into which functional cards (CPU, DRAM, static RAM, serial I/O, floppy disk controllers, video cards) plugged directly.
* **The Multivendor Ecosystem**: IMSAI, Cromemco, North Star, Vector Graphic, and Seattle Computer Products built interoperable S-100 hardware. Enthusiasts and engineers configured custom computing racks powered by Intel 8080, Zilog Z80, and Motorola 68000 boards running CP/M.
* **The First 16-bit Milestone**: In 1979, **Seattle Computer Products (SCP)** released their legendary **S-100 8086 CPU Board**—one of the very first operational 16-bit microcomputer systems in the world, capable of addressing a massive 1 MB of RAM when 64 KB was the desktop standard.

---

## 2. 86-DOS / QDOS: The Framed Relic (Serial #87) & The Paterson Genesis

Before Microsoft bought it, DOS was written in Seattle by a single 27-year-old engineer named **Tim Paterson**:

* **Quick and Dirty Operating System (QDOS)**: In early 1980, Digital Research was late delivering CP/M-86 for the new 16-bit Intel 8086 CPU. To sell their S-100 8086 boards, Seattle Computer Products tasked Tim Paterson with writing an internal 16-bit operating system.
* **Architecture**: Paterson created QDOS (later rebranded **86-DOS**) in just four months. He adopted CP/M-style system calls and file control blocks (FCBs) for easy software porting, but replaced the primitive CP/M filesystem with a robust **FAT (File Allocation Table)** disk structure.
* **The 8-Inch Floppy Relic**:
  * Original 86-DOS copies were shipped by SCP on **8-inch floppy disks** (often colloquially called 9-inch by European engineers due to protective sleeves) for S-100 systems.
  * **Historic Disk Serial #87**: An authentic, framed 8-inch Seattle Computer Products 86-DOS disk bearing serial #87 predates the watershed July 1981 transaction in which Bill Gates and Paul Allen bought all rights to 86-DOS for **\$50,000**, rebranded it as PC-DOS 1.0 for IBM, and established Microsoft's multi-decade desktop monopoly.

---

## 3. Ashton-Tate Framework & The FRED Language: The Lost Paradigm

Designed by **Robert Carr** and **Marty Rubinstein** (Forefront Corporation, released by Ashton-Tate in 1984), **Framework** was arguably the most intellectually sophisticated integrated environment ever conceived for personal computers.

```
Apps  Disk  Create  Edit  Locate  Frames  Words  Numbers  Graphs  Print
┌─[ KRAFTWERK-WIEN: TURBINEN & TELEMETRIE ]─────────────────────────┐
│ BLOCK  SOLL_MW  IST_MW   TEMP_C  DRUCK_BAR  STATUS                │
│ T1      240.0   238.4    542°C    164.2     NOMINAL               │
│ T2      240.0   241.1    538°C    165.0     NOMINAL               │
│ G3      120.0   119.8    495°C    120.5     NETZEINSPEISUNG       │
└───────────────────────────────────────────────────────────────────┘
┌─[ ENERGIE-TAGESBILANZ (Spreadsheet) ]─────────────────────────────┐
│ ZEIT   ERZEUGUNG_MWH  VERBRAUCH_MWH  NETZ-SALDO   FRED-FORMEL    │
│ 08:00     598.2           540.0        +58.2      @SUM(B1:B3)    │
│ 09:00     612.4           585.1        +27.3      @DELTA(SALDO)  │
└───────────────────────────────────────────────────────────────────┘
[FRED]: @SUM(Turbinen.IST_MW) -> 599.3 MW NOMINAL (15 Jahre Betrieb)
```

### The Concept of "Frames"
* **Document-Centric, Not Application-Centric**: Unlike modern office suites where users launch separate Word, Excel, and Access applications, Framework was built entirely around nested **"Frames"**.
* A Frame could contain a word processor document, a relational database table, an active calculating spreadsheet, a business graph, or an outline. Frames could be nested indefinitely inside other frames.
* **FRED (Frame Editor Language)**:
  * A full functional/procedural programming language with Lisp-like elegance.
  * Calculations were live across frames: a database frame tracking industrial telemetry could feed fields directly into a spreadsheet frame using formulas like `@sum(Turbinen.IST_MW)`.
  * Developers could create custom menu bars, dialogue boxes, validation rules, and automatic reporting systems.

### Fleet & Field Lore: The 15-Year Viennese Power Plant Deployment
* A custom Framework application was written in FRED for an engineer at an Austrian energy corporation in Vienna (monitoring turbine temperatures, steam pressures, and grid balances).
* Running on a rugged **GRiD Compass / GRiDCase** portable with an amber display, the custom Framework executive cockpit ran continuously in production for **15 years** without a single system corruption or rewrite until the engineer's retirement.
* The engineer famously took personal credit for building the software to impress his corporate superiors—a testament to how bespoke and seamless Framework applications felt.

### The Demise in 1995
When Windows 95 rolled around, Microsoft pushed the monolithic silo model (Word, Excel, Access) and attempted to replicate Framework's compound document model using **OLE (Object Linking and Embedding)**. OLE suffered from heavy resource consumption, broken pointers, and frequent crashes, killing off the lightweight, indestructible text-mode integrated desk paradigm.

---

## 4. Borland Turbo Pascal (1983): The \$49.95 Revolution

In November 1983, **Philippe Kahn** and Danish compiler genius **Anders Hejlsberg** unleashed **Turbo Pascal 1.0**:

* **The Problem It Solved**: In 1983, writing Pascal on an IBM PC required IBM/Microsoft Pascal ($300), which came on three separate floppies, required complex multi-pass batch compilation to disk, took several minutes to compile a few hundred lines, and provided no built-in editor.
* **The Innovation**:
  * Hejlsberg wrote a lightning-fast, single-pass compiler that compiled directly into **RAM** rather than disk.
  * It integrated a WordStar-compatible full-screen code editor directly into the compiler. When an error occurred, the editor opened instantly with the cursor resting on the exact offending token.
  * It compiled **thousands of lines per second**.
* **The Commercial Disruption**: Kahn priced it at **\$49.95** by mail order (unprotected, with a "Book License" that allowed using it anywhere as long as only one person read it at a time).
* **Lineage**: Turbo Pascal evolved into Turbo Pascal with Objects (v5.5), Turbo Pascal 7.0, and eventually **Borland Delphi**. Anders Hejlsberg later moved to Microsoft, where he designed **C#** and **TypeScript**—meaning modern web development still runs on the direct intellectual lineage of Turbo Pascal.

---

## 5. The Hall of Early Software Greats

| Software | Creator / Company | Year | Defining Innovation |
| :--- | :--- | :--- | :--- |
| **Lotus 1-2-3** | Mitch Kapor & Jonathan Sachs | 1983 | Written in 100% hand-tuned x86 assembly. So fast and responsive it became the primary "killer app" that justified the purchase of the IBM PC in corporate America. |
| **WordPerfect 4.2 / 5.1** | Bruce Bastian & Alan Ashton | 1986 | The clean, distraction-free blank screen with `Alt+F3` **Reveal Codes**. Gave users complete deterministic control over printer formatting, dominating the legal and government sectors for decades. |
| **Sidekick** | Philippe Kahn / Borland | 1984 | The first great **TSR (Terminate and Stay Resident)** utility. Pressing `Ctrl+Alt` instantly popped up a notepad, calculator, phone dialer, and ASCII table over whatever DOS program was running. |
| **dBASE II / III** | Wayne Ratliff / Ashton-Tate | 1981 | Developed originally by Ratliff at NASA's Jet Propulsion Laboratory (JPL) under the name *Vulcan*. Standardized the `xBase` database query language and created the enterprise data market. |
| **Brief** | UnderWare (Maurer & White) | 1984 | The ultimate DOS programmer's editor. Featured multi-level infinite undo, regular expression search across files, and a C-like macro language (`B-macro`). |
| **SPI Open Access** | Software Products International | 1984 | European integrated powerhouse. Combined relational databases, financial spreadsheets, 3D graphics, and desk accessories with its own procedural programming language (PRO/DASL). |
| **Clipper** | Nantucket (Nantucket Corp.) | 1985 | The first true compiler for dBASE code (`Summer '87`, `Clipper 5.0`). Allowed developers to compile `.PRG` code into standalone `.EXE` binaries without paying runtime licenses. |

---

## 6. The Industrial Hardware Benchmark: GRiD Systems (1982–1990)

The software greats above found their most rugged and iconic physical embodiment in the portable computers designed by **Bill Moggridge** (co-founder of IDEO) for **GRiD Systems Corporation**:

* **GRiD Compass 1101 (1982)**: The world's first clamshell laptop. Featured a die-cast magnesium alloy tub, Intel 8086, bubble memory, and a glowing amber electroluminescent flat panel. Deployed on **NASA Space Shuttle missions (STS-51-A onwards)** as the SPOC (Shuttle Portable On-Orbit Computer).
* **GRiDCase 1520 (1987)**: IBM PC/AT-compatible 80286 @ 10 MHz with a 10″ Matsushita 640×400 amber gas-plasma display, Micro Switch ST capacitive keyboard, and dual GRiDROM cartridge sockets.
* **GRiDCase 1550 SX (1990)**: The apex of the series. Featured a 20 MHz Intel 80386SX, full 640×480 VGA 16-shade gas-plasma display, the patented **IsoPoint** roller-bar pointing device beneath the spacebar, and interchangeable modular **Power Pods** (blind-mating AC line supply or rechargeable NiCad battery pack).

---

*Preserved for the fleet archive. Cross-referenced in `mcp-central-docs/reference/` and `reversing-mcp/web_sota`.*
