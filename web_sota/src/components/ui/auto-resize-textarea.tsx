import * as React from "react"
import { cn } from "@/lib/utils"

export interface AutoResizeTextareaProps
    extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const AutoResizeTextarea = React.forwardRef<HTMLTextAreaElement, AutoResizeTextareaProps>(
    ({ className, value, onChange, ...props }, ref) => {
        const innerRef = React.useRef<HTMLTextAreaElement | null>(null)

        const resize = React.useCallback(() => {
            const el = innerRef.current
            if (!el) return
            const minH = props.rows ? props.rows * 20 : 24
            el.style.height = "0px"
            el.style.height = `${Math.max(minH, el.scrollHeight)}px`
        }, [props.rows])

        React.useEffect(() => {
            resize()
        }, [value, resize])

        const handleRef = (el: HTMLTextAreaElement | null) => {
            innerRef.current = el
            if (typeof ref === "function") ref(el)
            else if (ref) (ref as React.MutableRefObject<HTMLTextAreaElement | null>).current = el
        }

        return (
            <textarea
                ref={handleRef}
                value={value}
                onChange={(e) => {
                    onChange?.(e)
                    resize()
                }}
                className={cn(
                    "flex w-full min-h-[2.5rem] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none overflow-hidden",
                    className
                )}
                rows={props.rows ?? 1}
                {...props}
            />
        )
    }
)
AutoResizeTextarea.displayName = "AutoResizeTextarea"

export { AutoResizeTextarea }
