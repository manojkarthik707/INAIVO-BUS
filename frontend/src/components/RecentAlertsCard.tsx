import { AlertOctagon, Car, Droplets, Cone, Bell } from 'lucide-react';

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
  const defaultAlerts = [
    {
      id: 'static-1',
      title: 'Pothole Detected',
      location: 'T. Nagar, Chennai',
      time: '10:21 AM',
      severity: 'High',
      icon: AlertOctagon,
      iconColor: 'text-red-600 bg-red-50',
      badgeColor: 'bg-red-600 text-white',
    },
    {
      id: 'static-2',
      title: 'Traffic Jam',
      location: 'Anna Salai, Chennai',
      time: '10:18 AM',
      severity: 'Medium',
      icon: Car,
      iconColor: 'text-orange-600 bg-orange-50',
      badgeColor: 'bg-orange-600 text-white',
    },
    {
      id: 'static-3',
      title: 'Water Logging',
      location: 'Velachery Main Rd, Chennai',
      time: '10:10 AM',
      severity: 'Medium',
      icon: Droplets,
      iconColor: 'text-sky-600 bg-sky-50',
      badgeColor: 'bg-orange-600 text-white',
    },
    {
      id: 'static-4',
      title: 'Obstruction Detected',
      location: 'Tambaram High Rd, Chennai',
      time: '10:05 AM',
      severity: 'Low',
      icon: Cone,
      iconColor: 'text-purple-600 bg-purple-50',
      badgeColor: 'bg-yellow-400 text-slate-900',
    },
  ];

  const liveAlerts = events.map((e, idx) => {
    const isPothole = e.event_type.includes('POTHOLE');
    const isPed = e.event_type.includes('PEDESTRIAN') || e.event_type.includes('PERSON');
    const isRedLight = e.event_type.includes('RED_LIGHT');
    const isTraffic = e.event_type.includes('CONGESTION') || e.event_type.includes('CAR');

    let title = 'Road Hazard Detected';
    let icon = AlertOctagon;
    let iconColor = 'text-red-600 bg-red-50';
    let badgeColor = 'bg-red-600 text-white';
    let sev = e.severity || 'High';

    if (isPothole) {
      title = 'Pothole Detected';
      icon = AlertOctagon;
      iconColor = 'text-red-600 bg-red-50';
      badgeColor = 'bg-red-600 text-white';
    } else if (isPed) {
      title = 'Pedestrian Warning';
      icon = AlertOctagon;
      iconColor = 'text-amber-600 bg-amber-50';
      badgeColor = 'bg-amber-600 text-white';
    } else if (isRedLight) {
      title = 'Red Light Signal Alert';
      icon = Car;
      iconColor = 'text-red-600 bg-red-50';
      badgeColor = 'bg-red-600 text-white';
    } else if (isTraffic) {
      title = 'Traffic Congestion';
      icon = Car;
      iconColor = 'text-orange-600 bg-orange-50';
      badgeColor = 'bg-orange-600 text-white';
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

  const displayList = liveAlerts.length > 0 ? liveAlerts : defaultAlerts;

  return (
    <div className="bg-white border border-slate-200 rounded-none p-3.5 shadow-2xs select-none flex flex-col max-h-[340px] xl:max-h-[380px] overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between mb-2.5 pb-2 border-b border-slate-100 shrink-0">
        <div className="flex items-center gap-2">
          <Bell className="w-3.5 h-3.5 text-sky-600" />
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            Recent Alerts
          </h3>
          <span className="px-1.5 py-0.5 text-[8.5px] font-mono font-bold bg-sky-50 text-sky-700 border border-sky-200">
            {displayList.length} LIVE
          </span>
        </div>
        <button className="text-[11px] font-semibold text-sky-600 hover:text-sky-700 hover:underline">
          View All
        </button>
      </div>

      {/* Scrollable Alert List */}
      <div className="space-y-1.5 overflow-y-auto flex-1 pr-1.5 focus:outline-none">
        {displayList.map((alert) => {
          const Icon = alert.icon;
          return (
            <div
              key={alert.id}
              className="flex items-center justify-between gap-2.5 p-2 rounded-none border border-slate-100 hover:border-slate-200 hover:bg-slate-50/80 transition-colors"
            >
              {/* Icon & Details */}
              <div className="flex items-center gap-2.5 min-w-0 flex-1">
                <div className={`w-7 h-7 flex items-center justify-center shrink-0 rounded-none ${alert.iconColor}`}>
                  <Icon className="w-3.5 h-3.5" />
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

              {/* Time & Square Severity Badge */}
              <div className="flex items-center gap-2 shrink-0">
                <span className="text-[10px] font-mono text-slate-400">
                  {alert.time}
                </span>
                <span className={`text-[9.5px] font-bold px-2 py-0.5 rounded-none font-mono uppercase ${alert.badgeColor}`}>
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
