"use client";

import { SelectedAssetData } from "../three/SelectionHighlight";
import { X, Activity, ChevronRight, Wifi, AlertTriangle, CheckCircle2, Circle } from "lucide-react";

interface AssetFeedDrawerProps {
  asset: SelectedAssetData | null;
  onClose: () => void;
  onQuickSelect?: (id: string) => void;
}

const QUICK_ASSETS = [
  { id: "truck-dp",     label: "Double Parked Van",    icon: "bi-truck",            status: "VIOLATION", color: "#ef4444" },
  { id: "lamp-sl-01",  label: "Smart Lamp Post S-04",  icon: "bi-lightbulb-fill",   status: "ACTIVE",    color: "#22d3ee" },
  { id: "building-b1", label: "Residential Tower A",   icon: "bi-building-fill",    status: "MONITORED", color: "#f59e0b" },
  { id: "bus-017",     label: "Autonomous Bus 017",     icon: "bi-bus-front-fill",   status: "ACTIVE",    color: "#10b981" },
];

function StatusDot({ status }: { status: string }) {
  const color =
    status === "VIOLATION" ? "#ef4444"
    : status === "ACTIVE"   ? "#10b981"
    : status === "MONITORED"? "#f59e0b"
    : "#94a3b8";
  return (
    <span
      className="inline-block w-2 h-2 rounded-full animate-pulse"
      style={{ background: color, boxShadow: `0 0 6px ${color}` }}
    />
  );
}

export default function AssetFeedDrawer({ asset, onClose, onQuickSelect }: AssetFeedDrawerProps) {

  /* ─── Empty state ─── */
  if (!asset) {
    return (
      <div className="absolute top-24 left-6 z-40 w-[300px]">
        <div
          className="rounded-2xl overflow-hidden border"
          style={{
            background: "rgba(6, 10, 18, 0.88)",
            borderColor: "rgba(34, 211, 238, 0.18)",
            backdropFilter: "blur(20px)",
            boxShadow: "0 24px 60px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04) inset",
          }}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/[0.06]">
            <div className="flex items-center gap-2">
              <Activity className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
              <span className="text-[10px] font-mono font-bold tracking-[0.18em] text-cyan-400 uppercase">
                Urban Asset Feed
              </span>
            </div>
            <span
              className="text-[9px] font-mono font-bold tracking-widest uppercase px-2 py-0.5 rounded-full"
              style={{ background: "rgba(34,211,238,0.1)", color: "#22d3ee", border: "1px solid rgba(34,211,238,0.2)" }}
            >
              LIVE
            </span>
          </div>

          {/* Instruction */}
          <div className="px-4 py-3 border-b border-white/[0.06]">
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Click any{" "}
              <span className="text-cyan-400 font-semibold">vehicle</span>,{" "}
              <span className="text-cyan-400 font-semibold">lamp</span> or{" "}
              <span className="text-cyan-400 font-semibold">building</span>{" "}
              in the 3D scene to inspect live AI telemetry.
            </p>
          </div>

          {/* Quick select assets */}
          <div className="px-4 py-3">
            <span className="text-[9px] font-mono font-bold tracking-[0.16em] text-slate-500 uppercase block mb-2.5">
              Featured Assets
            </span>
            <div className="space-y-1.5">
              {QUICK_ASSETS.map((item) => (
                <button
                  key={item.id}
                  onClick={() => onQuickSelect?.(item.id)}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition-all text-left group"
                  style={{
                    background: "rgba(255,255,255,0.03)",
                    border: "1px solid rgba(255,255,255,0.06)",
                  }}
                  onMouseEnter={e => {
                    (e.currentTarget as HTMLElement).style.background = `rgba(${item.color === "#ef4444" ? "239,68,68" : item.color === "#22d3ee" ? "34,211,238" : item.color === "#f59e0b" ? "245,158,11" : "16,185,129"},0.08)`;
                    (e.currentTarget as HTMLElement).style.borderColor = `${item.color}30`;
                  }}
                  onMouseLeave={e => {
                    (e.currentTarget as HTMLElement).style.background = "rgba(255,255,255,0.03)";
                    (e.currentTarget as HTMLElement).style.borderColor = "rgba(255,255,255,0.06)";
                  }}
                >
                  <div className="flex items-center gap-2.5">
                    <div
                      className="w-7 h-7 rounded-lg flex items-center justify-center text-[13px]"
                      style={{ background: `${item.color}15`, color: item.color }}
                    >
                      <i className={`bi ${item.icon}`}></i>
                    </div>
                    <div>
                      <div className="text-[11px] font-semibold text-slate-200">{item.label}</div>
                      <div className="flex items-center gap-1 mt-0.5">
                        <StatusDot status={item.status} />
                        <span className="text-[9px] font-mono" style={{ color: item.color }}>{item.status}</span>
                      </div>
                    </div>
                  </div>
                  <ChevronRight className="w-3.5 h-3.5 text-slate-600 group-hover:text-slate-400 transition-colors flex-shrink-0" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  /* ─── Selected asset state ─── */
  const isViolation = asset.status === "VIOLATION";
  const accentColor = isViolation ? "#ef4444" : "#22d3ee";
  const accentRgb   = isViolation ? "239,68,68" : "34,211,238";

  return (
    <div className="absolute top-20 left-6 z-40 w-[300px]">
      <div
        className="rounded-2xl overflow-hidden border"
        style={{
          background: "rgba(6, 10, 18, 0.92)",
          borderColor: `rgba(${accentRgb}, 0.22)`,
          backdropFilter: "blur(24px)",
          boxShadow: `0 24px 60px rgba(0,0,0,0.65), 0 0 30px rgba(${accentRgb},0.06), 0 0 0 1px rgba(255,255,255,0.04) inset`,
        }}
      >
        {/* ── Header bar ── */}
        <div
          className="flex items-center justify-between px-4 py-3 border-b"
          style={{ borderColor: `rgba(${accentRgb},0.12)` }}
        >
          <div className="flex items-center gap-2">
            <StatusDot status={asset.status} />
            <span className="text-[10px] font-mono font-bold tracking-[0.16em] uppercase" style={{ color: accentColor }}>
              {asset.category}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span
              className="text-[9px] font-mono font-bold tracking-widest uppercase px-2 py-0.5 rounded-full"
              style={{
                background: `rgba(${accentRgb},0.12)`,
                color: accentColor,
                border: `1px solid rgba(${accentRgb},0.25)`,
              }}
            >
              {asset.status}
            </span>
            <button
              onClick={onClose}
              className="w-6 h-6 rounded-full flex items-center justify-center transition-colors"
              style={{ background: "rgba(255,255,255,0.06)", color: "#94a3b8" }}
              onMouseEnter={e => (e.currentTarget.style.background = "rgba(255,255,255,0.12)")}
              onMouseLeave={e => (e.currentTarget.style.background = "rgba(255,255,255,0.06)")}
              aria-label="Close"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* ── Asset name ── */}
        <div className="px-4 pt-3 pb-2">
          <h3 className="text-[17px] font-display font-bold text-white leading-tight tracking-tight">
            {asset.name}
          </h3>
          <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">{asset.description}</p>
        </div>

        {/* ── Metrics grid ── */}
        <div className="px-4 pb-3">
          <div className="grid grid-cols-2 gap-2">
            {asset.metrics.map((m, i) => (
              <div
                key={i}
                className="rounded-xl px-3 py-2.5"
                style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)" }}
              >
                <div className="text-[9px] font-mono uppercase tracking-wider text-slate-500 mb-1">{m.label}</div>
                <div className="text-[13px] font-mono font-bold text-white">{m.value}</div>
              </div>
            ))}
          </div>
        </div>

        {/* ── AI Insight logs ── */}
        {asset.details.length > 0 && (
          <div
            className="px-4 py-3 border-t"
            style={{ borderColor: "rgba(255,255,255,0.06)" }}
          >
            <span className="text-[9px] font-mono font-bold tracking-[0.16em] text-slate-500 uppercase block mb-2.5">
              AI Insight Log
            </span>
            <div className="space-y-2">
              {asset.details.map((detail, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <div
                    className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0"
                    style={{ background: accentColor, boxShadow: `0 0 4px ${accentColor}` }}
                  />
                  <span className="text-[11px] text-slate-300 leading-relaxed">{detail}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── CTA ── */}
        <div className="px-4 pb-4 pt-2">
          <button
            onClick={() => alert(`Inspection opened for asset: ${asset.name}`)}
            className="w-full flex items-center justify-between px-4 py-2.5 rounded-xl text-[11px] font-bold tracking-wider uppercase transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
            style={{
              background: `linear-gradient(135deg, rgba(${accentRgb},0.2) 0%, rgba(${accentRgb},0.08) 100%)`,
              border: `1px solid rgba(${accentRgb},0.3)`,
              color: accentColor,
            }}
          >
            <span>Inspect Asset</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
