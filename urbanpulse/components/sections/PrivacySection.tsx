"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const PRINCIPLES = [
  { icon: "🏗", title: "Edge-First Processing", desc: "AI runs onboard. Raw video never leaves the vehicle without cause.", color: "#00d4ff", r: 0, g: 212, b: 255 },
  { icon: "📦", title: "Event-Only Upload", desc: "Only semantic events transmitted. Minimum required evidence principle.", color: "#4488ff", r: 68, g: 136, b: 255 },
  { icon: "🔐", title: "Encrypted Buffers", desc: "Local ring buffer encrypted at rest. Secure transport in transit.", color: "#8855ff", r: 136, g: 85, b: 255 },
  { icon: "👤", title: "PII Masking", desc: "Faces and plates blurred at edge before any upload. Privacy preserved.", color: "#ff8800", r: 255, g: 136, b: 0 },
  { icon: "🎭", title: "Role-Based Access", desc: "Evidence accessible only to authorized roles. Full audit trail.", color: "#00ff88", r: 0, g: 255, b: 136 },
  { icon: "📋", title: "Retention Policy", desc: "Configurable retention. Unrelated footage not stored indefinitely.", color: "#ffaa00", r: 255, g: 170, b: 0 },
  { icon: "🔍", title: "Explainable Confidence", desc: "Every decision shows evidence used, uncertainty, and camera health.", color: "#00d4ff", r: 0, g: 212, b: 255 },
  { icon: "👁", title: "Human Oversight", desc: "Enforcement actions require human review. System is assistive, not autonomous.", color: "#ff3333", r: 255, g: 51, b: 51 },
  { icon: "📊", title: "Inference Metadata", desc: "Model version, camera health, and quality score attached to every event.", color: "#4488ff", r: 68, g: 136, b: 255 },
];

export default function PrivacySection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".privacy-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".privacy-card",
        { opacity: 0, scale: 0.95, y: 20 },
        {
          opacity: 1, scale: 1, y: 0, duration: 0.4, stagger: 0.05,
          scrollTrigger: { trigger: ".privacy-grid", start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".trust-model",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: ".trust-model", start: "top 85%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <Section
      ref={sectionRef as any}
      id="privacy"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, #00ff88, transparent)" }}
      />

      <PageContainer>
        <div className="privacy-header">
          <SectionHeader
            eyebrow="Privacy, Trust & Transparency"
            title={
              <>
                Intelligence Without <br className="hidden md:block" />
                <span style={{ color: "var(--accent-green)" }}>Surveillance.</span>
              </>
            }
            description="Privacy is engineered into every layer — not bolted on after. The system collects what it needs, retains what is justified, and shows its reasoning every step of the way."
          />
        </div>

        <div className="privacy-grid grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5 lg:gap-6 mb-20">
          {PRINCIPLES.map((p) => (
            <div
              key={p.title}
              className="privacy-card opacity-0 p-6 rounded-2xl glass-card transition-all duration-300 hover:-translate-y-1 hover:shadow-lg flex flex-col"
              style={{
                borderColor: `rgba(${p.r},${p.g},${p.b},0.15)`,
                background: `rgba(${p.r},${p.g},${p.b},0.03)`,
              }}
            >
              <div className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-5 relative overflow-hidden flex-shrink-0">
                <div className="absolute inset-0 opacity-20" style={{ background: p.color }} />
                <span className="relative z-10">{p.icon}</span>
              </div>
              <h4 className="font-heading font-bold text-base mb-2" style={{ color: p.color }}>
                {p.title}
              </h4>
              <p className="text-[13px] leading-relaxed text-text-secondary mt-auto">
                {p.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Camera trust model */}
        <div
          className="trust-model p-8 md:p-12 rounded-3xl glass-card relative overflow-hidden"
          style={{ background: "rgba(0,100,200,0.04)", borderColor: "rgba(0,212,255,0.2)" }}
        >
          {/* Subtle glow */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent pointer-events-none" />

          <div className="relative z-10">
            <h3 className="font-heading font-bold text-2xl mb-8 text-center text-text-primary tracking-tight">
              Camera Trust Score Model
            </h3>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {[
                { label: "Model Confidence", val: 91, color: "var(--accent-cyan)", r: 0, g: 212, b: 255 },
                { label: "Camera Quality", val: 78, color: "var(--accent-blue)", r: 68, g: 136, b: 255 },
                { label: "GPS Accuracy", val: 89, color: "var(--accent-electric)", r: 136, g: 85, b: 255 },
                { label: "Independent Confirms", val: 3, isCount: true, color: "var(--accent-green)", r: 0, g: 255, b: 136 },
              ].map((item) => (
                <div
                  key={item.label}
                  className="p-5 rounded-2xl text-center glass-card hover:scale-[1.02] transition-transform"
                  style={{ 
                    background: "rgba(255,255,255,0.02)", 
                    borderColor: `rgba(${item.r},${item.g},${item.b},0.2)` 
                  }}
                >
                  <div className="font-heading font-bold text-3xl mb-2" style={{ color: item.color }}>
                    {item.isCount ? item.val : `${item.val}%`}
                  </div>
                  <div className="text-[11px] font-bold uppercase tracking-widest text-text-muted">{item.label}</div>
                  {!item.isCount && (
                    <div className="mt-4 h-1.5 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.1)" }}>
                      <div className="h-full rounded-full" style={{ width: `${item.val}%`, background: item.color, boxShadow: `0 0 10px ${item.color}88` }} />
                    </div>
                  )}
                </div>
              ))}
            </div>
            
            <p className="text-sm text-center mt-8 text-text-secondary max-w-2xl mx-auto">
              Final evidence confidence is calculated from all signals — not just the detector score.
              Uncertainty is always disclosed.
            </p>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
