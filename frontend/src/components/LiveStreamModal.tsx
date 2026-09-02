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
  events?: EventItem[];
}

export default function LiveStreamModal({
  isOpen,
  onClose,
  selectedBus,
  setSelectedBus,
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
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-none w-full max-w-5xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 bg-sky-600 text-white flex items-center justify-center rounded-none">
              <Video className="w-3.5 h-3.5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white leading-tight flex items-center gap-2">
                <span>Live Dashcam & AI Object Sensing</span>
                <span className="bg-emerald-500/20 border border-emerald-400 text-emerald-300 text-[9px] font-mono px-1.5 py-0.2 rounded-none flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-emerald-400 animate-pulse"></span>
                  LIVE 1080p
                </span>
              </h3>
              <p className="text-[11px] text-slate-400">
                Connected to {selectedBus} dashcam feed
              </p>
            </div>
          </div>

          {/* Square Bus Selector Tabs */}
          <div className="flex items-center gap-1.5">
            {['BUS_01', 'BUS_02', 'BUS_03'].map((busId) => (
              <button
                key={busId}
                onClick={() => {
                  setSelectedBus(busId);
                  setStreamReady(false);
                }}
                className={`px-3 py-1 text-xs font-mono font-bold flex items-center gap-1.5 transition-colors rounded-none border ${
                  selectedBus === busId
                    ? 'bg-sky-600 border-sky-500 text-white'
                    : 'bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                <Bus className="w-3 h-3" />
                <span>{busId}</span>
              </button>
            ))}

            {/* Close Button */}
            <button
              onClick={onClose}
              className="w-7 h-7 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center ml-2 transition-colors rounded-none border border-slate-700"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Video Canvas Container */}
        <div className="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
          {!streamReady && (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-2.5 bg-slate-950/90 z-10">
              <div className="w-7 h-7 border-2 border-slate-700 border-t-sky-400 rounded-full animate-spin"></div>
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
        </div>

        {/* Modal Footer */}
        <div className="p-2.5 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 text-slate-300">
              <Sparkles className="w-3.5 h-3.5 text-sky-400" />
              <span>Model: YOLOv11n + Terracotta Pothole CV</span>
            </span>
            <span className="text-slate-600">|</span>
            <span>Resolution: 1280x720 HD</span>
          </div>
          <div className="flex items-center gap-1.5 font-mono text-[10.5px] text-emerald-400">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>REAL-TIME INFERENCE ACTIVE</span>
          </div>
        </div>
      </div>
    </div>
  );
}
