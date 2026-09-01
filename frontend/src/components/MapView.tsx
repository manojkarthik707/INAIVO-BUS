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

// Default initial spawn positions on the road loop (so radar never defaults to empty 0,0)
const DEFAULT_BUS_POSITIONS: Record<string, { sim_x: number; sim_y: number; speed: number }> = {
  'BUS_01': { sim_x: 4.36, sim_y: 53.21, speed: 30 },
  'BUS_02': { sim_x: -113.21, sim_y: 5.04, speed: 30 },
  'BUS_03': { sim_x: 36.79, sim_y: -34.25, speed: 30 },
}

export default function MapView({ busLocation, events, selectedBus = 'BUS_01', allBuses = {} }: MapViewProps) {
  const [zoom, setZoom] = useState<number>(1)
  const [pan, setPan] = useState<{ x: number; y: number }>({ x: 0, y: 0 })

  // Map Bounds in SUMO coordinate space (min_x: -9.07, max_x: 348.07, min_y: -8.06, max_y: 426.58)
  const bounds = mapData.bounds
  const rangeX = bounds.max_x - bounds.min_x
  const rangeY = bounds.max_y - bounds.min_y

  // Aspect-Ratio Preserving SVG Coordinate Transformation
  const SVG_W = 400
  const SVG_H = 480
  const scaleX = (SVG_W - 30) / rangeX
  const scaleY = (SVG_H - 30) / rangeY
  const scale = Math.min(scaleX, scaleY)
  const offX = (SVG_W - rangeX * scale) / 2
  const offY = (SVG_H - rangeY * scale) / 2

  // SUMO (x, y) -> SVG (sx, sy)
  const toSvgX = (x: number) => offX + (x - bounds.min_x) * scale
  const toSvgY = (y: number) => SVG_H - (offY + (y - bounds.min_y) * scale)

  // Webots World (wx, wy) -> SUMO -> SVG (sx, sy)
  // Webots netOffset is: netOffset="175.00,187.51"
  const webotsToSvg = (wx: number, wy: number) => {
    const sumoX = wx + 175.0
    const sumoY = wy + 187.51
    return {
      x: toSvgX(sumoX),
      y: toSvgY(sumoY),
      sumoX,
      sumoY,
    }
  }

  // Pre-generate SVG road paths from simulationMapData.json
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
  }, [rangeX, rangeY])

  // Merge live fleet positions with defaults
  const activeFleet = useMemo(() => {
    return {
      ...DEFAULT_BUS_POSITIONS,
      ...allBuses,
    }
  }, [allBuses])

  // Calculate current selected bus position in SVG coordinates
  const currentBusPos = useMemo(() => {
    if (busLocation && typeof busLocation.sim_x === 'number' && typeof busLocation.sim_y === 'number') {
      return webotsToSvg(busLocation.sim_x, busLocation.sim_y)
    }
    if (activeFleet[selectedBus] && typeof activeFleet[selectedBus].sim_x === 'number') {
      return webotsToSvg(activeFleet[selectedBus].sim_x, activeFleet[selectedBus].sim_y)
    }
    const def = DEFAULT_BUS_POSITIONS[selectedBus] || DEFAULT_BUS_POSITIONS['BUS_01']
    return webotsToSvg(def.sim_x, def.sim_y)
  }, [busLocation, activeFleet, selectedBus])

  return (
    <div className="relative w-full h-full bg-[#242f3e] rounded-xl overflow-hidden border border-slate-800 shadow-xl select-none flex flex-col group">
      {/* Top HUD Header - Dark Theme */}
      <div className="absolute top-2 left-2 z-20 flex items-center gap-1.5 bg-[#1b2431]/95 backdrop-blur-md px-2.5 py-1 rounded-md border border-[#2c3847] text-[11px] font-mono shadow-sm">
        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_6px_rgba(16,185,129,0.8)]"></div>
        <span className="text-slate-200 font-bold tracking-wider">RADAR MAP</span>
        <span className="text-slate-300">|</span>
        <span className="text-emerald-600 font-extrabold">{selectedBus}</span>
        {busLocation?.sim_x !== undefined && (
          <span className="text-slate-500 text-[10px] hidden sm:inline font-mono">
            [{Math.round(busLocation.sim_x)}m, {Math.round(busLocation.sim_y ?? 0)}m]
          </span>
        )}
      </div>

      {/* Top Right Controls - Dark Theme */}
      <div className="absolute top-2 right-2 z-20 flex items-center gap-1 bg-[#1b2431]/95 backdrop-blur-md p-0.5 rounded-md border border-[#2c3847] shadow-sm">
        <button
          onClick={() => setZoom(z => Math.min(z + 0.3, 3.0))}
          className="w-6 h-6 bg-[#242f3e] hover:bg-[#2c3847] text-slate-300 border border-[#38414e] rounded flex items-center justify-center text-xs font-bold transition active:scale-95 shadow-xs"
          title="Zoom In"
        >
          +
        </button>
        <button
          onClick={() => setZoom(z => Math.max(z - 0.3, 0.7))}
          className="w-6 h-6 bg-[#242f3e] hover:bg-[#2c3847] text-slate-300 border border-[#38414e] rounded flex items-center justify-center text-xs font-bold transition active:scale-95 shadow-xs"
          title="Zoom Out"
        >
          -
        </button>
        <button
          onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }) }}
          className="w-7 h-7 bg-[#242f3e] hover:bg-[#2c3847] text-emerald-500 border border-[#38414e] rounded flex items-center justify-center text-xs font-mono transition active:scale-95 shadow-sm"
          title="Reset View / Fit Map"
        >
          ⟲
        </button>
      </div>

      {/* SVG Canvas Map - Google Maps Dark Theme */}
      <div className="flex-1 w-full h-full flex items-center justify-center overflow-hidden p-2">
        <svg
          viewBox={`0 0 ${SVG_W} ${SVG_H}`}
          className="w-full h-full object-contain transition-transform duration-300"
          style={{
            transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          }}
        >
          <defs>

            {/* Glowing filter for active bus beacon */}
            <filter id="bus-beacon-glow" x="-100%" y="-100%" width="300%" height="300%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            {/* Glowing filter for AI incident pins */}
            <filter id="incident-glow" x="-100%" y="-100%" width="300%" height="300%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Solid Google Maps Dark Background */}
          <rect width={SVG_W} height={SVG_H} fill="#242f3e" />

          {/* Road Outer Border / Curb */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`base-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#2c3847"
                strokeWidth="11"
              />
            ))}
          </g>

          {/* Road Asphalt (Google Maps dark mode style) */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`asphalt-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#38414e"
                strokeWidth="9"
              />
            ))}
          </g>

          {/* Very Subtle Center Line (No dashes) */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`line-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#424c5a"
                strokeWidth="0.8"
                strokeOpacity="0.8"
              />
            ))}
          </g>


          {/* All Other Fleet Buses (BUS_02, BUS_03) */}
          {Object.entries(activeFleet).map(([id, bus]) => {
            if (id === selectedBus) return null // Rendered with primary beacon below
            const bPos = webotsToSvg(bus.sim_x, bus.sim_y)
            return (
              <g key={id} transform={`translate(${bPos.x}, ${bPos.y})`}>
                <circle r="6" fill="#3b82f6" fillOpacity="0.3" stroke="#2563eb" strokeWidth="1.5" />
                <circle r="3.5" fill="#2563eb" />
                <circle r="1" fill="#ffffff" />
                <g transform="translate(8, -6)">
                  <rect x="0" y="0" width="40" height="13" rx="2" fill="#1e3a8a" stroke="#3b82f6" strokeWidth="0.8" fillOpacity="0.95" />
                  <text x="3" y="9.5" fill="#ffffff" fontSize="8" fontFamily="monospace" fontWeight="bold">
                    {id}
                  </text>
                </g>
              </g>
            )
          })}

          {/* Primary Selected Bus Beacon (e.g. BUS_01 / BUS_03) */}
          {currentBusPos && (
            <g transform={`translate(${currentBusPos.x}, ${currentBusPos.y})`} filter="url(#bus-beacon-glow)">
              {/* Pulsing Radar Wave */}
              <circle r="16" fill="none" stroke="#059669" strokeWidth="1.5" strokeOpacity="0.4" className="animate-ping" />
              <circle r="9.5" fill="#10b981" fillOpacity="0.3" stroke="#059669" strokeWidth="2" />
              <circle r="5" fill="#059669" />
              <circle r="1.8" fill="#ffffff" />

              {/* High-Visibility Fleet Badge */}
              <g transform="translate(10, -10)">
                <rect x="0" y="0" width="54" height="17" rx="4" fill="#047857" stroke="#065f46" strokeWidth="1.2" fillOpacity="0.98" />
                <text x="5" y="12" fill="#ffffff" fontSize="9" fontFamily="monospace" fontWeight="extrabold">
                  {selectedBus}
                </text>
              </g>
            </g>
          )}

          {/* AI Hazard / Incident Event Markers */}
          {events.slice(0, 6).map((ev, idx) => {
            const evX = ev.metadata?.sim_x !== undefined ? ev.metadata.sim_x : (busLocation?.sim_x ?? 0)
            const evY = ev.metadata?.sim_y !== undefined ? ev.metadata.sim_y : (busLocation?.sim_y ?? 0)
            const evPos = webotsToSvg(evX, evY)

            return (
              <g key={ev.event_id || idx} transform={`translate(${evPos.x}, ${evPos.y})`} filter="url(#incident-glow)">
                <circle r="8" fill="#ef4444" fillOpacity="0.4" className="animate-pulse" />
                <circle r="4" fill="#dc2626" stroke="#ffffff" strokeWidth="1.2" />
                <g transform="translate(6, -8)">
                  <rect x="0" y="0" width="62" height="14" rx="2" fill="#991b1b" stroke="#dc2626" strokeWidth="0.8" fillOpacity="0.95" />
                  <text x="3" y="10" fill="#ffffff" fontSize="8" fontFamily="monospace" fontWeight="bold">
                    ⚠️ {ev.event_type.replace('_DETECTED', '')}
                  </text>
                </g>
              </g>
            )
          })}
        </svg>
      </div>

      {/* Bottom Telemetry HUD - Dark Theme */}
      <div className="bg-[#1b2431]/95 backdrop-blur border-t border-[#2c3847] px-2.5 py-1 flex items-center justify-between text-[10px] font-mono text-slate-400 shadow-sm shrink-0">
        <div className="flex items-center gap-3">
          <span>GRID: <strong className="text-slate-300">340m×418m</strong></span>
          <span>ROADS: <strong className="text-sky-400">{mapData.roads.length} LANES</strong></span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-emerald-500 font-bold">LIVE RADAR</span>
        </div>
      </div>
    </div>
  )
}
