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
  Clock,
  PanelLeftClose,
  PanelLeftOpen
} from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  openStreamModal?: () => void;
  isCollapsed?: boolean;
  setIsCollapsed?: (collapsed: boolean | ((prev: boolean) => boolean)) => void;
}

export default function Sidebar({
  activeTab,
  setActiveTab,
  openStreamModal,
  isCollapsed: controlledCollapsed,
  setIsCollapsed: setControlledCollapsed,
}: SidebarProps) {
  const [internalCollapsed, setInternalCollapsed] = useState(false);
  const isCollapsed = controlledCollapsed !== undefined ? controlledCollapsed : internalCollapsed;
  const toggleCollapse = () => {
    if (setControlledCollapsed) {
      setControlledCollapsed((prev) => !prev);
    } else {
      setInternalCollapsed((prev) => !prev);
    }
  };

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
    <aside
      className={`shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between select-none h-screen max-h-screen overflow-y-auto transition-all duration-300 ease-in-out ${
        isCollapsed ? 'w-20 p-2.5' : 'w-72 p-3.5'
      }`}
    >
      {/* Top Section: Logo, Collapse Toggle & Navigation */}
      <div className="w-full">
        {/* Header with Logo and Retract Toggle Button */}
        <div className={`flex items-center pb-3 mb-3 border-b border-slate-200/80 ${isCollapsed ? 'flex-col gap-2 justify-center' : 'justify-between px-1 pt-1'}`}>
          {!isCollapsed ? (
            <>
              <img
                src="/inetra-logo.png"
                alt="INETRA"
                className="w-44 h-auto object-contain cursor-pointer"
              />
              <button
                onClick={toggleCollapse}
                title="Retract sidebar"
                className="p-1.5 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-none transition-colors"
              >
                <PanelLeftClose className="w-5 h-5" />
              </button>
            </>
          ) : (
            <button
              onClick={toggleCollapse}
              title="Expand sidebar"
              className="w-full flex flex-col items-center justify-center p-2 text-sky-600 hover:bg-sky-50 transition-colors border border-slate-200"
            >
              <PanelLeftOpen className="w-6 h-6" />
              <span className="text-[9px] font-bold mt-1 text-slate-600 uppercase tracking-wider">Expand</span>
            </button>
          )}
        </div>

        {/* Navigation List */}
        <nav className="space-y-1 w-full text-left">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                title={item.label}
                onClick={() => {
                  setActiveTab(item.id);
                  if (item.id === 'cctv-feeds' && openStreamModal) {
                    openStreamModal();
                  }
                }}
                className={`w-full flex items-center transition-colors text-left rounded-none ${
                  isCollapsed
                    ? 'justify-center p-3 border-l-0'
                    : 'justify-start gap-4 px-4 py-2.5 text-[18px] border-l-4'
                } ${
                  isActive
                    ? 'border-sky-600 bg-sky-50/90 text-sky-900 font-bold shadow-2xs'
                    : 'border-transparent text-slate-700 hover:text-slate-900 hover:bg-slate-50/90 font-medium'
                }`}
              >
                <Icon className={`shrink-0 ${isCollapsed ? 'w-6 h-6' : 'w-5.5 h-5.5'} ${isActive ? 'text-sky-600' : 'text-slate-500'}`} />
                {!isCollapsed && <span className="leading-tight truncate">{item.label}</span>}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Section: Clock Widget */}
      <div className="pt-3 border-t border-slate-200/80">
        {!isCollapsed ? (
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
        ) : (
          <div className="flex flex-col items-center justify-center p-2 bg-slate-50 border border-slate-200 text-slate-700 text-center">
            <Clock className="w-4 h-4 text-sky-600 mb-1" />
            <span className="text-[10px] font-mono font-bold leading-tight">{timeStr || '10:24 AM'}</span>
          </div>
        )}
      </div>
    </aside>
  );
}
