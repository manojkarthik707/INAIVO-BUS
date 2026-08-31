"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

export default function OfflineMeshSection() {
  const containerRef = useRef<HTMLElement>(null);

  useEffect(() => {
    gsap.registerPlugin(ScrollTrigger);
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".mesh-text",
        { opacity: 0, y: 30 },
        {
          opacity: 1,
          y: 0,
          duration: 0.8,
          stagger: 0.2,
          ease: "power2.out",
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top 75%",
          },
        }
      );

      const tl = gsap.timeline({ repeat: -1 });

      tl.to("#bus-a", { x: 150, duration: 2, ease: "none" })
        .to(".packet", { x: 50, opacity: 1, duration: 0.5, ease: "power1.inOut" })
        .to(".packet", { opacity: 0, duration: 0.1 })
        .set(".packet", { x: 0 })
        .to("#bus-b", { x: 150, duration: 2, ease: "none" }, "+=0.5")
        .to(".packet-to-relay", { y: -50, opacity: 1, duration: 0.5, ease: "power1.inOut" })
        .to(".packet-to-relay", { opacity: 0, duration: 0.1 })
        .set(".packet-to-relay", { y: 0 })
        .to(["#bus-a", "#bus-b"], { x: 0, duration: 0, delay: 1 });

    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <Section 
      ref={containerRef as any} 
      id="mesh" 
      style={{ background: "var(--bg-base)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, rgba(68,136,255,0.5), transparent)" }}
      />
      
      <PageContainer>
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          {/* Left: Content */}
          <div className="flex flex-col">
            <div className="mesh-text inline-flex items-center gap-2 mb-8 px-5 py-2.5 rounded-full self-start" style={{ background: "rgba(68, 136, 255, 0.08)", border: "1px solid rgba(68, 136, 255, 0.25)" }}>
              <span className="label-text" style={{ color: "var(--accent-electric)", letterSpacing: "0.15em" }}>OPPORTUNISTIC NETWORKING</span>
            </div>
            
            <h2 className="mesh-text text-title font-heading font-extrabold mb-6 tracking-tight text-text-primary">
              No Internet? <br />
              <span className="gradient-text">No Problem.</span>
            </h2>
            
            <p className="mesh-text text-body mb-10 text-text-secondary max-w-xl">
              Continuous cellular connectivity across an entire city is unrealistic. UrbanMesh introduces a 
              <strong className="font-semibold text-text-primary"> Semantic Delay-Tolerant Urban Network</strong>. Buses store observations and exchange critical event capsules when they pass each other, eventually routing intelligence to fixed city relays.
            </p>
            
            {/* 2x2 Grid for the Process */}
            <div className="mesh-text grid grid-cols-2 gap-4 lg:gap-6 w-full">
              {[
                { label: "Store", value: "Local Storage" },
                { label: "Carry", value: "Physical Transit" },
                { label: "Forward", value: "Peer Discovery" },
                { label: "Upload", value: "Dynamic Gateways" },
              ].map((step, idx) => (
                <div 
                  key={idx} 
                  className="p-5 rounded-2xl transition-all duration-300 hover:scale-[1.02] glass-card"
                  style={{
                    padding: "20px",
                  }}
                >
                  <div className="text-xs mb-3 font-mono text-text-muted">0{idx + 1}</div>
                  <div className="font-heading font-bold text-lg mb-1" style={{ color: "var(--accent-electric)" }}>{step.label}</div>
                  <div className="text-sm text-text-secondary">{step.value}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Right: Diagram */}
          <div className="mesh-text w-full flex items-center justify-center h-full min-h-[400px] lg:min-h-[500px]">
            <div 
              className="relative w-full h-[400px] lg:h-[500px] rounded-3xl overflow-hidden glass-card flex flex-col items-center justify-center" 
            >
              <div className="absolute inset-0 grid-bg opacity-30 pointer-events-none"></div>
              
              <div className="relative z-10 w-full flex flex-col items-center justify-center">
                
                {/* Cloud Relay */}
                <div className="relative mb-24">
                  <div className="w-16 h-16 rounded-xl flex items-center justify-center text-3xl" style={{ background: "rgba(0, 212, 255, 0.1)", border: "1px solid var(--accent-cyan)" }}>
                    ☁️
                  </div>
                  <div className="absolute top-full mt-3 left-1/2 -translate-x-1/2 text-xs font-mono text-cyan-400 whitespace-nowrap">
                    CITY PLATFORM
                  </div>
                  
                  {/* Packet to relay */}
                  <div className="packet-to-relay absolute top-full left-1/2 -translate-x-1/2 w-4 h-4 bg-cyan-400 rounded-full opacity-0 shadow-[0_0_15px_#00d4ff]"></div>
                </div>

                {/* Road / Bus track */}
                <div className="relative w-[80%] max-w-sm h-32 border-t border-b border-dashed border-white/20 flex items-center">
                  
                  <div id="bus-a" className="absolute left-[10%] w-12 h-12 rounded-xl flex items-center justify-center text-xl z-20" style={{ background: "rgba(68, 136, 255, 0.2)", border: "1px solid var(--accent-electric)" }}>
                    🚌
                    <div className="absolute -top-7 text-[10px] font-mono text-blue-400 whitespace-nowrap bg-base/80 px-2 py-0.5 rounded backdrop-blur">
                      BUS-A (Offline)
                    </div>
                  </div>

                  {/* Packet transfer */}
                  <div className="packet absolute left-[30%] w-3 h-3 bg-amber-400 rounded-full opacity-0 shadow-[0_0_10px_#ffaa00]"></div>

                  <div id="bus-b" className="absolute left-[50%] w-12 h-12 rounded-xl flex items-center justify-center text-xl z-20" style={{ background: "rgba(68, 136, 255, 0.2)", border: "1px solid var(--accent-electric)" }}>
                    🚌
                    <div className="absolute -bottom-7 text-[10px] font-mono text-blue-400 whitespace-nowrap bg-base/80 px-2 py-0.5 rounded backdrop-blur">
                      BUS-B (Gateway)
                    </div>
                  </div>

                </div>
                
                <div className="mt-12 text-center px-8">
                   <p className="text-xs font-mono text-text-secondary">
                     Event Capsule exchange via WiFi-Aware / BLE.<br/>Routing algorithm prioritizes critical events.
                   </p>
                </div>

              </div>
            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
