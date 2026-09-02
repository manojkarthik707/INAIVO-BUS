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
        <div className="flex items-center gap-3 px-2 py-2 mb-6">
          <div className="relative w-10 h-10 flex items-center justify-center">
            {/* Eye / Radar Sensing Logo Mark */}
            <svg viewBox="0 0 44 44" className="w-10 h-10 drop-shadow-sm">
              <defs>
                <linearGradient id="inetraGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#0284c7" />
                </linearGradient>
              </defs>
              <polygon points="22,3 41,22 22,41 3,22" fill="none" stroke="url(#inetraGrad)" strokeWidth="2.5" />
              <circle cx="22" cy="22" r="12" fill="none" stroke="#0ea5e9" strokeWidth="2" strokeDasharray="3 2" />
              <circle cx="22" cy="22" r="6" fill="url(#inetraGrad)" />
              <path d="M14 22 Q22 12 30 22 Q22 32 14 22 Z" fill="none" stroke="#0369a1" strokeWidth="1.5" />
              {/* Skyline subtle bars */}
              <rect x="18" y="16" width="2" height="6" fill="#ffffff" rx="0.5" />
              <rect x="21" y="14" width="2" height="8" fill="#ffffff" rx="0.5" />
              <rect x="24" y="17" width="2" height="5" fill="#ffffff" rx="0.5" />
            </svg>
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight text-slate-900 leading-none">
              INETRA
            </h1>
            <p className="text-[8.5px] font-bold tracking-wider text-sky-600 uppercase mt-0.5">
              UNIFIED URBAN SENSING PLATFORM
            </p>
          </div>
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
