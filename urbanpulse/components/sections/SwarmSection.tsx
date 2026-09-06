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
        
        {/* INAIVO Logo overlay to hide Gemini watermark */}
        <div className="absolute bottom-[10%] right-[8%] z-20 p-2 rounded-full aspect-square backdrop-blur-sm bg-black/40 flex items-center justify-center scale-125">
          <Image src="/LOGO_INAIVO.png" alt="INAIVO Logo" width={64} height={64} className="object-contain w-auto h-12 opacity-100" />
        </div>

        {/* No overlay — image stays fully vivid. Text shadows handle contrast. */}

        {/* Centered Text Overlay */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-6 z-10 -translate-y-12">

          {/* Eyebrow */}
          <span
            className="inline-block text-[11px] lg:text-[12px] font-bold tracking-[0.22em] uppercase mb-5"
            style={{ color: "#A855F7" }}
          >
            RESILIENT NETWORK
          </span>

          {/* Title */}
          <h2
            className="text-[44px] lg:text-[66px] xl:text-[80px] font-display font-bold leading-[1.05] mb-5"
          >
            <span className="text-white">Urban </span>
            <span style={{ color: "#A855F7" }}>Swarm Mesh</span>
          </h2>

          {/* Subtitle */}
          <p
            className="text-[16px] lg:text-[20px] text-white font-medium leading-[1.6] max-w-xl mb-10"
          >
            A self-connected intelligence network built across the city.
          </p>

          {/* Feature Pills */}
          <div className="flex flex-wrap justify-center gap-2.5 lg:gap-3 max-w-2xl">
            {FEATURES.map((feature, idx) => (
              <div
                key={idx}
                className="flex items-center gap-2 px-4 py-2 rounded-full"
                style={{
                  background: "rgba(0,0,0,0.65)",
                  border: "1px solid rgba(168,85,247,0.45)",
                  backdropFilter: "blur(8px)",
                }}
              >
                <i className={`bi ${feature.icon}`} style={{ color: "#A855F7", fontSize: "13px" }}></i>
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
