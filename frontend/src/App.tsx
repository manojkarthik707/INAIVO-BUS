import { useEffect, useState } from 'react'
import MapView from './components/MapView'
import EventStream from './components/EventStream'
import ScenarioController from './components/ScenarioController'

interface EventData {
  event_id: string;
  event_type: string;
  severity: string;
  timestamp: string;
  confidence: number;
  location: { latitude: number; longitude: number };
  source: any;
}

function App() {
  const [events, setEvents] = useState<EventData[]>([])
  const [busLocation, setBusLocation] = useState<{lat: number, lng: number} | null>(null)
  const [cameraFrames, setCameraFrames] = useState<Record<string, string>>({})
  const [selectedBus, setSelectedBus] = useState<string>('BUS_01')

  useEffect(() => {
    // Connect to WebSocket using IPv4 to avoid Windows localhost delays
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/events')
    
    ws.onmessage = (message) => {
      try {
        const data = JSON.parse(message.data)
        if (data.type === 'TELEMETRY') {
          if (data.bus_id === selectedBus) {
            setBusLocation({ lat: data.latitude, lng: data.longitude })
          }
          if (data.frame) {
            setCameraFrames(prev => ({ ...prev, [data.bus_id]: data.frame }))
          }
        } else if (data.event_type) {
          setEvents(prev => [data, ...prev].slice(0, 50))
        }
      } catch (err) {
        console.error("WS error:", err)
      }
    }

    return () => {
      ws.close()
    }
  }, [selectedBus])

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-4 font-sans">
      <header className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            Urban Intelligence Command Center
          </h1>
          <p className="text-slate-400 font-light">SIH26124 - AI-Powered Mobile Urban Intelligence Platform</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="text-emerald-400 font-semibold tracking-wider">SYSTEM ONLINE</span>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[85vh]">
        {/* Main Column: Cinematic Live Camera */}
        <div className="lg:col-span-2 bg-black rounded-xl overflow-hidden border border-slate-700 shadow-2xl relative flex flex-col group">
          
          <div className="absolute top-4 left-4 z-50 flex gap-3">
            {['BUS_01', 'BUS_02', 'BUS_03'].map(busId => (
              <button 
                key={busId}
                onClick={() => setSelectedBus(busId)}
                className={`px-4 py-2 rounded-full border flex items-center gap-2 backdrop-blur-md transition-colors ${
                  selectedBus === busId 
                    ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]' 
                    : 'bg-black/60 border-slate-700/50 text-slate-400 hover:text-slate-200'
                }`}
              >
                <div className={`w-2 h-2 rounded-full ${selectedBus === busId ? 'bg-red-500 animate-pulse' : 'bg-slate-600'}`}></div>
                <span className="font-mono text-sm tracking-widest">{busId} : LIVE</span>
              </button>
            ))}
          </div>

          <div className="absolute bottom-4 right-4 z-50 bg-black/60 backdrop-blur-md px-4 py-2 rounded-lg border border-slate-700/50">
             <span className="font-mono text-emerald-400">YOLOv11 SENSOR ARRAY ACTIVE</span>
          </div>

          <div className="flex-1 relative w-full h-full bg-slate-900 overflow-hidden flex items-center justify-center">
            <div className="relative w-full h-full transition-transform duration-1000 group-hover:scale-[1.02]">
              {cameraFrames[selectedBus] ? (
                <img 
                  src={`data:image/jpeg;base64,${cameraFrames[selectedBus]}`}
                  className="w-full h-full object-fill"
                  alt={`Live ${selectedBus} Camera`}
                />
              ) : (
                <div className="flex flex-col items-center justify-center h-full gap-4">
                  <div className="w-12 h-12 border-4 border-slate-600 border-t-emerald-500 rounded-full animate-spin"></div>
                  <span className="text-slate-500 font-mono tracking-widest">INITIALIZING {selectedBus} FEED...</span>
                </div>
              )}

              {/* Render actual AI bounding boxes */}
              {events.filter(e => e.source?.bus_id === selectedBus && Date.now() - new Date(e.timestamp).getTime() < 1000).map((event, idx) => {
                if (!event.metadata || !event.metadata.bbox) return null;
                const [x1, y1, x2, y2] = event.metadata.bbox;
                const x_pct = (x1 / 640) * 100;
                const y_pct = (y1 / 360) * 100;
                const w_pct = ((x2 - x1) / 640) * 100;
                const h_pct = ((y2 - y1) / 360) * 100;
                
                return (
                  <div 
                    key={event.event_id || idx}
                    className="absolute border-2 border-emerald-400 bg-emerald-400/10 shadow-[0_0_15px_rgba(52,211,153,0.4)] flex flex-col justify-end overflow-hidden transition-all duration-75"
                    style={{
                      left: `${x_pct}%`,
                      top: `${y_pct}%`,
                      width: `${w_pct}%`,
                      height: `${h_pct}%`
                    }}
                  >
                    <div className="bg-emerald-400 text-slate-900 font-mono text-[10px] sm:text-xs px-1 py-0.5 uppercase tracking-wider font-bold truncate">
                      🎯 {event.event_type.replace('_DETECTED', '')} {Math.round(event.confidence * 100)}%
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right Column: Controls & Events */}
        <div className="flex flex-col gap-6 h-full overflow-hidden">
          <div className="bg-slate-800/80 backdrop-blur-md rounded-xl p-5 border border-slate-700 shadow-xl shrink-0">
            <ScenarioController />
          </div>
          
          <div className="bg-slate-800/80 backdrop-blur-md rounded-xl p-5 border border-slate-700 shadow-xl flex-1 flex flex-col overflow-hidden">
            <h2 className="text-lg font-semibold mb-4 text-emerald-400 tracking-wider flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              LIVE EVENT STREAM
            </h2>
            <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
              <EventStream events={events} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
