import * as React from "react"
import { Activity, Server, Loader2, RefreshCw } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { API_BASE } from "@/lib/api"

interface HealthData {
  status: string
  server: string
  version: string
  uptime_seconds: number
  tool_count: number
  providers: Record<string, any>
}

export function Admin() {
  const [health, setHealth] = React.useState<HealthData | null>(null)
  const [loading, setLoading] = React.useState(true)
  const [tools, setTools] = React.useState<number>(0)

  const fetchHealth = React.useCallback(async () => {
    setLoading(true)
    try {
      const [h, t] = await Promise.all([
        fetch(API_BASE + "/api/health").then(r => r.json()).catch(() => null),
        fetch(API_BASE + "/api/tools").then(r => r.json()).then(d => d.tools?.length ?? 0).catch(() => 0),
      ])
      if (h) setHealth(h)
      setTools(t)
    } catch {}
    setLoading(false)
  }, [])

  React.useEffect(() => { fetchHealth() }, [fetchHealth])

  if (loading && !health) {
    return <div className="flex-1 flex items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>
  }

  const uptime = health?.uptime_seconds ? `${Math.floor(health.uptime_seconds / 60)}m ${health.uptime_seconds % 60}s` : "N/A"

    return (
        <div data-testid="admin-page" className="flex-1 flex flex-col min-h-0 container max-w-5xl mx-auto py-8 px-6 space-y-6 overflow-y-auto">
      <div className="flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Activity className="w-8 h-8 text-primary" />
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Admin</h1>
            <p className="text-muted-foreground">Server health, diagnostics, and system KPIs.</p>
          </div>
        </div>
        <Button variant="outline" size="sm" onClick={fetchHealth} className="gap-2">
          <RefreshCw className="w-4 h-4" /> Refresh
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 shrink-0">
        <Card data-testid="kpi-server">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">Server</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold">{health?.server || "N/A"}</div><p className="text-sm text-muted-foreground">v{health?.version || "?"}</p></CardContent>
        </Card>
        <Card data-testid="kpi-status">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">Status</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold text-emerald-500">{health?.status || "?"}</div><p className="text-sm text-muted-foreground">Uptime: {uptime}</p></CardContent>
        </Card>
        <Card data-testid="kpi-tools">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">Tools</CardTitle></CardHeader>
          <CardContent><div className="text-2xl font-bold">{tools}</div><p className="text-sm text-muted-foreground">Registered MCP tools</p></CardContent>
        </Card>
        <Card data-testid="kpi-providers">
          <CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-muted-foreground">Vector DB</CardTitle></CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{health?.providers?.vector_db?.chunks || 0}</div>
            <p className="text-sm text-muted-foreground">Chunks · {health?.providers?.vector_db?.sources || 0} sources</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg flex items-center gap-2"><Server className="w-5 h-5 text-primary" /> Providers</CardTitle>
        </CardHeader>
        <CardContent>
          {health?.providers ? (
            <div className="space-y-3">
              {Object.entries(health.providers).map(([name, info]: [string, any]) => (
                <div key={name} className="flex items-center justify-between border-b pb-2 last:border-0">
                  <span className="text-sm font-medium capitalize">{name.replace("_", " ")}</span>
                  <span className={`text-sm font-mono ${info?.status === "ok" ? "text-emerald-500" : "text-amber-500"}`}>
                    {info?.status || "unknown"}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No provider data available.</p>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
