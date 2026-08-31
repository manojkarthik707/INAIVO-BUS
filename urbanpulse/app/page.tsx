import CinematicSimulation from "@/components/sections/CinematicSimulation";
import HeroSection from "@/components/sections/HeroSection";
import ContextSection from "@/components/sections/ContextSection";
import DashcamSection from "@/components/sections/DashcamSection";
import CctvSection from "@/components/sections/CctvSection";
import SwarmSection from "@/components/sections/SwarmSection";

export default function Home() {
  return (
    <main className="bg-base min-h-screen text-white font-body selection:bg-[var(--cyan)]/30">
      <HeroSection />
      
      {/* Context Section flows naturally now (No Sticky/Parallax scroll trap) */}
      <div className="relative w-full z-10 bg-[var(--bg-secondary)]">
        <ContextSection />
      </div>
      
      {/* Stacked Panels Container for the rest of the app */}
      <div className="relative w-full">

         {/* Dashcam Section (Sticky on Desktop) */}
         <div className="relative lg:sticky top-0 min-h-screen w-full z-20 shadow-[0_-20px_50px_rgba(0,0,0,0.8)]">
            <DashcamSection />
         </div>
         <div className="hidden lg:block h-[50vh] w-full pointer-events-none" />

         {/* Cctv Section (Sticky on Desktop) */}
         <div className="relative lg:sticky top-0 min-h-screen w-full z-30 shadow-[0_-20px_50px_rgba(0,0,0,0.8)]">
            <CctvSection />
         </div>
         <div className="hidden lg:block h-[50vh] w-full pointer-events-none" />

         {/* Swarm Section (Sticky on Desktop) */}
         <div className="relative lg:sticky top-0 min-h-screen w-full z-40 shadow-[0_-20px_50px_rgba(0,0,0,0.8)]">
            <SwarmSection />
         </div>
         <div className="hidden lg:block h-[50vh] w-full pointer-events-none" />

         {/* Simulation Section (Sticky on Desktop) - Restored Parallax & 360 */}
         <div className="relative lg:sticky top-0 h-screen w-full z-50 shadow-[0_-20px_50px_rgba(0,0,0,1)] bg-black">
            <div id="simulation" className="h-full w-full">
               <CinematicSimulation />
            </div>
         </div>

      </div>
    </main>
  );
}
