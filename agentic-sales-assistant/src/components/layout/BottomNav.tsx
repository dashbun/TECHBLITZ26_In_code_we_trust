import { NavLink } from "react-router-dom"
import { motion } from "framer-motion"
import { Home, Inbox, ListTodo, CalendarClock, Bell } from "lucide-react"

const NAV_ITEMS = [
  { id: "dashboard", path: "/", icon: Home, label: "Home" },
  { id: "inbox", path: "/inbox", icon: Inbox, label: "Inbox" },
  { id: "pipeline", path: "/pipeline", icon: ListTodo, label: "Pipeline" },
  { id: "automation", path: "/automation", icon: CalendarClock, label: "Follow-ups" },
  { id: "notifications", path: "/notifications", icon: Bell, label: "Alerts" },
]

export function BottomNav() {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-around border-t bg-background px-2 pb-safe shadow-lg md:hidden">
      {NAV_ITEMS.map((item) => {
        const Icon = item.icon
        return (
          <NavLink
            key={item.id}
            to={item.path}
            className={({ isActive }) =>
              `relative flex h-full w-16 flex-col items-center justify-center space-y-1 ${
                isActive ? "text-[--color-primary]" : "text-muted-foreground hover:text-foreground"
              }`
            }
          >
            {({ isActive }) => (
              <>
                <motion.div
                  whileTap={{ scale: 0.9 }}
                  className="flex flex-col items-center justify-center relative"
                >
                  <Icon className="h-5 w-5" strokeWidth={isActive ? 2.5 : 2} />
                  <span className="text-[10px] font-medium leading-none mt-1">
                    {item.label}
                  </span>
                </motion.div>
                {isActive && (
                  <motion.div
                    layoutId="bottom-nav-indicator"
                    className="absolute -top-[1px] h-[3px] w-8 rounded-b-md bg-[--color-primary]"
                  />
                )}
              </>
            )}
          </NavLink>
        )
      })}
    </div>
  )
}
