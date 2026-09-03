import React, { useEffect, useRef, useState, useCallback } from 'react';
import {
  Compass,
  RotateCcw,
  ZoomIn,
  ZoomOut,
  Play,
  Pause,
  ChevronLeft,
  ChevronRight,
  Crosshair,
} from 'lucide-react';

interface Interactive360ViewerProps {
  streamUrl: string;
  cameraName: string;
  junctionId: string;
}

export default function Interactive360Viewer({
  streamUrl,
  cameraName,
  junctionId,
}: Interactive360ViewerProps) {
  const [headingDeg, setHeadingDeg] = useState<number>(0);
  const [zoomLevel, setZoomLevel] = useState<number>(1.0);
  const [isPatrolling, setIsPatrolling] = useState<boolean>(false);
  const [streamLoaded, setStreamLoaded] = useState<boolean>(false);
  const [isDragging, setIsDragging] = useState<boolean>(false);

  const dragStartRef = useRef<{ startX: number; startHeading: number } | null>(null);
  const lastCommandTimeRef = useRef<number>(0);
  const headingRef = useRef<number>(0);
  headingRef.current = headingDeg;

  // Send real-time motorized PTZ command to the Webots camera controller
  const sendPtzCommand = useCallback((pan: number, patrol?: boolean) => {
    try {
      const url = new URL(streamUrl);
      const patrolParam = patrol !== undefined ? `&patrol=${patrol ? 1 : 0}` : '';
      const ptzUrl = `${url.protocol}//${url.hostname}:${url.port}/ptz?pan=${Math.round(pan)}${patrolParam}`;
      fetch(ptzUrl).catch(() => {});
    } catch {
      // ignore
    }
  }, [streamUrl]);

  // Helper to calculate cardinal direction text
  const getCardinalDirection = (deg: number) => {
    const normalized = ((deg % 360) + 360) % 360;
    if (normalized >= 337.5 || normalized < 22.5) return 'NORTH (0°)';
    if (normalized >= 22.5 && normalized < 67.5) return 'NORTH-EAST (45°)';
    if (normalized >= 67.5 && normalized < 112.5) return 'EAST (90°)';
    if (normalized >= 112.5 && normalized < 157.5) return 'SOUTH-EAST (135°)';
    if (normalized >= 157.5 && normalized < 202.5) return 'SOUTH (180°)';
    if (normalized >= 202.5 && normalized < 247.5) return 'SOUTH-WEST (225°)';
    if (normalized >= 247.5 && normalized < 292.5) return 'WEST (270°)';
    return 'NORTH-WEST (315°)';
  };

  // Turn camera to specific heading
  const rotateTo = (deg: number) => {
    const norm = ((deg % 360) + 360) % 360;
    setHeadingDeg(norm);
    setIsPatrolling(false);
    sendPtzCommand(norm, false);
  };

  // Pan by relative delta
  const panBy = (deltaDeg: number) => {
    const next = ((headingRef.current + deltaDeg) % 360 + 360) % 360;
    setHeadingDeg(next);
    setIsPatrolling(false);
    sendPtzCommand(next, false);
  };

  // Toggle 360° Auto-Patrol sweep
  const togglePatrol = () => {
    setIsPatrolling((prev) => {
      const next = !prev;
      sendPtzCommand(headingRef.current, next);
      return next;
    });
  };

  // Mouse & Touch Drag Pan Handlers
  const handlePointerDown = (e: React.PointerEvent) => {
    setIsDragging(true);
    dragStartRef.current = { startX: e.clientX, startHeading: headingRef.current };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!isDragging || !dragStartRef.current) return;
    const deltaX = e.clientX - dragStartRef.current.startX;
    // 0.3 degrees per pixel of mouse drag
    const newHeading = ((dragStartRef.current.startHeading - deltaX * 0.3) % 360 + 360) % 360;
    setHeadingDeg(Math.round(newHeading));

    // Throttle PTZ HTTP commands to every ~40ms to avoid flooding
    const now = performance.now();
    if (now - lastCommandTimeRef.current > 40) {
      lastCommandTimeRef.current = now;
      sendPtzCommand(newHeading, false);
    }
  };

  const handlePointerUp = (e: React.PointerEvent) => {
    if (isDragging) {
      setIsDragging(false);
      dragStartRef.current = null;
      sendPtzCommand(headingRef.current, false);
    }
    try {
      (e.target as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      // ignore
    }
  };

  // Wheel zoom
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    setZoomLevel((prev) => Math.max(1.0, Math.min(2.5, prev - e.deltaY * 0.0015)));
  };

  // Periodic telemetry poll to sync heading if auto-patrolling
  useEffect(() => {
    if (!isPatrolling) return;
    const interval = setInterval(() => {
      try {
        const url = new URL(streamUrl);
        fetch(`${url.protocol}//${url.hostname}:${url.port}/ptz`)
          .then((res) => res.json())
          .then((data) => {
            if (data && typeof data.pan === 'number') {
              setHeadingDeg(Math.round(data.pan));
            }
          })
          .catch(() => {});
      } catch {
        // ignore
      }
    }, 200);
    return () => clearInterval(interval);
  }, [isPatrolling, streamUrl]);

  return (
    <div className="relative w-full h-full bg-slate-950 select-none overflow-hidden flex flex-col">
      {/* Main Viewport Container */}
      <div
        className="relative flex-1 w-full h-full overflow-hidden cursor-grab active:cursor-grabbing flex items-center justify-center bg-black"
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={handlePointerUp}
        onPointerCancel={handlePointerUp}
        onWheel={handleWheel}
      >
        {/* Loading Overlay */}
        {!streamLoaded && (
          <div className="absolute inset-0 bg-slate-950/90 backdrop-blur-xs flex flex-col items-center justify-center gap-2.5 z-30 pointer-events-none">
            <div className="w-8 h-8 border-2 border-slate-700 border-t-amber-400 rounded-full animate-spin"></div>
            <span className="text-slate-300 font-mono text-xs tracking-wider">
              CONNECTING TO 720p HD PTZ CAMERA ({junctionId})...
            </span>
            <span className="text-slate-500 font-mono text-[10px]">
              INITIALIZING MOTORIZED 360° SURVEILLANCE FEED
            </span>
          </div>
        )}

        {/* Live Pristine 720p HD Video Stream */}
        <div
          className="w-full h-full flex items-center justify-center transition-transform duration-75"
          style={{ transform: `scale(${zoomLevel})` }}
        >
          <img
            src={streamUrl}
            alt={`${cameraName} Stream`}
            crossOrigin="anonymous"
            className="w-full h-full object-contain pointer-events-none"
            onLoad={() => setStreamLoaded(true)}
            onError={() => setStreamLoaded(false)}
          />
        </div>

        {/* Tactical Crosshair Overlay */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-20">
          <Crosshair className="w-16 h-16 text-amber-400 stroke-1" />
        </div>

        {/* Top-Left Smart-City HUD Badge */}
        <div className="absolute top-3 left-3 z-20 flex flex-col gap-1.5 pointer-events-none">
          <div className="bg-slate-900/90 border border-slate-700/80 backdrop-blur-md px-3 py-1.5 flex items-center gap-2.5 text-xs text-white shadow-lg">
            <Compass className="w-4 h-4 text-amber-400 animate-pulse" />
            <div>
              <div className="font-bold text-[11px] leading-tight flex items-center gap-2">
                <span>{junctionId} • 360° MOTORIZED PTZ SURVEILLANCE</span>
                <span className="text-[9px] bg-amber-500/20 text-amber-300 px-1 py-0.2 border border-amber-500/40 font-mono">
                  {getCardinalDirection(headingDeg)}
                </span>
              </div>
              <div className="text-[10px] text-slate-400 font-mono flex items-center gap-2 mt-0.5">
                <span>AZIMUTH: {headingDeg}°</span>
                <span>•</span>
                <span>TILT: -12°</span>
                <span>•</span>
                <span>ZOOM: {zoomLevel.toFixed(1)}x</span>
                <span>•</span>
                <span className="text-emerald-400 font-semibold">720p HD (1280x720)</span>
              </div>
            </div>
          </div>

          <div className="text-[10px] text-slate-400 font-mono bg-slate-950/70 border border-slate-800 px-2 py-0.5 w-fit">
            CLICK & DRAG TO PAN 360° • SCROLL TO ZOOM
          </div>
        </div>

        {/* Top-Right Compass Quick-Select Approach Presets */}
        <div className="absolute top-3 right-3 z-20 flex items-center gap-1.5 bg-slate-900/90 border border-slate-700/80 p-1 backdrop-blur-md shadow-lg">
          <button
            type="button"
            onClick={() => rotateTo(0)}
            className={`px-2 py-1 text-[11px] font-mono transition-colors ${
              Math.abs(headingDeg - 0) < 15 || Math.abs(headingDeg - 360) < 15
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
            title="Point camera North (0°)"
          >
            N (0°)
          </button>
          <button
            type="button"
            onClick={() => rotateTo(90)}
            className={`px-2 py-1 text-[11px] font-mono transition-colors ${
              Math.abs(headingDeg - 90) < 15
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
            title="Point camera East (90°)"
          >
            E (90°)
          </button>
          <button
            type="button"
            onClick={() => rotateTo(180)}
            className={`px-2 py-1 text-[11px] font-mono transition-colors ${
              Math.abs(headingDeg - 180) < 15
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
            title="Point camera South (180°)"
          >
            S (180°)
          </button>
          <button
            type="button"
            onClick={() => rotateTo(270)}
            className={`px-2 py-1 text-[11px] font-mono transition-colors ${
              Math.abs(headingDeg - 270) < 15
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
            title="Point camera West (270°)"
          >
            W (270°)
          </button>
        </div>

        {/* Bottom-Right Tactical PTZ D-Pad & Controls */}
        <div className="absolute bottom-3 right-3 z-20 flex flex-col gap-1 items-end">
          <div className="bg-slate-900/90 border border-slate-700/80 p-1.5 backdrop-blur-md shadow-xl flex flex-col gap-1 items-center">
            {/* Top row: Patrol toggle & Reset */}
            <div className="flex items-center gap-1 w-full justify-between pb-1 border-b border-slate-800">
              <button
                type="button"
                onClick={togglePatrol}
                className={`flex items-center gap-1 text-[10px] font-mono px-1.5 py-0.5 border transition-colors ${
                  isPatrolling
                    ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 animate-pulse'
                    : 'bg-slate-800/80 text-slate-400 border-slate-700 hover:text-white'
                }`}
                title="Toggle 360° Auto-Patrol sweep"
              >
                {isPatrolling ? <Pause className="w-2.5 h-2.5" /> : <Play className="w-2.5 h-2.5" />}
                <span>{isPatrolling ? 'SWEEPING' : 'PATROL'}</span>
              </button>
              <button
                type="button"
                onClick={() => rotateTo(0)}
                className="p-1 hover:bg-slate-800 text-slate-400 hover:text-white transition-colors"
                title="Reset to North (0°)"
              >
                <RotateCcw className="w-3 h-3" />
              </button>
            </div>

            {/* Middle row: Pan Left & Right */}
            <div className="flex items-center gap-2 pt-0.5">
              <button
                type="button"
                onClick={() => panBy(20)}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 active:bg-amber-500 active:text-slate-950 text-slate-200 transition-colors border border-slate-700"
                title="Pan Left (+20°)"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <div className="text-[10px] font-mono text-amber-400 font-bold w-9 text-center">
                {headingDeg}°
              </div>
              <button
                type="button"
                onClick={() => panBy(-20)}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 active:bg-amber-500 active:text-slate-950 text-slate-200 transition-colors border border-slate-700"
                title="Pan Right (-20°)"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            {/* Bottom row: Zoom In / Zoom Out */}
            <div className="flex items-center gap-1 w-full justify-between pt-1 border-t border-slate-800">
              <button
                type="button"
                onClick={() => setZoomLevel((prev) => Math.min(2.5, prev + 0.25))}
                className="p-1 hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
                title="Zoom In"
              >
                <ZoomIn className="w-3.5 h-3.5" />
              </button>
              <span className="text-[9px] font-mono text-slate-400">
                {zoomLevel.toFixed(1)}x
              </span>
              <button
                type="button"
                onClick={() => setZoomLevel((prev) => Math.max(1.0, prev - 0.25))}
                className="p-1 hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
                title="Zoom Out"
              >
                <ZoomOut className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
