"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const RAW_PACKET = [
  { label: "RAW FRAME", size: "2.1 MB", color: "#ff3333", icon: "🎞" },
  { label: "FULL RESOLUTION", size: "1.8 MB", color: "#ff6600", icon: "📸" },
  { label: "AUDIO STREAM", size: "0.4 MB", color: "#ffaa00", icon: "🔊" },
  { label: "METADATA", size: "0.8 KB", color: "#aaaaaa", icon: "📋" },
];

const EVENT_PACKET = [
  { label: "CAMERA ID", size: "12 B", color: "#00d4ff", icon: "🆔" },
  { label: "GPS + TIMESTAMP", size: "24 B", color: "#4488ff", icon: "📍" },
  { label: "EVENT CLASS", size: "4 B", color: "#00d4ff", icon: "🏷" },
  { label: "CONFIDENCE", size: "4 B", color: "#4488ff", icon: "📊" },
  { label: "BOUNDING BOX", size: "16 B", color: "#00d4ff", icon: "📐" },
  { label: "EMBEDDING", size: "512 B", color: "#4488ff", icon: "🧠" },
  { label: "THUMBNAIL (opt)", size: "12 KB", color: "#00d4ff", icon: "🖼" },
];

export default function EdgeBandwidthSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".edge-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".packet-item",
        { opacity: 0, x: -20 },
        {
          opacity: 1, x: 0, duration: 0.4, stagger: 0.05,
          scrollTrigger: { trigger: ".packet-grid", start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".feature-card",
        { opacity: 0, y: 20 },
        {
          opacity: 1, y: 0, duration: 0.6, stagger: 0.15,
          scrollTrigger: { trigger: ".features-grid", start: "top 85%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <Section
      ref={sectionRef as any}
      id="bandwidth"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-green), transparent)" }}
      />

      <PageContainer>
        <div className="edge-header">
          <SectionHeader
            eyebrow="Edge AI + Low-Bandwidth Design"
            title={
              <>
                Raw Video Streaming is <span className="text-text-muted font-light">Wasteful.</span>
                <br />
                <span className="gradient-text">Semantic Events are Intelligent.</span>
              </>
            }
            description="AI runs onboard the bus. Only meaningful events are transmitted. Full clips upload only when escalated. Bandwidth savings: up to 99.95%."
          />
        </div>

        <div className="packet-grid grid lg:grid-cols-2 gap-8 lg:gap-12 mb-16 items-stretch">
          
          {/* Raw stream (Old Way) */}
          <div className="p-8 lg:p-10 rounded-3xl flex flex-col h-full glass-card hover:scale-[1.01] transition-transform" style={{ background: "rgba(255,51,51,0.03)", borderColor: "rgba(255,51,51,0.15)" }}>
            <div className="flex items-center gap-4 mb-8">
              <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse shadow-[0_0_15px_rgba(255,51,51,0.8)]" />
              <h3 className="font-heading font-bold text-xl tracking-tight text-white">
                Raw Stream Upload <span className="text-text-muted font-normal text-sm ml-2">(Old Way)</span>
              </h3>
            </div>
            
            <div className="space-y-4 mb-8 flex-1">
              {RAW_PACKET.map((item) => (
                <div
                  key={item.label}
                  className="packet-item opacity-0 flex items-center gap-4 p-4 rounded-xl"
                  style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,51,51,0.1)" }}
                >
                  <span className="text-xl">{item.icon}</span>
                  <span className="flex-1 text-sm font-medium text-text-primary">
                    {item.label}
                  </span>
                  <span className="font-mono text-sm font-bold" style={{ color: item.color }}>
                    {item.size}
                  </span>
                </div>
              ))}
            </div>
            
            <div className="text-center p-6 rounded-2xl glass-card" style={{ background: "rgba(255,51,51,0.08)", borderColor: "rgba(255,51,51,0.25)" }}>
              <div className="font-heading font-bold text-2xl mb-1" style={{ color: "#ff5555" }}>
                ≈ 4.3 MB / frame
              </div>
              <div className="text-sm font-medium" style={{ color: "rgba(255,255,255,0.7)" }}>
                @30fps = ~1000 Mbps per camera. Impractical for fleets.
              </div>
            </div>
          </div>

          {/* Event capsule (UrbanPulse Way) */}
          <div className="p-8 lg:p-10 rounded-3xl flex flex-col h-full glass-card hover:scale-[1.01] transition-transform" style={{ background: "rgba(0,255,136,0.03)", borderColor: "rgba(0,255,136,0.2)" }}>
            <div className="flex items-center gap-4 mb-8">
              <div className="w-3 h-3 rounded-full animate-pulse shadow-[0_0_15px_rgba(0,255,136,0.8)]" style={{ background: "var(--accent-green)" }} />
              <h3 className="font-heading font-bold text-xl tracking-tight text-white">
                Semantic Event Capsule <span className="text-text-muted font-normal text-sm ml-2">(UrbanPulse)</span>
              </h3>
            </div>
            
            <div className="space-y-3 mb-8 flex-1">
              {EVENT_PACKET.map((item) => (
                <div
                  key={item.label}
                  className="packet-item opacity-0 flex items-center gap-4 p-3 rounded-xl"
                  style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(0,255,136,0.15)" }}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="flex-1 text-sm font-medium text-text-primary">
                    {item.label}
                  </span>
                  <span className="font-mono text-sm font-bold" style={{ color: item.color }}>
                    {item.size}
                  </span>
                </div>
              ))}
            </div>
            
            <div
              className="text-center p-6 rounded-2xl glass-card"
              style={{ background: "rgba(0,255,136,0.08)", borderColor: "rgba(0,255,136,0.3)" }}
            >
              <div className="font-heading font-bold text-2xl mb-1" style={{ color: "var(--accent-green)" }}>
                &lt; 2 KB / event
              </div>
              <div className="text-sm font-medium" style={{ color: "rgba(255,255,255,0.7)" }}>
                Only when meaningful. 99.95% less data bandwidth.
              </div>
            </div>
          </div>
        </div>

        {/* Store and forward + pipeline */}
        <div className="features-grid grid md:grid-cols-3 gap-6 lg:gap-8">
          {[
            {
              title: "Store & Forward",
              icon: "💾",
              color: "#4488ff",
              desc: "Poor connectivity? Events queue locally. Upload resumes when connection returns. Critical events prioritized. No data lost.",
              r: 68, g: 136, b: 255
            },
            {
              title: "Escalate to Clip",
              icon: "🎬",
              color: "#ffaa00",
              desc: "Only high-priority incidents trigger a clip upload request. Clips are short, relevant windows — not 24-hour recordings.",
              r: 255, g: 170, b: 0
            },
            {
              title: "Privacy First",
              icon: "🔐",
              color: "#00ff88",
              desc: "Faces and plates blurred on edge before any upload. Evidence retained only for confirmed events. Auditable access log.",
              r: 0, g: 255, b: 136
            },
          ].map((item) => (
            <div
              key={item.title}
              className="feature-card opacity-0 p-8 rounded-3xl glass-card transition-transform duration-300 hover:-translate-y-2"
              style={{
                background: `rgba(${item.r}, ${item.g}, ${item.b}, 0.04)`,
                borderColor: `rgba(${item.r}, ${item.g}, ${item.b}, 0.15)`,
              }}
            >
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl mb-6 relative overflow-hidden">
                 <div className="absolute inset-0 opacity-20" style={{ background: item.color }} />
                 <span className="relative z-10">{item.icon}</span>
              </div>
              <h4 className="font-heading font-bold text-lg mb-3 tracking-tight text-white">
                {item.title}
              </h4>
              <p className="text-sm leading-relaxed text-text-secondary">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </PageContainer>
    </Section>
  );
}
