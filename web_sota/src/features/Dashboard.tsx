import * as React from "react"
import { useNavigate } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Activity, Book, Database, Server, Zap, Loader2, RefreshCw } from "lucide-react"
import { viewToPathname, type ViewState } from "@/routes"
import { API_BASE } from "@/lib/api"
import { isTauri } from "@/lib/is-tauri"

interface SystemStatus {
    success: boolean
    chunk_count: number
    source_count: number
    fleet_count: number
    provider: string
    model: string
    memory: any
    status: string
}

const BACKOFF_INTERVALS = [1000, 2000, 4000, 8000, 16000]
const MAX_INTERVAL = 30000

export function Dashboard() {
    const navigate = useNavigate()
    const to = (view: ViewState) => navigate(viewToPathname(view))
    const [status, setStatus] = React.useState<SystemStatus | null>(null)
    const [loading, setLoading] = React.useState(true)
    const [backendOk, setBackendOk] = React.useState<boolean | null>(null)
    const [restarting, setRestarting] = React.useState(false)
    const retryIndexRef = React.useRef(0)
    const intervalRef = React.useRef<ReturnType<typeof setTimeout> | null>(null)

    const fetchStatus = React.useCallback(async () => {
        try {
            const res = await fetch(API_BASE + "/api/status")
            const data = await res.json()
            setStatus(data)
            setBackendOk(true)
            retryIndexRef.current = 0
        } catch (err) {
            console.error("Failed to fetch system status:", err)
            setBackendOk(false)
            const delay = retryIndexRef.current < BACKOFF_INTERVALS.length
                ? BACKOFF_INTERVALS[retryIndexRef.current]
                : MAX_INTERVAL
            retryIndexRef.current = Math.min(retryIndexRef.current + 1, BACKOFF_INTERVALS.length)
            if (intervalRef.current) clearTimeout(intervalRef.current)
            intervalRef.current = setTimeout(fetchStatus, delay)
            return
        } finally {
            setLoading(false)
        }
        if (intervalRef.current) clearTimeout(intervalRef.current)
        intervalRef.current = setTimeout(fetchStatus, MAX_INTERVAL)
    }, [])

    React.useEffect(() => {
        fetchStatus()
        return () => { if (intervalRef.current) clearTimeout(intervalRef.current) }
    }, [fetchStatus])

    React.useEffect(() => {
        if (!isTauri()) return
        let unlisten: (() => void) | undefined
        ;(async () => {
            const { listen } = await import("@tauri-apps/api/event")
            unlisten = await listen<string>("backend-status", (event) => {
                if (event.payload === "ready") {
                    fetchStatus()
                    setRestarting(false)
                } else if (typeof event.payload === "string" && event.payload.startsWith("error:")) {
                    setBackendOk(false)
                    setRestarting(false)
                }
            })
        })()
        return () => { if (unlisten) unlisten() }
    }, [fetchStatus])

    const restartBackend = React.useCallback(async () => {
        if (!isTauri()) return
        setRestarting(true)
        const { invoke } = await import("@tauri-apps/api/core")
        try {
            await invoke("start_backend")
        } catch {
            setRestarting(false)
        }
    }, [])

    return (
        <div
            data-testid="dashboard"
            className="flex-1 flex flex-col min-h-0 container max-w-6xl mx-auto py-8 px-4 space-y-12 overflow-y-auto"
        >
            {/* Hero Section: Industrial Documentation Management */}
            <div className="relative overflow-hidden rounded-3xl border bg-card/30 backdrop-blur-md p-8 md:p-12 shadow-2xl ring-1 ring-white/10 transition-all duration-500 hover:shadow-primary/5 shrink-0">
                <div className="absolute top-0 right-0 -mr-20 -mt-20 h-64 w-64 rounded-full bg-primary/5 blur-3xl" />
                <div className="absolute bottom-0 left-0 -ml-20 -mb-20 h-64 w-64 rounded-full bg-primary/10 blur-3xl opacity-50" />

                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 relative z-10">
                    <div className="max-w-2xl space-y-4">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-xs font-semibold text-primary uppercase tracking-wider mb-2">
                            <Zap className="w-3 h-3" />
                            System Active
                        </div>
                        <h1 className="text-3xl font-extrabold tracking-tight text-foreground leading-tight">
                            Project <span className="text-primary bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/60">Documents</span>
                        </h1>
                        <p className="text-lg text-muted-foreground leading-relaxed">
                            A unified environment for managing, searching, and synthesizing technical documentation from local and remote repositories.
                        </p>
                    </div>

                    <div className="flex flex-col items-end gap-3 shrink-0">
                        <div className="flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-xl transition-all duration-300 hover:bg-emerald-500/15">
                            <div
                                data-testid="backend-dot"
                                className={`h-2.5 w-2.5 rounded-full ${backendOk === null ? "bg-gray-500" : backendOk ? "bg-emerald-500" : "bg-red-500"} animate-pulse`}
                            />
                            <span className="text-sm font-semibold text-emerald-500 uppercase tracking-widest">
                                {restarting
                                    ? "Restarting..."
                                    : status?.status === "ready"
                                        ? "Operational"
                                        : status?.status === "index_empty"
                                            ? "Index Empty"
                                            : backendOk === null
                                                ? "Connecting..."
                                                : "Offline"}
                            </span>
                        </div>
                        {backendOk === false && (
                            <button
                                onClick={restartBackend}
                                disabled={restarting}
                                className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs font-medium text-amber-500 hover:bg-amber-500/20 transition-colors disabled:opacity-50"
                            >
                                {restarting ? <Loader2 className="w-3 h-3 animate-spin" /> : <RefreshCw className="w-3 h-3" />}
                                Restart Backend
                            </button>
                        )}
                        <p className="text-xs text-muted-foreground font-mono uppercase tracking-tighter opacity-60">
                            Provider: {status?.provider || "Detecting..."} | Nodes: {status?.fleet_count || 0}
                        </p>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 pt-8 border-t border-white/5">
                    <div className="space-y-2">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <Book className="w-5 h-5 text-primary" />
                            Fleet Registry
                        </h3>
                        <p className="text-sm text-muted-foreground">Single point of access for all project-wide technical resources.</p>
                    </div>
                    <div className="space-y-2">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <Database className="w-5 h-5 text-primary" />
                            Vector Retrieval
                        </h3>
                        <p className="text-sm text-muted-foreground">Natural language retrieval utilizing integrated semantic systems.</p>
                    </div>
                    <div className="space-y-2">
                        <h3 className="font-bold text-lg flex items-center gap-2">
                            <Server className="w-5 h-5 text-primary" />
                            Service Control
                        </h3>
                        <p className="text-sm text-muted-foreground">Direct status and management of all connected MCP services.</p>
                    </div>
                </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 shrink-0">
                <Card data-testid="kpi-chunks">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Indexed Chunks</CardTitle>
                        <Book className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : status?.chunk_count.toLocaleString() || "0"}
                        </div>
                        <p className="text-xs text-muted-foreground">From {status?.source_count || 0} document sources</p>
                    </CardContent>
                </Card>
                <Card data-testid="kpi-registry">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Registry Status</CardTitle>
                        <Database className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-emerald-500">OPERATIONAL</div>
                        <p className="text-xs text-muted-foreground">Vector Engine Active</p>
                    </CardContent>
                </Card>
                <Card data-testid="kpi-apps">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Connected Apps</CardTitle>
                        <Server className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.fleet_count || 0} Registered</div>
                        <p className="text-xs text-muted-foreground">Direct service coordination</p>
                    </CardContent>
                </Card>
                <Card data-testid="kpi-model">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Inference Model</CardTitle>
                        <Zap className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{status?.model || "None"}</div>
                        <p className="text-xs text-muted-foreground">Active LLM endpoint</p>
                    </CardContent>
                </Card>
            </div>

            {/* Recent Activity / Integration Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-0 container pb-12">
                <Card className="flex flex-col">
                    <CardHeader>
                        <CardTitle>Infrastructure Health</CardTitle>
                        <CardDescription>Real-time metrics from the DocsOps system.</CardDescription>
                    </CardHeader>
                    <CardContent className="flex-1 overflow-y-auto">
                        <div className="space-y-4">
                            {[
                                { name: "Vector Database", status: "OPERATIONAL" },
                                { name: "Persistence Layer", status: status?.memory ? "HEALTHY" : "NOT_READY" },
                                { name: "Semantic Search", status: "OPERATIONAL" },
                                { name: "MPC Bridge", status: "CONNECTED" }
                            ].map((service, i) => (
                                <div key={i} className="flex items-center justify-between border-b pb-2 last:border-0 last:pb-0">
                                    <div className="flex items-center gap-3">
                                        <div className={`h-2 w-2 rounded-full ${service.status === "OPERATIONAL" || service.status === "HEALTHY" || service.status === "CONNECTED" ? "bg-emerald-500" : "bg-amber-500"}`} />
                                        <span className="font-medium text-sm">{service.name}</span>
                                    </div>
                                    <span className="text-[10px] font-mono text-muted-foreground uppercase">{service.status}</span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <Card className="flex flex-col">
                    <CardHeader>
                        <CardTitle>System Procedures</CardTitle>
                        <CardDescription>Common operational tasks.</CardDescription>
                    </CardHeader>
                    <CardContent className="grid gap-3">
                        <div className="p-3 border rounded-xl hover:bg-accent cursor-pointer transition-all flex items-center gap-4 group" onClick={() => to("documents")}>
                            <div className="p-3 bg-primary/10 rounded-lg group-hover:bg-primary group-hover:text-primary-foreground transition-colors"><Book className="w-5 h-5 text-primary group-hover:text-inherit" /></div>
                            <div>
                                <div className="font-semibold">Technical Docs</div>
                                <div className="text-xs text-muted-foreground">Browse standards and protocols</div>
                            </div>
                        </div>
                        <div className="p-3 border rounded-xl hover:bg-accent cursor-pointer transition-all flex items-center gap-4 group" onClick={() => to("semantic")}>
                            <div className="p-3 bg-primary/10 rounded-lg group-hover:bg-primary group-hover:text-primary-foreground transition-colors"><Activity className="w-5 h-5 text-primary group-hover:text-inherit" /></div>
                            <div>
                                <div className="font-semibold">Vector Retrieval</div>
                                <div className="text-xs text-muted-foreground">Direct semantic search operations</div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
