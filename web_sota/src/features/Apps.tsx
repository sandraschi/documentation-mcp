import * as React from "react"
import { ExternalLink, Globe, HardDrive, Cpu, Database, Brain, Loader2, Zap, Play } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { API_BASE } from "@/lib/api"
/** Normalized app item (from catalog: label, whatItIs, whatYouCanDo, startScript; or registry: id, name, description, repo_path). */
export interface AppItem {
    id: string
    name: string
    description: string
    usage: string
    port: number | null
    url: string
    /** For POST /api/apps/launch */
    label?: string
    /** For POST /api/fleet/launch */
    repoPath?: string
    category?: string
    icon?: string
}

function normalizeApp(raw: Record<string, unknown>): AppItem {
    const hasLabel = typeof raw.label === "string"
    if (hasLabel) {
        const label = raw.label as string
        const startScript = (raw.startScript as string) || ""
        const repoPath = startScript ? `D:/Dev/repos/${startScript.split("/")[0]}` : undefined
        return {
            id: label.toLowerCase().replace(/\s+/g, "-"),
            name: label,
            description: (raw.whatItIs as string) || "",
            usage: (raw.whatYouCanDo as string) || "",
            port: (raw.port as number) ?? null,
            url: (raw.url as string) || "#",
            label,
            repoPath,
            category: (raw.whatItIs as string) || "App",
        }
    }
    return {
        id: (raw.id as string) || (raw.name as string) || "app",
        name: (raw.name as string) || "App",
        description: (raw.description as string) || "",
        usage: (raw.description as string) || "",
        port: (raw.port as number) ?? null,
        url: (raw.url as string) || "#",
        repoPath: raw.repo_path as string | undefined,
        category: (raw.category as string) || "App",
        icon: raw.icon as string | undefined,
    }
}

export function Apps() {
    const [apps, setApps] = React.useState<AppItem[]>([])
    const [loading, setLoading] = React.useState(true)
    const [selectedApp, setSelectedApp] = React.useState<AppItem | null>(null)
    const [launching, setLaunching] = React.useState(false)
    const [launchMessage, setLaunchMessage] = React.useState<string | null>(null)

    const launchApp = React.useCallback(async (app: AppItem) => {
        setLaunching(true)
        setLaunchMessage(null)
        try {
            if (app.label) {
                const res = await fetch(API_BASE + "/api/apps/launch", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ label: app.label }),
                })
                const data = await res.json().catch(() => ({}))
                if (!res.ok) {
                    setLaunchMessage(data.error || `Launch failed: ${res.statusText}`)
                    return
                }
                setLaunchMessage(data.message || `Launched ${app.name}`)
                if (app.port && app.url !== "#") {
                    window.open(app.url, "_blank")
                }
            } else if (app.repoPath) {
                const res = await fetch(API_BASE + "/api/fleet/launch", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ repo_path: app.repoPath }),
                })
                const data = await res.json().catch(() => ({}))
                if (!res.ok) {
                    setLaunchMessage(data.error || `Launch failed: ${res.statusText}`)
                    return
                }
                setLaunchMessage(data.message || `Launched ${app.name}`)
                if (app.port) {
                    window.open(`http://127.0.0.1:${app.port}`, "_blank")
                }
            } else {
                setLaunchMessage("No launch method (label or repo_path) for this app.")
            }
        } catch (err) {
            const msg = err instanceof Error ? err.message : "Launch failed"
            setLaunchMessage(msg)
        } finally {
            setLaunching(false)
        }
    }, [])

    React.useEffect(() => {
        fetch(API_BASE + "/api/apps")
            .then((res) => res.json())
            .then((data: unknown) => {
                const list = Array.isArray(data)
                    ? data
                    : (data && typeof data === "object" && "apps" in data && Array.isArray((data as { apps: unknown[] }).apps))
                        ? (data as { apps: unknown[] }).apps
                        : []
                setApps(list.map((a: Record<string, unknown>) => normalizeApp(a)))
                setLoading(false)
            })
            .catch((err) => {
                console.error("Failed to fetch apps:", err)
                setLoading(false)
            })
    }, [])

    const getIcon = (app: AppItem) => {
        const iconName = (app.icon || app.category || "").toLowerCase()
        if (iconName.includes("globe") || iconName.includes("map")) return <Globe className="w-5 h-5 text-primary" />
        if (iconName.includes("drive") || iconName.includes("video")) return <HardDrive className="w-5 h-5 text-primary" />
        if (iconName.includes("music") || iconName.includes("waves")) return <Zap className="w-5 h-5 text-primary" />
        if (iconName.includes("cpu") || iconName.includes("shield")) return <Cpu className="w-5 h-5 text-primary" />
        if (iconName.includes("database")) return <Database className="w-5 h-5 text-primary" />
        if (iconName.includes("brain") || iconName.includes("library")) return <Brain className="w-5 h-5 text-primary" />
        return <Globe className="w-5 h-5 text-primary" />
    }

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        )
    }

    return (
        <div className="flex-1 flex flex-col min-h-0 container max-w-6xl mx-auto py-8 px-6">
            <div className="mb-8 space-y-2 shrink-0">
                <h1 className="text-3xl font-bold tracking-tight">Fleet Dashboard</h1>
                <p className="text-muted-foreground">
                    Centralized directory for all integrated MCP applications and autonomous services.
                </p>
            </div>

            <div className="flex-1 overflow-y-auto min-h-0 pr-2 -mr-2">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-8">
                    {apps.map((app) => (
                        <Card
                            key={app.id}
                            className="group hover:border-primary/50 transition-all hover:shadow-xl flex flex-col bg-card/30 backdrop-blur-md border-white/5 shadow-2xl cursor-pointer"
                            onClick={() => setSelectedApp(app)}
                        >
                            <CardHeader className="pb-4">
                                <div className="flex justify-between items-start">
                                    <div className="p-3 bg-primary/10 rounded-xl group-hover:bg-primary/20 transition-colors">
                                        {getIcon(app)}
                                    </div>
                                    {app.port != null && (
                                        <Badge variant="outline" className="text-[10px] font-mono border-primary/20 text-primary uppercase tracking-widest">
                                            PORT {app.port}
                                        </Badge>
                                    )}
                                </div>
                                <CardTitle className="mt-5 text-xl tracking-tight font-bold">{app.name}</CardTitle>
                                <CardDescription className="mt-1 text-[10px] font-semibold uppercase tracking-widest text-primary/70">
                                    {app.category ?? "Service Node"}
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="flex-1">
                                <p className="text-sm text-muted-foreground leading-relaxed line-clamp-3">
                                    {app.description}
                                </p>
                            </CardContent>
                            <CardFooter className="pt-4 border-t border-white/5 mt-4">
                                <Button
                                    className="w-full gap-2 group/btn"
                                    variant="ghost"
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        setSelectedApp(app)
                                    }}
                                >
                                    <Play className="w-4 h-4 group-hover/btn:scale-110 transition-transform" />
                                    Launch Instance
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>

            <Dialog open={!!selectedApp} onOpenChange={(open) => !open && setSelectedApp(null)}>
                <DialogContent className="sm:max-w-md bg-card border-white/10 text-foreground">
                    {selectedApp && (
                        <>
                            <DialogHeader>
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-primary/10 rounded-lg">{getIcon(selectedApp)}</div>
                                    <DialogTitle className="text-xl">{selectedApp.name}</DialogTitle>
                                </div>
                                <DialogDescription className="uppercase text-[10px] tracking-widest text-primary font-bold">
                                    {selectedApp.category ?? "Autonomous Node"}
                                </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4 py-4">
                                <div>
                                    <h4 className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-1">Functional Overview</h4>
                                    <p className="text-sm text-muted-foreground leading-relaxed">{selectedApp.description}</p>
                                </div>
                                <div>
                                    <h4 className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground mb-1">Operation Commands</h4>
                                    <p className="text-sm text-muted-foreground leading-relaxed">{selectedApp.usage}</p>
                                </div>
                                {launchMessage && (
                                    <div className={`p-3 rounded-lg border text-sm ${launchMessage.startsWith("Launched") ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-500" : "bg-amber-500/10 border-amber-500/20 text-amber-500"}`}>
                                        {launchMessage}
                                    </div>
                                )}
                            </div>
                            <DialogFooter className="gap-2 sm:gap-0">
                                <Button
                                    variant="outline"
                                    onClick={() => setSelectedApp(null)}
                                >
                                    Close
                                </Button>
                                <Button
                                    onClick={() => launchApp(selectedApp)}
                                    disabled={launching}
                                    className="gap-2"
                                >
                                    {launching ? (
                                        <Loader2 className="w-4 h-4 animate-spin" />
                                    ) : (
                                        <Play className="w-4 h-4" />
                                    )}
                                    Start Service
                                </Button>
                                {selectedApp.port != null && selectedApp.url !== "#" && (
                                    <Button
                                        variant="secondary"
                                        className="gap-2"
                                        onClick={() => window.open(selectedApp.url, "_blank")}
                                    >
                                        <ExternalLink className="w-4 h-4" />
                                        Open Web UI
                                    </Button>
                                )}
                            </DialogFooter>
                        </>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    )
}
