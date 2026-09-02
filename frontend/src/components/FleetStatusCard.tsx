export default function FleetStatusCard({ total = 128 }: { total?: number }) {
  // Percentages matching screenshot: 77% Moving, 14% Idle, 9% Offline
  const moving = Math.round(total * 0.77);
  const idle = Math.round(total * 0.14);
  const offline = total - moving - idle;

  // SVG Donut calculation
  const radius = 38;
  const strokeWidth = 12;
  const circumference = 2 * Math.PI * radius;

  const movingPct = 0.77;
  const idlePct = 0.14;
  const offlinePct = 0.09;

  const movingStroke = circumference * movingPct;
  const idleStroke = circumference * idlePct;
  const offlineStroke = circumference * offlinePct;

  const movingOffset = 0;
  const idleOffset = -movingStroke;
  const offlineOffset = -(movingStroke + idleStroke);

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-sm select-none h-full flex flex-col justify-between">
      <h3 className="text-xs font-bold text-slate-800 tracking-wide mb-2">
        Fleet Status
      </h3>

      <div className="flex items-center justify-between gap-4 flex-1">
        {/* SVG Donut Chart */}
        <div className="relative w-28 h-28 flex items-center justify-center shrink-0">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            {/* Background Circle */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#f1f5f9"
              strokeWidth={strokeWidth}
            />
            {/* Moving Segment (Teal) */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#06b6d4"
              strokeWidth={strokeWidth}
              strokeDasharray={`${movingStroke} ${circumference}`}
              strokeDashoffset={movingOffset}
              strokeLinecap="round"
            />
            {/* Idle Segment (Blue) */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#0284c7"
              strokeWidth={strokeWidth}
              strokeDasharray={`${idleStroke} ${circumference}`}
              strokeDashoffset={idleOffset}
            />
            {/* Offline Segment (Slate Gray) */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#94a3b8"
              strokeWidth={strokeWidth}
              strokeDasharray={`${offlineStroke} ${circumference}`}
              strokeDashoffset={offlineOffset}
            />
          </svg>
          {/* Centered Total */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-base font-extrabold text-slate-900 leading-none">{total}</span>
            <span className="text-[9px] font-medium text-slate-400 uppercase mt-0.5">Total</span>
          </div>
        </div>

        {/* Legend List */}
        <div className="space-y-2 flex-1 min-w-0 pr-1">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 rounded-full bg-cyan-500 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Moving</span>
            </div>
            <span className="font-bold text-slate-800 text-right">{moving} (77%)</span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 rounded-full bg-sky-600 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Idle</span>
            </div>
            <span className="font-bold text-slate-800 text-right">{idle} (14%)</span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 rounded-full bg-slate-400 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Offline</span>
            </div>
            <span className="font-bold text-slate-800 text-right">{offline} (9%)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
