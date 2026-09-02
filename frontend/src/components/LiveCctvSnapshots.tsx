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
    <div className="bg-white border border-slate-200 rounded-none p-3 shadow-2xs select-none">
      {/* Header */}
      <div className="flex items-center justify-between mb-2 px-0.5">
        <div className="flex items-center gap-2">
          <Video className="w-3.5 h-3.5 text-slate-700" />
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
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

      {/* Square Camera Thumbnails Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
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
              className={`group relative rounded-none overflow-hidden cursor-pointer transition-all bg-slate-900 border ${
                isSelected
                  ? 'border-sky-600 ring-1 ring-sky-600'
                  : 'border-slate-200 hover:border-slate-400'
              }`}
            >
              {/* Image Preview Container */}
              <div className="relative aspect-[16/10] overflow-hidden bg-slate-950 flex items-center justify-center rounded-none">
                {!hasError ? (
                  <img
                    src={cam.streamUrl}
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

                {/* Square LIVE Badge */}
                <div className="absolute top-1 left-1 bg-emerald-600 text-white text-[8px] font-bold px-1.5 py-0.5 rounded-none flex items-center gap-1 font-mono">
                  <span className="w-1 h-1 bg-emerald-300 animate-pulse"></span>
                  <span>LIVE</span>
                </div>

                {/* Square Hover Overlay */}
                <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <span className="bg-white text-slate-900 font-bold text-[9px] px-2 py-0.5 rounded-none shadow-xs uppercase tracking-wider">
                    View Stream
                  </span>
                </div>
              </div>

              {/* Caption Label */}
              <div className="p-1.5 bg-white border-t border-slate-100 flex items-center justify-between">
                <span className="text-[10px] font-bold text-slate-800 truncate leading-tight">
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
