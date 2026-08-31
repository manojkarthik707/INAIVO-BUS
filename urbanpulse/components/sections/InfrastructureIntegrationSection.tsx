"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

export default function InfrastructureIntegrationSection() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".infra-item",
        { opacity: 0, x: -20 },
        {
          opacity: 1,
          x: 0,
          duration: 0.6,
          stagger: 0.1,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ".infra-list",
            start: "top 80%",
          },
        }
      );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <Section ref={containerRef as any} id="infrastructure" style={{ background: "var(--bg-base)" }}>
      <div className="absolute top-0 left-0 right-0 h-[1px]" style={{ background: "linear-gradient(90deg, transparent, var(--accent-purple), transparent)" }} />
      
      <PageContainer>
        <div className="grid lg:grid-cols-[50%_50%] gap-12 lg:gap-20 items-center">
          
          {/* Left Visualization - 50% */}
          <div className="order-2 lg:order-1 relative w-full h-[450px] rounded-3xl overflow-hidden glass-card" style={{ borderColor: "rgba(136, 85, 255, 0.2)" }}>
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-cyan-500/5 pointer-events-none" />
            
            <div className="absolute inset-0 flex flex-col items-center justify-center p-8 z-10">
              <div className="grid grid-cols-2 gap-8 mb-8 w-full max-w-sm">
                <div className="w-full aspect-square rounded-2xl glass-card flex flex-col items-center justify-center gap-3 relative overflow-hidden group hover:scale-[1.02] transition-transform" style={{ background: "rgba(0,0,0,0.3)", borderColor: "rgba(136, 85, 255, 0.3)" }}>
                   <div className="absolute inset-0 bg-purple-500/10 group-hover:bg-purple-500/20 transition-colors" />
                   <div className="text-4xl">📸</div>
                   <div className="text-xs font-mono font-bold tracking-widest text-purple-300">Legacy CCTV</div>
                </div>
                <div className="w-full aspect-square rounded-2xl glass-card flex flex-col items-center justify-center gap-3 relative overflow-hidden group hover:scale-[1.02] transition-transform" style={{ background: "rgba(0,0,0,0.3)", borderColor: "rgba(136, 85, 255, 0.3)" }}>
                   <div className="absolute inset-0 bg-purple-500/10 group-hover:bg-purple-500/20 transition-colors" />
                   <div className="text-4xl">🚌</div>
                   <div className="text-xs font-mono font-bold tracking-widest text-purple-300">Bus MDVR</div>
                </div>
              </div>
              
              <div className="w-[2px] h-12 bg-gradient-to-b from-purple-500 to-cyan-500" />
              
              <div className="w-full max-w-sm h-20 rounded-2xl glass-card flex items-center justify-center relative shadow-[0_0_30px_rgba(0,212,255,0.15)]" style={{ background: "rgba(0,212,255,0.05)", borderColor: "rgba(0,212,255,0.4)" }}>
                 <div className="font-heading font-extrabold text-lg text-accent-cyan tracking-wide">UrbanPulse Edge AI</div>
                 <div className="absolute -right-3 -top-3 w-8 h-8 rounded-full bg-cyan-500/20 border border-cyan-400 flex items-center justify-center animate-pulse shadow-[0_0_15px_rgba(0,212,255,0.5)]">
                   <div className="w-3 h-3 bg-cyan-400 rounded-full" />
                 </div>
              </div>
            </div>
          </div>

          {/* Right Text - 50% */}
          <div className="order-1 lg:order-2 flex flex-col">
            <div className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full self-start" style={{ background: "rgba(136, 85, 255, 0.08)", border: "1px solid rgba(136, 85, 255, 0.25)" }}>
              <span className="label-text" style={{ color: "var(--accent-purple)" }}>EXISTING INFRASTRUCTURE</span>
            </div>
            
            <h2 className="text-title font-heading font-extrabold mb-6 text-text-primary tracking-tight">
              We Don&apos;t Rebuild.<br />
              <span className="gradient-text">We Augment.</span>
            </h2>
            
            <p className="text-body mb-10 text-text-secondary max-w-xl">
              Deploying a completely new city-wide sensor network is capital-intensive and slow. 
              UrbanPulse Fusion is an intelligence layer designed to make better use of infrastructure that <strong className="text-text-primary font-semibold">already exists</strong>.
            </p>
            
            <div className="infra-list space-y-4 w-full">
              {[
                "RTSP / ONVIF IP Camera Feeds",
                "Existing Bus MDVR / GPS units",
                "Junction ANPR Cameras",
                "Traffic Command Centre APIs"
              ].map((item, idx) => (
                <div key={idx} className="infra-item flex items-center gap-5 glass-card p-4 rounded-xl transition-transform hover:scale-[1.01]" style={{ borderColor: "rgba(136, 85, 255, 0.2)" }}>
                  <div className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0" style={{ background: "rgba(136, 85, 255, 0.1)", color: "var(--accent-purple)" }}>
                    <svg width="18" height="18" viewBox="0 0 14 14" fill="none">
                      <path d="M11.6667 3.5L5.25 9.91667L2.33333 7" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                  <span className="text-[15px] font-semibold text-text-primary">{item}</span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </PageContainer>
    </Section>
  );
}
