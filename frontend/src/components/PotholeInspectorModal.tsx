import { useState } from 'react';
import { X, AlertTriangle, CheckCircle2, ShieldAlert, Download, Copy, Check, Eye, MapPin, Radio, Clock, Target } from 'lucide-react';

export interface PotholeEvidenceData {
  id: string;
  busId: string;
  count: number;
  time: string;
  confidence: number;
  lat: string;
  lng: string;
  range: number | null;
  lateral: number | null;
  wx: number;
  wy: number;
  evidenceImage?: string | null;
}

interface PotholeInspectorModalProps {
  pothole: PotholeEvidenceData | null;
  onClose: () => void;
}

export default function PotholeInspectorModal({ pothole, onClose }: PotholeInspectorModalProps) {
  const [copied, setCopied] = useState(false);

  if (!pothole) return null;

  const handleCopyGPS = () => {
    navigator.clipboard.writeText(`${pothole.lat}, ${pothole.lng}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!pothole.evidenceImage) return;
    const a = document.createElement('a');
    a.href = pothole.evidenceImage.startsWith('http') || pothole.evidenceImage.startsWith('data:')
      ? pothole.evidenceImage
      : `http://127.0.0.1:8000${pothole.evidenceImage}`;
    a.download = `pothole_evidence_${pothole.id}.jpg`;
    a.click();
  };

  const imgSrc = pothole.evidenceImage
    ? (pothole.evidenceImage.startsWith('http') || pothole.evidenceImage.startsWith('data:')
        ? pothole.evidenceImage
        : `http://127.0.0.1:8000${pothole.evidenceImage}`)
    : null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-none w-full max-w-4xl overflow-hidden shadow-2xl flex flex-col max-h-[92vh] animate-in fade-in zoom-in-95 duration-150">
        {/* Modal Header */}
        <div className="flex items-center justify-between px-4 py-2.5 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 bg-amber-500/20 border border-amber-500 text-amber-400 flex items-center justify-center rounded-none">
              <AlertTriangle className="w-3.5 h-3.5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white leading-tight flex items-center gap-2">
                <span>Pothole Defect Evidence Inspector</span>
                <span className="bg-amber-500/20 border border-amber-400 text-amber-300 text-[9px] font-mono px-1.5 py-0.2 rounded-none flex items-center gap-1">
                  <span className="w-1.5 h-1.5 bg-amber-400 animate-pulse"></span>
                  VERIFIED DEFECT
                </span>
                {pothole.count > 1 && (
                  <span className="bg-sky-500/20 border border-sky-400 text-sky-300 text-[9px] font-mono px-1.5 py-0.2 rounded-none">
                    {pothole.count}x SIGHTINGS
                  </span>
                )}
              </h3>
              <p className="text-[11px] text-slate-400">
                Pothole Hazard ID: <span className="font-mono text-slate-300">{pothole.id}</span>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 hover:bg-slate-800 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-4 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1">
          {/* Left Column: Visual Evidence Frame */}
          <div className="lg:col-span-7 flex flex-col gap-2">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
              <span className="flex items-center gap-1.5">
                <Eye className="w-3.5 h-3.5 text-sky-400" />
                Dashcam Evidence Frame
              </span>
              <span className="text-[10px] font-mono text-emerald-400">
                AI Vision Annotated
              </span>
            </div>

            <div className="relative aspect-video bg-black border border-slate-800 rounded-none overflow-hidden flex items-center justify-center shadow-inner group">
              {imgSrc ? (
                <img
                  src={imgSrc}
                  alt="Pothole Visual Evidence"
                  className="w-full h-full object-contain"
                />
              ) : (
                <div className="text-center p-6 space-y-2">
                  <div className="w-10 h-10 mx-auto bg-slate-800 text-slate-400 flex items-center justify-center border border-slate-700">
                    <ShieldAlert className="w-5 h-5 text-amber-400" />
                  </div>
                  <p className="text-xs font-semibold text-slate-300">Live Dashcam Snapshot Queued</p>
                  <p className="text-[10px] font-mono text-slate-500">Evidence frame recorded by {pothole.busId}</p>
                </div>
              )}

              {/* Watermark Overlay (Positioned top-right to avoid top-left camera HUD) */}
              <div className="absolute top-2.5 right-2.5 bg-slate-950/85 border border-slate-700 text-[10px] font-mono font-medium text-slate-200 px-2.5 py-1 pointer-events-none shadow-md backdrop-blur-xs flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                AI SENSING EVIDENCE • {pothole.busId}
              </div>

              {pothole.range !== null && (
                <div className="absolute bottom-2.5 left-2.5 bg-emerald-950/90 border border-emerald-500/80 text-[10px] font-mono text-emerald-300 px-2.5 py-1 pointer-events-none flex items-center gap-1.5 shadow-md backdrop-blur-xs">
                  <Target className="w-3 h-3 text-emerald-400" />
                  OPTICAL DIST: {pothole.range}m {pothole.lateral !== null ? `(${pothole.lateral > 0 ? '+' : ''}${pothole.lateral}m lateral)` : ''}
                </div>
              )}
            </div>

            {/* Evidence Actions */}
            <div className="flex items-center gap-2 mt-1">
              <button
                onClick={handleDownload}
                disabled={!imgSrc}
                className="flex-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 text-xs py-1.5 px-3 border border-slate-700 font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                <Download className="w-3.5 h-3.5" />
                Download Evidence Frame
              </button>
              <button
                onClick={handleCopyGPS}
                className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs py-1.5 px-3 border border-slate-700 font-semibold flex items-center gap-1.5 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'GPS Copied!' : 'Copy GPS'}
              </button>
            </div>
          </div>

          {/* Right Column: Defect Metadata & Inspection Details */}
          <div className="lg:col-span-5 flex flex-col gap-3">
            <div className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
              Inspection Details
            </div>

            <div className="bg-slate-950 border border-slate-800 p-3 space-y-2.5 text-xs">
              {/* Defect Status */}
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 text-[11px]">Hazard Severity:</span>
                <span className="font-mono font-bold text-rose-400 bg-rose-950/50 border border-rose-800/50 px-2 py-0.5 text-[10px]">
                  CRITICAL DEFECT
                </span>
              </div>

              {/* Confidence */}
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 text-[11px]">AI Confidence:</span>
                <span className="font-mono font-bold text-emerald-400 flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                  {pothole.confidence}% (Multi-Spectral)
                </span>
              </div>

              {/* Sighting Bus */}
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 text-[11px]">Reporting Fleet:</span>
                <span className="font-mono font-semibold text-sky-400">
                  {pothole.busId}
                </span>
              </div>

              {/* Sighting Count */}
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 text-[11px]">Verification Count:</span>
                <span className="font-mono font-bold text-amber-400">
                  {pothole.count} Sightings Logged
                </span>
              </div>

              {/* Closest Range */}
              {pothole.range !== null && (
                <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                  <span className="text-slate-400 text-[11px]">Closest Range:</span>
                  <span className="font-mono font-bold text-white">
                    {pothole.range}m {pothole.lateral !== null ? `(${pothole.lateral > 0 ? '+' : ''}${pothole.lateral}m offset)` : ''}
                  </span>
                </div>
              )}

              {/* Timestamp */}
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 text-[11px]">Sighting Timestamp:</span>
                <span className="font-mono text-slate-300 flex items-center gap-1 text-[11px]">
                  <Clock className="w-3 h-3 text-slate-400" />
                  {pothole.time}
                </span>
              </div>

              {/* GPS Coordinates */}
              <div className="pt-1 space-y-1">
                <div className="text-slate-400 text-[10px] uppercase font-semibold flex items-center gap-1">
                  <MapPin className="w-3 h-3 text-rose-400" />
                  Exact GPS Coordinates
                </div>
                <div className="bg-slate-900 border border-slate-800 p-2 font-mono text-[11px] text-white flex items-center justify-between">
                  <span>{pothole.lat}° N, {pothole.lng}° E</span>
                  <span className="text-[9px] text-slate-500">Coimbatore</span>
                </div>
              </div>

              {/* Simulation Grid Coordinates */}
              <div className="space-y-1">
                <div className="text-slate-400 text-[10px] uppercase font-semibold flex items-center gap-1">
                  <Radio className="w-3 h-3 text-cyan-400" />
                  Simulation Road Grid (sim_x, sim_y)
                </div>
                <div className="bg-slate-900 border border-slate-800 p-2 font-mono text-[11px] text-cyan-300">
                  X: {pothole.wx.toFixed(2)}m, Y: {pothole.wy.toFixed(2)}m
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-4 py-2 border-t border-slate-800 bg-slate-950 flex items-center justify-between text-[11px] text-slate-400 font-mono">
          <span>AI-POWERED ROAD ANOMALY AUDIT TRAIL</span>
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-700 text-white font-sans text-xs px-3 py-1 font-semibold border border-slate-700 transition-colors"
          >
            Close Inspector
          </button>
        </div>
      </div>
    </div>
  );
}
