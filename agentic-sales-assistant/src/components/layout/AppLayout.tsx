import { Outlet } from "react-router-dom"
import { BottomNav } from "./BottomNav"
import { Sidebar } from "./Sidebar"
import { Toaster } from "@/components/ui/toaster"
import { AIChatPanel } from "./AIChatPanel"

export function AppLayout() {
  return (
    <div className="flex min-h-screen w-full bg-background relative">
      <Sidebar />
      <div className="flex flex-1 flex-col relative overflow-hidden">
        <main className="flex-1 overflow-y-auto pb-20 md:pb-0 scrollbar-hide">
          <Outlet />
        </main>
        <AIChatPanel />
      </div>
      <BottomNav />
      <Toaster />
    </div>
  )
}
