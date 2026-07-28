import * as React from "react"
import { Settings as SettingsIcon, Cpu, Database, RefreshCcw, Loader2, Save, ExternalLink } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { API_BASE } from "@/lib/api"

export function Settings() {
    const [ollamaUrl, setOllamaUrl] = React.useState("")
    const [ollamaModel, setOllamaModel] = React.useState("")
    const [localLlmUrl, setLocalLlmUrl] = React.useState("")
    const [localLlmKey, setLocalLlmKey] = React.useState("")
    const [provider, setProvider] = React.useState("")
    const [lmstudioUrl, setLmstudioUrl] = React.useState("")
    const [lmstudioModel, setLmstudioModel] = React.useState("")
    const [ollamaModels, setOllamaModels] = React.useState<string[]>([])
    const [ollamaMessage, setOllamaMessage] = React.useState<string | null>(null)
    const [lmstudioModels, setLmstudioModels] = React.useState<string[]>([])
    const [modelsLoading, setModelsLoading] = React.useState(false)
    const [lmstudioModelsLoading, setLmstudioModelsLoading] = React.useState(false)
    const [saveLoading, setSaveLoading] = React.useState(false)
    const [saveMessage, setSaveMessage] = React.useState<string | null>(null)
    const [reindexLoading, setReindexLoading] = React.useState(false)
    const [reindexMessage, setReindexMessage] = React.useState<string | null>(null)
    const [ragExtraPaths, setRagExtraPaths] = React.useState("")
    const [ragFederateMemory, setRagFederateMemory] = React.useState(false)
    const [ragDocsRoot, setRagDocsRoot] = React.useState("")

    const loadSettings = React.useCallback(async () => {
        try {
            const res = await fetch(API_BASE + "/api/settings")
            if (!res.ok) return
            const data = await res.json()
            const defaultOllamaUrl = "http://localhost:11434"
            const defaultLmstudioUrl = "http://localhost:1234/v1"
            const oUrl = (data.ollama_url ?? "").trim() || defaultOllamaUrl
            const lUrl = (data.lmstudio_url ?? "").trim() || defaultLmstudioUrl
            setOllamaUrl(data.ollama_url ?? defaultOllamaUrl)
            setOllamaModel(data.ollama_model ?? "")
            setLocalLlmUrl(data.local_llm_url ?? "")
            setLocalLlmKey(data.local_llm_key ?? "")
            setLmstudioUrl(data.lmstudio_url ?? defaultLmstudioUrl)
            setLmstudioModel(data.lmstudio_model ?? "")
            setProvider((data.provider ?? "").toLowerCase())
            const extraPaths = Array.isArray(data.rag_extra_paths) ? data.rag_extra_paths : []
            setRagExtraPaths(extraPaths.join("\n"))
            setRagFederateMemory(Boolean(data.rag_federate_memory))
            setRagDocsRoot(data.rag?.docs_root ?? "")

            // Auto-load model lists so dropdowns are populated (Ollama / LM Studio often run locally)
            setModelsLoading(true)
            fetch(`${API_BASE}/api/models/ollama?url=${encodeURIComponent(oUrl)}`)
                .then((r) => r.json())
                .then((d) => {
                    const list = Array.isArray(d.models) ? d.models : []
                    setOllamaModels(list)
                    setOllamaMessage(list.length === 0 ? (d.message || null) : null)
                    setOllamaModel((prev) => (list.length > 0 ? (data.ollama_model && list.includes(data.ollama_model) ? data.ollama_model : list[0]) : prev))
                })
                .catch(() => {
                    setOllamaModels([])
                    setOllamaMessage("Request failed.")
                })
                .finally(() => setModelsLoading(false))
            if (lUrl) {
                setLmstudioModelsLoading(true)
                fetch(`${API_BASE}/api/models/lmstudio?url=${encodeURIComponent(lUrl)}`)
                    .then((r) => r.json())
                    .then((d) => {
                        const list = Array.isArray(d.models) ? d.models : []
                        setLmstudioModels(list)
                        setLmstudioModel((prev) => (list.length > 0 ? (data.lmstudio_model && list.includes(data.lmstudio_model) ? data.lmstudio_model : list[0]) : prev))
                    })
                    .catch(() => setLmstudioModels([]))
                    .finally(() => setLmstudioModelsLoading(false))
            }
        } catch {
            // ignore
        }
    }, [])

    React.useEffect(() => {
        loadSettings()
    }, [loadSettings])

    const fetchOllamaModels = React.useCallback(async (overrideUrl?: string) => {
        const url = (overrideUrl ?? ollamaUrl ?? "").trim()
        setModelsLoading(true)
        try {
            const res = await fetch(url ? `${API_BASE}/api/models/ollama?url=${encodeURIComponent(url)}` : `${API_BASE}/api/models/ollama`)
            const data = await res.json()
            const list = Array.isArray(data.models) ? data.models : []
            setOllamaModels(list)
            setOllamaModel((prev) => (list.length > 0 && !prev ? list[0] : prev))
        } catch {
            setOllamaModels([])
        } finally {
            setModelsLoading(false)
        }
    }, [ollamaUrl])

    const fetchLmstudioModels = React.useCallback(async (overrideUrl?: string) => {
        const url = (overrideUrl ?? lmstudioUrl ?? "").trim()
        setLmstudioModelsLoading(true)
        try {
            const res = await fetch(url ? `${API_BASE}/api/models/lmstudio?url=${encodeURIComponent(url)}` : `${API_BASE}/api/models/lmstudio`)
            const data = await res.json()
            const list = Array.isArray(data.models) ? data.models : []
            setLmstudioModels(list)
            setLmstudioModel((prev) => (list.length > 0 && !prev ? list[0] : prev))
        } catch {
            setLmstudioModels([])
        } finally {
            setLmstudioModelsLoading(false)
        }
    }, [lmstudioUrl])

    const handleSave = async () => {
        setSaveLoading(true)
        setSaveMessage(null)
        try {
            const res = await fetch(API_BASE + "/api/settings", {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    ollama_url: ollamaUrl.trim(),
                    ollama_model: ollamaModel.trim(),
                    local_llm_url: localLlmUrl.trim(),
                    local_llm_key: localLlmKey.trim(),
                    lmstudio_url: lmstudioUrl.trim(),
                    lmstudio_model: lmstudioModel.trim(),
                    provider: provider.trim().toLowerCase(),
                    rag_extra_paths: ragExtraPaths,
                    rag_federate_memory: ragFederateMemory,
                }),
            })
            const data = await res.json()
            if (data.success) {
                setSaveMessage("Saved.")
                if (data.rag?.docs_root) setRagDocsRoot(data.rag.docs_root)
                loadSettings()
            } else {
                setSaveMessage(data.error ?? "Save failed.")
            }
        } catch {
            setSaveMessage("Request failed.")
        } finally {
            setSaveLoading(false)
        }
    }

    const handleReindex = async () => {
        setReindexLoading(true)
        setReindexMessage(null)
        try {
            const res = await fetch(API_BASE + "/api/reindex", { method: "POST", signal: AbortSignal.timeout(10000) })
            const data = await res.json()
            const msg = data.message ?? (res.ok ? "Reindex started in background." : "Reindex failed.")
            setReindexMessage(msg)
        } catch (e) {
            setReindexMessage("Request failed.")
        } finally {
            setReindexLoading(false)
        }
    }

    return (
        <div data-testid="settings-page" className="container max-w-4xl mx-auto py-8 px-6 space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight flex items-center gap-3">
                    <SettingsIcon className="w-8 h-8 text-primary" />
                    Settings
                </h1>
                <p className="text-muted-foreground mt-1">Local LLM, Ollama, model loading, and RAG.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Chat LLM provider</CardTitle>
                    <CardDescription>Choose which backend powers the AI Assistant. Leave empty for RAG-only (no LLM).</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Provider</span>
                        <Select value={provider || "none"} onValueChange={(v) => setProvider(v === "none" ? "" : v)}>
                            <SelectTrigger>
                                <SelectValue placeholder="None (RAG only)" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="none">None (RAG only)</SelectItem>
                                <SelectItem value="ollama">Ollama</SelectItem>
                                <SelectItem value="local">Local LLM (OpenAI-compatible)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Cpu className="w-5 h-5" />
                        Local LLM
                    </CardTitle>
                    <CardDescription>API endpoint and key for local or remote LLM (e.g. OpenAI-compatible).</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Base URL</span>
                        <Input
                            placeholder="http://localhost:8080/v1"
                            value={localLlmUrl}
                            onChange={(e) => setLocalLlmUrl(e.target.value)}
                            className="font-mono"
                        />
                    </div>
                    <div className="space-y-2">
                        <span className="text-sm font-medium">API Key (optional)</span>
                        <Input
                            type="password"
                            placeholder="sk-..."
                            value={localLlmKey}
                            onChange={(e) => setLocalLlmKey(e.target.value)}
                            className="font-mono"
                        />
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">LM Studio</CardTitle>
                    <CardDescription>LM Studio server (OpenAI-compatible). Load a model in LM Studio, then set URL and pick model. No API key needed. Using another PC? Use LM Link (Tailscale). Run Tailscale on both machines, then set Server URL to your remote machine.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Server URL</span>
                        <Input
                            placeholder="http://localhost:1234/v1"
                            value={lmstudioUrl}
                            onChange={(e) => setLmstudioUrl(e.target.value)}
                            className="font-mono"
                        />
                    </div>
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Model</span>
                        <div className="flex gap-2">
                            <Select
                                value={lmstudioModel || (lmstudioModels[0] ?? "")}
                                onValueChange={setLmstudioModel}
                                disabled={lmstudioModels.length === 0}
                            >
                                <SelectTrigger className="flex-1">
                                    <SelectValue placeholder={lmstudioModelsLoading ? "Loading..." : "Set URL and refresh"} />
                                </SelectTrigger>
                                <SelectContent>
                                    {lmstudioModels.map((m) => (
                                        <SelectItem key={m} value={m}>{m}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <Button
                                type="button"
                                variant="outline"
                                size="icon"
                                onClick={() => fetchLmstudioModels(lmstudioUrl)}
                                disabled={lmstudioModelsLoading || !lmstudioUrl.trim()}
                                title="Refresh model list from LM Studio"
                            >
                                {lmstudioModelsLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCcw className="w-4 h-4" />}
                            </Button>
                        </div>
                        {lmstudioModels.length === 0 && lmstudioUrl.trim() && !lmstudioModelsLoading && (
                            <p className="text-sm text-muted-foreground">No models returned. Start LM Studio, load a model, and ensure local server is running.</p>
                        )}
                    </div>
                    <div className="flex flex-wrap gap-4">
                        <a
                            href="https://lmstudio.ai"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-primary hover:underline inline-flex items-center gap-1"
                        >
                            LM Studio <ExternalLink className="w-3 h-3" />
                        </a>
                        <a
                            href="https://lmstudio.ai/docs/lmlink/basics"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-primary hover:underline inline-flex items-center gap-1"
                        >
                            LM Link (remote PC via Tailscale) <ExternalLink className="w-3 h-3" />
                        </a>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">Ollama</CardTitle>
                    <CardDescription>Ollama server URL. Model list is loaded from the API (no hardcoded list).</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Ollama base URL</span>
                        <Input
                            placeholder="http://localhost:11434"
                            value={ollamaUrl}
                            onChange={(e) => setOllamaUrl(e.target.value)}
                            className="font-mono"
                        />
                    </div>
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Model</span>
                        <div className="flex gap-2">
                            <Select
                                value={ollamaModel || (ollamaModels[0] ?? "")}
                                onValueChange={setOllamaModel}
                                disabled={ollamaModels.length === 0}
                            >
                                <SelectTrigger className="flex-1">
                                    <SelectValue placeholder={modelsLoading ? "Loading..." : "Set URL and refresh"} />
                                </SelectTrigger>
                                <SelectContent>
                                    {ollamaModels.map((m) => (
                                        <SelectItem key={m} value={m}>{m}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <Button
                                type="button"
                                variant="outline"
                                size="icon"
                                onClick={() => fetchOllamaModels(ollamaUrl)}
                                disabled={modelsLoading || !ollamaUrl.trim()}
                                title="Refresh model list from Ollama"
                            >
                                {modelsLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCcw className="w-4 h-4" />}
                            </Button>
                        </div>
                        {ollamaModels.length === 0 && ollamaUrl.trim() && !modelsLoading && (
                            <p className="text-sm text-muted-foreground">{ollamaMessage ?? "No models returned. Check URL and that Ollama is running."}</p>
                        )}
                    </div>
                </CardContent>
            </Card>

            <div className="flex items-center gap-4">
                <Button onClick={handleSave} disabled={saveLoading} className="gap-2">
                    {saveLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                    Save all settings
                </Button>
                {saveMessage && <span className="text-sm text-muted-foreground">{saveMessage}</span>}
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Database className="w-5 h-5" />
                        RAG &amp; indexing
                    </CardTitle>
                    <CardDescription>
                        Primary index: <code className="text-xs">{ragDocsRoot || "documentation-mcp/docs"}</code>.
                        Add extra markdown roots (one absolute path per line), then reindex.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <span className="text-sm font-medium">Extra RAG paths</span>
                        <textarea
                            className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm font-mono ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                            placeholder={"D:\\Dev\\repos\\some-repo\\docs\nD:\\Dev\\repos\\another-repo\\README.md"}
                            value={ragExtraPaths}
                            onChange={(e) => setRagExtraPaths(e.target.value)}
                        />
                        <p className="text-sm text-muted-foreground">
                            Each path is scanned recursively for <code>.md</code> files. Env var <code>DOCS_EXTRA_PATHS</code> is merged at runtime.
                        </p>
                    </div>
                    <label className="flex items-center gap-2 text-sm">
                        <input
                            type="checkbox"
                            checked={ragFederateMemory}
                            onChange={(e) => setRagFederateMemory(e.target.checked)}
                        />
                        Include Advanced Memory (<code>advanced-memory-mcp/knowledge</code> and <code>notes</code>)
                    </label>
                    <Button
                        onClick={handleReindex}
                        disabled={reindexLoading}
                        className="gap-2"
                    >
                        {reindexLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCcw className="w-4 h-4" />}
                        {reindexLoading ? "Reindexing..." : "Reindex all documentation"}
                    </Button>
                    {reindexMessage && (
                        <p className="text-sm text-muted-foreground">{reindexMessage}</p>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
