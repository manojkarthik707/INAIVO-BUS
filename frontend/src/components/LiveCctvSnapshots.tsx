import { useState, useEffect } from 'react';
import { Video, Maximize2, Compass, Bus } from 'lucide-react';

interface LiveCctvSnapshotsProps {
  selectedBus: string;
  setSelectedBus: (busId: string) => void;
  openStreamModal: (busId?: string) => void;
}

export default function LiveCctvSnapshots({
  selectedBus,
  setSelectedBus,
  openStreamModal,
}: LiveCctvSnapshotsProps) {
  const [imgErrors, setImgErrors] = useState<Record<string, boolean>>({});
  const [filterType, setFilterType] = useState<'all' | 'bus' | 'cctv'>('all');
  const [snapshotKey, setSnapshotKey] = useState(Date.now());

  useEffect(() => {
    // Refresh CCTV thumbnail snapshots periodically (every 3s) to avoid 5 concurrent live MJPEG streams
    const timer = setInterval(() => {
      setSnapshotKey(Date.now());
    }, 3000);
    return () => clearInterval(timer);
  }, []);

  const host = typeof window !== 'undefined' ? window.location.hostname : '127.0.0.1';

  const cameras = [
    {
      id: 'BUS_01',
      name: 'Bus 01 (Anna Salai)',
      streamUrl: `http://${host}:8011/`,
      type: 'bus',
      busId: 'BUS_01',
      fallbackImg: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=300&q=80',
    },
    {
      id: 'BUS_02',
      name: 'Bus 02 (T. Nagar)',
      streamUrl: `http://${host}:8012/`,
      type: 'bus',
      busId: 'BUS_02',
      fallbackImg: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=300&q=80',
    },
    {
      id: 'BUS_03',
      name: 'Bus 03 (Guindy)',
      streamUrl: `http://${host}:8013/`,
      type: 'bus',
      busId: 'BUS_03',
      fallbackImg: 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=300&q=80',
    },
    {
      id: 'J25',
      name: 'J25 360° (SE 4-Way)',
      streamUrl: `http://${host}:8025/`,
      type: 'cctv',
      busId: 'J25',
      fallbackImg: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?w=300&q=80',
    },
    {
      id: 'J26',
      name: 'J26 360° (NW Blvd)',
      streamUrl: `http://${host}:8026/`,
      type: 'cctv',
      busId: 'J26',
      fallbackImg: 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=300&q=80',
    },
    {
      id: 'J27',
      name: 'J27 360° (NE Highway)',
      streamUrl: `http://${host}:8027/`,
      type: 'cctv',
      busId: 'J27',
      fallbackImg: 'https://images.unsplash.com/photo-1477959858617-67f30bc75b82?w=300&q=80',
    },
    {
      id: 'J41',
      name: 'J41 360° (SW 3-Way)',
      streamUrl: `http://${host}:8041/`,
      type: 'cctv',
      busId: 'J41',
      fallbackImg: 'https://images.unsplash.com/photo-1517649763962-0c623266ddc0?w=300&q=80',
    },
    {
      id: 'J43',
      name: 'J43 360° (Plaza 3-Way)',
      streamUrl: `http://${host}:8043/`,
      type: 'cctv',
      busId: 'J43',
      fallbackImg: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=300&q=80',
    },
  ];

  const filteredCameras = cameras.filter((c) => filterType === 'all' || c.type === filterType);

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3 shadow-2xs select-none">
      {/* Header */}
      <div className="flex items-center justify-between mb-2 px-0.5">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <Video className="w-3.5 h-3.5 text-slate-700" />
            <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Live Fleet & 360° CCTV Feeds
            </h3>
          </div>

          {/* Quick Filter Buttons */}
          <div className="hidden sm:flex items-center gap-1 bg-slate-100 p-0.5 border border-slate-200 text-[10px] font-mono">
            <button
              onClick={() => setFilterType('all')}
              className={`px-2 py-0.5 font-bold transition-colors ${
                filterType === 'all' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              ALL (8)
            </button>
            <button
              onClick={() => setFilterType('bus')}
              className={`px-2 py-0.5 font-bold flex items-center gap-1 transition-colors ${
                filterType === 'bus' ? 'bg-sky-600 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Bus className="w-2.5 h-2.5" />
              BUSES (3)
            </button>
            <button
              onClick={() => setFilterType('cctv')}
              className={`px-2 py-0.5 font-bold flex items-center gap-1 transition-colors ${
                filterType === 'cctv' ? 'bg-amber-600 text-white shadow-xs' : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <Compass className="w-2.5 h-2.5" />
              360° CCTVS (5)
            </button>
          </div>
        </div>

        <button
          onClick={() => openStreamModal(selectedBus)}
          className="text-[11px] font-semibold text-sky-600 hover:text-sky-700 hover:underline flex items-center gap-1"
        >
          <span>Open Player</span>
          <Maximize2 className="w-3 h-3" />
        </button>
      </div>

      {/* Camera Thumbnails Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-4 lg:grid-cols-8 gap-2">
        {filteredCameras.map((cam) => {
          const isSelected = selectedBus === cam.busId;
          const hasError = imgErrors[cam.id];
          const isCctv = cam.type === 'cctv';

          return (
            <div
              key={cam.id}
              onClick={() => {
                if (cam.busId) setSelectedBus(cam.busId);
                openStreamModal(cam.busId);
              }}
              className={`group relative rounded-none overflow-hidden cursor-pointer transition-all bg-slate-900 border ${
                isSelected
                  ? isCctv
                    ? 'border-amber-500 ring-1 ring-amber-500'
                    : 'border-sky-600 ring-1 ring-sky-600'
                  : 'border-slate-200 hover:border-slate-400'
              }`}
            >
              {/* Image Preview Container */}
              <div className="relative aspect-[16/10] overflow-hidden bg-slate-950 flex items-center justify-center rounded-none">
                {!hasError ? (
                  <img
                    src={isCctv ? `${cam.streamUrl}snapshot.jpg?t=${snapshotKey}` : cam.streamUrl}
                    alt={cam.name}
                    className="w-full h-full object-cover group-hover:scale-102 transition-transform duration-200 rounded-none"
                    onError={() => setImgErrors((prev) => ({ ...prev, [cam.id]: true }))}
                  />
                ) : (
                  <img
                    src={cam.fallbackImg}
                    alt={cam.name}
                    className="w-full h-full object-cover group-hover:scale-102 transition-transform duration-200 opacity-80 rounded-none"
                  />
                )}

                {/* Badge (LIVE or 360) */}
                <div
                  className={`absolute top-1 left-1 text-white text-[8px] font-bold px-1 py-0.2 rounded-none flex items-center gap-0.5 font-mono ${
                    isCctv ? 'bg-amber-600' : 'bg-emerald-600'
                  }`}
                >
                  <span className="w-1 h-1 bg-white animate-pulse"></span>
                  <span>{isCctv ? '360°' : 'LIVE'}</span>
                </div>

                {/* Square Hover Overlay */}
                <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <span className="bg-white text-slate-900 font-bold text-[8px] px-1.5 py-0.5 rounded-none shadow-xs uppercase tracking-wider">
                    Inspect
                  </span>
                </div>
              </div>

              {/* Caption Label */}
              <div className="p-1 bg-white border-t border-slate-100 flex items-center justify-between">
                <span className="text-[9.5px] font-bold text-slate-800 truncate leading-tight">
                  {cam.name}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
