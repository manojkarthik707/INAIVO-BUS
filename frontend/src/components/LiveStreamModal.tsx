import { useState, useRef } from 'react';
import { X, Bus, Video, ShieldAlert, Sparkles } from 'lucide-react';

interface EventItem {
  event_id?: string;
  event_type: string;
  severity: string;
  confidence?: number;
  timestamp: string;
  location?: { latitude: number; longitude: number };
  metadata?: any;
  source?: any;
}

interface LiveStreamModalProps {
  isOpen: boolean;
  onClose: () => void;
  selectedBus: string;
  setSelectedBus: (busId: string) => void;
  events: EventItem[];
}

export default function LiveStreamModal({
  isOpen,
  onClose,
  selectedBus,
  setSelectedBus,
  events,
}: LiveStreamModalProps) {
  const [streamReady, setStreamReady] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  if (!isOpen) return null;

  const MJPEG_PORT: Record<string, number> = {
    BUS_01: 8011,
    BUS_02: 8012,
    BUS_03: 8013,
  };

  const streamUrl = `http://127.0.0.1:${MJPEG_PORT[selectedBus] || 8011}/`;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-5xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-950/80">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-sky-600 text-white flex items-center justify-center">
              <Video className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white leading-tight flex items-center gap-2">
                <span>Live Dashcam & AI Object Sensing</span>
                <span className="bg-emerald-500/20 border border-emerald-400 text-emerald-300 text-[10px] font-mono px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  LIVE 1080p
                </span>
              </h3>
              <p className="text-xs text-slate-400">
                Connected to {selectedBus} high-definition dashcam feed
              </p>
            </div>
          </div>

          {/* Bus Selector Tabs */}
          <div className="flex items-center gap-2">
            {['BUS_01', 'BUS_02', 'BUS_03'].map((busId) => (
              <button
                key={busId}
                onClick={() => {
                  setSelectedBus(busId);
                  setStreamReady(false);
                }}
                className={`px-3 py-1 rounded-full text-xs font-mono font-bold flex items-center gap-1.5 transition-all ${
                  selectedBus === busId
                    ? 'bg-sky-600 text-white shadow-md'
                    : 'bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Bus className="w-3 h-3" />
                <span>{busId}</span>
              </button>
            ))}

            {/* Close Button */}
            <button
              onClick={onClose}
              className="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center ml-2 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Video Canvas Container */}
        <div className="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
          {!streamReady && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-2.5 bg-slate-950/90 z-10">
              <div className="w-8 h-8 border-3 border-slate-700 border-t-sky-400 rounded-full animate-spin"></div>
              <span className="text-slate-400 font-mono text-xs">
                INITIALIZING {selectedBus} LIVE STREAM...
              </span>
            </div>
          )}

          {/* Live MJPEG Stream */}
          <img
            ref={imgRef}
            src={streamUrl}
            alt={`${selectedBus} Live Stream`}
            className={`w-full h-full object-contain transition-opacity duration-300 ${
              streamReady ? 'opacity-100' : 'opacity-0'
            }`}
            onLoad={() => setStreamReady(true)}
            onError={() => setStreamReady(false)}
          />

          {/* AI Bounding Box Overlays */}
          {events
            .filter((e) => e.source?.bus_id === selectedBus && Date.now() - new Date(e.timestamp).getTime() < 1200)
            .map((event, idx) => {
              if (!event.metadata?.bbox) return null;
              const [x1, y1, x2, y2] = event.metadata.bbox;
              const isPothole = event.event_type.includes('POTHOLE');

              return (
                <div
                  key={event.event_id || idx}
                  className={`absolute border-2 flex flex-col justify-end overflow-hidden transition-all duration-75 pointer-events-none ${
                    isPothole
                      ? 'border-emerald-400 bg-emerald-400/20 shadow-[0_0_15px_rgba(52,211,153,0.4)]'
                      : 'border-cyan-400 bg-cyan-400/15 shadow-[0_0_15px_rgba(6,182,212,0.4)]'
                  }`}
                  style={{
                    left: `${(x1 / 1280) * 100}%`,
                    top: `${(y1 / 720) * 100}%`,
                    width: `${((x2 - x1) / 1280) * 100}%`,
                    height: `${((y2 - y1) / 720) * 100}%`,
                  }}
                >
                  <div
                    className={`text-[9px] font-mono font-bold px-1.5 py-0.5 flex items-center justify-between text-white ${
                      isPothole ? 'bg-emerald-500' : 'bg-cyan-600'
                    }`}
                  >
                    <span>{event.event_type.replace('_DETECTED', '')} {Math.round((event.confidence || 0.95) * 100)}%</span>
                  </div>
                </div>
              );
            })}
        </div>

        {/* Modal Footer / Telemetry Bar */}
        <div className="p-3 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1 text-slate-300">
              <Sparkles className="w-3.5 h-3.5 text-sky-400" />
              <span>Model: YOLOv11n + Terracotta Pothole CV</span>
            </span>
            <span className="text-slate-500">|</span>
            <span>Resolution: 1280x720 HD</span>
          </div>
          <div className="flex items-center gap-2 font-mono text-[11px] text-emerald-400">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>REAL-TIME INFERENCE ACTIVE</span>
          </div>
        </div>
      </div>
    </div>
  );
}
