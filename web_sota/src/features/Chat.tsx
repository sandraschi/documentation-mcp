import * as React from "react"
import { Send, Loader2, User, Bot, Trash2, Download, ChevronDown, ChevronUp } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AutoResizeTextarea } from "@/components/ui/auto-resize-textarea"

interface Message {
    role: 'user' | 'assistant'
    content: string
    sources?: string[]
}

const PERSONAS = [
    { id: 'default', label: 'Default', hint: 'General documentation assistant' },
    { id: 'technical', label: 'Technical', hint: 'Precise, code-focused answers' },
    { id: 'concise', label: 'Concise', hint: 'Short, to-the-point' },
    { id: 'educator', label: 'Educator', hint: 'Step-by-step explanations' },
]

export function ChatView() {
    const [messages, setMessages] = React.useState<Message[]>([
        { role: 'assistant', content: "Hello! I'm your Docs MCP assistant. Ask me anything about the documentation." }
    ])
    const [input, setInput] = React.useState('')
    const [loading, setLoading] = React.useState(false)
    const [persona, setPersona] = React.useState('default')
    const [systemPromptOverride, setSystemPromptOverride] = React.useState('')
    const [showPromptRefine, setShowPromptRefine] = React.useState(false)
    const scrollRef = React.useRef<HTMLDivElement>(null)

    const handleSend = async () => {
        if (!input.trim() || loading) return

        const userMessage = input.trim()
        setInput('')
        setMessages(prev => [...prev, { role: 'user', content: userMessage }])
        setLoading(true)

        try {
            const body: Record<string, string> = { message: userMessage }
            if (persona !== 'default') body.persona = persona
            if (systemPromptOverride.trim()) body.system_prompt = systemPromptOverride.trim()

            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            })
            if (!res.ok) throw new Error("Synthesis failed")
            const data = await res.json()

            const assistantMessage: Message = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources
            }

            setMessages(prev => [...prev, assistantMessage])
        } catch (error) {
            setMessages(prev => [...prev, { role: 'assistant', content: "I'm sorry, I encountered an error while synthesizing your answer." }])
        } finally {
            setLoading(false)
        }
    }

    const exportChat = () => {
        const text = messages.map(m => `${m.role === 'user' ? 'You' : 'Assistant'}: ${m.content}`).join('\n\n')
        const blob = new Blob([text], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `docs-chat-${new Date().toISOString().slice(0, 10)}.txt`
        a.click()
        URL.revokeObjectURL(url)
    }

    React.useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [messages])

    return (
        <div className="flex-1 flex flex-col min-h-0 container max-w-5xl mx-auto py-4 md:py-6 px-4 md:px-6">
            <div className="mb-4 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-card/30 backdrop-blur-md p-4 rounded-xl border border-primary/10">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center shadow-lg transform rotate-3">
                        <Bot className="w-6 h-6 text-primary-foreground" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight">AI Assistant</h1>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-widest">Conversational RAG Core</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 flex-wrap self-end md:self-auto">
                    <Select value={persona} onValueChange={setPersona}>
                        <SelectTrigger className="w-[140px] h-9 bg-background/50 border-primary/20">
                            <SelectValue placeholder="Persona" />
                        </SelectTrigger>
                        <SelectContent>
                            {PERSONAS.map(p => (
                                <SelectItem key={p.id} value={p.id}>{p.label}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    <Button variant="outline" size="sm" onClick={exportChat} className="h-9 gap-2 border-primary/20 hover:bg-primary/5">
                        <Download className="w-3.5 h-3.5" /> Export
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setMessages([messages[0]])} className="h-9 gap-2 border-destructive/20 hover:bg-destructive/5 hover:text-destructive">
                        <Trash2 className="w-3.5 h-3.5" /> Clear
                    </Button>
                </div>
            </div>

            {/* Prompt refining (system prompt override) */}
            <div className="mb-4">
                <Button
                    variant="ghost"
                    size="sm"
                    className="text-muted-foreground gap-1"
                    onClick={() => setShowPromptRefine(!showPromptRefine)}
                >
                    {showPromptRefine ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    Prompt refining
                </Button>
                {showPromptRefine && (
                    <div className="mt-2">
                        <AutoResizeTextarea
                            placeholder="Optional system prompt override (e.g. 'Always cite file paths.')"
                            value={systemPromptOverride}
                            onChange={(e) => setSystemPromptOverride(e.target.value)}
                            className="min-h-[60px] max-h-[120px] text-sm bg-muted/30 border rounded-lg p-3"
                            rows={2}
                        />
                    </div>
                )}
            </div>

            <Card className="flex-1 flex flex-col min-h-0 border-primary/20 shadow-[0_0_50px_-12px_rgba(0,0,0,0.3)] dark:shadow-[0_0_50px_-12px_rgba(var(--primary),0.1)] overflow-hidden bg-background/40 backdrop-blur-sm relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-secondary/5 pointer-events-none opacity-50" />
                <ScrollArea className="flex-1 p-6">
                    <div className="space-y-6">
                        {messages.map((msg, i) => (
                            <div key={i} className={cn(
                                "flex gap-4 max-w-[85%]",
                                msg.role === 'user' ? "ml-auto flex-row-reverse" : ""
                            )}>
                                <div className={cn(
                                    "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                                    msg.role === 'assistant' ? "bg-primary text-primary-foreground" : "bg-muted border"
                                )}>
                                    {msg.role === 'assistant' ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
                                </div>
                                <div className="space-y-2">
                                    <div className={cn(
                                        "p-4 rounded-2xl text-sm leading-relaxed",
                                        msg.role === 'assistant' 
                                            ? "bg-muted/80 backdrop-blur-md border border-primary/10 shadow-sm" 
                                            : "bg-gradient-to-br from-primary to-primary/80 text-primary-foreground shadow-lg shadow-primary/20 border border-primary/20"
                                    )}>
                                        {msg.content}
                                    </div>
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="flex flex-wrap gap-2 px-1">
                                            {msg.sources.map(s => (
                                                <span key={s} className="text-[10px] font-bold uppercase tracking-widest bg-primary/10 text-primary px-2 py-0.5 rounded border border-primary/20">
                                                    {s}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex gap-4 max-w-[85%] animate-pulse">
                                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                                    <Loader2 className="w-5 h-5 animate-spin text-primary" />
                                </div>
                                <div className="bg-muted/30 border h-10 w-32 rounded-2xl"></div>
                            </div>
                        )}
                        <div ref={scrollRef} />
                    </div>
                </ScrollArea>

                <div className="p-4 border-t bg-card/50 backdrop-blur-md">
                    <form className="flex gap-2 items-end" onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
                        <AutoResizeTextarea
                            placeholder="Ask about MCP architecture, tools, or patterns..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
                            className="flex-1 min-h-[2.5rem] max-h-[200px] bg-background shadow-inner resize-none"
                            disabled={loading}
                            rows={1}
                        />
                        <Button type="submit" disabled={loading || !input.trim()} className="shrink-0">
                            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                        </Button>
                    </form>
                    <div className="mt-2 text-[10px] text-center text-muted-foreground font-medium uppercase tracking-widest">
                        Powered by FastMCP Sampling & neural retrieval
                    </div>
                </div>
            </Card>
        </div>
    )
}
