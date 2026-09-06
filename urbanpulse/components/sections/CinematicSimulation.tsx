"use client";

import { useEffect, useRef, useState, Suspense } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import dynamic from "next/dynamic";
import { SelectedAssetData } from "@/components/three/SelectionHighlight";
import AssetFeedDrawer from "@/components/ui/AssetFeedDrawer";

// Dynamically import the R3F scene to avoid SSR issues
const SmartCityScene = dynamic(() => import("@/components/three/SmartCityScene"), {
  ssr: false,
  loading: () => (
    <div
      className="w-full h-full flex items-center justify-center"
      style={{ background: "var(--bg-base)" }}
    >
      <div className="text-center">
        <div
          className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto mb-3"
        />
        <p className="label-text" style={{ color: "var(--accent-cyan)" }}>
          Initializing Scene
        </p>
      </div>
    </div>
  ),
});

// ─── Scene stages for UI overlay ─────────────────────────────
const STAGES = [
  {
    range: [0.00, 0.12],
    title: "EDGE AI",
    subtitle: "Intelligence begins at the edge. Real-time perception runs directly across buses and existing city cameras.",
  },
  {
    range: [0.12, 0.25],
    title: "EVENT GENERATION",
    subtitle: "Every frame becomes an event. Raw visual observations transform into structured event markers.",
  },
  {
    range: [0.25, 0.38],
    title: "CONFIDENCE & VERIFICATION",
    subtitle: "Independent observations build confidence. Multiple observations progressively validate hazards.",
  },
  {
    range: [0.38, 0.50],
    title: "MESH SYSTEM",
    subtitle: "The fleet becomes a distributed sensing network, communicating seamlessly across the city.",
  },
  {
    range: [0.50, 0.63],
    title: "ACTIONABLE ALERTS",
    subtitle: "Verified intelligence reaches the people who can act. High-risk alerts are escalated instantly.",
  },
  {
    range: [0.63, 0.75],
    title: "TRAFFIC ANALYSIS",
    subtitle: "Individual events become city-wide intelligence. Real-time traffic patterns emerge.",
  },
  {
    range: [0.75, 0.88],
    title: "INSIGHTS & REPORTS",
    subtitle: "Intelligence becomes action. Data patterns drive maintenance scheduling and route optimization.",
  },
  {
    range: [0.88, 1.00],
    title: "ONE URBAN INTELLIGENCE LAYER",
    subtitle: "Discover. Corroborate. Understand. Act. All streams converge into the persistent city database.",
  },
];

function useScrollProgress(containerRef: React.RefObject<HTMLDivElement | null>, mode: "parallax" | "360") {
  const progressRef = useRef(0);
  const [stageIndex, setStageIndex] = useState(0);

  useEffect(() => {
    if (!containerRef.current || mode !== "parallax") return;

    gsap.registerPlugin(ScrollTrigger);

    const trigger = ScrollTrigger.create({
      trigger: containerRef.current,
      start: "top top",
      end: "bottom bottom",
      scrub: 0.8,
      onUpdate: (self) => {
        progressRef.current = self.progress;
        const newStage = STAGES.findIndex(
          (s) => self.progress >= s.range[0] && self.progress < s.range[1]
        );
        if (newStage !== -1) {
          setStageIndex(newStage);
        } else if (self.progress >= 0.94) {
          setStageIndex(STAGES.length - 1);
        }
      },
    });

    return () => trigger.kill();
  }, [containerRef, mode]);

  return { progressRef, stageIndex };
}

export default function CinematicSimulation() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mode, setMode] = useState<"parallax" | "360">("parallax");
  const [selectedAsset, setSelectedAsset] = useState<SelectedAssetData | null>(null);

  const { progressRef, stageIndex } = useScrollProgress(containerRef, mode);
  const currentStage = STAGES[stageIndex];

  const handleQuickSelect = (id: string) => {
    if (id === "truck-dp") {
      setSelectedAsset({
        id: "truck-dp",
        name: "DOUBLE PARKING",
        category: "VEHICLE",
        position: [4.8, 1.6, -10],
        size: [2.5, 3.2, 7.2],
        status: "VIOLATION",
        statusColor: "#ff4d4d",
        description: "Just one double parked vehicle can increase the likelihood of crashes and wreaks havoc on traffic and public transit on-time performance.",
        metrics: [
          { label: "LICENSE PLATE", value: "KA-01-EQ-9182" },
          { label: "VIOLATION TIME", value: "14 MINS EXCEEDED" },
          { label: "SPEED", value: "0.0 KM/H (PARKED)" },
          { label: "CONFIDENCE", value: "98.7% EDGE AI" },
        ],
        details: [
          "Blocking Lane #2 right shoulder",
          "Bus 017 trajectory obstructed",
          "Citation auto-generated to RTO database",
        ],
      });
    } else if (id === "lamp-sl-01") {
      setSelectedAsset({
        id: "lamp-sl-01",
        name: "SMART LAMP S-04",
        category: "INFRASTRUCTURE",
        position: [-7, 6.2, -5],
        size: [2.0, 6.5, 1.2],
        status: "ACTIVE",
        statusColor: "#00d4ff",
        description: "Connected IoT streetlight equipped with ambient light sensors, power metering, and edge AI optical node.",
        metrics: [
          { label: "POWER DRAW", value: "42 W (DIMMED 70%)" },
          { label: "SENSOR STATE", value: "HEALTHY (100%)" },
          { label: "NETWORK", value: "5G EDGE · 12 ms" },
          { label: "RUNTIME", value: "14,280 HRS" },
        ],
        details: [
          "Automatic light dimming based on traffic density",
          "Acoustic anomaly detector active",
          "Connected to District Grid-04",
        ],
      });
    } else if (id === "building-b1") {
      setSelectedAsset({
        id: "building-b1",
        name: "Residential Tower B",
        category: "BUILDING",
        position: [22, 10, -20],
        size: [8.5, 20.5, 15.5],
        status: "MONITORED",
        statusColor: "#f59e0b",
        description: "Multi-story residential apartment structure with integrated solar facade panels and AI building management.",
        metrics: [
          { label: "HEIGHT", value: "60 METERS" },
          { label: "EST. OCCUPANCY", value: "92%" },
          { label: "ENERGY RATING", value: "A+ SMART GRID" },
          { label: "BALCONIES", value: "18 UNITS FRAMED" },
        ],
        details: [
          "Solar facade generation: 18.6 kWh",
          "HVAC load optimized by AI twin",
          "Air Quality Index (AQI): 38 (EXCELLENT)",
        ],
      });
    } else if (id === "bus-017") {
      setSelectedAsset({
        id: "bus-017",
        name: "Autonomous Bus 017",
        category: "VEHICLE",
        position: [-2, 1.8, 30],
        size: [2.8, 3.2, 8.5],
        status: "ACTIVE",
        statusColor: "#00d4ff",
        description: "Mobile sensing platform equipped with dual front dashcams, LiDAR, and edge inference module parsing road hazards in real-time.",
        metrics: [
          { label: "PASSENGERS", value: "24 / 40" },
          { label: "ROUTE", value: "ROUTE #14 - CENTRAL" },
          { label: "SPEED", value: "32 KM/H" },
          { label: "EDGE INFERENCE", value: "18.2 FPS" },
        ],
        details: [
          "Onboard AI running local edge detection",
          "Pothole #PO-142 detected & transmitted",
          "5G Event Sync active",
        ],
      });
    }
  };

  return (
    <section
      id="simulation"
      ref={containerRef}
      className="relative w-full"
      style={{ height: mode === "parallax" ? "700vh" : "100vh" }}
    >
      {/* Sticky canvas container */}
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        {/* R3F 3D scene */}
        <div className="absolute inset-0 z-0">
          <SmartCityScene
            progressRef={progressRef}
            mode={mode}
            selectedAsset={selectedAsset}
            onSelectAsset={setSelectedAsset}
          />
        </div>

        {/* ─── Left Asset Feed Drawer UI (Removed as requested) ─── */}

        {/* ─── Mode Toggle Button ─── */}
        <div className="absolute top-6 right-6 z-50">
          <button
            onClick={() => setMode(mode === "parallax" ? "360" : "parallax")}
            className="flex items-center gap-3 px-5 py-2.5 rounded-full transition-all duration-300 hover:scale-105"
            style={{
              background: "rgba(5,8,16,0.85)",
              border: "1px solid rgba(0,212,255,0.4)",
              backdropFilter: "blur(12px)",
              color: "white",
              fontWeight: 500,
              boxShadow: "0 4px 20px rgba(0, 212, 255, 0.15)"
            }}
          >
            <div
              className="w-2.5 h-2.5 rounded-full"
              style={{
                background: mode === "360" ? "var(--accent-cyan)" : "#777",
                boxShadow: mode === "360" ? "0 0 10px var(--accent-cyan)" : "none",
              }}
            />
            <span>360° MODE</span>
          </button>
        </div>

        {/* ─── UI Overlay (360 Mode) ─── */}
        {mode === "360" && (
          <div className="absolute inset-0 pointer-events-none z-10 flex flex-col justify-between">
            <div className="flex justify-center pt-24">
              <div
                className="flex items-center gap-2 px-4 py-1.5 rounded-full"
                style={{
                  background: "rgba(0,212,255,0.1)",
                  border: "1px solid rgba(0,212,255,0.25)",
                  backdropFilter: "blur(8px)",
                }}
              >
                <span className="w-1.5 h-1.5 rounded-full animate-pulse bg-cyan-400" />
                <span className="label-text text-cyan-400">
                  URBANPULSE FUSION · INTERACTIVE 360° SNAPSHOT
                </span>
              </div>
            </div>
            <div className="flex justify-center pb-8">
              <div 
                className="text-white/50 text-sm font-mono tracking-widest px-6 py-2 rounded-lg"
                style={{ background: "rgba(0,0,0,0.4)", backdropFilter: "blur(4px)" }}
              >
                [ LEFT CLICK OBJECT TO SELECT ] [ DRAG TO ROTATE ] [ SCROLL TO ZOOM ]
              </div>
            </div>
          </div>
        )}

        {/* ─── UI Overlay (Parallax Mode) ─── */}
        {mode === "parallax" && (
          <div className="absolute inset-0 pointer-events-none z-10">
            {/* Top section label */}
            <div className="absolute top-6 left-1/2 -translate-x-1/2">
              <div
                className="flex items-center gap-2 px-4 py-1.5 rounded-full"
                style={{
                  background: "rgba(0,212,255,0.1)",
                  border: "1px solid rgba(0,212,255,0.25)",
                }}
              >
                <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "var(--accent-cyan)" }} />
                <span className="label-text" style={{ color: "var(--accent-cyan)" }}>
                  URBANPULSE FUSION · LIVE SIMULATION
                </span>
              </div>
            </div>

            {/* HUD overlays removed as requested */}

            {/* Center narrative text (only when asset is not blocking center) */}
            {!selectedAsset && (
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center w-full max-w-3xl px-8 pointer-events-none">
                <h2
                  className="font-heading text-4xl lg:text-6xl font-bold mb-6 tracking-tight drop-shadow-2xl"
                  style={{
                    background: "linear-gradient(180deg, #FFFFFF 0%, rgba(255,255,255,0.6) 100%)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                  }}
                >
                  {currentStage.title}
                </h2>
                <p className="text-lg lg:text-xl text-white/80 font-medium drop-shadow-lg mx-auto max-w-2xl leading-relaxed">
                  {currentStage.subtitle}
                </p>
              </div>
            )}

            {/* Progress indicator */}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2">
              {STAGES.map((_, i) => (
                <div
                  key={i}
                  className="h-1 rounded-full transition-all duration-300"
                  style={{
                    width: i === stageIndex ? "24px" : "8px",
                    background: i === stageIndex ? "var(--accent-cyan)" : "rgba(255,255,255,0.2)",
                  }}
                />
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
