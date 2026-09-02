import { AlertOctagon, Car, Droplets, Cone } from 'lucide-react';

interface EventItem {
  event_id?: string;
  event_type: string;
  severity: string;
  timestamp: string;
  location?: { latitude: number; longitude: number };
  metadata?: any;
  source?: any;
}

interface RecentAlertsCardProps {
  events?: EventItem[];
}

export default function RecentAlertsCard({ events = [] }: RecentAlertsCardProps) {
  // Static mock events matching screenshot, merged with live events from WebSocket
  const defaultAlerts = [
    {
      id: 'static-1',
      title: 'Pothole Detected',
      location: 'T. Nagar, Chennai',
      time: '10:21 AM',
      severity: 'High',
      icon: AlertOctagon,
      iconColor: 'text-red-500 bg-red-50',
      badgeColor: 'bg-red-500 text-white',
    },
    {
      id: 'static-2',
      title: 'Traffic Jam',
      location: 'Anna Salai, Chennai',
      time: '10:18 AM',
      severity: 'Medium',
      icon: Car,
      iconColor: 'text-orange-500 bg-orange-50',
      badgeColor: 'bg-orange-500 text-white',
    },
    {
      id: 'static-3',
      title: 'Water Logging',
      location: 'Velachery Main Rd, Chennai',
      time: '10:10 AM',
      severity: 'Medium',
      icon: Droplets,
      iconColor: 'text-sky-500 bg-sky-50',
      badgeColor: 'bg-orange-500 text-white',
    },
    {
      id: 'static-4',
      title: 'Obstruction Detected',
      location: 'Tambaram High Rd, Chennai',
      time: '10:05 AM',
      severity: 'Low',
      icon: Cone,
      iconColor: 'text-purple-500 bg-purple-50',
      badgeColor: 'bg-yellow-400 text-slate-900',
    },
  ];

  // Map dynamic live events if available
  const liveAlerts = events.slice(0, 3).map((e, idx) => {
    const isPothole = e.event_type.includes('POTHOLE');
    const isPed = e.event_type.includes('PEDESTRIAN') || e.event_type.includes('PERSON');
    const isRedLight = e.event_type.includes('RED_LIGHT');
    const isTraffic = e.event_type.includes('CONGESTION') || e.event_type.includes('CAR');

    let title = 'Road Hazard Detected';
    let icon = AlertOctagon;
    let iconColor = 'text-red-500 bg-red-50';
    let badgeColor = 'bg-red-500 text-white';
    let sev = e.severity || 'High';

    if (isPothole) {
      title = 'Pothole Detected';
      icon = AlertOctagon;
      iconColor = 'text-red-500 bg-red-50';
      badgeColor = 'bg-red-500 text-white';
    } else if (isPed) {
      title = 'Pedestrian Warning';
      icon = AlertOctagon;
      iconColor = 'text-amber-500 bg-amber-50';
      badgeColor = 'bg-amber-500 text-white';
    } else if (isRedLight) {
      title = 'Red Light Signal Alert';
      icon = Car;
      iconColor = 'text-red-500 bg-red-50';
      badgeColor = 'bg-red-500 text-white';
    } else if (isTraffic) {
      title = 'Traffic Congestion';
      icon = Car;
      iconColor = 'text-orange-500 bg-orange-50';
      badgeColor = 'bg-orange-500 text-white';
    }

    const t = new Date(e.timestamp);
    const timeStr = isNaN(t.getTime())
      ? 'Just now'
      : t.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

    return {
      id: e.event_id || `live-${idx}`,
      title,
      location: e.metadata?.description || `${e.source?.bus_id || 'Bus 01'} Dashcam AI`,
      time: timeStr,
      severity: sev,
      icon,
      iconColor,
      badgeColor,
    };
  });

  const displayList = [...liveAlerts, ...defaultAlerts].slice(0, 4);

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-sm select-none flex-1 flex flex-col justify-between">
      {/* Header */}
      <div className="flex items-center justify-between mb-2.5">
        <h3 className="text-xs font-bold text-slate-800 tracking-wide">
          Recent Alerts
        </h3>
        <button className="text-[11px] font-semibold text-sky-600 hover:text-sky-700 hover:underline">
          View All
        </button>
      </div>

      {/* Alert List */}
      <div className="space-y-2.5 flex-1">
        {displayList.map((alert) => {
          const Icon = alert.icon;
          return (
            <div
              key={alert.id}
              className="flex items-center justify-between gap-3 p-2 rounded-xl hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-100"
            >
              {/* Icon & Details */}
              <div className="flex items-center gap-2.5 min-w-0 flex-1">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${alert.iconColor}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <h4 className="text-xs font-bold text-slate-900 truncate leading-tight">
                    {alert.title}
                  </h4>
                  <p className="text-[10px] text-slate-500 font-medium truncate mt-0.5">
                    {alert.location}
                  </p>
                </div>
              </div>

              {/* Time & Severity Badge */}
              <div className="flex items-center gap-2.5 shrink-0">
                <span className="text-[10px] font-medium text-slate-400 font-mono">
                  {alert.time}
                </span>
                <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-md ${alert.badgeColor}`}>
                  {alert.severity}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
