import * as React from "react"
import { BookOpen, FileText, Folder, ChevronRight, Search, Loader2, Maximize2, Minimize2, RefreshCcw } from "lucide-react"
import { cn } from "@/lib/utils"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import ReactMarkdown from "react-markdown"
import rehypeHighlight from "rehype-highlight"
import "highlight.js/styles/github-dark.css"
import { API_BASE } from "@/lib/api" // Import highlight.js styles

interface DocNode {
    id: string
    title: string
    type: 'folder' | 'file'
    children?: DocNode[]
    path?: string
}

export function Documents() {
    const [docTree, setDocTree] = React.useState<DocNode[]>([])
    const [selectedDoc, setSelectedDoc] = React.useState<DocNode | null>(null)
    const [searchQuery, setSearchQuery] = React.useState("")
    const [content, setContent] = React.useState<string | null>(null)
    const [treeLoading, setTreeLoading] = React.useState(true)
    const [contentLoading, setContentLoading] = React.useState(false)
    const [ingestFolder, setIngestFolder] = React.useState("")
    const [ingestLoading, setIngestLoading] = React.useState(false)
    const [ingestMessage, setIngestMessage] = React.useState<string | null>(null)
    const [reindexLoading, setReindexLoading] = React.useState(false)
    const [reindexMessage, setReindexMessage] = React.useState<string | null>(null)

    // Fetch Doc Tree
    React.useEffect(() => {
        const fetchTree = async () => {
            try {
                const res = await fetch(API_BASE + '/api/tree')
                if (!res.ok) throw new Error("Failed to load documentation tree")
                const data = await res.json()
                setDocTree(data)
            } catch (err) {
                console.error("Failed to load doc tree:", err)
            } finally {
                setTreeLoading(false)
            }
        }
        fetchTree()
    }, [])

    // Fetch Content when Doc Selected
    React.useEffect(() => {
        if (!selectedDoc || selectedDoc.type === 'folder' || !selectedDoc.path) return

        const fetchContent = async () => {
            setContentLoading(true)
            try {
                const res = await fetch(selectedDoc.path!)
                if (!res.ok) throw new Error("Failed to load content")
                const data = await res.json()
                setContent(data.content)
            } catch (err) {
                console.error("Failed to load content:", err)
                setContent("# Error loading content\n\nCould not retrieve document.")
            } finally {
                setContentLoading(false)
            }
        }
        fetchContent()
    }, [selectedDoc])

    const [isFullScreen, setIsFullScreen] = React.useState(false)

    // Recursive search filter
    const filterTree = (nodes: DocNode[], query: string): DocNode[] => {
        return nodes.reduce((acc: DocNode[], node) => {
            if (node.title.toLowerCase().includes(query.toLowerCase())) {
                acc.push(node)
            } else if (node.children) {
                const filteredChildren = filterTree(node.children, query)
                if (filteredChildren.length > 0) {
                    acc.push({ ...node, children: filteredChildren })
                }
            }
            return acc
        }, [])
    }

    const displayedTree = searchQuery ? filterTree(docTree, searchQuery) : docTree

    return (
        <div data-testid="documents-page" className={cn(
            "mx-auto py-6 px-4 flex-1 h-0 min-h-0 flex gap-6 transition-all duration-300",
            isFullScreen ? "max-w-[98vw]" : "container max-w-7xl"
        )}>

            {/* Sidebar Navigation */}
            {!isFullScreen && (
                <Card className="w-80 flex flex-col h-full border-white/10 shadow-2xl bg-card/30 backdrop-blur-md shrink-0 rounded-2xl overflow-hidden">
                    <div className="p-4 border-b border-white/5 space-y-4 shrink-0 bg-muted/20">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2 font-bold text-base uppercase tracking-wider">
                                <BookOpen className="w-4 h-4 text-primary" />
                                <span>Artifacts</span>
                            </div>
                        </div>

                        <form onSubmit={async (e) => {
                            e.preventDefault();
                            if (!ingestFolder.trim()) return;
                            setIngestLoading(true);
                            try {
                                const res = await fetch(API_BASE + "/api/ingest_folder", {
                                    method: "POST",
                                    headers: { "Content-Type": "application/json" },
                                    body: JSON.stringify({ folder_path: ingestFolder })
                                });
                                const data = await res.json();
                                if (data.success) {
                                    setIngestMessage(data.message);
                                } else {
                                    setIngestMessage(data.error || "Failed to ingest folder");
                                }
                            } catch (err) {
                                setIngestMessage("Network error during ingestion");
                            } finally {
                                setIngestLoading(false);
                            }
                        }} className="space-y-2">
                            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest pl-1">Source Registry</div>
                            <div className="flex gap-2">
                                <Input
                                    className="h-8 bg-background/50 text-[11px] font-mono border-white/5"
                                    placeholder="D:/Research/Notes"
                                    value={ingestFolder}
                                    onChange={e => setIngestFolder(e.target.value)}
                                />
                                <Button type="submit" size="sm" className="h-8 px-3 text-[11px] font-bold uppercase tracking-widest" disabled={ingestLoading || !ingestFolder.trim()}>
                                    {ingestLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : "Index"}
                                </Button>
                            </div>
                            {ingestMessage && <div className="text-[10px] text-primary/80 mt-1 pl-1 line-clamp-1">{ingestMessage}</div>}
                        </form>

                        <div className="space-y-2">
                            <div className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest pl-1">Vector Engine</div>
                            <Button
                                variant="outline"
                                size="sm"
                                className="w-full h-8 gap-2 text-[11px] font-bold uppercase tracking-widest border-white/5"
                                disabled={reindexLoading}
                                    onClick={async () => {
                                        setReindexLoading(true); setReindexMessage(null);
                                        try {
                                            const r = await fetch(API_BASE + "/api/reindex", { method: "POST", signal: AbortSignal.timeout(10000) });
                                            const d = await r.json();
                                            setReindexMessage(d.message ?? (r.ok ? "Reindex started in background." : "Failed."));
                                        } catch { setReindexMessage("Could not reach backend."); }
                                        finally { setReindexLoading(false); }
                                    }}
                            >
                                {reindexLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : <RefreshCcw className="w-3 h-3" />}
                                {reindexLoading ? "Processing" : "Force Reindex"}
                            </Button>
                            {reindexMessage && <div className="text-[10px] text-muted-foreground pl-1 line-clamp-1">{reindexMessage}</div>}
                        </div>

                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-3 w-3 text-muted-foreground" />
                            <Input
                                placeholder="Search registry..."
                                className="h-9 pl-9 bg-background/50 text-sm border-white/5"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </div>
                    <ScrollArea className="flex-1 p-2 min-h-0">
                        {treeLoading ? (
                            <div className="flex justify-center p-8">
                                <Loader2 className="w-6 h-6 animate-spin text-primary/50" />
                            </div>
                        ) : (
                            <div className="space-y-1">
                                {displayedTree.map((node) => (
                                    <DocTreeItem key={node.id} node={node} onSelect={setSelectedDoc} selectedId={selectedDoc?.id} />
                                ))}
                            </div>
                        )}
                    </ScrollArea>
                </Card>
            )}

            {/* Main Content Area */}
            <div className="flex-1 h-full overflow-hidden flex flex-col min-w-0">
                {selectedDoc ? (
                    <Card className="h-full border-white/10 shadow-2xl bg-card/30 backdrop-blur-md flex flex-col rounded-2xl overflow-hidden">
                        <CardHeader className="border-b border-white/5 px-6 py-4 bg-muted/20 shrink-0 flex flex-row items-center justify-between space-y-0">
                            <div className="min-w-0">
                                <div className="flex items-center gap-2 text-[10px] font-bold uppercase tracking-widest text-primary mb-1">
                                    <span>Workspace</span>
                                    <ChevronRight className="w-3 h-3" />
                                    <span className="text-muted-foreground">{selectedDoc.type === 'folder' ? 'Registry Node' : 'Logical Object'}</span>
                                </div>
                                <CardTitle className="text-xl font-bold truncate">{selectedDoc.title}</CardTitle>
                            </div>
                            <Button
                                variant="ghost"
                                size="icon"
                                className="hover:bg-primary/10 hover:text-primary transition-colors h-8 w-8"
                                onClick={() => setIsFullScreen(!isFullScreen)}
                                title={isFullScreen ? "Exit Full Screen" : "Enter Full Screen"}
                            >
                                {isFullScreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                            </Button>
                        </CardHeader>
                        <ScrollArea className="flex-1 min-h-0 bg-background/20">
                            <div className="prose prose-slate dark:prose-invert max-w-4xl mx-auto py-10 px-8 pb-32">
                                {contentLoading ? (
                                    <div className="flex items-center gap-3 text-muted-foreground font-mono text-sm py-12 justify-center">
                                        <Loader2 className="w-5 h-5 animate-spin text-primary" />
                                        <span>RETRIEVING CONTENT...</span>
                                    </div>
                                ) : (
                                    <ReactMarkdown
                                        rehypePlugins={[rehypeHighlight]}
                                        components={{
                                            h1: ({ node, ...props }) => <h1 className="text-3xl font-extrabold mb-8 mt-12 text-foreground tracking-tight" {...props} />,
                                            h2: ({ node, ...props }) => <h2 className="text-xl font-bold mb-6 mt-10 pb-2 border-b border-white/10 uppercase tracking-wider text-primary" {...props} />,
                                            h3: ({ node, ...props }) => <h3 className="text-lg font-bold mb-4 mt-8 tracking-tight" {...props} />,
                                            p: ({ node, ...props }) => <p className="leading-relaxed mb-6 text-muted-foreground" {...props} />,
                                            ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-6 space-y-3 marker:text-primary [&>li]:pl-1" {...props} />,
                                            ol: ({ node, ...props }) => <ol className="list-decimal pl-6 mb-6 space-y-3 marker:text-primary marker:font-bold [&>li]:pl-1" {...props} />,
                                            // li: Removed to satisfy structural lint constraints
                                            code: ({ node, className, children, ...props }) => {
                                                const match = /language-(\w+)/.exec(className || '')
                                                return match ? (
                                                    <code className={cn("text-[13px] font-mono", className)} {...props}>
                                                        {children}
                                                    </code>
                                                ) : (
                                                    <code className="bg-primary/10 text-primary px-1.5 py-0.5 rounded text-[12px] font-mono font-medium border border-primary/20" {...props}>
                                                        {children}
                                                    </code>
                                                )
                                            },
                                            pre: ({ node, ...props }) => <pre className="bg-muted/30 p-5 rounded-xl overflow-x-auto mb-8 border border-white/5 shadow-inner font-mono text-[13px]" {...props} />,
                                            blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-primary bg-primary/5 p-4 rounded-r-lg italic my-8 text-muted-foreground" {...props} />,
                                            table: ({ node, ...props }) => (
                                                <div className="overflow-x-auto mb-8 border border-white/10 rounded-xl">
                                                    <table className="w-full border-collapse text-sm" {...props} />
                                                </div>
                                            ),
                                            th: ({ node, ...props }) => <th className="bg-muted/50 p-3 border-b border-white/10 text-left font-bold uppercase tracking-widest text-[10px]" {...props} />,
                                            td: ({ node, ...props }) => <td className="p-3 border-b border-white/5 text-muted-foreground" {...props} />,
                                        }}
                                    >
                                        {content || ""}
                                    </ReactMarkdown>
                                )}
                            </div>
                        </ScrollArea>
                    </Card>
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-muted-foreground space-y-6">
                        <div className="p-8 bg-primary/5 rounded-full ring-1 ring-primary/20 animate-pulse">
                            <FileText className="w-16 h-16 text-primary/30" />
                        </div>
                        <div className="text-center space-y-2">
                            <h2 className="text-2xl font-extrabold text-foreground tracking-tight">Select Object</h2>
                            <p className="max-w-xs text-sm leading-relaxed text-muted-foreground mx-auto">
                                Browse the documentation hierarchy in the sidebar to retrieve technical specifications or memory snapshots.
                            </p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}

function DocTreeItem({ node, onSelect, selectedId, level = 0 }: { node: DocNode, onSelect: (n: DocNode) => void, selectedId?: string, level?: number }) {
    const isSelected = selectedId === node.id
    const [isOpen, setIsOpen] = React.useState(level < 1) // Auto-open root level
    const hasChildren = node.children && node.children.length > 0

    return (
        <div className="select-none text-sm">
            <Button
                variant={isSelected ? "secondary" : "ghost"}
                className="w-full justify-start h-8 px-2 relative font-normal"
                style={{ paddingLeft: `${(level * 12) + 8}px` }}
                onClick={() => {
                    if (node.type === 'folder') setIsOpen(!isOpen)
                    else onSelect(node)
                }}
            >
                <span className="flex items-center gap-2 truncate w-full text-left">
                    {node.type === 'folder' && (
                        <ChevronRight
                            className={`w-3 h-3 transition-transform text-muted-foreground/70 ${isOpen ? 'rotate-90' : ''}`}
                        />
                    )}
                    {node.type === 'folder' ? (
                        <Folder className="w-4 h-4 text-primary/60" />
                    ) : (
                        <FileText className="w-4 h-4 text-muted-foreground/80" />
                    )}
                    <span className="truncate">{node.title}</span>
                </span>
            </Button>
            {hasChildren && isOpen && (
                <div>
                    {node.children!.map(child => (
                        <DocTreeItem key={child.id} node={child} onSelect={onSelect} selectedId={selectedId} level={level + 1} />
                    ))}
                </div>
            )}
        </div>
    )
}
