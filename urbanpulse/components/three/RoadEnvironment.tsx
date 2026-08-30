"use client";

import { useRef, useMemo, useEffect, useState } from "react";
import * as THREE from "three";
import { SelectedAssetData } from "./SelectionHighlight";

interface RoadEnvironmentProps {
  progressRef: React.MutableRefObject<number>;
  mode: "parallax" | "360";
  onSelectAsset?: (asset: SelectedAssetData) => void;
  selectedAssetId?: string;
}

// ─── Lane marking geometry ────────────────────────────────────
function LaneMarkings() {
  const markings = useMemo(() => {
    const positions: [number, number, number][] = [];
    for (let z = -80; z < 80; z += 6) {
      positions.push([0, 0.01, z]);
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

      {/* Lane dashes left & right */}
      {markings.map(([_, y, z], i) => (
        <group key={`dashes-${i}`}>
          <mesh position={[-3, y, z]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[0.08, 2.5]} />
            <meshBasicMaterial color={0xffffff} opacity={0.6} transparent />
          </mesh>
          <mesh position={[3, y, z]} rotation={[-Math.PI / 2, 0, 0]}>
            <planeGeometry args={[0.08, 2.5]} />
            <meshBasicMaterial color={0xffffff} opacity={0.6} transparent />
          </mesh>
        </group>
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

// ─── Fixed & Seamlessly Connected Street Light Pole ──────────────────
function StreetPole({
  id,
  position,
  rotationY = 0,
  onSelect,
}: {
  id: string;
  position: [number, number, number];
  rotationY?: number;
  onSelect?: (asset: SelectedAssetData) => void;
}) {
  const [hovered, setHovered] = useState(false);

  const handleClick = (e: any) => {
    e.stopPropagation();
    onSelect?.({
      id,
      name: `SMART LAMP ${id.toUpperCase()}`,
      category: "INFRASTRUCTURE",
      position: [position[0], 6.2, position[2]],
      size: [2.0, 6.5, 1.2],
      status: "ACTIVE",
      statusColor: "#00d4ff",
      description: "Connected IoT streetlight equipped with ambient light sensors, power metering, and edge AI optical node.",
      metrics: [
        { label: "POWER DRAW", value: "42 W (DIMMED 70%)" },
        { label: "SENSOR STATE", value: "HEALTHY (100%)" },
        { label: "NETWORK", value: "5G EDGE · 12 ms" },
        { label: "RUNTIME", value: "14,280 HRS" },
      ],
      details: [
        "Automatic light dimming based on traffic density",
        "Acoustic anomaly detector active",
        "Connected to District Grid-04",
      ],
    });
  };

  return (
    <group
      position={position}
      rotation={[0, rotationY, 0]}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = "default"; }}
    >
      {/* Heavy Base Ring */}
      <mesh position={[0, 0.15, 0]}>
        <cylinderGeometry args={[0.18, 0.22, 0.3, 10]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x222233} metalness={0.9} roughness={0.3} />
      </mesh>

      {/* Main Vertical Trunk */}
      <mesh position={[0, 3.0, 0]}>
        <cylinderGeometry args={[0.07, 0.12, 5.7, 10]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x2d3748} metalness={0.8} roughness={0.3} />
      </mesh>

      {/* Arm Collar Bracket */}
      <mesh position={[0, 5.8, 0]}>
        <cylinderGeometry args={[0.09, 0.09, 0.2, 10]} />
        <meshStandardMaterial color={0x1a202c} metalness={0.9} roughness={0.2} />
      </mesh>

      {/* ── Seamlessly Angled Arm & Integrated Head ── */}
      <group position={[0, 5.8, 0]} rotation={[0, 0, -Math.PI / 10]}>
        {/* Arm Tube */}
        <mesh position={[0.7, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.045, 0.045, 1.4, 10]} />
          <meshStandardMaterial color={hovered ? 0x00d4ff : 0x2d3748} metalness={0.85} roughness={0.3} />
        </mesh>

        {/* Fixture Joint Elbow */}
        <mesh position={[1.4, 0, 0]}>
          <sphereGeometry args={[0.06, 10, 10]} />
          <meshStandardMaterial color={0x1a202c} metalness={0.9} roughness={0.2} />
        </mesh>

        {/* Lamp Fixture Housing */}
        <mesh position={[1.65, -0.05, 0]}>
          <boxGeometry args={[0.6, 0.12, 0.26]} />
          <meshStandardMaterial color={0x111827} metalness={0.9} roughness={0.2} />
        </mesh>

        {/* LED Emitter Face */}
        <mesh position={[1.65, -0.12, 0]}>
          <boxGeometry args={[0.5, 0.02, 0.2]} />
          <meshBasicMaterial color={0xffea9f} />
        </mesh>

        {/* Soft Downward Cone Glow */}
        <mesh position={[1.65, -0.4, 0]}>
          <coneGeometry args={[0.4, 0.5, 10, 1, true]} />
          <meshBasicMaterial color={0xffaa44} opacity={0.15} transparent side={THREE.DoubleSide} />
        </mesh>
      </group>
    </group>
  );
}

// ─── Heavy-Duty CCTV Pole ──────────────────────────────────────
function CCTVPole({
  id,
  position,
  rotationY = 0,
  onSelect,
}: {
  id: string;
  position: [number, number, number];
  rotationY?: number;
  onSelect?: (asset: SelectedAssetData) => void;
}) {
  const [hovered, setHovered] = useState(false);

  const handleClick = (e: any) => {
    e.stopPropagation();
    onSelect?.({
      id,
      name: `CCTV MONITOR ${id.toUpperCase()}`,
      category: "INFRASTRUCTURE",
      position: [position[0], 8.5, position[2]],
      size: [2.2, 9.5, 1.5],
      status: "ACTIVE",
      statusColor: "#00d4ff",
      description: "Fixed urban CCTV pole streaming multi-lane junction traffic feeds to Central Traffic Operations.",
      metrics: [
        { label: "RESOLUTION", value: "4K UHD @ 60FPS" },
        { label: "AI ENGINE", value: "VEHICLE TRACKING" },
        { label: "STREAM", value: "RTSP ENCRYPTED" },
        { label: "UPTIME", value: "99.98%" },
      ],
      details: [
        "Continuous 24/7 recording enabled",
        "License plate OCR active",
        "Direct integration with BEL UrbanPulse Core",
      ],
    });
  };

  return (
    <group
      position={position}
      rotation={[0, rotationY, 0]}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = "default"; }}
    >
      <mesh position={[0, 4.5, 0]}>
        <cylinderGeometry args={[0.14, 0.18, 9.0, 12]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x1e293b} metalness={0.85} roughness={0.3} />
      </mesh>
      
      <mesh position={[0, 8.5, 0]}>
        <boxGeometry args={[0.35, 0.35, 0.35]} />
        <meshStandardMaterial color={0x0f172a} metalness={0.9} roughness={0.2} />
      </mesh>

      <mesh position={[0.9, 8.5, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.07, 0.07, 1.5, 10]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x1e293b} metalness={0.85} roughness={0.3} />
      </mesh>

      <group position={[1.65, 8.35, 0]} rotation={[0, 0, -0.2]}>
        <mesh>
          <boxGeometry args={[0.7, 0.35, 0.35]} />
          <meshStandardMaterial color={0x0f172a} metalness={0.9} roughness={0.2} />
        </mesh>
        
        <mesh position={[0.05, 0.2, 0]}>
          <boxGeometry args={[0.65, 0.04, 0.38]} />
          <meshStandardMaterial color={0x334155} />
        </mesh>
        
        <mesh position={[0.38, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.13, 0.13, 0.1, 12]} />
          <meshStandardMaterial color={0x000000} metalness={0.95} roughness={0.05} />
        </mesh>
      </group>
    </group>
  );
}

// ─── Roadside AI Camera Gantry ───────────────────────
function RoadsideAICamera({
  id,
  position,
  rotationY = 0,
  onSelect,
}: {
  id: string;
  position: [number, number, number];
  rotationY?: number;
  onSelect?: (asset: SelectedAssetData) => void;
}) {
  const [hovered, setHovered] = useState(false);

  const handleClick = (e: any) => {
    e.stopPropagation();
    onSelect?.({
      id,
      name: `AI GANTRY NODE ${id.toUpperCase()}`,
      category: "INFRASTRUCTURE",
      position: [position[0], 8.5, position[2]],
      size: [4.8, 9.2, 2.0],
      status: "ACTIVE",
      statusColor: "#00d4ff",
      description: "High-speed roadside Gantry AI processing unit executing edge model inference for speed enforcement & vehicle trajectory.",
      metrics: [
        { label: "INFERENCE TIME", value: "4.2 ms / FRAME" },
        { label: "ACCURACY", value: "98.4% OCR" },
        { label: "PROCESSOR", value: "NVIDIA JETSON ORIN" },
        { label: "RADAR STATE", value: "77 GHz DUAL-BAND" },
      ],
      details: [
        "Real-time violation detection active",
        "Vehicle count & density estimation",
        "Local event buffer synchronized",
      ],
    });
  };

  return (
    <group
      position={position}
      rotation={[0, rotationY, 0]}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { setHovered(false); document.body.style.cursor = "default"; }}
    >
      <mesh position={[0, 4.5, 0]}>
        <boxGeometry args={[0.5, 9, 0.5]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x1e293b} metalness={0.8} roughness={0.3} />
      </mesh>
      
      <mesh position={[-2, 8.5, 0]}>
        <boxGeometry args={[4.5, 0.35, 0.35]} />
        <meshStandardMaterial color={hovered ? 0x00d4ff : 0x1e293b} metalness={0.8} roughness={0.3} />
      </mesh>
      
      <mesh position={[0, 3, -0.35]}>
        <boxGeometry args={[0.8, 1.3, 0.45]} />
        <meshStandardMaterial color={0x0f172a} metalness={0.9} roughness={0.2} />
      </mesh>
    </group>
  );
}

// ─── Building Definition Data ─────────────────────────
interface BuildingConfig {
  id: string;
  name: string;
  pos: [number, number, number];
  size: [number, number, number];
  color: number;
  hasBalconies: boolean;
}

const BUILDINGS: BuildingConfig[] = [
  // Left side
  { id: "b-l-1", name: "Commercial Center A", pos: [-22, 8, -20], size: [8, 16, 15], color: 0x1e293b, hasBalconies: false },
  { id: "b-l-2", name: "Urban Heights Apartments", pos: [-22, 12, -40], size: [8, 24, 12], color: 0x0f172a, hasBalconies: true },
  { id: "b-l-3", name: "Tech Residency Block C", pos: [-23, 6, 0], size: [6, 12, 18], color: 0x334155, hasBalconies: true },
  { id: "b-l-4", name: "BEL Innovation Tower", pos: [-22, 18, -60], size: [10, 36, 14], color: 0x1e293b, hasBalconies: false },
  { id: "b-l-5", name: "Suburban Complex L5", pos: [-23, 5, 20], size: [6, 10, 20], color: 0x0f172a, hasBalconies: true },
  // Right side
  { id: "b-r-1", name: "Residential Block B", pos: [22, 10, -20], size: [8, 20, 15], color: 0x0f172a, hasBalconies: true },
  { id: "b-r-2", name: "Financial Plaza Tower 2", pos: [22, 14, -38], size: [8, 28, 12], color: 0x1e293b, hasBalconies: false },
  { id: "b-r-3", name: "Metro Suites & Offices", pos: [23, 7, 5], size: [6, 14, 18], color: 0x334155, hasBalconies: true },
  { id: "b-r-4", name: "Apex Horizon Center", pos: [22, 22, -55], size: [10, 44, 14], color: 0x0f172a, hasBalconies: false },
  { id: "b-r-5", name: "Eastside Residency R5", pos: [23, 5, 25], size: [7, 10, 20], color: 0x1e293b, hasBalconies: true },
];

// ─── High-Performance Instanced Building Windows & Balconies ─────────
function BuildingCitySystem({ onSelectAsset }: { onSelectAsset?: (asset: SelectedAssetData) => void }) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  // Compute all window matrices across city once
  const { litMatrices, unlitMatrices, balconySlabMatrices, balconyRailMatrices } = useMemo(() => {
    const lit: THREE.Matrix4[] = [];
    const unlit: THREE.Matrix4[] = [];
    const balcSlab: THREE.Matrix4[] = [];
    const balcRail: THREE.Matrix4[] = [];

    const dummy = new THREE.Object3D();

    BUILDINGS.forEach((b) => {
      const [bx, by, bz] = b.pos;
      const [w, h, d] = b.size;

      const floors = Math.floor(h / 2.8);
      const colsX = Math.floor(w / 2.2);

      for (let f = 1; f < floors; f++) {
        const wy = by - h / 2 + f * 2.8;

        for (let c = 0; c < colsX; c++) {
          const wx = bx - w / 2 + (c + 0.5) * (w / colsX);
          const isLit = (f * 7 + c * 3) % 3 !== 0;

          // Front window
          dummy.position.set(wx, wy, bz + d / 2 + 0.02);
          dummy.rotation.set(0, 0, 0);
          dummy.updateMatrix();
          if (isLit) lit.push(dummy.matrix.clone());
          else unlit.push(dummy.matrix.clone());

          // Back window
          dummy.position.set(wx, wy, bz - d / 2 - 0.02);
          dummy.rotation.set(0, Math.PI, 0);
          dummy.updateMatrix();
          if (isLit) lit.push(dummy.matrix.clone());
          else unlit.push(dummy.matrix.clone());

          // Balcony
          if (b.hasBalconies && f % 2 === 0 && (f + c) % 2 === 0) {
            dummy.position.set(wx, wy - 0.5, bz + d / 2 + 0.3);
            dummy.rotation.set(0, 0, 0);
            dummy.updateMatrix();
            balcSlab.push(dummy.matrix.clone());

            dummy.position.set(wx, wy - 0.25, bz + d / 2 + 0.58);
            dummy.rotation.set(0, 0, 0);
            dummy.updateMatrix();
            balcRail.push(dummy.matrix.clone());
          }
        }
      }
    });

    return {
      litMatrices: lit,
      unlitMatrices: unlit,
      balconySlabMatrices: balcSlab,
      balconyRailMatrices: balcRail,
    };
  }, []);

  // Refs for Instanced Meshes
  const litRef = useRef<THREE.InstancedMesh>(null);
  const unlitRef = useRef<THREE.InstancedMesh>(null);
  const slabRef = useRef<THREE.InstancedMesh>(null);
  const railRef = useRef<THREE.InstancedMesh>(null);

  useEffect(() => {
    if (litRef.current) {
      litMatrices.forEach((m, i) => litRef.current!.setMatrixAt(i, m));
      litRef.current.instanceMatrix.needsUpdate = true;
    }
    if (unlitRef.current) {
      unlitMatrices.forEach((m, i) => unlitRef.current!.setMatrixAt(i, m));
      unlitRef.current.instanceMatrix.needsUpdate = true;
    }
    if (slabRef.current) {
      balconySlabMatrices.forEach((m, i) => slabRef.current!.setMatrixAt(i, m));
      slabRef.current.instanceMatrix.needsUpdate = true;
    }
    if (railRef.current) {
      balconyRailMatrices.forEach((m, i) => railRef.current!.setMatrixAt(i, m));
      railRef.current.instanceMatrix.needsUpdate = true;
    }
  }, [litMatrices, unlitMatrices, balconySlabMatrices, balconyRailMatrices]);

  return (
    <group>
      {/* ── Main Building Structural Masses (10 Clickable Boxes) ── */}
      {BUILDINGS.map((b) => {
        const [w, h, d] = b.size;
        const isHovered = hoveredId === b.id;

        const handleClick = (e: any) => {
          e.stopPropagation();
          onSelectAsset?.({
            id: b.id,
            name: b.name,
            category: "BUILDING",
            position: [b.pos[0], b.pos[1], b.pos[2]],
            size: [w + 0.5, h + 0.5, d + 0.5],
            status: "MONITORED",
            statusColor: "#f59e0b",
            description: `Multi-story urban structural asset located along Central Avenue with real-time structural health & occupancy telemetry.`,
            metrics: [
              { label: "HEIGHT", value: `${Math.round(h * 3)} METERS` },
              { label: "EST. OCCUPANCY", value: "84%" },
              { label: "ENERGY RATING", value: "A+ SMART GRID" },
              { label: "STRUCTURAL SENSORS", value: "48 NODES ACTIVE" },
            ],
            details: [
              "Solar facade generation: 14.2 kWh",
              "HVAC load optimized by AI twin",
              "Air Quality Index (AQI): 42 (GOOD)",
            ],
          });
        };

        return (
          <group
            key={b.id}
            position={b.pos}
            onClick={handleClick}
            onPointerOver={(e) => { e.stopPropagation(); setHoveredId(b.id); document.body.style.cursor = "pointer"; }}
            onPointerOut={() => { setHoveredId(null); document.body.style.cursor = "default"; }}
          >
            {/* Building Mass */}
            <mesh>
              <boxGeometry args={[w, h, d]} />
              <meshStandardMaterial
                color={isHovered ? 0x3b82f6 : b.color}
                metalness={0.3}
                roughness={0.7}
              />
            </mesh>

            {/* Roof Parapet */}
            <mesh position={[0, h / 2 + 0.15, 0]}>
              <boxGeometry args={[w + 0.2, 0.3, d + 0.2]} />
              <meshStandardMaterial color={0x1e293b} roughness={0.8} />
            </mesh>

            {/* Rooftop HVAC Box */}
            <mesh position={[0, h / 2 + 0.6, 0]}>
              <boxGeometry args={[w * 0.4, 0.8, d * 0.4]} />
              <meshStandardMaterial color={0x334155} metalness={0.6} roughness={0.4} />
            </mesh>
          </group>
        );
      })}

      {/* ── Instanced Lit Windows (Rendered in 1 Draw Call) ── */}
      {litMatrices.length > 0 && (
        <instancedMesh ref={litRef} args={[undefined, undefined, litMatrices.length]}>
          <planeGeometry args={[0.9, 1.2]} />
          <meshBasicMaterial color={0xffea88} />
        </instancedMesh>
      )}

      {/* ── Instanced Unlit Windows (Rendered in 1 Draw Call) ── */}
      {unlitMatrices.length > 0 && (
        <instancedMesh ref={unlitRef} args={[undefined, undefined, unlitMatrices.length]}>
          <planeGeometry args={[0.9, 1.2]} />
          <meshStandardMaterial color={0x0f172a} metalness={0.9} roughness={0.1} />
        </instancedMesh>
      )}

      {/* ── Instanced Balcony Slabs & Rails (Rendered in 2 Draw Calls) ── */}
      {balconySlabMatrices.length > 0 && (
        <instancedMesh ref={slabRef} args={[undefined, undefined, balconySlabMatrices.length]}>
          <boxGeometry args={[1.1, 0.1, 0.6]} />
          <meshStandardMaterial color={0x334155} roughness={0.8} />
        </instancedMesh>
      )}
      {balconyRailMatrices.length > 0 && (
        <instancedMesh ref={railRef} args={[undefined, undefined, balconyRailMatrices.length]}>
          <planeGeometry args={[1.06, 0.4]} />
          <meshStandardMaterial color={0x38bdf8} transparent opacity={0.4} side={THREE.DoubleSide} />
        </instancedMesh>
      )}
    </group>
  );
}

// ─── Pothole ──────────────────────────────────────────────────
function Pothole({
  position,
  visible,
  onSelect,
}: {
  position: [number, number, number];
  visible: boolean;
  onSelect?: (asset: SelectedAssetData) => void;
}) {
  if (!visible) return null;

  const handleClick = (e: any) => {
    e.stopPropagation();
    onSelect?.({
      id: "pothole-01",
      name: "ROAD DEFECT #PO-142",
      category: "INCIDENT",
      position: [position[0], 0.2, position[2]],
      size: [1.8, 0.5, 1.8],
      status: "VIOLATION",
      statusColor: "#ff4d4d",
      description: "Severe asphalt pothole detected by bus fleet AI optical sensors. Work order dispatched to municipal repair crew.",
      metrics: [
        { label: "DEPTH", value: "4.8 CM" },
        { label: "AREA", value: "0.42 M²" },
        { label: "CONFIDENCE", value: "96.4%" },
        { label: "DISCOVERED BY", value: "BUS-017 & BUS-023" },
      ],
      details: [
        "First detected: 10:05 AM today",
        "Corroborated by 2 independent mobile edge cameras",
        "Work Order #WO-8891 assigned to Public Works",
      ],
    });
  };

  return (
    <group
      position={position}
      onClick={handleClick}
      onPointerOver={(e) => { e.stopPropagation(); document.body.style.cursor = "pointer"; }}
      onPointerOut={() => { document.body.style.cursor = "default"; }}
    >
      <mesh position={[0, -0.01, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <circleGeometry args={[0.6, 16]} />
        <meshBasicMaterial color={0x010203} />
      </mesh>
      <mesh position={[0, 0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.65, 0.75, 24]} />
        <meshBasicMaterial color={0xff6600} opacity={0.85} transparent />
      </mesh>
    </group>
  );
}

// ─── Main road environment ────────────────────────────────────
export default function RoadEnvironment({
  progressRef,
  mode,
  onSelectAsset,
}: RoadEnvironmentProps) {
  return (
    <group>
      {/* Asphalt road surface */}
      <mesh position={[0, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[12, 160, 2, 40]} />
        <meshStandardMaterial
          color={0x1e293b}
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Sidewalks */}
      {[-8, 8].map((x, i) => (
        <mesh key={i} position={[x, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[3.5, 160]} />
          <meshStandardMaterial color={0x0f172a} roughness={0.9} />
        </mesh>
      ))}

      {/* Road lane markings */}
      <LaneMarkings />

      {/* Zebra crossing */}
      <ZebraCrossing position={[0, 0, -22]} />

      {/* Pothole */}
      <Pothole position={[2.5, 0, -8]} visible={true} onSelect={onSelectAsset} />

      {/* Street lamps — left & right */}
      {[-35, -20, -5, 10, 25, 40].map((z, i) => (
        <StreetPole key={`sl${i}`} id={`lamp-l-${i}`} position={[-7, 0, z]} onSelect={onSelectAsset} />
      ))}
      {[-35, -20, -5, 10, 25, 40].map((z, i) => (
        <StreetPole key={`sr${i}`} id={`lamp-r-${i}`} position={[7, 0, z]} rotationY={Math.PI} onSelect={onSelectAsset} />
      ))}

      {/* CCTV Poles */}
      <CCTVPole id="cctv-01" position={[6.8, 0, -15]} rotationY={Math.PI} onSelect={onSelectAsset} />
      <CCTVPole id="cctv-02" position={[-6.8, 0, -45]} onSelect={onSelectAsset} />
      
      {/* Roadside AI Camera Gantries */}
      <RoadsideAICamera id="gantry-01" position={[7.5, 0, 5]} rotationY={Math.PI} onSelect={onSelectAsset} />
      <RoadsideAICamera id="gantry-02" position={[-7.5, 0, -35]} onSelect={onSelectAsset} />

      {/* Ultra-Fast Instanced City Buildings (Windows & Balconies rendered in ~4 draw calls total) */}
      <BuildingCitySystem onSelectAsset={onSelectAsset} />

      {/* Ground plane extend */}
      <mesh position={[0, -0.02, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[200, 200]} />
        <meshStandardMaterial color={0x030712} roughness={1} />
      </mesh>
    </group>
  );
}
