"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const STACK = [
  {
    category: "Edge AI & Vision",
    items: ["Python", "PyTorch", "ONNX Runtime", "OpenCV", "RT-DETR"],
    color: "var(--accent-cyan)",
    r: 0, g: 212, b: 255
  },
  {
    category: "Perception & Fusion",
    items: ["DINOv2 (Fingerprinting)", "LightGlue", "ByteTrack", "PaddleOCR"],
    color: "var(--accent-blue)",
    r: 68, g: 136, b: 255
  },
  {
    category: "Offline Mesh & Comms",
    items: ["WiFi-Aware", "BLE", "DTN / Bundle Protocol", "MQTT (Cloud)"],
    color: "var(--accent-amber)",
    r: 255, g: 170, b: 0
  },
  {
    category: "City Platform & GIS",
    items: ["FastAPI", "PostgreSQL + PostGIS", "H3 Hexagons", "Next.js", "MapLibre GL JS"],
    color: "var(--accent-purple)",
    r: 136, g: 85, b: 255
  }
];

export default function TechStackSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".stack-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".stack-card",
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ".stack-grid",
            start: "top 80%",
          },
        }
      );
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <Section ref={sectionRef as any} id="stack" style={{ background: "var(--bg-base)" }}>
      <div className="absolute top-0 left-0 right-0 h-[1px]" style={{ background: "linear-gradient(90deg, transparent, rgba(68,136,255,0.3), transparent)" }} />

      <PageContainer>
        <div className="stack-header">
          <SectionHeader
            eyebrow="Proposed Architecture"
            title={
              <>
                Engineering the <span className="gradient-text">Intelligence Layer.</span>
              </>
            }
          />
        </div>

        <div className="stack-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {STACK.map((group, i) => (
            <div 
              key={i} 
              className="stack-card glass-card p-6 md:p-8 rounded-3xl transition-transform duration-300 hover:-translate-y-2 flex flex-col h-full"
              style={{
                background: `rgba(${group.r}, ${group.g}, ${group.b}, 0.03)`,
                borderColor: `rgba(${group.r}, ${group.g}, ${group.b}, 0.15)`
              }}
            >
              <h3 className="font-heading font-bold text-[15px] mb-6 tracking-wide uppercase" style={{ color: group.color }}>
                {group.category}
              </h3>
              <div className="space-y-4 flex-1">
                {group.items.map((tech, j) => (
                  <div key={j} className="text-[14px] font-mono flex items-center gap-3 text-text-secondary">
                    <div className="w-1.5 h-1.5 rounded-full shadow-[0_0_8px_currentColor]" style={{ backgroundColor: group.color, opacity: 0.8 }} />
                    {tech}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-16 text-center max-w-2xl mx-auto opacity-0 stack-card">
          <p className="text-xs font-mono text-text-muted leading-relaxed">
            * This is a proposed SIH prototype architecture. It is designed to be hardware-agnostic, capable of running on NVIDIA Jetson Orin-class edge nodes or equivalent industrial edge computers.
          </p>
        </div>
      </PageContainer>
    </Section>
  );
}
