import * as React from "react"
import { useNavigate } from "react-router-dom"
import { mockApi } from "@/services/mockApi"
import type { Lead } from "@/types"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { useToast } from "@/hooks/use-toast"

export function Inbox() {
  const [leads, setLeads] = React.useState<Lead[]>([])
  const [loading, setLoading] = React.useState(true)
  const [processing, setProcessing] = React.useState<string | null>(null)
  const { toast } = useToast()
  const navigate = useNavigate()

  React.useEffect(() => {
    mockApi.getLeads().then((data) => {
      // Show only New Leads or Contacted that need approval
      setLeads(data.filter(l => l.status === "New Lead" || l.status === "Contacted"))
      setLoading(false)
    })
  }, [])

  const handleApprove = async (e: React.MouseEvent, leadId: string) => {
    e.stopPropagation()
    setProcessing(leadId)
    try {
      await mockApi.approveOutreach(leadId)
      await mockApi.updateLeadStatus(leadId, "Interested")
      setLeads(prev => prev.filter(l => l.id !== leadId))
      toast({ title: "Agent Sent Outreach", description: "The AI agent has sent the message.", type: "success" })
    } catch (err) {
      toast({ title: "Error", description: "Failed to send outreach.", type: "destructive" })
    } finally {
      setProcessing(null)
    }
  }

  const handleReject = async (e: React.MouseEvent, leadId: string) => {
    e.stopPropagation()
    setProcessing(leadId)
    await mockApi.updateLeadStatus(leadId, "Closed") // For simplicity assume rejected -> closed
    setLeads(prev => prev.filter(l => l.id !== leadId))
    toast({ title: "Lead Rejected", description: "The lead has been dismissed." })
    setProcessing(null)
  }

  if (loading) {
    return <div className="p-4 space-y-4 animate-pulse mt-4">
      {[1, 2, 3].map(i => <div key={i} className="h-32 bg-card rounded-xl" />)}
    </div>
  }

  return (
    <div className="p-4 pt-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold tracking-tight">Agent Inbox</h1>
        <Badge variant="secondary" className="px-3 py-1 text-sm font-medium">{leads.length} New</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {leads.length === 0 && (
          <div className="text-center p-8 border rounded-xl bg-card text-muted-foreground">
            No new leads requiring action. Your agents are resting!
          </div>
        )}
        
        {leads.map((lead) => (
          <Card 
            key={lead.id} 
            className="cursor-pointer hover:border-[--color-primary] transition-colors"
            onClick={() => navigate(`/lead/${lead.id}`)}
          >
            <CardContent className="p-4">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h3 className="font-semibold text-base">{lead.name}</h3>
                  <p className="text-sm text-muted-foreground">{lead.company}</p>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <Badge variant={lead.intent === "Hot" ? "destructive" : lead.intent === "Warm" ? "warning" : "secondary"}>
                    {lead.intent}
                  </Badge>
                  <span className="text-xs text-muted-foreground">Score: <span className="font-bold text-foreground">{lead.score}</span></span>
                </div>
              </div>

              <div className="flex gap-2 mb-4">
                <Badge variant="outline" className="text-xs bg-accent text-accent-foreground border-transparent">
                  Source: {lead.source}
                </Badge>
                <div className="text-xs text-muted-foreground mt-0.5">
                  {new Date(lead.receivedAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </div>
              </div>

              <div className="flex gap-2">
                <Button 
                  className="w-full font-semibold" 
                  variant="default"
                  disabled={processing === lead.id}
                  onClick={(e) => handleApprove(e, lead.id)}
                >
                  {processing === lead.id ? "Working..." : "Approve Outreach"}
                </Button>
                <Button 
                  className="w-full" 
                  variant="outline"
                  disabled={processing === lead.id}
                  onClick={(e) => handleReject(e, lead.id)}
                >
                  Reject
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
