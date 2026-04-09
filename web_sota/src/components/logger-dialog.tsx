import * as React from "react"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Terminal, RefreshCcw, Loader2, Trash2, ShieldAlert } from "lucide-react"

export function LoggerDialog() {
    const [logs, setLogs] = React.useState<string[]>([])
    const [loading, setLoading] = React.useState(false)
    const [autoRefresh, setAutoRefresh] = React.useState(false)

    const fetchLogs = async () => {
        setLoading(true)
        try {
            const res = await fetch('/api/logs')
            if (!res.ok) throw new Error("Logger offline")
            const data = await res.json()
            setLogs(data.logs || [])
        } catch (err) {
            console.error("Failed to fetch logs:", err)
            setLogs(["CRITICAL: Logger subsystem returned an invalid response.", "Verify d:/Dev/repos/mcp-central-docs/debug.log exists."])
        } finally {
            setLoading(false)
        }
    }

    React.useEffect(() => {
        let interval: any
        if (autoRefresh) {
            interval = setInterval(fetchLogs, 3000)
        }
        return () => clearInterval(interval)
    }, [autoRefresh])

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button variant="ghost" size="icon" title="System Logs" onClick={() => fetchLogs()}>
                    <Terminal className="h-[1.2rem] w-[1.2rem]" />
                    <span className="sr-only">Logs</span>
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[800px] h-[600px] flex flex-col overflow-hidden bg-zinc-950 text-zinc-100 border-zinc-800">
                <DialogHeader className="border-b border-zinc-800 pb-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <DialogTitle className="flex items-center gap-2 font-mono text-xl uppercase tracking-tighter">
                                <Terminal className="h-5 w-5 text-emerald-500" />
                                System.Kernel.Output
                            </DialogTitle>
                            <DialogDescription className="text-zinc-500 font-mono text-[10px] tracking-widest uppercase">
                                Real-time Diagnostic Stream • WebSocket Simulator
                            </DialogDescription>
                        </div>
                        <div className="flex items-center gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                onClick={() => setAutoRefresh(!autoRefresh)}
                                className={React.useMemo(() => autoRefresh ? "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" : "bg-transparent", [autoRefresh])}
                            >
                                {autoRefresh ? "Live: On" : "Live: Off"}
                            </Button>
                            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={fetchLogs} disabled={loading}>
                                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <RefreshCcw className="h-4 w-4" />}
                            </Button>
                        </div>
                    </div>
                </DialogHeader>

                <ScrollArea className="flex-1 bg-black/40 p-4 font-mono text-xs">
                    <div className="space-y-1">
                        {logs.length === 0 && !loading && (
                            <div className="flex items-center gap-2 text-zinc-600 italic py-20 justify-center">
                                <ShieldAlert className="w-4 h-4" />
                                <span>No log entries detected in debug.log</span>
                            </div>
                        )}
                        {logs.map((log, i) => (
                            <div key={i} className="flex gap-3 group border-b border-zinc-900/50 py-1 hover:bg-zinc-900/30">
                                <span className="text-zinc-700 select-none w-6">{i + 1}</span>
                                <span className={React.useMemo(() => {
                                    if (log.includes('ERROR') || log.includes('CRITICAL')) return "text-rose-500"
                                    if (log.includes('DEBUG')) return "text-emerald-500/80"
                                    if (log.includes('WARN')) return "text-amber-500"
                                    return "text-zinc-400"
                                }, [log])}>{log}</span>
                            </div>
                        ))}
                    </div>
                </ScrollArea>

                <div className="border-t border-zinc-800 pt-3 flex items-center justify-between">
                    <div className="flex items-center gap-4 text-[10px] uppercase tracking-widest text-zinc-600">
                        <span>Buffer: {logs.length}L</span>
                        <span>Stream: {loading ? "Active" : "Idle"}</span>
                    </div>
                    <Button variant="ghost" size="sm" className="h-8 text-zinc-500 hover:text-rose-500 transition-colors" onClick={() => setLogs([])}>
                        <Trash2 className="w-3.5 h-3.5 mr-2" /> Clear Buffer
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    )
}
