"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import Image from "next/image";

const COLUMNS = [
  {
    id: "mesh",
    eyebrow: "RESILIENT NETWORK",
    eyebrowColor: "#A855F7",
    titleStart: "Urban",
    titleEnd: "Swarm Mesh",
    titleEndColor: "#A855F7",
    description: "A self-connected intelligence network built across the city.",
    image: "/FINAL PHOTO FOR URBAN MESH.png",
    features: [
      { icon: "bi-diagram-2-fill", text: "Peer-to-Peer Connectivity", color: "#A855F7" },
      { icon: "bi-wifi-off", text: "Works in Low Connectivity", color: "#A855F7" },
      { icon: "bi-signpost-split-fill", text: "Dynamic Data Routing", color: "#A855F7" },
      { icon: "bi-shield-check", text: "Self-Healing Network", color: "#A855F7" },
    ],
  },
  {
    id: "cctv",
    eyebrow: "FIXED VISION",
    eyebrowColor: "#00d4ff",
    titleStart: "CCTV",
    titleEnd: "Cameras",
    titleEndColor: "#00d4ff",
    description: "Continuous intelligence from fixed urban viewpoints.",
    image: "/FINAL PHOTO FOR CCTV.png",
    features: [
      { icon: "bi-clock-history", text: "24/7 Urban Monitoring", color: "#00d4ff" },
      { icon: "bi-car-front-fill", text: "Traffic & Violation Detection", color: "#00d4ff" },
      { icon: "bi-exclamation-triangle-fill", text: "Incident & Anomaly Detection", color: "#00d4ff" },
      { icon: "bi-bell-fill", text: "Real-Time Alerts", color: "#00d4ff" },
    ],
  },
  {
    id: "dashcams",
    eyebrow: "MOBILE VISION",
    eyebrowColor: "#F59E0B",
    titleStart: "Bus",
    titleEnd: "Dashcams",
    titleEndColor: "#F59E0B",
    description: "Turn moving public transport into intelligent city sensors.",
    image: "/FINAL PHOTO FOR DASHCAM ANALYSIS.png",
    features: [
      { icon: "bi-camera-video-fill", text: "Moving-Camera Intelligence", color: "#F59E0B" },
      { icon: "bi-cpu-fill", text: "On-Bus Edge AI", color: "#F59E0B" },
      { icon: "bi-geo-alt-fill", text: "Geo-Tagged Event Detection", color: "#F59E0B" },
      { icon: "bi-bar-chart-fill", text: "Multi-Bus Evidence Fusion", color: "#F59E0B" },
    ],
  },
];

export default function ThreeCameraLayersSection() {
  return (
    <Section id="system" style={{ background: "var(--bg-base)" }}>
      <PageContainer>
        {/* Header Section */}
        <div className="flex flex-col items-center justify-center text-center mb-12">
          <span className="text-[10px] md:text-xs font-bold tracking-[0.25em] text-text-secondary uppercase mb-4">
            SMART CITIES. REAL IMPACT.
          </span>
          <h2 className="text-3xl md:text-5xl font-display font-bold mb-4 tracking-tight">
            Multiple Perspectives. <span style={{ color: "#A855F7" }}>A Safer Tomorrow.</span>
          </h2>
          <p className="text-sm md:text-base text-text-secondary max-w-2xl mx-auto">
            INETRA integrates connected vehicles, fixed cameras and public transport sensors
            to create a resilient and intelligent urban network.
          </p>
        </div>

        {/* 3-Column Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 xl:gap-8 items-stretch w-full">
          {COLUMNS.map((col) => (
            <div
              key={col.id}
              className="flex flex-col rounded-3xl overflow-hidden glass-card h-full transition-transform duration-300 hover:scale-[1.02]"
              style={{
                background: "rgba(10, 15, 25, 0.4)",
                border: `1px solid ${col.eyebrowColor}33`,
                boxShadow: `0 8px 32px rgba(0,0,0,0.15)`,
              }}
            >
              {/* Image Container */}
              <div className="relative w-full aspect-[4/3] md:aspect-[16/9] lg:aspect-[4/3] overflow-hidden border-b" style={{ borderColor: `${col.eyebrowColor}22` }}>
                <Image
                  src={col.image}
                  alt={`${col.titleStart} ${col.titleEnd}`}
                  fill
                  className="object-cover object-center"
                  sizes="(max-width: 1024px) 100vw, 33vw"
                  quality={90}
                />
                {/* Gradient overlay for smooth transition */}
                <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#0a0f19] to-transparent" />
                
                {/* INAIVO Logo overlay to hide Gemini watermark */}
                <div className="absolute bottom-[10%] right-[8%] z-20 p-2 rounded-full aspect-square backdrop-blur-sm bg-black/40 flex items-center justify-center scale-125">
                  <Image src="/LOGO_INAIVO.png" alt="INAIVO Logo" width={64} height={64} className="object-contain w-auto h-8 md:h-10 opacity-100" />
                </div>
              </div>

              {/* Content Container */}
              <div className="flex flex-col flex-grow p-6 md:p-8 items-center text-center -mt-8 relative z-10">
                <span
                  className="text-[10px] md:text-xs font-bold tracking-[0.2em] uppercase mb-3"
                  style={{ color: col.eyebrowColor }}
                >
                  {col.eyebrow}
                </span>
                
                <h3 className="text-2xl md:text-3xl font-display font-bold mb-3">
                  <span className="text-white">{col.titleStart} </span>
                  <span style={{ color: col.titleEndColor }}>{col.titleEnd}</span>
                </h3>
                
                <p className="text-sm text-text-secondary font-medium leading-relaxed mb-8 flex-grow">
                  {col.description}
                </p>

                {/* Feature Pills */}
                <div className="w-full flex flex-col gap-5 mt-auto pb-4">
                  {col.features.map((feature, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-4 px-5 py-3.5 rounded-full w-full justify-start transition-colors"
                      style={{
                        background: "rgba(0,0,0,0.5)",
                        border: `1px solid ${col.eyebrowColor}40`,
                      }}
                    >
                      <i className={`bi ${feature.icon}`} style={{ color: feature.color, fontSize: "16px" }} />
                      <span className="text-[13px] md:text-sm font-semibold text-white/90 truncate">
                        {feature.text}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </PageContainer>
    </Section>
  );
}
