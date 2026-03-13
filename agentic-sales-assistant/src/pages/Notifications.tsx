import type { Notification } from "@/types"
import { BellRing, CheckCircle2, AlertTriangle, AlertCircle } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

const MOCK_NOTIFICATIONS: Notification[] = [
  { id: "n1", title: "Meeting Scheduled", description: "Rahul Sharma booked for Thursday 2 PM.", time: "10 mins ago", read: false, type: "success" },
  { id: "n2", title: "Hot Lead Requires Action", description: "Amit Kumar is waiting for outreach approval.", time: "1 hr ago", read: false, type: "warning" },
  { id: "n3", title: "Lead Replied", description: "Priya Patel replied to WhatsApp: Let's do it.", time: "3 hrs ago", read: true, type: "info" },
  { id: "n4", title: "AI Outreach Completed", description: "Follow-up Day 1 sequence sent to 12 leads.", time: "1 day ago", read: true, type: "info" },
]

export function Notifications() {
  return (
    <div className="p-4 pt-6 pb-20">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold tracking-tight">Alerts</h1>
        <Badge variant="secondary">{MOCK_NOTIFICATIONS.filter(n => !n.read).length} Unread</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {MOCK_NOTIFICATIONS.map(notif => {
          let Icon = BellRing
          let colorClass = "bg-primary/10 text-primary"
          if (notif.type === "success") { Icon = CheckCircle2; colorClass = "bg-[--color-success]/10 text-[--color-success]" }
          if (notif.type === "warning") { Icon = AlertTriangle; colorClass = "bg-[--color-warning]/10 text-[--color-warning]" }
          if (notif.type === "error") { Icon = AlertCircle; colorClass = "bg-[--color-danger]/10 text-[--color-danger]" }

          return (
            <Card key={notif.id} className={`transition-colors ${!notif.read ? 'bg-muted/30 border-[--color-primary]/20' : 'bg-transparent shadow-none'}`}>
              <CardContent className="p-4 flex gap-3 items-start">
                <div className={`mt-0.5 p-2 rounded-full ${colorClass}`}>
                  <Icon className="h-4 w-4" />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start mb-1">
                    <h3 className={`font-medium text-sm ${!notif.read ? 'text-foreground' : 'text-muted-foreground'}`}>{notif.title}</h3>
                    <span className="text-[10px] text-muted-foreground whitespace-nowrap">{notif.time}</span>
                  </div>
                  <p className="text-sm text-muted-foreground">{notif.description}</p>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
