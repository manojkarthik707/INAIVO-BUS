"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

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
    <div className="flex items-center gap-3 w-full">
      <div
        className="flex-1 h-1.5 rounded-full overflow-hidden"
        style={{ background: "rgba(255,255,255,0.1)" }}
      >
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{ width: `${value * 100}%`, background: color }}
        />
      </div>
      <span className="font-mono text-xs font-semibold" style={{ color }}>
        {(value * 100).toFixed(0)}%
      </span>
    </div>
  );
}

export default function FleetConsensusSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const [activeState, setActiveState] = useState(0);

  useEffect(() => {
    // Lifecycle animation
    const interval = setInterval(() => {
      setActiveState((s) => (s + 1) % LIFECYCLE_STATES.length);
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
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

  const finalConfidence = 0.96;

  return (
    <Section
      ref={sectionRef as any}
      id="intelligence"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, #4488ff, transparent)" }}
      />

      <PageContainer>
        <div className="consensus-header">
          <SectionHeader
            eyebrow="FLEET CONSENSUS + URBAN MEMORY"
            title={
              <>
                Detection is <span className="text-text-muted font-light">Commodity.</span>
                <br />
                <span className="gradient-text">Fusion is the Product.</span>
              </>
            }
            description="A single AI detection is an observation — not truth. Independent observations from different buses build confidence. The system decides what to trust, not just what to detect."
          />
        </div>

        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-start">
          {/* Left: Observations merging */}
          <div className="flex flex-col w-full">
            <h3 className="font-heading font-semibold text-sm mb-6 text-text-secondary uppercase tracking-widest text-center md:text-left">
              THREE INDEPENDENT BUS OBSERVATIONS — SAME LOCATION
            </h3>

            <div className="obs-grid grid grid-cols-1 gap-4 mb-6 w-full">
              {BUS_OBSERVATIONS.map((obs) => (
                <div
                  key={obs.bus}
                  className="obs-card opacity-0 p-5 rounded-2xl glass-card transition-transform duration-300 hover:scale-[1.02]"
                  style={{
                    borderColor: `${obs.color}33`,
                    background: `rgba(${parseInt(obs.color.slice(1,3),16)}, ${parseInt(obs.color.slice(3,5),16)}, ${parseInt(obs.color.slice(5,7),16)}, 0.05)`,
                  }}
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-2.5 h-2.5 rounded-full animate-pulse" style={{ background: obs.color, boxShadow: `0 0 10px ${obs.color}` }} />
                      <span className="font-mono font-bold text-sm" style={{ color: obs.color }}>
                        {obs.bus}
                      </span>
                    </div>
                    <span className="label-text text-text-muted">{obs.time}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-4 mb-4 text-sm text-text-secondary">
                    <div className="flex flex-col">
                      <span className="text-[10px] uppercase tracking-wider text-text-muted mb-1">Class</span>
                      <span className="text-accent-amber font-semibold uppercase">{obs.type}</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-[10px] uppercase tracking-wider text-text-muted mb-1">Segment</span>
                      <span className="font-mono">{obs.segment}</span>
                    </div>
                  </div>
                  <ConfidenceBar value={obs.conf} color={obs.color} />
                </div>
              ))}
            </div>

            {/* Merge arrow / Engine representation */}
            <div className="flex flex-col items-center gap-2 mb-6">
              <div className="label-text text-text-muted">
                SPATIAL MATCH: 92% · INDEPENDENT CAMERAS: 3
              </div>
              <div
                className="w-[2px] h-12 rounded-full"
                style={{ background: "linear-gradient(to bottom, var(--accent-blue), var(--accent-cyan))" }}
              />
              <div className="label-text font-bold text-accent-cyan tracking-widest">
                ↓ FLEET FUSION ENGINE
              </div>
            </div>

            {/* Result: Urban Object */}
            <div
              className="p-6 rounded-3xl glass-card w-full relative overflow-hidden"
              style={{
                borderColor: "var(--accent-cyan)",
                boxShadow: "0 0 30px rgba(0,212,255,0.1)",
              }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent pointer-events-none" />
              
              <div className="relative z-10">
                <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
                  <div>
                    <div className="font-mono text-xs mb-1 font-bold tracking-widest text-accent-cyan">
                      URBAN OBJECT
                    </div>
                    <div className="font-heading font-extrabold text-2xl text-text-primary">
                      #PO-142-08
                    </div>
                  </div>
                  <div
                    className="px-4 py-1.5 rounded-full text-[11px] font-bold tracking-widest uppercase"
                    style={{ background: "rgba(0,255,136,0.15)", color: "var(--accent-green)", border: "1px solid rgba(0,255,136,0.3)" }}
                  >
                    CORROBORATED
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-y-4 gap-x-6 text-sm mb-6">
                  {[
                    ["Type", "Pothole"],
                    ["Confidence", "96%"],
                    ["Independent Cams", "3"],
                    ["Severity", "INCREASING"],
                    ["First Seen", "10:05"],
                    ["Last Seen", "16:45"],
                    ["Priority", "HIGH"],
                    ["Status", "WORK ORDER"],
                  ].map(([k, v]) => (
                    <div key={k} className="flex flex-col">
                      <span className="text-[10px] uppercase tracking-wider text-text-muted mb-1">{k}</span>
                      <span
                        className="font-medium"
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
                <div className="pt-4 border-t border-white/10">
                  <ConfidenceBar value={finalConfidence} color="var(--accent-cyan)" />
                </div>
              </div>
            </div>
          </div>

          {/* Right: Lifecycle + principle */}
          <div className="flex flex-col w-full h-full">
            <h3 className="font-heading font-semibold text-sm mb-6 text-text-secondary uppercase tracking-widest text-center md:text-left">
              URBAN OBJECT LIFECYCLE
            </h3>

            <div className="space-y-3 mb-10 w-full">
              {LIFECYCLE_STATES.map((ls, i) => (
                <div
                  key={ls.state}
                  className="flex items-center gap-4 p-4 rounded-xl transition-all duration-500 w-full glass-card"
                  style={{
                    background: i === activeState ? `rgba(${parseInt(ls.color.slice(1,3),16)}, ${parseInt(ls.color.slice(3,5),16)}, ${parseInt(ls.color.slice(5,7),16)}, 0.12)` : "var(--bg-card)",
                    borderColor: i === activeState ? ls.color : "var(--border-glass)",
                    transform: i === activeState ? "translateX(8px)" : "none",
                  }}
                >
                  <div
                    className="w-3 h-3 rounded-full flex-shrink-0"
                    style={{
                      background: ls.color,
                      boxShadow: i === activeState ? `0 0 12px ${ls.color}` : "none",
                    }}
                  />
                  <div className="flex-1 flex flex-col sm:flex-row sm:items-center sm:justify-between">
                    <span
                      className="font-mono text-sm font-bold tracking-wider"
                      style={{ color: i === activeState ? ls.color : "var(--text-secondary)" }}
                    >
                      {ls.state}
                    </span>
                    {i === activeState && (
                      <span className="text-xs sm:ml-3 text-text-primary opacity-90 mt-1 sm:mt-0 font-medium">
                        {ls.desc}
                      </span>
                    )}
                  </div>
                  {i === activeState && (
                    <div className="w-2 h-2 rounded-full animate-pulse flex-shrink-0" style={{ background: ls.color }} />
                  )}
                </div>
              ))}
            </div>

            {/* Key principle */}
            <div className="p-8 rounded-3xl glass-card mt-auto w-full">
              <h4 className="font-heading font-bold text-lg mb-6 text-text-primary">
                The Hierarchy of Trust
              </h4>
              <div className="space-y-0 relative">
                <div className="absolute left-1.5 top-2 bottom-6 w-[2px] bg-white/10" />
                
                {[
                  ["FRAME", "Raw image from camera"],
                  ["DETECTION", "AI model output"],
                  ["OBSERVATION", "Geotagged, timestamped event"],
                  ["CORROBORATION", "2+ independent cameras agree"],
                  ["URBAN OBJECT", "Persistent city-state entity"],
                  ["WORK ITEM", "Municipal action created"],
                  ["VERIFICATION", "Future camera confirms change"],
                ].map(([tier, desc], i, arr) => (
                  <div key={tier} className="flex items-start gap-5 relative z-10 pb-5 last:pb-0">
                    <div className="flex-shrink-0 mt-1">
                      <div
                        className="w-3.5 h-3.5 rounded-full ring-4 ring-bg-surface"
                        style={{
                          background: `hsl(${200 + i * 20}, 80%, ${50 + i * 4}%)`,
                        }}
                      />
                    </div>
                    <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3 flex-1 pt-0.5">
                      <span className="font-mono text-[13px] font-bold text-accent-cyan tracking-wider min-w-[120px]">
                        {tier}
                      </span>
                      <span className="text-sm text-text-muted">{desc}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
