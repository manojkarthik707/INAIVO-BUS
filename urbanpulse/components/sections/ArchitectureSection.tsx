"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

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
    <section
      ref={sectionRef}
      id="architecture"
      className="relative py-32"
      style={{ background: "var(--bg-surface)" }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: "linear-gradient(90deg, transparent, #ff8800, transparent)" }}
      />

      <div className="max-w-7xl mx-auto px-6 md:px-12">
        <div className="arch-header text-center mb-16">
          <div
            className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full"
            style={{ background: "rgba(255,136,0,0.08)", border: "1px solid rgba(255,136,0,0.25)" }}
          >
            <span className="label-text" style={{ color: "#ff8800" }}>System Architecture</span>
          </div>
          <h2 className="font-heading text-4xl md:text-5xl font-bold mb-5" style={{ color: "var(--text-primary)" }}>
            Six Layers. <span className="gradient-text">One Platform.</span>
          </h2>
          <p className="text-lg max-w-2xl mx-auto" style={{ color: "var(--text-secondary)" }}>
            From camera to city action — every component has a clear role.
            Edge-first. Privacy-aware. Built for BEL&apos;s smart-city ecosystem.
          </p>
        </div>

        {/* Architecture stack */}
        <div className="arch-stack flex flex-col items-center space-y-0 w-full mb-20">
          {LAYERS.map((layer, i) => (
            <div key={layer.id} className="flex flex-col items-center w-full">
              <div
                className="arch-layer w-full opacity-0 p-6 rounded-2xl group transition-all duration-300 hover:scale-[1.01]"
                style={{
                  background: `rgba(${layer.color.replace("#", "").match(/.{2}/g)?.map(h=>parseInt(h,16)).join(",")}, 0.05)`,
                  border: `1px solid ${layer.color}22`,
                }}
              >
                <div className="flex flex-wrap items-start gap-6">
                <div className="flex-shrink-0 w-48">
                  <div className="flex items-center gap-2 mb-1">
                    <div
                      className="w-2 h-2 rounded-full"
                      style={{ background: layer.color }}
                    />
                    <span className="font-heading font-semibold text-sm" style={{ color: layer.color }}>
                      {layer.label}
                    </span>
                  </div>
                  <div className="label-text" style={{ color: "var(--text-muted)" }}>
                    Layer {i + 1} of {LAYERS.length}
                  </div>
                </div>
                <div className="flex-1 flex flex-wrap gap-2">
                  {layer.items.map((item) => (
                    <span
                      key={item}
                      className="px-3 py-1.5 rounded-lg text-xs"
                      style={{
                        background: "rgba(255,255,255,0.04)",
                        border: "1px solid rgba(255,255,255,0.08)",
                        color: "var(--text-secondary)",
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
                    className="w-px h-6"
                    style={{ background: `linear-gradient(to bottom, ${layer.color}, ${LAYERS[i+1].color})` }}
                  />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Tech stack */}
        <div>
          <h3 className="font-heading font-semibold text-sm text-center mb-8" style={{ color: "var(--text-secondary)" }}>
            TECHNICAL STACK
          </h3>
          <div className="grid md:grid-cols-5 gap-4">
            {TECH_STACK.map((cat) => (
              <div
                key={cat.cat}
                className="p-4 rounded-xl"
                style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}
              >
                <div className="label-text mb-3" style={{ color: "var(--accent-cyan)" }}>
                  {cat.cat}
                </div>
                {cat.items.map((item) => (
                  <div
                    key={item}
                    className="text-xs py-1"
                    style={{ color: "var(--text-secondary)", borderBottom: "1px solid rgba(255,255,255,0.04)" }}
                  >
                    {item}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
