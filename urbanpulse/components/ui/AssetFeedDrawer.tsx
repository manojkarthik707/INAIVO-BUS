"use client";

import { SelectedAssetData } from "../three/SelectionHighlight";
import { X, ExternalLink, Activity, ShieldAlert, Cpu, Zap, Radio, ChevronRight } from "lucide-react";

interface AssetFeedDrawerProps {
  asset: SelectedAssetData | null;
  onClose: () => void;
  onQuickSelect?: (id: string) => void;
}

export default function AssetFeedDrawer({ asset, onClose, onQuickSelect }: AssetFeedDrawerProps) {
  if (!asset) {
    return (
      <div className="absolute top-24 left-6 z-40 w-80 p-4 rounded-2xl backdrop-blur-md bg-slate-950/80 border border-cyan-500/20 text-white shadow-2xl transition-all duration-300">
        <div className="flex items-center justify-between pb-3 border-b border-white/10">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-cyan-400 animate-pulse" />
            <span className="text-xs font-mono font-bold tracking-wider text-cyan-400">
              URBAN ASSET FEED
            </span>
          </div>
          <span className="text-[10px] font-mono text-slate-400 px-2 py-0.5 rounded bg-white/5">
            INTERACTIVE
          </span>
        </div>

        <p className="text-xs text-slate-300 my-3 leading-relaxed">
          Click any 3D asset in the scene (<span className="text-cyan-400 font-medium">Vehicle</span>, <span className="text-cyan-400 font-medium">Street Lamp</span>, or <span className="text-cyan-400 font-medium">Building</span>) to inspect live AI telemetry.
        </p>

        <div className="space-y-1.5 pt-1">
          <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-1">
            Featured Assets:
          </span>
          {[
            { id: "truck-dp", label: "Double Parked Van", icon: "🚛", status: "VIOLATION", color: "text-red-400" },
            { id: "lamp-sl-01", label: "Smart Lamp Post S-04", icon: "💡", status: "ACTIVE", color: "text-cyan-400" },
            { id: "building-b1", label: "Residential Tower A", icon: "🏢", status: "MONITORED", color: "text-amber-400" },
            { id: "bus-017", label: "Autonomous Bus 017", icon: "🚌", status: "ACTIVE", color: "text-emerald-400" },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => onQuickSelect?.(item.id)}
              className="w-full flex items-center justify-between px-3 py-2 rounded-xl bg-white/5 hover:bg-cyan-500/15 border border-white/5 hover:border-cyan-500/30 transition-all text-left group"
            >
              <div className="flex items-center gap-2.5">
                <span className="text-sm">{item.icon}</span>
                <span className="text-xs font-medium text-slate-200 group-hover:text-white transition-colors">
                  {item.label}
                </span>
              </div>
              <ChevronRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-400 transition-colors" />
            </button>
          ))}
        </div>
      </div>
    );
  }

  const isViolation = asset.status === "VIOLATION";

  return (
    <div className="absolute top-20 left-6 z-40 max-w-sm w-full transition-all duration-300 animate-in fade-in slide-in-from-left-4">
      {/* ── Outer Card Frame (Designed like the image feed UI) ── */}
      <div 
        className="rounded-2xl p-6 shadow-2xl border transition-all duration-300"
        style={{
          background: "rgba(242, 243, 240, 0.96)",
          borderColor: isViolation ? "rgba(239, 68, 68, 0.4)" : "rgba(0, 212, 255, 0.4)",
          backdropFilter: "blur(16px)",
          boxShadow: isViolation 
            ? "0 20px 40px -15px rgba(239, 68, 68, 0.3)" 
            : "0 20px 40px -15px rgba(0, 212, 255, 0.25)"
        }}
      >
        {/* Card Top Banner */}
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2">
              <h3 
                className="text-lg font-black tracking-tight font-heading uppercase"
                style={{ color: isViolation ? "#2563eb" : "#0284c7" }}
              >
                {asset.name}
              </h3>
              <span className="text-sm text-slate-400 font-bold">+</span>
            </div>
            <div className="flex items-center gap-2 mt-1">
              <span 
                className="text-[10px] font-mono font-bold tracking-widest uppercase px-2 py-0.5 rounded"
                style={{
                  background: isViolation ? "rgba(239, 68, 68, 0.15)" : "rgba(14, 165, 233, 0.15)",
                  color: isViolation ? "#dc2626" : "#0369a1",
                  border: `1px solid ${isViolation ? "#fca5a5" : "#7dd3fc"}`
                }}
              >
                {asset.status}
              </span>
              <span className="text-[11px] font-mono text-slate-500 font-semibold">
                {asset.category}
              </span>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-full bg-slate-200/80 hover:bg-slate-300 text-slate-600 hover:text-slate-900 transition-colors"
            aria-label="Close feed"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Narrative Description (matching screenshot) */}
        <p className="text-xs text-slate-700 leading-relaxed font-normal mb-4 font-sans">
          {asset.description}
        </p>

        {/* Telemetry Metrics Grid */}
        <div className="grid grid-cols-2 gap-2 mb-4">
          {asset.metrics.map((m, i) => (
            <div 
              key={i} 
              className="p-2.5 rounded-xl bg-slate-100/90 border border-slate-200/80 flex flex-col justify-between"
            >
              <span className="text-[10px] font-mono uppercase text-slate-500 font-semibold tracking-wider">
                {m.label}
              </span>
              <span className="text-xs font-mono font-bold text-slate-900 mt-1">
                {m.value}
              </span>
            </div>
          ))}
        </div>

        {/* Bullet details list */}
        {asset.details.length > 0 && (
          <div className="space-y-1.5 mb-5 border-t border-slate-200 pt-3">
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider block font-bold">
              AI Insight & Event Logs
            </span>
            {asset.details.map((detail, idx) => (
              <div key={idx} className="flex items-start gap-2 text-[11px] text-slate-700">
                <span className="text-cyan-600 font-bold mt-0.5">•</span>
                <span>{detail}</span>
              </div>
            ))}
          </div>
        )}

        {/* Action Button CTA (matches "LEARN MORE ->" green pill in Image 2) */}
        <button
          onClick={() => alert(`Inspection opened for asset: ${asset.name}`)}
          className="w-full flex items-center justify-between px-5 py-3 rounded-full text-xs font-bold tracking-wider uppercase transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] shadow-md"
          style={{
            background: isViolation
              ? "linear-gradient(135deg, #059669 0%, #0d9488 100%)"
              : "linear-gradient(135deg, #0284c7 0%, #0d9488 100%)",
            color: "white",
            boxShadow: "0 4px 15px rgba(13, 148, 136, 0.35)",
          }}
        >
          <span>LEARN MORE</span>
          <span className="text-sm font-bold">→</span>
        </button>
      </div>
    </div>
  );
}
