import CinematicSimulation from "@/components/sections/CinematicSimulation";
import HeroSection from "@/components/sections/HeroSection";
import ContextSection from "@/components/sections/ContextSection";
import ThreeCameraLayersSection from "@/components/sections/ThreeCameraLayersSection";
import QADomeSection from "@/components/sections/QADomeSection";

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

         {/* Three Camera Layers Section */}
         <div className="relative z-20 w-full shadow-[0_-20px_50px_rgba(0,0,0,0.8)]">
            <ThreeCameraLayersSection />
         </div>

         {/* Q&A Dome Section */}
         <div className="relative z-30 w-full shadow-[0_-20px_50px_rgba(0,0,0,0.8)]">
            <QADomeSection />
         </div>

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
