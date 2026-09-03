import { useState, useRef } from 'react';
import { X, Bus, Video, ShieldAlert, Sparkles, Compass } from 'lucide-react';
import Interactive360Viewer from './Interactive360Viewer';

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

export const CAMERAS_CONFIG: Record<
  string,
  { port: number; label: string; name: string; type: 'bus' | 'cctv'; desc: string }
> = {
  BUS_01: {
    port: 8011,
    label: 'BUS_01',
    name: 'Bus 01 Dashcam',
    type: 'bus',
    desc: 'Anna Salai Line — Front Dashcam + Pothole CV',
  },
  BUS_02: {
    port: 8012,
    label: 'BUS_02',
    name: 'Bus 02 Dashcam',
    type: 'bus',
    desc: 'T. Nagar Express — Front Dashcam + Pothole CV',
  },
  BUS_03: {
    port: 8013,
    label: 'BUS_03',
    name: 'Bus 03 Dashcam',
    type: 'bus',
    desc: 'Guindy Flyover — Front Dashcam + Pothole CV',
  },
  J25: {
    port: 8025,
    label: 'J25 360°',
    name: 'Junction 25 CCTV',
    type: 'cctv',
    desc: 'South-East 4-Way Arterial — 360° Equirectangular Surveillance',
  },
  J26: {
    port: 8026,
    label: 'J26 360°',
    name: 'Junction 26 CCTV',
    type: 'cctv',
    desc: 'North-West 4-Way Boulevard — 360° Equirectangular Surveillance',
  },
  J27: {
    port: 8027,
    label: 'J27 360°',
    name: 'Junction 27 CCTV',
    type: 'cctv',
    desc: 'Perimeter Highway — 360° Equirectangular Surveillance',
  },
  J41: {
    port: 8041,
    label: 'J41 360°',
    name: 'Junction 41 CCTV',
    type: 'cctv',
    desc: 'South-West 3-Way Junction — 360° Equirectangular Surveillance',
  },
  J43: {
    port: 8043,
    label: 'J43 360°',
    name: 'Junction 43 CCTV',
    type: 'cctv',
    desc: 'Central Plaza 3-Way Tower — 360° Equirectangular Surveillance',
  },
};

export default function LiveStreamModal({
  isOpen,
  onClose,
  selectedBus,
  setSelectedBus,
}: LiveStreamModalProps) {
  const [streamReady, setStreamReady] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  if (!isOpen) return null;

  const activeCam = CAMERAS_CONFIG[selectedBus] || CAMERAS_CONFIG['BUS_01'];
  const host = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1';
  const streamUrl = `http://${host}:${activeCam.port}/`;
  const isCctv = activeCam.type === 'cctv';

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-xs flex items-center justify-center p-4 select-none">
      <div className="bg-slate-900 border border-slate-700 rounded-none w-full max-w-5xl overflow-hidden shadow-2xl flex flex-col max-h-[92vh]">
        {/* Modal Header */}
        <div className="flex flex-wrap items-center justify-between px-4 py-2.5 border-b border-slate-800 bg-slate-950 gap-2">
          <div className="flex items-center gap-3">
            <div
              className={`w-7 h-7 ${
                isCctv ? 'bg-amber-600' : 'bg-sky-600'
              } text-white flex items-center justify-center rounded-none`}
            >
              {isCctv ? <Compass className="w-3.5 h-3.5" /> : <Video className="w-3.5 h-3.5" />}
            </div>
            <div>
              <h3 className="text-sm font-bold text-white leading-tight flex items-center gap-2">
                <span>{activeCam.name}</span>
                <span
                  className={`${
                    isCctv
                      ? 'bg-amber-500/20 border-amber-400 text-amber-300'
                      : 'bg-emerald-500/20 border-emerald-400 text-emerald-300'
                  } border text-[9px] font-mono px-1.5 py-0.2 rounded-none flex items-center gap-1`}
                >
                  <span
                    className={`w-1.5 h-1.5 ${
                      isCctv ? 'bg-amber-400' : 'bg-emerald-400'
                    } animate-pulse`}
                  ></span>
                  {isCctv ? 'LIVE 360° CCTV' : 'LIVE DASHCAM 1080p'}
                </span>
              </h3>
              <p className="text-[11px] text-slate-400">{activeCam.desc}</p>
            </div>
          </div>

          {/* Close Button */}
          <button
            onClick={onClose}
            className="w-7 h-7 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition-colors rounded-none border border-slate-700"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Camera Selector Bar */}
        <div className="px-4 py-2 bg-slate-950/70 border-b border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
          {/* Bus Fleet Category */}
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] font-mono uppercase text-slate-500 mr-1 flex items-center gap-1">
              <Bus className="w-3 h-3 text-sky-400" />
              <span>Buses:</span>
            </span>
            {['BUS_01', 'BUS_02', 'BUS_03'].map((id) => (
              <button
                key={id}
                onClick={() => {
                  setSelectedBus(id);
                  setStreamReady(false);
                }}
                className={`px-2.5 py-0.8 text-xs font-mono font-bold transition-colors rounded-none border ${
                  selectedBus === id
                    ? 'bg-sky-600 border-sky-400 text-white'
                    : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                {id}
              </button>
            ))}
          </div>

          {/* 360 Junction CCTV Category */}
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] font-mono uppercase text-slate-500 mr-1 flex items-center gap-1">
              <Compass className="w-3 h-3 text-amber-400" />
              <span>360° Traffic Lights:</span>
            </span>
            {['J25', 'J26', 'J27', 'J41', 'J43'].map((id) => (
              <button
                key={id}
                onClick={() => {
                  setSelectedBus(id);
                  setStreamReady(false);
                }}
                className={`px-2 py-0.8 text-xs font-mono font-bold transition-colors rounded-none border ${
                  selectedBus === id
                    ? 'bg-amber-600 border-amber-400 text-white'
                    : 'bg-slate-800/80 border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700'
                }`}
              >
                {id}
              </button>
            ))}
          </div>
        </div>

        {/* Video Canvas Container */}
        <div className="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
          {isCctv ? (
            <Interactive360Viewer
              key={selectedBus}
              streamUrl={streamUrl}
              cameraName={activeCam.name}
              junctionId={selectedBus}
            />
          ) : (
            <>
              {!streamReady && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-2.5 bg-slate-950/90 z-10">
                  <div className="w-7 h-7 border-2 border-slate-700 border-t-sky-400 rounded-full animate-spin"></div>
                  <span className="text-slate-400 font-mono text-xs">
                    CONNECTING TO {selectedBus} LIVE STREAM (PORT {activeCam.port})...
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
            </>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-2.5 bg-slate-950 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 text-slate-300">
              <Sparkles className={`w-3.5 h-3.5 ${isCctv ? 'text-amber-400' : 'text-sky-400'}`} />
              <span>
                {isCctv
                  ? '720p HD Motorized PTZ Sensor: 360° Surveillance'
                  : '720p HD Sensor: Forward Dashcam + Pothole Segmentation'}
              </span>
            </span>
            <span className="text-slate-600">|</span>
            <span>Port: {activeCam.port}</span>
          </div>
          <div
            className={`flex items-center gap-1.5 font-mono text-[10.5px] ${
              isCctv ? 'text-amber-400' : 'text-emerald-400'
            }`}
          >
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>{isCctv ? '360° MOTORIZED PTZ SURVEILLANCE' : 'REAL-TIME INFERENCE ACTIVE'}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
