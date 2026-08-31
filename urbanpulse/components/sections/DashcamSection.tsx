"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import Image from "next/image";

const FEATURES = [
  {
    title: "Moving-Camera Intelligence",
    description: "Continuously understand traffic, road conditions and surrounding activity while the bus moves.",
    icon: "bi-camera-video",
  },
  {
    title: "On-Bus Edge AI",
    description: "Analyze video locally to reduce latency, bandwidth consumption and dependence on cloud connectivity.",
    icon: "bi-cpu",
  },
  {
    title: "Geo-Tagged Event Detection",
    description: "Attach location, timestamp and confidence scores to detected road events.",
    icon: "bi-geo-alt",
  },
  {
    title: "Multi-Bus Evidence Fusion",
    description: "Combine observations from multiple buses to confirm incidents and reduce false alerts.",
    icon: "bi-diagram-3",
  },
  {
    title: "Real-Time Road Intelligence",
    description: "Detect hazards and traffic events while the vehicle is still moving through the city.",
    icon: "bi-lightning-charge",
  }
];

export default function DashcamSection() {
  return (
    <Section id="dashcam" className="bg-[var(--bg-main)] text-white !pt-[50px] lg:!pt-[80px] !pb-10 flex flex-col justify-start min-h-screen overflow-x-hidden">
      <div className="w-full flex flex-col lg:flex-row items-center justify-between gap-10 lg:gap-0">
        
        {/* Text Content */}
        <div className="flex flex-col z-10 w-full lg:w-[42%] pl-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] pr-[max(clamp(20px,5vw,88px),calc((100vw-1600px)/2+88px))] lg:pr-10 xl:pr-16">
            {/* Header */}
            <div className="mb-10 lg:mb-12">
              <span className="inline-block text-[12px] lg:text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--orange)] mb-4">
                MOBILE VISION
              </span>
              <h2 className="text-[36px] lg:text-[46px] xl:text-[56px] font-display font-bold text-white mb-4 leading-[1.05]">
                Bus <span className="text-[var(--orange)]">Dashcams</span>
              </h2>
              <h3 className="text-[18px] lg:text-[22px] text-[var(--text-secondary)] font-medium tracking-tight leading-[1.3]">
                Turn moving public transport into intelligent city sensors.
              </h3>
            </div>

            {/* Features List */}
            <div className="flex flex-col gap-[20px] lg:gap-[26px]">
              {FEATURES.map((feature, idx) => (
                <div key={idx} className="grid grid-cols-[38px_1fr] lg:grid-cols-[42px_1fr] gap-[16px] group">
                  <div className="w-[38px] h-[38px] lg:w-[42px] lg:h-[42px] flex items-center justify-center rounded-[10px] border border-[var(--orange)]/20 bg-[var(--orange)]/5 text-[var(--orange)] text-[18px] lg:text-[20px] transition-all duration-300 group-hover:bg-[var(--orange)]/10 group-hover:border-[var(--orange)]/40">
                    <i className={`bi ${feature.icon}`}></i>
                  </div>
                  <div>
                    <h4 className="text-[16px] lg:text-[19px] font-semibold text-white mb-1 group-hover:text-[var(--orange)] transition-colors duration-300">
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
                src="/dashcam analysis.png"
                alt="Bus Dashcam Analysis"
                fill
                className="object-cover object-center group-hover:scale-105 transition-transform duration-[1200ms] ease-out"
                sizes="(max-width: 1024px) 100vw, 60vw"
                priority
              />
              {/* Fade out to the left to blend with background */}
              <div className="absolute inset-0 bg-gradient-to-r from-[var(--bg-main)] via-[var(--bg-main)]/60 to-transparent w-[35%]" />
            </div>

            {/* Top Node Telemetry Card */}
            <div className="!absolute top-4 lg:top-8 left-4 lg:left-[-20px] premium-card p-3 lg:p-5 min-w-[200px] lg:min-w-[260px] shadow-[0_20px_50px_rgba(0,0,0,0.5)] border-[var(--orange)]/20 backdrop-blur-[24px]">
              <div className="flex justify-between items-center mb-2 lg:mb-3">
                <span className="hud-text text-[var(--orange)] font-medium text-[11px] lg:text-[13px]">BUS TN-38-XXXX</span>
                <div className="flex items-center gap-1.5 lg:gap-2">
                  <span className="w-1.5 h-1.5 lg:w-2 lg:h-2 rounded-full bg-[var(--success)] animate-pulse shadow-[0_0_8px_var(--success)]"></span>
                  <span className="hud-text text-[var(--success)] text-[10px] lg:text-[12px]">ACTIVE</span>
                </div>
              </div>
              <div className="space-y-2 lg:space-y-3 pt-2 lg:pt-3 border-t border-white/10">
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">GPS</span>
                  <span className="font-mono text-white">11.0168, 76.9558</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">TIMESTAMP</span>
                  <span className="font-mono text-white">09:42:16</span>
                </div>
                <div className="flex justify-between items-center text-[10px] lg:text-[12px]">
                  <span className="text-[var(--text-muted)] font-medium">TRAFFIC</span>
                  <span className="font-mono text-[var(--warning)]">MODERATE</span>
                </div>
              </div>
            </div>

            {/* Detections Overlay */}
            <div className="!absolute top-1/2 right-4 lg:right-8 -translate-y-1/2 flex flex-col gap-2 lg:gap-4">
               <div className="premium-card p-2 lg:p-3 px-3 lg:px-5 border-[var(--orange)]/30 shadow-[0_10px_30px_rgba(245,158,11,0.15)] bg-[rgba(10,15,23,0.85)]">
                 <div className="text-[12px] lg:text-[14px] font-bold text-white mb-0.5">POTHOLE</div>
                 <div className="text-[9px] lg:text-[11px] font-mono text-[var(--text-muted)] tracking-wide">CONFIDENCE <span className="text-[var(--orange)] ml-1">96%</span></div>
               </div>
               <div className="premium-card p-2 lg:p-3 px-3 lg:px-5 border-[var(--danger)]/30 shadow-[0_10px_30px_rgba(244,63,94,0.15)] bg-[rgba(10,15,23,0.85)]">
                 <div className="text-[12px] lg:text-[14px] font-bold text-white mb-0.5">NEAR COLLISION</div>
                 <div className="text-[9px] lg:text-[11px] font-mono text-[var(--text-muted)] tracking-wide">RISK <span className="text-[var(--danger)] ml-1">HIGH</span></div>
               </div>
               <div className="premium-card p-2 lg:p-3 px-3 lg:px-5 border-[var(--warning)]/30 shadow-[0_10px_30px_rgba(251,191,36,0.15)] bg-[rgba(10,15,23,0.85)] opacity-80">
                 <div className="text-[12px] lg:text-[14px] font-bold text-white mb-0.5">PEDESTRIAN RISK</div>
                 <div className="text-[9px] lg:text-[11px] font-mono text-[var(--text-muted)] tracking-wide">CONFIDENCE <span className="text-[var(--warning)] ml-1">89%</span></div>
               </div>
            </div>

            {/* Bottom Pipeline */}
            <div className="!absolute bottom-4 lg:bottom-8 left-1/2 -translate-x-1/2 w-[90%] lg:w-[85%] premium-card p-2.5 lg:p-4 flex items-center justify-between text-[8px] lg:text-[11px] font-mono text-[var(--text-muted)] border-white/5 bg-[rgba(10,15,23,0.95)] z-20 overflow-x-auto whitespace-nowrap scrollbar-hide">
              <div className="flex flex-col items-center gap-1 lg:gap-1.5 min-w-[40px] lg:min-w-[60px]">
                <i className="bi bi-camera-video text-[14px] lg:text-[18px] text-[var(--text-primary)]"></i>
                <span>CAMERA</span>
              </div>
              <i className="bi bi-arrow-right text-[var(--orange)] mx-1 lg:mx-2"></i>
              <div className="flex flex-col items-center gap-1 lg:gap-1.5 min-w-[40px] lg:min-w-[60px]">
                <i className="bi bi-cpu text-[14px] lg:text-[18px] text-[var(--text-primary)]"></i>
                <span>EDGE AI</span>
              </div>
              <i className="bi bi-arrow-right text-[var(--orange)] mx-1 lg:mx-2"></i>
              <div className="flex flex-col items-center gap-1 lg:gap-1.5 min-w-[40px] lg:min-w-[60px]">
                <i className="bi bi-geo-alt text-[14px] lg:text-[18px] text-[var(--text-primary)]"></i>
                <span>EVENT</span>
              </div>
              <i className="bi bi-arrow-right text-[var(--orange)] mx-1 lg:mx-2"></i>
              <div className="flex flex-col items-center gap-1 lg:gap-1.5 min-w-[40px] lg:min-w-[60px]">
                <i className="bi bi-diagram-3 text-[14px] lg:text-[18px] text-[var(--text-primary)]"></i>
                <span>MESH</span>
              </div>
              <i className="bi bi-arrow-right text-[var(--orange)] mx-1 lg:mx-2"></i>
              <div className="flex flex-col items-center gap-1 lg:gap-1.5 min-w-[40px] lg:min-w-[60px]">
                <i className="bi bi-cloud text-[14px] lg:text-[18px] text-[var(--blue)]"></i>
                <span className="text-[var(--blue)]">PLATFORM</span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </Section>
  );
}
