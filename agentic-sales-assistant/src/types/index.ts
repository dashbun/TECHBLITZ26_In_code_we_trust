export type LeadStatus = "New Lead" | "Contacted" | "Interested" | "Meeting Booked" | "Closed"

export interface Lead {
  id: string
  name: string
  company: string
  source: "Website" | "Instagram" | "WhatsApp" | "Email"
  score: number
  intent: "Hot" | "Warm" | "Cold"
  status: LeadStatus
  receivedAt: string
  lastActivity?: string
  aiSummary: string
  aiRationale: string
}

export interface DashboardMetrics {
  leadsToday: number
  hotLeads: number
  followUpsPending: number
  meetingsScheduled: number
  dealsClosed: number
}

export interface OutreachMessage {
  id: string
  leadId: string
  type: "Email" | "WhatsApp" | "Call Script"
  content: string
  status: "Draft" | "Sent" | "Delivered" | "Replied"
}

export interface FollowUpSchedule {
  id: string
  leadId: string
  dayDelay: number
  messageTitle: string
  content: string
  status: "Pending" | "Completed" | "Paused"
}

export interface Notification {
  id: string
  title: string
  description: string
  time: string
  read: boolean
  type: "info" | "success" | "warning" | "error"
}
