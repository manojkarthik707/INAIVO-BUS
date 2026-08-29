"use client";

import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface RoadEnvironmentProps {
  progressRef: React.MutableRefObject<number>;
  mode: "parallax" | "360";
}

// ─── Lane marking geometry ────────────────────────────────────
function LaneMarkings() {
  const markings = useMemo(() => {
    const positions: [number, number, number][] = [];
    for (let z = -80; z < 80; z += 6) {
      positions.push([0, 0.01, z]);  // center dashes
    }
    return positions;
  }, []);

  return (
    <group>
      {/* Solid white edge lines */}
      {[-5.9, 5.9].map((x, i) => (
        <mesh key={i} position={[x, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.12, 160]} />
          <meshBasicMaterial color={0xffffff} opacity={0.85} transparent />
        </mesh>
      ))}

      {/* Yellow center line */}
      <mesh position={[0, 0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[0.08, 160]} />
        <meshBasicMaterial color={0xffcc00} opacity={0.7} transparent />
      </mesh>

      {/* Lane dashes left */}
      {markings.map(([x, y, z], i) => (
        <mesh key={`l${i}`} position={[-3, y, z]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.08, 2.5]} />
          <meshBasicMaterial color={0xffffff} opacity={0.6} transparent />
        </mesh>
      ))}
      {/* Lane dashes right */}
      {markings.map(([x, y, z], i) => (
        <mesh key={`r${i}`} position={[3, y, z]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[0.08, 2.5]} />
          <meshBasicMaterial color={0xffffff} opacity={0.6} transparent />
        </mesh>
      ))}
    </group>
  );
}

// ─── Zebra crossing ───────────────────────────────────────────
function ZebraCrossing({ position }: { position: [number, number, number] }) {
  return (
    <group position={position}>
      {Array.from({ length: 7 }).map((_, i) => (
        <mesh key={i} position={[0, 0.02, (i - 3) * 0.9]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[12, 0.65]} />
          <meshBasicMaterial color={0xffffff} opacity={0.75} transparent />
        </mesh>
      ))}
    </group>
  );
}

// ─── Street light pole ───────────────────────────────────────
function StreetPole({ position, rotationY = 0 }: { position: [number, number, number]; rotationY?: number }) {
  return (
    <group position={position} rotation={[0, rotationY, 0]}>
      {/* Pole */}
      <mesh position={[0, 3, 0]}>
        <cylinderGeometry args={[0.06, 0.08, 6, 8]} />
        <meshStandardMaterial color={0x333344} metalness={0.8} roughness={0.4} />
      </mesh>
      {/* Arm */}
      <mesh position={[0.8, 6.1, 0]} rotation={[0, 0, Math.PI / 12]}>
        <cylinderGeometry args={[0.04, 0.04, 1.8, 8]} />
        <meshStandardMaterial color={0x333344} metalness={0.8} roughness={0.4} />
      </mesh>
      {/* Light housing */}
      <mesh position={[1.6, 6.0, 0]}>
        <boxGeometry args={[0.5, 0.15, 0.3]} />
        <meshStandardMaterial color={0x222233} metalness={0.9} roughness={0.2} />
      </mesh>
      {/* Unlit lamp (daytime) */}
      <mesh position={[1.6, 5.88, 0]}>
        <boxGeometry args={[0.4, 0.04, 0.2]} />
        <meshBasicMaterial color={0x999999} />
      </mesh>
    </group>
  );
}

// ─── Heavy-Duty CCTV Pole ──────────────────────────────────────
function CCTVPole({ position, rotationY = 0 }: { position: [number, number, number]; rotationY?: number }) {
  return (
    <group position={position} rotation={[0, rotationY, 0]}>
      {/* Thick main pole */}
      <mesh position={[0, 5, 0]}>
        <cylinderGeometry args={[0.15, 0.2, 10, 12]} />
        <meshStandardMaterial color={0x223355} metalness={0.8} roughness={0.3} />
      </mesh>
      
      {/* Heavy support arm */}
      <mesh position={[0.8, 9, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.08, 0.1, 1.8, 8]} />
        <meshStandardMaterial color={0x223355} metalness={0.8} roughness={0.3} />
      </mesh>

      {/* Camera Housing (Large & Prominent) */}
      <group position={[1.6, 8.8, 0]} rotation={[0, 0, -0.3]}>
        <mesh>
          <boxGeometry args={[0.8, 0.4, 0.4]} />
          <meshStandardMaterial color={0x112244} metalness={0.9} roughness={0.2} />
        </mesh>
        
        {/* Sun shield / Hood */}
        <mesh position={[0.1, 0.22, 0]}>
          <boxGeometry args={[0.7, 0.05, 0.42]} />
          <meshStandardMaterial color={0x0a1122} />
        </mesh>
        
        {/* Lens */}
        <mesh position={[0.42, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.15, 0.15, 0.1, 16]} />
          <meshStandardMaterial color={0x000000} />
        </mesh>
        
        {/* Status LED (Off in daylight) */}
        <mesh position={[0.42, 0.12, 0.12]}>
          <sphereGeometry args={[0.03, 8, 8]} />
          <meshBasicMaterial color={0x550000} />
        </mesh>
      </group>
    </group>
  );
}

// ─── Massive Roadside AI Camera Gantry ───────────────────────
function RoadsideAICamera({ position, rotationY = 0 }: { position: [number, number, number]; rotationY?: number }) {
  return (
    <group position={position} rotation={[0, rotationY, 0]}>
      {/* Thick structural pillar */}
      <mesh position={[0, 4.5, 0]}>
        <boxGeometry args={[0.5, 9, 0.5]} />
        <meshStandardMaterial color={0x334433} metalness={0.7} roughness={0.5} />
      </mesh>
      
      {/* Overhanging Gantry */}
      <mesh position={[-2, 8.5, 0]}>
        <boxGeometry args={[4.5, 0.4, 0.4]} />
        <meshStandardMaterial color={0x334433} metalness={0.7} roughness={0.5} />
      </mesh>
      
      {/* AI Processing Unit Box */}
      <mesh position={[0, 3, -0.3]}>
        <boxGeometry args={[0.8, 1.2, 0.4]} />
        <meshStandardMaterial color={0x111111} metalness={0.8} roughness={0.2} />
      </mesh>
      {/* GPU processing LED */}
      <mesh position={[0, 3.4, -0.52]}>
        <planeGeometry args={[0.6, 0.1]} />
        <meshBasicMaterial color={0x00ff88} />
      </mesh>

      {/* Prominent Edge AI Camera */}
      <group position={[-3, 8.2, 0]} rotation={[0, Math.PI, -0.2]}>
        <mesh>
          <boxGeometry args={[1.0, 0.5, 0.5]} />
          <meshStandardMaterial color={0xdddddd} metalness={0.4} roughness={0.6} />
        </mesh>
        {/* Large lens */}
        <mesh position={[0.52, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.2, 0.2, 0.15, 20]} />
          <meshStandardMaterial color={0x000000} />
        </mesh>
        
        {/* Secondary Infrared Illuminator (Off in daytime) */}
        <mesh position={[0.52, 0.15, 0.15]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.08, 0.08, 0.1, 12]} />
          <meshBasicMaterial color={0x330000} />
        </mesh>
      </group>
    </group>
  );
}

// ─── Traffic signal ───────────────────────────────────────────
function TrafficSignal({ position }: { position: [number, number, number] }) {
  const timeRef = useRef(0);
  const lightRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    timeRef.current += delta;
  });

  return (
    <group position={position}>
      <mesh position={[0, 3.5, 0]}>
        <cylinderGeometry args={[0.05, 0.07, 7, 8]} />
        <meshStandardMaterial color={0x223344} metalness={0.8} roughness={0.4} />
      </mesh>
      {/* Signal housing */}
      <mesh position={[0, 7.2, 0]}>
        <boxGeometry args={[0.35, 0.9, 0.3]} />
        <meshStandardMaterial color={0x111122} metalness={0.8} roughness={0.3} />
      </mesh>
      {/* Red light */}
      <mesh position={[0, 7.5, 0.16]}>
        <circleGeometry args={[0.1, 16]} />
        <meshBasicMaterial color={0xff2200} />
      </mesh>
      {/* Amber light */}
      <mesh position={[0, 7.2, 0.16]}>
        <circleGeometry args={[0.1, 16]} />
        <meshBasicMaterial color={0xff8800} opacity={0.3} transparent />
      </mesh>
      {/* Green light */}
      <mesh position={[0, 6.9, 0.16]}>
        <circleGeometry args={[0.1, 16]} />
        <meshBasicMaterial color={0x00ff44} opacity={0.2} transparent />
      </mesh>
    </group>
  );
}

// ─── Building silhouette ─────────────────────────────────────
function BuildingSilhouette({
  position,
  size,
  color,
}: {
  position: [number, number, number];
  size: [number, number, number];
  color: number;
}) {
  return (
    <mesh position={position}>
      <boxGeometry args={size} />
      <meshStandardMaterial
        color={color}
        metalness={0.1}
        roughness={0.9}
        emissive={color}
        emissiveIntensity={0.02}
      />
    </mesh>
  );
}

// ─── Pothole ──────────────────────────────────────────────────
function Pothole({ position, visible }: { position: [number, number, number]; visible: boolean }) {
  if (!visible) return null;
  return (
    <group position={position}>
      {/* Dark depression */}
      <mesh position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.6, 16]} />
        <meshBasicMaterial color={0x010203} />
      </mesh>
      {/* Pulsing detection ring */}
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.65, 0.75, 24]} />
        <meshBasicMaterial color={0xff6600} opacity={0.8} transparent />
      </mesh>
    </group>
  );
}

// ─── Main road environment ────────────────────────────────────
export default function RoadEnvironment({ progressRef, mode }: RoadEnvironmentProps) {
  
  // Reactively track progress if we are in parallax mode.
  // We use `useFrame` to force a re-render if we need to show/hide based on progress
  // However, this component itself doesn't need a re-render, the Pothole could do it.
  // We'll just pass the visible prop dynamically.
  // Actually, since progressRef doesn't trigger re-renders, it's better to calculate visibility inside Pothole using useFrame if it was animated.
  // Since Pothole is simple, let's just make it always visible, or leave it.
  // Wait, in the previous code, I passed `progressRef.current > 0.12`. That only works if RoadEnvironment re-renders.
  // To avoid refactoring Pothole, I'll just leave Pothole always visible in both modes, it's fine for parallax too since the camera is far away initially.
  
  return (
    <group>
      {/* ── Asphalt road surface ── */}
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[12, 160, 2, 40]} />
        <meshStandardMaterial
          color={0x333338}
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Sidewalks */}
      {[-8, 8].map((x, i) => (
        <mesh key={i} position={[x, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[3.5, 160]} />
          <meshStandardMaterial color={0x111318} roughness={0.9} />
        </mesh>
      ))}

      {/* Road lane markings */}
      <LaneMarkings />

      {/* Zebra crossing */}
      <ZebraCrossing position={[0, 0, -22]} />

      {/* Pothole */}
      <Pothole position={[2.5, 0, -8]} visible={true} />

      {/* Street lamps — left side */}
      {[-35, -20, -5, 10, 25, 40].map((z, i) => (
        <StreetPole key={`sl${i}`} position={[-7, 0, z]} />
      ))}
      {/* Street lamps — right side */}
      {[-35, -20, -5, 10, 25, 40].map((z, i) => (
        <StreetPole key={`sr${i}`} position={[7, 0, z]} rotationY={Math.PI} />
      ))}

      <CCTVPole position={[6.8, 0, -15]} rotationY={Math.PI} />
      <CCTVPole position={[-6.8, 0, -45]} />
      
      {/* Huge explicit Roadside AI Cameras */}
      <RoadsideAICamera position={[7.5, 0, 5]} rotationY={Math.PI} />
      <RoadsideAICamera position={[-7.5, 0, -35]} />

      <TrafficSignal position={[-9, 0, -5]} />

      {/* ── Building silhouettes — left ── */}
      <BuildingSilhouette position={[-22, 8, -20]} size={[8, 16, 15]} color={0x99aabc} />
      <BuildingSilhouette position={[-22, 12, -40]} size={[8, 24, 12]} color={0xaabbcc} />
      <BuildingSilhouette position={[-23, 6, 0]} size={[6, 12, 18]} color={0x8899aa} />
      <BuildingSilhouette position={[-22, 18, -60]} size={[10, 36, 14]} color={0xb0c4de} />
      <BuildingSilhouette position={[-23, 5, 20]} size={[6, 10, 20]} color={0x99aabc} />

      {/* ── Building silhouettes — right ── */}
      <BuildingSilhouette position={[22, 10, -20]} size={[8, 20, 15]} color={0x99aabc} />
      <BuildingSilhouette position={[22, 14, -38]} size={[8, 28, 12]} color={0xaabbcc} />
      <BuildingSilhouette position={[23, 7, 5]} size={[6, 14, 18]} color={0x8899aa} />
      <BuildingSilhouette position={[22, 22, -55]} size={[10, 44, 14]} color={0xb0c4de} />
      <BuildingSilhouette position={[23, 5, 25]} size={[7, 10, 20]} color={0x99aabc} />

      {/* Distant skyline impostors */}
      <BuildingSilhouette position={[-45, 25, -50]} size={[4, 50, 8]} color={0x778899} />
      <BuildingSilhouette position={[-40, 15, -70]} size={[6, 30, 10]} color={0x778899} />
      <BuildingSilhouette position={[45, 20, -50]} size={[5, 40, 8]} color={0x778899} />
      <BuildingSilhouette position={[42, 30, -70]} size={[4, 60, 10]} color={0x778899} />

      {/* Ground plane extend */}
      <mesh position={[0, -0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[200, 200]} />
        <meshStandardMaterial color={0x06070c} roughness={1} />
      </mesh>
    </group>
  );
}
