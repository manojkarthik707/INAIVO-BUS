"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import { Camera, Cpu, Search, Network, Zap, Shield, AlertTriangle } from "lucide-react";

export default function ContextSection() {
  return (
    <Section id="platform" className="bg-[var(--bg-secondary)] text-white relative min-h-screen flex items-center py-12">
      {/* Subtle texture */}
      <div className="bg-texture" />

      <PageContainer className="relative z-10 w-full">
        {/* Title */}
        <div className="text-center mb-12">
          <span className="inline-block text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--blue)] mb-4">
            CONNECTED INTELLIGENCE
          </span>
          <h2 className="text-[40px] md:text-[56px] font-display font-bold text-white leading-[1.1] tracking-tight">
            Cities have cameras.<br />
            <span className="text-[var(--text-muted)]">They don&apos;t have </span>
            <span className="text-[var(--blue)]">connected intelligence.</span>
          </h2>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 items-stretch max-w-5xl mx-auto">
          
          {/* Left: The Problem */}
          <div className="premium-card !p-8 flex flex-col justify-center relative overflow-hidden group border-red-500/10 hover:border-red-500/30 transition-colors">
             <div className="absolute top-0 right-0 w-64 h-64 bg-red-500/5 rounded-full blur-3xl group-hover:bg-red-500/10 transition-colors" />
             
             <h3 className="text-xl md:text-2xl font-display font-bold mb-8 text-white flex items-center gap-3">
                <AlertTriangle className="text-red-400 w-6 h-6" /> The Problem
             </h3>
             
             <div className="space-y-6 relative z-10">
                <div className="flex items-start gap-4">
                   <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center shrink-0 border border-red-500/20">
                     <Camera className="text-red-400 w-5 h-5" />
                   </div>
                   <div>
                     <h4 className="font-bold text-slate-200 text-sm md:text-base">Fragmented Cameras</h4>
                     <p className="text-xs md:text-sm text-slate-400 mt-1 leading-relaxed">Isolated video feeds lack cross-communication, leaving blind spots.</p>
                   </div>
                </div>
                <div className="flex items-start gap-4">
                   <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center shrink-0 border border-red-500/20">
                     <Search className="text-red-400 w-5 h-5" />
                   </div>
                   <div>
                     <h4 className="font-bold text-slate-200 text-sm md:text-base">Isolated Systems</h4>
                     <p className="text-xs md:text-sm text-slate-400 mt-1 leading-relaxed">Data gets stuck in organizational silos, missing the broader context.</p>
                   </div>
                </div>
                <div className="flex items-start gap-4">
                   <div className="w-10 h-10 rounded-lg bg-red-500/10 flex items-center justify-center shrink-0 border border-red-500/20">
                     <Zap className="text-red-400 w-5 h-5" />
                   </div>
                   <div>
                     <h4 className="font-bold text-slate-200 text-sm md:text-base">Slow Response Time</h4>
                     <p className="text-xs md:text-sm text-slate-400 mt-1 leading-relaxed">Manual monitoring inherently delays critical emergency actions.</p>
                   </div>
                </div>
             </div>
          </div>

          {/* Right: The Solution Architecture */}
          <div className="premium-card !p-8 flex flex-col justify-center relative overflow-hidden group border-blue-500/10 hover:border-blue-500/30 transition-colors">
             <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl group-hover:bg-blue-500/10 transition-colors" />
             
             <h3 className="text-xl md:text-2xl font-display font-bold mb-4 text-white flex items-center gap-3">
                <Shield className="text-blue-400 w-6 h-6" /> The Solution
             </h3>
             <p className="text-sm text-slate-400 mb-8 max-w-sm relative z-10 leading-relaxed">
                A unified edge architecture designed to turn passive observation into immediate, coordinated action.
             </p>
             
             {/* Architecture cascade Grid */}
             <div className="grid grid-cols-3 gap-y-8 gap-x-4 relative z-10">
                <div className="flex flex-col items-center text-center gap-3 group/item">
                   <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center group-hover/item:border-blue-400/50 group-hover/item:text-blue-400 transition-colors">
                     <Camera className="w-5 h-5 text-slate-400 group-hover/item:text-blue-400 transition-colors" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-slate-300">Vision</span>
                </div>
                <div className="flex flex-col items-center text-center gap-3 group/item">
                   <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center group-hover/item:border-blue-400/50 group-hover/item:text-blue-400 transition-colors">
                     <Cpu className="w-5 h-5 text-slate-400 group-hover/item:text-blue-400 transition-colors" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-slate-300">Edge AI</span>
                </div>
                <div className="flex flex-col items-center text-center gap-3 group/item">
                   <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center group-hover/item:border-violet-400/50 group-hover/item:text-violet-400 transition-colors">
                     <Network className="w-5 h-5 text-slate-400 group-hover/item:text-violet-400 transition-colors" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-slate-300">Fusion</span>
                </div>
                <div className="flex flex-col items-center text-center gap-3 group/item">
                   <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center group-hover/item:border-violet-400/50 group-hover/item:text-violet-400 transition-colors">
                     <Search className="w-5 h-5 text-slate-400 group-hover/item:text-violet-400 transition-colors" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-slate-300">Event</span>
                </div>
                <div className="flex flex-col items-center text-center gap-3 group/item">
                   <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center group-hover/item:border-emerald-400/50 group-hover/item:text-emerald-400 transition-colors">
                     <Zap className="w-5 h-5 text-slate-400 group-hover/item:text-emerald-400 transition-colors" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-slate-300">Alert</span>
                </div>
                <div className="flex flex-col items-center text-center gap-3">
                   <div className="w-12 h-12 rounded-xl bg-blue-600 shadow-[0_0_20px_rgba(37,99,235,0.4)] flex items-center justify-center border border-blue-400">
                     <Shield className="w-5 h-5 text-white" />
                   </div>
                   <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400">Response</span>
                </div>
             </div>
          </div>

        </div>
      </PageContainer>
    </Section>
  );
}
