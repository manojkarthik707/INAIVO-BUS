"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

const SOURCE_NODES = [
  { label: "MOVING CAMERAS", color: "#00d4ff", x: "-40%", icon: "🚌" },
  { label: "FIXED CAMERAS", color: "#4488ff", x: "0%", icon: "📡" },
  { label: "EXISTING CCTV", color: "#8855ff", x: "40%", icon: "🎥" },
];

export default function FinalCTASection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: sectionRef.current,
          start: "top 70%",
        },
      });

      tl.fromTo(
        ".cta-node",
        { opacity: 0, scale: 0.5, y: 30 },
        { opacity: 1, scale: 1, y: 0, duration: 0.6, stagger: 0.15, ease: "back.out(1.7)" }
      )
        .fromTo(
          ".cta-line",
          { opacity: 0, scaleY: 0 },
          { opacity: 1, scaleY: 1, duration: 0.4, stagger: 0.1, ease: "power2.out" },
          "-=0.2"
        )
        .fromTo(
          ".cta-fusion-node",
          { opacity: 0, scale: 0.3 },
          { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.4)" },
          "-=0.1"
        )
        .fromTo(
          ".cta-headline",
          { opacity: 0, y: 30 },
          { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" },
          "-=0.3"
        )
        .fromTo(
          ".cta-sub",
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.5, ease: "power2.out" },
          "-=0.3"
        )
        .fromTo(
          ".cta-btn",
          { opacity: 0, scale: 0.9 },
          { opacity: 1, scale: 1, duration: 0.4, stagger: 0.1, ease: "back.out(1.4)" },
          "-=0.2"
        );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      id="demo"
      className="relative py-40 overflow-hidden grid-bg"
      style={{ background: "var(--bg-base)" }}
    >
      {/* Atmospheric blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[800px] h-[800px] rounded-full opacity-10"
          style={{ background: "radial-gradient(circle, #0066ff, transparent 65%)", filter: "blur(80px)" }}
        />
        <div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] rounded-full opacity-15"
          style={{ background: "radial-gradient(ellipse, #00d4ff, transparent 70%)", filter: "blur(60px)" }}
        />
      </div>

      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-cyan), transparent)" }}
      />

      <div className="relative z-10 max-w-5xl mx-auto px-6 md:px-12 text-center">
        {/* Three source nodes converging */}
        <div className="flex justify-center items-end gap-12 md:gap-20 mb-2">
          {SOURCE_NODES.map((node) => (
            <div key={node.label} className="cta-node opacity-0 flex flex-col items-center gap-3">
              <div
                className="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl"
                style={{
                  background: `rgba(${node.color.replace("#", "").match(/.{2}/g)?.map(h=>parseInt(h,16)).join(",")}, 0.15)`,
                  border: `1px solid ${node.color}`,
                  boxShadow: `0 0 20px ${node.color}44`,
                }}
              >
                {node.icon}
              </div>
              <span className="label-text" style={{ color: node.color }}>
                {node.label}
              </span>
            </div>
          ))}
        </div>

        {/* Converging lines */}
        <div className="flex justify-center mb-0 h-8 relative">
          <svg width="400" height="32" viewBox="0 0 400 32" className="overflow-visible">
            <path
              className="cta-line opacity-0"
              d="M60 0 L200 32"
              stroke="url(#lineGrad1)"
              strokeWidth="1.5"
              fill="none"
              strokeDasharray="none"
            />
            <path
              className="cta-line opacity-0"
              d="M200 0 L200 32"
              stroke="#4488ff"
              strokeWidth="1.5"
              fill="none"
            />
            <path
              className="cta-line opacity-0"
              d="M340 0 L200 32"
              stroke="url(#lineGrad2)"
              strokeWidth="1.5"
              fill="none"
            />
            <defs>
              <linearGradient id="lineGrad1" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#00d4ff" />
                <stop offset="100%" stopColor="#4488ff" />
              </linearGradient>
              <linearGradient id="lineGrad2" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#4488ff" />
                <stop offset="100%" stopColor="#8855ff" />
              </linearGradient>
            </defs>
          </svg>
        </div>

        {/* Central fusion node */}
        <div className="flex justify-center mb-12">
          <div
            className="cta-fusion-node opacity-0 px-8 py-4 rounded-2xl"
            style={{
              background: "rgba(0,100,200,0.12)",
              border: "1px solid var(--accent-cyan)",
              boxShadow: "0 0 60px rgba(0,212,255,0.2), inset 0 0 30px rgba(0,100,200,0.1)",
            }}
          >
            <div className="font-heading text-xl font-bold gradient-text">
              URBANPULSE FUSION
            </div>
          </div>
        </div>

        {/* Main headline */}
        <h2
          className="cta-headline opacity-0 font-heading text-4xl md:text-6xl xl:text-7xl font-bold mb-6 leading-tight"
          style={{ color: "var(--text-primary)" }}
        >
          One Urban Intelligence Layer{" "}
          <span
            className="gradient-text"
            style={{ display: "block" }}
          >
            Across Every Camera.
          </span>
        </h2>

        <p
          className="cta-sub opacity-0 text-xl md:text-2xl font-heading font-medium mb-4"
          style={{ color: "var(--text-secondary)" }}
        >
          Discover. Corroborate. Understand. Act.{" "}
          <span style={{ color: "var(--accent-green)" }}>Verify.</span>
        </p>

        <p
          className="cta-sub opacity-0 text-base max-w-2xl mx-auto mb-12"
          style={{ color: "var(--text-muted)" }}
        >
          From isolated video feeds to a shared, self-verifying urban intelligence network.
          Built for BEL&apos;s Smart City Ecosystem. SIH Problem Statement 26124.
        </p>

        {/* CTA buttons */}
        <div className="flex flex-wrap justify-center gap-4">
          <a
            id="final-cta-explore"
            href="#simulation"
            className="cta-btn opacity-0 inline-flex items-center gap-2 px-8 py-4 rounded-xl font-heading font-semibold text-base transition-all duration-300 hover:scale-105"
            style={{
              background: "linear-gradient(135deg, #0066ff, #00d4ff)",
              color: "white",
              boxShadow: "0 0 40px rgba(0,102,255,0.4)",
            }}
          >
            Explore the Intelligence
          </a>
          <a
            id="final-cta-architecture"
            href="#architecture"
            className="cta-btn opacity-0 inline-flex items-center gap-2 px-8 py-4 rounded-xl font-heading font-semibold text-base transition-all duration-300 hover:scale-105"
            style={{
              background: "var(--bg-glass)",
              backdropFilter: "var(--blur-glass)",
              border: "1px solid var(--border-active)",
              color: "var(--accent-cyan)",
            }}
          >
            View System Architecture
          </a>
        </div>

        {/* Footer */}
        <div className="mt-24 pt-8 pb-12" style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}>
          <div className="flex flex-wrap justify-center gap-8 text-xs" style={{ color: "var(--text-muted)" }}>
            <span>SIH Problem Statement: 26124</span>
            <span>Organization: Bharat Electronics Limited (BEL)</span>
            <span>Category: Smart City Infrastructure</span>
            <span>
              &quot;Others analyze cameras. UrbanPulse Fusion makes cameras cooperate.&quot;
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
