import * as React from "react"
import { cn } from "@/lib/utils"

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "brutal-border bg-white px-4 py-3 font-mono text-base focus:outline-none focus:ring-4 focus:ring-black focus:ring-offset-4 disabled:cursor-not-allowed disabled:opacity-50 w-full min-h-[100px] resize-y",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Textarea.displayName = "Textarea"

export { Textarea }
