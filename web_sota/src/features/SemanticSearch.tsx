import * as React from "react"
import { Search, FileText, Loader2, RefreshCcw, ArrowRight } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { AutoResizeTextarea } from "@/components/ui/auto-resize-textarea"

interface SearchResult {
    id: number | string
    title: string
    excerpt: string
    source: string
    score?: number
}

export function SemanticSearchView() {
    const [query, setQuery] = React.useState("")
    const [results, setResults] = React.useState<SearchResult[]>([])
    const [loading, setLoading] = React.useState(false)
    const [syncing, setSyncing] = React.useState(false)
    const [error, setError] = React.useState<string | null>(null)
    const [submitted, setSubmitted] = React.useState(false)

    const runSearch = React.useCallback(async () => {
        if (!query.trim()) return
        setLoading(true)
        setError(null)
        setSubmitted(true)
        try {
            const res = await fetch(`/api/search?q=${encodeURIComponent(query.trim())}`)
            if (!res.ok) throw new Error(res.statusText)
            const data = await res.json()
            setResults((Array.isArray(data) ? data : []).map((r: any) => ({
                id: r.id ?? Math.random(),
                title: r.filename ?? "Untitled",
                excerpt: r.content ? r.content.substring(0, 220) + "..." : "",
                source: r.relative_path ?? "docs",
                score: r.score
            })))
        } catch (e) {
            setError("Search failed.")
            setResults([])
        } finally {
            setLoading(false)
        }
    }, [query])

    const handleReindex = async () => {
        setSyncing(true)
        try {
            await fetch("/api/reindex")
        } finally {
            setSyncing(false)
        }
    }

    return (
        <div className="container max-w-4xl mx-auto py-8 px-6">
            <div className="mb-8 text-center space-y-2">
                <Badge variant="outline" className="text-[10px] uppercase tracking-wider">Docs only</Badge>
                <h1 className="text-3xl font-bold tracking-tight">Semantic Search</h1>
                <p className="text-muted-foreground">Neural retrieval over mcp-central-docs. No Plex/Calibre.</p>
                <Button
                    variant="ghost"
                    size="sm"
                    className="mt-2 gap-2 text-muted-foreground"
                    onClick={handleReindex}
                    disabled={syncing}
                >
                    {syncing ? <Loader2 className="w-3 h-3 animate-spin" /> : <RefreshCcw className="w-3 h-3" />}
                    {syncing ? "Reindexing..." : "Reindex docs"}
                </Button>
            </div>

            <Card className="mb-8">
                <CardContent className="pt-6">
                    <div className="flex gap-2">
                        <AutoResizeTextarea
                            placeholder="Ask in natural language..."
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); runSearch(); } }}
                            className="min-h-[2.5rem] max-h-[200px]"
                            rows={1}
                        />
                        <Button onClick={runSearch} disabled={loading || !query.trim()} className="shrink-0">
                            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {error && (
                <div className="mb-6 p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
                    {error}
                </div>
            )}

            <div className="space-y-4">
                {results.map((r) => (
                    <Card key={r.id} className="hover:bg-accent/5 transition-colors">
                        <CardHeader className="pb-2">
                            <div className="flex justify-between items-start gap-2">
                                <CardTitle className="text-base font-semibold line-clamp-2">{r.title}</CardTitle>
                                {r.score != null && (
                                    <Badge variant="secondary" className="text-[10px] font-mono shrink-0">
                                        {(r.score * 100).toFixed(0)}%
                                    </Badge>
                                )}
                            </div>
                            <p className="text-[11px] font-medium text-primary/70 uppercase tracking-wider">{r.source}</p>
                        </CardHeader>
                        <CardContent className="pt-0">
                            <p className="text-sm text-muted-foreground line-clamp-3">{r.excerpt || "No excerpt."}</p>
                        </CardContent>
                        <CardFooter className="pt-0 pb-4 border-t mt-4">
                            <span className="text-xs text-muted-foreground flex items-center gap-1">
                                <FileText className="w-3 h-3" /> View in Documentation
                                <ArrowRight className="w-3 h-3" />
                            </span>
                        </CardFooter>
                    </Card>
                ))}
            </div>

            {submitted && !loading && results.length === 0 && !error && (
                <p className="text-center text-muted-foreground py-8">No results. Try different wording or reindex docs.</p>
            )}
        </div>
    )
}
