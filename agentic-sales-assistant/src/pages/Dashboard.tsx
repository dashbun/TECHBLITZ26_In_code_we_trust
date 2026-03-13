import * as React from "react"
import { mockApi } from "@/services/mockApi"
import type { DashboardMetrics } from "@/types"

export function Dashboard() {
  const [metrics, setMetrics] = React.useState<DashboardMetrics | null>(null)
  
  React.useEffect(() => {
    mockApi.getDashboardMetrics().then(setMetrics)
  }, [])

  return (
    <div className="p-4 pt-8">
      <h1 className="text-2xl font-bold tracking-tight mb-6">Dashboard</h1>
      {!metrics ? (
        <div className="animate-pulse flex flex-col gap-4">
          {[1,2,3].map(i => <div key={i} className="h-24 bg-card rounded-xl" />)}
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {Object.entries(metrics).map(([key, val]) => (
            <div key={key} className="bg-card border rounded-xl p-4 shadow-sm flex flex-col">
              <span className="text-muted-foreground text-xs uppercase font-semibold mb-1">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
              <span className="text-2xl font-bold">{val}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
