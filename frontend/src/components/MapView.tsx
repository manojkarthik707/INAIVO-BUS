import { useState, useMemo, useRef } from 'react';
import { Map as MapIcon, Plus, Minus, RotateCcw } from 'lucide-react';
import mapData from './simulationMapData.json';

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
  busLocation?: BusLocation | null;
  events?: EventItem[];
  selectedBus?: string;
  allBuses?: Record<string, { sim_x: number; sim_y: number; speed: number }>;
  onSelectBus?: (busId: string) => void;
}

// Default initial spawn positions
const DEFAULT_BUS_POSITIONS: Record<string, { sim_x: number; sim_y: number; speed: number }> = {
  BUS_01: { sim_x: 4.36, sim_y: 53.21, speed: 30 },
  BUS_02: { sim_x: -113.21, sim_y: 5.04, speed: 30 },
  BUS_03: { sim_x: 36.79, sim_y: -34.25, speed: 30 },
};

export default function MapView({
  selectedBus = 'BUS_01',
  allBuses = {},
  onSelectBus,
}: MapViewProps) {
  const [zoom, setZoom] = useState<number>(1);
  const [pan, setPan] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  
  const containerRef = useRef<HTMLDivElement>(null);

  // Map Bounds in SUMO coordinate space
  const bounds = mapData.bounds;
  const rangeX = bounds.max_x - bounds.min_x;
  const rangeY = bounds.max_y - bounds.min_y;

  const SVG_W = 600;
  const SVG_H = 380;
  const scaleX = (SVG_W - 40) / rangeX;
  const scaleY = (SVG_H - 40) / rangeY;
  const scale = Math.min(scaleX, scaleY);
  const offX = (SVG_W - rangeX * scale) / 2;
  const offY = (SVG_H - rangeY * scale) / 2;

  // SUMO (x, y) -> SVG (sx, sy)
  const toSvgX = (x: number) => offX + (x - bounds.min_x) * scale;
  const toSvgY = (y: number) => SVG_H - (offY + (y - bounds.min_y) * scale);

  // Webots World (wx, wy) -> SUMO -> SVG (sx, sy)
  const webotsToSvg = (wx: number, wy: number) => {
    const sumoX = wx + 175.0;
    const sumoY = wy + 187.51;
    return {
      x: toSvgX(sumoX),
      y: toSvgY(sumoY),
    };
  };

  // Pre-generate SVG road paths and junction polygons
  const { roadPaths, junctionPolys } = useMemo(() => {
    const paths: any[] = [];
    mapData.roads.forEach((road, idx) => {
      if (!road.points || road.points.length < 2) return;
      const pts = road.points.map((pt) => ({ x: toSvgX(pt[0]), y: toSvgY(pt[1]) }));
      const d = pts.reduce((acc, pt, pIdx) => {
        return pIdx === 0 ? `M ${pt.x} ${pt.y}` : `${acc} L ${pt.x} ${pt.y}`;
      }, '');
      const isLane0 = road.lane.endsWith('_0');
      paths.push({ id: road.id, lane: road.lane, d, key: idx, isLane0 });
    });

    const polys: any[] = [];
    (mapData.junctions || []).forEach((junc: any) => {
      if (!junc.points || junc.points.length < 3) return;
      const ptsStr = junc.points
        .map((pt: [number, number]) => `${toSvgX(pt[0])},${toSvgY(pt[1])}`)
        .join(' ');
      polys.push({ id: junc.id, points: ptsStr });
    });

    return { roadPaths: paths, junctionPolys: polys };
  }, []);

  // Hotspot clusters matching the visual heatmap
  const hotspots = [
    { cx: 160, cy: 150, r: 42, intensity: 'medium' }, // Anna Nagar West
    { cx: 200, cy: 190, r: 48, intensity: 'high' },   // Nungambakkam
    { cx: 285, cy: 140, r: 45, intensity: 'high' },   // Anna Nagar Central
    { cx: 350, cy: 135, r: 48, intensity: 'high' },   // T. Nagar North
    { cx: 365, cy: 195, r: 52, intensity: 'high' },   // T. Nagar Main
    { cx: 425, cy: 140, r: 40, intensity: 'medium' }, // Guindy North
    { cx: 420, cy: 230, r: 38, intensity: 'low' },    // Adyar
    { cx: 285, cy: 250, r: 35, intensity: 'low' },    // Guindy South
    { cx: 190, cy: 265, r: 32, intensity: 'medium' }, // South Link
  ];

  // Active bus markers
  const activeBuses = ['BUS_01', 'BUS_02', 'BUS_03'].map((busId) => {
    const live = allBuses[busId];
    const def = DEFAULT_BUS_POSITIONS[busId];
    const wx = live?.sim_x ?? def.sim_x;
    const wy = live?.sim_y ?? def.sim_y;
    const coords = webotsToSvg(wx, wy);
    return {
      id: busId,
      x: coords.x,
      y: coords.y,
      isSelected: busId === selectedBus,
    };
  });

  // Pan / Drag Handlers
  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setPan({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Wheel Zoom Handler
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const zoomDelta = -e.deltaY * 0.0015;
    setZoom((prev) => Math.min(4.0, Math.max(0.5, prev + zoomDelta)));
  };

  // Touch Handlers for mobile / trackpads
  const handleTouchStart = (e: React.TouchEvent) => {
    if (e.touches.length === 1) {
      setIsDragging(true);
      setDragStart({
        x: e.touches[0].clientX - pan.x,
        y: e.touches[0].clientY - pan.y,
      });
    }
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!isDragging || e.touches.length !== 1) return;
    setPan({
      x: e.touches[0].clientX - dragStart.x,
      y: e.touches[0].clientY - dragStart.y,
    });
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  const resetView = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none relative flex flex-col h-full overflow-hidden">
      {/* Header Pill */}
      <div className="absolute top-3.5 left-3.5 z-20 flex items-center gap-2 bg-white/95 px-2.5 py-1 rounded-none border border-slate-200 shadow-2xs">
        <MapIcon className="w-3.5 h-3.5 text-sky-600" />
        <span className="text-[11px] font-bold text-slate-800 uppercase tracking-wider">Road Issues Heatmap</span>
      </div>

      {/* Pan & Zoom Controls Toolbar */}
      <div className="absolute top-3.5 right-3.5 z-20 flex flex-col bg-white border border-slate-200 rounded-none shadow-2xs">
        <button
          title="Zoom In"
          onClick={() => setZoom((z) => Math.min(4.0, z + 0.25))}
          className="p-1.5 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors border-b border-slate-200"
        >
          <Plus className="w-3.5 h-3.5" />
        </button>
        <button
          title="Zoom Out"
          onClick={() => setZoom((z) => Math.max(0.5, z - 0.25))}
          className="p-1.5 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors border-b border-slate-200"
        >
          <Minus className="w-3.5 h-3.5" />
        </button>
        <button
          title="Reset View"
          onClick={resetView}
          className="p-1.5 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-colors"
        >
          <RotateCcw className="w-3 h-3" />
        </button>
      </div>

      {/* Interactive Map Canvas Container (Pan & Zoomable) */}
      <div
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onWheel={handleWheel}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        className={`flex-1 w-full h-full relative overflow-hidden bg-slate-50/50 rounded-none flex items-center justify-center ${
          isDragging ? 'cursor-grabbing' : 'cursor-grab'
        }`}
      >
        <div
          className="w-full h-full flex items-center justify-center transition-transform duration-75 ease-out origin-center"
          style={{
            transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
          }}
        >
          <svg
            viewBox={`0 0 ${SVG_W} ${SVG_H}`}
            className="w-full h-full object-contain pointer-events-none"
          >
            <defs>
              <radialGradient id="heatHigh" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#ef4444" stopOpacity="0.85" />
                <stop offset="40%" stopColor="#f97316" stopOpacity="0.65" />
                <stop offset="70%" stopColor="#eab308" stopOpacity="0.35" />
                <stop offset="100%" stopColor="#eab308" stopOpacity="0.0" />
              </radialGradient>

              <radialGradient id="heatMed" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#f97316" stopOpacity="0.75" />
                <stop offset="50%" stopColor="#eab308" stopOpacity="0.45" />
                <stop offset="100%" stopColor="#eab308" stopOpacity="0.0" />
              </radialGradient>

              <radialGradient id="heatLow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#eab308" stopOpacity="0.65" />
                <stop offset="60%" stopColor="#fde047" stopOpacity="0.30" />
                <stop offset="100%" stopColor="#fde047" stopOpacity="0.0" />
              </radialGradient>
            </defs>

            {/* Grid Background Lines (City Layout) */}
            <g stroke="#e2e8f0" strokeWidth="1" opacity="0.6">
              {Array.from({ length: 15 }).map((_, i) => (
                <line key={`v-${i}`} x1={i * 45} y1="0" x2={i * 45} y2={SVG_H} />
              ))}
              {Array.from({ length: 10 }).map((_, i) => (
                <line key={`h-${i}`} x1="0" y1={i * 40} x2={SVG_W} y2={i * 40} />
              ))}
            </g>

            {/* 1. Seamless Junction Polygons */}
            <g fill="#94a3b8" stroke="#94a3b8" strokeWidth="1" strokeLinejoin="round">
              {junctionPolys.map((j) => (
                <polygon key={j.id} points={j.points} />
              ))}
            </g>

            {/* 2. Seamless Road Asphalt Strips */}
            <g fill="none" stroke="#94a3b8" strokeWidth="7" strokeLinecap="round" strokeLinejoin="round">
              {roadPaths.map((r) => (
                <path key={r.key} d={r.d} />
              ))}
            </g>

            {/* 3. Clean Lane Divider Dashes */}
            <g fill="none" stroke="#ffffff" strokeWidth="1.2" strokeDasharray="3 3" opacity="0.9">
              {roadPaths
                .filter((r) => r.isLane0)
                .map((r) => (
                  <path key={`dash-${r.key}`} d={r.d} />
                ))}
            </g>

            {/* 4. Heatmap Glowing Halos */}
            <g>
              {hotspots.map((h, idx) => {
                const gradId = h.intensity === 'high' ? 'url(#heatHigh)' : h.intensity === 'medium' ? 'url(#heatMed)' : 'url(#heatLow)';
                return (
                  <circle
                    key={`heat-${idx}`}
                    cx={h.cx}
                    cy={h.cy}
                    r={h.r}
                    fill={gradId}
                    className="animate-pulse"
                    style={{ animationDuration: `${2.5 + (idx % 3)}s` }}
                  />
                );
              })}
            </g>

            {/* 5. Neighborhood Labels */}
            <g fill="#334155" fontSize="9" fontWeight="700" fontFamily="sans-serif" letterSpacing="0.08em">
              <text x="220" y="115" textAnchor="middle">ANNA NAGAR</text>
              <text x="240" y="150" textAnchor="middle">NUNGAMBAKKAM</text>
              <text x="280" y="175" textAnchor="middle">T. NAGAR</text>
              <text x="340" y="210" textAnchor="middle">GUINDY</text>
              <text x="390" y="235" textAnchor="middle">ADYAR</text>
            </g>

            {/* 6. Active Bus Markers (Circular badges with radar pulse) */}
            {activeBuses.map((bus) => (
              <g
                key={bus.id}
                transform={`translate(${bus.x}, ${bus.y})`}
                className="pointer-events-auto cursor-pointer transition-transform duration-300"
                onClick={() => onSelectBus && onSelectBus(bus.id)}
              >
                <circle r="10" fill="#0284c7" fillOpacity="0.25" className="animate-ping" />
                <circle
                  r="7"
                  fill={bus.isSelected ? '#0284c7' : '#0369a1'}
                  stroke="#ffffff"
                  strokeWidth="2"
                  className="drop-shadow-sm"
                />
                <circle r="2.5" fill="#ffffff" />
              </g>
            ))}
          </svg>
        </div>
      </div>

      {/* Legend Overlay */}
      <div className="absolute bottom-3.5 left-3.5 z-20 bg-white/95 border border-slate-200 rounded-none px-2.5 py-1.5 shadow-2xs space-y-1 text-[10.5px] font-medium text-slate-600">
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 bg-red-500 shrink-0"></span>
          <span>High</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 bg-orange-500 shrink-0"></span>
          <span>Medium</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 bg-yellow-400 shrink-0"></span>
          <span>Low</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-sky-600 shrink-0"></span>
          <span>Bus Active</span>
        </div>
      </div>
    </div>
  );
}
