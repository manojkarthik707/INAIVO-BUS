"use client";

import Section from "@/components/layout/Section";
import Image from "next/image";

const FEATURES = [
  { title: "Peer-to-Peer Connectivity", icon: "bi-diagram-2-fill" },
  { title: "Works in Low Connectivity", icon: "bi-wifi-off" },
  { title: "Dynamic Data Routing", icon: "bi-signpost-split-fill" },
  { title: "Self-Healing Network", icon: "bi-shield-check" },
];

export default function SwarmSection() {
  return (
    <Section id="swarm" className="!p-0 min-h-screen overflow-hidden">
      <div className="relative w-full h-screen min-h-[600px]">

        {/* Background Image — full quality */}
        <Image
          src="/FINAL PHOTO FOR URBAN MESH.png"
          alt="Urban Swarm Mesh"
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
            style={{ color: "#A855F7" }}
          >
            RESILIENT NETWORK
          </span>

          {/* Title */}
          <h2
            className="text-[44px] lg:text-[66px] xl:text-[80px] font-display font-bold leading-[1.05] mb-5 sm:mb-6"
          >
            <span className="text-white">Urban </span>
            <span style={{ color: "#A855F7" }}>Swarm Mesh</span>
          </h2>

          {/* Subtitle / Description */}
          <p
            className="text-[16px] lg:text-[20px] text-white font-medium leading-[1.6] max-w-xl mb-4 sm:mb-5"
          >
            A self-connected intelligence network built across the city.
          </p>

          {/* Feature Pills Container - max-w-5xl wide spread with gap-x-6 and gap-y-4 */}
          <div 
            className="w-full max-w-5xl mx-auto px-4 mt-8 sm:mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-4"
            style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", columnGap: "24px", rowGap: "16px", marginTop: "2.5rem" }}
          >
            {FEATURES.map((feature, idx) => (
              <div
                key={idx}
                className="inline-flex items-center gap-2.5 px-5 py-2.5 text-sm md:text-base tracking-wide whitespace-nowrap rounded-full transition-transform hover:scale-105"
                style={{
                  background: "rgba(0, 0, 0, 0.2)",
                  border: "1px solid rgba(168, 85, 247, 0.45)",
                }}
              >
                <i 
                  className={`bi ${feature.icon} shrink-0`} 
                  style={{ 
                    color: "#A855F7", 
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
