import { create } from "zustand"
import { API_BASE } from "./api"

export interface AppState {
  backendOk: boolean | null
  sidebarOpen: boolean
  setBackendOk: (ok: boolean | null) => void
  setSidebarOpen: (open: boolean) => void
  checkHealth: () => Promise<void>
}

export const useAppStore = create<AppState>((set) => ({
  backendOk: null,
  sidebarOpen: true,
  setBackendOk: (ok) => set({ backendOk: ok }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  checkHealth: async () => {
    try {
      const res = await fetch(API_BASE + "/api/health", { signal: AbortSignal.timeout(5000) })
      set({ backendOk: res.ok })
    } catch {
      set({ backendOk: false })
    }
  },
}))
