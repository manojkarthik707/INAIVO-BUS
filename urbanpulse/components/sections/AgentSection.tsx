"use client";

import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

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
  const [activeAgent, setActiveAgent] = useState<string>("perception"); // Default to Perception

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

  const active = AGENTS.find((a) => a.id === activeAgent) || AGENTS[0];

  return (
    <Section
      ref={sectionRef as any}
      id="agents"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, #8855ff, transparent)" }}
      />

      <PageContainer>
        <div className="agent-header">
          <SectionHeader
            eyebrow="AGENTIC AI ORCHESTRATION LAYER"
            title={
              <>
                10 Specialized AI Agents. <br className="hidden md:block" />
                <span className="gradient-text">One Cooperative System.</span>
              </>
            }
            description="UrbanPulse Fusion behaves as an intelligent operational system, not a passive dashboard. Specialized agents coordinate to discover, corroborate, reconstruct and verify."
          />
        </div>

        <div className="grid lg:grid-cols-[65%_35%] gap-8 items-start">
          {/* Agent grid - 65% width */}
          <div className="w-full">
            <div className="agent-grid grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 lg:gap-5">
              {AGENTS.map((agent) => {
                const isActive = activeAgent === agent.id;
                
                // Hex to RGB conversion
                let r = 0, g = 0, b = 0;
                if (agent.color.length === 7) {
                  r = parseInt(agent.color.substring(1, 3), 16);
                  g = parseInt(agent.color.substring(3, 5), 16);
                  b = parseInt(agent.color.substring(5, 7), 16);
                }

                return (
                  <button
                    key={agent.id}
                    id={`agent-${agent.id}`}
                    onClick={() => setActiveAgent(agent.id)}
                    className="agent-card opacity-0 text-left p-5 rounded-2xl transition-all duration-300 group flex flex-col h-full glass-card"
                    style={{
                      background: isActive
                        ? `rgba(${r}, ${g}, ${b}, 0.12)`
                        : "var(--bg-card)",
                      borderColor: isActive ? agent.color : "var(--border-glass)",
                      boxShadow: isActive ? `0 10px 30px ${agent.color}22` : "none",
                      transform: isActive ? "translateY(-4px)" : "none",
                    }}
                  >
                    <div className="text-4xl mb-4">{agent.icon}</div>
                    <div className="font-heading font-bold text-[15px] mb-2 leading-tight transition-colors" style={{ color: isActive ? agent.color : "var(--text-primary)" }}>
                      {agent.label}
                    </div>
                    <div className="text-[13px] leading-relaxed line-clamp-3 text-text-muted mt-auto">
                      {agent.shortDesc}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Active agent detail - 35% width */}
          <div className="w-full sticky top-24">
            <div
              className="p-8 rounded-3xl h-full flex flex-col glass-card"
              style={{
                borderColor: `${active.color}44`,
                boxShadow: `0 8px 32px rgba(0,0,0,0.15)`,
              }}
            >
              {/* Optional animated glow background based on agent color */}
              <div 
                className="absolute inset-0 opacity-10 pointer-events-none rounded-3xl"
                style={{
                  background: `radial-gradient(circle at top right, ${active.color}, transparent 60%)`
                }}
              />

              <div className="relative z-10">
                <div className="text-5xl mb-6">{active.icon}</div>
                <h3 className="font-heading font-extrabold text-2xl mb-3 tracking-tight" style={{ color: active.color }}>
                  {active.label}
                </h3>
                <p className="text-[15px] mb-8 leading-relaxed text-text-secondary">
                  {active.shortDesc}
                </p>
                <h4 className="label-text mb-4 text-text-muted tracking-widest uppercase">
                  RESPONSIBILITIES
                </h4>
                <ul className="space-y-4 flex-1">
                  {active.tasks.map((task, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-text-primary">
                      <span className="mt-0.5" style={{ color: active.color, flexShrink: 0, textShadow: `0 0 10px ${active.color}` }}>✦</span>
                      {task}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Agentic flow */}
        <div className="mt-24 max-w-full overflow-hidden">
          <h3 className="font-heading font-bold text-sm text-center mb-10 tracking-[0.2em] text-text-secondary uppercase">
            Agentic Flow — Event to Verified Resolution
          </h3>
          <div className="flex flex-wrap justify-center gap-2 md:gap-3 items-center">
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
              <div key={i} className="flex items-center gap-2 md:gap-3">
                <div
                  className="px-3 py-2 md:px-4 md:py-2.5 rounded-xl text-xs md:text-[13px] font-medium transition-all"
                  style={{
                    background: step === "VERIFIED" || step === "EVENT DISCOVERED"
                      ? "rgba(0,212,255,0.12)"
                      : "rgba(255,255,255,0.04)",
                    border: `1px solid ${step === "VERIFIED" || step === "EVENT DISCOVERED" ? "rgba(0,212,255,0.3)" : "rgba(255,255,255,0.08)"}`,
                    color: step === "VERIFIED" ? "var(--accent-green)" : step === "EVENT DISCOVERED" ? "var(--accent-cyan)" : "var(--text-primary)",
                    fontFamily: "var(--font-mono)",
                    whiteSpace: "nowrap",
                  }}
                >
                  {step}
                </div>
                {i < arr.length - 1 && (
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-text-muted opacity-50 md:w-4 md:h-4">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                )}
              </div>
            ))}
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
