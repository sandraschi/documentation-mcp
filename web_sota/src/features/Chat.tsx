import * as React from "react"
import { Send, Loader2, User, Bot, Trash2, Download, ChevronDown, ChevronUp, Cpu, Settings as SettingsIcon, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { cn } from "@/lib/utils"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AutoResizeTextarea } from "@/components/ui/auto-resize-textarea"
import { Badge } from "@/components/ui/badge"
import { API_BASE } from "@/lib/api"

interface Message {
    id: string
    role: 'user' | 'assistant'
    content: string
    sources?: string[]
}

interface ProviderInfo {
    key: string
    label: string
    models: string[]
}

const PROVIDERS: ProviderInfo[] = [
    { key: "", label: "None (RAG only)", models: [] },
    { key: "ollama", label: "Ollama", models: [] },
    { key: "local", label: "Local LLM (OpenAI)", models: [] },
    { key: "openai", label: "OpenAI", models: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"] },
    { key: "anthropic", label: "Anthropic", models: ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022"] },
    { key: "gemini", label: "Google Gemini", models: ["gemini-2.5-pro", "gemini-2.5-flash"] },
]

const PERSONAS = [
    { id: 'default', label: 'Default', hint: 'General documentation assistant' },
    { id: 'technical', label: 'Technical', hint: 'Precise, code-focused answers' },
    { id: 'concise', label: 'Concise', hint: 'Short, to-the-point' },
    { id: 'educator', label: 'Educator', hint: 'Step-by-step explanations' },
]

let _msgId = 0
function nextId() { return `m${++_msgId}` }

export function ChatView() {
    const [messages, setMessages] = React.useState<Message[]>([])
    const [input, setInput] = React.useState('')
    const [loading, setLoading] = React.useState(false)
    const [streamingContent, setStreamingContent] = React.useState('')
    const [streamingSources, setStreamingSources] = React.useState<string[]>([])
    const [persona, setPersona] = React.useState('default')
    const [provider, setProvider] = React.useState('')
    const [model, setModel] = React.useState('')
    const [apiKey, setApiKey] = React.useState('')
    const [apiUrl, setApiUrl] = React.useState('')
    const [conversationId, setConversationId] = React.useState<string | null>(null)
    const [systemPromptOverride, setSystemPromptOverride] = React.useState('')
    const [showPromptRefine, setShowPromptRefine] = React.useState(false)
    const [showSettings, setShowSettings] = React.useState(false)
    const [discoveredOllama, setDiscoveredOllama] = React.useState(false)
    const [discoveredLmstudio, setDiscoveredLmstudio] = React.useState(false)
    const scrollRef = React.useRef<HTMLDivElement>(null)

    // Auto-discover LLM engines on mount
    React.useEffect(() => {
        fetch(API_BASE + "/api/auto-discover")
            .then(r => r.json())
            .then(d => {
                if (d.ollama) setDiscoveredOllama(true)
                if (d.lmstudio) setDiscoveredLmstudio(true)
            })
            .catch(() => {})
    }, [])

    const handleSend = async () => {
        if (!input.trim() || loading) return

        const userMsg: Message = { id: nextId(), role: 'user', content: input.trim() }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setLoading(true)
        setStreamingContent('')
        setStreamingSources([])

        try {
            const body: Record<string, string> = {
                message: userMsg.content,
                persona,
                provider,
                model,
            }
            if (conversationId) body.conversation_id = conversationId
            if (apiKey.trim()) body.api_key = apiKey.trim()
            if (apiUrl.trim()) body.api_url = apiUrl.trim()
            if (systemPromptOverride.trim()) body.system_prompt = systemPromptOverride.trim()

            const res = await fetch(API_BASE + '/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            })
            if (!res.ok) throw new Error(`HTTP ${res.status}`)

            const reader = res.body?.getReader()
            if (!reader) throw new Error("No response body")

            const decoder = new TextDecoder()
            let buffer = ""

            while (true) {
                const { done, value } = await reader.read()
                if (done) break
                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split("\n")
                buffer = lines.pop() || ""

                for (const line of lines) {
                    if (!line.startsWith("data: ")) continue
                    const raw = line.slice(6).trim()
                    if (!raw) continue
                    try {
                        const ev = JSON.parse(raw)
                        if (ev.type === "token") {
                            setStreamingContent(prev => prev + ev.content)
                        } else if (ev.type === "sources") {
                            setStreamingSources(ev.content || [])
                        } else if (ev.type === "done") {
                            if (ev.conversation_id) setConversationId(ev.conversation_id)
                        }
                    } catch { /* skip malformed */ }
                }
            }

            // Finalize the streaming message into the message list
            setMessages(prev => {
                const last = prev[prev.length - 1]
                if (last?.role === 'assistant' && last.content === streamingContent + "") {
                    return prev
                }
                return [...prev]
            })
        } catch (error) {
            const errMsg = error instanceof Error ? error.message : "Request failed"
            setStreamingContent(`Error: ${errMsg}`)
        } finally {
            // Commit streamed content as final message
            setMessages(prev => [...prev, { id: nextId(), role: 'assistant', content: streamingContent, sources: streamingSources }])
            setStreamingContent('')
            setStreamingSources([])
            setLoading(false)
        }
    }

    const exportChat = () => {
        const text = messages.map(m => `${m.role === 'user' ? 'You' : 'Assistant'}: ${m.content}${m.sources?.length ? `\nSources: ${m.sources.join(', ')}` : ''}`).join('\n\n---\n\n')
        const blob = new Blob([text], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `docs-chat-${new Date().toISOString().slice(0, 10)}.txt`
        a.click()
        URL.revokeObjectURL(url)
    }

    const clearChat = () => {
        setMessages([])
        setConversationId(null)
        setStreamingContent('')
        setStreamingSources([])
    }

    React.useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [messages, streamingContent])

    // Handle initial query from URL
    React.useEffect(() => {
        const params = new URLSearchParams(window.location.search)
        const query = params.get('q')
        if (query && messages.length === 0) {
            setInput(query)
            window.history.replaceState({}, '', window.location.pathname)
        }
    }, [])

    const currentProvider = PROVIDERS.find(p => p.key === provider)
    const availableModels = currentProvider?.models || []

    return (
        <div data-testid="chat-page" className="flex-1 flex flex-col min-h-0 container max-w-5xl mx-auto py-4 md:py-6 px-4 md:px-6">
            {/* Header */}
            <div className="mb-4 flex flex-col md:flex-row md:items-center justify-between gap-4 bg-card/30 backdrop-blur-md p-4 rounded-xl border border-primary/10">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center shadow-lg transform rotate-3">
                        <Bot className="w-6 h-6 text-primary-foreground" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight">AI Assistant</h1>
                        <p className="text-sm text-muted-foreground font-medium uppercase tracking-widest">Conversational RAG</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 flex-wrap self-end md:self-auto">
                    {(discoveredOllama || discoveredLmstudio) && (
                        <div className="flex gap-1">
                            {discoveredOllama && <Badge variant="outline" className="text-[9px] border-emerald-500/30 text-emerald-500">Ollama</Badge>}
                            {discoveredLmstudio && <Badge variant="outline" className="text-[9px] border-blue-500/30 text-blue-500">LM Studio</Badge>}
                        </div>
                    )}
                        <Select value={persona} onValueChange={setPersona}>
                        <SelectTrigger data-testid="personality-select" className="w-[130px] h-9 bg-background/50 border-primary/20">
                            <SelectValue placeholder="Persona" />
                        </SelectTrigger>
                        <SelectContent>
                            {PERSONAS.map(p => (
                                <SelectItem key={p.id} value={p.id}>{p.label}</SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    <Button variant="outline" size="sm" onClick={() => setShowSettings(!showSettings)} className="h-9 gap-1 border-primary/20">
                        <SettingsIcon className="w-3.5 h-3.5" /> Models
                    </Button>
                    <Button data-testid="chat-export" variant="outline" size="sm" onClick={exportChat} className="h-9 gap-2 border-primary/20">
                        <Download className="w-3.5 h-3.5" /> Export
                    </Button>
                    <Button data-testid="chat-clear" variant="outline" size="sm" onClick={clearChat} className="h-9 gap-2 border-destructive/20 hover:bg-destructive/5 hover:text-destructive">
                        <Trash2 className="w-3.5 h-3.5" /> Clear
                    </Button>
                </div>
            </div>

            {/* Provider settings panel */}
            {showSettings && (
                <Card className="mb-4 p-4 space-y-3 border-primary/10">
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Provider</label>
                            <Select value={provider} onValueChange={(v) => { setProvider(v); setModel('') }}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select provider" />
                                </SelectTrigger>
                                <SelectContent>
                                    {PROVIDERS.map(p => (
                                        <SelectItem key={p.key} value={p.key}>{p.label}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        {availableModels.length > 0 && (
                            <div className="space-y-2">
                                <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Model</label>
                                <Select value={model} onValueChange={setModel}>
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select model" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {availableModels.map(m => (
                                            <SelectItem key={m} value={m}>{m}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                        )}
                        {(provider === "openai" || provider === "anthropic" || provider === "gemini") && (
                            <div className="space-y-2">
                                <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground">API Key</label>
                                <input
                                    type="password"
                                    placeholder="sk-..."
                                    value={apiKey}
                                    onChange={(e) => setApiKey(e.target.value)}
                                    className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm font-mono"
                                />
                            </div>
                        )}
                        {provider === "local" && (
                            <div className="space-y-2">
                                <label className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Server URL</label>
                                <input
                                    type="text"
                                    placeholder="http://localhost:1234/v1"
                                    value={apiUrl}
                                    onChange={(e) => setApiUrl(e.target.value)}
                                    className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm font-mono"
                                />
                            </div>
                        )}
                    </div>
                </Card>
            )}

            {/* Prompt refining */}
            <div className="mb-4">
                <Button variant="ghost" size="sm" className="text-muted-foreground gap-1"
                    onClick={() => setShowPromptRefine(!showPromptRefine)}>
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

            {/* Chat area */}
            <Card className="flex-1 flex flex-col min-h-0 border-primary/20 shadow-[0_0_50px_-12px_rgba(0,0,0,0.3)] overflow-hidden bg-background/40 backdrop-blur-sm relative">
                <ScrollArea data-testid="chat-messages" className="flex-1 p-6">
                    <div className="space-y-6">
                        {messages.map((msg) => (
                            <div key={msg.id} className={cn("flex gap-4 max-w-[85%]", msg.role === 'user' ? "ml-auto flex-row-reverse" : "")}>
                                <div className={cn("w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                                    msg.role === 'assistant' ? "bg-primary text-primary-foreground" : "bg-muted border")}>
                                    {msg.role === 'assistant' ? <Bot className="w-5 h-5" /> : <User className="w-5 h-5" />}
                                </div>
                                <div className="space-y-2">
                                    <div className={cn("p-4 rounded-2xl text-sm leading-relaxed",
                                        msg.role === 'assistant'
                                            ? "bg-muted/80 backdrop-blur-md border border-primary/10 shadow-sm"
                                            : "bg-gradient-to-br from-primary to-primary/80 text-primary-foreground shadow-lg")}>
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
                        {/* Streaming message */}
                        {loading && streamingContent && (
                            <div className="flex gap-4 max-w-[85%]">
                                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center shrink-0">
                                    <Bot className="w-5 h-5 text-primary-foreground" />
                                </div>
                                <div className="space-y-2">
                                    <div className="p-4 rounded-2xl text-sm leading-relaxed bg-muted/80 backdrop-blur-md border border-primary/10 shadow-sm">
                                        {streamingContent}
                                        <span className="inline-block w-2 h-4 bg-primary/60 ml-0.5 animate-pulse" />
                                    </div>
                                    {streamingSources.length > 0 && (
                                        <div className="flex flex-wrap gap-2 px-1">
                                            {streamingSources.map(s => (
                                                <span key={s} className="text-[10px] font-bold uppercase tracking-widest bg-primary/10 text-primary px-2 py-0.5 rounded border border-primary/20">
                                                    {s}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                        {/* Typing indicator */}
                        {loading && !streamingContent && (
                            <div className="flex gap-4 max-w-[85%]">
                                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                                    <Loader2 className="w-5 h-5 animate-spin text-primary" />
                                </div>
                                <div className="bg-muted/30 border h-10 w-32 rounded-2xl flex items-center justify-center gap-1 px-3">
                                    <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                                    <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                                    <span className="w-1.5 h-1.5 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                                </div>
                            </div>
                        )}
                        <div ref={scrollRef} />
                    </div>
                </ScrollArea>

                <div className="p-4 border-t bg-card/50 backdrop-blur-md">
                    <form className="flex gap-2 items-end" onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
                        <AutoResizeTextarea
                            data-testid="chat-input"
                            placeholder="Ask about MCP architecture, tools, or patterns..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
                            className="flex-1 min-h-[2.5rem] max-h-[200px] bg-background shadow-inner resize-none"
                            disabled={loading}
                            rows={1}
                        />
                        <Button data-testid="chat-send" type="submit" disabled={loading || !input.trim()} className="shrink-0">
                            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                        </Button>
                    </form>
                    <div className="mt-2 text-[10px] text-center text-muted-foreground font-medium uppercase tracking-widest flex items-center justify-center gap-2">
                        {discoveredOllama && <><Cpu className="w-3 h-3 text-emerald-500" /> Ollama</>}
                        {discoveredLmstudio && <><Sparkles className="w-3 h-3 text-blue-500" /> LM Studio</>}
                        {!discoveredOllama && !discoveredLmstudio && <>Memory · Streaming · Personalities</>}
                    </div>
                </div>
            </Card>
        </div>
    )
}
