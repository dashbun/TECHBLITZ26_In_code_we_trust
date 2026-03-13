import { useToast } from "@/hooks/use-toast"
import { motion, AnimatePresence } from "framer-motion"
import { CheckCircle2, AlertCircle, Info, AlertTriangle, X } from "lucide-react"

export function Toaster() {
  const { toasts, dismiss } = useToast()

  return (
    <div className="fixed top-4 left-1/2 z-[100] flex max-h-screen w-full -translate-x-1/2 flex-col-reverse p-4 sm:top-auto sm:bottom-20 sm:flex-col md:max-w-[420px]">
      <AnimatePresence>
        {toasts.map((t) => {
          let Icon = Info
          let colorClass = "bg-card text-card-foreground border"
          let iconColor = "text-indigo-500"

          if (t.type === "success") {
            Icon = CheckCircle2
            iconColor = "text-[--color-success]"
          } else if (t.type === "destructive") {
            Icon = AlertCircle
            colorClass = "bg-[--color-danger] text-white"
            iconColor = "text-white"
          } else if (t.type === "warning") {
            Icon = AlertTriangle
            colorClass = "bg-[--color-warning] text-white"
            iconColor = "text-white"
          }

          return (
            <motion.div
              key={t.id}
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
              className={`pointer-events-auto mt-2 flex w-full items-center gap-3 space-y-1 rounded-lg p-4 shadow-lg ${colorClass}`}
            >
              <Icon className={`h-5 w-5 shrink-0 ${iconColor}`} />
              <div className="flex-1 px-1">
                <p className="text-sm font-semibold">{t.title}</p>
                {t.description && (
                  <p className="text-sm opacity-90">{t.description}</p>
                )}
              </div>
              <button
                onClick={() => dismiss(t.id)}
                className="shrink-0 rounded-md p-1 opacity-70 transition-opacity hover:bg-black/10 hover:opacity-100"
              >
                <X className="h-4 w-4" />
              </button>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}
