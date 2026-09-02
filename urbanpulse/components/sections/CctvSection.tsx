"use client";

import Section from "@/components/layout/Section";
import Image from "next/image";

const FEATURES = [
  { title: "24/7 Urban Monitoring", icon: "bi-clock-history" },
  { title: "Traffic & Violation Detection", icon: "bi-car-front-fill" },
  { title: "Incident & Anomaly Detection", icon: "bi-exclamation-triangle-fill" },
  { title: "Multi-Camera Intelligence", icon: "bi-camera-video-fill" },
  { title: "Real-Time Alerts", icon: "bi-bell-fill" },
];

export default function CctvSection() {
  return (
    <Section id="cctv" className="!p-0 min-h-screen overflow-hidden">
      <div className="relative w-full h-screen min-h-[600px]">

        {/* Background Image — full quality */}
        <Image
          src="/FINAL PHOTO FOR CCTV.png"
          alt="CCTV Analysis"
          fill
          className="object-cover object-center"
          sizes="100vw"
          priority
          quality={100}
        />

        {/* Centered Content Stack */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-4 sm:px-6 z-10 pt-8 md:pt-12">

          {/* Eyebrow */}
          <span
            className="inline-block text-[11px] lg:text-[12px] font-bold tracking-[0.22em] uppercase mb-4 sm:mb-5"
            style={{ color: "#22D3EE" }}
          >
            FIXED VISION
          </span>

          {/* Title */}
          <h2
            className="text-[44px] lg:text-[66px] xl:text-[80px] font-display font-bold leading-[1.05] mb-5 sm:mb-6"
          >
            <span className="text-white">CCTV </span>
            <span style={{ color: "#22D3EE" }}>Cameras</span>
          </h2>

          {/* Subtitle / Description */}
          <p
            className="text-[16px] lg:text-[20px] text-white font-medium leading-[1.6] max-w-xl mb-4 sm:mb-5"
          >
            Continuous intelligence from fixed urban viewpoints.
          </p>

          {/* Feature Pills Container - max-w-6xl wide spread with gap-x-8 and gap-y-5 */}
          <div 
            className="w-full max-w-6xl mx-auto px-6 mt-12 flex flex-wrap items-center justify-center gap-x-8 gap-y-5"
            style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: "32px", rowGap: "20px", marginTop: "3rem" }}
          >
            {FEATURES.map((feature, idx) => (
              <div
                key={idx}
                className="inline-flex items-center gap-3 px-6 py-2.5 text-sm md:text-base font-medium tracking-wider whitespace-nowrap rounded-full border border-cyan-400/50 bg-black/20 transition-transform hover:scale-105"
                style={{
                  background: "rgba(0, 0, 0, 0.2)",
                  border: "1.5px solid rgba(34, 211, 238, 0.5)",
                }}
              >
                <i 
                  className={`bi ${feature.icon} shrink-0`} 
                  style={{ 
                    color: "#22D3EE", 
                    fontSize: "15px",
                  }}
                ></i>
                <span className="font-extrabold text-white tracking-wider leading-relaxed whitespace-nowrap">
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

