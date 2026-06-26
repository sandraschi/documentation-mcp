import { useNavigate } from "react-router-dom"
import * as React from "react"
import { BookOpen, MessageSquare, Search, Server, Terminal, FileText, ExternalLink } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { viewToPathname, type ViewState } from "@/routes"

const helpItems: { title: string; desc: string; action: string; path: ViewState; icon: React.ComponentType<{ className?: string }> }[] = [
  {
    title: "Search Documentation",
    desc: "Semantic search across all indexed fleet documentation and standards.",
    action: "Search",
    path: "semantic",
    icon: Search,
  },
  {
    title: "Browse Documents",
    desc: "Navigate the documentation tree and read full file contents in the browser.",
    action: "Browse",
    path: "documents",
    icon: BookOpen,
  },
  {
    title: "AI Assistant",
    desc: "Ask natural-language questions. Uses MCP sampling or local LLM fallback.",
    action: "Chat",
    path: "chat",
    icon: MessageSquare,
  },
  {
    title: "Tools Hub",
    desc: "Explore registered MCP tools, their parameters, and portmanteau operations.",
    action: "Explore",
    path: "tools",
    icon: Terminal,
  },
  {
    title: "Fleet Dashboard",
    desc: "Discover and launch other MCP fleet webapps across the ecosystem.",
    action: "Open",
    path: "apps",
    icon: Server,
  },
]

const faq = [
  { q: "How do I add my own docs?", a: "Set DOCS_EXTRA_PATHS env var with comma-separated paths, then reindex via the Settings page or the reindex_docs MCP tool." },
  { q: "No results in search?", a: "Run a reindex first (reindex_docs tool or Settings page). The index is empty until the first scan." },
  { q: "Where is the server running?", a: "Backend: port 11033. Frontend: port 11032. Both in the fleet 10700-11500 range." },
  { q: "How do I use the MCP server in Cursor/Claude?", a: "Add mcpServers entry pointing to the backend URL (HTTP mode) or run `uv run docs-mcp` (stdio mode)." },
  { q: "Can I see the REST API?", a: "The backend exposes /api/search, /api/tree, /api/content, /api/status, etc. No built-in Swagger — hit the endpoints directly." },
]

export function Help() {
  const navigate = useNavigate()
  return (
    <div className="flex-1 flex flex-col min-h-0 container max-w-5xl mx-auto py-8 px-6 space-y-8 overflow-y-auto">
      <div className="space-y-2 shrink-0">
        <h1 className="text-3xl font-bold tracking-tight">Help & Guide</h1>
        <p className="text-muted-foreground">Quick reference for using the Documentation MCP webapp and server.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 shrink-0">
        {helpItems.map((item) => (
          <Card key={item.path} className="cursor-pointer hover:border-primary/40 transition-colors" onClick={() => navigate(viewToPathname(item.path))}>
            <CardHeader className="pb-3">
              <item.icon className="w-6 h-6 text-primary mb-1" />
              <CardTitle className="text-sm">{item.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-xs text-muted-foreground space-y-3">
              <p>{item.desc}</p>
              <Button variant="outline" size="sm" className="w-full text-xs gap-1">
                {item.action} <ExternalLink className="w-3 h-3" />
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="shrink-0">
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2">
            <FileText className="w-5 h-5 text-primary" />
            Frequently Asked Questions
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {faq.map((item, i) => (
            <details key={i} className="group">
              <summary className="cursor-pointer text-sm font-medium text-foreground hover:text-primary transition-colors list-none flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center text-xs text-primary shrink-0">?</span>
                {item.q}
              </summary>
              <p className="mt-2 ml-7 text-sm text-muted-foreground">{item.a}</p>
            </details>
          ))}
        </CardContent>
      </Card>

      <Card className="shrink-0">
        <CardHeader>
          <CardTitle className="text-lg">Keyboard Shortcuts</CardTitle>
        </CardHeader>
        <CardContent className="text-sm space-y-2">
          <div className="flex justify-between border-b pb-2"><kbd className="px-2 py-0.5 rounded bg-muted text-xs font-mono">Ctrl+K</kbd><span className="text-muted-foreground">Open search</span></div>
          <div className="flex justify-between border-b pb-2"><kbd className="px-2 py-0.5 rounded bg-muted text-xs font-mono">Ctrl+Scroll</kbd><span className="text-muted-foreground">Zoom in/out (0.8x - 3x)</span></div>
        </CardContent>
      </Card>
    </div>
  )
}
