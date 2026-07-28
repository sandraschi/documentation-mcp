import * as React from "react"
import { BookMarked, Loader2, Copy, Download, ChevronDown, ChevronUp, Info, ExternalLink, Store } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { API_BASE } from "@/lib/api"

type Skill = {
    id: string
    name: string
    description: string
    content: string
    uri: string
}

type Marketplace = {
    name: string
    description: string
    url: string
    install_hint: string
    install_command: string | null
}

export function Skills() {
    const [skills, setSkills] = React.useState<Skill[]>([])
    const [marketplaces, setMarketplaces] = React.useState<Marketplace[]>([])
    const [loading, setLoading] = React.useState(true)
    const [expandedId, setExpandedId] = React.useState<string | null>(null)
    const [copiedId, setCopiedId] = React.useState<string | null>(null)
    const [copiedMarketplace, setCopiedMarketplace] = React.useState<string | null>(null)

    React.useEffect(() => {
        Promise.all([
            fetch(API_BASE + "/api/skills").then((res) => res.json()).then((d) => setSkills(Array.isArray(d.skills) ? d.skills : [])),
            fetch(API_BASE + "/api/skill_marketplaces").then((res) => res.json()).then((d) => setMarketplaces(Array.isArray(d.marketplaces) ? d.marketplaces : [])),
        ]).catch(() => {}).finally(() => setLoading(false))
    }, [])

    const copyToClipboard = (skill: Skill) => {
        const text = skill.content.trimStart()
        navigator.clipboard.writeText(text).then(() => {
            setCopiedId(skill.id)
            setTimeout(() => setCopiedId(null), 2000)
        })
    }

    const downloadFile = (skill: Skill) => {
        const blob = new Blob([skill.content], { type: "text/markdown" })
        const url = URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `${skill.id}-SKILL.md`
        a.click()
        URL.revokeObjectURL(url)
    }

    if (loading) {
        return (
            <div className="container max-w-4xl mx-auto py-12 flex items-center justify-center gap-2">
                <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                <span className="text-muted-foreground">Loading skills…</span>
            </div>
        )
    }

    return (
        <div data-testid="skills-page" className="container max-w-4xl mx-auto py-12 px-6">
            <div className="mb-10 space-y-4">
                <h1 className="text-4xl font-bold tracking-tight flex items-center gap-3">
                    <BookMarked className="w-10 h-10 text-primary" />
                    Skills
                </h1>
                <p className="text-lg text-muted-foreground">
                    Skills exposed by this server (FastMCP 3.1). These are bundled with the Docs MCP server and
                    exposed as <code className="text-sm bg-muted px-1 rounded">skill://</code> resources. View, copy, or
                    download to install in Claude or Cursor.
                </p>
                <div className="rounded-lg border bg-muted/30 p-4 flex gap-3">
                    <Info className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                    <div className="text-sm text-muted-foreground">
                        <strong>Not a central repository.</strong> This page lists only the skills this server provides.
                        The skill provider runs on this server—not by Anthropic. For a global catalog, you’d use a
                        separate marketplace or registry.
                    </div>
                </div>
            </div>

            {skills.length === 0 ? (
                <Card>
                    <CardContent className="py-12 text-center text-muted-foreground">
                        No skills registered. Add folders under <code>src/docs_mcp/skills/</code> with a{" "}
                        <code>SKILL.md</code> in each.
                    </CardContent>
                </Card>
            ) : (
                <div data-testid="skills-list" className="space-y-4">
                    {skills.map((skill) => (
                        <Card key={skill.id}>
                            <CardHeader className="pb-2">
                                <CardTitle className="text-xl">{skill.name}</CardTitle>
                                {skill.description && (
                                    <CardDescription>{skill.description}</CardDescription>
                                )}
                                <p className="text-xs font-mono text-muted-foreground">{skill.uri}</p>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex flex-wrap gap-2">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => copyToClipboard(skill)}
                                        className="gap-1"
                                    >
                                        <Copy className="w-4 h-4" />
                                        {copiedId === skill.id ? "Copied" : "Copy content"}
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => downloadFile(skill)}
                                        className="gap-1"
                                    >
                                        <Download className="w-4 h-4" />
                                        Download SKILL.md
                                    </Button>
                                </div>

                                <Button
                                    variant="ghost"
                                    size="sm"
                                    className="gap-1 -ml-2"
                                    onClick={() => setExpandedId(expandedId === skill.id ? null : skill.id)}
                                >
                                    {expandedId === skill.id ? (
                                        <ChevronUp className="w-4 h-4" />
                                    ) : (
                                        <ChevronDown className="w-4 h-4" />
                                    )}
                                    {expandedId === skill.id ? "Hide content" : "View content"}
                                </Button>
                                {expandedId === skill.id && (
                                    <pre className="p-4 rounded-lg bg-muted text-sm overflow-auto max-h-96 whitespace-pre-wrap font-sans border">
                                        {skill.content}
                                    </pre>
                                )}

                                <details className="group">
                                    <summary className="cursor-pointer list-none flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground">
                                        <ChevronDown className="w-4 h-4 group-open:rotate-180 transition-transform" />
                                        Install instructions
                                    </summary>
                                    <div className="mt-2 space-y-3 text-sm border rounded-lg p-4 bg-muted/20">
                                        <div>
                                            <strong>Claude</strong>: Save the downloaded file (or paste content) to{" "}
                                            <code className="bg-muted px-1 rounded">
                                                ~/.claude/skills/{skill.id}/SKILL.md
                                            </code>
                                        </div>
                                        <div>
                                            <strong>Cursor</strong>: Save to your Cursor skills directory (e.g.{" "}
                                            <code className="bg-muted px-1 rounded">~/.cursor/skills/</code> or project{" "}
                                            <code className="bg-muted px-1 rounded">.cursor/skills/</code>) as{" "}
                                            <code className="bg-muted px-1 rounded">{skill.id}/SKILL.md</code>.
                                        </div>
                                        <div className="text-muted-foreground">
                                            MCP clients that support resources can also read{" "}
                                            <code className="bg-muted px-1 rounded">{skill.uri}</code> from this server
                                            directly—no file copy needed.
                                        </div>
                                    </div>
                                </details>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

            {marketplaces.length > 0 && (
                <div className="mt-16 space-y-6">
                    <h2 className="text-2xl font-bold tracking-tight flex items-center gap-2">
                        <Store className="w-7 h-7 text-primary" />
                        Skill marketplaces
                    </h2>
                    <p className="text-muted-foreground">
                        Curated registries where you can browse and install skills. Visit to download or follow their install steps.
                    </p>
                    <div className="grid gap-4 md:grid-cols-2">
                        {marketplaces.map((m) => (
                            <Card key={m.name} className="flex flex-col">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-lg">{m.name}</CardTitle>
                                    <CardDescription className="line-clamp-2">{m.description}</CardDescription>
                                </CardHeader>
                                <CardContent className="mt-auto space-y-3">
                                    <div className="flex flex-wrap gap-2">
                                        <Button asChild variant="default" size="sm" className="gap-1">
                                            <a href={m.url} target="_blank" rel="noopener noreferrer">
                                                <ExternalLink className="w-4 h-4" />
                                                Visit &amp; install
                                            </a>
                                        </Button>
                                        {m.install_command && (
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                className="gap-1"
                                                onClick={() => {
                                                    navigator.clipboard.writeText(m.install_command!)
                                                    setCopiedMarketplace(m.name)
                                                    setTimeout(() => setCopiedMarketplace(null), 2000)
                                                }}
                                            >
                                                <Copy className="w-4 h-4" />
                                                {copiedMarketplace === m.name ? "Copied" : "Copy install command"}
                                            </Button>
                                        )}
                                    </div>
                                    {m.install_hint && (
                                        <p className="text-sm text-muted-foreground">{m.install_hint}</p>
                                    )}
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}
