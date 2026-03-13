import type { Lead, DashboardMetrics, LeadStatus } from "@/types"

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

const MOCK_LEADS: Lead[] = [
  {
    id: "l_1",
    name: "Rahul Sharma",
    company: "TechNova Solutions",
    source: "Website",
    score: 95,
    intent: "Hot",
    status: "New Lead",
    receivedAt: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
    aiSummary: "CTO of a mid-size tech agency looking for automation tools.",
    aiRationale: "High budget indicated, visited pricing page 4 times today.",
  },
  {
    id: "l_2",
    name: "Priya Patel",
    company: "DesignGrid",
    source: "Instagram",
    score: 72,
    intent: "Warm",
    status: "Contacted",
    receivedAt: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
    lastActivity: "Sent intro WhatsApp",
    aiSummary: "Freelance agency owner needing CRM.",
    aiRationale: "Engaged with our IG ad, but hasn't replied to first message.",
  },
  {
    id: "l_3",
    name: "Amit Kumar",
    company: "BuildFast Inc",
    source: "WhatsApp",
    score: 88,
    intent: "Hot",
    status: "Interested",
    receivedAt: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    lastActivity: "Replied interested",
    aiSummary: "Operations Manager seeking workflow optimizations.",
    aiRationale: "Explicitly asked for a demo on WhatsApp.",
  },
]

export const mockApi = {
  async getDashboardMetrics(): Promise<DashboardMetrics> {
    await delay(600)
    return {
      leadsToday: 12,
      hotLeads: 4,
      followUpsPending: 8,
      meetingsScheduled: 3,
      dealsClosed: 1,
    }
  },

  async getLeads(): Promise<Lead[]> {
    await delay(800)
    return [...MOCK_LEADS]
  },

  async getLeadById(id: string): Promise<Lead> {
    await delay(500)
    const lead = MOCK_LEADS.find((l) => l.id === id)
    if (!lead) throw new Error("Lead not found")
    return lead
  },

  async approveOutreach(leadId: string): Promise<{ success: boolean; message: string }> {
    await delay(1200)
    console.log(`Outreach approved for ${leadId}`)
    return { success: true, message: "Outreach sent successfully by AI Agent" }
  },

  async updateLeadStatus(leadId: string, status: LeadStatus): Promise<{ success: boolean }> {
    await delay(500)
    console.log(`Updated lead ${leadId} to ${status}`)
    return { success: true }
  },
}
