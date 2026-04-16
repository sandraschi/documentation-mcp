import os

# Target base path
REPOS_DIR = r"D:\Dev\repos"

# Templates
APP_TSX_TEMPLATE = """import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AppLayout } from '@/components/layout/app-layout';
import { Dashboard } from '@/pages/dashboard';
import { Chat } from '@/pages/chat';
import { Settings } from '@/pages/settings';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;
"""

SIDEBAR_TSX_TEMPLATE = """import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/common/utils';
import {
    LayoutDashboard,
    Bot,
    Settings,
    ChevronLeft,
    ChevronRight,
    Server
} from 'lucide-react';

interface SidebarProps {
    collapsed: boolean;
    onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
    const location = useLocation();

    const navItems = [
        { href: '/', label: 'Overview', icon: LayoutDashboard },
        { href: '/chat', label: 'AI Command', icon: Bot },
        { href: '/settings', label: 'Settings', icon: Settings },
    ];

    return (
        <aside
            className={cn(
                "relative flex flex-col border-r border-slate-800 bg-slate-950/50 " +
                "backdrop-blur-xl transition-all duration-300 ease-in-out",
                collapsed ? "w-16" : "w-64"
            )}
        >
            <div className="flex h-16 items-center border-b border-slate-800 px-4">
                <div className="flex items-center gap-2 font-semibold text-slate-100">
                    <Server className="h-6 w-6 text-blue-500" />
                    {!collapsed && <span className="animate-in fade-in duration-300">{REPO_NAME}</span>}
                </div>
            </div>

            <nav className="flex-1 space-y-1 p-2">
                {navItems.map((item) => {
                    const isActive = location.pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            to={item.href}
                            className={cn(
                                "group flex items-center rounded-md px-3 py-2 text-sm font-medium " +
                                "transition-colors hover:bg-slate-800 hover:text-white",
                                isActive ? "bg-slate-800 text-white" : "text-slate-400",
                                collapsed ? "justify-center" : "justify-start"
                            )}
                        >
                            <item.icon className={cn("h-5 w-5", !collapsed && "mr-3", isActive && "text-blue-400")} />
                            {!collapsed && <span>{item.label}</span>}

                            {/* Tooltip for collapsed mode */}
                            {collapsed && (
                                <div className="absolute left-full ml-2 hidden rounded bg-slate-800 px-2 py-1 text-xs text-white group-hover:block z-50 whitespace-nowrap">
                                    {item.label}
                                </div>
                            )}
                        </Link>
                    );
                })}
            </nav>

            <div className="border-t border-slate-800 p-2">
                <button
                    onClick={onToggle}
                    className="flex w-full items-center justify-center rounded-md p-2 text-slate-400 " +
                              "hover:bg-slate-800 hover:text-white transition-colors"
                >
                    {collapsed ? (
                        <ChevronRight className="h-5 w-5" />
                    ) : (
                        <div className="flex items-center w-full">
                            <ChevronLeft className="h-5 w-5 mr-3" />
                            <span>Collapse</span>
                        </div>
                    )}
                </button>
            </div>
        </aside>
    );
}
"""

DASHBOARD_TSX_TEMPLATE = """import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Shield, Network, Cpu, HardDrive } from "lucide-react";

export function Dashboard() {
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">{REPO_NAME} Dashboard</h2>
                    <p className="text-slate-400">System overview and status</p>
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Service Status
                        </CardTitle>
                        <Shield className="h-4 w-4 text-emerald-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Online</div>
                        <p className="text-xs text-slate-400">
                            Active connection established
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            System Load
                        </CardTitle>
                        <Cpu className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Nominal</div>
                        <p className="text-xs text-slate-400">
                            Resource usage minimal
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            API Bridge
                        </CardTitle>
                        <Activity className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Connected</div>
                        <p className="text-xs text-slate-400">
                            FastMCP bridge active
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium text-slate-200">
                            Network
                        </CardTitle>
                        <Network className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-white">Healthy</div>
                        <p className="text-xs text-slate-400">
                            Latency under 10ms
                        </p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4 border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Recent Logs</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[200px] font-mono text-xs p-4 overflow-y-auto border border-slate-800 rounded-md bg-slate-900/50 text-slate-400 space-y-1">
                            <p className="text-blue-400">[system] Daemon connection initialized...</p>
                            <p>[network] API endpoints reachable.</p>
                            <p className="text-emerald-400">[success] FastMCP Server active and bound.</p>
                            <div className="animate-pulse inline-block h-2 w-1 bg-slate-500 ml-1" />
                        </div>
                    </CardContent>
                </Card>
                <Card className="col-span-3 border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Status</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center">
                                <HardDrive className="h-4 w-4 text-slate-400 mr-2" />
                                <div className="ml-2 space-y-1">
                                    <p className="text-sm font-medium leading-none text-white">Local Storage</p>
                                    <p className="text-xs text-slate-400">Access verified</p>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <Activity className="h-4 w-4 text-emerald-500 mr-2" />
                                <div className="ml-2 space-y-1">
                                    <p className="text-sm font-medium leading-none text-white">Heartbeat</p>
                                    <p className="text-xs text-slate-400">Nominal ping tracking</p>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
"""

CHAT_TSX_TEMPLATE = """import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Send, Bot, User } from "lucide-react";

export function Chat() {
    return (
        <div className="flex h-[calc(100vh-8rem)] flex-col space-y-4">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-white">Command Interface</h2>
                    <p className="text-slate-400">Natural language tool orchestration (LLM)</p>
                </div>
            </div>

            <Card className="flex-1 border-slate-800 bg-slate-950/50 flex flex-col overflow-hidden">
                <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
                    {/* Placeholder Chat History */}
                    <div className="flex gap-3">
                        <div className="h-8 w-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
                            <User className="h-4 w-4 text-slate-400" />
                        </div>
                        <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium text-slate-200">Operator</span>
                                <span className="text-xs text-slate-500">System Start</span>
                            </div>
                            <p className="text-sm text-slate-300 bg-slate-900/50 p-3 rounded-md border border-slate-800 inline-block">
                                Perform a system check and report connection status.
                            </p>
                        </div>
                    </div>

                    <div className="flex gap-3">
                        <div className="h-8 w-8 rounded-full bg-blue-900/20 flex items-center justify-center border border-blue-800">
                            <Bot className="h-4 w-4 text-blue-400" />
                        </div>
                        <div className="flex-1 space-y-1">
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium text-blue-400">System AI</span>
                                <span className="text-xs text-slate-500">System Start</span>
                            </div>
                            <div className="text-sm text-slate-300 bg-blue-950/10 p-3 rounded-md border border-blue-900/30 inline-block">
                                <p>Acknowledged. Connecting to API bridge...</p>
                                <br />
                                <p className="font-mono text-emerald-400 text-xs">
                                    {">"} SYSTEM_CHECK: PASS <br />
                                    {">"} TOOLS: ONLINE <br />
                                    {">"} MCP: READY
                                </p>
                            </div>
                        </div>
                    </div>

                </CardContent>
                <div className="p-4 border-t border-slate-800 bg-slate-900/30">
                    <div className="flex gap-2">
                        <input
                            className="flex-1 bg-slate-950 border border-slate-800 rounded-md px-4 py-2 " +
                                      "text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none"
                            placeholder="Type a natural language command..."
                        />
                        <Button size="icon" className="bg-blue-600 hover:bg-blue-700">
                            <Send className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    );
}
"""

SETTINGS_TSX_TEMPLATE = """import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function Settings() {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold tracking-tight text-white">Configuration</h2>
                <p className="text-slate-400">Manage connections and preferences</p>
            </div>

            <div className="grid gap-6">
                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">API Bridge Configuration</CardTitle>
                        <CardDescription className="text-slate-400">Connection details for the backend server</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">API Host</Label>
                            <Input
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="http://localhost:107xx"
                            />
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Test Connection
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-950/50">
                    <CardHeader>
                        <CardTitle className="text-white">Advanced Integration</CardTitle>
                        <CardDescription className="text-slate-400">Custom connection parameters</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">Timeout (ms)</Label>
                            <Input
                                className="bg-slate-900 border-slate-800 text-slate-100 placeholder:text-slate-400"
                                defaultValue="5000"
                            />
                        </div>
                        <Button variant="outline" className="border-slate-800 text-slate-300 hover:bg-slate-800">
                            Save Parameters
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
"""


def main():
    cleaned_count = 0
    dirs = os.listdir(REPOS_DIR)

    for folder in dirs:
        repo_path = os.path.join(REPOS_DIR, folder)
        if not os.path.isdir(repo_path):
            continue

        web_sota_pth = os.path.join(repo_path, "web_sota")
        if not os.path.exists(web_sota_pth):
            continue

        dashboard_pth = os.path.join(web_sota_pth, "src", "pages", "dashboard.tsx")
        if os.path.exists(dashboard_pth):
            with open(dashboard_pth, encoding="utf-8") as f:
                content = f.read()

            if "Unitree" in content or "Active Robots" in content:
                print(f"[*] Found dirty robotic boilerplate in {folder}, applying SOTA cleanse...")

                # Format Name (e.g., ring-mcp -> Ring MCP)
                friendly_name = folder.replace("-mcp", "").capitalize() + " MCP"

                # Overwrite App.tsx
                app_path = os.path.join(web_sota_pth, "src", "App.tsx")
                with open(app_path, "w", encoding="utf-8") as f:
                    f.write(APP_TSX_TEMPLATE)

                # Overwrite layout/sidebar.tsx
                sidebar_path = os.path.join(web_sota_pth, "src", "components", "layout", "sidebar.tsx")
                if os.path.exists(sidebar_path):
                    with open(sidebar_path, "w", encoding="utf-8") as f:
                        f.write(SIDEBAR_TSX_TEMPLATE.replace("{REPO_NAME}", friendly_name))

                # Overwrite dashboard.tsx
                with open(dashboard_pth, "w", encoding="utf-8") as f:
                    f.write(DASHBOARD_TSX_TEMPLATE.replace("{REPO_NAME}", friendly_name))

                # Overwrite chat.tsx
                chat_pth = os.path.join(web_sota_pth, "src", "pages", "chat.tsx")
                if os.path.exists(chat_pth):
                    with open(chat_pth, "w", encoding="utf-8") as f:
                        f.write(CHAT_TSX_TEMPLATE)

                # Overwrite settings.tsx
                settings_pth = os.path.join(web_sota_pth, "src", "pages", "settings.tsx")
                if os.path.exists(settings_pth):
                    with open(settings_pth, "w", encoding="utf-8") as f:
                        f.write(SETTINGS_TSX_TEMPLATE)

                # Delete control.tsx and visualizer.tsx
                control_pth = os.path.join(web_sota_pth, "src", "pages", "control.tsx")
                if os.path.exists(control_pth):
                    os.remove(control_pth)

                visualizer_pth = os.path.join(web_sota_pth, "src", "pages", "visualizer.tsx")
                if os.path.exists(visualizer_pth):
                    os.remove(visualizer_pth)

                cleaned_count += 1

    print(f"\n[DONE] Successfully sanitized {cleaned_count} MCP webapp boilerplates.")


if __name__ == "__main__":
    main()
