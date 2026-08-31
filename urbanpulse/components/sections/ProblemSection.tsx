"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

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
    <Section
      ref={sectionRef as any}
      id="problem"
      style={{ background: "var(--bg-surface)" }}
    >
      {/* Top border line */}
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-blue), transparent)" }}
      />

      <PageContainer>
        <div className="problem-header">
          <SectionHeader
            eyebrow="THE PROBLEM WITH CURRENT SYSTEMS"
            title={
              <>
                Smart City Cameras Are <span style={{ color: "#ff6633" }}>Brilliant in Isolation.</span>
                <br />
                <span className="text-text-secondary">Blind as a System.</span>
              </>
            }
            description="Current camera deployments generate alerts, not intelligence. Detection without corroboration. Coverage without memory. Technology without a closed loop."
          />
        </div>

        {/* Problem cards */}
        <div className="problem-grid grid sm:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 mb-32">
          {PROBLEMS.map((p) => (
            <div
              key={p.id}
              className="problem-card opacity-0 glass-card group flex flex-col justify-between h-full transition-transform duration-300 hover:scale-[1.02]"
              style={{
                background: `rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.05)`,
                borderColor: `rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.15)`,
              }}
            >
              <div>
                <div className="mb-5">{p.icon}</div>
                <h3
                  className="font-heading font-bold text-xl mb-4 tracking-tight"
                  style={{ color: p.color }}
                >
                  {p.title}
                </h3>
                <p className="text-body mb-8 text-text-secondary">
                  {p.body}
                </p>
              </div>
              <div
                className="pt-5"
                style={{ borderTop: `1px solid rgba(${p.color === "#ff3333" ? "255,51,51" : p.color === "#ffaa00" ? "255,170,0" : "136,85,255"}, 0.15)` }}
              >
                <div className="font-mono font-bold text-2xl" style={{ color: p.color }}>
                  {p.stat}
                </div>
                <div className="text-xs mt-1 text-text-muted">
                  {p.statLabel}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Fusion diagram */}
        <div className="fusion-diagram max-w-4xl mx-auto flex flex-col items-center">
          <div className="text-center mb-10 w-full">
            <h3 className="text-subtitle font-heading font-bold mb-3 text-text-primary">
              The Solution: Cooperative Perception
            </h3>
            <p className="text-body text-text-secondary">
              Three camera layers. One intelligence network. Zero wasted observations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full items-stretch">
            {[
              { label: "Moving Cameras", sub: "Coverage + Discovery", color: "#00d4ff" },
              { label: "Fixed Cameras", sub: "Continuity + Trajectory", color: "#4488ff" },
              { label: "Existing CCTV", sub: "Low-CAPEX Extension", color: "#8855ff" },
            ].map((src) => (
              <div
                key={src.label}
                className="p-5 rounded-xl text-center glass-card"
                style={{
                  background: `rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.08)`,
                  borderColor: `rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.2)`,
                }}
              >
                <div className="font-heading font-semibold text-sm mb-1" style={{ color: src.color }}>
                  {src.label}
                </div>
                <div className="text-xs text-text-muted">
                  {src.sub}
                </div>
              </div>
            ))}
          </div>

          {/* Arrow converging (hidden on very small mobile for layout simplicity, visible md+) */}
          <div className="hidden md:flex justify-center my-6 w-full relative">
            <svg width="400" height="40" viewBox="0 0 400 40" className="max-w-full">
              <path
                className="fusion-arrow"
                d="M50 5 L200 35"
                stroke="#4488ff"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeDasharray="4 3"
                opacity="0.6"
              />
              <path
                className="fusion-arrow"
                d="M200 5 L200 35"
                stroke="#00d4ff"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
              <path
                className="fusion-arrow"
                d="M350 5 L200 35"
                stroke="#8855ff"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeDasharray="4 3"
                opacity="0.6"
              />
              <circle cx="200" cy="38" r="4" fill="#00d4ff" />
            </svg>
          </div>
          
          {/* Mobile connecting arrow */}
          <div className="md:hidden flex justify-center my-4">
             <div className="w-[2px] h-8 bg-gradient-to-b from-cyan-500/50 to-cyan-500" />
          </div>

          <div
            className="p-6 rounded-2xl text-center glass-card w-full md:w-auto md:min-w-[400px]"
            style={{
              background: "rgba(0, 100, 200, 0.1)",
              borderColor: "rgba(0, 212, 255, 0.3)",
              boxShadow: "0 0 40px rgba(0, 212, 255, 0.08)",
            }}
          >
            <div className="font-heading text-xl font-bold gradient-text mb-2">
              UrbanPulse Fusion
            </div>
            <div className="text-sm text-text-secondary">
              Persistent Urban Objects · Fleet Consensus · Closed-Loop Verification
            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
