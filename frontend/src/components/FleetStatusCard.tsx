export default function FleetStatusCard({ total = 128 }: { total?: number }) {
  const moving = Math.round(total * 0.77);
  const idle = Math.round(total * 0.14);
  const offline = total - moving - idle;

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
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none h-full flex flex-col justify-between">
      <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2">
        Fleet Status
      </h3>

      <div className="flex items-center justify-between gap-4 flex-1">
        {/* SVG Donut Chart */}
        <div className="relative w-26 h-26 flex items-center justify-center shrink-0">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#f1f5f9"
              strokeWidth={strokeWidth}
            />
            <circle
              cx="50"
              cy="50"
              r={radius}
              fill="transparent"
              stroke="#06b6d4"
              strokeWidth={strokeWidth}
              strokeDasharray={`${movingStroke} ${circumference}`}
              strokeDashoffset={movingOffset}
            />
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
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-base font-bold text-slate-900 leading-none">{total}</span>
            <span className="text-[8.5px] font-semibold text-slate-400 uppercase tracking-wider mt-0.5">Total</span>
          </div>
        </div>

        {/* Legend List */}
        <div className="space-y-2 flex-1 min-w-0 pr-1">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 bg-cyan-500 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Moving</span>
            </div>
            <span className="font-bold text-slate-900 text-right">{moving} <span className="text-slate-400 font-normal">(77%)</span></span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 bg-sky-600 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Idle</span>
            </div>
            <span className="font-bold text-slate-900 text-right">{idle} <span className="text-slate-400 font-normal">(14%)</span></span>
          </div>

          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2 truncate">
              <span className="w-2 h-2 bg-slate-400 shrink-0"></span>
              <span className="text-slate-600 font-medium truncate">Offline</span>
            </div>
            <span className="font-bold text-slate-900 text-right">{offline} <span className="text-slate-400 font-normal">(9%)</span></span>
          </div>
        </div>
      </div>
    </div>
  );
}
