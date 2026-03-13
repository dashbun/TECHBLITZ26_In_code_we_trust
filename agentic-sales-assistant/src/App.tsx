import { BrowserRouter, Routes, Route } from "react-router-dom"
import { ToastProvider } from "@/hooks/use-toast"
import { AppLayout } from "@/components/layout/AppLayout"

// Lazy load pages for now, or just import them directly since it's a small app
import { Dashboard } from "@/pages/Dashboard"
import { Inbox } from "@/pages/Inbox"
import { LeadDetails } from "@/pages/LeadDetails"
import { Outreach } from "@/pages/Outreach"
import { Pipeline } from "@/pages/Pipeline"
import { Automation } from "@/pages/Automation"
import { Notifications } from "@/pages/Notifications"

function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/inbox" element={<Inbox />} />
            <Route path="/lead/:id" element={<LeadDetails />} />
            <Route path="/outreach" element={<Outreach />} />
            <Route path="/pipeline" element={<Pipeline />} />
            <Route path="/automation" element={<Automation />} />
            <Route path="/notifications" element={<Notifications />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  )
}

export default App
