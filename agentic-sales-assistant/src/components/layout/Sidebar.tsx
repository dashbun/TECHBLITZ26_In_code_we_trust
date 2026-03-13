import { NavLink } from "react-router-dom"
import { Home, Inbox, ListTodo, CalendarClock, Bell, LayoutDashboard } from "lucide-react"

const NAV_ITEMS = [
  { id: "dashboard", path: "/", icon: Home, label: "Home" },
  { id: "inbox", path: "/inbox", icon: Inbox, label: "Inbox" },
  { id: "pipeline", path: "/pipeline", icon: ListTodo, label: "Pipeline" },
  { id: "automation", path: "/automation", icon: CalendarClock, label: "Follow-ups" },
  { id: "notifications", path: "/notifications", icon: Bell, label: "Alerts" },
]

export function Sidebar() {
  return (
    <div className="hidden md:flex flex-col w-64 h-screen border-r bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 p-4 sticky top-0">
      <div className="flex items-center gap-2 px-2 py-4 mb-6">
        <LayoutDashboard className="h-6 w-6 text-primary" />
        <h1 className="text-xl font-bold tracking-tight">SalesAgent</h1>
      </div>
      
      <nav className="flex-1 space-y-2">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon
          return (
            <NavLink
              key={item.id}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 transition-colors ${
                  isActive 
                    ? "bg-primary text-primary-foreground font-medium" 
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                }`
              }
            >
              <Icon className="h-5 w-5" />
              <span>{item.label}</span>
            </NavLink>
          )
        })}
      </nav>
      
      <div className="mt-auto px-2 py-4">
        {/* Can add user profile or settings here later */}
        <div className="text-xs text-muted-foreground">Agentic Sales v1.0</div>
      </div>
    </div>
  )
}
