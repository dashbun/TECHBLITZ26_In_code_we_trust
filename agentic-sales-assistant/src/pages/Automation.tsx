import * as React from "react"
import type { FollowUpSchedule } from "@/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Edit2, PauseCircle, PlayCircle } from "lucide-react"

const MOCK_SCHEDULE: FollowUpSchedule[] = [
  { id: "s1", leadId: "l_1", dayDelay: 1, messageTitle: "Introduction & Value Prop", content: "Following up from yesterday...", status: "Completed" },
  { id: "s2", leadId: "l_1", dayDelay: 3, messageTitle: "Case Study & Social Proof", content: "Thought you might find our recent case study interesting...", status: "Pending" },
  { id: "s3", leadId: "l_1", dayDelay: 7, messageTitle: "Meeting Invite", content: "Do you have 10 mins next week...", status: "Paused" },
]

export function Automation() {
  const [schedules, setSchedules] = React.useState(MOCK_SCHEDULE)

  const toggleStatus = (id: string) => {
    setSchedules(prev => prev.map(s => {
      if (s.id === id && s.status !== "Completed") {
        return { ...s, status: s.status === "Pending" ? "Paused" : "Pending" }
      }
      return s
    }))
  }

  return (
    <div className="p-4 pt-6 pb-20">
      <h1 className="text-2xl font-bold tracking-tight mb-2">Automated Sequences</h1>
      <p className="text-muted-foreground mb-6">Manage scheduled drip communications tailored by the AI for each lead.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {schedules.map((schedule) => (
          <Card key={schedule.id} className={`border-l-4 ${schedule.status === 'Completed' ? 'border-l-[--color-success]' : schedule.status === 'Paused' ? 'border-l-[--color-warning]' : 'border-l-[--color-primary]'}`}>
            <CardContent className="p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className="px-1.5 py-0 min-w-0">Day {schedule.dayDelay}</Badge>
                    <h3 className="font-semibold text-sm truncate max-w-[150px]">{schedule.messageTitle}</h3>
                  </div>
                </div>
                <Badge variant={schedule.status === "Completed" ? "success" : schedule.status === "Paused" ? "warning" : "default"}>
                  {schedule.status}
                </Badge>
              </div>
              <p className="text-xs text-muted-foreground line-clamp-2 mt-2 mb-3 bg-muted/30 p-2 rounded">
                "{schedule.content}"
              </p>
              
              <div className="flex gap-2">
                <Button variant="outline" size="sm" className="flex-1 h-8 text-xs" onClick={() => toggleStatus(schedule.id)} disabled={schedule.status === 'Completed'}>
                  {schedule.status === "Pending" ? (
                    <><PauseCircle className="h-3 w-3 mr-1" /> Pause</>
                  ) : schedule.status === "Paused" ? (
                    <><PlayCircle className="h-3 w-3 mr-1" /> Resume</>
                  ) : "Done"}
                </Button>
                <Button variant="outline" size="sm" className="flex-1 h-8 text-xs" disabled={schedule.status === 'Completed'}>
                  <Edit2 className="h-3 w-3 mr-1" /> Edit
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
