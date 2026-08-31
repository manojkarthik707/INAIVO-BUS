"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import SectionHeader from "@/components/layout/SectionHeader";

const LAYERS = [
  {
    id: "cameras",
    label: "Camera Sources",
    color: "#00d4ff",
    items: [
      "Bus Front / Rear / Side Camera",
      "Fixed Junction Camera",
      "Existing City CCTV",
      "Roadside AI Camera",
      "Municipal Fleet Camera",
    ],
  },
  {
    id: "edge",
    label: "Edge / Camera AI",
    color: "#4488ff",
    items: [
      "Object Detection (YOLO-family)",
      "Multi-object Tracking (ByteTrack)",
      "Semantic Segmentation",
      "ANPR / OCR Pipeline",
      "Camera Health Check",
      "Privacy Filtering (PII mask)",
      "Event Packaging",
    ],
  },
  {
    id: "connectivity",
    label: "Connectivity Layer",
    color: "#8855ff",
    items: [
      "Live metadata stream",
      "Store-and-forward queue",
      "Event-triggered clip upload",
      "MQTT / WebSocket transport",
      "Encrypted secure channel",
    ],
  },
  {
    id: "central",
    label: "Central Intelligence",
    color: "#ff8800",
    items: [
      "Event normalization",
      "Spatiotemporal clustering",
      "Duplicate suppression",
      "Fleet consensus engine",
      "Vehicle Re-ID",
      "Evidence graph builder",
      "Urban Object Registry",
      "Agentic orchestration",
    ],
  },
  {
    id: "geo",
    label: "Geospatial / 4D Twin",
    color: "#00ff88",
    items: [
      "PostGIS road segment state",
      "GIS / OpenStreetMap base",
      "Congestion heat maps",
      "Event history timeline",
      "Coverage freshness map",
      "Semantic urban twin",
    ],
  },
  {
    id: "action",
    label: "Action Layer",
    color: "#ffaa00",
    items: [
      "Real-time alerts",
      "Incident review queue",
      "Municipal work orders",
      "Infrastructure prioritization",
      "Traffic insights dashboard",
      "Repair verification",
    ],
  },
];

const TECH_STACK = [
  { cat: "AI / Vision", items: ["PyTorch", "YOLO", "ByteTrack", "ANPR", "ONNX/TensorRT"] },
  { cat: "Edge", items: ["Jetson-class hardware", "Local inference service", "Event queue", "Encrypted buffer"] },
  { cat: "Backend", items: ["FastAPI", "PostgreSQL", "PostGIS", "Redis", "WebSocket"] },
  { cat: "Geospatial", items: ["PostGIS", "OpenStreetMap", "MapLibre / deck.gl"] },
  { cat: "Frontend", items: ["Next.js", "React", "TypeScript", "Three.js", "GSAP"] },
];

export default function ArchitectureSection() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        ".arch-layer",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.5, stagger: 0.1,
          scrollTrigger: { trigger: ".arch-stack", start: "top 80%" },
        }
      );
      gsap.fromTo(
        ".arch-header",
        { opacity: 0, y: 30 },
        {
          opacity: 1, y: 0, duration: 0.8,
          scrollTrigger: { trigger: sectionRef.current, start: "top 80%" },
        }
      );
    }, sectionRef);
    return () => ctx.revert();
  }, []);

  return (
    <Section
      ref={sectionRef as any}
      id="architecture"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-[1px]"
        style={{ background: "linear-gradient(90deg, transparent, #ff8800, transparent)" }}
      />

      <PageContainer>
        <div className="arch-header">
          <SectionHeader
            eyebrow="SYSTEM ARCHITECTURE"
            title={
              <>
                Six Layers. <span className="gradient-text">One Platform.</span>
              </>
            }
            description="From camera to city action — every component has a clear role. Edge-first. Privacy-aware. Built for BEL's smart-city ecosystem."
          />
        </div>

        {/* Architecture stack */}
        <div className="arch-stack flex flex-col items-center space-y-0 w-full mb-20">
          {LAYERS.map((layer, i) => {
            // Hex to RGB conversion for transparent backgrounds
            let r = 0, g = 0, b = 0;
            if (layer.color.length === 7) {
              r = parseInt(layer.color.substring(1, 3), 16);
              g = parseInt(layer.color.substring(3, 5), 16);
              b = parseInt(layer.color.substring(5, 7), 16);
            }

            return (
              <div key={layer.id} className="flex flex-col items-center w-full max-w-6xl">
                <div
                  className="arch-layer w-full opacity-0 p-6 md:p-8 rounded-3xl group transition-all duration-300 hover:scale-[1.01]"
                  style={{
                    background: `rgba(${r}, ${g}, ${b}, 0.05)`,
                    border: `1px solid ${layer.color}33`,
                    boxShadow: `0 8px 32px rgba(0,0,0,0.2)`
                  }}
                >
                  <div className="grid grid-cols-1 md:grid-cols-[220px_minmax(0,1fr)] gap-6 md:gap-8 items-start md:items-center">
                    <div className="flex-shrink-0">
                      <div className="flex items-center gap-2 mb-1">
                        <div
                          className="w-2.5 h-2.5 rounded-full"
                          style={{ background: layer.color }}
                        />
                        <span className="font-heading font-semibold text-lg" style={{ color: layer.color }}>
                          {layer.label}
                        </span>
                      </div>
                      <div className="label-text text-text-muted mt-2">
                        Layer {i + 1} of {LAYERS.length}
                      </div>
                    </div>
                    
                    <div className="flex flex-wrap gap-3">
                      {layer.items.map((item) => (
                        <span
                          key={item}
                          className="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
                          style={{
                            background: "rgba(255,255,255,0.04)",
                            border: "1px solid rgba(255,255,255,0.08)",
                            color: "var(--text-primary)",
                          }}
                        >
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                {i < LAYERS.length - 1 && (
                  <div className="flex justify-center py-2">
                    <div
                      className="w-[2px] h-6"
                      style={{ background: `linear-gradient(to bottom, ${layer.color}, ${LAYERS[i+1].color})` }}
                    />
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Tech stack */}
        <div className="max-w-6xl mx-auto">
          <h3 className="font-heading font-semibold text-sm text-center mb-8 text-text-secondary tracking-widest uppercase">
            Technical Stack
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {TECH_STACK.map((cat) => (
              <div
                key={cat.cat}
                className="p-5 rounded-2xl glass-card h-full"
              >
                <div className="label-text mb-4 font-bold" style={{ color: "var(--accent-cyan)" }}>
                  {cat.cat}
                </div>
                <ul className="flex flex-col gap-2">
                  {cat.items.map((item) => (
                    <li
                      key={item}
                      className="text-sm text-text-secondary pb-2 border-b border-white/5 last:border-0 last:pb-0"
                    >
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
