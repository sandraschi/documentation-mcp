import * as React from "react"
import { Brain, Shield, Zap, Database, Loader2, Terminal, Play } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"

const PERSISTENCE_TOOL_PREFIX = "persistence"

interface Tool {
    name: string
    description: string
    parameters?: { properties?: Record<string, { type?: string; description?: string }> }
}

const PLANNED_TOOLS: { name: string; args: string; description: string }[] = [
    { name: "persistence_store", args: "namespace, content", description: "Persist structured records with verified security guardrails." },
    { name: "persistence_recall", args: "namespace, query", description: "Semantic retrieval over the authorized memory registry." },
    { name: "persistence_optimize", args: "", description: "Monitor record density and execute background compaction." },
]

function getParamFields(tool: Tool): { key: string; type: string; description?: string }[] {
    const props = tool.parameters?.properties
    if (!props || typeof props !== "object") return []
    return Object.entries(props).map(([key, schema]) => ({
        key,
        type: (schema?.type as string) || "string",
        description: schema?.description,
    }))
}

export function Memory() {
    const [tools, setTools] = React.useState<Tool[]>([])
    const [loading, setLoading] = React.useState(true)
    const [executing, setExecuting] = React.useState<string | null>(null)
    const [results, setResults] = React.useState<Record<string, string>>({})
    const [toolArgs, setToolArgs] = React.useState<Record<string, Record<string, string>>>({})

    React.useEffect(() => {
        fetch("/api/tools")
            .then((res) => res.json())
            .then((data) => {
                const list = Array.isArray(data) ? data : []
                setTools(list.filter((t: Tool) => t.name.toLowerCase().includes(PERSISTENCE_TOOL_PREFIX)))
                setLoading(false)
            })
            .catch(() => {
                setTools([])
                setLoading(false)
            })
    }, [])

    const setArg = React.useCallback((toolName: string, paramKey: string, value: string) => {
        setToolArgs((prev) => ({
            ...prev,
            [toolName]: { ...(prev[toolName] ?? {}), [paramKey]: value },
        }))
    }, [])

    const handleExecute = async (toolName: string) => {
        setExecuting(toolName)
        const args = toolArgs[toolName] ?? {}
        try {
            const res = await fetch("/api/execute", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: toolName, arguments: args }),
            })
            const data = await res.json()
            const out = data.result ?? data.error ?? "No output"
            setResults((prev) => ({
                ...prev,
                [toolName]: typeof out === "string" ? out : JSON.stringify(out),
            }))
        } catch {
            setResults((prev) => ({ ...prev, [toolName]: "Execution failed" }))
        } finally {
            setExecuting(null)
        }
    }

    return (
        <div className="flex-1 flex flex-col min-h-0 container max-w-5xl mx-auto py-8 px-6 space-y-8">
            {/* Hero */}
            <div className="space-y-4 shrink-0">
                <div className="flex items-center gap-3">
                    <div className="p-3 rounded-xl bg-primary/10">
                        <Database className="w-8 h-8 text-primary" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold tracking-tight">Persistence Layer</h1>
                        <p className="text-muted-foreground">
                            Operational state management and long-horizon context retention for autonomous documentation processing.
                        </p>
                    </div>
                </div>
                <div className="flex flex-wrap gap-2">
                    <Badge variant="secondary" className="text-[10px] font-bold uppercase tracking-widest">Context Isolation</Badge>
                    <Badge variant="secondary" className="text-[10px] font-bold uppercase tracking-widest">Semantic Recall</Badge>
                    <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-widest">Substrate Active</Badge>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto min-h-0 pr-2 -mr-2 space-y-8">
                {/* Summary cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 shrink-0">
                    <Card className="bg-card/30 backdrop-blur-sm border-white/5">
                        <CardHeader className="pb-2">
                            <Shield className="w-5 h-5 text-primary mb-1" />
                            <CardTitle className="text-sm font-bold uppercase tracking-tight">Security Sandbox</CardTitle>
                            <CardDescription className="text-xs leading-relaxed">
                                Isolated runtime with policy-based guardrails ensures agents cannot perform unauthorized access when recalling or modifying persistent data.
                            </CardDescription>
                        </CardHeader>
                    </Card>
                    <Card className="bg-card/30 backdrop-blur-sm border-white/5">
                        <CardHeader className="pb-2">
                            <Zap className="w-5 h-5 text-primary mb-1" />
                            <CardTitle className="text-sm font-bold uppercase tracking-tight">Memory Density</CardTitle>
                            <CardDescription className="text-xs leading-relaxed">
                                Integrated compaction and summarization protocols reduce resource utilization for state history while maintaining high retrieval accuracy.
                            </CardDescription>
                        </CardHeader>
                    </Card>
                    <Card className="bg-card/30 backdrop-blur-sm border-white/5">
                        <CardHeader className="pb-2">
                            <Brain className="w-5 h-5 text-primary mb-1" />
                            <CardTitle className="text-sm font-bold uppercase tracking-tight">Persistent Context</CardTitle>
                            <CardDescription className="text-xs leading-relaxed">
                                Provides reliable, long-term context for documentation synthesis, bypassing volatile cache limitations.
                            </CardDescription>
                        </CardHeader>
                    </Card>
                </div>

                {/* tools: live or planned */}
                <Card className="flex flex-col border-white/10 shadow-xl overflow-hidden">
                    <CardHeader className="bg-muted/30 border-b shrink-0">
                        <div className="flex items-center gap-2">
                            <Terminal className="w-5 h-5 text-primary" />
                            <CardTitle className="text-lg">State Management Tools</CardTitle>
                        </div>
                        <CardDescription className="text-xs">
                            Direct interface for memory store, recall, and compaction operations.
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="p-6">
                        {loading ? (
                            <div className="flex items-center justify-center py-12">
                                <Loader2 className="w-8 h-8 animate-spin text-primary" />
                            </div>
                        ) : tools.length > 0 ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {tools.map((tool) => (
                                    <Card key={tool.name} className="border-white/5 bg-muted/20">
                                        <CardHeader className="pb-3 border-b border-white/5">
                                            <CardTitle className="text-sm font-mono text-primary">
                                                {tool.name.replace('persistence_', '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                            </CardTitle>
                                            <CardDescription className="text-[10px] leading-relaxed line-clamp-2">
                                                {tool.description.replace(/persistence/gi, 'Persistence').replace(/robofang/gi, 'Agent')}
                                            </CardDescription>
                                        </CardHeader>
                                        <CardContent className="space-y-4 pt-4">
                                            {getParamFields(tool).length > 0 &&
                                                getParamFields(tool).map(({ key, type, description }) => (
                                                    <div key={key} className="space-y-1.5">
                                                        <Label htmlFor={`mem-${tool.name}-${key}`} className="text-[10px] font-bold uppercase text-muted-foreground/80">
                                                            {key}
                                                        </Label>
                                                        <Input
                                                            id={`mem-${tool.name}-${key}`}
                                                            type={type === "number" ? "number" : "text"}
                                                            placeholder={(description || key).replace(/nemoclaw/gi, 'Persistence').replace(/robofang/gi, 'Agent')}
                                                            value={toolArgs[tool.name]?.[key] ?? ""}
                                                            onChange={(e) => setArg(tool.name, key, e.target.value)}
                                                            className="font-mono text-xs h-9 bg-background/50 border-white/5 focus-visible:ring-primary/50"
                                                        />
                                                    </div>
                                                ))}
                                            {results[tool.name] && (
                                                <ScrollArea className="h-32 rounded-lg border border-primary/20 bg-primary/5 p-3 text-[10px] font-mono whitespace-pre-wrap shadow-inner">
                                                    <div className="pr-4">{results[tool.name]}</div>
                                                </ScrollArea>
                                            )}
                                            <Button
                                                size="sm"
                                                className="w-full gap-2 font-bold uppercase tracking-widest text-[10px]"
                                                onClick={() => handleExecute(tool.name)}
                                                disabled={executing === tool.name}
                                            >
                                                {executing === tool.name ? (
                                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                                ) : (
                                                    <Play className="w-3.5 h-3.5 fill-current" />
                                                )}
                                                {executing === tool.name ? "Excuting Operation" : "Run Transaction"}
                                            </Button>
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>
                        ) : (
                            <div className="rounded-xl border border-dashed border-white/10 bg-muted/10 p-8 text-center space-y-6">
                                <div className="p-4 bg-primary/5 rounded-full w-fit mx-auto">
                                    <Database className="w-12 h-12 text-muted-foreground/30" />
                                </div>
                                <div className="space-y-2 max-w-md mx-auto">
                                    <p className="font-bold text-sm">No Persistence Tools Found</p>
                                    <p className="text-xs text-muted-foreground leading-relaxed">
                                        The subsystem is currently awaiting registry confirmation from the backend. Ensure the Docs MCP service is operational and exposes state management endpoints.
                                    </p>
                                </div>
                                <div className="pt-4 grid grid-cols-1 gap-3 max-w-sm mx-auto">
                                    {PLANNED_TOOLS.map((t) => (
                                        <div key={t.name} className="p-3 bg-card border border-white/5 rounded-lg text-left">
                                            <div className="font-mono text-[10px] text-primary font-bold">{t.name.replace('persistence_', '')}</div>
                                            <div className="text-[10px] text-muted-foreground mt-1">{t.description.replace(/NemoClaw/g, "Persistence")}</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
