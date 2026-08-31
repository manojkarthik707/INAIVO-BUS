"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

const SOURCE_NODES = [
  { label: "MOVING CAMERAS", color: "#00d4ff", icon: "🚌", r: 0, g: 212, b: 255 },
  { label: "FIXED CAMERAS", color: "#4488ff", icon: "📡", r: 68, g: 136, b: 255 },
  { label: "EXISTING CCTV", color: "#8855ff", icon: "🎥", r: 136, g: 85, b: 255 },
];

export default function FinalCTASection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
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
    <Section
      ref={sectionRef as any}
      id="demo"
      className="relative overflow-hidden grid-bg min-h-screen flex items-center justify-center"
      style={{ background: "var(--bg-base)" }}
    >
      {/* Atmospheric blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[800px] h-[800px] rounded-full opacity-[0.08]"
          style={{ background: "radial-gradient(circle, #0066ff, transparent 65%)", filter: "blur(80px)" }}
        />
        <div
          className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] rounded-full opacity-[0.12]"
          style={{ background: "radial-gradient(ellipse, #00d4ff, transparent 70%)", filter: "blur(60px)" }}
        />
      </div>

      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, var(--accent-cyan), transparent)" }}
      />

      <PageContainer className="relative z-10 w-full">
        <div className="text-center flex flex-col items-center max-w-4xl mx-auto">
          
          {/* Three source nodes converging */}
          <div className="flex justify-center items-end gap-10 md:gap-24 mb-4">
            {SOURCE_NODES.map((node) => (
              <div key={node.label} className="cta-node opacity-0 flex flex-col items-center gap-4">
                <div
                  className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl transition-transform hover:scale-110"
                  style={{
                    background: `rgba(${node.r},${node.g},${node.b}, 0.15)`,
                    borderColor: `rgba(${node.r},${node.g},${node.b}, 0.5)`,
                    borderWidth: "1px",
                    borderStyle: "solid",
                    boxShadow: `0 0 25px rgba(${node.r},${node.g},${node.b},0.3)`,
                  }}
                >
                  {node.icon}
                </div>
                <span className="font-mono text-[11px] font-bold tracking-widest uppercase" style={{ color: node.color }}>
                  {node.label}
                </span>
              </div>
            ))}
          </div>

          {/* Converging lines (SVG) */}
          <div className="flex justify-center h-12 relative w-full mb-2">
            <svg width="100%" height="48" viewBox="0 0 400 48" preserveAspectRatio="none" className="overflow-visible">
              {/* Left Line */}
              <path
                className="cta-line opacity-0"
                d="M100 0 C150 24, 180 36, 200 48"
                stroke="url(#lineGrad1)"
                strokeWidth="2"
                fill="none"
              />
              {/* Center Line */}
              <path
                className="cta-line opacity-0"
                d="M200 0 L200 48"
                stroke="#4488ff"
                strokeWidth="2"
                fill="none"
              />
              {/* Right Line */}
              <path
                className="cta-line opacity-0"
                d="M300 0 C250 24, 220 36, 200 48"
                stroke="url(#lineGrad2)"
                strokeWidth="2"
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
          <div className="flex justify-center mb-16">
            <div
              className="cta-fusion-node opacity-0 px-10 py-5 rounded-2xl relative overflow-hidden"
              style={{
                background: "rgba(0,100,200,0.12)",
                border: "1px solid var(--accent-cyan)",
                boxShadow: "0 0 60px rgba(0,212,255,0.2), inset 0 0 30px rgba(0,100,200,0.1)",
              }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/0 via-cyan-500/20 to-cyan-500/0 animate-shimmer" />
              <div className="font-heading text-2xl font-extrabold gradient-text tracking-widest uppercase relative z-10">
                UrbanPulse Fusion
              </div>
            </div>
          </div>

          {/* Main headline */}
          <h2 className="cta-headline opacity-0 text-title font-heading font-extrabold mb-8 leading-tight tracking-tight text-text-primary">
            One Urban Intelligence Layer{" "}
            <span className="gradient-text block">
              Across Every Camera.
            </span>
          </h2>

          <p className="cta-sub opacity-0 text-xl md:text-3xl font-heading font-medium mb-6 text-text-secondary">
            Discover. Corroborate. Understand. Act.{" "}
            <span style={{ color: "var(--accent-green)" }}>Verify.</span>
          </p>

          <p className="cta-sub opacity-0 text-body mb-16 text-text-muted max-w-2xl">
            From isolated video feeds to a shared, self-verifying urban intelligence network.
            Built for BEL&apos;s Smart City Ecosystem. SIH Problem Statement 26124.
          </p>

          {/* CTA buttons */}
          <div className="flex flex-col sm:flex-row justify-center items-center gap-5 w-full sm:w-auto">
            <a
              id="final-cta-explore"
              href="#architecture"
              className="cta-btn opacity-0 inline-flex items-center justify-center gap-2 px-10 py-5 rounded-xl font-heading font-bold text-lg transition-transform hover:-translate-y-1 w-full sm:w-auto"
              style={{
                background: "linear-gradient(135deg, #0066ff, #00d4ff)",
                color: "white",
                boxShadow: "0 10px 40px rgba(0,102,255,0.4)",
              }}
            >
              Explore the Architecture
            </a>
            <a
              id="final-cta-demo"
              href="#demo"
              className="cta-btn opacity-0 inline-flex items-center justify-center gap-2 px-10 py-5 rounded-xl font-heading font-bold text-lg transition-all hover:bg-white/5 w-full sm:w-auto glass-card"
              style={{
                color: "var(--text-primary)",
              }}
            >
              Watch Video Demo
            </a>
          </div>

          {/* Footer Metadata */}
          <div className="mt-32 pt-10 border-t border-white/10 w-full flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex flex-col md:flex-row gap-4 text-xs font-medium text-text-muted text-center md:text-left">
              <span><strong className="text-text-secondary">SIH:</strong> 26124</span>
              <span className="hidden md:block opacity-30">|</span>
              <span><strong className="text-text-secondary">Org:</strong> Bharat Electronics Limited</span>
              <span className="hidden md:block opacity-30">|</span>
              <span><strong className="text-text-secondary">Category:</strong> Smart City</span>
            </div>
            <div className="text-xs font-mono font-bold tracking-widest text-accent-cyan opacity-70 uppercase text-center md:text-right">
              &quot;Cameras that Cooperate&quot;
            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
