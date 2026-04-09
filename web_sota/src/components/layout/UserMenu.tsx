import * as React from "react"
import { useAuth } from "../../contexts/AuthContext"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { User as UserIcon, Settings, LogOut, Shield } from "lucide-react"
import { LoginDialog } from "./LoginDialog"

interface UserMenuProps {
    onNavigateToSettings?: () => void
}

export function UserMenu({ onNavigate }: UserMenuProps) {
    const { user, isAuthenticated, logout } = useAuth()
    const [loginOpen, setLoginOpen] = React.useState(false)

    if (!isAuthenticated) {
        return (
            <>
                <Button variant="outline" size="sm" onClick={() => setLoginOpen(true)} className="font-bold text-[10px] uppercase tracking-widest px-4 border-primary/30 hover:bg-primary/10">
                    Login
                </Button>
                <LoginDialog open={loginOpen} onOpenChange={setLoginOpen} />
            </>
        )
    }

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-9 w-9 rounded-full ring-1 ring-border shadow-sm p-0 overflow-hidden">
                    {user?.avatar ? (
                        <img src={user.avatar} alt={user.name} className="h-full w-full object-cover" />
                    ) : (
                        <UserIcon className="h-5 w-5" />
                    )}
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-1">
                        <p className="text-sm font-bold leading-none">{user?.name}</p>
                        <p className="text-[10px] font-mono leading-none text-muted-foreground uppercase tracking-tighter">
                            {user?.email}
                        </p>
                    </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="gap-2 cursor-pointer">
                    <UserIcon className="h-4 w-4" />
                    <span>Profile</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="gap-2 cursor-pointer" onClick={onNavigateToSettings}>
                    <Settings className="h-4 w-4" />
                    <span>Settings</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                {user?.role === 'admin' && (
                    <>
                        <DropdownMenuItem className="gap-2 cursor-pointer text-primary">
                            <Shield className="h-4 w-4" />
                            <span>Admin Dashboard</span>
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                    </>
                )}
                <DropdownMenuItem className="gap-2 cursor-pointer text-destructive focus:text-destructive" onClick={logout}>
                    <LogOut className="h-4 w-4" />
                    <span>Log out</span>
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}
