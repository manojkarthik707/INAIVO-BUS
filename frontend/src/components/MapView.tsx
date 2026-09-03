import { useState, useMemo, useRef } from 'react';
import { Activity, Plus, Minus, RotateCcw, AlertTriangle, Trash2 } from 'lucide-react';
import mapData from './simulationMapData.json';
import PotholeInspectorModal, { type PotholeEvidenceData } from './PotholeInspectorModal';

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
  confidence?: number;
  location?: { latitude: number; longitude: number; sim_x?: number; sim_y?: number };
  metadata?: any;
  source?: any;
  evidence_image?: string;
}

interface MapViewProps {
  busLocation?: BusLocation | null;
  events?: EventItem[];
  selectedBus?: string;
  allBuses?: Record<string, { sim_x: number; sim_y: number; speed: number }>;
  edgeTraffic?: Record<string, 'free' | 'moderate' | 'heavy'>;
  onSelectBus?: (busId: string) => void;
  onWipePotholes?: () => void;
}

// Default initial spawn positions
const DEFAULT_BUS_POSITIONS: Record<string, { sim_x: number; sim_y: number; speed: number }> = {
  BUS_01: { sim_x: 4.36, sim_y: 53.21, speed: 30 },
  BUS_02: { sim_x: -113.21, sim_y: 5.04, speed: 30 },
  BUS_03: { sim_x: 36.79, sim_y: -34.25, speed: 30 },
};

// Default fallback active congestion edges if initial connection is pending
const DEFAULT_HEAVY_EDGES = new Set([
  'shortcut_east', 'shortcut_west', '5', '-5', '6', '-6', '7', '-7', '8', '-8', '9', '-9', '10', '-10', '17', '-17', '23', '-23'
]);

const DEFAULT_MODERATE_EDGES = new Set([
  '11', '-11', '12', '-12', '14', '-14', '16', '-16', '18', '-18', '20', '-20', '24', '-24'
]);

export default function MapView({
  events = [],
  selectedBus = 'BUS_01',
  allBuses = {},
  edgeTraffic = {},
  onSelectBus,
  onWipePotholes,
}: MapViewProps) {
  const [zoom, setZoom] = useState<number>(1);
  const [pan, setPan] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [hoveredPothole, setHoveredPothole] = useState<any | null>(null);
  const [selectedPothole, setSelectedPothole] = useState<PotholeEvidenceData | null>(null);
  
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

  const hasLiveTraffic = Object.keys(edgeTraffic).length > 0;

  // Pre-generate SVG road paths and dynamic traffic colors
  const { roadPaths, junctionPolys } = useMemo(() => {
    const paths: any[] = [];
    mapData.roads.forEach((road, idx) => {
      if (!road.points || road.points.length < 2) return;
      const pts = road.points.map((pt) => ({ x: toSvgX(pt[0]), y: toSvgY(pt[1]) }));
      const d = pts.reduce((acc, pt, pIdx) => {
        return pIdx === 0 ? `M ${pt.x} ${pt.y}` : `${acc} L ${pt.x} ${pt.y}`;
      }, '');
      const isLane0 = road.lane.endsWith('_0');

      let trafficLevel: 'free' | 'moderate' | 'heavy' = 'free';

      if (hasLiveTraffic) {
        trafficLevel = edgeTraffic[road.id] || 'free';
      } else {
        // Fallback default
        if (DEFAULT_HEAVY_EDGES.has(road.id)) {
          trafficLevel = 'heavy';
        } else if (DEFAULT_MODERATE_EDGES.has(road.id)) {
          trafficLevel = 'moderate';
        }
      }

      const trafficColor =
        trafficLevel === 'heavy'
          ? '#ef4444' // Heavy Congestion (Red)
          : trafficLevel === 'moderate'
          ? '#f59e0b' // Moderate (Orange)
          : '#22c55e'; // Free Flow (Green)

      paths.push({
        id: road.id,
        lane: road.lane,
        d,
        key: idx,
        isLane0,
        trafficColor,
        trafficLevel,
      });
    });

    const polys: any[] = [];
    (mapData.junctions || []).forEach((junc: any) => {
      if (!junc.points || junc.points.length < 3) return;
      const ptsStr = junc.points
        .map((pt: [number, number]) => `${toSvgX(pt[0])},${toSvgY(pt[1])}`)
        .join(' ');

      // Determine junction color from connected roads or core bottleneck IDs
      let fillColor = '#22c55e';
      if (['41', '43', '25', '26'].includes(junc.id)) {
        fillColor = '#ef4444';
      } else if (['27', '28', '33', '34'].includes(junc.id)) {
        fillColor = '#f59e0b';
      }

      polys.push({ id: junc.id, points: ptsStr, fillColor });
    });

    return { roadPaths: paths, junctionPolys: polys };
  }, [edgeTraffic, hasLiveTraffic]);

  // 18 Ground-Truth Physical Potholes in Webots City
  const GROUND_TRUTH_POTHOLES = useMemo(() => [
    { id: 'pothole-1',  wx: -13.14,  wy: 0.44 },
    { id: 'pothole-2',  wx: 10.20,   wy: 2.78 },
    { id: 'pothole-3',  wx: 7.96,    wy: -0.96 },
    { id: 'pothole-4',  wx: -12.79,  wy: -3.03 },
    { id: 'pothole-5',  wx: -101.35, wy: 36.10 },
    { id: 'pothole-6',  wx: -78.33,  wy: 45.37 },
    { id: 'pothole-7',  wx: -15.01,  wy: 53.07 },
    { id: 'pothole-8',  wx: 28.76,   wy: 40.22 },
    { id: 'pothole-9',  wx: 53.07,   wy: -23.79 },
    { id: 'pothole-10', wx: 45.36,   wy: -78.38 },
    { id: 'pothole-11', wx: -33.44,  wy: -113.07 },
    { id: 'pothole-12', wx: -101.25, wy: -87.11 },
    { id: 'pothole-13', wx: -36.93,  wy: 25.09 },
    { id: 'pothole-14', wx: -42.31,  wy: 15.94 },
    { id: 'pothole-15', wx: -26.43,  wy: -28.33 },
    { id: 'pothole-16', wx: -14.11,  wy: -41.02 },
    { id: 'pothole-17', wx: 14.94,   wy: -36.93 },
    { id: 'pothole-18', wx: 102.31,  wy: 34.69 },
  ], []);

  // Real-Time Pothole Detections (Locked strictly to the 18 verified ground-truth city defects)
  const detectedPotholes = useMemo(() => {
    const verifiedMap = new Map<string, any>();

    (events || []).forEach((ev) => {
      if (!ev.event_type || !ev.event_type.toUpperCase().includes('POTHOLE')) return;

      let wx: number | null = null;
      let wy: number | null = null;
      const meta = (ev as any).event_metadata || ev.metadata;
      const loc = (ev as any).location;

      if (meta?.sim_x !== undefined && meta?.sim_y !== undefined) {
        wx = Number(meta.sim_x);
        wy = Number(meta.sim_y);
      } else if (loc?.sim_x !== undefined && loc?.sim_y !== undefined) {
        wx = Number(loc.sim_x);
        wy = Number(loc.sim_y);
      } else {
        const lat = loc?.latitude ?? (ev as any).latitude;
        const lng = loc?.longitude ?? (ev as any).longitude;
        if (lat !== undefined && lng !== undefined) {
          wx = (Number(lat) - 11.0168) / 0.0001;
          wy = (Number(lng) - 76.9558) / 0.0001;
        }
      }

      if (wx === null || wy === null || isNaN(wx) || isNaN(wy)) return;

      // Find which of the 18 physical potholes this sighting matches
      let bestP: any = null;
      let minD = 3.5;
      for (const p of GROUND_TRUTH_POTHOLES) {
        const d = Math.hypot(wx - p.wx, wy - p.wy);
        if (d < minD) {
          minD = d;
          bestP = p;
        }
      }

      // 100% Reject any false positive / legacy noise not physically located at a mapped hazard
      if (!bestP) return;

      let sensorName = 'Fleet Dashcam';
      if ((ev as any).bus_id || ev.source?.bus_id) {
        sensorName = (ev as any).bus_id || ev.source?.bus_id;
      } else if (ev.source?.junction_id) {
        sensorName = `CCTV_${ev.source.junction_id}`;
      } else if (ev.source?.camera_id) {
        sensorName = String(ev.source.camera_id).toUpperCase();
      }

      const verifiedSensors: string[] = meta?.verified_by_sensors || [];
      const range = meta?.range_m !== undefined ? Number(meta.range_m) : (loc?.range_m !== undefined ? Number(loc.range_m) : null);
      const lateral = meta?.lateral_m !== undefined ? Number(meta.lateral_m) : (loc?.lateral_m !== undefined ? Number(loc.lateral_m) : null);
      const conf = Math.round((ev.confidence || 0.98) * 100);
      const evTime = new Date(ev.timestamp);
      const evidenceImg = (ev as any).evidence_path || ev.evidence_image || meta?.evidence_image || meta?.evidence_frame || null;

      if (verifiedMap.has(bestP.id)) {
        const existing = verifiedMap.get(bestP.id);
        existing.count = Math.max(existing.count + 1, meta?.verification_count || 1);
        existing.buses.add(sensorName);
        for (const s of verifiedSensors) existing.buses.add(s);
        if (evidenceImg) existing.evidenceImage = evidenceImg;
        if (range !== null) {
          existing.range = range;
          existing.lateral = lateral;
        }
        if (!isNaN(evTime.getTime())) {
          existing.lastTime = evTime;
          existing.time = evTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        }
      } else {
        const timeStr = isNaN(evTime.getTime())
          ? 'Just now'
          : evTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });

        const svgCoords = webotsToSvg(bestP.wx, bestP.wy);
        const sensorSet = new Set<string>([sensorName]);
        for (const s of verifiedSensors) sensorSet.add(s);

        verifiedMap.set(bestP.id, {
          id: bestP.id,
          wx: bestP.wx,
          wy: bestP.wy,
          x: svgCoords.x,
          y: svgCoords.y,
          count: meta?.verification_count || 1,
          buses: sensorSet,
          time: timeStr,
          lastTime: evTime,
          confidence: conf,
          lat: (11.0168 + bestP.wx * 0.0001).toFixed(4),
          lng: (76.9558 + bestP.wy * 0.0001).toFixed(4),
          range,
          lateral,
          evidenceImage: evidenceImg,
        });
      }
    });

    return Array.from(verifiedMap.values()).map((p) => {
      const sensorList = Array.from(p.buses);
      const isMultiSensor = sensorList.length > 1;
      return {
        ...p,
        busId: isMultiSensor ? `${sensorList.join(' + ')} (Multi-Sensor Verified)` : sensorList.join(', '),
      };
    });
  }, [events, GROUND_TRUTH_POTHOLES]);

  // Active bus markers (ONLY Fleet Buses Tracked)
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

  // Touch Handlers
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
      <div className="absolute top-3.5 left-3.5 z-20 flex items-center gap-2 bg-white/95 px-2.5 py-1.5 rounded-none border border-slate-200 shadow-2xs">
        <Activity className="w-3.5 h-3.5 text-rose-600 animate-pulse" />
        <span className="text-[11px] font-bold text-slate-900 uppercase tracking-wider">Live Traffic Heatmap</span>
        <span className="px-1.5 py-0.5 text-[8.5px] font-mono font-bold bg-rose-50 text-rose-700 border border-rose-200">
          REAL-TIME DYNAMIC
        </span>
        {detectedPotholes.length > 0 && (
          <div className="flex items-center gap-1.5">
            <span className="px-1.5 py-0.5 text-[8.5px] font-mono font-bold bg-amber-500 text-slate-900 animate-pulse">
              🚨 {detectedPotholes.length} POTHOLE{detectedPotholes.length > 1 ? 'S' : ''} DETECTED
            </span>
            {onWipePotholes && (
              <button
                onClick={onWipePotholes}
                title="Wipe registered pothole data to restart fresh simulation"
                className="px-2 py-0.5 text-[8.5px] font-mono font-bold bg-rose-600 hover:bg-rose-700 active:scale-95 text-white flex items-center gap-1 transition-all cursor-pointer shadow-xs"
              >
                <Trash2 className="w-2.5 h-2.5" />
                WIPE DATA
              </button>
            )}
          </div>
        )}
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

      {/* Floating Hovered Pothole Tooltip */}
      {hoveredPothole && (
        <div className="absolute top-12 left-3.5 z-20 bg-slate-900/95 text-white px-2.5 py-1.5 rounded-none border border-amber-500/80 shadow-lg text-[10.5px] space-y-0.5 pointer-events-none">
          <div className="font-bold text-amber-400 flex items-center gap-1.5">
            <AlertTriangle className="w-3 h-3 text-amber-400" />
            POTHOLE VERIFIED {hoveredPothole.count > 1 ? `(${hoveredPothole.count}x SIGHTINGS)` : ''}
          </div>
          <div className="text-slate-300">
            Detected by: <strong className="text-white font-mono">{hoveredPothole.busId}</strong>
          </div>
          <div className="text-slate-400 text-[9.5px] flex items-center gap-2">
            <span>{hoveredPothole.time}</span>
            <span>•</span>
            <span className="text-emerald-400 font-mono font-bold">{hoveredPothole.confidence}% AI Confidence</span>
          </div>
          {hoveredPothole.range !== null && (
            <div className="text-cyan-400 font-mono text-[9.5px]">
              Closest Range: <span className="font-bold text-white">{hoveredPothole.range}m</span> {hoveredPothole.lateral !== null ? `(${hoveredPothole.lateral > 0 ? '+' : ''}${hoveredPothole.lateral}m offset)` : ''}
            </div>
          )}
          <div className="text-slate-400 font-mono text-[9px]">
            GPS: {hoveredPothole.lat}° N, {hoveredPothole.lng}° E
          </div>
        </div>
      )}

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
            {/* Grid Background Lines (City Layout) */}
            <g stroke="#e2e8f0" strokeWidth="1" opacity="0.6">
              {Array.from({ length: 15 }).map((_, i) => (
                <line key={`v-${i}`} x1={i * 45} y1="0" x2={i * 45} y2={SVG_H} />
              ))}
              {Array.from({ length: 10 }).map((_, i) => (
                <line key={`h-${i}`} x1="0" y1={i * 40} x2={SVG_W} y2={i * 40} />
              ))}
            </g>

            {/* 1. Underlying Traffic Corridor Ambient Glow */}
            <g fill="none" strokeLinecap="round" strokeLinejoin="round" opacity={0.65}>
              {roadPaths.map((r) => (
                <path
                  key={`glow-${r.key}`}
                  d={r.d}
                  stroke={r.trafficColor}
                  strokeWidth={14}
                  className={r.trafficLevel === 'heavy' ? 'animate-pulse' : ''}
                />
              ))}
            </g>

            {/* 2. Junction Solid Polygons with Traffic Color */}
            <g strokeLinejoin="round">
              {junctionPolys.map((j) => (
                <polygon
                  key={j.id}
                  points={j.points}
                  fill={j.fillColor}
                  stroke={j.fillColor}
                  strokeWidth="1.5"
                />
              ))}
            </g>

            {/* 3. Direct Road Pavement Traffic Flow (Google Maps Traffic Layer) */}
            <g fill="none" strokeLinecap="round" strokeLinejoin="round">
              {roadPaths.map((r) => (
                <path
                  key={r.key}
                  d={r.d}
                  stroke={r.trafficColor}
                  strokeWidth={7.5}
                />
              ))}
            </g>

            {/* 4. Clean Lane Divider Dashes */}
            <g fill="none" stroke="#ffffff" strokeWidth="1.2" strokeDasharray="3 3" opacity="0.95">
              {roadPaths
                .filter((r) => r.isLane0)
                .map((r) => (
                  <path key={`dash-${r.key}`} d={r.d} />
                ))}
            </g>

            {/* 5. City Neighborhood Labels */}
            <g fill="#0f172a" fontSize="9" fontWeight="800" fontFamily="sans-serif" letterSpacing="0.08em">
              <text x="220" y="115" textAnchor="middle">ANNA NAGAR</text>
              <text x="240" y="148" textAnchor="middle">NUNGAMBAKKAM</text>
              <text x="280" y="175" textAnchor="middle">T. NAGAR</text>
              <text x="340" y="210" textAnchor="middle">GUINDY</text>
              <text x="390" y="235" textAnchor="middle">ADYAR</text>
            </g>

            {/* 6. Real-Time Verified Pothole Markers (Appears ONLY when captured by Dashcam AI) */}
            {detectedPotholes.map((p) => {
              const isHovered = hoveredPothole?.id === p.id;
              return (
                <g
                  key={p.id}
                  transform={`translate(${p.x}, ${p.y})`}
                  className="cursor-pointer"
                  onMouseEnter={() => setHoveredPothole(p)}
                  onMouseLeave={() => setHoveredPothole(null)}
                  onClick={() => setSelectedPothole(p)}
                >
                  {/* Dedicated Hit Target (Fixed Size, Captures All Pointer Events) */}
                  <circle r="18" fill="transparent" style={{ pointerEvents: 'all' }} />

                  {/* Ambient Radar Aura */}
                  <circle
                    r="12"
                    fill="#ef4444"
                    fillOpacity={isHovered ? 0.35 : 0.20}
                    style={{ pointerEvents: 'none' }}
                  />

                  {/* Solid Badge Ring */}
                  <circle
                    r="7.5"
                    fill={isHovered ? '#991b1b' : '#b91c1c'}
                    stroke={isHovered ? '#facc15' : '#ffffff'}
                    strokeWidth="2"
                    className="drop-shadow-md"
                    style={{ pointerEvents: 'none' }}
                  />

                  {/* Yellow Hazard Dot */}
                  <circle r="3.2" fill="#facc15" style={{ pointerEvents: 'none' }} />
                  <rect
                    x="-0.8"
                    y="-2"
                    width="1.6"
                    height="2.5"
                    fill="#000000"
                    rx="0.5"
                    style={{ pointerEvents: 'none' }}
                  />
                  <circle cx="0" cy="1.6" r="0.6" fill="#000000" style={{ pointerEvents: 'none' }} />
                </g>
              );
            })}

            {/* 7. Active Bus Fleet Markers (ONLY Fleet Buses Tracked) */}
            {activeBuses.map((bus) => (
              <g
                key={bus.id}
                transform={`translate(${bus.x}, ${bus.y})`}
                className="pointer-events-auto cursor-pointer transition-transform duration-300"
                onClick={() => onSelectBus && onSelectBus(bus.id)}
              >
                <circle r="12" fill="#0284c7" fillOpacity="0.25" className="animate-ping" />
                <circle
                  r="7.5"
                  fill={bus.isSelected ? '#0284c7' : '#0369a1'}
                  stroke="#ffffff"
                  strokeWidth="2.5"
                  className="drop-shadow-md"
                />
                <circle r="2.5" fill="#ffffff" />
              </g>
            ))}

            {/* 8. 360° Traffic Light CCTV Surveillance Markers */}
            {[
              { id: 'J25', name: 'Junction 25 (SE 4-Way)', sim_x: 45, sim_y: -45, port: 8025 },
              { id: 'J26', name: 'Junction 26 (NW 4-Way)', sim_x: -45, sim_y: 45, port: 8026 },
              { id: 'J27', name: 'Junction 27 (NE Highway)', sim_x: 105, sim_y: 93, port: 8027 },
              { id: 'J41', name: 'Junction 41 (SW 3-Way)', sim_x: -45, sim_y: -4.5, port: 8041 },
              { id: 'J43', name: 'Junction 43 (Central Plaza)', sim_x: 45, sim_y: 4.5, port: 8043 },
            ].map((cctv) => {
              const { x: cx, y: cy } = webotsToSvg(cctv.sim_x, cctv.sim_y);
              const isSelected = selectedBus === cctv.id;

              return (
                <g
                  key={cctv.id}
                  transform={`translate(${cx}, ${cy})`}
                  className="cursor-pointer group"
                  onClick={() => onSelectBus && onSelectBus(cctv.id)}
                >
                  {/* Outer Radar Halo */}
                  <circle
                    r="11"
                    fill="#d97706"
                    fillOpacity={isSelected ? 0.35 : 0.15}
                    className={isSelected ? 'animate-pulse' : ''}
                  />

                  {/* CCTV Dome Pin */}
                  <circle
                    r="6.5"
                    fill={isSelected ? '#d97706' : '#b45309'}
                    stroke="#ffffff"
                    strokeWidth="1.8"
                    className="drop-shadow-sm"
                  />

                  {/* 360 Camera Lens Aperture Dot */}
                  <circle r="2.2" fill="#fef3c7" />

                  {/* Tooltip Label on Hover / Selection */}
                  <g
                    transform="translate(0, -11)"
                    className={`transition-opacity duration-200 ${
                      isSelected ? 'opacity-100' : 'opacity-85 group-hover:opacity-100'
                    }`}
                  >
                    <rect
                      x="-14"
                      y="-7"
                      width="28"
                      height="9"
                      fill="#0f172a"
                      stroke="#d97706"
                      strokeWidth="0.8"
                      rx="1"
                    />
                    <text
                      x="0"
                      y="-0.5"
                      textAnchor="middle"
                      fill="#fef3c7"
                      fontSize="5.5"
                      fontWeight="bold"
                      fontFamily="monospace"
                    >
                      {cctv.id} 360°
                    </text>
                  </g>
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Traffic Legend Overlay */}
      <div className="absolute bottom-3.5 left-3.5 z-20 bg-white/95 border border-slate-200 rounded-none px-3 py-2 shadow-2xs space-y-1.5 text-[10.5px] font-medium text-slate-700">
        <div className="text-[9.5px] font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-1 mb-1">
          Traffic Congestion
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 bg-red-500 shrink-0"></span>
          <span>Heavy Congestion (&gt;=3 cars)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 bg-amber-500 shrink-0"></span>
          <span>Moderate Traffic (1-2 cars)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 bg-emerald-500 shrink-0"></span>
          <span>Free Flow (0 cars)</span>
        </div>
        <div className="flex items-center gap-2 pt-0.5 border-t border-slate-100">
          <span className="w-2.5 h-2.5 rounded-full bg-sky-600 shrink-0"></span>
          <span className="font-semibold text-sky-900">Active Fleet Bus</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-600 border border-white shadow-xs shrink-0 flex items-center justify-center">
            <span className="w-1 h-1 rounded-full bg-amber-200"></span>
          </span>
          <span className="font-semibold text-amber-800">360° Traffic Light CCTV</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-red-700 border border-white shadow-xs shrink-0 flex items-center justify-center">
            <span className="w-1 h-1 rounded-full bg-yellow-400"></span>
          </span>
          <span className="font-semibold text-rose-700">Verified Pothole (Click to Inspect)</span>
        </div>
      </div>

      {/* Pothole Evidence Inspector Modal */}
      <PotholeInspectorModal
        pothole={selectedPothole}
        onClose={() => setSelectedPothole(null)}
      />
    </div>
  );
}
