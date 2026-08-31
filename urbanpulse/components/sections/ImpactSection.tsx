"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

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
    return () => {
      st.kill();
    };
  }, [target, suffix]);

  return <div ref={ref}>{display || target}</div>;
}

export default function ImpactSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".impact-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".impact-card",
        { opacity: 0, y: 40, scale: 0.95 },
        {
          opacity: 1, y: 0, scale: 1, duration: 0.6, stagger: 0.1,
          scrollTrigger: { trigger: ".impact-grid", start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".impact-quote",
        { opacity: 0, scale: 0.95 },
        {
          opacity: 1, scale: 1, duration: 0.8,
          scrollTrigger: { trigger: ".impact-quote", start: "top 85%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <Section
      ref={sectionRef as any}
      id="impact"
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-amber), transparent)" }}
      />

      <PageContainer>
        <div className="impact-header">
          <SectionHeader
            eyebrow="Impact & Outcomes"
            title={
              <>
                Real Results for <span style={{ color: "var(--accent-amber)" }}>Real Cities.</span>
              </>
            }
            description="UrbanPulse Fusion is designed for measurable urban improvement — not surveillance theater. Every metric traces back to a closed-loop action."
          />
        </div>

        <div className="impact-grid grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 lg:gap-6 mb-24">
          {IMPACTS.map((item) => (
            <div
              key={item.label}
              className="impact-card opacity-0 p-8 rounded-3xl glass-card transition-all duration-300 hover:-translate-y-2 hover:shadow-xl group flex flex-col h-full text-center items-center"
              style={{
                borderColor: "rgba(255,170,0,0.15)",
                background: "rgba(255,170,0,0.03)",
              }}
            >
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl mb-5 relative overflow-hidden bg-black/40">
                <div className="absolute inset-0 bg-amber-500/20 group-hover:bg-amber-500/30 transition-colors" />
                <span className="relative z-10">{item.icon}</span>
              </div>
              <div className="font-heading font-extrabold text-5xl tracking-tighter mb-4" style={{ color: "var(--accent-amber)" }}>
                <AnimatedCounter target={item.value} />
              </div>
              <h4 className="font-heading font-bold text-lg mb-2 text-text-primary tracking-tight">
                {item.label}
              </h4>
              <p className="text-sm text-text-secondary leading-relaxed mt-auto">
                {item.desc}
              </p>
            </div>
          ))}
        </div>

        {/* Quote */}
        <div
          className="impact-quote max-w-4xl mx-auto p-10 md:p-14 rounded-3xl text-center glass-card relative overflow-hidden"
          style={{
            borderColor: "rgba(0,212,255,0.2)",
            background: "rgba(0,100,200,0.05)",
          }}
        >
          {/* Subtle gradient background */}
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-transparent pointer-events-none" />
          
          <div className="relative z-10">
            <blockquote
              className="font-heading text-xl md:text-3xl font-bold mb-8 leading-tight tracking-tight text-text-primary"
            >
              &ldquo;Current smart-city cameras operate mostly as isolated sensors.
              UrbanPulse Fusion makes them cooperate — turning a fragmented
              observation network into a <span className="gradient-text">self-verifying urban memory.</span>&rdquo;
            </blockquote>
            <div className="inline-flex flex-col items-center">
              <div className="font-mono font-bold text-sm tracking-widest text-accent-cyan uppercase mb-1">
                SIH26124
              </div>
              <div className="text-sm font-medium text-text-muted">
                Bharat Electronics Limited · UrbanPulse Fusion Team
              </div>
            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
