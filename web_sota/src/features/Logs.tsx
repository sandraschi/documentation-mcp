import * as React from "react"
import { 
    Terminal, 
    RefreshCw, 
    Activity, 
    ShieldAlert, 
    Search,
    ArrowDown,
    Square
} from "lucide-react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { API_BASE } from "@/lib/api"

interface Process {
    id: string
    pid: number
    status: string
}

export function Logs() {
    const [logs, setLogs] = React.useState<string[]>([])
    const [processes, setProcesses] = React.useState<Process[]>([])
    const [, setLoading] = React.useState(true)
    const [autoScroll, setAutoScroll] = React.useState(true)
    const [filter, setFilter] = React.useState("ALL")
    const [search, setSearch] = React.useState("")
    const scrollRef = React.useRef<HTMLDivElement>(null)

    const fetchLogs = React.useCallback(async () => {
        try {
            const res = await fetch(API_BASE + "/api/logs?limit=500")
            const data = await res.json()
            if (data.logs) {
                setLogs(data.logs)
            }
        } catch (error) {
            console.error("Failed to fetch logs:", error)
        }
    }, [])

    const fetchProcesses = React.useCallback(async () => {
        try {
            const res = await fetch(API_BASE + "/api/processes")
            const data = await res.json()
            if (data.processes) {
                setProcesses(data.processes)
            }
        } catch (error) {
            console.error("Failed to fetch processes:", error)
        }
    }, [])

    const killProcess = async (id: string, pid: number) => {
        try {
            const res = await fetch(API_BASE + "/api/processes/stop", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, pid })
            })
            if (res.ok) {
                fetchProcesses()
            }
        } catch (error) {
            console.error("Failed to kill process:", error)
        }
    }

    React.useEffect(() => {
        fetchLogs()
        fetchProcesses()
        const logInt = setInterval(fetchLogs, 2000)
        const procInt = setInterval(fetchProcesses, 5000)
        setLoading(false)
        return () => {
            clearInterval(logInt)
            clearInterval(procInt)
        }
    }, [fetchLogs, fetchProcesses])

    React.useEffect(() => {
        if (autoScroll && scrollRef.current) {
            const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]')
            if (scrollContainer) {
                scrollContainer.scrollTop = scrollContainer.scrollHeight
            }
        }
    }, [logs, autoScroll])

    const filteredLogs = logs.filter(line => {
        if (filter !== "ALL" && !line.includes(filter)) return false
        if (search && !line.toLowerCase().includes(search.toLowerCase())) return false
        return true
    })

    const getLineColor = (line: string) => {
        if (line.includes("ERROR")) return "text-red-400"
        if (line.includes("WARNING")) return "text-yellow-400"
        if (line.includes("DEBUG")) return "text-blue-400 font-light opacity-80"
        if (line.includes("INFO")) return "text-emerald-400"
        return "text-zinc-300"
    }

    return (
        <div className="flex flex-col h-[calc(100vh-4rem)] bg-zinc-950 text-zinc-300 font-mono">
            {/* Control Bar */}
            <header className="h-14 border-b border-zinc-800 bg-zinc-900/50 flex items-center px-4 gap-4 shrink-0">
                <div className="flex items-center gap-2 mr-4">
                    <Terminal className="w-5 h-5 text-emerald-500" />
                    <span className="font-bold text-sm tracking-widest uppercase text-emerald-500">System Logs</span>
                </div>

                <div className="flex items-center gap-2 bg-zinc-950 px-3 py-1 rounded border border-zinc-800 flex-1 max-w-md">
                    <Search className="w-4 h-4 text-zinc-500" />
                    <input 
                        type="text" 
                        placeholder="Filter trace..." 
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="bg-transparent border-none outline-none text-xs w-full focus:ring-0"
                    />
                </div>

                <div className="flex items-center gap-1">
                    {["ALL", "INFO", "WARN", "ERROR", "DEBUG"].map((lvl) => (
                        <Button
                            key={lvl}
                            variant="ghost"
                            size="sm"
                            onClick={() => setFilter(lvl)}
                            className={cn(
                                "h-7 px-2 text-[10px] font-bold",
                                filter === lvl ? "bg-emerald-500/10 text-emerald-500 border border-emerald-500/50" : "text-zinc-500"
                            )}
                        >
                            {lvl}
                        </Button>
                    ))}
                </div>

                <div className="ml-auto flex items-center gap-2">
                    <Button 
                        variant="ghost" 
                        size="sm" 
                        onClick={() => setAutoScroll(!autoScroll)}
                        className={cn("h-8 gap-2 text-xs", autoScroll && "text-emerald-500")}
                    >
                        <ArrowDown className={cn("w-3 h-3 transition-transform", autoScroll ? "translate-y-0" : "-translate-y-1")} />
                        Auto-scroll
                    </Button>
                    <Button variant="ghost" size="sm" onClick={fetchLogs} className="h-8 w-8 p-0">
                        <RefreshCw className="w-4 h-4" />
                    </Button>
                </div>
            </header>

            <div className="flex-1 flex overflow-hidden">
                {/* Main Terminal View */}
                <div className="flex-1 relative overflow-hidden flex flex-col">
                    <ScrollArea ref={scrollRef} className="flex-1 p-4">
                        <div className="space-y-0.5 min-w-max pb-10">
                            {filteredLogs.map((log, i) => (
                                <div key={i} className={cn("text-xs whitespace-pre break-all hover:bg-zinc-900/50 flex group", getLineColor(log))}>
                                    <span className="mr-4 text-zinc-600 select-none w-8 text-right shrink-0">{i + 1}</span>
                                    <span>{log.replace(/\n$/, "")}</span>
                                </div>
                            ))}
                            {filteredLogs.length === 0 && (
                                <div className="text-zinc-600 italic py-10 text-center">No logs matching current filter...</div>
                            )}
                        </div>
                    </ScrollArea>
                </div>

                {/* Process Panel */}
                <aside className="w-80 border-l border-zinc-800 bg-zinc-900/30 flex flex-col shrink-0">
                    <div className="p-4 border-b border-zinc-800 flex items-center justify-between">
                        <h3 className="text-[11px] font-bold uppercase tracking-wider flex items-center gap-2">
                            <Activity className="w-3 h-3 text-emerald-500" />
                            Live Subprocesses
                        </h3>
                        <Badge variant="outline" className="text-[10px] bg-zinc-950 border-zinc-700">
                            {processes.length} Active
                        </Badge>
                    </div>
                    
                    <ScrollArea className="flex-1">
                        <div className="p-4 space-y-3">
                            {processes.map((proc) => (
                                <Card key={proc.id} className="bg-zinc-950/50 border-zinc-800 shadow-none hover:border-emerald-500/30 transition-colors overflow-hidden">
                                    <CardHeader className="p-3 pb-0">
                                        <CardTitle className="text-xs flex items-center justify-between">
                                            <span className="truncate max-w-[120px] text-emerald-500 font-mono">{proc.id}</span>
                                            <Badge variant="outline" className="text-[9px] h-4 py-0 font-normal border-emerald-500/20 text-emerald-500/80">
                                                PID: {proc.pid}
                                            </Badge>
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="p-3 space-y-2">
                                        <div className="flex items-center gap-2">
                                            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                                            <span className="text-[10px] text-zinc-500 uppercase tracking-tighter">Status: {proc.status}</span>
                                        </div>
                                        <Button 
                                            variant="destructive" 
                                            size="sm" 
                                            className="w-full h-7 text-[10px] gap-2 font-bold uppercase"
                                            onClick={() => killProcess(proc.id, proc.pid)}
                                        >
                                            <Square className="w-3 h-3 fill-current" />
                                            Terminate Task
                                        </Button>
                                    </CardContent>
                                </Card>
                            ))}
                            
                            {processes.length === 0 && (
                                <div className="flex flex-col items-center justify-center py-20 text-center space-y-4">
                                    <ShieldAlert className="w-8 h-8 text-zinc-800" />
                                    <div className="space-y-1">
                                        <div className="text-[11px] text-zinc-500 font-bold uppercase">No Active Tasks</div>
                                        <div className="text-[10px] text-zinc-700">Background processes will appear here when launched.</div>
                                    </div>
                                    <Button 
                                        variant="outline" 
                                        size="sm" 
                                        className="h-7 text-[9px] border-zinc-800 text-zinc-500 hover:text-emerald-500 transition-colors"
                                        onClick={() => window.location.hash = "#/apps"}
                                    >
                                        Go to Fleet Dashboard
                                    </Button>
                                </div>
                            )}
                        </div>
                    </ScrollArea>

                    <footer className="p-3 border-t border-zinc-800 bg-zinc-950 text-[10px] text-zinc-600 flex flex-col gap-1">
                        <div className="flex justify-between items-center">
                            <span>Control Plane: v1.0.1</span>
                            <span className="text-emerald-900/50 font-bold">STABLE</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span>Poll Interval: 5s</span>
                            <Activity className="w-2 h-2 text-emerald-800" />
                        </div>
                    </footer>
                </aside>
            </div>
        </div>
    )
}
