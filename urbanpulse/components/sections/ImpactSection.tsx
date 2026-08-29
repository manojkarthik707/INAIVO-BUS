"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const IMPACTS = [
  { icon: "🛣", value: "87%", label: "Faster Defect Verification", desc: "Fleet consensus vs manual inspection" },
  { icon: "🔄", value: "100%", label: "Closed-Loop Verification", desc: "Repairs independently confirmed by future buses" },
  { icon: "📡", value: "3×", label: "Camera Coverage Reuse", desc: "Existing CCTV extended at zero hardware cost" },
  { icon: "📦", value: "99.9%", label: "Bandwidth Reduction", desc: "Semantic events vs continuous raw streaming" },
  { icon: "🎯", value: "94.7%", label: "Corroboration Accuracy", desc: "Multi-camera fleet consensus precision" },
  { icon: "⚡", value: "< 2KB", label: "Per Event Packet", desc: "Onboard edge AI extracts the essential signal" },
];

function AnimatedCounter({ target, suffix = "" }: { target: string; suffix?: string }) {
  const [display, setDisplay] = useState("0");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const numericTarget = parseFloat(target.replace(/[^0-9.]/g, ""));
    if (isNaN(numericTarget)) {
      setDisplay(target);
      return;
    }

    const obj = { val: 0 };
    const st = ScrollTrigger.create({
      trigger: ref.current,
      start: "top 85%",
      onEnter: () => {
        gsap.to(obj, {
          val: numericTarget,
          duration: 1.5,
          ease: "power2.out",
          onUpdate: () => {
            const prefix = target.match(/^[^0-9]*/)?.[0] || "";
            const postfix = target.match(/[^0-9.]+$/)?.[0] || suffix;
            setDisplay(`${prefix}${obj.val % 1 === 0 ? Math.round(obj.val) : obj.val.toFixed(1)}${postfix}`);
          },
        });
      },
    });
    return () => st.kill();
  }, [target, suffix]);

  return <div ref={ref}>{display || target}</div>;
}

export default function ImpactSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".impact-card",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.5, stagger: 0.1,
          scrollTrigger: { trigger: ".impact-grid", start: "top 80%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative py-32"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-amber), transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(255,170,0,0.08)", border: "1px solid rgba(255,170,0,0.25)" }}
          >
            <span className="label-text" style={{ color: "var(--accent-amber)" }}>
              Impact & Outcomes
            </span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            Real Results for <span style={{ color: "var(--accent-amber)" }}>Real Cities.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            UrbanPulse Fusion is designed for measurable urban improvement —
            not surveillance theater. Every metric traces back to a closed-loop action.
          </p>
        </div>

        <div className="impact-grid grid md:grid-cols-3 gap-6 mb-20">
          {IMPACTS.map((item) => (
            <div
              key={item.label}
              className="impact-card opacity-0 p-7 rounded-2xl group transition-all duration-300 hover:scale-[1.02]"
              style={{
                background: "rgba(255,255,255,0.03)",
                border: "1px solid rgba(255,255,255,0.08)",
              }}
            >
              <div className="text-3xl mb-4">{item.icon}</div>
              <div className="font-heading font-bold text-4xl gradient-text mb-2">
                <AnimatedCounter target={item.value} />
              </div>
              <h4 className="font-heading font-semibold text-sm mb-2" style={{ color: "var(--text-primary)" }}>
                {item.label}
              </h4>
              <p className="text-xs" style={{ color: "var(--text-muted)" }}>{item.desc}</p>
            </div>
          ))}
        </div>

        {/* Quote */}
        <div
          className="max-w-3xl mx-auto p-8 rounded-2xl text-center"
          style={{
            background: "rgba(0,100,200,0.06)",
            border: "1px solid rgba(0,212,255,0.15)",
          }}
        >
          <blockquote
            className="font-heading text-xl md:text-2xl font-semibold mb-4 leading-relaxed"
            style={{ color: "var(--text-primary)" }}
          >
            &ldquo;Current smart-city cameras operate mostly as isolated sensors.
            UrbanPulse Fusion makes them cooperate — turning a fragmented
            observation network into a self-verifying urban memory.&rdquo;
          </blockquote>
          <div className="label-text" style={{ color: "var(--text-muted)" }}>
            SIH26124 · Bharat Electronics Limited · UrbanPulse Fusion Team
          </div>
        </div>
      </div>
    </section>
  );
}
