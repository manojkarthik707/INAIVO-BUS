export default function EventStream({ events }: { events: any[] }) {
  if (events.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-slate-500">
        No active tracks.
      </div>
    )
  }

  // Deduplicate events by track_id so we only see the latest state of each vehicle
  const uniqueEvents = [];
  const seenTracks = new Set();
  for (const ev of events) {
    const trackId = ev.metadata?.track_id;
    if (trackId !== undefined && trackId !== null) {
      if (!seenTracks.has(trackId)) {
        seenTracks.add(trackId);
        uniqueEvents.push(ev);
      }
    } else {
      uniqueEvents.push(ev);
    }
  }

  return (
    <div className="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
      {uniqueEvents.map((ev, idx) => {
        const isStale = Date.now() - new Date(ev.timestamp).getTime() > 2000;
        const trackId = ev.metadata?.track_id;
        
        return (
          <div key={idx} className={`bg-slate-700/50 p-3 rounded-lg border shadow-sm transition-all duration-500 ${isStale ? 'border-slate-600 opacity-50' : 'border-emerald-500/50 animate-fade-in-down'}`}>
            <div className="flex justify-between items-start mb-1">
              <span className="text-xs text-slate-400">{new Date(ev.timestamp).toLocaleTimeString()}</span>
              <span className={`text-xs px-2 py-1 rounded font-bold ${isStale ? 'bg-slate-600 text-slate-300' : 'bg-emerald-900/80 text-emerald-300'}`}>
                {isStale ? 'TRACK LOST' : 'ACTIVE TRACK'}
              </span>
            </div>
            <div className={`font-bold flex items-center gap-2 ${isStale ? 'text-slate-400' : 'text-emerald-400'}`}>
              🎯 {ev.event_type.replace(/_/g, ' ')} {trackId ? `#${trackId}` : ''}
            </div>
            <div className="text-sm text-slate-300 mt-1 flex justify-between">
              <span>{ev.source.bus_id}</span>
              <span>Confidence: {(ev.confidence * 100).toFixed(0)}%</span>
            </div>
          </div>
        );
      })}
    </div>
  )
}
