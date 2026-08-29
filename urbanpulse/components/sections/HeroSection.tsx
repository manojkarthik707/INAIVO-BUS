"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { motion } from "framer-motion";

const SOURCE_INDICATORS = [
  {
    id: "moving",
    label: "Moving Cameras",
    sublabel: "Buses · Fleet · Municipal",
    color: "#00d4ff",
    icon: "🚌",
    count: "2,847",
    unit: "camera nodes",
  },
  {
    id: "fixed",
    label: "Fixed Cameras",
    sublabel: "Junctions · Roadside · Poles",
    color: "#4488ff",
    icon: "📡",
    count: "1,203",
    unit: "fixed nodes",
  },
  {
    id: "cctv",
    label: "Existing CCTV",
    sublabel: "City Infrastructure Reuse",
    color: "#8855ff",
    icon: "🎥",
    count: "5,610",
    unit: "integrated feeds",
  },
];

const STATS = [
  { value: "94.7%", label: "Defect Corroboration Accuracy" },
  { value: "< 2KB", label: "Per Event Packet" },
  { value: "10 AI Agents", label: "Cooperative Intelligence" },
];

export default function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const subtitleRef = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ delay: 0.3 });

      tl.fromTo(
        ".hero-badge",
        { opacity: 0, y: -20 },
        { opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }
      )
        .fromTo(
          titleRef.current,
          { opacity: 0, y: 50 },
          { opacity: 1, y: 0, duration: 0.9, ease: "power3.out" },
          "-=0.2"
        )
        .fromTo(
          subtitleRef.current,
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" },
          "-=0.4"
        )
        .fromTo(
          ".hero-stat",
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: "power2.out" },
          "-=0.3"
        )
        .fromTo(
          ".hero-cta",
          { opacity: 0, scale: 0.95 },
          { opacity: 1, scale: 1, duration: 0.5, stagger: 0.1, ease: "back.out(1.4)" },
          "-=0.2"
        )
        .fromTo(
          ".source-card",
          { opacity: 0, y: 40 },
          { opacity: 1, y: 0, duration: 0.6, stagger: 0.12, ease: "power2.out" },
          "-=0.3"
        );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={containerRef}
      className="relative min-h-screen flex flex-col justify-center overflow-hidden grid-bg"
      style={{ background: "var(--bg-base)" }}
    >
      {/* Atmospheric gradient blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] rounded-full opacity-10"
          style={{
            background: "radial-gradient(circle, #0066ff, transparent 70%)",
            filter: "blur(80px)",
          }}
        />
        <div
          className="absolute top-[20%] right-[-10%] w-[500px] h-[500px] rounded-full opacity-8"
          style={{
            background: "radial-gradient(circle, #00d4ff, transparent 70%)",
            filter: "blur(80px)",
          }}
        />
        <div
          className="absolute bottom-[-10%] left-[40%] w-[400px] h-[400px] rounded-full opacity-6"
          style={{
            background: "radial-gradient(circle, #8855ff, transparent 70%)",
            filter: "blur(80px)",
          }}
        />
      </div>

      {/* Navbar */}
      <nav className="absolute top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-5">
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: "linear-gradient(135deg, #0066ff, #00d4ff)" }}
          >
            <span className="text-white text-sm font-bold">UP</span>
          </div>
          <span
            className="font-heading font-semibold text-base tracking-tight"
            style={{ color: "var(--text-primary)" }}
          >
            UrbanPulse Fusion
          </span>
        </div>
        <div className="hidden md:flex items-center gap-8">
          {["System", "Intelligence", "Architecture", "Demo"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="text-sm transition-colors duration-200 hover:text-cyan-400"
              style={{ color: "var(--text-secondary)" }}
            >
              {item}
            </a>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <span
            className="label-text px-3 py-1 rounded-full"
            style={{
              background: "rgba(0, 212, 255, 0.1)",
              border: "1px solid rgba(0, 212, 255, 0.3)",
              color: "var(--accent-cyan)",
            }}
          >
            BEL · SIH26124
          </span>
        </div>
      </nav>

      <div className="relative z-10 max-w-7xl mx-auto px-6 md:px-12 pt-28 pb-20">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left: Text */}
          <div>
            <div
              className="hero-badge inline-flex items-center gap-2 mb-8 px-4 py-2 rounded-full"
              style={{
                background: "rgba(0, 212, 255, 0.08)",
                border: "1px solid rgba(0, 212, 255, 0.25)",
              }}
            >
              <span
                className="w-2 h-2 rounded-full animate-pulse"
                style={{ background: "var(--accent-cyan)" }}
              />
              <span className="label-text" style={{ color: "var(--accent-cyan)" }}>
                AI-Powered Urban Intelligence Platform
              </span>
            </div>

            <h1
              ref={titleRef}
              className="font-heading text-5xl md:text-6xl xl:text-7xl font-bold mb-6 leading-tight opacity-0"
              style={{ color: "var(--text-primary)" }}
            >
              Cities Don&apos;t Need{" "}
              <span className="gradient-text">More Cameras.</span>
              <br />
              They Need Cameras That{" "}
              <span
                style={{
                  color: "var(--accent-cyan)",
                  textShadow: "0 0 30px rgba(0,212,255,0.4)",
                }}
              >
                Cooperate.
              </span>
            </h1>

            <p
              ref={subtitleRef}
              className="text-lg md:text-xl mb-10 leading-relaxed max-w-xl opacity-0"
              style={{ color: "var(--text-secondary)" }}
            >
              UrbanPulse Fusion transforms public transport vision, roadside cameras
              and existing CCTV into a shared, self-verifying urban intelligence
              network — for BEL&apos;s smart city ecosystem.
            </p>

            {/* Stats */}
            <div className="flex flex-wrap gap-8 mb-10">
              {STATS.map((stat) => (
                <div key={stat.label} className="hero-stat opacity-0">
                  <div
                    className="font-heading text-2xl font-bold gradient-text"
                  >
                    {stat.value}
                  </div>
                  <div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>

            {/* CTAs */}
            <div className="flex flex-wrap gap-4">
              <a
                href="#simulation"
                id="cta-enter-city"
                className="hero-cta opacity-0 group relative inline-flex items-center gap-2 px-7 py-3.5 rounded-xl font-medium text-sm transition-all duration-300 hover:scale-105"
                style={{
                  background: "linear-gradient(135deg, #0066ff, #00d4ff)",
                  color: "white",
                  boxShadow: "0 0 30px rgba(0, 102, 255, 0.4)",
                }}
              >
                <span>Enter the City</span>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path
                    d="M3 8h10M9 4l4 4-4 4"
                    stroke="white"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </a>
              <a
                href="#architecture"
                id="cta-architecture"
                className="hero-cta opacity-0 inline-flex items-center gap-2 px-7 py-3.5 rounded-xl font-medium text-sm transition-all duration-300 hover:scale-105"
                style={{
                  background: "var(--bg-glass)",
                  backdropFilter: "var(--blur-glass)",
                  border: "1px solid var(--border-active)",
                  color: "var(--accent-cyan)",
                }}
              >
                See Architecture
              </a>
            </div>
          </div>

          {/* Right: Source Indicator Cards */}
          <div className="flex flex-col gap-4">
            {/* Central fusion node */}
            <div
              className="relative flex items-center justify-center h-24 rounded-2xl mb-2 overflow-hidden"
              style={{
                background: "rgba(0, 100, 200, 0.08)",
                border: "1px solid rgba(0, 212, 255, 0.2)",
              }}
            >
              <div className="text-center">
                <div
                  className="font-heading text-xl font-semibold gradient-text"
                >
                  URBANPULSE FUSION
                </div>
                <div className="label-text mt-1" style={{ color: "var(--text-muted)" }}>
                  One Urban Intelligence Layer Across Every Camera
                </div>
              </div>
              {/* Animated corner accents */}
              {["tl", "tr", "bl", "br"].map((pos) => (
                <div
                  key={pos}
                  className="absolute w-4 h-4"
                  style={{
                    top: pos.startsWith("t") ? "8px" : "auto",
                    bottom: pos.startsWith("b") ? "8px" : "auto",
                    left: pos.endsWith("l") ? "8px" : "auto",
                    right: pos.endsWith("r") ? "8px" : "auto",
                    borderTop: pos.startsWith("t") ? "2px solid var(--accent-cyan)" : "none",
                    borderBottom: pos.startsWith("b") ? "2px solid var(--accent-cyan)" : "none",
                    borderLeft: pos.endsWith("l") ? "2px solid var(--accent-cyan)" : "none",
                    borderRight: pos.endsWith("r") ? "2px solid var(--accent-cyan)" : "none",
                  }}
                />
              ))}
            </div>

            {/* Source cards */}
            {SOURCE_INDICATORS.map((src, i) => (
              <div
                key={src.id}
                id={`source-card-${src.id}`}
                className="source-card opacity-0 group flex items-center gap-5 p-5 rounded-xl cursor-default transition-all duration-300 hover:scale-[1.02]"
                style={{
                  background: `rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.06)`,
                  border: `1px solid rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.2)`,
                }}
              >
                <div
                  className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
                  style={{
                    background: `rgba(${src.color === "#00d4ff" ? "0,212,255" : src.color === "#4488ff" ? "68,136,255" : "136,85,255"}, 0.1)`,
                  }}
                >
                  {src.icon}
                </div>
                <div className="flex-1">
                  <div
                    className="font-heading font-semibold text-sm"
                    style={{ color: src.color }}
                  >
                    {src.label}
                  </div>
                  <div
                    className="text-xs mt-0.5"
                    style={{ color: "var(--text-secondary)" }}
                  >
                    {src.sublabel}
                  </div>
                </div>
                <div className="text-right">
                  <div
                    className="font-mono font-semibold text-lg"
                    style={{ color: src.color }}
                  >
                    {src.count}
                  </div>
                  <div className="label-text" style={{ color: "var(--text-muted)" }}>
                    {src.unit}
                  </div>
                </div>
                <div
                  className="w-2 h-2 rounded-full animate-pulse flex-shrink-0"
                  style={{ background: src.color }}
                />
              </div>
            ))}

            {/* Tagline */}
            <div className="text-center mt-2">
              <p
                className="label-text"
                style={{ color: "var(--text-muted)" }}
              >
                &quot;Others analyze cameras. UrbanPulse Fusion makes cameras cooperate.&quot;
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 opacity-50">
        <span className="label-text" style={{ color: "var(--text-muted)" }}>
          Scroll to explore
        </span>
        <div
          className="w-px h-12 animate-pulse"
          style={{ background: "linear-gradient(to bottom, var(--accent-cyan), transparent)" }}
        />
      </div>
    </section>
  );
}
