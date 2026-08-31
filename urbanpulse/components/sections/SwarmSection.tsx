"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import Image from "next/image";

const FEATURES = [
  {
    title: "Peer-to-Peer Connectivity",
    description: "Nearby buses and sensing nodes communicate directly without depending on a central Wi-Fi network.",
    icon: "bi-diagram-2",
  },
  {
    title: "Works in Low Connectivity",
    description: "Critical events can be stored, carried, and forwarded until a connected node reaches the city platform.",
    icon: "bi-wifi-off",
  },
  {
    title: "Dynamic Data Routing",
    description: "Information automatically finds an available path through nearby nodes toward the central intelligence platform.",
    icon: "bi-signpost-split",
  },
  {
    title: "Self-Healing Network",
    description: "If one connection becomes unavailable, the system can continue exchanging intelligence through other nearby nodes.",
    icon: "bi-shield-check",
  }
];

export default function SwarmSection() {
  return (
    <Section id="swarm" className="bg-[var(--bg-main)] text-white !pt-[50px] lg:!pt-[80px] !pb-10 flex flex-col justify-start min-h-screen overflow-x-hidden">
      <div className="w-full flex flex-col lg:flex-row items-center justify-between gap-10 lg:gap-0">
        
        {/* Text Content */}
        <div className="flex flex-col z-10 w-full lg:w-[42%] pl-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] pr-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] lg:pr-10 xl:pr-16">
            {/* Header */}
            <div className="mb-10 lg:mb-12">
              <span className="inline-block text-[12px] lg:text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--violet)] mb-4">
                RESILIENT NETWORK
              </span>
              <h2 className="text-[36px] lg:text-[46px] xl:text-[56px] font-display font-bold text-white mb-4 leading-[1.05]">
                Urban <span className="text-[var(--violet)]">Swarm Mesh</span>
              </h2>
              <h3 className="text-[18px] lg:text-[22px] text-[var(--text-secondary)] font-medium tracking-tight leading-[1.3]">
                A self-connected intelligence network built across the city.
              </h3>
            </div>

            {/* Features List */}
            <div className="flex flex-col gap-[20px] lg:gap-[26px]">
              {FEATURES.map((feature, idx) => (
                <div key={idx} className="grid grid-cols-[38px_1fr] lg:grid-cols-[42px_1fr] gap-[16px] group">
                  <div className="w-[38px] h-[38px] lg:w-[42px] lg:h-[42px] flex items-center justify-center rounded-[10px] border border-[var(--violet)]/20 bg-[var(--violet)]/5 text-[var(--violet)] text-[18px] lg:text-[20px] transition-all duration-300 group-hover:bg-[var(--violet)]/10 group-hover:border-[var(--violet)]/40">
                    <i className={`bi ${feature.icon}`}></i>
                  </div>
                  <div>
                    <h4 className="text-[16px] lg:text-[19px] font-semibold text-white mb-1 group-hover:text-[var(--violet)] transition-colors duration-300">
                      {feature.title}
                    </h4>
                    <p className="text-[14px] lg:text-[17px] text-[var(--text-muted)] leading-[1.55] font-normal max-w-[520px]">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

        {/* Cinematic Image Content */}
        <div className="w-full lg:w-[58%] px-[clamp(20px,5vw,88px)] lg:px-0 mt-8 lg:mt-0">
          <div className="relative w-full min-h-[400px] h-[50vh] lg:h-[calc(100vh-140px)] lg:max-h-[700px] group">
            <div className="absolute inset-0 rounded-[24px] lg:rounded-l-[32px] lg:rounded-r-none overflow-hidden">
              <Image
                src="/changed photo for mesh.png"
                alt="Urban Swarm Mesh"
                fill
                className="object-cover object-center group-hover:scale-105 transition-transform duration-[1200ms] ease-out"
                sizes="(max-width: 1024px) 100vw, 60vw"
                priority
              />
              {/* Fade out to the left to blend with background */}
              <div className="absolute inset-0 bg-gradient-to-r from-[var(--bg-main)] via-[var(--bg-main)]/60 to-transparent w-[35%]" />
              <div className="absolute inset-0 bg-[var(--violet)]/10 mix-blend-color" />
            </div>

            {/* SVG Animated Mesh Overlay */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-[24px]">
              <svg className="w-full h-full" preserveAspectRatio="xMidYMid slice" viewBox="0 0 800 800">
                <defs>
                  <filter id="glowMesh" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="4" result="blur" />
                    <feMerge>
                      <feMergeNode in="blur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                </defs>
                
                {/* Mesh Lines */}
                <g stroke="rgba(168, 85, 247, 0.4)" strokeWidth="1.5" fill="none" filter="url(#glowMesh)">
                  <path d="M 200 600 L 400 400 L 600 500 L 500 700 Z" className="opacity-60" />
                  <path d="M 400 400 L 450 200 L 650 300 L 600 500 Z" className="opacity-60" />
                  <path d="M 200 600 L 100 400 L 300 250 L 450 200" className="opacity-60" />
                  
                  {/* Dynamic Data Pulses */}
                  <circle r="4" fill="#A855F7">
                    <animateMotion dur="3s" repeatCount="indefinite" path="M 200 600 L 400 400 L 600 500 L 500 700 Z" />
                  </circle>
                  <circle r="4" fill="#A855F7">
                    <animateMotion dur="4s" repeatCount="indefinite" path="M 400 400 L 450 200 L 650 300 L 600 500" />
                  </circle>
                  <circle r="4" fill="#A855F7">
                    <animateMotion dur="2.5s" repeatCount="indefinite" path="M 200 600 L 100 400 L 300 250 L 450 200" />
                  </circle>
                </g>

                {/* Mesh Nodes */}
                <g fill="#A855F7" filter="url(#glowMesh)">
                  <circle cx="200" cy="600" r="8" />
                  <circle cx="400" cy="400" r="10">
                     <animate attributeName="r" values="10; 14; 10" dur="2s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="600" cy="500" r="8" />
                  <circle cx="500" cy="700" r="6" />
                  <circle cx="450" cy="200" r="12">
                    <animate attributeName="r" values="12; 16; 12" dur="3s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="650" cy="300" r="7" />
                  <circle cx="100" cy="400" r="6" />
                  <circle cx="300" cy="250" r="8" />
                </g>

                {/* Connection Status Text */}
                <text x="420" y="395" fill="white" fontSize="12" fontFamily="monospace" fontWeight="bold">NODE 01_A</text>
                <text x="470" y="195" fill="white" fontSize="12" fontFamily="monospace" fontWeight="bold">NODE 02_M</text>
              </svg>
            </div>

            {/* Mesh UI Card */}
            <div className="!absolute bottom-6 lg:bottom-10 left-6 lg:left-10 premium-card p-3 lg:p-5 min-w-[200px] lg:min-w-[260px] shadow-[0_20px_50px_rgba(0,0,0,0.5)] border-[var(--violet)]/20 backdrop-blur-[24px]">
              <div className="flex justify-between items-center mb-2 lg:mb-3">
                <span className="hud-text text-[var(--violet)] font-medium text-[11px] lg:text-[13px]">SWARM MESH</span>
                <div className="flex items-center gap-1.5 lg:gap-2">
                  <span className="w-1.5 h-1.5 lg:w-2 lg:h-2 rounded-full bg-[var(--violet)] animate-pulse shadow-[0_0_8px_var(--violet)]"></span>
                  <span className="hud-text text-[var(--violet)] text-[10px] lg:text-[12px]">SYNCED</span>
                </div>
              </div>
              <div className="space-y-2 lg:space-y-3 pt-2 lg:pt-3 border-t border-white/10">
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">ACTIVE NODES</span>
                  <span className="font-mono text-white">124</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">P2P LATENCY</span>
                  <span className="font-mono text-[var(--success)]">12ms</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">DATA PACKETS</span>
                  <span className="font-mono text-white">45.2K/s</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </Section>
  );
}
