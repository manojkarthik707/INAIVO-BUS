"use client";

import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const EVIDENCE_TIMELINE = [
  {
    time: "10:30:55",
    camera: "CCTV-A",
    type: "existing",
    event: "Pre-incident — suspect vehicle enters frame",
    confidence: 0.74,
    color: "#8855ff",
    note: "Pre-incident",
  },
  {
    time: "10:31:22",
    camera: "BUS-017",
    type: "moving",
    event: "INCIDENT DETECTED — collision observed, plate partial capture",
    confidence: 0.93,
    color: "#ff3333",
    note: "⚠ INCIDENT",
  },
  {
    time: "10:31:41",
    camera: "JUNCTION-02",
    type: "fixed",
    event: "Suspect vehicle turns north — trajectory confirmed",
    confidence: 0.87,
    color: "#4488ff",
    note: "Direction: N",
  },
  {
    time: "10:32:18",
    camera: "CCTV-C",
    type: "existing",
    event: "Vehicle matching visual embedding — plate candidate 0.81",
    confidence: 0.81,
    color: "#8855ff",
    note: "Match: 0.81",
  },
  {
    time: "10:34:05",
    camera: "BUS-008",
    type: "moving",
    event: "Matching candidate observed — 1.2km from incident",
    confidence: 0.88,
    color: "#00d4ff",
    note: "Match: 0.88",
  },
];

const CAMERA_TYPE_COLOR: Record<string, string> = {
  existing: "#8855ff",
  moving: "#00d4ff",
  fixed: "#4488ff",
};

const CAMERA_TYPE_LABEL: Record<string, string> = {
  existing: "EXISTING CCTV",
  moving: "MOVING CAM",
  fixed: "FIXED CAM",
};

export default function HitAndRunSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const [activeStep, setActiveStep] = useState(-1);
  const [playing, setPlaying] = useState(false);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".htr-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: {
            trigger: sectionRef.current,
            start: "top 80%",
            onEnter: () => setPlaying(true),
          },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  useEffect(() => {
    if (!playing) return;
    if (activeStep >= EVIDENCE_TIMELINE.length - 1) return;
    const timer = setTimeout(() => setActiveStep((s) => s + 1), 700);
    return () => clearTimeout(timer);
  }, [playing, activeStep]);

  return (
    <Section
      ref={sectionRef as any}
      id="incident"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, #ff3333, transparent)" }}
      />

      <PageContainer>
        <div className="htr-header">
          <SectionHeader
            eyebrow="Cross-Camera Incident Reconstruction"
            title={
              <>
                Agentic Evidence <span style={{ color: "#ff6633" }}>Reconstruction</span>
              </>
            }
            description="When a bus detects an incident, the Camera Orchestration Agent identifies relevant nearby cameras. Evidence is correlated across feeds — with explicit confidence and uncertainty — for authorized human review."
          />
        </div>

        <div className="grid lg:grid-cols-[60%_40%] gap-10 lg:gap-16 items-start relative">
          
          {/* Left: Timeline (approx 60%) */}
          <div className="flex flex-col w-full relative">
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/10">
              <h3 className="font-heading font-semibold text-sm text-text-secondary tracking-widest uppercase">
                EVIDENCE TIMELINE
              </h3>
              <button
                id="replay-timeline"
                onClick={() => { setActiveStep(-1); setPlaying(false); setTimeout(() => setPlaying(true), 100); }}
                className="label-text px-4 py-2 rounded-xl transition-all hover:scale-105 glass-card"
                style={{ padding: "8px 16px", color: "var(--text-primary)" }}
              >
                ↺ REPLAY
              </button>
            </div>

            <div className="relative">
              {/* Timeline vertical line */}
              <div
                className="absolute left-[24px] top-4 bottom-0 w-[2px]"
                style={{ background: "rgba(255,255,255,0.05)" }}
              />

              <div className="space-y-6">
                {EVIDENCE_TIMELINE.map((ev, i) => {
                  const visible = i <= activeStep;
                  const isIncident = ev.camera === "BUS-017";
                  
                  // Color RGB parsing for alpha manipulation
                  let r = 0, g = 0, b = 0;
                  if (ev.color.length === 7) {
                    r = parseInt(ev.color.substring(1, 3), 16);
                    g = parseInt(ev.color.substring(3, 5), 16);
                    b = parseInt(ev.color.substring(5, 7), 16);
                  }

                  return (
                    <div
                      key={ev.camera}
                      className="flex gap-6 transition-all duration-500 w-full"
                      style={{
                        opacity: visible ? 1 : 0.15,
                        transform: visible ? "none" : "translateX(-15px)",
                      }}
                    >
                      {/* Timeline dot */}
                      <div
                        className="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 relative z-10"
                        style={{
                          background: visible ? `rgba(${r},${g},${b},0.15)` : "rgba(255,255,255,0.05)",
                          border: `1px solid ${visible ? ev.color : "rgba(255,255,255,0.1)"}`,
                          boxShadow: visible && isIncident ? `0 0 25px ${ev.color}88` : "none",
                        }}
                      >
                        <span className="text-sm">
                          {ev.type === "moving" ? "🚌" : ev.type === "fixed" ? "📡" : "🎥"}
                        </span>
                      </div>

                      {/* Content */}
                      <div
                        className="flex-1 rounded-2xl p-5 md:p-6 w-full glass-card transition-all"
                        style={{
                          background: visible ? (isIncident ? "rgba(255,51,51,0.08)" : "var(--bg-card)") : "transparent",
                          borderColor: visible ? (isIncident ? ev.color : "var(--border-glass)") : "transparent",
                          boxShadow: visible && isIncident ? `0 8px 32px rgba(255,51,51,0.15)` : "none",
                        }}
                      >
                        {/* Consistent grid structure for the data */}
                        <div className="grid grid-cols-1 sm:grid-cols-[auto_1fr_auto] gap-3 sm:gap-6 mb-4 items-start sm:items-center w-full">
                          
                          {/* Time & Camera */}
                          <div className="flex items-center gap-3 w-full sm:w-auto">
                            <span className="font-mono text-base font-bold" style={{ color: ev.color }}>
                              {ev.time}
                            </span>
                            <span
                              className="font-mono text-[11px] font-bold px-2 py-1 rounded tracking-widest uppercase hidden sm:block"
                              style={{ background: `rgba(${r},${g},${b},0.15)`, color: ev.color }}
                            >
                              {ev.camera}
                            </span>
                          </div>
                          
                          {/* Event Type / Note */}
                          <div className="flex-1 flex justify-start sm:justify-center">
                            <span className="label-text text-text-muted hidden sm:block">
                              {CAMERA_TYPE_LABEL[ev.type]}
                            </span>
                          </div>

                          <div className="flex justify-end">
                            <span
                              className="font-mono text-[10px] font-bold px-3 py-1.5 rounded tracking-widest uppercase text-center"
                              style={{
                                background: isIncident ? "rgba(255,51,51,0.2)" : "rgba(255,255,255,0.08)",
                                color: isIncident ? "#ff3333" : "var(--text-muted)",
                                border: isIncident ? "1px solid rgba(255,51,51,0.4)" : "none"
                              }}
                            >
                              {ev.note}
                            </span>
                          </div>
                        </div>

                        {/* Description */}
                        <p className="text-sm leading-relaxed text-text-secondary mb-5">
                          {ev.event}
                        </p>

                        {/* Confidence Visualization */}
                        {visible && (
                          <div className="flex items-center gap-4 bg-black/20 p-3 rounded-xl border border-white/5">
                            <span className="label-text text-text-muted uppercase">CONFIDENCE</span>
                            <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.1)" }}>
                              <div
                                className="h-full rounded-full"
                                style={{ width: `${ev.confidence * 100}%`, background: ev.color }}
                              />
                            </div>
                            <span className="font-mono text-xs font-bold" style={{ color: ev.color }}>
                              {(ev.confidence * 100).toFixed(0)}%
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Right: Summary + Verdict (approx 40%) */}
          <div className="w-full flex flex-col gap-6 sticky top-28 h-fit pb-12 pt-[48px] md:pt-0">
            {/* Overall Result */}
            <div
              className="p-8 rounded-3xl glass-card flex flex-col h-full relative overflow-hidden"
              style={{
                background: "rgba(0,212,255,0.03)",
                borderColor: "rgba(0,212,255,0.2)",
              }}
            >
              {/* Subtle ambient light */}
              <div 
                className="absolute top-0 right-0 w-full h-full opacity-20 pointer-events-none"
                style={{ background: "radial-gradient(circle at top right, #00d4ff, transparent 70%)" }}
              />

              <div className="relative z-10">
                <h4 className="font-heading font-semibold mb-8 text-text-primary text-xl tracking-tight">
                  Evidence Summary
                </h4>
                
                <div className="space-y-4 text-sm mb-8">
                  {[
                    ["Camera feeds analyzed", "5"],
                    ["Evidence type", "Multi-source"],
                    ["Vehicle matches", "4 candidates"],
                    ["Strongest match", "91% confidence"],
                    ["Gap in coverage", "1 (10:33–10:34)"],
                    ["Plate confidence", "0.81"],
                    ["Route reconstructed", "~1.2 km"],
                  ].map(([k, v]) => (
                    <div key={k} className="flex justify-between items-center py-2 border-b border-white/5 last:border-0">
                      <span className="text-text-muted">{k}</span>
                      <span className="text-text-primary font-medium">{v}</span>
                    </div>
                  ))}
                </div>
                
                <div
                  className="p-5 rounded-2xl text-center glass-card mt-auto"
                  style={{ background: "rgba(0,212,255,0.1)", borderColor: "rgba(0,212,255,0.3)" }}
                >
                  <div className="font-heading font-bold text-2xl gradient-text mb-2 tracking-tight">
                    LIKELY MATCH — 91%
                  </div>
                  <div className="text-xs text-text-secondary leading-relaxed">
                    Evidence candidate ready for authorized human review
                  </div>
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div
              className="p-6 rounded-2xl glass-card"
              style={{ background: "rgba(255,170,0,0.06)", borderColor: "rgba(255,170,0,0.2)" }}
            >
              <div className="label-text mb-3 text-accent-amber font-bold tracking-widest">
                ⚠ IMPORTANT
              </div>
              <p className="text-xs leading-relaxed text-text-secondary">
                This is an <strong className="text-accent-amber font-semibold">assistive evidence-reconstruction system</strong>,
                not an automated law-enforcement engine. All outputs require authorized human
                review before any enforcement action. Confidence scores and coverage gaps
                are always disclosed.
              </p>
            </div>

            {/* Camera Type Legend */}
            <div className="p-6 rounded-2xl glass-card">
              <h4 className="font-heading font-semibold text-xs mb-5 text-text-secondary tracking-widest uppercase">
                Sources in Chain
              </h4>
              <div className="flex flex-wrap gap-4">
                {Object.entries(CAMERA_TYPE_LABEL).map(([type, label]) => (
                  <div key={type} className="flex items-center gap-2">
                    <div className="w-2.5 h-2.5 rounded-full" style={{ background: CAMERA_TYPE_COLOR[type], boxShadow: `0 0 8px ${CAMERA_TYPE_COLOR[type]}88` }} />
                    <span className="text-xs font-medium text-text-secondary">{label}</span>
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
