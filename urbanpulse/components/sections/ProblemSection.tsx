"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const PROBLEMS = [
  {
    id: "isolated",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <rect x="4" y="4" width="10" height="10" rx="2" stroke="#ff3333" strokeWidth="1.5" />
        <rect x="18" y="4" width="10" height="10" rx="2" stroke="#ff3333" strokeWidth="1.5" />
        <rect x="11" y="18" width="10" height="10" rx="2" stroke="#ff3333" strokeWidth="1.5" />
        <path d="M14 9h4M9 14v4" stroke="#ff3333" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="2 2" />
      </svg>
    ),
    title: "Isolated Detections",
    body: "Each camera sees its own slice of the city. A pothole detected by Bus A and the same pothole detected by Bus B remain two separate, unverified alerts — forever.",
    stat: "~73%",
    statLabel: "false-positive rate in single-source detection systems",
    color: "#ff3333",
  },
  {
    id: "fragmented",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <circle cx="16" cy="16" r="12" stroke="#ffaa00" strokeWidth="1.5" strokeDasharray="4 3" />
        <path d="M10 16h4M18 16h4M16 10v4M16 18v4" stroke="#ffaa00" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="16" cy="16" r="2" fill="#ffaa00" />
      </svg>
    ),
    title: "Fragmented Coverage",
    body: "Moving cameras have coverage but no continuity. Fixed cameras have continuity but no coverage. Existing CCTV sits underused. The intelligence is permanently divided.",
    stat: "60%+",
    statLabel: "of city road segments unobserved on any given day",
    color: "#ffaa00",
  },
  {
    id: "no-memory",
    icon: (
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <path d="M8 24V12a2 2 0 012-2h12a2 2 0 012 2v12" stroke="#8855ff" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M6 24h20" stroke="#8855ff" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M13 14h6M13 18h4" stroke="#8855ff" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M16 8V5" stroke="#8855ff" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="2 2" />
      </svg>
    ),
    title: "No Urban Memory",
    body: "Alerts fire and disappear. There is no persistent record of a road segment's condition over time. A repaired pothole looks identical to an unrepaired one — no verification, no closed loop.",
    stat: "0%",
    statLabel: "of city camera systems verify repair automatically",
    color: "#8855ff",
  },
];

export default function ProblemSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".problem-card",
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.7,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ".problem-grid",
            start: "top 75%",
            end: "bottom 60%",
            toggleActions: "play none none reverse",
          },
        }
      );

      gsap.fromTo(
        ".problem-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          ease: "power2.out",
          scrollTrigger: {
            trigger: sectionRef.current,
            start: "top 80%",
          },
        }
      );

      gsap.fromTo(
        ".fusion-arrow",
        { opacity: 0, scaleX: 0 },
        {
          opacity: 1,
          scaleX: 1,
          duration: 0.6,
          stagger: 0.1,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ".fusion-diagram",
            start: "top 80%",
          },
        }
      );
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="problem"
      className="relative py-32 overflow-hidden"
      style={{ background: "var(--bg-surface)" }}
    >
      {/* Top border line */}
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-blue), transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        {/* Header */}
        <div className="problem-header text-center mb-20">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{
              background: "rgba(255, 51, 51, 0.08)",
              border: "1px solid rgba(255, 51, 51, 0.25)",
            }}
          >
            <span className="label-text" style={{ color: "#ff3333" }}>
              The Problem With Current Systems
            </span>
          </div>
          <h2
            className="font-heading text-4xl md:text-5xl font-bold mb-6"
            style={{ color: "var(--text-primary)" }}
          >
            Smart City Cameras Are{" "}
            <span style={{ color: "#ff6633" }}>Brilliant in Isolation.</span>
            <br />
            <span style={{ color: "var(--text-secondary)" }}>Blind as a System.</span>
          </h2>
          <p
            className="text-lg max-w-2xl mx-auto"
            style={{ color: "var(--text-secondary)" }}
          >
            Current camera deployments generate alerts, not intelligence. Detection
            without corroboration. Coverage without memory. Technology without a closed loop.
          </p>
        </div>

        {/* Problem cards */}
        <div className="problem-grid grid md:grid-cols-3 gap-6 mb-24">
          {PROBLEMS.map((p) => (
            <div
              key={p.id}
              className="problem-card opacity-0 p-7 rounded-2xl group transition-all duration-300 hover:scale-[1.02]"
              style={{
                background: `rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.05)`,
                border: `1px solid rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.15)`,
              }}
            >
              <div className="mb-5">{p.icon}</div>
              <h3
                className="font-heading font-semibold text-lg mb-3"
                style={{ color: p.color }}
              >
                {p.title}
              </h3>
              <p className="text-sm leading-relaxed mb-6" style={{ color: "var(--text-secondary)" }}>
                {p.body}
              </p>
              <div
                className="pt-5"
                style={{ borderTop: `1px solid rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.15)` }}
              >
                <div className="font-mono font-bold text-2xl" style={{ color: p.color }}>
                  {p.stat}
                </div>
                <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                  {p.statLabel}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Fusion diagram */}
        <div className="fusion-diagram max-w-4xl mx-auto">
          <div className="text-center mb-10">
            <h3
              className="font-heading text-2xl font-bold mb-3"
              style={{ color: "var(--text-primary)" }}
            >
              The Solution: Cooperative Perception
            </h3>
            <p className="text-sm" style={{ color: "var(--text-secondary)" }}>
              Three camera layers. One intelligence network. Zero wasted observations.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 items-center">
            {[
              { label: "Moving Cameras", sub: "Coverage + Discovery", color: "#00d4ff" },
              { label: "Fixed Cameras", sub: "Continuity + Trajectory", color: "#4488ff" },
              { label: "Existing CCTV", sub: "Low-CAPEX Extension", color: "#8855ff" },
            ].map((src) => (
              <div
                key={src.label}
                className="p-5 rounded-xl text-center"
                style={{
                  background: `rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.08)`,
                  border: `1px solid rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.2)`,
                }}
              >
                <div className="font-heading font-semibold text-sm mb-1" style={{ color: src.color }}>
                  {src.label}
                </div>
                <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                  {src.sub}
                </div>
              </div>
            ))}
          </div>

          {/* Arrow converging */}
          <div className="flex justify-center mt-4 mb-4">
            <svg width="300" height="40" viewBox="0 0 300 40">
              <path
                className="fusion-arrow"
                d="M50 5 L150 35"
                stroke="#4488ff"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeDasharray="4 3"
                opacity="0.6"
              />
              <path
                className="fusion-arrow"
                d="M150 5 L150 35"
                stroke="#00d4ff"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
              <path
                className="fusion-arrow"
                d="M250 5 L150 35"
                stroke="#8855ff"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeDasharray="4 3"
                opacity="0.6"
              />
              <circle cx="150" cy="38" r="3" fill="#00d4ff" />
            </svg>
          </div>

          <div
            className="p-6 rounded-2xl text-center"
            style={{
              background: "rgba(0, 100, 200, 0.1)",
              border: "1px solid rgba(0, 212, 255, 0.3)",
              boxShadow: "0 0 40px rgba(0, 212, 255, 0.08)",
            }}
          >
            <div className="font-heading text-xl font-bold gradient-text mb-2">
              UrbanPulse Fusion
            </div>
            <div className="text-sm" style={{ color: "var(--text-secondary)" }}>
              Persistent Urban Objects · Fleet Consensus · Closed-Loop Verification
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
