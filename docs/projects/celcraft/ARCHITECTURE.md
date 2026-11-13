# CelCraft — System Architecture & Technical Specification

**Document Version:** 1.0.0
**Date:** 2026-11-11
**Status:** Approved
**Parent Standard:** [`standards/RUST_ARTCRAFT_STANDARD.md`](../../standards/RUST_ARTCRAFT_STANDARD.md)

---

## 1. Architectural Philosophy & Principles

CelCraft is built around three inviolable principles:
1. **Total Decoupling of Engine & Presentation:** The core raster and document engine (`cel-core`, `cel-tlv`) has zero knowledge of `egui`, `wgpu`, or any UI library. It can be run headlessly in CI, in microservices, or driven by autonomous AI agents.
2. **Dual-Channel 32-Bit Packed Pixels:** Unlike standard 32-bit RGBA buffers where line and fill overwrite each other destructively, CelCraft preserves the ink skeleton and fill region independently within a single 32-bit word.
3. **Provable Safety & Zero Panics:** Pure safe Rust (`forbid(unsafe_code)`), strict clippy deny walls (`unwrap_used`, `expect_used`, `panic`), bounded memory access, and structured error handling.

---

## 2. Workspace Crate Taxonomy

```text
               ┌────────────────┐
               │    cel-mcp     │  (L2: CLI + MCP stdio server)
               └───────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       │                               │
       ▼                               ▼
┌──────────────┐               ┌──────────────┐
│    cel-ui    │               │  cel-render  │  (wgpu DAG & Export)
└──────┬───────┘               └──────┬───────┘
       │                              │
       └───────────────┬──────────────┘
                       │
                       ▼
               ┌────────────────┐
               │    cel-core    │  (L1: Document AST, Palettes, X-Sheet, Bus)
               └───────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌──────────────┐┌──────────────┐┌──────────────┐
│   cel-tlv    ││   cel-dsp    ││  cel-audio   │
└──────────────┘└──────────────┘└──────────────┘
```

| Crate | Layer | Primary Responsibilities |
|---|---|---|
| `cel-core` | L1 Core | Document AST, project seeder, palette models, X-sheet matrix, transaction log, BLAKE3 CAS, and the universal `Command` bus |
| `cel-tlv` | L1 Engine | Dual-channel 32-bit packed raster canvas, ink-over-paint blending, SIMD scanline fill, autogap barriers, vector tape |
| `cel-dsp` | L1 Signal | Acme/Oxberry peg registration, Sauvola adaptive binarization, SAT / Integral Images, optical flow |
| `cel-render` | L1 Render | Evaluator DAG, `wgpu` compute shaders, 2.5D normal map synthesis, OpenEXR 16F and Apple ProRes 4444 streaming |
| `cel-audio` | L1 Audio | CPAL playback, jog/shuttle scrub micro-bursts, vertical waveform cache, LPC formant acoustic lip-sync |
| `cel-mcp` | L2 Driver | CLI-first binary (`clap` + `--json`) and pure-stdio MCP JSON-RPC 2024-11-05 driver executing `cel_core::dispatch` |
| `cel-ui` | L3 App | Native GPU desktop workstation (`egui` / `eframe`), spreadsheet X-sheet, canvas viewport, radial HUD |

---

## 3. Memory Layout: Packed Dual-Channel Pixel (`cel-tlv`)

### 3.1 32-Bit Bitfield Structure

```text
 Bit 31                                                            Bit 0
 [  flags  ] [   ink_tone   ] [     paint_style     ] [      ink_style      ]
   4 bits        8 bits              12 bits               12 bits
 (0xF0000000) (0x0FF00000)        (0x000FFF00)          (0x000000FF)
```

- **`ink_style` (Bits 0–11, 12 bits):** Swatch index from $1$ to $4095$. Value $0$ denotes empty / no line.
- **`paint_style` (Bits 12–23, 12 bits):** Swatch index from $1$ to $4095$. Value $0$ denotes transparent / unpainted.
- **`ink_tone` (Bits 24–27 + 28–31 overlap, 8 bits):** Anti-aliased edge coverage / alpha opacity ($0$ to $255$).
- **`flags` (Bits 28–31, 4 bits):** Autogap barrier bit, region lock bit, protected contour bit.

### 3.2 Ink-Over-Paint Compositing Equation

When rendering a pixel to RGBA, the engine looks up the linear float colors $\mathbf{C}_{\text{paint}}$ and $\mathbf{C}_{\text{ink}}$ from the active Palette LUT:

$$\mathbf{C}_{\text{final}} = \operatorname{lerp}\left(\mathbf{C}_{\text{paint}}, \mathbf{C}_{\text{ink}}, \frac{\text{ink\_tone}}{255.0}\right)$$

If $\text{ink\_style} == 0$, $\mathbf{C}_{\text{final}} = \mathbf{C}_{\text{paint}}$.
If $\text{paint\_style} == 0$, $\mathbf{C}_{\text{final}} = \mathbf{C}_{\text{ink}} \cdot \frac{\text{ink\_tone}}{255.0}$.

This mathematically eliminates all white fringes or antialiased halo seams when artists recolor lines or fill areas.

---

## 4. Directional Autogap Containment & Scanline Fill

### 4.1 Tangent Extraction & Collinear Convergence
1. **Endpoint Extraction:** Locate line terminals using $3 \times 3$ connectivity ($N_8$).
2. **Skeleton Backtracking:** Backtrack $k=5$ pixels along the skeleton to compute departure vector:
   $$\vec{v}_{\text{dep}} = \frac{P_{\text{term}} - P_{-k}}{\|P_{\text{term}} - P_{-k}\|}$$
3. **Bridge Validation:** A candidate gap pair $(P_A, P_B)$ with vectors $(\vec{v}_A, \vec{v}_B)$ is bridged if:
   - Distance: $\|P_A - P_B\|_2 \le d_{\text{max}}$
   - Forward Cone: $\frac{(P_B - P_A) \cdot \vec{v}_A}{\|P_B - P_A\|} \ge \cos(\theta_{\text{cone}})$
   - Opposing Arrival: $\vec{v}_A \cdot \vec{v}_B \le -\cos(\theta_{\text{align}})$
4. **Transient Barrier Mask:** Rasterize Bresenham line segments into a 1-bit barrier mask.

### 4.2 Fill Bleed & Core Halt
The scanline fill algorithm traverses horizontal spans. For each pixel:
- If `ink_tone < 180`, the paint style is applied underneath the semi-transparent edge.
- If `ink_tone >= 180` or the barrier bit is set, the scanline halts.

---

## 5. GTS Scan Alignment & Adaptive Sauvola Binarization (`cel-dsp`)

### 5.1 Acme / Oxberry Peg Registration
Standard animation pegs use 3 punched holes:
1. **Center Circular Hole:** Aspect ratio $\approx 1.0$, solidity $> 0.90$. Defines translation $(x_c, y_c)$.
2. **Two Outer Rectangular Slots:** Aspect ratio $2.0–4.5$. The centroid line between slots defines rotation angle $\theta$.
3. **Rigid Affine Warp:** Warps the scanned cel into absolute canvas coordinates with sub-pixel bilinear interpolation:
   $$\mathbf{M} = \begin{bmatrix} \cos\theta & -\sin\theta & x_c \\ \sin\theta & \cos\theta & y_c \\ 0 & 0 & 1 \end{bmatrix}$$

### 5.2 Constant-Time Sauvola Binarization ($O(1)$)
Calculates local threshold over window $W$:
$$T(x,y) = m(x,y) \cdot \left[1 + k \cdot \left(\frac{s(x,y)}{R} - 1\right)\right]$$
where $m(x,y)$ and standard deviation $s(x,y)$ are computed from Integral Images (Summed-Area Tables) in constant time $O(1)$ per pixel, independent of window radius.

---

## 6. The Universal Command Bus (`cel-core`)

All capabilities execute through the `Command` enum:
- `Command::Status` $\to$ Returns engine health, canvas metrics, and memory usage.
- `Command::ProjectNew` $\to$ Initializes a new project, resolution, and palette.
- `Command::PaletteList` $\to$ Lists swatches in the active palette.
- `Command::PaletteSetSwatch` $\to$ Updates a swatch RGBA value in the LUT.
- `Command::XSheetGet` $\to$ Returns exposure matrix slice.
- `Command::XSheetSetCell` $\to$ Modifies a cell's level and frame index.
- `Command::CanvasInfo` $\to$ Inspects dual-channel buffer dimensions and active styles.
- `Command::DemoScene` $\to$ Seeds deterministic production presets (Ghibli, Cyberpunk, 80s OVA).

Dispatched via:
```rust
pub async fn dispatch(cmd: Command) -> serde_json::Value;
```
Ensuring complete fidelity between CLI, MCP, and Desktop UI.
