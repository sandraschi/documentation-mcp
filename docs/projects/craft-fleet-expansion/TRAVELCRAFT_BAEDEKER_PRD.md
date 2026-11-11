# TravelCraft & The Spatial CountryCraft Engines (Baedeker 2030)
**Concept Paper, Product Requirements Document (PRD) & Epistemic Research Foundation**

**Document Identifier**: `CRAFT-PRD-2026-GEO-001`  
**Version**: 1.0.0-PROPOSAL  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Spatial Chrono-Cartography, Deep Cultural Intelligence, Multimedia Journey Synthesis  
**Standard Control Port**: 14123 (TravelCraft), 14124 (AustriaCraft), 14125 (JapanCraft)  
**Target Enterprise / Commercialization**: Ready for Storytold licensing or sovereign fleet deployment  

---

## 1. Executive Summary & Epistemic Thesis

### The Tragic Degradation of Modern Travel Software
Modern digital travel tools have deteriorated into **monetization funnels and SEO garbage dumps**:
- **TripAdvisor, Yelp, Google Maps**: Plagued by bot reviews, paid sponsored placements, fake influencers, and generic "Top 10 Tourist Traps".
- **Booking.com, Expedia**: High-pressure urgency banners ("Only 1 room left! 14 people looking at this!"), obscured pricing, and zero cultural depth.
- **Lonely Planet / Generic E-Books**: Flat, static, outdated PDFs with no live geospatial context, no temporal scheduling, and zero personalization.

### The Vision: Baedeker 2030 (Chrono-Spatial Cultural Hyper-Guides)
In the 19th and early 20th century, **Karl Baedeker** revolutionized world travel not through advertising, but through **obsessive, peerless editorial rigor, hand-drawn typography, detailed architectural cross-sections, and deep historical context**.

**TravelCraft** revives this golden age with 21st-century sovereign intelligence. It is **Baedeker 2030**: an offline-first, pure-Rust spatial engine that fuses **cartography, 3D photogrammetry/Gaussian splats, literary narratives, archival photography, high-resolution transit topologies, and real-time scheduling** into a magnificent personal travel atelier.

---

## 2. The CountryCraft Regional Archetypes

TravelCraft acts as the master platform engine, while specialized **CountryCraft** instances deliver hyper-vertical cultural immersion:

```
                          ┌─────────────────────────────┐
                          │         TravelCraft         │
                          │   (Master Spatial Engine)   │
                          └──────────────┬──────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
 ┌──────────────┐                 ┌──────────────┐                 ┌──────────────┐
 │ AustriaCraft │                 │  JapanCraft  │                 │ NordicCraft  │
 │  (Mitteleuropa                 │ (Nihon Chrono-                 │ (Fjords, Sagas│
 │   Kultur &     │                 │  Spatial &   │                 │ & Wilderness)│
 │   Alpine Eng.) │                 │  Wayfinding) │                 │              │
 └──────────────┘                 └──────────────┘                 └──────────────┘
```

### 🇦🇹 1. AustriaCraft (Vienna, Alps & Habsburg Kultur)
- **Fleet Repos Consolidated**: `vienna-life-assistant`, `vienna-registry`, `vienna-ai-building-corp`, `publictransport-mcp`.
- **Specialized Cultural Modules**:
  - **Wiener Kaffeehaus & Gastronomie Cadastre**: Archival guide to historic coffeehouses, pastry genealogies (Sachertorte vs. Imperial), wine taverns (Heurige), and strict non-tourist cellar dining.
  - **Archival Architecture & Biedermeier-to-Jugendstil 3D Walkers**: Otto Wagner Stadtbahn pavilion cross-sections, Looshaus, and Ringstraße historical slider (view the same street corner in 1895, 1928, and 2026).
  - **Alpine Topography & Bergtouren**: High-precision Swiss/Austrian DEM elevation contour integration, mountain hut (Alpenvereinshütten) availability, and weather risk vectors.

### 🇯🇵 2. JapanCraft (Chrono-Spatial Nihon Wayfinding)
- **Fleet Repos Consolidated**: `japanophile-mcp`, `publictransport-mcp`, `bakemono-runter`.
- **Specialized Cultural Modules**:
  - **Complex Shinkansen & Transit Graph**: Accurate transfer timing down to the track platform, car door alignment, and Ekiben (train bento) regional guides.
  - **Culinary & Soba/Ramen/Kaiseki Protocol**: Etiquette engines, reservation secret methods (table check / omakase vetting), and hyper-local regional specialties (e.g., Sanuki Udon vs. Wanko Soba).
  - **Onsen & Ryokan Vetting**: Tattoo policy verification, mineral composition analysis (sulfur, carbonated, iron), architectural epoch, and bath rotation schedules.
  - **Shrine & Temple History (Goshuin Registry)**: Digital stamp collection journal, seasonal night illuminations, and Zen rock garden viewing guides.

---

## 3. Core Technical Architecture & Stigmergic Pipelines

```
Layer 4: Multimedia Presentation Atelier
  • Interactive vector map canvas (MapLibre GL / wgpu tiles)
  • 3D Gaussian splat / photogrammetry viewer (walk historic palaces before visiting)
  • Export to ArtCraft: compile custom 80-page leather-bound print guide (DesignCraft / PdfCraft)
──────────────────────────────────────────────────────────────────
Layer 3: Temporal & Wayfinding Engine (travelcraft-core)
  • Multi-modal routing: walking + bicycle + heritage tram + regional rail
  • Crowd-avoidance algorithms: calculating tourist density waves
  • Solar azimuth tracking: "When does golden-hour hit the cathedral stained glass?"
──────────────────────────────────────────────────────────────────
Layer 2: Sovereign Knowledge & Epistemic Depot (DatabaseCraft)
  • Local offline SQLite/GeoPackage spatial database (OpenStreetMap extract + POIs)
  • Vector RAG: semantically search literary travel essays, historical accounts, poems
  • Immutable expense, booking, and ticket voucher ledger
──────────────────────────────────────────────────────────────────
Layer 1: Offline Cache & Telemetry HAL
  • GPX/KML logger, offline tile packager, NMEA GPS receiver bridge
```

---

## 4. Product Requirements Document (PRD)

### 4.1 Functional Requirements
- **FR-01: 100% Offline Autonomy**: Once a regional pack (e.g., `austria_tyrol.craft` or `japan_kyoto.craft`) is downloaded, zero network connection is required. Maps, elevations, routing, and historical notes function in deep subway tunnels and alpine valleys.
- **FR-02: Chrono-Spatial Sliders**: UI slider allowing the user to view historic maps (e.g., Vienna 1860, Edo Tokyo 1845) seamlessly blended over current GPS coordinates.
- **FR-03: Bespoke Print Guide Generation**: 1-click integration with **ArtCraft (`DesignCraft`)** to lay out, typeset, and bind a personalized, publication-grade hardcover travel guide with custom maps, trip schedules, and note pages.
- **FR-04: Sovereign Ticket & Vouchering Vault**: Encrypted on-device storage of boarding passes, train QR codes, and hotel confirmations; zero third-party telemetry.

### 4.2 Universal Command Bus API (`travelcraft-core`)

```rust
pub enum TravelCommand {
    LoadRegionPack { pack_path: String },
    PlanItinerary { constraints: TravelConstraints },
    CalculateRoute { origin: GeoCoord, dest: GeoCoord, mode: TransitMode },
    QueryCulturalPoi { bounds: GeoBounds, category: String, era: Option<String> },
    SynthesizePersonalBaedeker { format: ExportFormat },
    AuditTripExpenses { currency: String },
}
```

---

## 5. Epistemic Research Bibliography & Academic Foundation

1. **Baedeker, Karl** (1861). *Handbook for Travellers: Austria, Northern Italy, and Central Germany*. Coblenz: Verlag von Karl Baedeker. *(The foundational canon of objective, uncorrupted cultural wayfinding)*.
2. **Lynch, Kevin** (1960). *The Image of the City*. MIT Press. *(Mental maps, paths, edges, nodes, landmarks, and spatial cognition)*.
3. **Tufte, Edward R.** (1990). *Envisioning Information*. Graphics Press. *(Micro/macro readings, spatial-temporal layering, and high-density cartography)*.
4. **Schivelbusch, Wolfgang** (1986). *The Railway Journey: The Industrialization of Time and Space in the Nineteenth Century*. University of California Press. *(Perception of landscape and transit topologies)*.
5. **Kerouac, Jack** (1957) & **Bashō, Matsuo** (1694). *Oku no Hosomichi (The Narrow Road to the Deep North)*. *(Literary journey narratives and poetic spatial grounding)*.
