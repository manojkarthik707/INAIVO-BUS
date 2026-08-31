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

  // Map Bounds in SUMO coordinate space (min_x: -9.07, max_x: 348.07, min_y: -8.06, max_y: 426.58)
  const bounds = mapData.bounds
  const rangeX = bounds.max_x - bounds.min_x
  const rangeY = bounds.max_y - bounds.min_y

  // Exact Aspect-Ratio Preserving SVG Coordinate Transformation
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

  // Filter traffic light intersections
  const trafficLights = useMemo(() => {
    return mapData.nodes.filter(n => n.type === 'traffic_light')
  }, [])

  // Calculate current bus position in SVG coordinates
  const currentBusPos = useMemo(() => {
    if (busLocation && typeof busLocation.sim_x === 'number' && typeof busLocation.sim_y === 'number') {
      return webotsToSvg(busLocation.sim_x, busLocation.sim_y)
    }
    if (allBuses[selectedBus] && typeof allBuses[selectedBus].sim_x === 'number') {
      return webotsToSvg(allBuses[selectedBus].sim_x, allBuses[selectedBus].sim_y)
    }
    return null
  }, [busLocation, allBuses, selectedBus])

  return (
    <div className="relative w-full h-full bg-[#080d1a] rounded-xl overflow-hidden border border-slate-700/70 shadow-2xl select-none flex flex-col group">
      {/* Top HUD Header */}
      <div className="absolute top-2.5 left-2.5 z-20 flex items-center gap-2 bg-slate-900/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-700/70 text-xs font-mono shadow-lg">
        <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.8)]"></div>
        <span className="text-slate-200 font-bold tracking-wider">LIVE SIMULATION RADAR</span>
        <span className="text-slate-600">|</span>
        <span className="text-emerald-400 font-extrabold">{selectedBus}</span>
        {busLocation?.sim_x !== undefined && (
          <span className="text-slate-400 text-[10px] hidden sm:inline">
            [{Math.round(busLocation.sim_x)}m, {Math.round(busLocation.sim_y ?? 0)}m]
          </span>
        )}
      </div>

      {/* Top Right Controls */}
      <div className="absolute top-2.5 right-2.5 z-20 flex items-center gap-1.5 bg-slate-900/80 backdrop-blur-md p-1 rounded-lg border border-slate-700/60 shadow-lg">
        <button
          onClick={() => setZoom(z => Math.min(z + 0.3, 3.0))}
          className="w-7 h-7 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded flex items-center justify-center text-sm font-bold transition active:scale-95"
          title="Zoom In"
        >
          +
        </button>
        <button
          onClick={() => setZoom(z => Math.max(z - 0.3, 0.7))}
          className="w-7 h-7 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded flex items-center justify-center text-sm font-bold transition active:scale-95"
          title="Zoom Out"
        >
          -
        </button>
        <button
          onClick={() => { setZoom(1); setPan({ x: 0, y: 0 }) }}
          className="w-7 h-7 bg-slate-800 hover:bg-slate-700 text-emerald-400 rounded flex items-center justify-center text-xs font-mono transition active:scale-95"
          title="Reset View / Fit Map"
        >
          ⟲
        </button>
      </div>

      {/* SVG Canvas Map */}
      <div className="flex-1 w-full h-full flex items-center justify-center overflow-hidden p-2">
        <svg
          viewBox={`0 0 ${SVG_W} ${SVG_H}`}
          className="w-full h-full object-contain transition-transform duration-300"
          style={{
            transform: `scale(${zoom}) translate(${pan.x}px, ${pan.y}px)`,
          }}
        >
          <defs>
            {/* Cyber Radar Background Grid */}
            <pattern id="radar-grid" width="25" height="25" patternUnits="userSpaceOnUse">
              <path d="M 25 0 L 0 0 0 25" fill="none" stroke="rgba(30, 41, 59, 0.5)" strokeWidth="0.5" />
            </pattern>

            {/* Glowing filter for active bus beacon */}
            <filter id="bus-beacon-glow" x="-100%" y="-100%" width="300%" height="300%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>

            {/* Glowing filter for AI incident pins */}
            <filter id="incident-glow" x="-100%" y="-100%" width="300%" height="300%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* Background Grid */}
          <rect width={SVG_W} height={SVG_H} fill="url(#radar-grid)" />

          {/* Road Outer Base Outline / Curbs */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`base-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#1e293b"
                strokeWidth="12"
                strokeOpacity="0.95"
              />
            ))}
          </g>

          {/* Road Asphalt Dark Surface */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`asphalt-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#0b1329"
                strokeWidth="8.5"
              />
            ))}
          </g>

          {/* Road Center Lane Track Line */}
          <g strokeLinecap="round" strokeLinejoin="round">
            {roadPaths.map(r => r && (
              <path
                key={`line-${r.key}`}
                d={r.d}
                fill="none"
                stroke="#0284c7"
                strokeWidth="1.2"
                strokeDasharray="4,4"
                strokeOpacity="0.75"
              />
            ))}
          </g>

          {/* Traffic Light Intersections */}
          {trafficLights.map(tl => {
            const sx = toSvgX(tl.x)
            const sy = toSvgY(tl.y)
            return (
              <g key={tl.id} transform={`translate(${sx}, ${sy})`}>
                <circle r="8" fill="none" stroke="#f59e0b" strokeWidth="1" strokeDasharray="3,3" strokeOpacity="0.6" />
                <circle r="3" fill="#f59e0b" />
                <circle r="1" fill="#fff" />
              </g>
            )
          })}

          {/* All Other Fleet Buses (BUS_02, BUS_03) */}
          {Object.entries(allBuses).map(([id, bus]) => {
            if (id === selectedBus) return null // Rendered with primary beacon below
            const bPos = webotsToSvg(bus.sim_x, bus.sim_y)
            return (
              <g key={id} transform={`translate(${bPos.x}, ${bPos.y})`}>
                <circle r="6" fill="#0284c7" fillOpacity="0.4" stroke="#38bdf8" strokeWidth="1.5" />
                <circle r="3" fill="#38bdf8" />
                <g transform="translate(8, -6)">
                  <rect x="0" y="0" width="38" height="12" rx="2" fill="#0f172a" stroke="#38bdf8" strokeWidth="0.8" fillOpacity="0.85" />
                  <text x="3" y="9" fill="#93c5fd" fontSize="7.5" fontFamily="monospace" fontWeight="bold">
                    {id}
                  </text>
                </g>
              </g>
            )
          })}

          {/* Primary Selected Bus Beacon (BUS_01) */}
          {currentBusPos && (
            <g transform={`translate(${currentBusPos.x}, ${currentBusPos.y})`} filter="url(#bus-beacon-glow)">
              {/* Pulsing Radar Ring */}
              <circle r="16" fill="none" stroke="#10b981" strokeWidth="1.2" strokeOpacity="0.3" className="animate-ping" />
              <circle r="9" fill="#10b981" fillOpacity="0.25" stroke="#10b981" strokeWidth="2" />
              <circle r="4.5" fill="#34d399" />
              <circle r="1.5" fill="#ffffff" />

              {/* High-Visibility Fleet Badge */}
              <g transform="translate(10, -10)">
                <rect x="0" y="0" width="52" height="16" rx="4" fill="#022c22" stroke="#10b981" strokeWidth="1.2" fillOpacity="0.95" />
                <text x="5" y="11" fill="#6ee7b7" fontSize="9" fontFamily="monospace" fontWeight="extrabold">
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
                <circle r="8" fill="#ef4444" fillOpacity="0.3" className="animate-pulse" />
                <circle r="3.5" fill="#ef4444" stroke="#ffffff" strokeWidth="1" />
                <g transform="translate(6, -8)">
                  <rect x="0" y="0" width="60" height="13" rx="2" fill="#450a0a" stroke="#ef4444" strokeWidth="0.8" fillOpacity="0.9" />
                  <text x="3" y="9.5" fill="#fca5a5" fontSize="7.5" fontFamily="monospace" fontWeight="bold">
                    ⚠️ {ev.event_type.replace('_DETECTED', '')}
                  </text>
                </g>
              </g>
            )
          })}
        </svg>
      </div>

      {/* Bottom Telemetry HUD */}
      <div className="bg-slate-900/95 backdrop-blur border-t border-slate-800/80 px-3.5 py-2 flex items-center justify-between text-[11px] font-mono text-slate-400">
        <div className="flex items-center gap-4">
          <span>GRID: <strong className="text-slate-200">340m × 418m</strong></span>
          <span>ROADS: <strong className="text-sky-400">{mapData.roads.length} LANES</strong></span>
          <span>SIGNALS: <strong className="text-amber-400">{trafficLights.length} TLS</strong></span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="text-emerald-400 font-bold">RADAR SYNC ACTIVE</span>
        </div>
      </div>
    </div>
  )
}
