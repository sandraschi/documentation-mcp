import { Routes, Route, Navigate } from "react-router-dom"
import { AppLayout } from "@/components/layout/AppLayout"
import { SearchView } from "@/features/Search"
import { SemanticSearchView } from "@/features/SemanticSearch"
import { Dashboard } from "@/features/Dashboard"
import { Documents } from "@/features/Documents"
import { ToolsHub } from "@/features/ToolsHub"
import { Memory } from "@/features/Memory"
import { Help } from "@/features/Help"
import { Skills } from "@/features/Skills"
import { Apps } from "@/features/Apps"
import { DockerDesktop } from "@/features/DockerDesktop"
import { Settings } from "@/features/Settings"
import { ChatView } from "@/features/Chat"

function App() {
    return (
        <Routes>
            <Route path="/" element={<AppLayout />}>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="search" element={<SearchView />} />
                <Route path="semantic" element={<SemanticSearchView />} />
                <Route path="documents" element={<Documents />} />
                <Route path="tools" element={<ToolsHub />} />
                <Route path="memory" element={<Memory />} />
                <Route path="help" element={<Help />} />
                <Route path="skills" element={<Skills />} />
                <Route path="chat" element={<ChatView />} />
                <Route path="apps" element={<Apps />} />
                <Route path="docker" element={<DockerDesktop />} />
                <Route path="settings" element={<Settings />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Route>
        </Routes>
    )
}

export default App
