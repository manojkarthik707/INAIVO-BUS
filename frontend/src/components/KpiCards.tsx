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
      trendPositive: false,
      icon: AlertOctagon,
      iconBg: 'bg-red-600',
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
      trendPositive: true,
      icon: Timer,
      iconBg: 'bg-teal-600',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2.5 mb-3.5 select-none">
      {kpis.map((kpi) => {
        const Icon = kpi.icon;
        return (
          <div
            key={kpi.id}
            className="bg-white border border-slate-200 p-3 rounded-none shadow-2xs hover:border-slate-300 transition-colors flex items-center gap-3"
          >
            {/* Square Icon Box */}
            <div className={`w-9 h-9 ${kpi.iconBg} text-white flex items-center justify-center shrink-0 rounded-none`}>
              <Icon className="w-4 h-4" />
            </div>

            {/* Metric Content */}
            <div className="min-w-0 flex-1">
              <p className="text-[11px] font-medium text-slate-500 truncate uppercase tracking-wider">
                {kpi.label}
              </p>
              <h2 className="text-lg font-bold tracking-tight text-slate-900 leading-tight">
                {kpi.value}
              </h2>
              <div className="flex items-center gap-1 mt-0.5">
                {kpi.trendUp ? (
                  <ArrowUp className={`w-2.5 h-2.5 ${kpi.trendPositive ? 'text-emerald-600' : 'text-red-600'}`} />
                ) : (
                  <ArrowDown className={`w-2.5 h-2.5 ${kpi.trendPositive ? 'text-emerald-600' : 'text-red-600'}`} />
                )}
                <span className={`text-[9.5px] font-semibold ${kpi.trendPositive ? 'text-emerald-600' : 'text-red-600'}`}>
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
