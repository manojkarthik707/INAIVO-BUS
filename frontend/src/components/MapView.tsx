import { useState, useMemo } from 'react'
import mapData from './simulationMapData.json'

interface BusLocation {
  lat?: number;
  lng?: number;
  sim_x?: number;
  sim_y?: number;
}

interface EventItem {
  event_id?: string;
  event_type: string;
  severity: string;
  timestamp: string;
  location?: { latitude: number; longitude: number };
  metadata?: any;
  source?: any;
}

interface MapViewProps {
  busLocation: BusLocation | null;
  events: EventItem[];
  selectedBus?: string;
  allBuses?: Record<string, { sim_x: number; sim_y: number; speed: number }>;
}

export default function MapView({ busLocation, events, selectedBus = 'BUS_01', allBuses = {} }: MapViewProps) {
  const [zoom, setZoom] = useState<number>(1)
  const [pan, setPan] = useState<{ x: number; y: number }>({ x: 0, y: 0 })

  // Map Bounds in SUMO coordinate space
  const bounds = mapData.bounds // min_x: -9, max_x: 348, min_y: -8, max_y: 426
  const mapW = bounds.max_x - bounds.min_x + 20
  const mapH = bounds.max_y - bounds.min_y + 20

  // Coordinate mapping: SUMO coords (x: 0..340, y: 0..418, y goes UP in SUMO) -> SVG coords (y goes DOWN in SVG)
  const toSvgX = (x: number) => ((x - bounds.min_x + 10) / mapW) * 400
  const toSvgY = (y: number) => 440 - ((y - bounds.min_y + 10) / mapH) * 440

  // Convert Webots world coordinates (center roughly 0,0) to SUMO/SVG coords
  // Webots: netOffset is 175.0, 187.51
  const webotsToSvg = (wx: number, wy: number) => {
    const sumoX = wx + 175.0
    const sumoY = wy + 187.51
    return {
      x: toSvgX(sumoX),
      y: toSvgY(sumoY),
    }
  }

  // Pre-generate SVG path strings for all roads
  const roadPaths = useMemo(() => {
    return mapData.roads.map((road, idx) => {
      if (!road.points || road.points.length < 2) return null
      const d = road.points.reduce((acc, pt, pIdx) => {
        const sx = toSvgX(pt[0])
        const sy = toSvgY(pt[1])
        return pIdx === 0 ? `M ${sx} ${sy}` : `${acc} L ${sx} ${sy}`
      }, '')
      return { id: road.id, d, key: idx }
    }).filter(Boolean)
  }, [mapW, mapH])

  // Filter traffic light junctions
  const trafficLights = useMemo(() => {
    return mapData.nodes.filter(n => n.type === 'traffic_light')
  }, [])

  // Calculate current bus SVG position
  const currentBusPos = useMemo(() => {
    if (busLocation && typeof busLocation.sim_x === 'number' && typeof busLocation.sim_y === 'number') {
      return webotsToSvg(busLocation.sim_x, busLocation.sim_y)
    }
    // Fallback default position on loop
    return webotsToSvg(0, 0)
  }, [busLocation])

  return (
    <div className="relative w-full h-full bg-[#090d16] rounded-lg overflow-hidden border border-slate-700/60 shadow-inner select-none flex flex-col">
      {/* Header HUD Bar */}
      <div className="absolute top-2 left-2 z-20 flex items-center gap-2 bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-md border border-slate-700/60 text-[11px] font-mono">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span className="text-slate-300 font-bold tracking-wider">SIMULATION RADAR MAP</span>
        <span className="text-slate-500">|</span>
        <span className="text-emerald-400 font-bold">{selectedBus}</span>
      </div>

      {/* Map Control Buttons */}
      <div className="absolute top-2 right-2 z-20 flex flex-col gap-1">
        <button
          onClick={() => setZoom(z => Math.min(z + 0.3, 2.5))}
          className="w-6 h-6 bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded flex items-center justify-center text-xs font-bold transition shadow"
          title="Zoom In"
        >
          +
        </button>
        <button
          onClick={() => setZoom(z => Math.max(z - 0.3, 0.8))}
          className="w-6 h-6 bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded flex items-center justify-center text-xs font-bold transition shadow"
          title="Zoom Out"
        >
          -
        </button>
        <button
          onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }) }}
          className="w-6 h-6 bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded flex items-center justify-center text-[9px] font-mono transition shadow"
          title="Reset View"
        >
          ⟲
        </button>
      </div>

      {/* SVG Canvas Map */}
      <div className="flex-1 w-full h-full flex items-center justify-center overflow-hidden">
        <svg
          viewBox="0 0 400 440"
          className="w-full h-full object-contain transition-transform duration-200"
          style={{
            transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          }}
        >
          <defs>
            {/* Background Cyber Grid */}
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(30, 41, 59, 0.4)" strokeWidth="0.5" />
            </pattern>

            {/* Glowing filter for active bus and beacons */}
            <filter id="glow-emerald" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            <filter id="glow-alert" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Grid Background */}
          <rect width="400" height="440" fill="url(#grid)" />

          {/* Outer Highway & Main Road Base Outlines */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`base-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#1e293b"
                strokeWidth="10"
                strokeOpacity="0.9"
              />
            ))}
          </g>

          {/* Road Asphalt Fill */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`asphalt-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#0f172a"
                strokeWidth="7"
              />
            ))}
          </g>

          {/* Road Center Glowing Track Lines */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`line-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#0284c7"
                strokeWidth="1"
                strokeDasharray="3,3"
                strokeOpacity="0.6"
              />
            ))}
          </g>

          {/* Traffic Light Intersections */}
          {trafficLights.map(tl => {
            const sx = toSvgX(tl.x)
            const sy = toSvgY(tl.y)
            return (
              <g key={tl.id} transform={`translate(${sx}, ${sy})`}>
                <circle r="6" fill="none" stroke="#f59e0b" strokeWidth="1" strokeDasharray="2,2" strokeOpacity="0.7" />
                <circle r="2.5" fill="#f59e0b" />
              </g>
            )
          })}

          {/* Live Bus Markers for all detected fleet vehicles */}
          {Object.entries(allBuses).map(([id, bus]) => {
            if (id === selectedBus) return null // Handled below with special highlight
            const bPos = webotsToSvg(bus.sim_x, bus.sim_y)
            return (
              <g key={id} transform={`translate(${bPos.x}, ${bPos.y})`}>
                <circle r="4" fill="#38bdf8" fillOpacity="0.8" />
                <text x="6" y="3" fill="#94a3b8" fontSize="8" fontFamily="monospace" fontWeight="bold">
                  {id}
                </text>
              </g>
            )
          })}

          {/* Active / Selected Bus Beacon */}
          {currentBusPos && (
            <g transform={`translate(${currentBusPos.x}, ${currentBusPos.y})`} filter="url(#glow-emerald)">
              {/* Pulsing Outer Waves */}
              <circle r="12" fill="none" stroke="#10b981" strokeWidth="1" strokeOpacity="0.4" className="animate-ping" />
              <circle r="7" fill="#10b981" fillOpacity="0.25" stroke="#10b981" strokeWidth="1.5" />
              <circle r="3.5" fill="#34d399" />

              {/* Label Tag */}
              <g transform="translate(8, -8)">
                <rect x="0" y="0" width="46" height="14" rx="3" fill="#022c22" stroke="#10b981" strokeWidth="1" fillOpacity="0.9" />
                <text x="4" y="10" fill="#a7f3d0" fontSize="8" fontFamily="monospace" fontWeight="bold">
                  {selectedBus}
                </text>
              </g>
            </g>
          )}

          {/* Live Event Detection Alerts */}
          {events.slice(0, 5).map((ev, idx) => {
            // If event has metadata coordinates, use them; otherwise anchor near bus
            const evX = ev.metadata?.sim_x !== undefined ? ev.metadata.sim_x : (busLocation?.sim_x ?? 0)
            const evY = ev.metadata?.sim_y !== undefined ? ev.metadata.sim_y : (busLocation?.sim_y ?? 0)
            const evPos = webotsToSvg(evX, evY)

            return (
              <g key={ev.event_id || idx} transform={`translate(${evPos.x}, ${evPos.y})`} filter="url(#glow-alert)">
                <circle r="6" fill="#ef4444" fillOpacity="0.3" className="animate-pulse" />
                <circle r="2.5" fill="#f87171" />
              </g>
            )
          })}
        </svg>
      </div>

      {/* Footer Info HUD */}
      <div className="bg-slate-900/90 backdrop-blur border-t border-slate-800 px-3 py-1.5 flex items-center justify-between text-[10px] font-mono text-slate-400">
        <div className="flex items-center gap-3">
          <span>CITY: <strong className="text-slate-200">WEBOTS MVP GRID</strong></span>
          <span>ROADS: <strong className="text-sky-400">{mapData.roads.length} LANES</strong></span>
        </div>
        <div className="flex items-center gap-2">
          <span>FLEET: <strong className="text-emerald-400">3 ACTIVE</strong></span>
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        </div>
      </div>
    </div>
  )
}
