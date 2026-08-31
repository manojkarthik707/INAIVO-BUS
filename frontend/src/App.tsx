import { useEffect, useState, useRef } from 'react'
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
  metadata?: any;
}

// camera_streamer serves MJPEG on: BUS_01→8011, BUS_02→8012, BUS_03→8013
const MJPEG_PORT: Record<string, number> = {
  'BUS_01': 8011,
  'BUS_02': 8012,
  'BUS_03': 8013,
}

function App() {
  const [events, setEvents] = useState<EventData[]>([])
  const [busLocation, setBusLocation] = useState<{lat?: number, lng?: number, sim_x?: number, sim_y?: number} | null>(null)
  const [allBuses, setAllBuses] = useState<Record<string, { sim_x: number; sim_y: number; speed: number }>>({})
  const [selectedBus, setSelectedBus] = useState<string>('BUS_01')
  const [streamReady, setStreamReady] = useState(false)
  const imgRef = useRef<HTMLImageElement>(null)

  // WebSocket for telemetry & events only (no video frames needed)
  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/events')
    ws.onmessage = (message) => {
      try {
        const data = JSON.parse(message.data)
        if (data.type === 'TELEMETRY') {
          if (data.bus_id) {
            setAllBuses(prev => ({
              ...prev,
              [data.bus_id]: {
                sim_x: data.sim_x ?? 0,
                sim_y: data.sim_y ?? 0,
                speed: data.speed ?? 0
              }
            }))
          }
          if (data.bus_id === selectedBus) {
            setBusLocation({
              lat: data.latitude,
              lng: data.longitude,
              sim_x: data.sim_x,
              sim_y: data.sim_y
            })
          }
        } else if (data.event_type) {
          setEvents(prev => [data, ...prev].slice(0, 50))
        }
      } catch (err) {
        console.error('WS parse error:', err)
      }
    }
    return () => ws.close()
  }, [selectedBus])

  // Instant sync when switching selected bus
  useEffect(() => {
    if (allBuses[selectedBus]) {
      setBusLocation({
        sim_x: allBuses[selectedBus].sim_x,
        sim_y: allBuses[selectedBus].sim_y,
      })
    }
  }, [selectedBus, allBuses])

  // Reset stream-ready state when switching cameras
  useEffect(() => {
    setStreamReady(false)
  }, [selectedBus])

  const streamUrl = `http://127.0.0.1:${MJPEG_PORT[selectedBus]}/`

  return (
    <div className="h-screen max-h-screen overflow-hidden flex flex-col p-3 bg-slate-950 text-slate-100 font-sans select-none">
      {/* Header Bar */}
      <header className="h-8 shrink-0 mb-2 flex items-center justify-between border-b border-slate-800/80 pb-1.5 px-1">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-teal-300 to-emerald-400 tracking-tight">
            Urban Intelligence Command Center
          </h1>
          <span className="hidden md:inline-block text-[11px] text-slate-400 font-medium tracking-wide">
            SIH26124 • Mobile Urban Intelligence
          </span>
        </div>
        <div className="flex items-center gap-2 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <span className="text-emerald-400 font-mono text-[11px] font-bold tracking-wider">SYSTEM ONLINE</span>
        </div>
      </header>

      {/* Main 2-Column Dashboard Grid */}
      <div className="flex-1 min-h-0 grid grid-cols-12 gap-3">
        {/* Left Column: Dashcam & YOLOv11 Visuals (8 cols) */}
        <div className="col-span-12 lg:col-span-7 xl:col-span-8 bg-black rounded-xl overflow-hidden border border-slate-800 shadow-2xl relative flex flex-col min-h-0">
          
          {/* Bus selector tabs */}
          <div className="absolute top-3 left-3 z-30 flex gap-2">
            {['BUS_01', 'BUS_02', 'BUS_03'].map(busId => (
              <button 
                key={busId}
                onClick={() => setSelectedBus(busId)}
                className={`px-3 py-1 rounded-full border flex items-center gap-1.5 backdrop-blur-md transition-all text-xs font-mono font-bold ${
                  selectedBus === busId 
                    ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300 shadow-[0_0_12px_rgba(16,185,129,0.35)]' 
                    : 'bg-slate-900/80 border-slate-700 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                }`}
              >
                <div className={`w-1.5 h-1.5 rounded-full ${selectedBus === busId ? 'bg-emerald-400 animate-pulse' : 'bg-slate-500'}`}></div>
                <span>{busId}</span>
              </button>
            ))}
          </div>

          {/* Video Container (Centers feed smoothly) */}
          <div className="relative flex-1 min-h-0 bg-slate-950 flex items-center justify-center overflow-hidden">
            {!streamReady && (
              <div className="absolute inset-0 flex flex-col items-center justify-center gap-2.5 bg-slate-950/90 backdrop-blur-sm z-10">
                <div className="w-8 h-8 border-3 border-slate-700 border-t-emerald-400 rounded-full animate-spin"></div>
                <span className="text-slate-400 font-mono text-[11px] tracking-wider">CONNECTING {selectedBus} LIVE STREAM...</span>
              </div>
            )}

            {/* Live MJPEG Stream directly from internal Webots camera controller */}
            <img
              ref={imgRef}
              src={streamUrl}
              alt={`${selectedBus} Live Feed`}
              className={`max-w-full max-h-full object-contain select-none transition-opacity duration-300 ${streamReady ? 'opacity-100' : 'opacity-0'}`}
              onLoad={() => setStreamReady(true)}
              onError={() => setStreamReady(false)}
            />

            {/* AI bounding boxes overlay */}
            {events
              .filter(e => e.source?.bus_id === selectedBus && Date.now() - new Date(e.timestamp).getTime() < 1000)
              .map((event, idx) => {
                if (!event.metadata?.bbox) return null;
                const [x1, y1, x2, y2] = event.metadata.bbox;
                return (
                  <div 
                    key={event.event_id || idx}
                    className="absolute border-2 border-emerald-400 bg-emerald-400/15 shadow-[0_0_15px_rgba(52,211,153,0.4)] flex flex-col justify-end overflow-hidden transition-all duration-75 pointer-events-none"
                    style={{
                      left:   `${(x1 / 1280) * 100}%`,
                      top:    `${(y1 / 720) * 100}%`,
                      width:  `${((x2 - x1) / 1280) * 100}%`,
                      height: `${((y2 - y1) / 720) * 100}%`,
                    }}
                  >
                    <div className="bg-emerald-400 text-slate-950 font-mono text-[9px] px-1 py-0.5 uppercase tracking-wider font-bold truncate">
                      🎯 {event.event_type.replace('_DETECTED', '')} {Math.round(event.confidence * 100)}%
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        {/* Right Column: Controls, Large Map & Live Event Feed (4-5 cols) */}
        <div className="col-span-12 lg:col-span-5 xl:col-span-4 flex flex-col gap-2 h-full min-h-0 overflow-hidden">
          {/* 1. Simulator Control Strip */}
          <div className="bg-slate-900/90 backdrop-blur-md rounded-xl p-2.5 border border-slate-800 shadow-lg shrink-0">
            <ScenarioController />
          </div>

          {/* 2. White Theme Simulation Radar Map */}
          <div className="bg-slate-900/90 backdrop-blur-md rounded-xl p-1.5 border border-slate-800 shadow-lg flex-1 min-h-0 overflow-hidden">
            <MapView busLocation={busLocation} events={events} selectedBus={selectedBus} allBuses={allBuses} />
          </div>
          
          {/* 3. Live AI Event Stream */}
          <div className="bg-slate-900/90 backdrop-blur-md rounded-xl p-2 border border-slate-800 shadow-lg h-32 shrink-0 flex flex-col overflow-hidden">
            <h2 className="text-[11px] font-bold mb-1 text-emerald-400 tracking-wider flex items-center gap-1.5 uppercase">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
              Live Event Stream
            </h2>
            <div className="flex-1 min-h-0 overflow-y-auto pr-1 custom-scrollbar">
              <EventStream events={events} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
