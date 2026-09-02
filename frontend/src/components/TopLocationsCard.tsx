export default function TopLocationsCard() {
  const data = [
    { name: 'T. Nagar', count: 70 },
    { name: 'Anna Nagar', count: 48 },
    { name: 'Guindy', count: 32 },
    { name: 'Velachery', count: 28 },
    { name: 'Tambaram', count: 15 },
  ];

  const maxVal = 80;

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none h-full flex flex-col justify-between">
      <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-1">
        Top Issue Locations
      </h3>

      <div className="flex-1 flex flex-col justify-end">
        {/* Bar Chart Area */}
        <div className="relative h-28 flex items-end justify-between pt-4 px-1">
          {/* Background Grid Lines & Y-axis labels */}
          <div className="absolute inset-0 flex flex-col justify-between pointer-events-none text-[8.5px] text-slate-400 font-mono">
            <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
              <span>80</span>
            </div>
            <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
              <span>60</span>
            </div>
            <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
              <span>40</span>
            </div>
            <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
              <span>20</span>
            </div>
            <div className="border-b border-slate-100 flex items-center justify-between pb-0.5">
              <span>0</span>
            </div>
          </div>

          {/* Vertical Bars (Square) */}
          <div className="w-full flex items-end justify-around z-10 pl-5 pr-1">
            {data.map((item) => {
              const heightPct = (item.count / maxVal) * 100;
              return (
                <div key={item.name} className="flex flex-col items-center gap-1 group">
                  <span className="text-[9.5px] font-bold text-sky-700 opacity-0 group-hover:opacity-100 transition-opacity">
                    {item.count}
                  </span>
                  <div
                    style={{ height: `${heightPct}%` }}
                    className="w-6 sm:w-7 bg-sky-700 hover:bg-sky-600 transition-colors cursor-pointer rounded-none"
                  ></div>
                </div>
              );
            })}
          </div>
        </div>

        {/* X-axis labels */}
        <div className="flex items-center justify-around pl-5 pr-1 mt-2 text-[10px] font-medium text-slate-600">
          {data.map((item) => (
            <span key={item.name} className="truncate max-w-[55px] text-center">
              {item.name}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
