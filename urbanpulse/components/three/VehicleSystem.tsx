"use client";

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface VehicleSystemProps {
  mode: "parallax" | "360";
  progressRef: React.MutableRefObject<number>;
}

// Highly detailed Bus geometry
function BusMesh({ color = 0x1a3a6a }: { color?: number }) {
  return (
    <group>
      {/* ── Main Chassis ── */}
      <mesh position={[0, 1.6, 0]}>
        <boxGeometry args={[2.4, 2.8, 8]} />
        <meshStandardMaterial color={color} metalness={0.4} roughness={0.6} />
      </mesh>
      
      {/* Front and rear bumpers */}
      <mesh position={[0, 0.6, 4.05]}>
        <boxGeometry args={[2.45, 0.4, 0.2]} />
        <meshStandardMaterial color={0x222222} metalness={0.8} roughness={0.2} />
      </mesh>
      <mesh position={[0, 0.6, -4.05]}>
        <boxGeometry args={[2.45, 0.4, 0.2]} />
        <meshStandardMaterial color={0x222222} metalness={0.8} roughness={0.2} />
      </mesh>

      {/* Front Grill */}
      <mesh position={[0, 1.2, 4.02]}>
        <boxGeometry args={[1.6, 0.6, 0.1]} />
        <meshStandardMaterial color={0x111111} metalness={0.9} roughness={0.5} />
      </mesh>
      {/* Grill slats */}
      {[1.3, 1.1, 0.9].map((y, i) => (
        <mesh key={`grill-${i}`} position={[0, y, 4.05]}>
          <boxGeometry args={[1.5, 0.05, 0.05]} />
          <meshStandardMaterial color={0x333333} metalness={0.8} roughness={0.4} />
        </mesh>
      ))}

      {/* ── Roof & AC Unit ── */}
      <mesh position={[0, 3.1, 0]}>
        <boxGeometry args={[2.3, 0.25, 7.8]} />
        <meshStandardMaterial color={0x0d2240} metalness={0.5} roughness={0.5} />
      </mesh>
      <mesh position={[0, 3.3, -1]}>
        <boxGeometry args={[1.4, 0.3, 2.5]} />
        <meshStandardMaterial color={0xcceeff} metalness={0.6} roughness={0.4} />
      </mesh>

      {/* ── Windows & Pillars ── */}
      <mesh position={[0, 2.1, 0]}>
        <boxGeometry args={[2.42, 1.1, 7.6]} />
        <meshStandardMaterial color={0x0a1a2e} metalness={0.9} roughness={0.1} />
      </mesh>
      {/* Window pillars (vertical dividers) */}
      {[-2.5, -1, 0.5, 2].map((z, i) => (
        <mesh key={`pillar-${i}`} position={[0, 2.1, z]}>
          <boxGeometry args={[2.44, 1.1, 0.15]} />
          <meshStandardMaterial color={color} metalness={0.4} roughness={0.6} />
        </mesh>
      ))}

      {/* ── Front Windshield ── */}
      <mesh position={[0, 2.1, 4.05]}>
        <boxGeometry args={[2.2, 1.3, 0.05]} />
        <meshStandardMaterial color={0x091625} metalness={0.95} roughness={0.05} transparent opacity={0.6} />
      </mesh>
      <mesh position={[0, 2.8, 4.06]}>
        <boxGeometry args={[2.2, 0.3, 0.02]} />
        <meshStandardMaterial color={0x000000} />
      </mesh>

      {/* ── HIGH VISIBILITY DASHCAM (Visible from inside) ── */}
      <group position={[0, 2.3, 3.8]}>
        {/* Dashcam mounting arm */}
        <mesh position={[0, 0.15, 0.1]} rotation={[-Math.PI/6, 0, 0]}>
          <cylinderGeometry args={[0.02, 0.02, 0.3]} />
          <meshStandardMaterial color={0x222222} />
        </mesh>
        {/* Dashcam body */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[0.4, 0.25, 0.3]} />
          <meshStandardMaterial color={0x111122} metalness={0.8} roughness={0.2} />
        </mesh>
        {/* Screen on the back (facing passengers) */}
        <mesh position={[0, 0, -0.16]}>
          <planeGeometry args={[0.3, 0.15]} />
          <meshBasicMaterial color={0x44ff44} />
        </mesh>
        {/* Dashcam lens tube */}
        <mesh position={[0, 0, 0.15]} rotation={[Math.PI/2, 0, 0]}>
          <cylinderGeometry args={[0.08, 0.08, 0.1]} />
          <meshStandardMaterial color={0x000000} />
        </mesh>
      </group>

      {/* ── INTERIOR (Visible from inside the bus) ── */}
      <group>
        {/* Floor */}
        <mesh position={[0, 0.5, 0]} rotation={[-Math.PI/2, 0, 0]}>
          <planeGeometry args={[2.3, 7.8]} />
          <meshStandardMaterial color={0x1c2b39} roughness={0.9} side={THREE.DoubleSide} />
        </mesh>
        
        {/* Ceiling */}
        <mesh position={[0, 2.9, 0]} rotation={[Math.PI/2, 0, 0]}>
          <planeGeometry args={[2.3, 7.8]} />
          <meshStandardMaterial color={0xdddddd} roughness={0.8} side={THREE.DoubleSide} />
        </mesh>

        {/* Interior Side Walls */}
        <mesh position={[-1.15, 1.3, 0]} rotation={[0, Math.PI/2, 0]}>
          <planeGeometry args={[7.8, 1.6]} />
          <meshStandardMaterial color={0xddeeff} roughness={0.7} side={THREE.DoubleSide} />
        </mesh>
        <mesh position={[1.15, 1.3, 0]} rotation={[0, -Math.PI/2, 0]}>
          <planeGeometry args={[7.8, 1.6]} />
          <meshStandardMaterial color={0xddeeff} roughness={0.7} side={THREE.DoubleSide} />
        </mesh>

        {/* Seats and Poles Array */}
        {[-2.5, -1.0, 0.5, 2.0].map((z, i) => (
          <group key={`row-${i}`} position={[0, 0, z]}>
            {/* Left Seats */}
            <group position={[-0.7, 0.9, 0]}>
              {/* Seat cushion */}
              <mesh position={[0, -0.1, 0.1]}>
                <boxGeometry args={[0.8, 0.15, 0.5]} />
                <meshStandardMaterial color={0x0055aa} roughness={0.6} />
              </mesh>
              {/* Seat back */}
              <mesh position={[0, 0.3, -0.2]}>
                <boxGeometry args={[0.8, 0.8, 0.1]} />
                <meshStandardMaterial color={0x0055aa} roughness={0.6} />
              </mesh>
              {/* Seat handle (top) */}
              <mesh position={[0, 0.75, -0.2]}>
                <boxGeometry args={[0.8, 0.05, 0.05]} />
                <meshStandardMaterial color={0x888888} metalness={0.8} roughness={0.2} />
              </mesh>
            </group>

            {/* Right Seats */}
            <group position={[0.7, 0.9, 0]}>
              <mesh position={[0, -0.1, 0.1]}>
                <boxGeometry args={[0.8, 0.15, 0.5]} />
                <meshStandardMaterial color={0x0055aa} roughness={0.6} />
              </mesh>
              <mesh position={[0, 0.3, -0.2]}>
                <boxGeometry args={[0.8, 0.8, 0.1]} />
                <meshStandardMaterial color={0x0055aa} roughness={0.6} />
              </mesh>
              <mesh position={[0, 0.75, -0.2]}>
                <boxGeometry args={[0.8, 0.05, 0.05]} />
                <meshStandardMaterial color={0x888888} metalness={0.8} roughness={0.2} />
              </mesh>
            </group>

            {/* Vertical Poles */}
            <mesh position={[-0.3, 1.7, 0]}>
              <cylinderGeometry args={[0.03, 0.03, 2.4]} />
              <meshStandardMaterial color={0xcccccc} metalness={0.9} roughness={0.1} />
            </mesh>
            <mesh position={[0.3, 1.7, 0]}>
              <cylinderGeometry args={[0.03, 0.03, 2.4]} />
              <meshStandardMaterial color={0xcccccc} metalness={0.9} roughness={0.1} />
            </mesh>
          </group>
        ))}

        {/* Overhead Horizontal Rails */}
        <mesh position={[-0.3, 2.7, 0]} rotation={[Math.PI/2, 0, 0]}>
          <cylinderGeometry args={[0.03, 0.03, 7.8]} />
          <meshStandardMaterial color={0xcccccc} metalness={0.9} roughness={0.1} />
        </mesh>
        <mesh position={[0.3, 2.7, 0]} rotation={[Math.PI/2, 0, 0]}>
          <cylinderGeometry args={[0.03, 0.03, 7.8]} />
          <meshStandardMaterial color={0xcccccc} metalness={0.9} roughness={0.1} />
        </mesh>

        {/* Ceiling Lights */}
        {[-3, -1, 1, 3].map((z, i) => (
          <mesh key={`light-${i}`} position={[0, 2.88, z]} rotation={[Math.PI/2, 0, 0]}>
            <planeGeometry args={[0.8, 0.4]} />
            <meshBasicMaterial color={0xffffee} />
          </mesh>
        ))}
        
        {/* Dummy Passengers */}
        {/* Passenger 1 (Sitting Left) */}
        <group position={[-0.7, 1.1, -1]}>
          {/* Body */}
          <mesh position={[0, 0.1, 0]}>
            <boxGeometry args={[0.5, 0.6, 0.3]} />
            <meshStandardMaterial color={0xaa4444} />
          </mesh>
          {/* Head */}
          <mesh position={[0, 0.55, 0.05]}>
            <sphereGeometry args={[0.18]} />
            <meshStandardMaterial color={0xffccaa} />
          </mesh>
        </group>

        {/* Passenger 2 (Standing) */}
        <group position={[0, 1.3, 0.5]}>
          <mesh position={[0, 0.3, 0]}>
            <boxGeometry args={[0.45, 0.8, 0.3]} />
            <meshStandardMaterial color={0x44aa44} />
          </mesh>
          <mesh position={[0, 0.85, 0]}>
            <sphereGeometry args={[0.18]} />
            <meshStandardMaterial color={0x8d5524} />
          </mesh>
        </group>
      </group>

      {/* ── Side Mirrors ── */}
      {[[-1.3, 2.0, 3.8], [1.3, 2.0, 3.8]].map(([x, y, z], i) => (
        <group key={`mirror-${i}`} position={[x, y, z]}>
          <mesh position={[Math.sign(x) * 0.15, 0, 0]} rotation={[0, 0, Math.PI/2]}>
            <cylinderGeometry args={[0.02, 0.02, 0.3]} />
            <meshStandardMaterial color={0x111111} />
          </mesh>
          <mesh position={[Math.sign(x) * 0.3, -0.2, 0]}>
            <boxGeometry args={[0.1, 0.5, 0.2]} />
            <meshStandardMaterial color={0x222222} metalness={0.8} roughness={0.2} />
          </mesh>
        </group>
      ))}

      {/* ── Detailed Wheels ── */}
      {[[-1.25, 0.55, 2.5], [1.25, 0.55, 2.5], [-1.25, 0.55, -2.5], [1.25, 0.55, -2.5]].map(
        ([x, y, z], i) => (
          <group key={`wheel-${i}`} position={[x, y, z]} rotation={[0, 0, Math.PI / 2]}>
            {/* Tire */}
            <mesh>
              <cylinderGeometry args={[0.55, 0.55, 0.35, 24]} />
              <meshStandardMaterial color={0x111111} metalness={0.2} roughness={0.9} />
            </mesh>
            {/* Rim */}
            <mesh position={[0, Math.sign(x) * 0.18, 0]}>
              <cylinderGeometry args={[0.35, 0.35, 0.05, 16]} />
              <meshStandardMaterial color={0xcccccc} metalness={0.9} roughness={0.1} />
            </mesh>
          </group>
        )
      )}

      {/* ── BMTC Livery & Headlights ── */}
      <mesh position={[0, 0.9, 0]}>
        <boxGeometry args={[2.42, 0.3, 7.82]} />
        <meshBasicMaterial color={0x0044cc} />
      </mesh>
      
      {/* Headlights & Taillights (Unlit for day) */}
      {[[-0.8, 0.9, 4.05], [0.8, 0.9, 4.05]].map(([x, y, z], i) => (
        <group key={`hl-${i}`} position={[x, y, z]}>
          <mesh>
            <boxGeometry args={[0.5, 0.25, 0.1]} />
            <meshStandardMaterial color={0xeeeeee} roughness={0.2} />
          </mesh>
        </group>
      ))}
      
      {[[-0.8, 1.2, -4.05], [0.8, 1.2, -4.05]].map(([x, y, z], i) => (
        <mesh key={`tl-${i}`} position={[x, y, z]}>
          <boxGeometry args={[0.3, 0.5, 0.1]} />
          <meshStandardMaterial color={0xaa0000} roughness={0.4} />
        </mesh>
      ))}
    </group>
  );
}

// Detailed car geometry
function CarMesh({ color = 0x1a1a2e }: { color?: number }) {
  return (
    <group>
      {/* ── Lower body ── */}
      <mesh position={[0, 0.55, 0]}>
        <boxGeometry args={[1.8, 0.7, 4.4]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Front hood slope */}
      <mesh position={[0, 0.7, 1.6]} rotation={[-Math.PI/16, 0, 0]}>
        <boxGeometry args={[1.78, 0.2, 1.4]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Rear trunk */}
      <mesh position={[0, 0.75, -1.8]}>
        <boxGeometry args={[1.78, 0.15, 0.9]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>

      {/* Grill & Bumper */}
      <mesh position={[0, 0.4, 2.21]}>
        <boxGeometry args={[1.4, 0.3, 0.05]} />
        <meshStandardMaterial color={0x111111} metalness={0.9} roughness={0.5} />
      </mesh>

      {/* ── Upper cabin ── */}
      <mesh position={[0, 1.15, -0.2]}>
        <boxGeometry args={[1.5, 0.6, 2.4]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>
      
      {/* Windshields (Front & Rear angled) */}
      <mesh position={[0, 1.15, 1.05]} rotation={[Math.PI/6, 0, 0]}>
        <boxGeometry args={[1.4, 0.6, 0.05]} />
        <meshStandardMaterial color={0x0a1625} metalness={0.95} roughness={0.05} transparent opacity={0.8} />
      </mesh>
      <mesh position={[0, 1.15, -1.45]} rotation={[-Math.PI/6, 0, 0]}>
        <boxGeometry args={[1.4, 0.6, 0.05]} />
        <meshStandardMaterial color={0x0a1625} metalness={0.95} roughness={0.05} transparent opacity={0.8} />
      </mesh>

      {/* Side Windows */}
      <mesh position={[0, 1.15, -0.2]}>
        <boxGeometry args={[1.52, 0.5, 2.2]} />
        <meshStandardMaterial color={0x0a1625} metalness={0.95} roughness={0.05} transparent opacity={0.8} />
      </mesh>
      {/* Door pillars */}
      <mesh position={[0, 1.15, -0.2]}>
        <boxGeometry args={[1.54, 0.5, 0.15]} />
        <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
      </mesh>

      {/* ── Side Mirrors ── */}
      {[[-0.8, 0.95, 0.8], [0.8, 0.95, 0.8]].map(([x, y, z], i) => (
        <mesh key={`carmirror-${i}`} position={[x, y, z]}>
          <boxGeometry args={[0.15, 0.1, 0.15]} />
          <meshStandardMaterial color={color} metalness={0.7} roughness={0.3} />
        </mesh>
      ))}

      {/* ── Detailed Wheels ── */}
      {[[-0.9, 0.38, 1.4], [0.9, 0.38, 1.4], [-0.9, 0.38, -1.4], [0.9, 0.38, -1.4]].map(
        ([x, y, z], i) => (
          <group key={`carwheel-${i}`} position={[x, y, z]} rotation={[0, 0, Math.PI / 2]}>
            <mesh>
              <cylinderGeometry args={[0.38, 0.38, 0.28, 20]} />
              <meshStandardMaterial color={0x0a0a0a} metalness={0.2} roughness={0.9} />
            </mesh>
            <mesh position={[0, Math.sign(x) * 0.15, 0]}>
              <cylinderGeometry args={[0.22, 0.22, 0.05, 12]} />
              <meshStandardMaterial color={0xeeeeee} metalness={0.9} roughness={0.2} />
            </mesh>
          </group>
        )
      )}

      {/* ── Headlights & Taillights (Unlit for day) ── */}
      {[[-0.6, 0.6, 2.22], [0.6, 0.6, 2.22]].map(([x, y, z], i) => (
        <mesh key={`carhl-${i}`} position={[x, y, z]}>
          <boxGeometry args={[0.3, 0.15, 0.05]} />
          <meshStandardMaterial color={0xdddddd} roughness={0.2} />
        </mesh>
      ))}
      {[[-0.6, 0.7, -2.22], [0.6, 0.7, -2.22]].map(([x, y, z], i) => (
        <mesh key={`cartl-${i}`} position={[x, y, z]}>
          <boxGeometry args={[0.3, 0.15, 0.05]} />
          <meshStandardMaterial color={0xaa0000} roughness={0.4} />
        </mesh>
      ))}
    </group>
  );
}

// Vehicle instances with spline paths
interface VehicleInstance {
  id: string;
  type: "bus" | "car";
  laneX: number;
  speed: number;
  startZ: number;
  color: number;
}

const VEHICLES: VehicleInstance[] = [
  { id: "bus1", type: "bus", laneX: -2, speed: 0.045, startZ: 30, color: 0x2255aa },
  { id: "bus2", type: "bus", laneX: 2, speed: 0.032, startZ: -50, color: 0x3366bb },
  { id: "car1", type: "car", laneX: -4.5, speed: 0.07, startZ: 15, color: 0x556677 },
  { id: "car2", type: "car", laneX: 4.5, speed: 0.06, startZ: -20, color: 0x665566 },
  { id: "car3", type: "car", laneX: -2, speed: 0.08, startZ: -35, color: 0x445566 },
  { id: "car4", type: "car", laneX: 4.5, speed: 0.05, startZ: 5, color: 0x666677 },
];

function Vehicle({ vehicle, mode, progressRef }: { vehicle: VehicleInstance; mode: "parallax" | "360"; progressRef: React.MutableRefObject<number> }) {
  const groupRef = useRef<THREE.Group>(null);
  
  const isLeftLane = vehicle.laneX < 0;

  useFrame(() => {
    if (!groupRef.current || mode === "360") return;
    
    const progress = progressRef.current;
    
    // Instead of time-based movement, we tether movement to scroll progress
    // so it scrubs back and forth deterministically.
    const distanceToMove = progress * vehicle.speed * 2000;
    
    let currentZ;
    if (isLeftLane) {
      currentZ = vehicle.startZ - distanceToMove;
      // Loop them smoothly
      currentZ = ((currentZ + 100) % 200) - 100; 
      if (currentZ > 100) currentZ -= 200;
    } else {
      currentZ = vehicle.startZ + distanceToMove;
      currentZ = ((currentZ + 100) % 200) - 100;
      if (currentZ < -100) currentZ += 200;
    }
    
    groupRef.current.position.set(vehicle.laneX, 0, currentZ);
  });

  const rotationY = isLeftLane ? Math.PI : 0;
  
  // In 360 mode, initialize at a nice looking scrub position (e.g. progress = 0.15)
  // so the snapshot looks good. Or just startZ.
  const staticZ = isLeftLane ? vehicle.startZ - (0.15 * vehicle.speed * 2000) : vehicle.startZ + (0.15 * vehicle.speed * 2000);
  const currentZ = mode === "360" ? ((staticZ + 100) % 200) - 100 : vehicle.startZ;

  return (
    <group ref={groupRef} position={[vehicle.laneX, 0, currentZ]} rotation={[0, rotationY, 0]}>
      {vehicle.type === "bus" ? (
        <BusMesh color={vehicle.color} />
      ) : (
        <CarMesh color={vehicle.color} />
      )}
    </group>
  );
}

export default function VehicleSystem({ mode, progressRef }: VehicleSystemProps) {
  return (
    <group>
      {VEHICLES.map((v) => (
        <Vehicle key={v.id} vehicle={v} mode={mode} progressRef={progressRef} />
      ))}
    </group>
  );
}
