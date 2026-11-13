# Vis.js (vis-network) & ForceAtlas2 Spatial Layout

**Status**: ACTIVE fleet visualization standard  
**Category**: Frontend Libraries & Graph Visualizers  
**Canonical Path**: `mcp-central-docs/integrations/vis-network-forceatlas2.md`  

---

## 1. What is Vis.js & ForceAtlas2?

### Vis.js (`vis-network`)
[Vis.js](https://visjs.github.io/vis-network/docs/network/) is a high-performance, canvas-rendered graph and network visualization library for the browser. Unlike DOM-heavy SVG visualizers or monolithic chart libraries, `vis-network`:
- Directly renders thousands of nodes and edges on an HTML5 canvas at 60 FPS.
- Supports interactive node dragging, dynamic physics simulation, smooth pan/zoom, custom node shapes/colors, tooltips, and click events.
- Zero mandatory framework dependencies: works in vanilla JS, Vite, React, Vue, or Tauri webviews.

### ForceAtlas2 (Spatial Layout Algorithm)
[ForceAtlas2](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679) is a continuous spatialization algorithm developed by Mathieu Jacomy et al. for the Gephi project. Unlike classical spring-embedder layouts (such as Fruchterman-Reingold), ForceAtlas2 is designed specifically for **real-world complex networks**:
1. **Degree-Dependent Repulsion**: Highly connected hub nodes (e.g. `speech-mcp`, `blender-mcp`) repel more strongly than leaf nodes. This naturally separates functional clusters and prevents the "hairball" collapse typical of standard physics models.
2. **Barnes-Hut Optimization**: Approximates $N$-body forces in $O(N \log N)$ rather than $O(N^2)$, allowing fluid simulations on consumer hardware.
3. **Linear Attraction**: Keeps clustered nodes close together without over-stretching long-distance cross-domain bridges.

---

## 2. Why the Sandra S. Fleet Uses It

The fleet consists of 200+ FastMCP repositories with complex multi-hub crossconnects:
- Multi-domain hubs (`speech-mcp`, `email-mcp`, `aiwatcher-mcp`, `blender-mcp`, `resonite-mcp`)
- Domain clusters (CAD/CAM, VR/Spatial, Maker Robotics, Voice Bus, Intelligence/Email, Audio/Video)

Standard SVG diagrams either get cluttered or require manual coordinates. ForceAtlas2 in `vis-network`:
- **Auto-clusters related repositories**: Nodes in the same subsystem naturally pull together into distinct visual constellations.
- **Interactive Navigation**: Users click any node to immediately jump to `https://github.com/sandraschi/<repo>`.
- **Search & Focus**: Typing in the search bar smoothly pans and zooms the camera straight to the target server.

---

## 3. Fleet Standard Configuration (Dark Mode SOTA)

The canonical fleet configuration used in `mcp-central-docs/web_sota/crossconnects.html`:

```javascript
const options = {
  physics: {
    solver: 'forceAtlas2Based',
    forceAtlas2Based: {
      gravitationalConstant: -60,  // Repulsion between nodes
      centralGravity: 0.01,        // Gentle pull toward center
      springLength: 140,           // Distance between connected companions
      springConstant: 0.08         // Elasticity of companion links
    },
    stabilization: {
      iterations: 150              // Pre-render simulation steps before initial paint
    }
  },
  interaction: {
    hover: true,
    tooltipDelay: 100,
    zoomView: true,
    dragView: true
  }
};
```

### Dark Mode Palette Standard
Nodes use dark fill with bright neon stroke outlines for high legibility:
- **CAD & DCC**: Background `#1e3a5f`, Border `#38bdf8` (Sky)
- **VR & Spatial**: Background `#4c1d95`, Border `#c084fc` (Purple)
- **Maker & Robotics**: Background `#78350f`, Border `#fbbf24` (Amber)
- **Voice Bus**: Background `#064e3b`, Border `#34d399` (Emerald)
- **Intelligence & Email**: Background `#312e81`, Border `#818cf8` (Indigo)
- **Audio & Media**: Background `#831843`, Border `#f472b6` (Pink)

---

## 4. Usage in Fleet Webapps

To embed the crossconnect explorer in any fleet dashboard or Vite webapp:

```html
<!-- CDN Import (Zero build step) -->
<script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

<!-- Or via Bun/npm in webapp/ -->
<!-- bun add vis-network -->
```

```typescript
import { Network } from 'vis-network/standalone';

const network = new Network(containerElement, { nodes, edges }, options);

network.on('click', (params) => {
  if (params.nodes.length > 0) {
    const repoId = params.nodes[0];
    window.open(`https://github.com/sandraschi/${repoId}`, '_blank');
  }
});
```

---

## 5. References & Links
- [Vis.js Network Documentation](https://visjs.github.io/vis-network/docs/network/)
- [ForceAtlas2 Paper (PLoS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0098679)
- [Fleet Crossconnect Map (`crossconnects.html`)](../web_sota/crossconnects.html)
- [Fleet Crossconnect Standard (`FLEET_CROSSCONNECT_STANDARD.md`)](../standards/FLEET_CROSSCONNECT_STANDARD.md)
