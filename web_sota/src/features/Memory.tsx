import * as React from "react"
import { Database, Loader2, Play } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"
import { API_BASE } from "@/lib/api"

const PERSISTENCE_TOOL_PREFIX = "persistence"

interface Tool {
    name: string
    description: string
    parameters?: { properties?: Record<string, { type?: string; description?: string }> }
}

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
        fetch(API_BASE + "/api/tools")
            .then((res) => res.json())
            .then((data: { tools?: Tool[] }) => {
                const list = data.tools ?? []
                setTools(list.filter((t) => t.name.toLowerCase().includes(PERSISTENCE_TOOL_PREFIX)))
                setLoading(false)
            })
            .catch(() => {
                setTools([])
                setLoading(false)
            })
    }, [])

    const handleExecute = async (toolName: string) => {
        setExecuting(toolName)
        const args = toolArgs[toolName] ?? {}
        try {
            const res = await fetch(API_BASE + "/api/execute", {
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
            <div className="space-y-2 shrink-0">
                <div className="flex items-center gap-3">
                    <Database className="w-8 h-8 text-primary" />
                    <h1 className="text-3xl font-bold tracking-tight">Persistence</h1>
                </div>
                <p className="text-muted-foreground">
                    Store and recall structured data across sessions via the backend&apos;s memory store.
                    Data persists in SQLite + LanceDB and survives server restarts.
                </p>
            </div>

            <div className="flex-1 overflow-y-auto min-h-0 space-y-4">
                <p className="text-xs text-muted-foreground">
                    Namespaces isolate data between use cases. Store content under a namespace,
                    then recall it later with a semantic query. Compaction reports show per-namespace stats.
                </p>

                <Card className="flex flex-col border-white/10 shadow-xl overflow-hidden">
                    <CardHeader className="bg-muted/30 border-b shrink-0">
                        <CardTitle className="text-lg">Tools</CardTitle>
                        <CardDescription className="text-xs">
                            Loaded from the backend tool registry. Execute directly from this page.
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
                                            <CardTitle className="text-sm font-mono text-primary">{tool.name}</CardTitle>
                                            <CardDescription className="text-xs leading-relaxed">
                                                {tool.description}
                                            </CardDescription>
                                        </CardHeader>
                                        <CardContent className="space-y-4 pt-4">
                                            {getParamFields(tool).map(({ key, type }) => (
                                                <div key={key} className="space-y-1.5">
                                                    <Label htmlFor={`mem-${tool.name}-${key}`} className="text-xs font-bold text-muted-foreground/80">
                                                        {key}
                                                    </Label>
                                                    <Input
                                                        id={`mem-${tool.name}-${key}`}
                                                        type={type === "number" ? "number" : "text"}
                                                        value={toolArgs[tool.name]?.[key] ?? ""}
                                                        onChange={(e) =>
                                                            setToolArgs((prev) => ({
                                                                ...prev,
                                                                [tool.name]: { ...(prev[tool.name] ?? {}), [key]: e.target.value },
                                                            }))
                                                        }
                                                        className="font-mono text-xs h-9 bg-background/50"
                                                    />
                                                </div>
                                            ))}
                                            {results[tool.name] && (
                                                <ScrollArea className="h-32 rounded-lg border bg-muted/20 p-3 text-xs font-mono whitespace-pre-wrap">
                                                    <div className="pr-4">{results[tool.name]}</div>
                                                </ScrollArea>
                                            )}
                                            <Button
                                                size="sm"
                                                className="w-full gap-2 text-xs"
                                                onClick={() => handleExecute(tool.name)}
                                                disabled={executing === tool.name}
                                            >
                                                {executing === tool.name ? (
                                                    <Loader2 className="w-3 h-3 animate-spin" />
                                                ) : (
                                                    <Play className="w-3 h-3 fill-current" />
                                                )}
                                                {executing === tool.name ? "Running..." : "Execute"}
                                            </Button>
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>
                        ) : (
                            <div className="rounded-xl border border-dashed border-white/10 bg-muted/10 p-8 text-center space-y-4">
                                <Database className="w-10 h-10 text-muted-foreground/30 mx-auto" />
                                <p className="font-bold text-sm">No persistence tools registered</p>
                                <p className="text-xs text-muted-foreground">
                                    The backend is running but does not expose any persistence tools.
                                    Check that the memory store initialized correctly.
                                </p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
