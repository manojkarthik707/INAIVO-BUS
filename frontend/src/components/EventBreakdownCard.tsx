export default function EventBreakdownCard({ total = 346 }: { total?: number }) {
  const categories = [
    { label: 'Pothole / Road Damage', count: 142, pct: '41%', color: '#ef4444' },
    { label: 'Traffic Jam', count: 78, pct: '23%', color: '#f97316' },
    { label: 'Accident', count: 45, pct: '13%', color: '#3b82f6' },
    { label: 'Water Logging', count: 34, pct: '10%', color: '#06b6d4' },
    { label: 'Obstruction', count: 24, pct: '7%', color: '#8b5cf6' },
    { label: 'Others', count: 23, pct: '6%', color: '#94a3b8' },
  ];

  const radius = 38;
  const strokeWidth = 12;
  const circumference = 2 * Math.PI * radius;

  const segments = [
    { pct: 0.41, color: '#ef4444' },
    { pct: 0.23, color: '#f97316' },
    { pct: 0.13, color: '#3b82f6' },
    { pct: 0.10, color: '#06b6d4' },
    { pct: 0.07, color: '#8b5cf6' },
    { pct: 0.06, color: '#94a3b8' },
  ];

  let cumulativeOffset = 0;

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none">
      <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2.5">
        Event Breakdown
      </h3>

      <div className="flex items-center gap-4">
        {/* SVG Donut */}
        <div className="relative w-26 h-26 flex items-center justify-center shrink-0">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r={radius} fill="transparent" stroke="#f1f5f9" strokeWidth={strokeWidth} />
            {segments.map((seg, idx) => {
              const strokeLength = circumference * seg.pct;
              const offset = -cumulativeOffset;
              cumulativeOffset += strokeLength;
              return (
                <circle
                  key={idx}
                  cx="50"
                  cy="50"
                  r={radius}
                  fill="transparent"
                  stroke={seg.color}
                  strokeWidth={strokeWidth}
                  strokeDasharray={`${strokeLength} ${circumference}`}
                  strokeDashoffset={offset}
                />
              );
            })}
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-base font-bold text-slate-900 leading-none">{total}</span>
            <span className="text-[8.5px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">Total</span>
          </div>
        </div>

        {/* Categories List */}
        <div className="space-y-1.5 flex-1 min-w-0">
          {categories.map((cat) => (
            <div key={cat.label} className="flex items-center justify-between text-[11px]">
              <div className="flex items-center gap-1.5 truncate">
                <span className="w-2 h-2 shrink-0" style={{ backgroundColor: cat.color }}></span>
                <span className="text-slate-600 truncate">{cat.label}</span>
              </div>
              <span className="font-bold text-slate-900 shrink-0 ml-1">
                {cat.count} <span className="text-slate-400 font-normal">({cat.pct})</span>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
