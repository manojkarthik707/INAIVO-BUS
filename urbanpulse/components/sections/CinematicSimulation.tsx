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
    range: [0, 0.1],
    title: "Transportation Intelligence,\nRoad by Road.",
    subtitle: "One AI layer across moving cameras, roadside cameras and existing CCTV.",
    hud: null,
    card: null,
  },
  {
    range: [0.1, 0.3],
    title: "Mobile Perception",
    subtitle: "Every bus becomes a city sensor. AI runs onboard — only events are transmitted.",
    hud: {
      camera: "BUS-017 FRONT CAM",
      gps: "12.9716° N, 77.5946° E",
      time: "10:31:22",
      inference: "EDGE",
      upload: "EVENT ONLY",
    },
    card: {
      title: "Moving Camera Intelligence",
      items: ["Road defect detection", "Lane marking analysis", "Vehicle classification", "Pedestrian monitoring"],
    },
  },
  {
    range: [0.3, 0.43],
    title: "Urban Memory",
    subtitle: "One detection is an observation. Two independent cameras make it a pattern. Three confirm truth.",
    hud: null,
    card: {
      title: "Fleet Consensus Engine",
      items: ["Obs #1: BUS-017 → Conf 0.71", "Obs #2: BUS-023 → Conf 0.86", "Match: 92% · Independent: 2", "→ URBAN OBJECT CREATED"],
    },
  },
  {
    range: [0.43, 0.58],
    title: "Fixed Camera Continuity",
    subtitle: "Moving cameras provide coverage. Fixed cameras provide continuity.",
    hud: {
      camera: "JUNCTION-CAM-04",
      gps: "12.9718° N, 77.5941° E",
      time: "10:31:55",
      inference: "EDGE",
      upload: "CONTINUOUS",
    },
    card: {
      title: "Junction Intelligence",
      items: ["Queue length: 14 vehicles", "Traffic density: HIGH", "Near-miss detected", "Pedestrian trajectory tracked"],
    },
  },
  {
    range: [0.58, 0.72],
    title: "Existing CCTV Integration",
    subtitle: "Reuse the cameras the city already owns. No replacement needed.",
    hud: null,
    card: {
      title: "Camera Integration Status",
      items: [
        "EXISTING-CCTV-04 ✓ Compatible",
        "EXISTING-CCTV-12 ✓ Compatible",
        "JUNCTION-CAM-02 ✓ Active",
        "BUS-017 ✓ Live Edge",
      ],
    },
  },
  {
    range: [0.72, 0.86],
    title: "Incident Reconstruction",
    subtitle: "Agentic AI traces evidence across camera networks — with explicit confidence and uncertainty.",
    hud: {
      camera: "INCIDENT AGENT",
      gps: "ACTIVE SEARCH",
      time: "10:31:22",
      inference: "CLOUD",
      upload: "EVIDENCE CLIP",
    },
    card: {
      title: "Evidence Candidate — 91% Match",
      items: [
        "10:30:55 · CCTV-A · Pre-incident",
        "10:31:22 · BUS-017 · INCIDENT",
        "10:31:41 · JUNCTION-02 · N-bound",
        "10:32:18 · CCTV-C · Match: 0.87",
        "→ FOR AUTHORIZED REVIEW",
      ],
    },
  },
  {
    range: [0.86, 0.94],
    title: "4D Semantic Urban Twin",
    subtitle: "Every observation updates the city's persistent state. From first seen to verified repaired.",
    hud: null,
    card: {
      title: "Road Segment RD-142",
      items: [
        "Health: 66/100 ↓ (was 82)",
        "Potholes: 2 · Confidence: 0.96",
        "Zebra crossing: FADED",
        "Status: WORK ORDER RAISED",
      ],
    },
  },
  {
    range: [0.94, 1.0],
    title: "ONE URBAN INTELLIGENCE LAYER\nACROSS EVERY CAMERA.",
    subtitle: "Discover. Corroborate. Understand. Act. Verify.",
    hud: null,
    card: {
      title: "VERIFIED REPAIRED ✓",
      items: [
        "Object: #PO-142-08",
        "First seen: 10:05 · 3 buses",
        "Work order completed",
        "Future bus verified: 14:32",
      ],
    },
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

        {/* ─── Left Asset Feed Drawer UI (Matches User Screenshot #2) ─── */}
        <AssetFeedDrawer
          asset={selectedAsset}
          onClose={() => setSelectedAsset(null)}
          onQuickSelect={handleQuickSelect}
        />

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

            {/* HUD — top right under mode button if card hidden */}
            {currentStage.hud && !selectedAsset && (
              <div
                className="absolute top-20 right-6 p-4 rounded-xl"
                style={{
                  background: "rgba(5,8,16,0.85)",
                  border: "1px solid rgba(0,212,255,0.25)",
                  backdropFilter: "blur(12px)",
                  minWidth: "220px",
                }}
              >
                <div className="label-text mb-3" style={{ color: "var(--accent-cyan)" }}>
                  {currentStage.hud.camera}
                </div>
                <div className="space-y-1.5">
                  {[
                    { k: "GPS", v: currentStage.hud.gps },
                    { k: "TIME", v: currentStage.hud.time },
                    { k: "INFERENCE", v: currentStage.hud.inference },
                    { k: "UPLOAD", v: currentStage.hud.upload },
                  ].map(({ k, v }) => (
                    <div key={k} className="flex justify-between gap-4">
                      <span className="label-text" style={{ color: "var(--text-muted)" }}>{k}</span>
                      <span
                        className="hud-text font-mono"
                        style={{
                          color: k === "UPLOAD" && v === "EVENT ONLY"
                            ? "var(--accent-green)"
                            : "var(--text-primary)",
                        }}
                      >
                        {v}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* HUD — bottom right */}
            {currentStage.card && !selectedAsset && (
              <div
                className="absolute bottom-6 right-6 p-5 rounded-xl max-w-sm"
                style={{
                  background: "rgba(5,8,16,0.85)",
                  border: "1px solid rgba(0,212,255,0.25)",
                  backdropFilter: "blur(12px)",
                }}
              >
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full" style={{ background: "var(--accent-cyan)" }} />
                  <h4 className="text-white font-medium">{currentStage.card.title}</h4>
                </div>
                <ul className="space-y-2">
                  {currentStage.card.items.map((item, i) => (
                    <li key={i} className="flex gap-2 items-start">
                      <span className="text-xs opacity-50 mt-1" style={{ color: "var(--accent-cyan)" }}>{`>`}</span>
                      <span className="text-sm font-mono text-white/80">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

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
