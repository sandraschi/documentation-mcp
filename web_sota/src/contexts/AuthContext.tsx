import * as React from "react"

interface User {
    id: string
    name: string
    email: string
    role: 'admin' | 'user'
    avatar?: string
}

interface AuthContextType {
    user: User | null
    isAuthenticated: boolean
    login: (username?: string, password?: string) => boolean
    logout: () => void
}

const AuthContext = React.createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = React.useState<User | null>(() => {
        const saved = localStorage.getItem('mcp_auth_user')
        return saved ? JSON.parse(saved) : null
    })

    const login = (username?: string, password?: string) => {
        // Standard Auth Scaffold logic
        if (username === 'admin' && password === 'admin') {
            const mockUser: User = {
                id: "1",
                name: "Sandra Schipal",
                email: "sandra.schipal@vienna.systems",
                role: "admin",
                avatar: "https://github.com/sandraschi.png"
            }
            setUser(mockUser)
            localStorage.setItem('mcp_auth_user', JSON.stringify(mockUser))
            return true
        }
        return false
    }

    const logout = () => {
        setUser(null)
        localStorage.removeItem('mcp_auth_user')
    }

    const isAuthenticated = !!user

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = React.useContext(AuthContext)
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}
