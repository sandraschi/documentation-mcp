import { create } from "zustand"
import { API_BASE } from "./api"

export interface ProviderInfo {
  key: string
  label: string
  models: string[]
  detected?: boolean
}

export interface AppState {
  backendOk: boolean | null
  sidebarOpen: boolean
  providers: ProviderInfo[]
  gpuDetected: boolean | null
  setBackendOk: (ok: boolean | null) => void
  setSidebarOpen: (open: boolean) => void
  setProviders: (providers: ProviderInfo[]) => void
  setGpuDetected: (detected: boolean) => void
  checkHealth: () => Promise<void>
  fetchProviders: () => Promise<void>
}

export const useAppStore = create<AppState>((set) => ({
  backendOk: null,
  sidebarOpen: true,
  providers: [],
  gpuDetected: null,
  setBackendOk: (ok) => set({ backendOk: ok }),
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  setProviders: (providers) => set({ providers }),
  setGpuDetected: (detected) => set({ gpuDetected: detected }),
  checkHealth: async () => {
    try {
      const res = await fetch(API_BASE + "/api/health", { signal: AbortSignal.timeout(5000) })
      set({ backendOk: res.ok })
    } catch {
      set({ backendOk: false })
    }
  },
  fetchProviders: async () => {
    try {
      const res = await fetch(API_BASE + "/api/llm/discover")
      const data = await res.json()
      const list: ProviderInfo[] = []
      if (data.ollama) list.push({ key: "ollama", label: "Ollama", models: data.ollama_models || [], detected: true })
      if (data.lmstudio) list.push({ key: "local", label: "LM Studio", models: data.lmstudio_models || [], detected: true })
      if (data.openai) list.push({ key: "openai", label: "OpenAI", models: data.openai_models || [], detected: true })
      set({ providers: list, gpuDetected: data.gpu_detected ?? null })
    } catch {
      set({ providers: [], gpuDetected: false })
    }
  },
}))
