"use client";

import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const LAYERS = [
  {
    id: "moving",
    label: "Moving Cameras",
    color: "#00d4ff",
    icon: "🚌",
    tagline: "Wide-area coverage. Discovery. Repeated route observation.",
    description:
      "Buses, municipal vehicles, and fleet vehicles become distributed city sensors. Each pass of a road segment generates a new observation. Multiple passes build confidence.",
    tasks: [
      "Road defect & pothole detection",
      "Waterlogging detection",
      "Damaged / faded road markings",
      "Zebra crossing condition",
      "Signboard detection & condition",
      "Divider / barrier condition",
      "Illegal parking detection",
      "Vehicle classification",
      "Moving-camera traffic density",
      "Pedestrian-risk observations",
      "Incident discovery",
      "Number-plate capture",
      "Store-and-forward when offline",
    ],
    principle: "BUS → EDGE AI → EVENT CAPSULE → FLEET FUSION → URBAN OBJECT",
    advantage: "Covers every road segment the bus serves",
    limitation: "Sees each location only when passing",
  },
  {
    id: "fixed",
    label: "Fixed Roadside Cameras",
    color: "#4488ff",
    icon: "📡",
    tagline: "Continuous local monitoring. Trajectory analysis. Persistent scene.",
    description:
      "Junction cameras and roadside AI cameras observe one location continuously. They provide traffic counts, queue lengths, trajectory analysis, and near-miss detection that moving cameras cannot.",
    tasks: [
      "Traffic count & density",
      "Queue length estimation",
      "Lane occupancy",
      "Intersection congestion",
      "Pedestrian crossing behavior",
      "Cyclist & two-wheeler tracking",
      "Near-miss detection",
      "Dangerous trajectory detection",
      "Wrong-way movement",
      "Stopped vehicle alert",
      "Accident detection",
      "Continuous risk-zone monitoring",
      "Temporal event reconstruction",
    ],
    principle: "FIXED CAMERA → CONTINUOUS SCENE → TRAJECTORIES → TRAFFIC / SAFETY EVENT",
    advantage: "Unbroken coverage of critical locations",
    limitation: "Limited geographic footprint",
  },
  {
    id: "cctv",
    label: "Existing City CCTV",
    color: "#8855ff",
    icon: "🎥",
    tagline: "Reuse deployed infrastructure. Extend without replacing.",
    description:
      "Cities already own extensive CCTV networks. UrbanPulse Fusion integrates compatible existing streams — IP cameras, NVR feeds, RTSP streams — into the same AI pipeline without requiring hardware replacement.",
    tasks: [
      "Camera adapter / stream ingest",
      "Quality & camera-health check",
      "Scene calibration",
      "AI analytics on existing streams",
      "Low-light enhancement",
      "Perspective / ROI calibration",
      "Timestamp synchronization",
      "Evidence forensics",
      "Hit-and-run reconstruction",
      "Cross-camera vehicle Re-ID",
      "Incident archive search",
      "Stream-health monitoring",
      "Graceful degradation reporting",
    ],
    principle: "EXISTING CCTV → STREAM ADAPTER → AI ANALYTICS → EVIDENCE EVENTS → FUSION",
    advantage: "Low CAPEX — reuses sunk infrastructure value",
    limitation: "Quality varies; some cameras may be unsuitable",
  },
];

export default function ThreeCameraLayersSection() {
  const [active, setActive] = useState(0);
  const sectionRef = useRef<HTMLElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".layer-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".layer-tab",
        { opacity: 0, y: 20 },
        {
          opacity: 1, y: 0, duration: 0.5, stagger: 0.1,
          scrollTrigger: { trigger: ".layer-tabs", start: "top 85%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);
  
  // Animate content on tab change
  useEffect(() => {
    if (contentRef.current) {
      gsap.fromTo(
        contentRef.current,
        { opacity: 0, y: 15 },
        { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }
      );
    }
  }, [active]);

  const current = LAYERS[active];

  return (
    <Section
      ref={sectionRef as any}
      id="system"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-cyan), transparent)" }}
      />

      <PageContainer>
        {/* Header */}
        <div className="layer-header">
          <SectionHeader
            eyebrow="THREE CAMERA INTELLIGENCE LAYERS"
            title={
              <>
                Coverage. Continuity. <span className="gradient-text">Reuse.</span>
              </>
            }
            description="Three fundamentally different camera types. One unified AI pipeline. Each solves what the others cannot."
          />
        </div>

        {/* Tab switcher */}
        <div className="layer-tabs flex gap-4 justify-center mb-16 flex-wrap">
          {LAYERS.map((layer, i) => (
            <button
              key={layer.id}
              id={`layer-tab-${layer.id}`}
              onClick={() => setActive(i)}
              className="layer-tab px-6 py-3.5 rounded-xl font-heading font-semibold text-sm transition-all duration-300 flex items-center justify-center gap-2"
              style={{
                background: active === i
                  ? `rgba(${layer.color === "#00d4ff" ? "0,212,255" : layer.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.15)`
                  : "rgba(255,255,255,0.04)",
                border: `1px solid ${active === i ? layer.color : "rgba(255,255,255,0.08)"}`,
                color: active === i ? layer.color : "var(--text-secondary)",
                boxShadow: active === i ? `0 0 20px ${layer.color}22` : "none",
                minWidth: "220px",
              }}
            >
              <span className="text-xl">{layer.icon}</span>
              {layer.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div ref={contentRef} className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-stretch" key={active}>
          {/* Left: Description */}
          <div
            className="p-8 lg:p-10 rounded-3xl h-full flex flex-col justify-between"
            style={{
              background: `rgba(${current.color === "#00d4ff" ? "0,212,255" : current.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.05)`,
              border: `1px solid ${current.color}33`,
              boxShadow: `0 8px 32px rgba(0,0,0,0.15)`,
            }}
          >
            <div>
              <div className="text-5xl mb-6">{current.icon}</div>
              <h3 className="font-heading text-3xl font-bold mb-3 tracking-tight" style={{ color: current.color }}>
                {current.label}
              </h3>
              <p className="text-base font-medium mb-5 text-text-secondary">
                {current.tagline}
              </p>
              <p className="text-body mb-10 text-text-secondary opacity-90">
                {current.description}
              </p>

              {/* Principle flow */}
              <div
                className="p-5 rounded-xl font-mono text-xs mb-8"
                style={{
                  background: "rgba(0,0,0,0.4)",
                  border: `1px solid ${current.color}22`,
                  color: current.color,
                  lineHeight: "2",
                }}
              >
                {current.principle.split("→").map((step, i, arr) => (
                  <span key={i}>
                    <span style={{ color: "var(--text-primary)" }}>{step.trim()}</span>
                    {i < arr.length - 1 && <span style={{ color: current.color }}> → </span>}
                  </span>
                ))}
              </div>
            </div>

            {/* Advantage / Limitation */}
            <div className="grid grid-cols-2 gap-4 mt-auto">
              <div className="p-4 rounded-xl" style={{ background: "rgba(0,255,136,0.06)", border: "1px solid rgba(0,255,136,0.15)" }}>
                <div className="label-text mb-2 text-accent-green">Advantage</div>
                <div className="text-sm text-text-secondary">{current.advantage}</div>
              </div>
              <div className="p-4 rounded-xl" style={{ background: "rgba(255,170,0,0.06)", border: "1px solid rgba(255,170,0,0.15)" }}>
                <div className="label-text mb-2 text-accent-amber">Limitation</div>
                <div className="text-sm text-text-secondary">{current.limitation}</div>
              </div>
            </div>
          </div>

          {/* Right: Task list */}
          <div className="h-full flex flex-col">
            <h4 className="font-heading font-semibold text-sm mb-6 tracking-widest text-text-secondary uppercase">
              AI Capabilities
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {current.tasks.map((task, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 p-4 rounded-xl transition-all duration-200 hover:scale-[1.02] glass-card"
                  style={{
                    padding: "16px",
                  }}
                >
                  <div
                    className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                    style={{ background: current.color, boxShadow: `0 0 10px ${current.color}` }}
                  />
                  <span className="text-[14px] font-medium text-text-primary">
                    {task}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Combined strength statement */}
        <div
          className="mt-16 p-8 rounded-2xl text-center max-w-4xl mx-auto glass-card"
          style={{
            background: "rgba(0,100,200,0.06)",
            border: "1px solid rgba(0,212,255,0.15)",
          }}
        >
          <p className="font-heading text-lg font-semibold mb-2 text-text-primary">
            Together: Coverage + Continuity + Reuse = <span className="gradient-text">Complete Urban Intelligence</span>
          </p>
          <p className="text-sm text-text-secondary max-w-2xl mx-auto">
            No single camera type can provide what all three provide together.
            UrbanPulse Fusion makes them cooperate through a common observation schema and
            spatiotemporal fusion engine.
          </p>
        </div>
      </PageContainer>
    </Section>
  );
}
