import * as React from "react"
import { ExternalLink, HardDrive, Cpu, Database, Brain, Loader2, Search, Filter, Layers, MessageSquare, BookOpen, Star } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { useNavigate } from "react-router-dom"
import { API_BASE } from "@/lib/api"

export interface FleetProject {
    id: string
    name: string
    description: string
    type: string
    localPath: string
    docsPath: string
    status: string
}

export function ProjectPortfolio() {

    const [projects, setProjects] = React.useState<FleetProject[]>([])
    const [loading, setLoading] = React.useState(true)
    const [search, setSearch] = React.useState("")
    const [typeFilter, setTypeFilter] = React.useState<string>("all")
    const navigate = useNavigate()

    React.useEffect(() => {
        fetch(API_BASE + "/api/fleet-projects")
            .then((res) => res.json())
            .then((data) => {
                setProjects(data)
                setLoading(false)
            })
            .catch((err) => {
                console.error("Failed to fetch fleet projects:", err)
                setLoading(false)
            })
    }, [])

    const filteredProjects = projects.filter((p) => {
        const matchesSearch = p.name.toLowerCase().includes(search.toLowerCase()) || 
                             p.description.toLowerCase().includes(search.toLowerCase())
        const matchesType = typeFilter === "all" || p.type === typeFilter
        return matchesSearch && matchesType
    })

    const projectTypes = Array.from(new Set(projects.map((p) => p.type)))

    const getIcon = (type: string) => {
        const t = type.toLowerCase()
        if (t.includes("mcp server")) return <Cpu className="w-5 h-5 text-primary" />
        if (t.includes("app")) return <Layers className="w-5 h-5 text-indigo-400" />
        if (t.includes("infrastructure")) return <Database className="w-5 h-5 text-emerald-400" />
        if (t.includes("skill")) return <Brain className="w-5 h-5 text-amber-400" />
        if (t.includes("experiment")) return <Star className="w-5 h-5 text-rose-400" />
        return <HardDrive className="w-5 h-5 text-primary" />
    }

    const getStatusColor = (status: string) => {
        const s = status.toLowerCase()
        if (s.includes("gold")) return "border-amber-500/50 text-amber-500 bg-amber-500/10"
        if (s.includes("active")) return "border-emerald-500/50 text-emerald-500 bg-emerald-500/10"
        if (s.includes("production")) return "border-blue-500/50 text-blue-500 bg-blue-500/10"
        return "border-muted-foreground/30 text-muted-foreground bg-muted/10"
    }

    const handleResearch = (project: FleetProject) => {
        const query = `Tell me everything about the ${project.name} repository and its capabilities.`
        navigate(`/chat?q=${encodeURIComponent(query)}`)
    }

    const handleOpenDocs = (project: FleetProject) => {
        // Ideally we would navigate to the document view and select this path
        // For now, we can navigate to /documents and maybe pass the path
        navigate(`/documents?path=${encodeURIComponent(project.docsPath)}`)
    }

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
            </div>
        )
    }

    return (
        <div className="flex-1 flex flex-col min-h-0 container max-w-7xl mx-auto py-8 px-6">
            <div className="mb-10 space-y-4 shrink-0">
                <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                    <div className="space-y-1">
                        <div className="flex items-center gap-2 mb-1">
                            <Badge variant="outline" className="text-[10px] font-bold uppercase tracking-widest text-primary border-primary/20">
                                Fleet Portfolio v1.0
                            </Badge>
                        </div>
                        <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-foreground via-foreground to-muted-foreground bg-clip-text text-transparent">
                            Project Portfolio
                        </h1>

                        <p className="text-muted-foreground text-lg max-w-2xl">
                             Interactive index of the 100+ active repositories in the MCP Fleet ecosystem.
                            High-fidelity orchestration for industrial agentic workflows.
                        </p>
                    </div>
                    <div className="flex items-center gap-4 bg-card/30 backdrop-blur-xl p-4 rounded-2xl border border-white/5 shadow-2xl">
                        <div className="text-center px-4 border-r border-white/10">
                            <div className="text-2xl font-bold">{projects.length}</div>
                            <div className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Projects</div>
                        </div>
                        <div className="text-center px-4 border-r border-white/10">
                            <div className="text-2xl font-bold text-amber-500">{projects.filter(p => p.status.includes("Gold")).length}</div>
                            <div className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Gold Stnd</div>
                        </div>
                        <div className="text-center px-4">
                            <div className="text-2xl font-bold text-primary">{projects.filter(p => p.type.includes("MCP")).length}</div>
                            <div className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Servers</div>
                        </div>
                    </div>
                </div>

                <div className="flex flex-col md:flex-row gap-4 pt-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <Input 
                            placeholder="Search project name, description, or capabilities..." 
                            className="pl-10 h-12 bg-card/30 border-white/10 backdrop-blur-md text-lg shadow-inner"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-2 bg-card/30 border-white/10 backdrop-blur-md px-4 rounded-lg shadow-inner h-12">
                        <Filter className="w-4 h-4 text-muted-foreground" />
                        <select 
                            className="bg-transparent border-none text-sm font-medium focus:ring-0 cursor-pointer outline-none min-w-[120px]"
                            value={typeFilter}
                            onChange={(e) => setTypeFilter(e.target.value)}
                        >
                            <option value="all">All Types</option>
                            {projectTypes.map((t) => (
                                <option key={t} value={t}>{t}</option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto min-h-0 pr-2 -mr-2 scrollbar-thin scrollbar-thumb-white/10">
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 pb-12">
                    {filteredProjects.map((project) => (
                        <Card 
                            key={project.id}
                            className="group relative overflow-hidden flex flex-col bg-card/20 backdrop-blur-xl border-white/5 hover:border-primary/40 transition-all duration-500 hover:shadow-2xl hover:shadow-primary/5 shadow-xl"
                        >
                            <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-primary/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                            <CardHeader className="pb-4">
                                <div className="flex justify-between items-start">
                                    <div className={cn(
                                        "p-3 rounded-xl transition-all duration-500 bg-white/5 group-hover:bg-primary/10 group-hover:scale-110",
                                        project.status.includes("Gold") ? "border border-amber-500/30" : ""
                                    )}>
                                        {getIcon(project.type)}
                                    </div>
                                    <Badge variant="outline" className={cn("text-[8px] font-bold uppercase tracking-tighter transition-all duration-300", getStatusColor(project.status))}>
                                        {project.status}
                                    </Badge>
                                </div>
                                <CardTitle className="mt-5 text-xl tracking-tight font-bold group-hover:text-primary transition-colors duration-300">
                                    {project.name}
                                </CardTitle>
                                <CardDescription className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground/70">
                                    {project.type}
                                </CardDescription>
                            </CardHeader>
                            <CardContent className="flex-1">
                                <p className="text-sm text-muted-foreground leading-relaxed line-clamp-4 group-hover:line-clamp-none transition-all duration-500">
                                    {project.description}
                                </p>
                            </CardContent>
                            <CardFooter className="pt-4 border-t border-white/5 flex gap-2">
                                <Button 
                                    size="sm"
                                    variant="ghost" 
                                    className="flex-1 gap-2 hover:bg-primary/10 hover:text-primary transition-all rounded-lg group/btn"
                                    onClick={() => handleResearch(project)}
                                >
                                    <MessageSquare className="w-3.5 h-3.5 group-hover/btn:scale-110 transition-transform" />
                                    Research
                                </Button>
                                <Button 
                                    size="sm"
                                    variant="ghost"
                                    className="flex-1 gap-2 hover:bg-indigo-500/10 hover:text-indigo-400 transition-all rounded-lg group/btn"
                                    onClick={() => handleOpenDocs(project)}
                                >
                                    <BookOpen className="w-3.5 h-3.5 group-hover/btn:scale-110 transition-transform" />
                                    Docs
                                </Button>
                                <Button 
                                    size="icon" 
                                    variant="ghost"
                                    className="hover:bg-emerald-500/10 hover:text-emerald-400 transition-all rounded-lg"
                                    asChild
                                >
                                    <a href={project.localPath} target="_blank" rel="noopener noreferrer">
                                        <ExternalLink className="w-4 h-4" />
                                    </a>
                                </Button>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    )
}

function cn(...classes: string[]) {
    return classes.filter(Boolean).join(" ")
}
