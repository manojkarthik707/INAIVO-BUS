"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

const ROADS = [
  { name: "Anna Salai (Arterial)", conf: 97, color: "var(--accent-green)", time: "10 mins ago" },
  { name: "OMR IT Expressway", conf: 82, color: "var(--accent-cyan)", time: "1 hour ago" },
  { name: "Mount Poonamallee Rd", conf: 45, color: "var(--accent-amber)", time: "8 hours ago" },
  { name: "Suburban Route 42", conf: 19, color: "var(--accent-red)", time: "2 days ago" },
];

export default function CityCoverageSection() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".coverage-bar",
        { scaleX: 0 },
        {
          scaleX: 1,
          duration: 1.2,
          stagger: 0.2,
          ease: "power3.out",
          scrollTrigger: {
            trigger: ".coverage-chart",
            start: "top 80%",
          },
        }
      );
      
      gsap.fromTo(
        ".coverage-text",
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.1,
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
    <Section ref={containerRef as any} id="coverage" style={{ background: "var(--bg-base)" }}>
      <PageContainer>
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          
          <div className="flex flex-col">
            <div className="coverage-text inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full self-start" style={{ background: "rgba(0, 255, 136, 0.08)", border: "1px solid rgba(0, 255, 136, 0.25)" }}>
              <span className="label-text" style={{ color: "var(--accent-green)" }}>CITY KNOWLEDGE COVERAGE</span>
            </div>
            
            <h2 className="coverage-text text-title font-heading font-extrabold mb-6 text-text-primary tracking-tight">
              Knowing What <br />
              <span className="gradient-text">We Don&apos;t Know.</span>
            </h2>
            
            <p className="coverage-text text-body mb-6 text-text-secondary">
              A unique capability of UrbanPulse Fusion is quantifying observation staleness. The platform doesn&apos;t just show what the city knows—it shows <strong className="font-semibold text-text-primary">where the city&apos;s information is outdated or uncertain</strong>.
            </p>
            
            <p className="coverage-text text-sm mb-8 text-text-muted leading-relaxed">
              Confidence scores decay over time and increase with repeated multi-bus passes, guiding municipal inspection vehicles only to areas the bus fleet hasn&apos;t recently covered.
            </p>
          </div>

          <div className="coverage-text coverage-chart glass-card p-8 md:p-10 rounded-3xl relative h-full flex flex-col justify-center border-l-4" style={{ borderLeftColor: "var(--accent-green)" }}>
            <div className="absolute top-0 right-0 p-8 opacity-[0.03] font-heading text-8xl font-black pointer-events-none">
              97%
            </div>
            
            <div className="mb-8 pb-4 border-b border-white/5 flex justify-between items-center relative z-10">
              <span className="text-sm font-mono font-bold tracking-widest text-text-secondary">SENSING CONFIDENCE</span>
              <span className="text-[10px] font-bold tracking-widest uppercase text-accent-cyan opacity-80">LIVE FLEET DATA</span>
            </div>
            
            <div className="space-y-8 relative z-10">
              {ROADS.map((road, idx) => (
                <div key={idx} className="group">
                  <div className="flex justify-between items-end mb-3">
                    <span className="font-semibold text-text-primary group-hover:text-white transition-colors text-[15px]">{road.name}</span>
                    <span className="font-mono text-lg font-bold" style={{ color: road.color }}>{road.conf}%</span>
                  </div>
                  <div className="h-2.5 bg-white/5 rounded-full overflow-hidden w-full relative mb-1.5">
                    <div 
                      className="coverage-bar h-full rounded-full origin-left" 
                      style={{ width: `${road.conf}%`, backgroundColor: road.color, boxShadow: `0 0 15px ${road.color}88` }} 
                    />
                  </div>
                  <div className="text-[10px] text-right font-mono font-bold uppercase tracking-widest text-text-muted">
                    LAST SEEN: {road.time}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </PageContainer>
    </Section>
  );
}
