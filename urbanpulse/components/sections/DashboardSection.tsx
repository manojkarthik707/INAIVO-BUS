"use client";

import Section from "@/components/layout/Section";
import PageContainer from "@/components/layout/PageContainer";
import Image from "next/image";

export default function DashboardSection() {
  return (
    <Section id="dashboard" className="bg-[var(--bg-main)] text-white">
      <PageContainer>
        <div className="flex flex-col items-center text-center mb-16 max-w-3xl mx-auto">
          <span className="inline-block text-[13px] font-bold tracking-[0.14em] uppercase text-[var(--blue)] mb-4">
            CITY INTELLIGENCE COMMAND CENTER
          </span>
          <h2 className="text-[42px] lg:text-[56px] font-display font-bold text-white mb-6 leading-[1.05]">
            Everything, everywhere. <br className="hidden md:block" />
            <span className="text-[var(--text-muted)]">All at once.</span>
          </h2>
          <p className="text-[17px] md:text-[18px] text-[var(--text-secondary)] leading-[1.65] font-normal">
            A centralized dashboard that aggregates live feeds from dashcams, CCTV, and drone nodes. Monitor the pulse of the city in real-time.
          </p>
        </div>

        {/* Dashboard UI Wrapper */}
        <div className="relative w-full max-w-[1400px] mx-auto rounded-[24px] border border-white/10 bg-[var(--surface)] shadow-[0_30px_100px_rgba(0,0,0,0.8)] overflow-hidden">
          
          {/* Dashboard Header Bar */}
          <div className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-[var(--surface-hover)]">
            <div className="flex items-center gap-4">
               <div className="flex gap-2">
                 <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                 <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                 <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
               </div>
               <div className="h-4 w-[1px] bg-white/10"></div>
               <span className="font-mono text-[13px] text-gray-400">URBANPULSE / LIVE DASHBOARD</span>
            </div>
            <div className="flex items-center gap-6 text-[13px] font-mono text-[var(--text-muted)]">
               <div className="flex items-center gap-2">
                 <span className="w-2 h-2 rounded-full bg-[var(--success)] animate-pulse shadow-[0_0_8px_var(--success)]"></span>
                 SYS: ONLINE
               </div>
               <span>{new Date().toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' })} UTC</span>
            </div>
          </div>

          {/* Dashboard Grid Content */}
          <div className="p-6 grid grid-cols-1 md:grid-cols-12 gap-6">
            
            {/* Main Video Feed Area */}
            <div className="md:col-span-8 flex flex-col gap-6">
               <div className="relative w-full aspect-video rounded-[16px] overflow-hidden bg-black border border-white/10">
                 <Image src="/dashcam analysis.png" fill className="object-cover opacity-80" alt="Main Feed" />
                 
                 {/* Feed Overlays */}
                 <div className="absolute top-4 left-4 flex gap-2">
                   <div className="bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded">REC</div>
                   <div className="bg-black/50 backdrop-blur text-white text-[10px] font-mono px-2 py-1 rounded border border-white/10">CAM_DASH_02</div>
                 </div>
                 
                 {/* Bounding Box Simulation */}
                 <div className="absolute top-[30%] left-[40%] w-[120px] h-[80px] border-2 border-[var(--danger)] bg-[var(--danger)]/10 rounded-sm">
                   <div className="absolute -top-6 left-[-2px] bg-[var(--danger)] text-white text-[10px] font-bold px-1.5 py-0.5 whitespace-nowrap">
                     ILLEGAL PARKING 94%
                   </div>
                 </div>

                 <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur rounded-[8px] p-3 border border-white/10">
                   <div className="text-[14px] font-bold text-white mb-1">GANDHIPURAM MAIN ST</div>
                   <div className="flex items-center gap-4 text-[11px] font-mono text-gray-400">
                     <span>FPS: 30</span>
                     <span>RES: 4K</span>
                     <span>PING: 12ms</span>
                   </div>
                 </div>
               </div>

               {/* Secondary Feeds */}
               <div className="grid grid-cols-2 gap-6">
                  <div className="relative aspect-video rounded-[12px] overflow-hidden bg-black border border-white/10">
                    <Image src="/cctv analysis.png" fill className="object-cover opacity-60" alt="Sub Feed 1" />
                    <div className="absolute top-2 left-2 bg-black/50 backdrop-blur text-white text-[9px] font-mono px-1.5 py-0.5 rounded border border-white/10">CCTV_NORTH_4</div>
                  </div>
                  <div className="relative aspect-video rounded-[12px] overflow-hidden bg-black border border-white/10">
                    <Image src="/changed photo for mesh.png" fill className="object-cover opacity-60" alt="Sub Feed 2" />
                    <div className="absolute top-2 left-2 bg-black/50 backdrop-blur text-white text-[9px] font-mono px-1.5 py-0.5 rounded border border-white/10">MESH_NODE_8</div>
                  </div>
               </div>
            </div>

            {/* Sidebar Alerts / Stats */}
            <div className="md:col-span-4 flex flex-col gap-6">
              
              {/* Stat Cards */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-black/30 border border-white/5 p-4 rounded-[12px]">
                  <div className="text-[12px] text-gray-400 font-mono mb-1">ACTIVE CAMERAS</div>
                  <div className="text-[28px] font-display font-bold text-white">412</div>
                </div>
                <div className="bg-black/30 border border-white/5 p-4 rounded-[12px]">
                  <div className="text-[12px] text-gray-400 font-mono mb-1">CITY RISK LVL</div>
                  <div className="text-[28px] font-display font-bold text-[var(--warning)]">MOD</div>
                </div>
              </div>

              {/* Event Log */}
              <div className="flex-1 bg-black/30 border border-white/5 rounded-[12px] flex flex-col overflow-hidden">
                <div className="p-4 border-b border-white/5 font-mono text-[12px] text-gray-400 font-semibold flex justify-between">
                  <span>LIVE EVENT LOG</span>
                  <span>(42)</span>
                </div>
                <div className="p-4 flex flex-col gap-3 overflow-y-auto">
                   
                   <div className="flex items-start gap-3 p-3 rounded-lg bg-[var(--danger)]/5 border border-[var(--danger)]/20">
                     <i className="bi bi-exclamation-triangle-fill text-[var(--danger)] mt-0.5"></i>
                     <div>
                       <div className="text-[13px] font-bold text-white mb-0.5">Near Collision Detected</div>
                       <div className="text-[11px] text-gray-400 font-mono">14s ago • Dashcam_08 • High Priority</div>
                     </div>
                   </div>

                   <div className="flex items-start gap-3 p-3 rounded-lg bg-[var(--warning)]/5 border border-[var(--warning)]/20">
                     <i className="bi bi-cone-striped text-[var(--warning)] mt-0.5"></i>
                     <div>
                       <div className="text-[13px] font-bold text-white mb-0.5">Lane Obstruction</div>
                       <div className="text-[11px] text-gray-400 font-mono">2m ago • CCTV_41 • Traffic Rerouted</div>
                     </div>
                   </div>

                   <div className="flex items-start gap-3 p-3 rounded-lg bg-[var(--cyan)]/5 border border-[var(--cyan)]/20">
                     <i className="bi bi-car-front text-[var(--cyan)] mt-0.5"></i>
                     <div>
                       <div className="text-[13px] font-bold text-white mb-0.5">Illegal Parking Cleared</div>
                       <div className="text-[11px] text-gray-400 font-mono">5m ago • Mesh_Node_2</div>
                     </div>
                   </div>

                   <div className="flex items-start gap-3 p-3 rounded-lg bg-[var(--blue)]/5 border border-[var(--blue)]/20 opacity-50">
                     <i className="bi bi-info-circle text-[var(--blue)] mt-0.5"></i>
                     <div>
                       <div className="text-[13px] font-bold text-white mb-0.5">Bus 44 Joined Mesh</div>
                       <div className="text-[11px] text-gray-400 font-mono">12m ago • Sync Complete</div>
                     </div>
                   </div>

                </div>
              </div>

            </div>
          </div>
        </div>
      </PageContainer>
    </Section>
  );
}
