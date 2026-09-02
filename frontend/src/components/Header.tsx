import { useState } from 'react';
import { MapPin, Calendar, Bell, ChevronDown, User } from 'lucide-react';

interface HeaderProps {
  unreadAlertCount?: number;
}

export default function Header({ unreadAlertCount = 3 }: HeaderProps) {
  const [selectedCity, setSelectedCity] = useState('Chennai');
  const [selectedTimeRange, setSelectedTimeRange] = useState('Last 24 Hours');
  const [showCityMenu, setShowCityMenu] = useState(false);
  const [showTimeMenu, setShowTimeMenu] = useState(false);

  const cities = ['Chennai', 'Coimbatore', 'Bengaluru', 'Hyderabad', 'Mumbai'];
  const timeRanges = ['Last 1 Hour', 'Last 6 Hours', 'Last 24 Hours', 'Last 7 Days', 'All Time'];

  return (
    <header className="flex items-center justify-between py-1.5 px-1 mb-3.5 select-none border-b border-slate-200/80 pb-3">
      {/* Title & Subtitle */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-slate-900 leading-tight">
          Dashboard
        </h1>
        <p className="text-xs text-slate-500 font-medium">
          Real-time overview of urban intelligence
        </p>
      </div>

      {/* Right Action Controls (Square-based) */}
      <div className="flex items-center gap-2.5">
        {/* City Filter Dropdown (Square) */}
        <div className="relative">
          <button
            onClick={() => { setShowCityMenu(!showCityMenu); setShowTimeMenu(false); }}
            className="flex items-center gap-2 bg-white border border-slate-200 hover:border-slate-300 px-3 py-1.5 rounded-none text-xs font-semibold text-slate-700 shadow-2xs transition-colors"
          >
            <MapPin className="w-3.5 h-3.5 text-sky-600" />
            <span>{selectedCity}</span>
            <ChevronDown className="w-3 h-3 text-slate-400 ml-1" />
          </button>

          {showCityMenu && (
            <div className="absolute right-0 mt-1 w-36 bg-white border border-slate-200 rounded-none shadow-md z-50 py-1">
              {cities.map((city) => (
                <button
                  key={city}
                  onClick={() => { setSelectedCity(city); setShowCityMenu(false); }}
                  className={`w-full text-left px-3 py-1.5 text-xs font-medium hover:bg-slate-50 transition-colors ${
                    selectedCity === city ? 'text-sky-600 font-bold bg-sky-50/50' : 'text-slate-600'
                  }`}
                >
                  {city}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Timeframe Filter Dropdown (Square) */}
        <div className="relative">
          <button
            onClick={() => { setShowTimeMenu(!showTimeMenu); setShowCityMenu(false); }}
            className="flex items-center gap-2 bg-white border border-slate-200 hover:border-slate-300 px-3 py-1.5 rounded-none text-xs font-semibold text-slate-700 shadow-2xs transition-colors"
          >
            <Calendar className="w-3.5 h-3.5 text-sky-600" />
            <span>{selectedTimeRange}</span>
            <ChevronDown className="w-3 h-3 text-slate-400 ml-1" />
          </button>

          {showTimeMenu && (
            <div className="absolute right-0 mt-1 w-40 bg-white border border-slate-200 rounded-none shadow-md z-50 py-1">
              {timeRanges.map((range) => (
                <button
                  key={range}
                  onClick={() => { setSelectedTimeRange(range); setShowTimeMenu(false); }}
                  className={`w-full text-left px-3 py-1.5 text-xs font-medium hover:bg-slate-50 transition-colors ${
                    selectedTimeRange === range ? 'text-sky-600 font-bold bg-sky-50/50' : 'text-slate-600'
                  }`}
                >
                  {range}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Notification Bell (Square) */}
        <div className="relative">
          <button className="w-8 h-8 flex items-center justify-center bg-white border border-slate-200 hover:border-slate-300 rounded-none text-slate-600 hover:text-slate-900 shadow-2xs transition-colors">
            <Bell className="w-3.5 h-3.5" />
          </button>
          {unreadAlertCount > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-600 text-white font-bold text-[9px] w-3.5 h-3.5 rounded-none flex items-center justify-center shadow-xs">
              {unreadAlertCount}
            </span>
          )}
        </div>

        {/* User Profile Avatar (Square) */}
        <button className="w-8 h-8 flex items-center justify-center bg-slate-100 border border-slate-200 rounded-none text-slate-700 shadow-2xs hover:border-slate-300 transition-colors">
          <User className="w-3.5 h-3.5" />
        </button>
      </div>
    </header>
  );
}
