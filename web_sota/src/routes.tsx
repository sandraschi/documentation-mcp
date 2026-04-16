/** Path-based routing: each view has a URL e.g. /help, /settings */
export type ViewState =
    | "dashboard"
    | "search"
    | "semantic"
    | "documents"
    | "tools"
    | "memory"
    | "help"
    | "skills"
    | "chat"
    | "apps"
    | "fleet"
    | "docker"
    | "logs"

    | "settings"

export const viewToPath: Record<ViewState, string> = {
    dashboard: "/dashboard",
    search: "/search",
    semantic: "/semantic",
    documents: "/documents",
    tools: "/tools",
    memory: "/memory",
    help: "/help",
    skills: "/skills",
    chat: "/chat",
    apps: "/apps",
    fleet: "/fleet",
    docker: "/docker",
    logs: "/logs",

    settings: "/settings",
}

const pathToView: Record<string, ViewState> = {}
for (const [view, path] of Object.entries(viewToPath)) {
    pathToView[path] = view as ViewState
}
pathToView["/"] = "dashboard"

export function pathnameToView(pathname: string): ViewState {
    const normalized = pathname.replace(/\/$/, "") || "/"
    return pathToView[normalized] ?? "dashboard"
}

export function viewToPathname(view: ViewState): string {
    return viewToPath[view]
}
