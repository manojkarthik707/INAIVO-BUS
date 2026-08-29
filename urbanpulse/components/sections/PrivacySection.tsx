"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const PRINCIPLES = [
  { icon: "🏗", title: "Edge-First Processing", desc: "AI runs onboard. Raw video never leaves the vehicle without cause.", color: "#00d4ff" },
  { icon: "📦", title: "Event-Only Upload", desc: "Only semantic events transmitted. Minimum required evidence principle.", color: "#4488ff" },
  { icon: "🔐", title: "Encrypted Buffers", desc: "Local ring buffer encrypted at rest. Secure transport in transit.", color: "#8855ff" },
  { icon: "👤", title: "PII Masking", desc: "Faces and plates blurred at edge before any upload. Privacy preserved.", color: "#ff8800" },
  { icon: "🎭", title: "Role-Based Access", desc: "Evidence accessible only to authorized roles. Full audit trail.", color: "#00ff88" },
  { icon: "📋", title: "Retention Policy", desc: "Configurable retention. Unrelated footage not stored indefinitely.", color: "#ffaa00" },
  { icon: "🔍", title: "Explainable Confidence", desc: "Every decision shows evidence used, uncertainty, and camera health.", color: "#00d4ff" },
  { icon: "👁", title: "Human Oversight", desc: "Enforcement actions require human review. System is assistive, not autonomous.", color: "#ff3333" },
  { icon: "📊", title: "Inference Metadata", desc: "Model version, camera health, and quality score attached to every event.", color: "#4488ff" },
];

export default function PrivacySection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".privacy-card",
        { opacity: 0, scale: 0.95 },
        {
          opacity: 1, scale: 1, duration: 0.4, stagger: 0.07,
          scrollTrigger: { trigger: ".privacy-grid", start: "top 80%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative py-32"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, #00ff88, transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(0,255,136,0.08)", border: "1px solid rgba(0,255,136,0.25)" }}
          >
            <span className="label-text" style={{ color: "var(--accent-green)" }}>
              Privacy, Trust & Transparency
            </span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            Intelligence Without{" "}
            <span style={{ color: "var(--accent-green)" }}>Surveillance.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            Privacy is engineered into every layer — not bolted on after.
            The system collects what it needs, retains what is justified, and
            shows its reasoning every step of the way.
          </p>
        </div>

        <div className="privacy-grid grid md:grid-cols-3 gap-4 mb-16">
          {PRINCIPLES.map((p) => (
            <div
              key={p.title}
              className="privacy-card opacity-0 p-5 rounded-xl group transition-all duration-300 hover:scale-[1.02]"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.07)",
              }}
            >
              <div className="text-2xl mb-3">{p.icon}</div>
              <h4 className="font-heading font-semibold text-sm mb-2" style={{ color: p.color }}>
                {p.title}
              </h4>
              <p className="text-xs leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                {p.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Camera trust model */}
        <div
          className="p-8 rounded-2xl"
          style={{ background: "rgba(0,100,200,0.06)", border: "1px solid rgba(0,212,255,0.15)" }}
        >
          <h3 className="font-heading font-semibold text-lg mb-6 text-center" style={{ color: "var(--text-primary)" }}>
            Camera Trust Score Model
          </h3>
          <div className="grid md:grid-cols-4 gap-4">
            {[
              { label: "Model Confidence", val: 91, color: "#00d4ff" },
              { label: "Camera Quality", val: 78, color: "#4488ff" },
              { label: "GPS Accuracy", val: 89, color: "#8855ff" },
              { label: "Independent Confirms", val: 3, isCount: true, color: "#00ff88" },
            ].map((item) => (
              <div
                key={item.label}
                className="p-4 rounded-xl text-center"
                style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}
              >
                <div className="font-mono font-bold text-2xl mb-1" style={{ color: item.color }}>
                  {item.isCount ? item.val : `${item.val}%`}
                </div>
                <div className="text-xs" style={{ color: "var(--text-muted)" }}>{item.label}</div>
                {!item.isCount && (
                  <div className="mt-3 h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.08)" }}>
                    <div className="h-full rounded-full" style={{ width: `${item.val}%`, background: item.color }} />
                  </div>
                )}
              </div>
            ))}
          </div>
          <p className="text-xs text-center mt-6" style={{ color: "var(--text-muted)" }}>
            Final evidence confidence is calculated from all signals — not just the detector score.
            Uncertainty is always disclosed.
          </p>
        </div>
      </div>
    </section>
  );
}
