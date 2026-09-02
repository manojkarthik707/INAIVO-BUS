import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import KpiCards from './components/KpiCards';
import MapView from './components/MapView';
import FleetStatusCard from './components/FleetStatusCard';
import TopLocationsCard from './components/TopLocationsCard';
import LiveCctvSnapshots from './components/LiveCctvSnapshots';
import EventBreakdownCard from './components/EventBreakdownCard';
import EventsOverTimeCard from './components/EventsOverTimeCard';
import RecentAlertsCard from './components/RecentAlertsCard';
import LiveStreamModal from './components/LiveStreamModal';

interface BusTelemetry {
  sim_x: number;
  sim_y: number;
  speed: number;
  latitude?: number;
  longitude?: number;
}

interface EventItem {
  event_id?: string;
  event_type: string;
  severity: string;
  confidence?: number;
  timestamp: string;
  location?: { latitude: number; longitude: number };
  metadata?: any;
  source?: any;
  evidence_image?: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedBus, setSelectedBus] = useState('BUS_01');
  const [isStreamModalOpen, setIsStreamModalOpen] = useState(false);

  const [allBuses, setAllBuses] = useState<Record<string, BusTelemetry>>({
    BUS_01: { sim_x: 4.36, sim_y: 53.21, speed: 32 },
    BUS_02: { sim_x: -113.21, sim_y: 5.04, speed: 30 },
    BUS_03: { sim_x: 36.79, sim_y: -34.25, speed: 28 },
  });

  const [events, setEvents] = useState<EventItem[]>([]);

  // Fetch initial events from backend
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/events')
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setEvents(data);
        }
      })
      .catch(() => {});
  }, []);

  // Real-time WebSocket connection to backend
  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimeout: ReturnType<typeof setTimeout>;

    const connect = () => {
      ws = new WebSocket('ws://127.0.0.1:8000/ws/events');

      ws.onmessage = (msg) => {
        try {
          const data = JSON.parse(msg.data);

          if (data.type === 'TELEMETRY' && data.bus_id) {
            setAllBuses((prev) => ({
              ...prev,
              [data.bus_id]: {
                sim_x: data.sim_x ?? prev[data.bus_id]?.sim_x ?? 0,
                sim_y: data.sim_y ?? prev[data.bus_id]?.sim_y ?? 0,
                speed: data.speed ?? 30,
                latitude: data.latitude,
                longitude: data.longitude,
              },
            }));
          } else if (data.event_type) {
            setEvents((prev) => [data, ...prev.slice(0, 49)]);
          }
        } catch (e) {
          console.error('WS Parse Error:', e);
        }
      };

      ws.onclose = () => {
        reconnectTimeout = setTimeout(connect, 3000);
      };

      ws.onerror = () => {
        ws?.close();
      };
    };

    connect();

    return () => {
      clearTimeout(reconnectTimeout);
      ws?.close();
    };
  }, []);

  const openStream = (busId?: string) => {
    if (busId) setSelectedBus(busId);
    setIsStreamModalOpen(true);
  };

  return (
    <div className="flex h-screen max-h-screen overflow-hidden bg-slate-100/70 font-sans text-slate-800">
      {/* Left Sidebar */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        openStreamModal={() => openStream(selectedBus)}
      />

      {/* Main Content Area */}
      <main className="flex-1 min-w-0 flex flex-col p-3.5 overflow-y-auto max-h-screen">
        {/* Top Header */}
        <Header unreadAlertCount={Math.max(3, events.length > 0 ? 4 : 3)} />

        {/* 6 Top Metric KPI Cards */}
        <KpiCards
          activeBusCount={60}
          totalEventCount={346 + events.length}
          criticalAlertCount={23}
          cctvOnlineCount={312}
        />

        {/* Dashboard 2-Column Grid (Square-based) */}
        <div className="grid grid-cols-12 gap-3 flex-1 min-h-0">
          {/* Left Column (8 Columns: Heatmap + Fleet & Locations + CCTV Snapshots) */}
          <div className="col-span-12 xl:col-span-8 flex flex-col gap-3 min-h-0">
            {/* Road Issues Heatmap Card */}
            <div className="h-80 xl:h-88">
              <MapView
                busLocation={allBuses[selectedBus] || null}
                events={events}
                selectedBus={selectedBus}
                allBuses={allBuses}
                onSelectBus={(bId) => {
                  setSelectedBus(bId);
                  openStream(bId);
                }}
              />
            </div>

            {/* Middle Row: Fleet Status (Donut) & Top Locations (Bar Chart) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 h-48">
              <FleetStatusCard total={128} />
              <TopLocationsCard />
            </div>

            {/* Bottom Row: Live CCTV Snapshot Horizontal Gallery */}
            <div>
              <LiveCctvSnapshots
                selectedBus={selectedBus}
                setSelectedBus={setSelectedBus}
                openStreamModal={openStream}
              />
            </div>
          </div>

          {/* Right Column (4 Columns: Event Breakdown + Events Over Time + Recent Alerts) */}
          <div className="col-span-12 xl:col-span-4 flex flex-col gap-3 min-h-0">
            {/* Event Breakdown Donut Card */}
            <EventBreakdownCard total={346 + events.length} />

            {/* Events Over Time Spline Chart */}
            <EventsOverTimeCard />

            {/* Recent Alerts Feed */}
            <RecentAlertsCard events={events} />
          </div>
        </div>
      </main>

      {/* Full Live Stream & AI Sensing Modal */}
      <LiveStreamModal
        isOpen={isStreamModalOpen}
        onClose={() => setIsStreamModalOpen(false)}
        selectedBus={selectedBus}
        setSelectedBus={setSelectedBus}
        events={events}
      />
    </div>
  );
}
