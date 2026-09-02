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
    <aside className="w-72 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between p-3.5 select-none h-screen max-h-screen overflow-y-auto">
      {/* Top Section: Logo & Left-Aligned Navigation */}
      <div className="w-full">
        {/* Brand Logo Header */}
        <div className="flex flex-col items-center px-1 pt-1 pb-3.5 mb-3 border-b border-slate-200/80">
          <img
            src="/inetra-logo.png"
            alt="INETRA Unified Urban Sensing Platform"
            className="w-48 h-auto object-contain cursor-pointer"
          />
        </div>

        {/* 2X Font Size Left-Aligned Navigation List */}
        <nav className="space-y-1 w-full text-left">
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
                className={`w-full flex items-center justify-start gap-4 px-4 py-2.5 text-[18px] transition-colors text-left rounded-none border-l-4 ${
                  isActive
                    ? 'border-sky-600 bg-sky-50/90 text-sky-900 font-bold shadow-2xs'
                    : 'border-transparent text-slate-700 hover:text-slate-900 hover:bg-slate-50/90 font-medium'
                }`}
              >
                <Icon className={`w-5.5 h-5.5 shrink-0 ${isActive ? 'text-sky-600' : 'text-slate-500'}`} />
                <span className="leading-tight truncate">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section: Clock Card */}
      <div className="pt-3 border-t border-slate-200/80">
        <div className="bg-slate-50 text-slate-800 rounded-none p-3 border border-slate-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-slate-600">
              <Clock className="w-4 h-4 text-sky-600" />
              <span className="text-sm font-mono font-bold text-slate-900">{timeStr || '10:24 AM'}</span>
            </div>
            <span className="text-xs font-semibold text-slate-500">
              {dateStr || '01 Jun 2025'}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
