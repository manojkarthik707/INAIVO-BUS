import { useState } from 'react';
import { Video, Maximize2 } from 'lucide-react';

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

  const cameras = [
    {
      id: 'BUS_01',
      name: 'Anna Salai Junction',
      streamUrl: 'http://127.0.0.1:8011/',
      isBus: true,
      busId: 'BUS_01',
      fallbackImg: 'https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=300&q=80',
    },
    {
      id: 'BUS_02',
      name: 'T. Nagar Bus Stand',
      streamUrl: 'http://127.0.0.1:8012/',
      isBus: true,
      busId: 'BUS_02',
      fallbackImg: 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=300&q=80',
    },
    {
      id: 'BUS_03',
      name: 'Guindy Flyover',
      streamUrl: 'http://127.0.0.1:8013/',
      isBus: true,
      busId: 'BUS_03',
      fallbackImg: 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=300&q=80',
    },
    {
      id: 'CCTV_04',
      name: 'Velachery Main Rd',
      streamUrl: 'http://127.0.0.1:8011/',
      isBus: false,
      busId: 'BUS_01',
      fallbackImg: 'https://images.unsplash.com/photo-1506521781263-d8422e82f27a?w=300&q=80',
    },
    {
      id: 'CCTV_05',
      name: 'Tambaram Railway Stn',
      streamUrl: 'http://127.0.0.1:8012/',
      isBus: false,
      busId: 'BUS_02',
      fallbackImg: 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=300&q=80',
    },
  ];

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-3.5 shadow-sm select-none">
      {/* Header */}
      <div className="flex items-center justify-between mb-2 px-1">
        <div className="flex items-center gap-2">
          <Video className="w-4 h-4 text-slate-700" />
          <h3 className="text-xs font-bold text-slate-800 tracking-wide">
            Live CCTV Snapshot
          </h3>
        </div>
        <button
          onClick={() => openStreamModal(selectedBus)}
          className="text-[11px] font-semibold text-sky-600 hover:text-sky-700 hover:underline flex items-center gap-1"
        >
          <span>View All</span>
          <Maximize2 className="w-3 h-3" />
        </button>
      </div>

      {/* Camera Thumbnails Horizontal Row */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5">
        {cameras.map((cam) => {
          const isSelected = selectedBus === cam.busId;
          const hasError = imgErrors[cam.id];

          return (
            <div
              key={cam.id}
              onClick={() => {
                if (cam.busId) setSelectedBus(cam.busId);
                openStreamModal(cam.busId);
              }}
              className={`group relative rounded-xl overflow-hidden cursor-pointer transition-all bg-slate-900 border ${
                isSelected
                  ? 'border-sky-500 ring-2 ring-sky-500/20 shadow-md'
                  : 'border-slate-200 hover:border-slate-400'
              }`}
            >
              {/* Image Preview Container */}
              <div className="relative aspect-[16/10] overflow-hidden bg-slate-950 flex items-center justify-center">
                {/* Live stream or fallback image */}
                {!hasError ? (
                  <img
                    src={cam.streamUrl}
                    alt={cam.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={() => setImgErrors((prev) => ({ ...prev, [cam.id]: true }))}
                  />
                ) : (
                  <img
                    src={cam.fallbackImg}
                    alt={cam.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 opacity-80"
                  />
                )}

                {/* LIVE Badge */}
                <div className="absolute top-1.5 left-1.5 bg-emerald-600/90 backdrop-blur-xs text-white text-[8.5px] font-bold px-1.5 py-0.5 rounded flex items-center gap-1 shadow-sm">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-300 animate-pulse"></span>
                  <span>LIVE</span>
                </div>

                {/* Overlay hover prompt */}
                <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <span className="bg-white/90 text-slate-900 font-bold text-[9.5px] px-2 py-0.5 rounded shadow-sm">
                    Open Feed
                  </span>
                </div>
              </div>

              {/* Caption Label */}
              <div className="p-1.5 bg-white border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10.5px] font-bold text-slate-800 truncate leading-tight">
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
