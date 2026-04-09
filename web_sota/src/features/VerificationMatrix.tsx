import * as React from "react"
import { CheckCircle2, XCircle, AlertCircle, Info, Loader2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

type Column = { id: string; label: string }
type Client = { name: string; status: string; features: Record<string, string> }
type MatrixData = { title: string; subtitle: string; columns: Column[]; clients: Client[]; error?: string }

const StatusIcon = ({ status }: { status: string }) => {
    switch (status) {
        case "pass": return <CheckCircle2 className="w-4 h-4 text-green-500" />
        case "fail": return <XCircle className="w-4 h-4 text-destructive" />
        case "partial": return <AlertCircle className="w-4 h-4 text-yellow-500" />
        default: return <Info className="w-4 h-4 text-muted-foreground" />
    }
}

export function VerificationMatrix() {
    const [data, setData] = React.useState<MatrixData | null>(null)
    const [loading, setLoading] = React.useState(true)
    const [error, setError] = React.useState<string | null>(null)

    React.useEffect(() => {
        let cancelled = false
        setLoading(true)
        setError(null)
        fetch("/api/verification_matrix")
            .then((res) => {
                if (!res.ok) throw new Error(res.status === 404 ? "Matrix data not found" : `HTTP ${res.status}`)
                return res.json()
            })
            .then((d: MatrixData) => {
                if (!cancelled) setData(d)
            })
            .catch((e) => {
                if (!cancelled) setError(e.message)
            })
            .finally(() => {
                if (!cancelled) setLoading(false)
            })
        return () => { cancelled = true }
    }, [])

    if (loading) {
        return (
            <div className="container max-w-6xl mx-auto py-12 px-6 flex items-center justify-center gap-2">
                <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                <span className="text-muted-foreground">Loading verification matrix…</span>
            </div>
        )
    }
    if (error || !data) {
        return (
            <div className="container max-w-6xl mx-auto py-12 px-6">
                <p className="text-destructive">Failed to load matrix: {error ?? "Unknown error"}</p>
            </div>
        )
    }

    const { title, subtitle, columns, clients } = data
    if (!Array.isArray(clients) || clients.length === 0) {
        return (
            <div className="container max-w-6xl mx-auto py-12 px-6">
                <h1 className="text-4xl font-bold tracking-tight">Multi-Client Verification Matrix</h1>
                <p className="mt-4 text-muted-foreground">No client data configured. Add entries to operations/verification_matrix.json.</p>
            </div>
        )
    }

    return (
        <div className="container max-w-6xl mx-auto py-12 px-6">
            <div className="mb-10 space-y-4">
                <h1 className="text-4xl font-bold tracking-tight">Multi-Client Verification Matrix</h1>
                <p className="text-lg text-muted-foreground">Compatibility status of MCP features across agentic IDEs and clients. Data from operations/verification_matrix.json.</p>
            </div>

            <Card className="border-primary/20 shadow-xl overflow-hidden backdrop-blur-sm bg-card/50">
                <CardHeader className="bg-primary/5 border-b border-primary/10">
                    <CardTitle>{title || "Compatibility Matrix"}</CardTitle>
                    {subtitle && <CardDescription>{subtitle}</CardDescription>}
                </CardHeader>
                <CardContent className="p-0">
                    <Table>
                        <TableHeader>
                            <TableRow className="hover:bg-transparent bg-muted/30">
                                <TableHead className="w-[180px] font-bold">Client / IDE</TableHead>
                                <TableHead className="font-bold">Status</TableHead>
                                {Array.isArray(columns) && columns.map((col) => (
                                    <TableHead key={col.id} className="text-center font-bold">{col.label}</TableHead>
                                ))}
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {clients.map((client) => (
                                <TableRow key={client.name} className="hover:bg-primary/5 transition-colors">
                                    <TableCell className="font-medium text-lg">{client.name}</TableCell>
                                    <TableCell>
                                        <Badge variant={client.status === "VERIFIED" ? "default" : "outline"} className="font-mono text-[10px]">
                                            {client.status}
                                        </Badge>
                                    </TableCell>
                                    {Array.isArray(columns) && columns.map((col) => (
                                        <TableCell key={col.id} className="text-center">
                                            <div className="flex justify-center">
                                                <StatusIcon status={client.features?.[col.id] ?? ""} />
                                            </div>
                                        </TableCell>
                                    ))}
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl border bg-card/30 flex items-start gap-3">
                    <CheckCircle2 className="w-5 h-5 text-green-500 mt-1" />
                    <div>
                        <h4 className="font-bold text-sm">Pass</h4>
                        <p className="text-xs text-muted-foreground">100% compliant with operational standards.</p>
                    </div>
                </div>
                <div className="p-4 rounded-xl border bg-card/30 flex items-start gap-3">
                    <AlertCircle className="w-5 h-5 text-yellow-500 mt-1" />
                    <div>
                        <h4 className="font-bold text-sm">Partial</h4>
                        <p className="text-xs text-muted-foreground">Limited support or known edge cases.</p>
                    </div>
                </div>
                <div className="p-4 rounded-xl border bg-card/30 flex items-start gap-3">
                    <XCircle className="w-5 h-5 text-destructive mt-1" />
                    <div>
                        <h4 className="font-bold text-sm">Fail</h4>
                        <p className="text-xs text-muted-foreground">Feature not implemented or broken.</p>
                    </div>
                </div>
            </div>
        </div>
    )
}
