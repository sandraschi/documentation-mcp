import { useNavigate } from "react-router-dom"
import { CircleHelp, Github, ShieldCheck, Zap } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { viewToPathname } from "@/routes"

export function Help() {
    const navigate = useNavigate()
    return (
        <div className="container max-w-4xl mx-auto py-16 px-6 space-y-12 text-center text-primary-foreground/90">

            <div className="space-y-6">
                <div className="inline-flex items-center justify-center p-4 bg-primary/5 rounded-full mb-4">
                    <CircleHelp className="w-12 h-12 text-primary" />
                </div>
                <h1 className="text-5xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-primary to-purple-600">
                    Docs MCP Help
                </h1>
                <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto">
                    The integrated hub for knowledge retrieval, standards enforcement, and agentic memory management.
                </p>
                <div className="flex justify-center gap-4 pt-4">
                    <Button variant="default" size="lg" className="rounded-full px-8" onClick={() => navigate(viewToPathname("documents"))}>Documentation</Button>
                    <Button variant="outline" size="lg" className="rounded-full px-8 gap-2">
                        <Github className="w-4 h-4" /> GitHub
                    </Button>
                </div>
            </div>

            <div className="grid md:grid-cols-3 gap-8 text-left mt-20">
                <Card className="bg-card/50 border-0 shadow-lg">
                    <CardContent className="pt-6 space-y-2">
                        <ShieldCheck className="w-8 h-8 text-green-500 mb-2" />
                        <h3 className="font-bold text-lg text-foreground">Industrial Grade</h3>
                        <p className="text-sm text-muted-foreground">Rigorous adherence to enterprise-grade web application standards and security protocols.</p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 border-0 shadow-lg">
                    <CardContent className="pt-6 space-y-2">
                        <Zap className="w-8 h-8 text-yellow-500 mb-2" />
                        <h3 className="font-bold text-lg text-foreground">Super Low Latency</h3>
                        <p className="text-sm text-muted-foreground">Powered by LanceDB and FastMCP for near-instant vector retrieval.</p>
                    </CardContent>
                </Card>
                <Card className="bg-card/50 border-0 shadow-lg">
                    <CardContent className="pt-6 space-y-2">
                        <CircleHelp className="w-8 h-8 text-blue-500 mb-2" />
                        <h3 className="font-bold text-lg text-foreground">Agent Ready</h3>
                        <p className="text-sm text-muted-foreground">Designed specifically for LLM function calling and automated context injection.</p>
                    </CardContent>
                </Card>
            </div>

            <div className="pt-20 text-sm text-muted-foreground">
                <p>Version 2.0.0 (January 2026 Build)</p>
                <p className="mt-2 text-primary-foreground/50">Vienna, Austria</p>
            </div>
        </div>
    )
}
