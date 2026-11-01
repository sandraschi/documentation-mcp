# The Young Dev's Illustrated Primer to Sovereign Agentic Wizardry
*(Or: A Guide for the Perplexed on How to Wield a 300-Repo Fleet with a \$20 Claude Account)*

> *"In the olden days (circa 2023), developers spent forty hours a week typing boilerplate syntax, wrestling with webpack configs, and arguing on Stack Overflow about missing semicolons. Today, you are an air-traffic controller of synthetic cognition. You sit in your workshop with an RTX 4090, a humble \$20/mo model account, and a fleet of robot-handles. Here is how you live like a 21st-century sorcerer without burning VC money."*

---

```mermaid
flowchart TD
  Brain["The \$20 Brain<br/>(Claude Opus / Bonsai Local)"]
  Fleet["The Sovereign MCP Fleet<br/>(300+ Robot Handles)"]
  
  Brain --> Fleet
  
  Fleet --> C1["🎮 Ch 1: Forge Worlds in GameCraft"]
  Fleet --> C2["💾 Ch 2: Attic Clunker Necromancy (ReviveCraft)"]
  Fleet --> C3["⚡ Ch 3: The Desk Lab Workbench"]
  Fleet --> C4["📐 Ch 4: Etch Silicon & PCBs (KiCraft)"]
  Fleet --> C5["🧠 Ch 5: The BCI Thinking Cap"]
  Fleet --> C6["📦 Ch 6: Shop Shenzhen like Li Mingxing"]
  Fleet --> C7["📐 Ch 7: Lean 4 Proofs without a Math PhD"]
```

---

## Chapter 1: Conjure a Living World in `gamecraft`
*“You don’t code pixels. You direct a simulation.”*

You want to make a game. In the old world, you'd spend three months watching Godot shader tutorials and fighting import pipelines. 
In the sovereign fleet, you open Claude, point it at **`gamecraft`** (and its siblings `godot-mcp` + `blender-mcp`), and say:
> *"Spawn a procedural low-poly dungeon, scatter 50 physics crates with PBR wood shaders, wire an orbit camera with WASD dampening, and export an HTML5 WebAssembly bundle."*

Before your espresso cools down, the agent drives Godot’s scene tree via MCP tools, constructs the node hierarchy, assigns PBR textures from GIMP, spins up GPU particle embers, and hands you a playable local web link. You are no longer a typist; you are the lead director of an automated studio.

---

## Chapter 2: Attic Necromancy with `reversing-mcp` *(The Artist Formerly Known as ReviveCraft)*
*“That dusty 1998 CD-ROM from your uncle's attic is not dead. It is just sleeping.”*

You found a forgotten 16-bit Windows game or a proprietary industrial binary from 2002 whose vendor went bankrupt during the Bush administration. The file format is completely undocumented, binary blobs refuse to boot, and modern Windows spits out compatibility errors.

**Enter `reversing-mcp`:**
1. Point Claude at the raw `.exe` or `.dki` file with `analyze_binary` and `extract_strings`.
2. The agent drives headless Ghidra behind the scenes, cross-referencing function addresses, resolving DLL import tables, and decompiling obfuscated C loops into readable pseudocode.
3. The LLM reads the decompiled disassembly: *"Aha! Offset 0x00401A20 expects an obsolete 8-bit palette buffer."*
4. It writes a modern Rust compatibility shim or Python extractor in 90 seconds. The clunker lives again.

---

## Chapter 3: The Frankenstein Maker Bench
*(Multimeter, Oscilloscope, Logic Analyzer, Power Supply)*

You want to build real physical hardware, but you don't have a \$50,000 Keysight laboratory rack. What you do have is a \$40 USB multimeter, a \$60 handheld digital oscilloscope, and a Raspberry Pi. Where did you leave that script again?

Don't panic. The bench is unified:
* **`multimeter-mcp`** (`dmm_run`): Measures real DC voltage and checks circuit continuity.
* **`oscilloscope-mcp`**: Captures raw signal waveforms and feeds them straight to Claude to diagnose ripple noise.
* **`logic-analyzer-mcp`**: Sniffs SPI/I2C packet bytes off the pins in real-time.
* **`power-supply-mcp`**: Sets voltage limits and guards against fried circuits.

You clip the leads to a mystery board, tell Claude: *"Watch pin 4. Ramp the voltage from 3.3V to 5V and tell me when the microcontroller starts emitting serial packets."* Claude monitors the USB telemetry, graphs the waterfall, and tells you: *"Serial output detected at 115200 baud on 4.8V. We're in."*

---

## Chapter 4: Etch Real PCBs with `kicad-mcp` *(KiCraft)*
*“Why breadboard when you can spin real copper?”*

You designed a custom ESP32 macro-pad. Traditionally, drawing schematics, routing 40 traces, and checking design rules in KiCad takes a weekend of eye-strain.

With **`kicad-mcp`**:
1. You describe the circuit in plain English: *"Connect GPIO 14, 15, and 16 to three Cherry MX switches with 10k pull-up resistors and an OLED display on I2C."*
2. The agent emits valid KiCad schematic S-expressions, places footprints, routes net connections, runs the Design Rule Check (DRC), and spits out production-ready Gerber files.
3. You zip the folder and upload it directly to JLCPCB. Total human design time: 12 minutes.

---

## Chapter 5: The BCI Thinking Cap with `openbci-mcp`
*“Look, ma, no hands!”*

You strap on an OpenBCI Ultracortex headset or a 4-channel EEG headband. It spits out microvolt spikes, alpha waves, and raw biosensor noise that looks like an earthquake seismograph.

Through **`openbci-mcp`**:
* The stream flows into local FastMCP bandpass filters.
* Claude correlates your frontal lobe Alpha/Theta ratio in real-time: *"You are losing focus. Pausing heavy compile jobs and dimming the Hue lamps."*
* Spike detection turns hard jaw-clenches or double-blinks into universal command bus triggers: clench twice to trigger an emergency stop on the Yahboom robot car.

---

## Chapter 6: Shop in Shenzhen Like Your Name is Li Mingxing
*“Why pay 5x Amazon markup for a re-badged sensor?”*

You need ten micro-LIDAR sensors, five mecanum wheels, and a pack of STM32 development boards. Amazon wants \$45 per sensor and two weeks shipping.

With **`prc-shopping-mcp`**:
* Claude navigates 1688 and Taobao directly in fluent Chinese.
* It searches wholesale component registries, compares factory batch prices, filters out drop-shippers, translates customer reviews from domestic electronics hobbyists in Guangdong, and calculates consolidator freight forwarding.
* You acquire the exact industrial components at domestic factory cost. You are sourcing hardware like a seasoned Huaqiangbei local.

---

## Chapter 7: Solve Mathematics Conjectures with `leanforge-mcp`
*“Formal mathematical verification without a PhD.”*

You want to prove a theorem or crack an Eötvös competition math puzzle. You don't know Lean 4 syntax, and type-theoretic dependent calculus makes your head spin.

**The Loop of Truth**:
1. You state the mathematical conjecture in plain English.
2. Claude translates it into a candidate Lean 4 proof file.
3. The real, unsparing Lean compiler evaluates the proof.
4. **Compile error!** The compiler spits out: *`type mismatch at term h1`*.
5. Claude reads the exact compiler feedback, adjusts its hypothesis, and tries again.
6. The loop continues until the Lean compiler outputs zero errors: **Verified True.**

No hallucinations. No bullshit. The LLM supplies the creative intuition; the formal compiler supplies the mathematical guarantee.

---

## Epilogue: The Creed of the Sovereign Architect

1. **Own the floor, rent the ceiling**: Run your daily models locally on your GPU for \$0; rent cloud brains only when an Eötvös proof needs raw horsepower.
2. **Never type what an agent can scaffold**: If you are writing boilerplate CRUD or hunting port numbers by hand, you have forgotten your station.
3. **Always verify against ground truth**: Compilers, linters, oscilloscopes, and test suites are your ground-truth oracles. Trust nothing until the green check appears.

*Now go into your workshop and build something impossible.*
