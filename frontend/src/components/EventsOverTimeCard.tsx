import { useState } from 'react';
import { ChevronDown } from 'lucide-react';

export default function EventsOverTimeCard() {
  const [timeframe, setTimeframe] = useState('Hourly');
  const [showMenu, setShowMenu] = useState(false);

  const points = [
    { label: '12 AM', val: 25, x: 20, y: 75 },
    { label: '4 AM',  val: 58, x: 65, y: 42 },
    { label: '8 AM',  val: 98, x: 110, y: 5 },
    { label: '12 PM', val: 50, x: 155, y: 50 },
    { label: '4 PM',  val: 62, x: 200, y: 38 },
    { label: '8 PM',  val: 85, x: 245, y: 15 },
    { label: '12 AM', val: 25, x: 290, y: 75 },
  ];

  const pathD = `
    M ${points[0].x} ${points[0].y}
    C 40 70, 50 45, ${points[1].x} ${points[1].y}
    C 80 40, 95 10, ${points[2].x} ${points[2].y}
    C 125 0, 140 45, ${points[3].x} ${points[3].y}
    C 170 55, 185 40, ${points[4].x} ${points[4].y}
    C 215 35, 230 18, ${points[5].x} ${points[5].y}
    C 260 12, 275 65, ${points[6].x} ${points[6].y}
  `;

  const areaD = `
    ${pathD}
    L ${points[6].x} 95
    L ${points[0].x} 95
    Z
  `;

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
          Events Over Time
        </h3>

        {/* Square Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="flex items-center gap-1 bg-slate-50 border border-slate-200 hover:border-slate-300 px-2.5 py-1 rounded-none text-[11px] font-medium text-slate-700 transition-colors"
          >
            <span>{timeframe}</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {showMenu && (
            <div className="absolute right-0 mt-1 w-28 bg-white border border-slate-200 rounded-none shadow-md z-50 py-1">
              {['Hourly', 'Daily', 'Weekly'].map((opt) => (
                <button
                  key={opt}
                  onClick={() => { setTimeframe(opt); setShowMenu(false); }}
                  className={`w-full text-left px-3 py-1 text-[11px] font-medium hover:bg-slate-50 ${
                    timeframe === opt ? 'text-sky-600 font-bold bg-sky-50/50' : 'text-slate-600'
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Line Chart */}
      <div className="relative h-28 flex flex-col justify-end pt-2">
        {/* Background Grid Lines & Y-axis labels */}
        <div className="absolute inset-0 flex flex-col justify-between pointer-events-none text-[8.5px] text-slate-400 font-mono pr-2">
          <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
            <span>100</span>
          </div>
          <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
            <span>75</span>
          </div>
          <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
            <span>50</span>
          </div>
          <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
            <span>25</span>
          </div>
          <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
            <span>0</span>
          </div>
        </div>

        {/* SVG Curve */}
        <div className="w-full h-full pl-6 pr-1 relative z-10">
          <svg viewBox="0 0 310 100" className="w-full h-full overflow-visible" preserveAspectRatio="none">
            <defs>
              <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0284c7" stopOpacity="0.12" />
                <stop offset="100%" stopColor="#0284c7" stopOpacity="0.0" />
              </linearGradient>
            </defs>

            <path d={areaD} fill="url(#areaGradient)" />

            <path
              d={pathD}
              fill="none"
              stroke="#0284c7"
              strokeWidth="2"
              strokeLinecap="square"
              strokeLinejoin="miter"
            />

            {points.map((pt, idx) => (
              <rect
                key={idx}
                x={pt.x - 3}
                y={pt.y - 3}
                width="6"
                height="6"
                fill="#ffffff"
                stroke="#0284c7"
                strokeWidth="2"
                className="cursor-pointer"
              />
            ))}
          </svg>
        </div>

        {/* X-axis labels */}
        <div className="flex items-center justify-between pl-6 pr-1 mt-1 text-[9px] font-mono text-slate-400">
          {points.map((pt) => (
            <span key={pt.label}>{pt.label}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
