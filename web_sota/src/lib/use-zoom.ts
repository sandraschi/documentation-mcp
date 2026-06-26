import { useCallback, useEffect } from "react";
import { isTauri } from "./is-tauri";

const ZOOM_LEVELS = [0.8, 1.0, 1.25, 1.5, 2.0, 3.0];

let _zoomIndex = (() => {
  try {
    const saved = localStorage.getItem("tauri-zoom");
    return saved ? Math.max(0, ZOOM_LEVELS.indexOf(parseFloat(saved))) : 1;
  } catch {
    return 1;
  }
})();

async function _applyZoom(level: number) {
  localStorage.setItem("tauri-zoom", String(level));
  if (isTauri()) {
    const { getCurrentWindow } = await import("@tauri-apps/api/window");
    const win = getCurrentWindow();
    (win as unknown as { setZoom: (z: number) => Promise<void> }).setZoom(level);
  } else {
    const root = document.documentElement;
    root.style.transform = `scale(${level})`;
    root.style.transformOrigin = "top left";
    root.style.width = `${100 / level}%`;
    root.style.height = `${100 / level}%`;
  }
}

export function useZoom() {
  const onWheel = useCallback((e: WheelEvent) => {
    if (!e.ctrlKey) return;
    e.preventDefault();
    const delta = e.deltaY < 0 ? 1 : -1;
    const nextIdx = Math.max(0, Math.min(ZOOM_LEVELS.length - 1, _zoomIndex + delta));
    if (nextIdx !== _zoomIndex) {
      _zoomIndex = nextIdx;
      _applyZoom(ZOOM_LEVELS[nextIdx]);
    }
  }, []);

  useEffect(() => {
    window.addEventListener("wheel", onWheel, { passive: false });
    const saved = localStorage.getItem("tauri-zoom");
    if (saved) {
      const idx = ZOOM_LEVELS.indexOf(parseFloat(saved));
      if (idx >= 0) {
        _zoomIndex = idx;
        _applyZoom(ZOOM_LEVELS[idx]);
      }
    }
    return () => window.removeEventListener("wheel", onWheel);
  }, [onWheel]);
}
