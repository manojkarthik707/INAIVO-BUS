"use client";

import { useRef, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";
import { SelectedAssetData } from "./SelectionHighlight";

interface VehicleSystemProps {
  mode: "parallax" | "360";
  progressRef: React.MutableRefObject<number>;
  onSelectAsset?: (asset: SelectedAssetData) => void;
}

// ─── Double Parked Truck / Cargo Van ─────────────────────────
function DoubleParkedTruckMesh({
  position,
  onSelect,
}: {
  position: [number, number, number];
  onSelect?: (asset: SelectedAssetData) => void;
}) {
  const [hovered, setHovered] = useState(false);

  const handleClick = (e: any) => {
    e.stopPropagation();
    onSelect?.({
      id: "truck-dp",
      name: "DOUBLE PARKING",
      category: "VEHICLE",
      position: [position[0], 1.6, position[2]],
      size: [2.5, 3.2, 7.2],
      status: "VIOLATION",
      statusColor: "#ff4d4d",
      description:
        "Just one double parked vehicle can increase the likelihood of crashes and wreaks havoc on traffic and public transit on-time performance.",
      metrics: [
        { label: "LICENSE PLATE", value: "KA-01-EQ-9182" },
        { label: "VIOLATION TIME", value: "14 MINS EXCEEDED" },
        { label: "SPEED", value: "0.0 KM/H (PARKED)" },
        { label: "CONFIDENCE", value: "98.7% EDGE AI" },
      ],
      details: [
        "Blocking Lane #2 right shoulder",
        "Bus 017 trajectory obstructed",
        "Citation auto-generated to RTO database",
      ],
    });
  };

  return (
    <group
      position={position}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = "default"; }}
    >
      {/* ── Main Cargo Container Body ── */}
      <mesh position={[0, 1.8, 0]}>
        <boxGeometry args={[2.3, 2.5, 5.5]} />
        <meshStandardMaterial color={hovered ? 0xef4444 : 0x475569} metalness={0.5} roughness={0.5} />
      </mesh>

      {/* Front Cab */}
      <mesh position={[0, 1.4, 3.4]}>
        <boxGeometry args={[2.2, 1.8, 1.8]} />
        <meshStandardMaterial color={hovered ? 0xef4444 : 0x1e293b} metalness={0.6} roughness={0.4} />
      </mesh>
      {/* Front Windshield */}
      <mesh position={[0, 1.7, 4.32]}>
        <boxGeometry args={[2.0, 0.9, 0.05]} />
        <meshStandardMaterial color={0x0284c7} metalness={0.9} roughness={0.1} transparent opacity={0.7} />
      </mesh>

      {/* Hazard Flashing Warning LED Lights */}
      <mesh position={[-1.1, 0.7, 4.33]}>
        <boxGeometry args={[0.2, 0.2, 0.05]} />
        <meshBasicMaterial color={0xffaa00} />
      </mesh>
      <mesh position={[1.1, 0.7, 4.33]}>
        <boxGeometry args={[0.2, 0.2, 0.05]} />
        <meshBasicMaterial color={0xffaa00} />
      </mesh>

      {/* Wheels */}
      {[[-1.15, 0.5, 2.5], [1.15, 0.5, 2.5], [-1.15, 0.5, -2.0], [1.15, 0.5, -2.0]].map(([x, y, z], i) => (
        <mesh key={i} position={[x, y, z]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.45, 0.45, 0.3, 16]} />
          <meshStandardMaterial color={0x0f172a} roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

// Highly detailed Bus geometry
function BusMesh({ color = 0x1a3a6a, hovered = false }: { color?: number; hovered?: boolean }) {
  return (
    <group>
      {/* ── Main Chassis ── */}
      <mesh position={[0, 1.6, 0]}>
        <boxGeometry args={[2.4, 2.8, 8]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : color} metalness={0.4} roughness={0.6} />
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

      {/* ── Windows ── */}
      <mesh position={[0, 2.1, 0]}>
        <boxGeometry args={[2.42, 1.1, 7.6]} />
        <meshStandardMaterial color={0x0a1a2e} metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Front Windshield */}
      <mesh position={[0, 2.1, 4.05]}>
        <boxGeometry args={[2.2, 1.3, 0.05]} />
        <meshStandardMaterial color={0x091625} metalness={0.95} roughness={0.05} transparent opacity={0.6} />
      </mesh>
    </group>
  );
}

// Sleek Sedan Car Geometry
function CarMesh({ color = 0x334455, hovered = false }: { color?: number; hovered?: boolean }) {
  return (
    <group>
      {/* Chassis */}
      <mesh position={[0, 0.65, 0]}>
        <boxGeometry args={[1.9, 0.7, 4.4]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : color} metalness={0.6} roughness={0.4} />
      </mesh>
      {/* Cabin Roof */}
      <mesh position={[0, 1.25, -0.2]}>
        <boxGeometry args={[1.7, 0.65, 2.4]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : color} metalness={0.6} roughness={0.4} />
      </mesh>
      {/* Windows */}
      <mesh position={[0, 1.25, -0.2]}>
        <boxGeometry args={[1.72, 0.55, 2.2]} />
        <meshStandardMaterial color={0x0f172a} metalness={0.95} roughness={0.05} />
      </mesh>
      {/* Wheels */}
      {[[-0.95, 0.35, 1.3], [0.95, 0.35, 1.3], [-0.95, 0.35, -1.3], [0.95, 0.35, -1.3]].map(([x, y, z], i) => (
        <mesh key={i} position={[x, y, z]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.35, 0.35, 0.22, 16]} />
          <meshStandardMaterial color={0x0f172a} roughness={0.9} />
        </mesh>
      ))}
    </group>
  );
}

interface VehicleInstance {
  id: string;
  name: string;
  type: "bus" | "car";
  laneX: number;
  speed: number;
  startZ: number;
  color: number;
}

const VEHICLES: VehicleInstance[] = [
  { id: "bus-017", name: "Autonomous Bus 017", type: "bus", laneX: -2, speed: 0.045, startZ: 30, color: 0x1e3a8a },
  { id: "bus-023", name: "Transit Bus 023", type: "bus", laneX: 2, speed: 0.032, startZ: -50, color: 0x0369a1 },
  { id: "car-01", name: "Sedan KA-03-M-1029", type: "car", laneX: -4.5, speed: 0.07, startZ: 15, color: 0x334155 },
  { id: "car-02", name: "EV Coupe KA-05-AB-4411", type: "car", laneX: 4.5, speed: 0.06, startZ: -20, color: 0x475569 },
  { id: "car-03", name: "Compact KA-01-P-8820", type: "car", laneX: -2, speed: 0.08, startZ: -35, color: 0x1e293b },
  { id: "car-04", name: "Patrol SUV KA-02-G-0001", type: "car", laneX: 4.5, speed: 0.05, startZ: 5, color: 0x0f172a },
];

function Vehicle({
  vehicle,
  mode,
  progressRef,
  onSelectAsset,
}: {
  vehicle: VehicleInstance;
  mode: "parallax" | "360";
  progressRef: React.MutableRefObject<number>;
  onSelectAsset?: (asset: SelectedAssetData) => void;
}) {
  const groupRef = useRef<THREE.Group>(null);
  const [hovered, setHovered] = useState(false);
  const isLeftLane = vehicle.laneX < 0;

  useFrame(() => {
    if (!groupRef.current || mode === "360") return;
    
    const progress = progressRef.current;
    const distanceToMove = progress * vehicle.speed * 2000;
    
    let currentZ;
    if (isLeftLane) {
      currentZ = vehicle.startZ - distanceToMove;
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
  const staticZ = isLeftLane ? vehicle.startZ - (0.15 * vehicle.speed * 2000) : vehicle.startZ + (0.15 * vehicle.speed * 2000);
  const currentZ = mode === "360" ? ((staticZ + 100) % 200) - 100 : vehicle.startZ;

  const handleClick = (e: any) => {
    e.stopPropagation();
    const curPos = groupRef.current ? groupRef.current.position : new THREE.Vector3(vehicle.laneX, 0, currentZ);

    if (vehicle.type === "bus") {
      onSelectAsset?.({
        id: vehicle.id,
        name: vehicle.name,
        category: "VEHICLE",
        position: [curPos.x, 1.8, curPos.z],
        size: [2.8, 3.2, 8.5],
        status: "ACTIVE",
        statusColor: "#00d4ff",
        description: "Mobile sensing platform equipped with dual front dashcams, LiDAR, and edge inference module parsing road hazards in real-time.",
        metrics: [
          { label: "PASSENGERS", value: "24 / 40" },
          { label: "ROUTE", value: "ROUTE #14 - CENTRAL" },
          { label: "SPEED", value: "32 KM/H" },
          { label: "EDGE INFERENCE", value: "18.2 FPS" },
        ],
        details: [
          "Onboard AI running local edge detection",
          "Pothole #PO-142 detected & transmitted",
          "5G Event Sync active",
        ],
      });
    } else {
      onSelectAsset?.({
        id: vehicle.id,
        name: vehicle.name,
        category: "VEHICLE",
        position: [curPos.x, 0.8, curPos.z],
        size: [2.2, 1.8, 4.8],
        status: "NOMINAL",
        statusColor: "#10b981",
        description: "Tracked passenger vehicle proceeding along urban corridor. Trajectory monitored by roadside edge cameras.",
        metrics: [
          { label: "SPEED", value: "45 KM/H" },
          { label: "LANE", value: isLeftLane ? "LANE 1 (WEST)" : "LANE 2 (EAST)" },
          { label: "HEADING", value: isLeftLane ? "270° WEST" : "090° EAST" },
          { label: "STATUS", value: "IN COMPLIANCE" },
        ],
        details: [
          "Zero traffic violations recorded",
          "Continuous ANPR tracking active",
        ],
      });
    }
  };

  return (
    <group
      ref={groupRef}
      position={[vehicle.laneX, 0, currentZ]}
      rotation={[0, rotationY, 0]}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = "default"; }}
    >
      {vehicle.type === "bus" ? (
        <BusMesh color={vehicle.color} hovered={hovered} />
      ) : (
        <CarMesh color={vehicle.color} hovered={hovered} />
      )}
    </group>
  );
}

export default function VehicleSystem({ mode, progressRef, onSelectAsset }: VehicleSystemProps) {
  return (
    <group>
      {/* Double Parked Truck (Matching Image 2 Violation) */}
      <DoubleParkedTruckMesh position={[4.8, 0, -10]} onSelect={onSelectAsset} />

      {/* Moving Vehicle Fleet */}
      {VEHICLES.map((v) => (
        <Vehicle
          key={v.id}
          vehicle={v}
          mode={mode}
          progressRef={progressRef}
          onSelectAsset={onSelectAsset}
        />
      ))}
    </group>
  );
}
