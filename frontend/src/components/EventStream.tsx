export default function EventStream({ events }: { events: any[] }) {
  if (events.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-slate-500">
        No events detected yet.
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
      {events.map((ev, idx) => (
        <div key={idx} className="bg-slate-700/50 p-3 rounded-lg border border-slate-600 shadow-sm animate-fade-in-down">
          <div className="flex justify-between items-start mb-1">
            <span className="text-xs text-slate-400">{new Date(ev.timestamp).toLocaleTimeString()}</span>
            <span className={`text-xs px-2 py-1 rounded font-bold ${ev.severity === 'HIGH' ? 'bg-red-900 text-red-200' : 'bg-yellow-900 text-yellow-200'}`}>
              {ev.severity}
            </span>
          </div>
          <div className="font-bold text-red-400 flex items-center gap-2">
            ⚠ {ev.event_type.replace(/_/g, ' ')}
          </div>
          <div className="text-sm text-slate-300 mt-1">
            {ev.source.bus_id} | Confidence: {(ev.confidence * 100).toFixed(0)}%
          </div>
        </div>
      ))}
    </div>
  )
}
