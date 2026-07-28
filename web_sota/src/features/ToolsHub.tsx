import * as React from "react"
import { Terminal, Play, Loader2, AlertCircle, Copy, Check, ExternalLink } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog"
import { API_BASE } from "@/lib/api"

interface Tool {
    name: string
    description: string
    parameters?: {
        properties?: Record<string, { type?: string; description?: string }>
        required?: string[]
    }
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

function formatResult(raw: string): string {
    const s = typeof raw === "string" ? raw : String(raw)
    try {
        const parsed = JSON.parse(s)
        return JSON.stringify(parsed, null, 2)
    } catch {
        return s
    }
}

export function ToolsHub() {
    const [tools, setTools] = React.useState<Tool[]>([])
    const [loading, setLoading] = React.useState(true)
    const [executing, setExecuting] = React.useState<string | null>(null)
    const [results, setResults] = React.useState<Record<string, string>>({})
    const [resultErrors, setResultErrors] = React.useState<Record<string, boolean>>({})
    const [copied, setCopied] = React.useState<string | null>(null)
    const [resultPopupTool, setResultPopupTool] = React.useState<string | null>(null)
    const [toolArgs, setToolArgs] = React.useState<Record<string, Record<string, string>>>({})

    React.useEffect(() => {
        fetch(API_BASE + '/api/tools')
            .then(res => res.json())
            .then(data => {
                setTools(Array.isArray(data) ? data : [])
                setLoading(false)
            })
            .catch(() => {
                setTools([])
                setLoading(false)
            })
    }, [])

    const setArg = React.useCallback((toolName: string, paramKey: string, value: string) => {
        setToolArgs(prev => ({
            ...prev,
            [toolName]: { ...(prev[toolName] ?? {}), [paramKey]: value },
        }))
    }, [])

    const handleExecute = async (toolName: string) => {
        setExecuting(toolName)
        const args = toolArgs[toolName] ?? {}
        try {
            const res = await fetch(API_BASE + '/api/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: toolName, arguments: args })
            })
            const data = await res.json()
            const out = data.result ?? data.error ?? "No output"
            const isError = !res.ok || data.error != null
            setResults(prev => ({ ...prev, [toolName]: typeof out === "string" ? out : JSON.stringify(out) }))
            setResultErrors(prev => ({ ...prev, [toolName]: isError }))
            setResultPopupTool(toolName)
        } catch (err) {
            setResults(prev => ({ ...prev, [toolName]: "Execution failed" }))
            setResultErrors(prev => ({ ...prev, [toolName]: true }))
            setResultPopupTool(toolName)
        } finally {
            setExecuting(null)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-64">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        )
    }

    return (
        <div data-testid="tools-page" className="container max-w-6xl mx-auto py-12 px-6">
            <div className="mb-10 space-y-4">
                <h1 className="text-4xl font-bold tracking-tight">Tools Hub</h1>
                <p className="text-lg text-muted-foreground">Direct access to registered MCP tools and utilities.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 items-stretch">
                {tools.map((tool) => (
                    <Card key={tool.name} className="group hover:border-primary/50 transition-all hover:shadow-lg flex flex-col h-full">
                        <CardHeader className="pb-4 shrink-0">
                            <div className="flex justify-between items-start">
                                <div className="p-2.5 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
                                    <Terminal className="w-5 h-5 text-primary" />
                                </div>
                                <Badge variant="default" className="uppercase text-[10px]">
                                    Active
                                </Badge>
                            </div>
                            <CardTitle className="mt-4 text-xl font-mono">{tool.name}</CardTitle>
                            <CardDescription className="mt-2 line-clamp-2">{tool.description}</CardDescription>
                        </CardHeader>
                        <CardContent className="flex-1 flex flex-col min-h-0 space-y-3">
                            {getParamFields(tool).length > 0 && (
                                <div className="space-y-2">
                                    {getParamFields(tool).map(({ key, type, description }) => (
                                        <div key={key} className="space-y-1">
                                            <Label htmlFor={`${tool.name}-${key}`} className="block">
                                                {key}
                                                {description && (
                                                    <span className="block text-muted-foreground font-normal text-sm">{description}</span>
                                                )}
                                            </Label>
                                            <Input
                                                id={`${tool.name}-${key}`}
                                                type={type === "number" ? "number" : "text"}
                                                placeholder={key}
                                                value={toolArgs[tool.name]?.[key] ?? ""}
                                                onChange={(e) => setArg(tool.name, key, e.target.value)}
                                                className="font-mono text-sm"
                                            />
                                        </div>
                                    ))}
                                </div>
                            )}
                            {results[tool.name] && (
                                <Button
                                    variant="outline"
                                    size="sm"
                                    className="w-full gap-2"
                                    onClick={() => setResultPopupTool(tool.name)}
                                >
                                    <ExternalLink className="w-3.5 h-3.5" />
                                    View output
                                </Button>
                            )}
                        </CardContent>
                        <CardFooter className="pt-2 shrink-0">
                            <Button
                                className="w-full gap-2"
                                variant="secondary"
                                onClick={() => handleExecute(tool.name)}
                                disabled={executing === tool.name}
                            >
                                {executing === tool.name ? (
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                ) : (
                                    <Play className="w-4 h-4" />
                                )}
                                {executing === tool.name ? "Executing..." : "Execute Tool"}
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            {tools.length === 0 && (
                <div className="text-center py-20 bg-muted/20 rounded-2xl border-2 border-dashed">
                    <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <h3 className="text-xl font-bold">No Tools Registered</h3>
                    <p className="text-muted-foreground">Ensure the MCP server is correctly initialized.</p>
                </div>
            )}

            <Dialog open={resultPopupTool !== null} onOpenChange={(open) => !open && setResultPopupTool(null)}>
                <DialogContent className="max-w-3xl max-h-[85vh] flex flex-col gap-4">
                    <DialogHeader>
                        <DialogTitle className="font-mono">
                            {resultPopupTool ? `Result: ${resultPopupTool}` : "Output"}
                        </DialogTitle>
                    </DialogHeader>
                    {resultPopupTool && results[resultPopupTool] != null && (
                        <>
                            <ScrollArea
                                className={`h-[60vh] rounded-lg border p-4 text-base font-mono whitespace-pre-wrap break-words ${resultErrors[resultPopupTool] ? "bg-destructive/10 border-destructive/30 text-destructive" : "bg-muted/50"}`}
                            >
                                <div className="pr-4">
                                    {formatResult(results[resultPopupTool])}
                                </div>
                            </ScrollArea>
                            <DialogFooter>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    className="gap-2"
                                    onClick={async () => {
                                        const text = formatResult(results[resultPopupTool])
                                        await navigator.clipboard.writeText(text)
                                        setCopied(resultPopupTool)
                                        setTimeout(() => setCopied(null), 2000)
                                    }}
                                >
                                    {copied === resultPopupTool ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                                    {copied === resultPopupTool ? "Copied" : "Copy"}
                                </Button>
                            </DialogFooter>
                        </>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    )
}
