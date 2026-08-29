"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const RAW_PACKET = [
  { label: "RAW FRAME", size: "2.1 MB", color: "#ff3333", icon: "🎞" },
  { label: "FULL RESOLUTION", size: "1.8 MB", color: "#ff6600", icon: "📸" },
  { label: "AUDIO STREAM", size: "0.4 MB", color: "#ffaa00", icon: "🔊" },
  { label: "METADATA", size: "0.8 KB", color: "#aaaaaa", icon: "📋" },
  { label: "TOTAL / FRAME", size: "≈ 4.3 MB", color: "#ff3333", icon: "📦" },
];

const EVENT_PACKET = [
  { label: "CAMERA ID", size: "12 B", color: "#00d4ff", icon: "🆔" },
  { label: "GPS + TIMESTAMP", size: "24 B", color: "#4488ff", icon: "📍" },
  { label: "EVENT CLASS", size: "4 B", color: "#00d4ff", icon: "🏷" },
  { label: "CONFIDENCE", size: "4 B", color: "#4488ff", icon: "📊" },
  { label: "BOUNDING BOX", size: "16 B", color: "#00d4ff", icon: "📐" },
  { label: "EMBEDDING", size: "512 B", color: "#4488ff", icon: "🧠" },
  { label: "THUMBNAIL (opt)", size: "12 KB", color: "#00d4ff", icon: "🖼" },
  { label: "TOTAL / EVENT", size: "< 2 KB", color: "#00ff88", icon: "⚡" },
];

export default function EdgeBandwidthSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
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
          opacity: 1, x: 0, duration: 0.4, stagger: 0.06,
          scrollTrigger: { trigger: ".packet-grid", start: "top 80%" },
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
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-green), transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="edge-header text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(0,255,136,0.08)", border: "1px solid rgba(0,255,136,0.25)" }}
          >
            <span className="label-text" style={{ color: "var(--accent-green)" }}>
              Edge AI + Low-Bandwidth Design
            </span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            Raw Video Streaming is{" "}
            <span style={{ color: "var(--text-muted)" }}>Wasteful.</span>
            <br />
            <span className="gradient-text">Semantic Events are Intelligent.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            AI runs onboard the bus. Only meaningful events are transmitted.
            Full clips upload only when escalated. Bandwidth savings: up to 99.95%.
          </p>
        </div>

        <div className="packet-grid grid lg:grid-cols-2 gap-8 mb-16 items-stretch">
          {/* Raw stream */}
          <div className="p-8 rounded-2xl flex flex-col h-full" style={{ background: "rgba(255,51,51,0.05)", border: "1px solid rgba(255,51,51,0.15)" }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
              <h3 className="font-heading font-semibold" style={{ color: "#ff5555" }}>
                Raw Stream Upload (Old Way)
              </h3>
            </div>
            <div className="space-y-3 mb-6 flex-1">
              {RAW_PACKET.map((item) => (
                <div
                  key={item.label}
                  className="packet-item opacity-0 flex items-center gap-4 p-3 rounded-lg"
                  style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,51,51,0.1)" }}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="flex-1 text-xs" style={{ color: "var(--text-secondary)" }}>
                    {item.label}
                  </span>
                  <span className="font-mono text-xs font-semibold" style={{ color: item.color }}>
                    {item.size}
                  </span>
                </div>
              ))}
            </div>
            <div className="text-center p-4 rounded-xl" style={{ background: "rgba(255,51,51,0.1)", border: "1px solid rgba(255,51,51,0.2)" }}>
              <div className="font-mono font-bold text-xl" style={{ color: "#ff3333" }}>
                ≈ 4.3 MB / frame
              </div>
              <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                @30fps = ~155 Mbps per camera. Impractical for fleets.
              </div>
            </div>
          </div>

          {/* Event capsule */}
          <div className="p-8 rounded-2xl flex flex-col h-full" style={{ background: "rgba(0,212,255,0.05)", border: "1px solid rgba(0,212,255,0.2)" }}>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-3 h-3 rounded-full animate-pulse" style={{ background: "var(--accent-green)" }} />
              <h3 className="font-heading font-semibold" style={{ color: "var(--accent-cyan)" }}>
                Semantic Event Capsule (UrbanPulse Way)
              </h3>
            </div>
            <div className="space-y-3 mb-6 flex-1">
              {EVENT_PACKET.map((item) => (
                <div
                  key={item.label}
                  className="packet-item opacity-0 flex items-center gap-4 p-3 rounded-lg"
                  style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(0,212,255,0.1)" }}
                >
                  <span className="text-lg">{item.icon}</span>
                  <span className="flex-1 text-xs" style={{ color: "var(--text-secondary)" }}>
                    {item.label}
                  </span>
                  <span className="font-mono text-xs font-semibold" style={{ color: item.color }}>
                    {item.size}
                  </span>
                </div>
              ))}
            </div>
            <div
              className="text-center p-4 rounded-xl"
              style={{ background: "rgba(0,255,136,0.08)", border: "1px solid rgba(0,255,136,0.25)" }}
            >
              <div className="font-heading font-bold text-xl" style={{ color: "var(--accent-green)" }}>
                &lt; 2 KB / event
              </div>
              <div className="text-xs mt-1" style={{ color: "var(--text-muted)" }}>
                Only when something meaningful is detected. 99.95% less data.
              </div>
            </div>
          </div>
        </div>

        {/* Store and forward + pipeline */}
        <div className="grid md:grid-cols-3 gap-6">
          {[
            {
              title: "Store & Forward",
              icon: "💾",
              color: "#4488ff",
              desc: "Poor connectivity? Events queue locally. Upload resumes when connection returns. Critical events prioritized. No data lost.",
            },
            {
              title: "Escalate to Clip",
              icon: "🎬",
              color: "#ffaa00",
              desc: "Only high-priority incidents trigger a clip upload request. Clips are short, relevant windows — not 24-hour recordings.",
            },
            {
              title: "Privacy First",
              icon: "🔐",
              color: "#00ff88",
              desc: "Faces and plates blurred on edge before any upload. Evidence retained only for confirmed events. Auditable access log.",
            },
          ].map((item) => (
            <div
              key={item.title}
              className="p-6 rounded-xl"
              style={{
                background: `rgba(${item.color === "#4488ff" ? "68,136,255" : item.color === "#ffaa00" ? "255,170,0" : "0,255,136"}, 0.06)`,
                border: `1px solid ${item.color}33`,
              }}
            >
              <div className="text-3xl mb-4">{item.icon}</div>
              <h4 className="font-heading font-semibold mb-2" style={{ color: item.color }}>
                {item.title}
              </h4>
              <p className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
