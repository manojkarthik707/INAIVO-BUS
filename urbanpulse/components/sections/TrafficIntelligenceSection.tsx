"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

export default function TrafficIntelligenceSection() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".traffic-card",
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top 75%",
          },
        }
      );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <Section ref={containerRef as any} id="traffic" style={{ background: "var(--bg-base)" }} className="relative">
      <div className="absolute inset-0 grid-bg opacity-30 pointer-events-none" />
      
      {/* Decorative gradient orb */}
      <div 
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full pointer-events-none opacity-[0.05]" 
        style={{ background: "radial-gradient(circle, var(--accent-cyan), transparent 60%)" }} 
      />

      <PageContainer className="relative z-10">
        
        <SectionHeader
          eyebrow="Traffic Intelligence"
          title={
            <>
              The Fleet Becomes a <br />
              <span className="gradient-text">City-Scale Sensor.</span>
            </>
          }
          description="Bus cameras aren't just for defects. By continuously analyzing the road ahead, the fleet acts as a massive moving probe, mapping traffic density, vehicle counts, and bottlenecks in real time."
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 mt-16">
          {[
            {
              title: "Congestion Heatmaps",
              desc: "Fleet-wide observations construct real-time corridor performance maps without installing thousands of new fixed sensors.",
              icon: "🗺️",
              color: "var(--accent-cyan)",
              r: 0, g: 212, b: 255
            },
            {
              title: "Vehicle Classification",
              desc: "Edge AI categorizes traffic mix (two-wheelers, cars, heavy vehicles) to understand lane occupancy and flow dynamics.",
              icon: "🚗",
              color: "var(--accent-blue)",
              r: 68, g: 136, b: 255
            },
            {
              title: "Queue Analytics",
              desc: "Measure intersection queue lengths and recurring bottleneck patterns from the perspective of the moving fleet.",
              icon: "🚥",
              color: "var(--accent-electric)",
              r: 136, g: 85, b: 255
            }
          ].map((item, idx) => (
            <div 
              key={idx} 
              className="traffic-card glass-card p-8 rounded-3xl transition-transform duration-300 hover:-translate-y-2 h-full flex flex-col"
              style={{
                borderColor: `rgba(${item.r}, ${item.g}, ${item.b}, 0.2)`,
                background: `rgba(${item.r}, ${item.g}, ${item.b}, 0.03)`
              }}
            >
              <div 
                className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-8 flex-shrink-0 relative overflow-hidden" 
              >
                <div className="absolute inset-0 opacity-20" style={{ background: item.color }} />
                <div className="absolute inset-0" style={{ border: `1px solid ${item.color}`, opacity: 0.4, borderRadius: "1rem" }} />
                <span className="relative z-10">{item.icon}</span>
              </div>
              <h3 className="font-heading text-xl font-bold mb-4 text-text-primary tracking-tight">
                {item.title}
              </h3>
              <p className="text-[15px] leading-relaxed text-text-secondary mt-auto">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </PageContainer>
    </Section>
  );
}
