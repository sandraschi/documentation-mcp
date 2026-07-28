import * as React from "react"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
    CircleHelp,
    Keyboard,
    Zap,
    BookOpen,
    Terminal,
    ChevronRight,
    ArrowLeft
} from "lucide-react"

type HelpCategory = 'architecture' | 'rag' | 'shortcuts' | null

export function HelpDialog() {
    const [category, setCategory] = React.useState<HelpCategory>(null)

    return (
        <Dialog onOpenChange={(open) => !open && setCategory(null)}>
            <DialogTrigger asChild>
                <Button variant="ghost" size="icon" title="Documentation & Help">
                    <CircleHelp className="h-[1.2rem] w-[1.2rem]" />
                    <span className="sr-only">Help</span>
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px] h-[600px] flex flex-col overflow-hidden">
                <DialogHeader className="border-b pb-4 shrink-0">
                    <div className="flex items-center gap-2">
                        {category && (
                            <Button variant="ghost" size="icon" className="h-8 w-8 -ml-2" onClick={() => setCategory(null)}>
                                <ArrowLeft className="h-4 w-4" />
                            </Button>
                        )}
                        <DialogTitle className="flex items-center gap-2 text-2xl font-bold">
                            <CircleHelp className="h-6 w-6 text-primary" />
                            {category ? category.charAt(0).toUpperCase() + category.slice(1) : "System Help"}
                        </DialogTitle>
                    </div>
                    <DialogDescription className="font-mono text-[10px] tracking-widest uppercase opacity-70">
                        Operational Documentation Management • Vienna
                    </DialogDescription>
                </DialogHeader>

                <div className="flex-1 overflow-hidden">
                    {!category ? (
                        <div className="grid grid-cols-1 gap-3 p-4">
                            <MenuButton
                                icon={Zap}
                                title="Webapp Architecture"
                                description="Modern React SPA, Vite, Shadcn UI"
                                onClick={() => setCategory('architecture')}
                            />
                            <MenuButton
                                icon={Terminal}
                                title="System Core & RAG"
                                description="FastMCP, LanceDB, Semantic Search"
                                onClick={() => setCategory('rag')}
                            />
                            <MenuButton
                                icon={Keyboard}
                                title="Global Shortcuts"
                                description="Command Palette, Chat, Navigation"
                                onClick={() => setCategory('shortcuts')}
                            />
                        </div>
                    ) : (
                        <ScrollArea className="h-full p-6">
                            {category === 'architecture' && <ArchitectureHelp />}
                            {category === 'rag' && <RagHelp />}
                            {category === 'shortcuts' && <ShortcutsHelp />}
                        </ScrollArea>
                    )}
                </div>

                <div className="border-t p-4 flex justify-between items-center bg-muted/30 shrink-0">
                    <div className="flex items-center gap-2 opacity-60">
                        <BookOpen className="h-4 w-4" />
                        <span className="text-[10px] font-medium">© 2026 Materialist-Reductionist Systems</span>
                    </div>
                    <Button variant="outline" size="sm" className="font-bold text-[10px] uppercase tracking-widest px-6" onClick={() => window.open('https://github.com/sandraschi/mcp-central-docs', '_blank')}>
                        Visit GitHub
                    </Button>
                </div>
            </DialogContent>
        </Dialog>
    )
}

function MenuButton({ icon: Icon, title, description, onClick }: { icon: any, title: string, description: string, onClick: () => void }) {
    return (
        <Button
            variant="outline"
            className="h-20 justify-between items-center text-left hover:bg-accent/50 group"
            onClick={onClick}
        >
            <div className="flex items-center gap-4">
                <div className="p-2 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
                    <Icon className="h-6 w-6 text-primary" />
                </div>
                <div>
                    <div className="font-bold text-sm tracking-tight">{title}</div>
                    <div className="text-[11px] text-muted-foreground">{description}</div>
                </div>
            </div>
            <ChevronRight className="h-5 w-5 text-muted-foreground/50 group-hover:translate-x-1 transition-transform" />
        </Button>
    )
}

function ArchitectureHelp() {
    return (
        <div className="space-y-6">
            <h4 className="text-sm font-bold uppercase tracking-widest text-primary border-b pb-2">Frontend Stack</h4>
            <div className="p-4 bg-muted/30 rounded-lg border border-border/50 space-y-3">
                <p className="text-sm leading-relaxed">
                    Modern React Single Page Application (SPA) optimized for industrial-grade documentation management.
                </p>
                <ul className="grid grid-cols-2 gap-2 text-[11px] font-mono opacity-80 list-none">
                    <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 bg-primary rounded-full" /> Vite HMR Engine</li>
                    <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 bg-primary rounded-full" /> Shadcn/ui & Tailwind</li>
                    <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 bg-primary rounded-full" /> Lucide Iconography</li>
                    <li className="flex items-center gap-2"><div className="h-1.5 w-1.5 bg-primary rounded-full" /> Framer Motion</li>
                </ul>
            </div>
            <div className="p-4 bg-muted/30 rounded-lg border border-border/50">
                <h5 className="text-sm font-bold mb-2">Design Philosophy</h5>
                <p className="text-sm text-muted-foreground leading-relaxed">
                    Strict adherence to the Materialist/Reductionist aesthetic: data-driven, neutral tones, high contrast, and zero-friction navigation. All UI components are verified for industrial-grade stability.
                </p>
            </div>
        </div>
    )
}

function RagHelp() {
    return (
        <div className="space-y-4">
            <div className="p-4 border rounded-lg bg-card">
                <h5 className="text-xs font-bold uppercase mb-2 flex items-center gap-2">
                    <div className="h-2 w-2 bg-blue-500 rounded-sm" /> FastMCP Server
                </h5>
                <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Python-based Model Context Protocol (MCP) implementation utilizing the FastMCP 2.14.4+ framework. Supports advanced tool sampling and agentic orchestration.
                </p>
            </div>

            <div className="p-4 border rounded-lg bg-card">
                <h5 className="text-xs font-bold uppercase mb-2 flex items-center gap-2">
                    <div className="h-2 w-2 bg-green-500 rounded-sm" /> RAG Facility
                </h5>
                <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Powered by LanceDB. Automated ingestion pipeline transforms documentation into a high-density neural index (~59,000 document chunks).
                </p>
            </div>

            <div className="p-4 border rounded-lg bg-card">
                <h5 className="text-xs font-bold uppercase mb-2 flex items-center gap-2">
                    <div className="h-2 w-2 bg-purple-500 rounded-sm" /> Semantic Search
                </h5>
                <p className="text-[11px] text-muted-foreground leading-relaxed">
                    Leverages dense vector embeddings and Cosine Similarity for high-precision context retrieval, enabling nuanced natural language queries across disparate datasets.
                </p>
            </div>
        </div>
    )
}

function ShortcutsHelp() {
    return (
        <div className="space-y-4">
            <h4 className="text-sm font-bold uppercase tracking-widest text-primary border-b pb-2">Keyboard Shortcuts</h4>
            <div className="space-y-2">
                <div className="flex justify-between items-center bg-muted/20 p-2.5 rounded border border-border/20">
                    <span className="text-sm font-medium">Command Palette</span>
                    <div className="flex gap-1">
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">⌘</kbd>
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">K</kbd>
                    </div>
                </div>
                <div className="flex justify-between items-center bg-muted/20 p-2.5 rounded border border-border/20">
                    <span className="text-sm font-medium">Chat Floater</span>
                    <div className="flex gap-1">
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">⌘</kbd>
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">J</kbd>
                    </div>
                </div>
                <div className="flex justify-between items-center bg-muted/20 p-2.5 rounded border border-border/20">
                    <span className="text-sm font-medium">Toggle Sidebar</span>
                    <div className="flex gap-1">
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">⌘</kbd>
                        <kbd className="h-5 rounded border bg-muted px-1.5 font-mono text-[10px] font-bold">B</kbd>
                    </div>
                </div>
            </div>
        </div>
    )
}
