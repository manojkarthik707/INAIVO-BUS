"use client";

import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const AGENTS = [
  {
    id: "perception",
    label: "Perception Agent",
    icon: "👁",
    color: "#00d4ff",
    shortDesc: "Receives normalized AI observations from all camera nodes",
    tasks: [
      "Normalizes detections from all camera types",
      "Validates observation schema",
      "Forwards to Fusion Agent",
    ],
  },
  {
    id: "camera-orch",
    label: "Camera Orchestration",
    icon: "📡",
    color: "#4488ff",
    shortDesc: "Determines which cameras are relevant to any event",
    tasks: [
      "Queries camera registry by location + direction",
      "Identifies time-window relevant feeds",
      "Requests clip retrieval if needed",
    ],
  },
  {
    id: "fusion",
    label: "Fusion Agent",
    icon: "🔗",
    color: "#8855ff",
    shortDesc: "Combines duplicate observations into Persistent Urban Objects",
    tasks: [
      "Spatiotemporal duplicate detection",
      "Confidence aggregation across sources",
      "Urban Object lifecycle management",
    ],
  },
  {
    id: "incident",
    label: "Incident Agent",
    icon: "🚨",
    color: "#ff3333",
    shortDesc: "Builds candidate evidence paths for incidents",
    tasks: [
      "Initiates cross-camera vehicle search",
      "Plate + Re-ID correlation",
      "Evidence graph construction",
    ],
  },
  {
    id: "urban-memory",
    label: "Urban Memory Agent",
    icon: "🧠",
    color: "#00aaff",
    shortDesc: "Tracks state and history of persistent infrastructure",
    tasks: [
      "Road segment health scoring",
      "Defect deterioration velocity",
      "Expected-vs-observed reasoning",
    ],
  },
  {
    id: "maintenance",
    label: "Maintenance Agent",
    icon: "🔧",
    color: "#ffaa00",
    shortDesc: "Converts verified defects into prioritized work items",
    tasks: [
      "Priority scoring by confidence + severity",
      "Work order generation",
      "Authority assignment",
    ],
  },
  {
    id: "verification",
    label: "Verification Agent",
    icon: "✅",
    color: "#00ff88",
    shortDesc: "Verifies repair via future independent observations",
    tasks: [
      "Monitors future bus passes at repaired locations",
      "Compares before/after observations",
      "Updates Urban Object to VERIFIED REPAIRED",
    ],
  },
  {
    id: "traffic",
    label: "Traffic Agent",
    icon: "🚦",
    color: "#ff8800",
    shortDesc: "Combines counts, density, bottlenecks and delays",
    tasks: [
      "Real-time congestion mapping",
      "Bottleneck identification",
      "Route delay analytics",
    ],
  },
  {
    id: "privacy",
    label: "Privacy Agent",
    icon: "🔐",
    color: "#aa88ff",
    shortDesc: "Enforces retention, masking, access scope and evidence policy",
    tasks: [
      "Edge-side PII filtering",
      "Role-based evidence access",
      "Retention policy enforcement",
    ],
  },
  {
    id: "coverage",
    label: "Coverage Agent",
    icon: "🗺",
    color: "#44ccff",
    shortDesc: "Tracks which roads have fresh observations vs stale",
    tasks: [
      "Observation freshness tracking",
      "Coverage gap identification",
      "Fleet routing recommendations",
    ],
  },
];

export default function AgentSection() {
  const sectionRef = useRef<HTMLElement>(null);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".agent-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".agent-card",
        { opacity: 0, scale: 0.92 },
        {
          opacity: 1, scale: 1, duration: 0.4, stagger: 0.05,
          scrollTrigger: { trigger: ".agent-grid", start: "top 80%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  const active = AGENTS.find((a) => a.id === activeAgent);

  return (
    <section
      ref={sectionRef}
      id="agents"
      className="relative py-32"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, #8855ff, transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="agent-header text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(136,85,255,0.08)", border: "1px solid rgba(136,85,255,0.25)" }}
          >
            <span className="label-text" style={{ color: "#8855ff" }}>
              Agentic AI Orchestration Layer
            </span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            10 Specialized AI Agents.{" "}
            <span className="gradient-text">One Cooperative System.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            UrbanPulse Fusion behaves as an intelligent operational system, not a passive
            dashboard. Specialized agents coordinate to discover, corroborate,
            reconstruct and verify. Hover any agent to learn more.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Agent grid */}
          <div className="lg:col-span-2">
            <div className="agent-grid grid grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
              {AGENTS.map((agent) => (
                <button
                  key={agent.id}
                  id={`agent-${agent.id}`}
                  onClick={() => setActiveAgent(activeAgent === agent.id ? null : agent.id)}
                  className="agent-card opacity-0 text-left p-4 rounded-xl transition-all duration-300 hover:scale-105 group"
                  style={{
                    background: activeAgent === agent.id
                      ? `rgba(${agent.color.replace("#", "").match(/.{2}/g)?.map(h=>parseInt(h,16)).join(",")}, 0.12)`
                      : "rgba(255,255,255,0.03)",
                    border: `1px solid ${activeAgent === agent.id ? agent.color : "rgba(255,255,255,0.07)"}`,
                    boxShadow: activeAgent === agent.id ? `0 0 20px ${agent.color}22` : "none",
                  }}
                >
                  <div className="text-3xl mb-4">{agent.icon}</div>
                  <div className="font-heading font-semibold text-sm mb-2 leading-tight" style={{ color: agent.color }}>
                    {agent.label}
                  </div>
                  <div className="text-xs leading-relaxed opacity-80 line-clamp-3" style={{ color: "var(--text-muted)" }}>
                    {agent.shortDesc}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Active agent detail */}
          <div className="lg:col-span-1">
            {active ? (
              <div
                className="p-6 rounded-2xl h-full"
                style={{
                  background: `rgba(${active.color.replace("#", "").match(/.{2}/g)?.map(h=>parseInt(h,16)).join(",")}, 0.06)`,
                  border: `1px solid ${active.color}44`,
                  animation: "fadeInUp 0.3s ease",
                }}
              >
                <div className="text-4xl mb-4">{active.icon}</div>
                <h3 className="font-heading font-bold text-lg mb-2" style={{ color: active.color }}>
                  {active.label}
                </h3>
                <p className="text-sm mb-6 leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                  {active.shortDesc}
                </p>
                <h4 className="label-text mb-3" style={{ color: "var(--text-muted)" }}>
                  RESPONSIBILITIES
                </h4>
                <ul className="space-y-2">
                  {active.tasks.map((task) => (
                    <li key={task} className="flex items-start gap-2 text-xs" style={{ color: "var(--text-secondary)" }}>
                      <span style={{ color: active.color, flexShrink: 0 }}>›</span>
                      {task}
                    </li>
                  ))}
                </ul>
              </div>
            ) : (
              <div
                className="p-6 rounded-2xl h-full flex items-center justify-center"
                style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}
              >
                <div className="text-center">
                  <div className="text-4xl mb-4 opacity-30">🤖</div>
                  <p className="text-sm" style={{ color: "var(--text-muted)" }}>
                    Select an agent to learn about its responsibilities
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Agentic flow */}
        <div className="mt-16">
          <h3 className="font-heading font-semibold text-sm text-center mb-8" style={{ color: "var(--text-secondary)" }}>
            AGENTIC FLOW — EVENT TO VERIFIED RESOLUTION
          </h3>
          <div className="flex flex-wrap justify-center gap-2 items-center">
            {[
              "EVENT DISCOVERED",
              "Perception Agent",
              "Fusion Agent",
              "Camera Orchestration",
              "Incident Agent",
              "Evidence Graph",
              "Human Review",
              "Action Created",
              "Verification Agent",
              "VERIFIED",
            ].map((step, i, arr) => (
              <div key={step} className="flex items-center gap-2">
                <div
                  className="px-3 py-2 rounded-lg text-xs"
                  style={{
                    background: step === "VERIFIED" || step === "EVENT DISCOVERED"
                      ? "rgba(0,212,255,0.12)"
                      : "rgba(255,255,255,0.04)",
                    border: `1px solid ${step === "VERIFIED" || step === "EVENT DISCOVERED" ? "var(--accent-cyan)" : "rgba(255,255,255,0.08)"}`,
                    color: step === "VERIFIED" ? "var(--accent-green)" : step === "EVENT DISCOVERED" ? "var(--accent-cyan)" : "var(--text-secondary)",
                    fontFamily: "var(--font-mono)",
                    whiteSpace: "nowrap",
                  }}
                >
                  {step}
                </div>
                {i < arr.length - 1 && (
                  <span style={{ color: "var(--text-muted)", fontSize: "10px" }}>→</span>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
