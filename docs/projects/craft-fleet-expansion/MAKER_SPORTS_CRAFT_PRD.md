# MakerCraft & SportsCraft Concept Papers & PRD
**Autonomous Digital Fabrication, Hardware Hacking & Kinetic Athletic Performance Studios**

**Document Identifier**: `CRAFT-PRD-2026-MAKER-SPORT-001`  
**Version**: 1.0.0-PROPOSAL  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Hardware Prototyping, 3D Slicing/G-Code, Computer Vision Biomechanics, Endurance Telemetry  
**Standard Ports**: 14126 (MakerCraft), 14127 (SportsCraft)  

---

# Part A: MakerCraft (The Sovereign Hardware Prototyping Studio)

## 1. Executive Summary: Breaking the Fragmented Hardware Toolchain
Hardware inventors and makers currently endure a miserable, disjointed workflow:
- 3D models in CAD $\to$ Export STL $\to$ Load separate slicer (Prusa/Bambu/Cura) $\to$ Separate firmware flasher $\to$ Separate oscilloscope/logic analyzer GUI $\to$ Disconnected spreadsheet for Bill of Materials (BOM).
- Commercial solutions are pushing aggressive cloud logins (e.g., Autodesk Fusion360 restrictions, Bambu cloud print queues).

### The MakerCraft Solution
MakerCraft is a unified desktop environment that integrates **parametric 3D slicing, CNC/G-code generation, circuit breadboard simulation, multi-meter/logic analyzer telemetry, and automated BOM cost reconciliation**:

```
                       ┌──────────────────────────────┐
                       │       MakerCraft Studio      │
                       │    (egui + wgpu 3D Visual)   │
                       └──────────────┬───────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│  CAD/CAM &   │               │ Electronics  │               │ BOM & Supply │
│ G-Code Engine│               │ & Lab Bench  │               │   Database   │
│ • STL/STEP   │               │ • Logic Anal.│               │ • Octopart/  │
│ • Toolpath   │               │ • Bus Pirate │               │   Digikey    │
│ • Klipper API│               │ • Siglent/Rig│               │ • Local Stock│
└──────┬───────┘               └──────┬───────┘               └──────┬───────┘
       └──────────────────────────────┼───────────────────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │   Physical Machine Control   │
                       │ • 3D Printers (Klipper/Moon) │
                       │ • CNC Routers (GRBL / TinyG) │
                       │ • Laser Cutters (LightBurn)  │
                       └──────────────────────────────┘
```

## 2. MakerCraft Crate Architecture & Fleet Consolidation
- **Fleet Repos Consolidated**: `bus-pirate-mcp`, `function-generator-mcp`, `spectrum-analyzer-mcp`, `kicad-mcp`, `freecad-mcp`.
- **Core Engine (`makercraft-core`)**:
  - Pure-Rust G-Code parser, backplotter, and visualizer.
  - Serial protocol streaming to Klipper (Moonraker API) and GRBL CNC microcontrollers.
  - Circuit logic analyzer packet parser (Bus Pirate & Sigrok libsigrokcxx bindings).
- **DatabaseCraft Integration**: Uses DatabaseCraft's `field_service` or `small_business` inventory tables to track resistor/capacitor bins, filament spools, and parts unit costs.

---

# Part B: SportsCraft (The Biomechanical & Endurance Training Atelier)

## 1. Executive Summary: Overcoming Predatory Cloud Fitness Trackers
Modern athletic tools (Strava, TrainingPeaks, Whoop, Garmin Connect) have become **walled gardens**:
- **Paywalled Physiology**: TrainingPeaks and Strava charge \$12–\$30/month just to view basic fatigue curves (CTL/ATL/TSB) or power duration models.
- **Privacy Intrusion**: Sensitive GPS coordinates of personal home addresses and routes are continuously leaked and mined.
- **Zero Computer Vision Integration**: Wearables track heart rate, but cannot correct running posture, deadlift form, or tennis swings.

### The SportsCraft Solution
SportsCraft is a private, sovereign **endurance performance lab and computer vision biomechanics coach**:

```
                       ┌──────────────────────────────┐
                       │       SportsCraft Studio     │
                       │  (Kinetic Biomechanics HUD)  │
                       └──────────────┬───────────────┘
                                      │
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
┌──────────────┐               ┌──────────────┐               ┌──────────────┐
│  Endurance   │               │ Video Pose & │               │  Club & Race │
│  Physiology  │               │ Biomechanics │               │  Management  │
│ • FIT/GPX/TCX│               │ • MediaPipe  │               │ • Regattas   │
│ • Banister   │               │   Pose Est.  │               │ • Track Roll │
│   Impulse HR │               │ • Joint Vels │               │ • Brackets   │
│ • Critical P.│               │ • Form Alerts│               │ • Live Timing│
└──────┬───────┘               └──────┬───────┘               └──────┬───────┘
       └──────────────────────────────┼───────────────────────────────┘
                                      │
                                      ▼
                       ┌──────────────────────────────┐
                       │  Sovereign Athletic Archive  │
                       │   (DatabaseCraft Powered)    │
                       │ • 100% Private Local Tracks  │
                       │ • Long-term Fatigue & VO2    │
                       │ • Direct Club Blueprints     │
                       └──────────────────────────────┘
```

## 2. Key Capabilities
1. **Algorithmic Biomechanics (Vision AI)**:
   - Feeds video files into an ultra-low latency pose estimation pipeline (21 3D joint landmarks).
   - Measures barbell bar path, spine curvature under load, running cadence/ground contact time, and cycling knee angles.
2. **Mathematical Physiology Engine**:
   - **Banister Impulse-Response Fatigue Model**: Computes Chronic Training Load (Fitness), Acute Training Load (Fatigue), and Training Stress Balance (Form).
   - **Critical Power (Monod-Scherrer & 3-Parameter W')**: Determines anaerobic work capacity and functional threshold power (FTP) without cloud subscriptions.
3. **Synergy with DatabaseCraft's `club` Blueprint**:
   - Manages club memberships, team rosters, seasonal dues, race entries, and regatta heat brackets directly out of the box.

---

## 3. Epistemic Research Bibliography

1. **Banister, Eric W.** (1991). *Modeling Elite Athletic Performance*. Physiological Testing of the High-Performance Athlete, Human Kinetics. *(Mathematical foundations of athletic impulse-response)*.
2. **Allen, Hunter; Coggan, Andrew; McGregor, Stephen** (2019). *Training and Racing with a Power Meter*. VeloPress. *(Normalized power, TSS, and power duration curves)*.
3. **Winter, David A.** (2009). *Biomechanics and Motor Control of Human Movement*. John Wiley & Sons. *(Kinetic joint forces, inverse dynamics, and motion analysis)*.
4. **Watanabe, Makoto** (2018). *G-Code and Digital Machining Principles*. Precision Engineering Review.
