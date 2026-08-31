"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import Image from "next/image";

const FEATURES = [
  {
    title: "24/7 Urban Monitoring",
    description: "Continuously observe critical junctions, public spaces, roads, and infrastructure.",
    icon: "bi-clock-history",
  },
  {
    title: "Traffic & Violation Detection",
    description: "Identify congestion, illegal parking, unsafe driving, blocked lanes, and traffic-rule violations.",
    icon: "bi-car-front",
  },
  {
    title: "Incident & Anomaly Detection",
    description: "Detect accidents, stalled vehicles, road obstructions, unusual activity, and other urban events.",
    icon: "bi-exclamation-triangle",
  },
  {
    title: "Multi-Camera Intelligence",
    description: "Fuse CCTV data with bus dashcams and fixed roadside cameras to improve coverage and event verification.",
    icon: "bi-camera-video",
  },
  {
    title: "Real-Time Alerts",
    description: "Send high-priority incidents to the city intelligence platform for faster response and decision-making.",
    icon: "bi-bell",
  }
];

export default function CctvSection() {
  return (
    <Section id="cctv" className="bg-[var(--bg-main)] text-white !pt-[50px] lg:!pt-[80px] !pb-10 flex flex-col justify-start min-h-screen overflow-x-hidden">
      <div className="w-full flex flex-col lg:flex-row items-center justify-between gap-10 lg:gap-0">
        
        {/* Text Content */}
        <div className="flex flex-col z-10 w-full lg:w-[42%] pl-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] pr-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] lg:pr-10 xl:pr-16">
            {/* Header */}
            <div className="mb-10 lg:mb-12">
              <span className="inline-block text-[12px] lg:text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--cyan)] mb-4">
                FIXED VISION
              </span>
              <h2 className="text-[36px] lg:text-[46px] xl:text-[56px] font-display font-bold text-white mb-4 leading-[1.05]">
                CCTV <span className="text-[var(--cyan)]">Cameras</span>
              </h2>
              <h3 className="text-[18px] lg:text-[22px] text-[var(--text-secondary)] font-medium tracking-tight leading-[1.3]">
                Continuous intelligence from fixed urban viewpoints.
              </h3>
            </div>

            {/* Features List */}
            <div className="flex flex-col gap-[20px] lg:gap-[26px]">
              {FEATURES.map((feature, idx) => (
                <div key={idx} className="grid grid-cols-[38px_1fr] lg:grid-cols-[42px_1fr] gap-[16px] group">
                  <div className="w-[38px] h-[38px] lg:w-[42px] lg:h-[42px] flex items-center justify-center rounded-[10px] border border-[var(--cyan)]/20 bg-[var(--cyan)]/5 text-[var(--cyan)] text-[18px] lg:text-[20px] transition-all duration-300 group-hover:bg-[var(--cyan)]/10 group-hover:border-[var(--cyan)]/40">
                    <i className={`bi ${feature.icon}`}></i>
                  </div>
                  <div>
                    <h4 className="text-[16px] lg:text-[19px] font-semibold text-white mb-1 group-hover:text-[var(--cyan)] transition-colors duration-300">
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
                src="/cctv analysis.png"
                alt="CCTV Analysis"
                fill
                className="object-cover object-center group-hover:scale-105 transition-transform duration-[1200ms] ease-out"
                sizes="(max-width: 1024px) 100vw, 60vw"
                priority
              />
              {/* Fade out to the left to blend with background if necessary */}
              <div className="absolute inset-0 bg-gradient-to-r from-[var(--bg-main)] via-[var(--bg-main)]/60 to-transparent w-[35%]" />
            </div>

            {/* Floating Product UI Overlays */}
            <div className="!absolute top-4 lg:top-8 right-4 lg:right-8 premium-card p-3 lg:p-5 min-w-[180px] lg:min-w-[220px] shadow-[0_20px_50px_rgba(0,0,0,0.5)] border-[var(--cyan)]/20 backdrop-blur-[24px]">
              <div className="flex justify-between items-center mb-2 lg:mb-3">
                <span className="hud-text text-[var(--cyan)] font-medium text-[11px] lg:text-[13px]">CAM 024</span>
                <div className="flex items-center gap-1.5 lg:gap-2">
                  <span className="w-1.5 h-1.5 lg:w-2 lg:h-2 rounded-full bg-[var(--danger)] animate-pulse shadow-[0_0_8px_var(--danger)]"></span>
                  <span className="hud-text text-[var(--danger)] text-[10px] lg:text-[12px]">LIVE</span>
                </div>
              </div>
              <div className="text-[9px] lg:text-[11px] font-mono text-[var(--text-muted)] mb-2 lg:mb-4 pb-2 lg:pb-3 border-b border-white/10 uppercase tracking-wider">
                Gandhipuram Junction
              </div>
              <div className="space-y-1.5 lg:space-y-3">
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">VEHICLES</span>
                  <span className="font-mono text-white">47</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">CONGESTION</span>
                  <span className="font-mono text-[var(--warning)]">HIGH</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">INCIDENTS</span>
                  <span className="font-mono text-[var(--danger)]">02</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">RISK SCORE</span>
                  <span className="font-mono text-white">74%</span>
                </div>
              </div>
            </div>

            <div className="!absolute bottom-6 lg:bottom-12 left-4 lg:left-[-20px] premium-card p-2 lg:p-3 px-3 lg:px-5 border-[var(--cyan)]/30 shadow-[0_10px_30px_rgba(34,211,238,0.15)] flex items-center gap-2 lg:gap-4">
               <div className="w-6 h-6 lg:w-10 lg:h-10 rounded-[6px] lg:rounded-[10px] bg-[var(--danger)]/10 border border-[var(--danger)]/20 flex items-center justify-center text-[var(--danger)] text-[12px] lg:text-[16px]">
                  <i className="bi bi-exclamation-triangle-fill"></i>
               </div>
               <div>
                 <div className="text-[12px] lg:text-[14px] font-bold text-white mb-0.5">Illegal Parking</div>
                 <div className="text-[9px] lg:text-[11px] font-mono text-[var(--text-muted)] tracking-wide">CONFIDENCE <span className="text-[var(--cyan)] ml-1">94%</span></div>
               </div>
            </div>
          </div>

        </div>
      </div>
    </Section>
  );
}
