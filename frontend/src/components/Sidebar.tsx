import { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Map, 
  Bus, 
  AlertTriangle, 
  AlertOctagon, 
  Activity, 
  BarChart3, 
  Video, 
  FileText, 
  Settings, 
  ShieldCheck, 
  Clock 
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  openStreamModal?: () => void;
}

export default function Sidebar({ activeTab, setActiveTab, openStreamModal }: SidebarProps) {
  const [timeStr, setTimeStr] = useState('');
  const [dateStr, setDateStr] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }));
      setDateStr(now.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'live-map', label: 'Live Map', icon: Map },
    { id: 'buses', label: 'Buses', icon: Bus },
    { id: 'alerts', label: 'Alerts', icon: AlertTriangle },
    { id: 'incidents', label: 'Incidents', icon: AlertOctagon },
    { id: 'road-conditions', label: 'Road Conditions', icon: Activity },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'cctv-feeds', label: 'CCTV Feeds', icon: Video },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-60 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between p-3 select-none h-screen max-h-screen overflow-y-auto">
      {/* Top Section: Logo & Navigation */}
      <div>
        {/* Brand Logo Header */}
        <div className="flex flex-col items-center px-1 pt-1 pb-3 mb-3 border-b border-slate-200/80">
          <img
            src="/inetra-logo.png"
            alt="INETRA Unified Urban Sensing Platform"
            className="w-40 h-auto object-contain cursor-pointer"
          />
        </div>

        {/* Square Navigation List */}
        <nav className="space-y-0.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  if (item.id === 'cctv-feeds' && openStreamModal) {
                    openStreamModal();
                  }
                }}
                className={`w-full flex items-center gap-3 px-3 py-2 text-[13px] transition-colors text-left rounded-none border-l-2 ${
                  isActive
                    ? 'border-sky-600 bg-sky-50/80 text-sky-900 font-semibold'
                    : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-normal'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-sky-600' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section: Square Status & Clock Cards */}
      <div className="space-y-2 pt-3 border-t border-slate-200/80">
        {/* System Status Card (Square) */}
        <div className="bg-slate-900 text-white rounded-none p-3 border border-slate-800">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] font-semibold tracking-wider text-slate-300 uppercase">System Status</span>
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 bg-emerald-500"></span>
            </span>
            <span className="text-[11.5px] font-medium text-emerald-400 font-mono">ALL SYSTEMS ONLINE</span>
          </div>
        </div>

        {/* Live Clock Card (Square) */}
        <div className="bg-slate-50 text-slate-800 rounded-none p-2.5 border border-slate-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-slate-600">
              <Clock className="w-3.5 h-3.5 text-sky-600" />
              <span className="text-xs font-mono font-bold text-slate-900">{timeStr || '10:24 AM'}</span>
            </div>
            <span className="text-[10.5px] font-medium text-slate-500">
              {dateStr || '01 Jun 2025'}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
