import * as React from "react"
import { mockApi } from "@/services/mockApi"
import type { Lead } from "@/types"
import { Badge } from "@/components/ui/badge"

const STAGES = ["New Lead", "Contacted", "Interested", "Meeting Booked", "Closed"] as const

export function Pipeline() {
  const [leads, setLeads] = React.useState<Lead[]>([])

  React.useEffect(() => {
    mockApi.getLeads().then(setLeads)
  }, [])

  return (
    <div className="flex h-full flex-col pt-6 pb-20">
      <div className="px-4 mb-4">
        <h1 className="text-2xl font-bold tracking-tight">Sales Pipeline</h1>
        <p className="text-muted-foreground text-sm">Drag to manually update stages</p>
      </div>

      <div className="flex-1 overflow-x-auto overflow-y-hidden px-4 pb-4 snap-x">
        <div className="flex gap-4 h-full snap-mandatory">
          {STAGES.map((stage) => {
            const stageLeads = leads.filter(l => l.status === stage)
            return (
              <div key={stage} className="min-w-[280px] snap-center shrink-0 flex flex-col h-full bg-muted/20 border rounded-xl overflow-hidden">
                <div className="p-3 bg-muted/50 border-b flex justify-between items-center">
                  <h3 className="font-semibold text-sm">{stage}</h3>
                  <Badge variant="secondary" className="text-xs bg-background">{stageLeads.length}</Badge>
                </div>
                
                <div className="p-3 overflow-y-auto flex-1 space-y-3">
                  {stageLeads.length === 0 ? (
                    <div className="text-xs text-center text-muted-foreground italic p-4 border border-dashed rounded-lg bg-transparent">
                      Empty stage
                    </div>
                  ) : (
                    stageLeads.map(lead => (
                      <div key={lead.id} className="bg-card p-3 rounded-lg shadow-sm border border-border/60 hover:border-[--color-primary] cursor-grab active:cursor-grabbing transition-colors">
                        <div className="flex justify-between items-start mb-2">
                          <p className="font-medium text-sm leading-tight max-w-[130px] truncate">{lead.name}</p>
                          <Badge variant={lead.intent === "Hot" ? "destructive" : "secondary"} className="text-[10px] px-1.5 py-0 min-w-0">Score {lead.score}</Badge>
                        </div>
                        <p className="text-xs text-muted-foreground truncate">{lead.company}</p>
                        <div className="mt-3 flex items-center justify-between">
                          <span className="text-[10px] bg-accent text-accent-foreground px-1.5 py-0.5 rounded-full">{lead.source}</span>
                          {lead.lastActivity && <span className="text-[10px] text-muted-foreground truncate max-w-[100px]">{lead.lastActivity}</span>}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
