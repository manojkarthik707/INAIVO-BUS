"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";

export default function ContextSection() {
  return (
    <Section id="platform" className="bg-[var(--bg-secondary)] text-white relative">
      {/* Subtle texture */}
      <div className="bg-texture" />

      <PageContainer className="relative z-10">
        <div className="grid lg:grid-cols-[0.45fr_0.55fr] gap-[clamp(40px,6vw,100px)] items-center">
          
          {/* Text Content */}
          <div className="flex flex-col">
            <span className="inline-block text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--blue)] mb-8">
              CONNECTED INTELLIGENCE
            </span>
            
            <h2 className="text-[48px] md:text-[62px] lg:text-[72px] font-display font-bold text-white mb-10 leading-[1.1] tracking-tight">
              Cities have cameras.<br />
              <span className="text-[var(--text-muted)]">They don&apos;t have<br /></span>
              <span className="text-[var(--blue)]">connected intelligence.</span>
            </h2>
            
            <p className="text-[17px] md:text-[18px] text-[var(--text-secondary)] leading-[1.7] font-normal max-w-[560px] mb-16">
              Connect public buses, CCTV cameras and roadside sensors through edge AI and resilient communication to detect hazards, traffic events and incidents as they happen.
            </p>

            {/* Metrics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 border-t border-white/10 pt-10">
              <div>
                <div className="text-[28px] font-display font-bold text-white mb-1">3</div>
                <div className="text-[13px] font-medium text-[var(--text-muted)] leading-snug">Camera Sources<br/>Unified</div>
              </div>
              <div>
                <div className="text-[28px] font-display font-bold text-white mb-1">&lt; 2s</div>
                <div className="text-[13px] font-medium text-[var(--text-muted)] leading-snug">Detection<br/>Pipeline</div>
              </div>
              <div>
                <div className="text-[28px] font-display font-bold text-white mb-1">24<span className="text-[20px] text-[var(--text-muted)]">x</span>7</div>
                <div className="text-[13px] font-medium text-[var(--text-muted)] leading-snug">Urban<br/>Monitoring</div>
              </div>
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <div className="w-2 h-2 rounded-full bg-[var(--danger)] animate-pulse shadow-[0_0_8px_var(--danger)]"></div>
                  <div className="text-[28px] font-display font-bold text-white leading-none">LIVE</div>
                </div>
                <div className="text-[13px] font-medium text-[var(--text-muted)] leading-snug mt-1">Incident<br/>Alerts</div>
              </div>
            </div>
          </div>

          {/* Live Architecture Diagram */}
          <div className="relative w-full h-[600px] flex items-center justify-center premium-card !bg-transparent !border-none !shadow-none">
            {/* SVG Background Lines */}
            <div className="absolute inset-0 flex items-center justify-center">
              <svg className="w-full h-full max-w-[600px]" viewBox="0 0 600 600" preserveAspectRatio="none">
                {/* Lines from sources to center */}
                <path d="M 120 150 C 250 150, 250 300, 300 300" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                <path d="M 120 300 L 300 300" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                <path d="M 120 450 C 250 450, 250 300, 300 300" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />

                {/* Animated Pulses in */}
                <circle r="4" fill="var(--orange)">
                    <animateMotion dur="3s" repeatCount="indefinite" path="M 120 150 C 250 150, 250 300, 300 300" />
                </circle>
                <circle r="4" fill="var(--cyan)">
                    <animateMotion dur="2.5s" repeatCount="indefinite" path="M 120 300 L 300 300" />
                </circle>
                <circle r="4" fill="var(--blue)">
                    <animateMotion dur="4s" repeatCount="indefinite" path="M 120 450 C 250 450, 250 300, 300 300" />
                </circle>

                {/* Lines from center to outputs */}
                <path d="M 300 300 C 400 300, 400 200, 480 200" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                <path d="M 300 300 C 400 300, 400 400, 480 400" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                
                {/* Animated Pulses out */}
                <circle r="4" fill="var(--danger)">
                    <animateMotion dur="2s" repeatCount="indefinite" path="M 300 300 C 400 300, 400 200, 480 200" />
                </circle>
                <circle r="4" fill="var(--success)">
                    <animateMotion dur="2.8s" repeatCount="indefinite" path="M 300 300 C 400 300, 400 400, 480 400" />
                </circle>
              </svg>
            </div>

            <div className="relative w-full max-w-[600px] h-[600px] flex items-center justify-between">
                {/* Left Column: Sources */}
                <div className="flex flex-col gap-12 z-10 w-[120px]">
                    <div className="premium-card !p-4 flex flex-col items-center justify-center gap-2 text-center bg-[rgba(12,18,27,0.9)] hover:border-[var(--orange)]/50 transition-colors">
                        <div className="w-10 h-10 rounded-full bg-[var(--orange)]/10 text-[var(--orange)] flex items-center justify-center text-[18px]">
                            <i className="bi bi-bus-front"></i>
                        </div>
                        <span className="text-[10px] font-bold tracking-wider text-white">BUS DASHCAMS</span>
                    </div>
                    <div className="premium-card !p-4 flex flex-col items-center justify-center gap-2 text-center bg-[rgba(12,18,27,0.9)] hover:border-[var(--cyan)]/50 transition-colors">
                        <div className="w-10 h-10 rounded-full bg-[var(--cyan)]/10 text-[var(--cyan)] flex items-center justify-center text-[18px]">
                            <i className="bi bi-camera-video"></i>
                        </div>
                        <span className="text-[10px] font-bold tracking-wider text-white">CCTV CAMERAS</span>
                    </div>
                    <div className="premium-card !p-4 flex flex-col items-center justify-center gap-2 text-center bg-[rgba(12,18,27,0.9)] hover:border-[var(--blue)]/50 transition-colors">
                        <div className="w-10 h-10 rounded-full bg-[var(--blue)]/10 text-[var(--blue)] flex items-center justify-center text-[18px]">
                            <i className="bi bi-webcam"></i>
                        </div>
                        <span className="text-[10px] font-bold tracking-wider text-white">ROADSIDE CAMERAS</span>
                    </div>
                </div>

                {/* Center: Intelligence */}
                <div className="z-10 absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
                    <div className="premium-card !p-6 flex flex-col items-center justify-center gap-4 text-center bg-[rgba(12,18,27,0.95)] border-[var(--blue)]/40 shadow-[0_0_40px_rgba(47,129,247,0.15)] relative">
                        <div className="absolute inset-0 bg-[var(--blue)]/5 animate-pulse rounded-[16px]"></div>
                        <div className="w-14 h-14 rounded-xl bg-[var(--blue)]/20 border border-[var(--blue)]/30 text-[var(--blue)] flex items-center justify-center text-[28px] shadow-[0_0_20px_rgba(47,129,247,0.4)]">
                            <i className="bi bi-cpu"></i>
                        </div>
                        <div>
                            <div className="text-[13px] font-extrabold tracking-widest text-white mb-1">INCIDENT ENGINE</div>
                            <div className="text-[10px] text-[var(--blue)] font-mono">CENTRAL INTELLIGENCE</div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Outputs */}
                <div className="flex flex-col gap-24 z-10 w-[120px] absolute right-0">
                    <div className="premium-card !p-4 flex flex-col items-center justify-center gap-2 text-center bg-[rgba(12,18,27,0.9)] hover:border-[var(--danger)]/50 transition-colors -translate-y-8">
                        <div className="w-10 h-10 rounded-full bg-[var(--danger)]/10 text-[var(--danger)] flex items-center justify-center text-[18px]">
                            <i className="bi bi-bell"></i>
                        </div>
                        <span className="text-[10px] font-bold tracking-wider text-white">REAL-TIME ALERTS</span>
                    </div>
                    <div className="premium-card !p-4 flex flex-col items-center justify-center gap-2 text-center bg-[rgba(12,18,27,0.9)] hover:border-[var(--success)]/50 transition-colors translate-y-8">
                        <div className="w-10 h-10 rounded-full bg-[var(--success)]/10 text-[var(--success)] flex items-center justify-center text-[18px]">
                            <i className="bi bi-bar-chart"></i>
                        </div>
                        <span className="text-[10px] font-bold tracking-wider text-white">CITY ANALYTICS</span>
                    </div>
                </div>

            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
