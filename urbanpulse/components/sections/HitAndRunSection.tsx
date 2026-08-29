"use client";

import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

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

  const overallConfidence = 0.91;

  return (
    <section
      ref={sectionRef}
      id="incident"
      className="relative py-32"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, #ff3333, transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        {/* Header */}
        <div className="htr-header text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(255,51,51,0.08)", border: "1px solid rgba(255,51,51,0.25)" }}
          >
            <span className="label-text" style={{ color: "#ff3333" }}>
              Cross-Camera Incident Reconstruction
            </span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            Agentic Evidence <span style={{ color: "#ff6633" }}>Reconstruction</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            When a bus detects an incident, the Camera Orchestration Agent identifies
            relevant nearby cameras. Evidence is correlated across feeds — with explicit
            confidence and uncertainty — for authorized human review.
          </p>
        </div>

        <div className="grid lg:grid-cols-5 gap-10">
          {/* Left: Timeline */}
          <div className="lg:col-span-3">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-heading font-semibold text-sm" style={{ color: "var(--text-secondary)" }}>
                EVIDENCE TIMELINE
              </h3>
              <button
                id="replay-timeline"
                onClick={() => { setActiveStep(-1); setPlaying(false); setTimeout(() => setPlaying(true), 100); }}
                className="label-text px-3 py-1.5 rounded-lg transition-all hover:scale-105"
                style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", color: "var(--text-secondary)" }}
              >
                ↺ REPLAY
              </button>
            </div>

            <div className="relative">
              {/* Timeline vertical line */}
              <div
                className="absolute left-[19px] top-0 bottom-0 w-px"
                style={{ background: "rgba(255,255,255,0.08)" }}
              />

              <div className="space-y-4">
                {EVIDENCE_TIMELINE.map((ev, i) => {
                  const visible = i <= activeStep;
                  const isIncident = ev.camera === "BUS-017";
                  return (
                    <div
                      key={ev.camera}
                      className="flex gap-5 transition-all duration-500"
                      style={{
                        opacity: visible ? 1 : 0.15,
                        transform: visible ? "none" : "translateX(-10px)",
                      }}
                    >
                      {/* Timeline dot */}
                      <div
                        className="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 relative z-10"
                        style={{
                          background: visible ? `rgba(${ev.color.replace("#", "").match(/.{2}/g)?.map(h=>parseInt(h,16)).join(",")}, 0.15)` : "rgba(255,255,255,0.05)",
                          border: `1px solid ${visible ? ev.color : "rgba(255,255,255,0.1)"}`,
                          boxShadow: visible && isIncident ? `0 0 20px ${ev.color}` : "none",
                        }}
                      >
                        <span className="text-xs">
                          {ev.type === "moving" ? "🚌" : ev.type === "fixed" ? "📡" : "🎥"}
                        </span>
                      </div>

                      {/* Content */}
                      <div
                        className="flex-1 p-4 rounded-xl"
                        style={{
                          background: visible ? (isIncident ? "rgba(255,51,51,0.08)" : "rgba(255,255,255,0.03)") : "transparent",
                          border: visible ? `1px solid ${ev.color}33` : "1px solid transparent",
                        }}
                      >
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center gap-2">
                            <span className="font-mono text-sm font-semibold" style={{ color: ev.color }}>
                              {ev.time}
                            </span>
                            <span
                              className="label-text px-2 py-0.5 rounded"
                              style={{ background: `${ev.color}22`, color: ev.color }}
                            >
                              {ev.camera}
                            </span>
                            <span className="label-text" style={{ color: "var(--text-muted)" }}>
                              {CAMERA_TYPE_LABEL[ev.type]}
                            </span>
                          </div>
                          <span
                            className="label-text px-2 py-0.5 rounded"
                            style={{
                              background: isIncident ? "rgba(255,51,51,0.15)" : "rgba(255,255,255,0.05)",
                              color: isIncident ? "#ff3333" : "var(--text-muted)",
                            }}
                          >
                            {ev.note}
                          </span>
                        </div>
                        <p className="text-xs leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                          {ev.event}
                        </p>
                        {visible && (
                          <div className="mt-2 flex items-center gap-3">
                            <span className="label-text" style={{ color: "var(--text-muted)" }}>CONF</span>
                            <div className="flex-1 h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.08)" }}>
                              <div
                                className="h-full rounded-full"
                                style={{ width: `${ev.confidence * 100}%`, background: ev.color }}
                              />
                            </div>
                            <span className="font-mono text-xs" style={{ color: ev.color }}>
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

          {/* Right: Summary + verdict */}
          <div className="lg:col-span-2 flex flex-col gap-6">
            {/* Overall result */}
            <div
              className="p-6 rounded-2xl"
              style={{
                background: "rgba(0,212,255,0.06)",
                border: "1px solid rgba(0,212,255,0.2)",
              }}
            >
              <h4 className="font-heading font-semibold mb-4" style={{ color: "var(--text-primary)" }}>
                Evidence Summary
              </h4>
              <div className="space-y-3 text-xs mb-5">
                {[
                  ["Camera feeds analyzed", "5"],
                  ["Evidence type", "Multi-source"],
                  ["Vehicle matches", "4 candidates"],
                  ["Strongest match", "91% confidence"],
                  ["Gap in coverage", "1 (10:33–10:34)"],
                  ["Plate confidence", "0.81"],
                  ["Route reconstructed", "~1.2 km"],
                ].map(([k, v]) => (
                  <div key={k} className="flex justify-between">
                    <span style={{ color: "var(--text-muted)" }}>{k}</span>
                    <span style={{ color: "var(--text-primary)" }}>{v}</span>
                  </div>
                ))}
              </div>
              <div
                className="p-3 rounded-xl text-center"
                style={{ background: "rgba(0,212,255,0.1)", border: "1px solid rgba(0,212,255,0.3)" }}
              >
                <div className="font-heading font-bold text-lg gradient-text">
                  LIKELY MATCH — 91%
                </div>
                <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                  Evidence candidate for authorized human review
                </div>
              </div>
            </div>

            {/* Disclaimer */}
            <div
              className="p-5 rounded-xl"
              style={{ background: "rgba(255,170,0,0.06)", border: "1px solid rgba(255,170,0,0.2)" }}
            >
              <div className="label-text mb-2" style={{ color: "var(--accent-amber)" }}>
                ⚠ IMPORTANT
              </div>
              <p className="text-xs leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                This is an <strong style={{ color: "var(--accent-amber)" }}>assistive evidence-reconstruction system</strong>,
                not an automated law-enforcement engine. All outputs require authorized human
                review before any enforcement action. Confidence scores and coverage gaps
                are always disclosed.
              </p>
            </div>

            {/* Camera type legend */}
            <div className="p-5 rounded-xl" style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
              <h4 className="font-heading font-semibold text-sm mb-4" style={{ color: "var(--text-secondary)" }}>
                CAMERA SOURCES IN EVIDENCE CHAIN
              </h4>
              {Object.entries(CAMERA_TYPE_LABEL).map(([type, label]) => (
                <div key={type} className="flex items-center gap-3 mb-2">
                  <div className="w-2 h-2 rounded-full" style={{ background: CAMERA_TYPE_COLOR[type] }} />
                  <span className="text-xs" style={{ color: "var(--text-secondary)" }}>{label}</span>
                </div>
              ))}
              <div className="mt-3 text-xs" style={{ color: "var(--text-muted)" }}>
                All three camera types contribute to the evidence chain — demonstrating the value of unified infrastructure.
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
