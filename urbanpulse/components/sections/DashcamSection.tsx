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

        {/* Centered Hero Content Stack */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4 sm:px-6 z-10 pt-8 md:pt-12">

          {/* Eyebrow */}
          <span
            className="inline-block text-[12px] sm:text-[13px] font-black tracking-[0.24em] uppercase mb-4 sm:mb-5"
            style={{ color: "#F59E0B" }}
          >
            MOBILE VISION
          </span>

          {/* Title */}
          <h2 className="text-4xl sm:text-6xl lg:text-7xl font-display font-black leading-tight mb-5 sm:mb-6">
            <span className="text-white">Bus </span>
            <span style={{ color: "#FBBF24" }}>Dashcams</span>
          </h2>

          {/* Subtitle / Tagline */}
          <p className="text-base sm:text-lg lg:text-xl text-white font-bold leading-relaxed max-w-xl mb-4 sm:mb-5">
            Turn moving public transport into intelligent city sensors.
          </p>

          {/* Feature Pills Container - Translucent style without dark shadows */}
          <div 
            className="w-full max-w-6xl mx-auto px-4 mt-8 sm:mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-4"
            style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: "24px", rowGap: "16px", marginTop: "2.5rem" }}
          >
            {FEATURES.map((feature, idx) => (
              <div
                key={idx}
                className="inline-flex items-center gap-2.5 px-5 py-2.5 text-sm md:text-base tracking-wide whitespace-nowrap rounded-full transition-transform hover:scale-105"
                style={{
                  background: "rgba(0, 0, 0, 0.2)",
                  border: "1px solid rgba(245, 158, 11, 0.45)",
                }}
              >
                <i 
                  className={`bi ${feature.icon} shrink-0`} 
                  style={{ 
                    color: "#FBBF24", 
                    fontSize: "15px",
                  }}
                ></i>
                <span className="font-extrabold text-white tracking-wide leading-relaxed whitespace-nowrap">
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









