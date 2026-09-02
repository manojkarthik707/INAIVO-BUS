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
      setDateStr(now.toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' }));
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
    <aside className="w-64 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between p-4 select-none h-screen max-h-screen overflow-y-auto">
      {/* Top Section: Logo & Navigation */}
      <div>
        {/* Brand Logo */}
        <div className="flex flex-col items-center px-1 pt-1 pb-3 mb-3 border-b border-slate-100">
          <img
            src="/inetra-logo.png"
            alt="INETRA Unified Urban Sensing Platform"
            className="w-44 h-auto object-contain drop-shadow-xs hover:scale-102 transition-transform duration-200 cursor-pointer"
          />
        </div>

        {/* Navigation List */}
        <nav className="space-y-1">
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
                className={`w-full flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl font-medium text-[13.5px] transition-all text-left ${
                  isActive
                    ? 'bg-gradient-to-r from-sky-600 via-cyan-600 to-teal-500 text-white font-semibold shadow-md shadow-sky-600/20'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section: Status & Clock Cards */}
      <div className="space-y-2.5 pt-4">
        {/* System Status Card */}
        <div className="bg-gradient-to-br from-cyan-600 via-teal-600 to-sky-700 text-white rounded-2xl p-3.5 shadow-md shadow-teal-700/15">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-semibold tracking-wide text-cyan-100">System Status</span>
            <ShieldCheck className="w-4 h-4 text-emerald-300" />
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-300 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
            </span>
            <span className="text-[11.5px] font-medium text-white">All Systems Operational</span>
          </div>
        </div>

        {/* Live Clock Card */}
        <div className="bg-gradient-to-br from-sky-700 via-cyan-700 to-teal-800 text-white rounded-2xl p-3.5 shadow-md shadow-sky-800/15">
          <div className="flex items-center gap-2 mb-0.5">
            <Clock className="w-4 h-4 text-cyan-300" />
            <span className="text-sm font-bold tracking-tight">{timeStr || '10:24 AM'}</span>
          </div>
          <p className="text-[11px] text-cyan-100/90 font-medium pl-6">
            {dateStr || '01 June 2025'}
          </p>
        </div>
      </div>
    </aside>
  );
}
