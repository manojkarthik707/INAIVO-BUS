"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

const EVENTS = [
  { id: 1, type: "Camera Detection", conf: 78, by: "BUS-14", time: "Monday" },
  { id: 2, type: "IMU Verification", conf: 92, by: "BUS-31", time: "Tuesday" },
  { id: 3, type: "Camera Detection", conf: 85, by: "BUS-07", time: "Wednesday" },
];

export default function RoadDNASection() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".dna-text",
        { opacity: 0, x: -30 },
        {
          opacity: 1,
          x: 0,
          duration: 0.8,
          stagger: 0.15,
          ease: "power2.out",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top 75%",
          },
        }
      );

      gsap.fromTo(
        ".dna-card",
        { opacity: 0, y: 30, scale: 0.95 },
        {
          opacity: 1,
          y: 0,
          scale: 1,
          duration: 0.6,
          stagger: 0.15,
          ease: "back.out(1.2)",
          scrollTrigger: {
            trigger: ".dna-visualization",
            start: "top 80%",
          },
        }
      );

      // Connecting lines animation
      gsap.fromTo(
        ".dna-line",
        { strokeDashoffset: 100 },
        {
          strokeDashoffset: 0,
          duration: 1.5,
          stagger: 0.2,
          ease: "power1.inOut",
          scrollTrigger: {
            trigger: ".dna-visualization",
            start: "top 80%",
          },
        }
      );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <Section ref={containerRef as any} id="roaddna" style={{ background: "var(--bg-surface)" }}>
      <div className="absolute top-0 left-0 right-0 h-[1px]" style={{ background: "linear-gradient(90deg, transparent, var(--accent-amber), transparent)" }} />

      <PageContainer>
        <div className="grid lg:grid-cols-[40%_60%] gap-12 lg:gap-20 items-center">
          
          {/* Left Text - 40% */}
          <div className="flex flex-col">
            <div className="dna-text inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full self-start" style={{ background: "rgba(255, 170, 0, 0.08)", border: "1px solid rgba(255, 170, 0, 0.25)" }}>
              <span className="label-text" style={{ color: "var(--accent-amber)" }}>PERSISTENT URBAN MEMORY</span>
            </div>
            
            <h2 className="dna-text text-title font-heading font-extrabold mb-6 text-text-primary tracking-tight">
              RoadDNA: <br />
              Infrastructure <br />
              <span className="gradient-text-gold">With a Memory.</span>
            </h2>
            
            <p className="dna-text text-body mb-8 text-text-secondary">
              GPS alone isn&apos;t enough. Urban environments introduce noise.
              Instead of creating 5 different pothole records when 5 buses pass by, UrbanPulse uses visual fingerprinting and geometric matching to assign a <strong className="text-text-primary font-semibold">persistent digital identity</strong> to physical defects.
            </p>

            <ul className="dna-text space-y-4 mb-8">
              {[
                "Tracks severity over time",
                "Verifies repairs automatically",
                "Fuses Vision, IMU & GPS",
              ].map((item, i) => (
                <li key={i} className="flex items-center gap-4 text-[15px] font-medium text-text-primary">
                  <div className="w-5 h-5 rounded-full flex items-center justify-center bg-amber-500/20 border border-amber-500/50 flex-shrink-0">
                    <div className="w-2 h-2 rounded-full bg-amber-400"></div>
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Right Visualization - 60% */}
          <div className="dna-visualization relative w-full h-full min-h-[400px] flex items-center justify-center">
            
            <div className="grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(0,1.2fr)] gap-8 md:gap-16 items-center w-full relative z-10">
              
              {/* Isolated Events */}
              <div className="flex flex-col gap-4">
                <div className="text-xs font-mono font-bold mb-2 tracking-widest text-text-muted">ISOLATED OBSERVATIONS</div>
                {EVENTS.map((ev, i) => (
                  <div key={i} className="dna-card glass-card p-4 md:p-5 flex justify-between items-center relative z-20 hover:scale-[1.02] transition-transform">
                    <div className="flex flex-col gap-1">
                      <div className="text-xs font-mono font-bold tracking-wider text-text-secondary">{ev.by} • {ev.time}</div>
                      <div className="font-semibold text-[15px]" style={{ color: "var(--accent-amber)" }}>{ev.type}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-text-primary">{ev.conf}%</div>
                      <div className="text-[10px] font-bold uppercase tracking-widest text-text-muted">Conf</div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Central Persistent Object */}
              <div className="relative z-20 flex justify-center h-full items-center">
                <div 
                  className="dna-card p-6 md:p-8 rounded-3xl w-full max-w-[400px] glass-card" 
                  style={{ 
                    borderColor: "var(--accent-amber)", 
                    boxShadow: "0 0 50px rgba(255, 170, 0, 0.15)",
                    background: "rgba(255,170,0,0.05)"
                  }}
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-transparent pointer-events-none rounded-3xl" />
                  
                  <div className="relative z-10">
                    <div className="flex flex-wrap justify-between items-start mb-6 gap-3">
                      <div>
                        <div className="label-text mb-1" style={{ color: "var(--accent-amber)" }}>PERSISTENT ROAD OBJECT</div>
                        <div className="font-heading text-3xl font-extrabold tracking-tight text-text-primary">PTH-00124</div>
                      </div>
                      <div className="px-3 py-1.5 rounded-full bg-amber-500/20 text-amber-400 text-[10px] font-bold tracking-widest border border-amber-500/30 uppercase">
                        ACTIVE
                      </div>
                    </div>
                    
                    <div className="space-y-4 pt-6 border-t border-amber-500/20">
                      <div className="flex justify-between items-center text-[15px]">
                        <span className="text-text-secondary">Type:</span>
                        <span className="font-semibold text-text-primary">Pothole (Severe)</span>
                      </div>
                      <div className="flex justify-between items-center text-[15px]">
                        <span className="text-text-secondary">Observations:</span>
                        <span className="font-semibold text-text-primary">47 total (18 buses)</span>
                      </div>
                      <div className="flex justify-between items-center text-[15px]">
                        <span className="text-text-secondary">Confidence:</span>
                        <span className="font-bold text-amber-400">97% (Multi-Sensor)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* SVG Connecting lines for Desktop */}
            <svg 
              className="absolute inset-0 w-full h-full pointer-events-none z-0 hidden md:block" 
              style={{ overflow: "visible" }}
            >
               {/* Drawing smooth bezier curves from left cards to the right card */}
               <path className="dna-line" d="M 45% 20% C 55% 20%, 55% 45%, 60% 45%" fill="none" stroke="var(--accent-amber)" strokeWidth="2" strokeDasharray="6 6" strokeDashoffset="100" opacity="0.4" />
               <path className="dna-line" d="M 45% 50% C 55% 50%, 55% 50%, 60% 50%" fill="none" stroke="var(--accent-amber)" strokeWidth="2" strokeDasharray="6 6" strokeDashoffset="100" opacity="0.6" />
               <path className="dna-line" d="M 45% 80% C 55% 80%, 55% 55%, 60% 55%" fill="none" stroke="var(--accent-amber)" strokeWidth="2" strokeDasharray="6 6" strokeDashoffset="100" opacity="0.4" />
            </svg>
          </div>

        </div>
      </PageContainer>
    </Section>
  );
}
