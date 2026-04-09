import * as React from "react"
import { Search, Database, Loader2, RefreshCcw, ArrowRight, FileText, Film, BookOpen, Layers } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"

interface SearchResult {
    id: number | string
    title: string
    excerpt: string
    source: string
    score?: number
    coverArt?: string
    metadata?: any
}

type SearchSource = 'docs' | 'plex' | 'calibre'

export function SearchView() {
    const [query, setQuery] = React.useState('')
    const [source, setSource] = React.useState<SearchSource>('docs')
    const [results, setResults] = React.useState<SearchResult[]>([])
    const [answer, setAnswer] = React.useState<string | null>(null)
    const [isNeural, setIsNeural] = React.useState(false)
    const [loading, setLoading] = React.useState(false)
    const [phase, setPhase] = React.useState<'idle' | 'searching' | 'synthesizing'>('idle')
    const [syncing, setSyncing] = React.useState(false)
    const [error, setError] = React.useState<string | null>(null)

    const searchPorts = {
        docs: "", // local relative
        plex: "http://localhost:10760",
        calibre: "http://localhost:10762"
    }

    React.useEffect(() => {
        if (!query) {
            setResults([])
            setError(null)
            return
        }

        if (!query.trim()) return

        setLoading(true)
        setPhase('searching')
        setError(null)
        setAnswer(null)

        const timeout = setTimeout(async () => {
            try {
                const baseUrl = searchPorts[source]

                let searchEndpoint = ""
                let chatEndpoint = ""

                if (source === 'docs') {
                    searchEndpoint = `/api/search?q=${encodeURIComponent(query)}`
                    chatEndpoint = `/api/chat`
                } else {
                    // Plex and Calibre expect POST /api/v1/search
                    searchEndpoint = `${baseUrl}/api/v1/search`
                    chatEndpoint = `${baseUrl}/api/v1/chat`
                }

                let data = null

                if (source === 'docs') {
                    const res = await fetch(searchEndpoint)
                    if (!res.ok) throw new Error(`Search service error: ${res.statusText}`)
                    data = await res.json()
                } else {
                    const res = await fetch(searchEndpoint, {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ query: query, limit: 12, search_type: 'metadata' })
                    })
                    if (!res.ok) throw new Error(`Search service error: ${res.statusText}`)
                    const payload = await res.json()
                    data = payload.data || payload.results || []
                }

                if (isNeural) {
                    setPhase('synthesizing')

                    try {
                        const synthRes = await fetch(chatEndpoint, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ message: query })
                        })
                        if (synthRes.ok) {
                            const synthData = await synthRes.json()
                            setAnswer(synthData.answer || synthData.response)
                        } else {
                            setAnswer("Documentation found, but AI synthesis failed.")
                        }
                    } catch (e) {
                        setAnswer("Chat endpoint unavailable.")
                    }
                }

                // Map results generically based on source
                if (source === 'docs') {
                    setResults(data.map((r: any) => ({
                        id: r.id || Math.random(),
                        title: r.filename || "Untitled",
                        excerpt: r.content ? r.content.substring(0, 200) + "..." : "",
                        source: r.relative_path || "docs",
                        score: r.score
                    })))
                } else if (source === 'plex') {
                    setResults(data.map((r: any) => ({
                        id: r.id || Math.random(),
                        title: r.metadata?.title || r.metadata?.fm_title || r.filename || "Untitled",
                        excerpt: r.content ? r.content.substring(0, 150) + "..." : (r.metadata?.summary || ""),
                        source: r.metadata?.type || r.metadata?.library_name || "plex",
                        score: r.score,
                        coverArt: r.metadata?.thumb || undefined,
                        metadata: r.metadata
                    })))
                } else if (source === 'calibre') {
                    setResults(data.map((r: any) => ({
                        id: r.id || Math.random(),
                        title: r.metadata?.title || r.filename || "Untitled Book",
                        excerpt: r.metadata?.blurb ? r.metadata.blurb.substring(0, 150) + "..." : (r.content ? r.content.substring(0, 150) + "..." : ""),
                        source: r.metadata?.authors || "calibre",
                        score: r.score,
                        metadata: r.metadata
                    })))
                }

            } catch (err) {
                console.error("Search failed:", err)
                setError(`Unable to connect to ${source.toUpperCase()} search service. Ensure the server is running on its designated port.`)
            } finally {
                setLoading(false)
                setPhase('idle')
            }
        }, 500)
        return () => clearTimeout(timeout)
    }, [query, isNeural, source])

    const handleSync = async () => {
        if (source !== 'docs') return // Only support syncing docs natively for now
        setSyncing(true)
        try {
            const res = await fetch('/api/reindex')
            await res.json()
        } catch (err) {
            console.error("Sync failed:", err)
        } finally {
            setSyncing(false)
        }
    }

    return (
        <div className="flex-1 flex flex-col min-h-0 container max-w-6xl mx-auto py-12 px-6 overflow-y-auto">
            <div className="mb-12 text-center space-y-4">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 mb-2">
                    <Database className="w-3.5 h-3.5 text-primary" />
                    <span className="text-[10px] font-bold uppercase tracking-wider text-primary">Hybrid Semantic Core</span>
                </div>
                <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-b from-foreground to-foreground/70 bg-clip-text text-transparent">
                    Context Search Hub
                </h1>
                <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
                    Semantic retrieval across documentation, infrastructure, and technical resources.
                </p>

                {source === 'docs' && (
                    <div className="flex justify-center mt-2">
                        <Button
                            variant="ghost"
                            size="sm"
                            className="text-[10px] uppercase font-bold tracking-widest gap-2 text-muted-foreground hover:text-primary"
                            onClick={handleSync}
                            disabled={syncing}
                        >
                            {syncing ? <Loader2 className="w-3 h-3 animate-spin" /> : <RefreshCcw className="w-3 h-3" />}
                            {syncing ? "Indexing..." : "Sync Documentation"}
                        </Button>
                    </div>
                )}
            </div>

            {/* Search Interface */}
            <div className="relative max-w-3xl mx-auto mb-16 group z-10">
                <div className="absolute -inset-1 bg-gradient-to-r from-primary to-secondary rounded-xl blur opacity-25 group-hover:opacity-60 transition duration-1000"></div>
                <div className="relative bg-card rounded-xl shadow-2xl border ring-1 ring-border/50">
                    <div className="flex flex-col">
                        <div className="flex items-center p-2 pl-4">
                            <Select value={source} onValueChange={(val: any) => setSource(val)}>
                                <SelectTrigger className="w-[140px] border-none shadow-none focus:ring-0 text-muted-foreground font-semibold uppercase tracking-wider text-xs bg-muted/30">
                                    <SelectValue placeholder="Source" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="docs"><div className="flex items-center gap-2"><FileText className="w-3 h-3" /> Docs</div></SelectItem>
                                    <SelectItem value="plex"><div className="flex items-center gap-2"><Film className="w-3 h-3" /> Plex</div></SelectItem>
                                    <SelectItem value="calibre"><div className="flex items-center gap-2"><BookOpen className="w-3 h-3" /> Calibre</div></SelectItem>
                                    <SelectItem value="all" disabled><div className="flex items-center gap-2 text-muted-foreground"><Layers className="w-3 h-3" /> All (WIP)</div></SelectItem>
                                </SelectContent>
                            </Select>

                            <div className="w-px h-8 bg-border mx-3"></div>

                            <Search className="w-6 h-6 text-muted-foreground mr-2" />
                            <Input
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                placeholder={`Search ${source.toUpperCase()} organically...`}
                                className="border-none shadow-none focus-visible:ring-0 text-xl py-8 bg-transparent"
                            />
                            {loading && <div className="w-5 h-5 border-2 border-primary border-t-transparent rounded-full animate-spin mx-4"></div>}
                        </div>
                        <div className="flex items-center gap-4 px-6 py-3 border-t bg-muted/20 rounded-b-xl">
                            <div className="flex items-center space-x-2">
                                <input
                                    type="checkbox"
                                    id="neural-mode"
                                    checked={isNeural}
                                    onChange={(e) => setIsNeural(e.target.checked)}
                                    className="w-4 h-4 accent-primary"
                                />
                                <label htmlFor="neural-mode" className="text-xs font-semibold uppercase tracking-widest text-muted-foreground cursor-pointer select-none">
                                    Autonomous Synthesis & Analysis
                                </label>
                            </div>
                            {loading && (
                                <div className="flex items-center gap-2 text-[10px] font-bold text-primary animate-pulse uppercase tracking-widest ml-4">
                                    <Loader2 className="w-3 h-3 animate-spin" />
                                    {phase === 'searching' ? 'Retrieving Vector Context...' : 'Synthesizing Technical Insight...'}
                                </div>
                            )}
                            <Badge variant="outline" className="ml-auto text-[9px] uppercase tracking-widest text-muted-foreground shadow-sm">
                                Vector Engine Backed
                            </Badge>
                        </div>
                    </div>
                </div>
            </div>

            {/* AI Answer Section */}
            {isNeural && answer && (
                <Card className="max-w-4xl mx-auto mb-12 border-primary/30 bg-primary/5 shadow-inner backdrop-blur-md animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <CardHeader className="pb-2">
                        <div className="flex items-center gap-2 text-primary">
                            <Database className="w-4 h-4" />
                            <CardTitle className="text-sm font-bold uppercase tracking-widest">AI Synthesis</CardTitle>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <p className="text-lg leading-relaxed text-foreground/90 font-medium">
                            {answer}
                        </p>
                        <div className="mt-4 pt-4 border-t border-primary/20 flex gap-4 text-xs text-muted-foreground">
                            <span>Context Chunks: {results.length}</span>
                            <span>Target Engine: {source.toUpperCase()}</span>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Error State */}
            {error && (
                <div className="max-w-3xl mx-auto mb-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-3 text-destructive animate-in fade-in">
                    <div className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                    <p className="font-semibold">{error}</p>
                </div>
            )}

            {/* Results Grid - Responsive based on source type */}
            <div className={`grid gap-6 ${source === 'plex' ? 'grid-cols-2 md:grid-cols-3 lg:grid-cols-4' : 'grid-cols-1 md:grid-cols-2'}`}>
                {results.map((result) => (
                    <Card key={result.id} className="group overflow-hidden flex flex-col hover:bg-accent/5 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 border-transparent ring-1 ring-border hover:border-primary/30 h-full">
                        {/* Cover Art for Plex */}
                        {source === 'plex' && result.coverArt && (
                            <div className="w-full aspect-[2/3] bg-muted relative overflow-hidden shrink-0 border-b">
                                {/* Normally we'd need to proxy the Plex image or have a valid URL. We handle missing images gracefully */}
                                <img
                                    src={`http://localhost:10760/proxy?url=${encodeURIComponent(result.coverArt)}`}
                                    alt="Cover"
                                    className="object-cover w-full h-full transform group-hover:scale-105 transition-transform duration-700"
                                    onError={(e) => { e.currentTarget.style.display = 'none'; e.currentTarget.parentElement!.classList.add('flex', 'items-center', 'justify-center'); e.currentTarget.parentElement!.innerHTML = '<span class="text-muted-foreground/30 font-bold text-4xl">PLEX</span>'; }}
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-4">
                                    <Button size="sm" className="w-full shadow-lg backdrop-blur-md">View Details</Button>
                                </div>
                            </div>
                        )}

                        <CardHeader className="pb-2 pt-4 flex-none">
                            <div className="flex justify-between items-start gap-3">
                                <CardTitle className="text-lg font-bold group-hover:text-primary transition-colors line-clamp-2 leading-tight">
                                    {result.title}
                                </CardTitle>
                                {result.score !== undefined && (
                                    <Badge variant="secondary" className="text-[10px] font-mono shrink-0">
                                        {(result.score * 100).toFixed(0)}%
                                    </Badge>
                                )}
                            </div>
                            <div className="text-[11px] font-medium text-primary/70 uppercase tracking-wider line-clamp-1 mt-1">
                                {result.source}
                            </div>
                        </CardHeader>
                        <CardContent className="flex-1">
                            <p className="text-sm text-muted-foreground leading-relaxed line-clamp-4">
                                {result.excerpt || "No description available."}
                            </p>
                        </CardContent>
                        {source !== 'plex' && (
                            <CardFooter className="pt-0 pb-4 border-t border-border/50 mt-4 bg-muted/10 h-12">
                                <div className="w-full flex items-center justify-between text-xs font-semibold text-muted-foreground group-hover:text-primary transition-colors mt-4">
                                    <span>{source === 'calibre' ? 'Read Metadata' : 'View Documentation'}</span>
                                    <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                                </div>
                            </CardFooter>
                        )}
                    </Card>
                ))}
            </div>

            {/* Empty State / Initial View */}
            {!query && !error && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 max-w-4xl mx-auto">
                    {[
                        { icon: FileText, title: "Docs Search", desc: "Instantly retrieve protocols from mcp-central-docs." },
                        { icon: Film, title: "Media RAG", desc: "Semantically search plots, themes, and subtitles across Plex." },
                        { icon: BookOpen, title: "Deep Library", desc: "Query Calibre books by concepts and metaphors." }
                    ].map((feature, i) => (
                        <div key={i} className="p-8 rounded-2xl bg-card/30 border border-border/50 backdrop-blur-md text-center hover:bg-card/60 transition-colors shadow-sm">
                            <feature.icon className="w-10 h-10 mx-auto mb-5 text-primary/70" />
                            <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                            <p className="text-sm text-muted-foreground leading-relaxed">{feature.desc}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
