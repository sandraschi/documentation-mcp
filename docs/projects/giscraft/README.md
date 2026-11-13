# GISCraft

**Version**: v0.1.0 — Sovereign Geographic Information Systems & Geospatial Analysis Studio.
**Repository**: [`d:\Dev\repos\giscraft`](file:///d:/Dev/repos/giscraft) | [GitHub: sandraschi/giscraft](https://github.com/sandraschi/giscraft)
**Ports**: Frontend `11253` | Backend `11254` (Axum REST `/api`)
**Parent Suite**: Sovereign Craft Suite / Spatial

---

## Architecture

```
giscraft-backend (Axum Sidecar, GeoTIFF / Shapefile / PostGIS Query Engine)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
  FastMCP Endpoint (11254)                     giscraft-frontend (11253)
(Spatial Queries & Vector Layers)             (Vite React / OpenLayers Canvas)
```

- Local-first map tiles, vector shapefiles, and GeoJSON layer inspection.
- Geocoding and route planning without external commercial API dependencies.
