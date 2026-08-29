"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const LIFECYCLE_STATES = [
  { state: "NEW", color: "#aaaaaa", desc: "First observation received" },
  { state: "UNVERIFIED", color: "#ffaa00", desc: "Single-camera detection" },
  { state: "CORROBORATED", color: "#00aaff", desc: "2+ independent cameras agree" },
  { state: "PERSISTENT", color: "#0066ff", desc: "Consistent across 3+ passes" },
  { state: "WORSENING", color: "#ff6600", desc: "Severity increasing over time" },
  { state: "WORK ORDER", color: "#ff3300", desc: "Assigned to municipal authority" },
  { state: "VERIFYING", color: "#ffcc00", desc: "Future observation in progress" },
  { state: "VERIFIED REPAIRED", color: "#00ff88", desc: "Independently confirmed fixed" },
];

const BUS_OBSERVATIONS = [
  {
    bus: "BUS-017",
    time: "10:05",
    conf: 0.71,
    gps: "12.9716° N, 77.5946° E",
    segment: "RD-142",
    type: "pothole",
    color: "#00d4ff",
  },
  {
    bus: "BUS-023",
    time: "11:20",
    conf: 0.86,
    gps: "12.9716° N, 77.5946° E",
    segment: "RD-142",
    type: "pothole",
    color: "#4488ff",
  },
  {
    bus: "BUS-031",
    time: "16:45",
    conf: 0.91,
    gps: "12.9716° N, 77.5946° E",
    segment: "RD-142",
    type: "pothole",
    color: "#8855ff",
  },
];

function ConfidenceBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="flex items-center gap-3">
      <div
        className="flex-1 h-1.5 rounded-full overflow-hidden"
        style={{ background: "rgba(255,255,255,0.1)" }}
      >
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${value * 100}%`, background: color }}
        />
      </div>
      <span className="font-mono text-xs" style={{ color }}>
        {(value * 100).toFixed(0)}%
      </span>
    </div>
  );
}

export default function FleetConsensusSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const [activeState, setActiveState] = useState(0);
  const [mergeStep, setMergeStep] = useState(0);

  useEffect(() => {
    // Lifecycle animation
    const interval = setInterval(() => {
      setActiveState((s) => (s + 1) % LIFECYCLE_STATES.length);
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".consensus-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".obs-card",
        { opacity: 0, x: -30 },
        {
          opacity: 1, x: 0, duration: 0.5, stagger: 0.15,
          scrollTrigger: { trigger: ".obs-grid", start: "top 80%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  // Trigger merge animation steps
  useEffect(() => {
    const timer = setTimeout(() => {
      if (mergeStep < 3) setMergeStep((s) => s + 1);
    }, 1200);
    return () => clearTimeout(timer);
  }, [mergeStep]);

  const finalConfidence = 0.96;

  return (
    <section
      ref={sectionRef}
      id="intelligence"
      className="relative py-32"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, #4488ff, transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        {/* Header */}
        <div className="consensus-header text-center mb-20">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(0,102,255,0.08)", border: "1px solid rgba(68,136,255,0.25)" }}
          >
            <span className="label-text" style={{ color: "var(--accent-electric)" }}>
              Fleet Consensus + Urban Memory
            </span>
          </div>
          <h2
            className="font-heading text-4xl md:text-5xl font-bold mb-5"
            style={{ color: "var(--text-primary)" }}
          >
            Detection is <span style={{ color: "var(--text-muted)" }}>Commodity.</span>
            <br />
            <span className="gradient-text">Fusion is the Product.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            A single AI detection is an observation — not truth. Independent
            observations from different buses build confidence. The system decides
            what to trust, not just what to detect.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-16 items-start">
          {/* Left: Three observations merging */}
          <div>
            <h3 className="font-heading font-semibold text-sm mb-6" style={{ color: "var(--text-secondary)" }}>
              THREE INDEPENDENT BUS OBSERVATIONS — SAME LOCATION
            </h3>

            <div className="obs-grid space-y-4 mb-8">
              {BUS_OBSERVATIONS.map((obs, i) => (
                <div
                  key={obs.bus}
                  className="obs-card opacity-0 p-5 rounded-xl"
                  style={{
                    background: `rgba(${obs.color === "#00d4ff" ? "0,212,255" : obs.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.06)`,
                    border: `1px solid ${obs.color}33`,
                  }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full animate-pulse" style={{ background: obs.color }} />
                      <span className="font-mono font-semibold text-sm" style={{ color: obs.color }}>
                        {obs.bus}
                      </span>
                    </div>
                    <span className="label-text" style={{ color: "var(--text-muted)" }}>{obs.time}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mb-3 text-xs" style={{ color: "var(--text-secondary)" }}>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>CLASS: </span>
                      <span style={{ color: "var(--accent-amber)" }}>POTHOLE</span>
                    </div>
                    <div>
                      <span style={{ color: "var(--text-muted)" }}>SEG: </span>
                      <span>{obs.segment}</span>
                    </div>
                  </div>
                  <ConfidenceBar value={obs.conf} color={obs.color} />
                </div>
              ))}
            </div>

            {/* Merge arrow */}
            <div className="flex flex-col items-center gap-1 mb-6">
              <div className="label-text" style={{ color: "var(--text-muted)" }}>
                SPATIAL MATCH: 92% · INDEPENDENT CAMERAS: 3
              </div>
              <div
                className="w-px h-10"
                style={{ background: "linear-gradient(to bottom, var(--accent-blue), var(--accent-cyan))" }}
              />
              <div className="label-text" style={{ color: "var(--accent-cyan)" }}>
                ↓ FLEET FUSION ENGINE
              </div>
            </div>

            {/* Result: Urban Object */}
            <div
              className="p-6 rounded-2xl"
              style={{
                background: "rgba(0,212,255,0.08)",
                border: "1px solid var(--accent-cyan)",
                boxShadow: "0 0 30px rgba(0,212,255,0.1)",
              }}
            >
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="font-mono text-xs mb-1" style={{ color: "var(--accent-cyan)" }}>
                    URBAN OBJECT
                  </div>
                  <div className="font-heading font-bold text-xl" style={{ color: "var(--text-primary)" }}>
                    #PO-142-08
                  </div>
                </div>
                <div
                  className="px-3 py-1 rounded-full text-xs font-semibold"
                  style={{ background: "rgba(0,255,136,0.15)", color: "var(--accent-green)", border: "1px solid rgba(0,255,136,0.3)" }}
                >
                  CORROBORATED
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 text-xs mb-4">
                {[
                  ["Type", "Pothole"],
                  ["Confidence", "96%"],
                  ["Independent cams", "3"],
                  ["Severity", "INCREASING"],
                  ["First seen", "10:05"],
                  ["Last seen", "16:45"],
                  ["Priority", "HIGH"],
                  ["Status", "WORK ORDER"],
                ].map(([k, v]) => (
                  <div key={k}>
                    <span style={{ color: "var(--text-muted)" }}>{k}: </span>
                    <span
                      style={{
                        color: v === "HIGH" || v === "WORK ORDER" ? "var(--accent-amber)"
                          : v === "CORROBORATED" ? "var(--accent-green)"
                          : "var(--text-primary)",
                      }}
                    >
                      {v}
                    </span>
                  </div>
                ))}
              </div>
              <ConfidenceBar value={finalConfidence} color="var(--accent-cyan)" />
            </div>
          </div>

          {/* Right: Lifecycle + principle */}
          <div>
            <h3 className="font-heading font-semibold text-sm mb-6" style={{ color: "var(--text-secondary)" }}>
              URBAN OBJECT LIFECYCLE
            </h3>

            <div className="space-y-2 mb-10">
              {LIFECYCLE_STATES.map((ls, i) => (
                <div
                  key={ls.state}
                  className="flex items-center gap-4 p-3 rounded-lg transition-all duration-500"
                  style={{
                    background: i === activeState ? `rgba(${ls.color.replace("#", "").match(/.{2}/g)?.map(h => parseInt(h,16)).join(",")}, 0.12)` : "rgba(255,255,255,0.02)",
                    border: `1px solid ${i === activeState ? ls.color : "rgba(255,255,255,0.06)"}`,
                    transform: i === activeState ? "translateX(8px)" : "none",
                  }}
                >
                  <div
                    className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                    style={{
                      background: ls.color,
                      boxShadow: i === activeState ? `0 0 8px ${ls.color}` : "none",
                    }}
                  />
                  <div className="flex-1">
                    <span
                      className="font-mono text-xs font-semibold"
                      style={{ color: i === activeState ? ls.color : "var(--text-secondary)" }}
                    >
                      {ls.state}
                    </span>
                    {i === activeState && (
                      <span className="text-xs ml-3" style={{ color: "var(--text-muted)" }}>
                        {ls.desc}
                      </span>
                    )}
                  </div>
                  {i === activeState && (
                    <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: ls.color }} />
                  )}
                </div>
              ))}
            </div>

            {/* Key principle */}
            <div
              className="p-6 rounded-2xl"
              style={{
                background: "rgba(0,0,0,0.4)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
            >
              <h4 className="font-heading font-semibold text-base mb-4" style={{ color: "var(--text-primary)" }}>
                The Hierarchy of Trust
              </h4>
              {[
                ["FRAME", "Raw image from camera"],
                ["DETECTION", "AI model output"],
                ["OBSERVATION", "Geotagged, timestamped event"],
                ["CORROBORATION", "2+ independent cameras agree"],
                ["URBAN OBJECT", "Persistent city-state entity"],
                ["WORK ITEM", "Municipal action created"],
                ["VERIFICATION", "Future camera confirms change"],
              ].map(([tier, desc], i, arr) => (
                <div key={tier} className="flex items-start gap-3">
                  <div className="flex flex-col items-center">
                    <div
                      className="w-2 h-2 rounded-full mt-1"
                      style={{
                        background: `hsl(${200 + i * 20}, 80%, ${50 + i * 4}%)`,
                      }}
                    />
                    {i < arr.length - 1 && (
                      <div className="w-px flex-1 my-1" style={{ background: "rgba(255,255,255,0.08)" }} />
                    )}
                  </div>
                  <div className="pb-3">
                    <span className="font-mono text-xs font-semibold" style={{ color: "var(--accent-cyan)" }}>
                      {tier}
                    </span>
                    <span className="text-xs ml-2" style={{ color: "var(--text-muted)" }}>{desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
