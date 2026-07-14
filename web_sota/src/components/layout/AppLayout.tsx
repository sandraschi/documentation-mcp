import * as React from "react"
import { Outlet, useLocation, useNavigate, NavLink } from "react-router-dom"
import { Search as SearchIcon, Home, CircleHelp, BookOpen, Menu, Terminal, MessageSquare, Bot, Send, X as CloseIcon, LayoutGrid, Settings as SettingsIcon, FileSearch, BookMarked, Brain, Shield, FolderOpen, ScrollText, ChevronLeft, ChevronRight, Code2, Activity } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Input } from "@/components/ui/input"
import { HelpDialog } from "@/components/help-dialog"
import { LoggerDialog } from "@/components/logger-dialog"
import { UserMenu } from "./UserMenu"
import { useAuth } from "../../contexts/AuthContext"
import { useZoom } from "../../lib/use-zoom"
import { useAppStore } from "../../lib/store"
import { pathnameToView, viewToPathname, type ViewState } from "../../routes"

interface NavItem {
    title: string
    view: ViewState
    icon: React.ComponentType<{ className?: string }>
}

const navItems: NavItem[] = [
    { title: "Dashboard", view: "dashboard", icon: Home },
    { title: "Documents", view: "documents", icon: BookOpen },
    { title: "Semantic Search", view: "semantic", icon: FileSearch },
    { title: "Tools Hub", view: "tools", icon: Terminal },
    { title: "Persistence", view: "memory", icon: Brain },
    { title: "Skills", view: "skills", icon: BookMarked },
    { title: "AI Assistant", view: "chat", icon: MessageSquare },
    { title: "Fleet Dashboard", view: "apps", icon: LayoutGrid },
    { title: "Project Portfolio", view: "fleet", icon: FolderOpen },
    { title: "System Logs", view: "logs", icon: ScrollText },

    { title: "API Docs", view: "api-docs", icon: Code2 },
    { title: "Admin", view: "admin", icon: Activity },
    { title: "Settings", view: "settings", icon: SettingsIcon },
    { title: "Help", view: "help", icon: CircleHelp },
]


export function AppLayout() {
    const [chatOpen, setChatOpen] = React.useState(false)
    const { user } = useAuth()
    const location = useLocation()
    const navigate = useNavigate()
    const currentView = pathnameToView(location.pathname)
    const isSidebarOpen = useAppStore((s) => s.sidebarOpen)
    const setSidebarOpen = useAppStore((s) => s.setSidebarOpen)
    useZoom()

    
    const cleanupLayers = () => {
        const allElements = document.querySelectorAll('*');
        let count = 0;
        allElements.forEach((el) => {
            const style = window.getComputedStyle(el);
            const zIndex = parseInt(style.zIndex);
            // Hide anything with extreme z-index that isn't part of our app (we use up to 100 usually, Sheets/Dialogs use ~50-100)
            if (zIndex > 1000 && !el.closest('#root') && !el.closest('[data-radix-portal]')) {
                (el as HTMLElement).style.display = 'none';
                count++;
            }
        });
        if (count > 0) {
            console.log(`Cleaned up ${count} invasive layers.`);
        }
    }

    return (
        <div className="min-h-screen bg-background font-sans selection:bg-accent selection:text-accent-foreground flex">

            {/* Desktop Sidebar */}
            <aside className={cn(
                "hidden md:flex flex-col border-r bg-card/50 backdrop-blur-xl h-screen sticky top-0 transition-all duration-300 overflow-x-hidden",
                isSidebarOpen ? "w-64" : "w-20"
            )}>
                <div className="h-16 flex items-center px-6 border-b">
                    <NavLink to="/dashboard" className="flex items-center gap-2 font-bold text-xl tracking-tight cursor-pointer">
                        <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                            <BookOpen className="w-5 h-5 text-primary-foreground" />
                        </div>
                        {isSidebarOpen && <span className="bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">Docs MCP</span>}
                    </NavLink>
                    <button
                        onClick={() => setSidebarOpen(!isSidebarOpen)}
                        className="ml-auto flex items-center justify-center rounded-md p-1.5 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
                        title={isSidebarOpen ? "Collapse sidebar" : "Expand sidebar"}
                    >
                        {isSidebarOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                    </button>
                </div>

                <div className="flex-1 py-6 px-4 space-y-2 overflow-y-auto scrollbar-none">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.view}
                            to={viewToPathname(item.view)}
                            className={({ isActive }) =>
                                cn(
                                    "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                                    isActive ? "bg-secondary text-secondary-foreground" : "hover:bg-accent hover:text-accent-foreground",
                                    !isSidebarOpen && "justify-center px-2"
                                )
                            }
                        >
                            <item.icon className="w-5 h-5 shrink-0" />
                            {isSidebarOpen && <span>{item.title}</span>}
                        </NavLink>
                    ))}

                    <div className="my-4 border-t border-border/50 mx-2"></div>

                    <NavLink
                        to="/search"
                        className={({ isActive }) =>
                            cn(
                                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                                isActive ? "bg-secondary text-secondary-foreground" : "hover:bg-accent hover:text-accent-foreground",
                                !isSidebarOpen && "justify-center px-2"
                            )
                        }
                    >
                        <SearchIcon className="w-5 h-5 shrink-0" />
                        {isSidebarOpen && <span>Search</span>}
                    </NavLink>
                </div>

            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0">
                <header className="sticky top-0 z-50 flex h-16 items-center gap-4 border-b bg-background/80 backdrop-blur-md px-4 md:px-6 shadow-sm">
                    <div className="flex items-center gap-4">
                        <Sheet>
                            <SheetTrigger asChild>
                                <Button variant="ghost" size="icon" className="md:hidden">
                                    <Menu className="w-5 h-5" />
                                </Button>
                            </SheetTrigger>
                            <SheetContent side="left" className="w-64 p-0">
                                <div className="h-16 flex items-center px-6 border-b">
                                    <span className="font-bold text-xl">Docs MCP</span>
                                </div>
                                <div className="p-4 space-y-2">
                                    {navItems.map((item) => (
                                        <Button
                                            key={item.title}
                                            variant="ghost"
                                            className="w-full justify-start gap-3"
                                            onClick={() => navigate(viewToPathname(item.view))}
                                        >
                                            <item.icon className="w-5 h-5" />
                                            <span>{item.title}</span>
                                        </Button>
                                    ))}
                                </div>
                            </SheetContent>
                        </Sheet>

                        <div className="hidden md:flex items-center text-sm font-medium text-foreground/80">
                            <span className="opacity-70">DOCS OPS</span>
                            <span className="mx-2 text-muted-foreground">/</span>
                            <span className="capitalize">{currentView.replace("-", " ")}</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <div className="relative group mr-2">
                            <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-lg blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
                            <div
                                className="relative flex items-center bg-muted/50 border rounded-lg px-3 py-1.5 text-sm text-foreground w-64 cursor-pointer hover:bg-muted transition-colors"
                                onClick={() => navigate("/search")}
                                role="button"
                                tabIndex={0}
                                onKeyDown={(e) => e.key === "Enter" && navigate("/search")}
                            >
                                <SearchIcon className="w-4 h-4 mr-2 text-muted-foreground" />
                                <span className="flex-1 text-left text-muted-foreground">Search docs...</span>
                                <kbd className="hidden sm:inline-flex h-5 items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium opacity-100 text-muted-foreground">
                                    <span className="text-xs">⌘</span>K
                                </kbd>
                            </div>
                        </div>
                        <Button 
                            variant="ghost" 
                            size="icon" 
                            onClick={cleanupLayers} 
                            title="Clean Overlays"
                            className="text-muted-foreground hover:text-primary transition-colors"
                        >
                            <Shield className="w-5 h-5" />
                        </Button>
                        <LoggerDialog />
                        <HelpDialog />
                        <UserMenu onNavigateToSettings={() => navigate("/settings")} />
                    </div>
                </header>

                <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
                    <Outlet />
                </div>
            </main>

            {/* Quick Chat Floater */}
            <div className="fixed bottom-6 right-6 z-[60]">
                {chatOpen ? (
                    <div className="bg-card border shadow-2xl rounded-2xl w-[380px] h-[500px] flex flex-col overflow-hidden animate-in zoom-in-95 fade-in duration-300">
                        <div className="p-4 border-b bg-primary flex items-center justify-between text-primary-foreground">
                            <div className="flex items-center gap-2">
                                <Bot className="w-5 h-5" />
                                <span className="font-bold text-sm tracking-tight">Docs Assistant</span>
                            </div>
                            <Button variant="ghost" size="icon" className="h-8 w-8 text-primary-foreground hover:bg-white/10" onClick={() => setChatOpen(false)}>
                                <CloseIcon className="w-4 h-4" />
                            </Button>
                        </div>
                        <div className="flex-1 p-4 overflow-y-auto bg-muted/20">
                            <div className="space-y-4">
                                <div className="flex gap-2">
                                    <div className="w-7 h-7 rounded-full bg-primary flex items-center justify-center text-[10px] text-primary-foreground">B</div>
                                    <div className="bg-background border p-3 rounded-2xl rounded-tl-none text-xs shadow-sm">
                                        Hi {user?.name.split(" ")[0] || "there"}! I'm ready to help with your documentation questions.
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="p-4 border-t bg-background">
                            <div className="relative">
                                <Input placeholder="Type your message..." className="pr-10 text-xs py-5 rounded-xl shadow-inner" />
                                <Button size="icon" className="absolute right-1 top-1 h-8 w-8 rounded-lg shadow-md" onClick={() => navigate("/chat")}>
                                    <Send className="w-3.5 h-3.5" />
                                </Button>
                            </div>
                        </div>
                    </div>
                ) : (
                    <Button
                        onClick={() => setChatOpen(true)}
                        className="h-14 w-14 rounded-full shadow-2xl shadow-primary/40 hover:scale-110 transition-transform duration-300 ring-2 ring-primary/20"
                    >
                        <MessageSquare className="w-6 h-6" />
                    </Button>
                )}
            </div>
        </div>
    )
}
