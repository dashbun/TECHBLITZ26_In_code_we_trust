import * as React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Bot, X, Send } from "lucide-react"

export function AIChatPanel() {
  const [open, setOpen] = React.useState(false)
  const [input, setInput] = React.useState("")
  const [messages, setMessages] = React.useState([
    { role: "agent", content: "Hi! I'm your Sales Agent. Want to see hot leads or schedule a follow-up?" }
  ])

  const [simulating, setSimulating] = React.useState(false)

  const handleSend = () => {
    if (!input.trim()) return
    setMessages(prev => [...prev, { role: "user", content: input }])
    setInput("")
    setSimulating(true)

    setTimeout(() => {
      setMessages(prev => [...prev, { role: "agent", content: "I've processed your request. 4 hot leads have been queued for next steps. Would you like me to draft their emails?" }])
      setSimulating(false)
    }, 1500)
  }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-20 right-4 z-40 bg-[--color-primary] text-white p-4 rounded-full shadow-2xl hover:scale-105 transition-transform"
      >
        <Bot className="h-6 w-6" />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ y: "100%", opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: "100%", opacity: 0 }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed inset-x-0 bottom-0 z-[60] h-[75vh] bg-background border-t rounded-t-2xl shadow-2xl flex flex-col"
          >
            <div className="p-4 border-b flex justify-between items-center bg-muted/30 rounded-t-2xl">
              <div className="flex items-center space-x-2">
                <div className="bg-[--color-primary]/10 p-2 rounded-full text-[--color-primary]">
                  <Bot className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-sm">AI Sales Agent</h3>
                  <p className="text-xs text-muted-foreground flex items-center">
                    <span className="w-2 h-2 rounded-full bg-green-500 mr-1.5 animate-pulse"></span> Online
                  </p>
                </div>
              </div>
              <button onClick={() => setOpen(false)} className="p-2 bg-muted rounded-full hover:bg-muted-foreground/20">
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] rounded-2xl p-3 text-sm ${
                    m.role === 'user' 
                      ? 'bg-[--color-primary] text-white rounded-br-none' 
                      : 'bg-muted rounded-bl-none text-foreground border border-border/50'
                  }`}>
                    {m.content}
                  </div>
                </div>
              ))}
              {simulating && (
                <div className="flex justify-start">
                  <div className="bg-muted rounded-2xl rounded-bl-none p-3 border border-border/50 flex space-x-1.5 items-center">
                    <span className="w-2 h-2 bg-muted-foreground/40 rounded-full animate-bounce"></span>
                    <span className="w-2 h-2 bg-muted-foreground/60 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-2 h-2 bg-muted-foreground/80 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                </div>
              )}
            </div>

            <div className="p-3 bg-background border-t pb-safe">
              <div className="flex items-center relative">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask agent to filter leads..."
                  className="w-full bg-muted border-none rounded-full pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-[--color-primary]/50"
                  type="text"
                />
                <button 
                  onClick={handleSend}
                  disabled={!input.trim() || simulating}
                  className="absolute right-1 text-white bg-[--color-primary] p-2 rounded-full disabled:opacity-50"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={() => setOpen(false)}
          className="fixed inset-0 bg-black/40 z-50 pointer-events-auto"
        />
      )}
    </>
  )
}
