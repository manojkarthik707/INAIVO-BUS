import CinematicSimulation from "@/components/sections/CinematicSimulation";

export default function Home() {
  return (
    <main className="bg-base min-h-screen text-white">
      <div className="absolute top-0 left-0 right-0 z-50 p-6 flex justify-between items-center bg-gradient-to-b from-black/80 to-transparent pointer-events-none">
        <h1 className="font-heading text-2xl font-bold tracking-wider" style={{ color: "var(--accent-cyan)" }}>
          URBANPULSE FUSION
        </h1>
        <div className="text-sm font-mono opacity-60">
          BEL · SIH26124
        </div>
      </div>
      <CinematicSimulation />
    </main>
  );
}
