import { Bus, MapPin, TrendingUp, AlertOctagon, Video, Timer, ArrowUp, ArrowDown } from 'lucide-react';

interface KpiCardsProps {
  activeBusCount?: number;
  totalEventCount?: number;
  criticalAlertCount?: number;
  cctvOnlineCount?: number;
}

export default function KpiCards({
  activeBusCount = 128,
  totalEventCount = 346,
  criticalAlertCount = 23,
  cctvOnlineCount = 312,
}: KpiCardsProps) {
  const kpis = [
    {
      id: 'buses',
      label: 'Active Buses',
      value: activeBusCount.toString(),
      trend: '12% vs yesterday',
      trendUp: true,
      trendPositive: true,
      icon: Bus,
      iconBg: 'bg-sky-600',
    },
    {
      id: 'distance',
      label: 'Distance Covered',
      value: '12,842 km',
      trend: '8% vs yesterday',
      trendUp: true,
      trendPositive: true,
      icon: MapPin,
      iconBg: 'bg-cyan-600',
    },
    {
      id: 'events',
      label: 'Total Events',
      value: totalEventCount.toString(),
      trend: '15% vs yesterday',
      trendUp: true,
      trendPositive: true,
      icon: TrendingUp,
      iconBg: 'bg-blue-600',
    },
    {
      id: 'alerts',
      label: 'Critical Alerts',
      value: criticalAlertCount.toString(),
      trend: '9% vs yesterday',
      trendUp: true,
      trendPositive: false, // critical alerts up is red
      icon: AlertOctagon,
      iconBg: 'bg-red-500',
    },
    {
      id: 'cctv',
      label: 'CCTV Online',
      value: cctvOnlineCount.toString(),
      trend: '5% vs yesterday',
      trendUp: true,
      trendPositive: true,
      icon: Video,
      iconBg: 'bg-purple-600',
    },
    {
      id: 'response',
      label: 'Avg. Response Time',
      value: '18 min',
      trend: '4 min vs yesterday',
      trendUp: false,
      trendPositive: true, // response time decreasing is good
      icon: Timer,
      iconBg: 'bg-teal-600',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-4 select-none">
      {kpis.map((kpi) => {
        const Icon = kpi.icon;
        return (
          <div
            key={kpi.id}
            className="bg-white border border-slate-200/90 rounded-2xl p-3.5 shadow-sm flex items-center gap-3.5 hover:shadow-md hover:border-slate-300 transition-all"
          >
            {/* Round Icon */}
            <div className={`w-11 h-11 rounded-full ${kpi.iconBg} text-white flex items-center justify-center shrink-0 shadow-sm`}>
              <Icon className="w-5 h-5" />
            </div>

            {/* Content */}
            <div className="min-w-0 flex-1">
              <p className="text-[11.5px] font-medium text-slate-500 truncate">
                {kpi.label}
              </p>
              <h2 className="text-xl font-extrabold tracking-tight text-slate-900 leading-tight">
                {kpi.value}
              </h2>
              <div className="flex items-center gap-1 mt-0.5">
                {kpi.trendUp ? (
                  <ArrowUp className={`w-3 h-3 ${kpi.trendPositive ? 'text-emerald-500' : 'text-red-500'}`} />
                ) : (
                  <ArrowDown className={`w-3 h-3 ${kpi.trendPositive ? 'text-emerald-500' : 'text-red-500'}`} />
                )}
                <span className={`text-[10px] font-semibold ${kpi.trendPositive ? 'text-emerald-500' : 'text-red-500'}`}>
                  {kpi.trend}
                </span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
