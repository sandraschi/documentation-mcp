import { useNavigate } from "react-router-dom"
import { Code2, ExternalLink, BookOpen, SlidersHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function ApiDocs() {
  const navigate = useNavigate()

  return (
    <div data-testid="api-docs-page" className="flex-1 flex flex-col min-h-0 container max-w-6xl mx-auto py-8 px-6 space-y-6">
      <div className="flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Code2 className="w-8 h-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold tracking-tight">API Docs</h1>
            <p className="text-muted-foreground">REST API reference for the Documentation MCP backend.</p>
          </div>
        </div>
        <a href="http://127.0.0.1:11033/docs" target="_blank" rel="noopener noreferrer">
          <Button variant="outline" className="gap-2">
            <ExternalLink className="w-4 h-4" /> Open in browser
          </Button>
        </a>
      </div>

      <div className="grid md:grid-cols-3 gap-4 shrink-0">
        <Card className="cursor-pointer hover:border-primary/40 transition-colors" onClick={() => navigate("/search")}>
          <CardHeader className="pb-2"><CardTitle className="text-sm flex items-center gap-2"><BookOpen className="w-4 h-4 text-primary" /> Search</CardTitle></CardHeader>
          <CardContent className="text-xs text-muted-foreground"><code className="text-primary">GET /api/search?q=&limit=&offset=&source=&category=</code></CardContent>
        </Card>
        <Card className="cursor-pointer hover:border-primary/40 transition-colors" onClick={() => navigate("/documents")}>
          <CardHeader className="pb-2"><CardTitle className="text-sm flex items-center gap-2"><BookOpen className="w-4 h-4 text-primary" /> Content</CardTitle></CardHeader>
          <CardContent className="text-xs text-muted-foreground"><code className="text-primary">GET /api/tree</code> · <code className="text-primary">GET /api/content?path=</code></CardContent>
        </Card>
        <Card className="cursor-pointer hover:border-primary/40 transition-colors" onClick={() => navigate("/settings")}>
          <CardHeader className="pb-2"><CardTitle className="text-sm flex items-center gap-2"><SlidersHorizontal className="w-4 h-4 text-primary" /> Admin</CardTitle></CardHeader>
          <CardContent className="text-xs text-muted-foreground"><code className="text-primary">GET /api/status</code> · <code className="text-primary">GET /api/health</code> · <code className="text-primary">POST /api/reindex</code></CardContent>
        </Card>
      </div>

      <Card className="flex-1 min-h-0 flex flex-col">
        <CardHeader className="shrink-0 border-b">
          <CardTitle className="text-lg flex items-center gap-2">
            <Code2 className="w-5 h-5 text-primary" />
            Swagger UI
          </CardTitle>
        </CardHeader>
        <CardContent className="flex-1 min-h-0 p-0">
          <iframe
            src="/docs"
            className="w-full h-[600px] border-0 rounded-b-lg"
            title="Swagger UI"
            sandbox="allow-scripts allow-same-origin"
          />
        </CardContent>
      </Card>
    </div>
  )
}
