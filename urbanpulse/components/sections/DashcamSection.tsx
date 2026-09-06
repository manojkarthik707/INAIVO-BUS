"use client";

import Section from "@/components/layout/Section";
import Image from "next/image";

const FEATURES = [
  { title: "Moving-Camera Intelligence", icon: "bi-camera-video-fill" },
  { title: "On-Bus Edge AI", icon: "bi-cpu-fill" },
  { title: "Geo-Tagged Event Detection", icon: "bi-geo-alt-fill" },
  { title: "Multi-Bus Evidence Fusion", icon: "bi-diagram-3-fill" },
  { title: "Real-Time Road Intelligence", icon: "bi-lightning-charge-fill" },
];

export default function DashcamSection() {
  return (
    <Section id="dashcam" className="!p-0 min-h-screen overflow-hidden">
      <div className="relative w-full h-screen min-h-[600px]">

        {/* Background Image — full quality */}
        <Image
          src="/FINAL PHOTO FOR DASHCAM ANALYSIS.png"
          alt="Bus Dashcam Analysis"
          fill
          className="object-cover object-center"
          sizes="100vw"
          priority
          quality={100}
        />
        
        {/* INAIVO Logo overlay to hide Gemini watermark */}
        <div className="absolute bottom-[10%] right-[8%] z-20 p-2 rounded-full aspect-square backdrop-blur-sm bg-black/40 flex items-center justify-center scale-125">
          <Image src="/LOGO_INAIVO.png" alt="INAIVO Logo" width={64} height={64} className="object-contain w-auto h-12 opacity-100" />
        </div>

        {/* No overlay — image stays fully vivid. Text shadows handle contrast. */}

        {/* Centered Text Overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-6 z-10 -translate-y-12">

          {/* Eyebrow */}
          <span
            className="inline-block text-[11px] lg:text-[12px] font-black tracking-[0.22em] uppercase mb-5"
            style={{ color: "#F59E0B", textShadow: "0 0 8px rgba(0,0,0,1), 0 2px 16px rgba(0,0,0,1), 0 4px 40px rgba(0,0,0,0.9)" }}
          >
            MOBILE VISION
          </span>

          {/* Title */}
          <h2
            className="text-[44px] lg:text-[66px] xl:text-[80px] font-display font-black leading-[1.05] mb-5"
          >
            <span className="text-white drop-shadow-md">Bus </span>
            <span style={{ color: "#FBBF24" }} className="drop-shadow-md">Dashcams</span>
          </h2>

          {/* Subtitle */}
          <p
            className="text-[16px] lg:text-[20px] text-white font-medium leading-[1.6] max-w-xl mb-10 drop-shadow-sm"
          >
            Turn moving public transport into intelligent city sensors.
          </p>

          {/* Feature Pills */}
          <div className="flex flex-wrap justify-center gap-2.5 lg:gap-3 max-w-3xl">
            {FEATURES.map((feature, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 px-4 py-2 rounded-full"
                style={{
                  background: "rgba(0,0,0,0.65)",
                  border: "1px solid rgba(245,158,11,0.45)",
                  backdropFilter: "blur(8px)",
                }}
              >
                <i className={`bi ${feature.icon}`} style={{ color: "#FBBF24", fontSize: "13px" }}></i>
                <span className="text-[15px] lg:text-[17px] font-semibold text-white">
                  {feature.title}
                </span>
              </div>
            ))}
          </div>

        </div>
      </div>
    </Section>
  );
}
