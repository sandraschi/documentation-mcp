import * as React from "react"
import { useAuth } from "../../contexts/AuthContext"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Lock, User } from "lucide-react"

interface LoginDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
}

export function LoginDialog({ open, onOpenChange }: LoginDialogProps) {
    const { login } = useAuth()
    const [username, setUsername] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [error, setError] = React.useState(false)

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault()
        const success = login(username, password)
        if (success) {
            onOpenChange(false)
            setError(false)
        } else {
            setError(true)
        }
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[400px]">
                <DialogHeader className="space-y-3">
                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mx-auto">
                        <Lock className="w-6 h-6 text-primary" />
                    </div>
                    <DialogTitle className="text-center text-xl font-bold tracking-tight">System Authentication</DialogTitle>
                    <DialogDescription className="text-center text-xs uppercase tracking-widest text-muted-foreground">
                        Enter credentials to access Docs MCP
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleLogin} className="space-y-4 py-4">
                    <div className="space-y-2">
                        <div className="relative">
                            <User className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Username"
                                className="pl-10"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                    </div>
                    <div className="space-y-2">
                        <div className="relative">
                            <Lock className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                type="password"
                                placeholder="Password"
                                className="pl-10"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        {error && (
                            <p className="text-[10px] text-destructive font-bold uppercase tracking-tighter">
                                Invalid credentials. Hint: admin / admin
                            </p>
                        )}
                    </div>
                    <Button type="submit" className="w-full font-bold uppercase tracking-widest">
                        Authenticate
                    </Button>
                </form>
                <DialogFooter className="text-center sm:justify-center">
                    <p className="text-[10px] text-muted-foreground">© 2026 VIENNA SYSTEMS • REDUCTIONIST LOGIC</p>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
