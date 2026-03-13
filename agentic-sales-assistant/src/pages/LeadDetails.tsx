import * as React from "react"
import { useParams, useNavigate } from "react-router-dom"
import { mockApi } from "@/services/mockApi"
import type { Lead } from "@/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowLeft, Sparkles, MessageSquare, Phone } from "lucide-react"

export function LeadDetails() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [lead, setLead] = React.useState<Lead | null>(null)
  
  React.useEffect(() => {
    if (id) {
      mockApi.getLeadById(id).then(setLead).catch(() => navigate('/inbox'))
    }
  }, [id, navigate])

  if (!lead) return <div className="p-4 animate-pulse"><div className="h-64 bg-card rounded-xl"></div></div>

  return (
    <div className="p-4 pt-6 pb-20">
      <Button variant="ghost" size="sm" onClick={() => navigate(-1)} className="mb-4 -ml-2 text-muted-foreground">
        <ArrowLeft className="h-4 w-4 mr-1" /> Back
      </Button>

      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">{lead.name}</h1>
        <p className="text-lg text-muted-foreground">{lead.company}</p>
        <div className="flex flex-wrap gap-2 mt-3">
          <Badge variant={lead.intent === "Hot" ? "destructive" : "secondary"}>{lead.intent} Intent</Badge>
          <Badge variant="outline">Score: {lead.score}</Badge>
          <Badge variant="outline">Source: {lead.source}</Badge>
        </div>
      </div>

      <div className="space-y-4">
        {/* AI Summary Section */}
        <Card className="border-indigo-100 bg-indigo-50/50 dark:bg-indigo-900/10 dark:border-indigo-900">
          <CardHeader className="pb-2 pt-4 px-4">
            <CardTitle className="text-sm font-semibold flex items-center text-indigo-700 dark:text-indigo-400">
              <Sparkles className="h-4 w-4 mr-2" />
              AI Sales Agent Analysis
            </CardTitle>
          </CardHeader>
          <CardContent className="px-4 pb-4">
            <p className="text-sm font-medium mb-2">{lead.aiSummary}</p>
            <div className="bg-white dark:bg-black/20 p-3 rounded-md border border-indigo-100 dark:border-indigo-900 text-sm italic">
              <span className="font-semibold not-italic block mb-1 text-xs text-muted-foreground">Why this lead is valuable:</span>
              "{lead.aiRationale}"
            </div>
          </CardContent>
        </Card>

        {/* Action Shortcuts */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <Button variant="outline" className="h-20 flex-col gap-2 bg-card">
            <MessageSquare className="h-5 w-5 text-green-600" />
            <span>Draft WhatsApp</span>
          </Button>
          <Button variant="outline" className="h-20 flex-col gap-2 bg-card">
            <Phone className="h-5 w-5 text-indigo-600" />
            <span>Call Script</span>
          </Button>
        </div>

        {/* Activity Timeline */}
        <h3 className="text-lg font-semibold mt-6 mb-3">Activity Timeline</h3>
        <div className="pl-4 border-l-2 border-muted space-y-6 relative">
          <div className="relative">
            <div className="absolute -left-[21px] top-1 h-3 w-3 rounded-full bg-[--color-primary] border-2 border-background" />
            <p className="text-sm font-semibold">Ready for Outreach</p>
            <p className="text-xs text-muted-foreground">Pending your approval</p>
          </div>
          <div className="relative">
            <div className="absolute -left-[21px] top-1 h-3 w-3 rounded-full bg-muted border-2 border-background" />
            <p className="text-sm font-medium">Research Completed</p>
            <p className="text-xs text-muted-foreground">AI Agent finished analysis</p>
          </div>
          <div className="relative">
            <div className="absolute -left-[21px] top-1 h-3 w-3 rounded-full bg-muted border-2 border-background" />
            <p className="text-sm font-medium">Lead Captured</p>
            <p className="text-xs text-muted-foreground">via {lead.source}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
