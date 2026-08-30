"use client";

import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import { Html } from "@react-three/drei";
import * as THREE from "three";

export interface SelectedAssetData {
  id: string;
  name: string;
  category: "VEHICLE" | "INFRASTRUCTURE" | "BUILDING" | "INCIDENT";
  position: [number, number, number];
  size: [number, number, number];
  status: "VIOLATION" | "ACTIVE" | "NOMINAL" | "ALERT" | "MONITORED";
  statusColor?: string;
  description: string;
  metrics: { label: string; value: string; highlight?: boolean }[];
  details: string[];
}

interface SelectionHighlightProps {
  asset: SelectedAssetData | null;
  onDeselect: () => void;
}

export default function SelectionHighlight({ asset, onDeselect }: SelectionHighlightProps) {
  const boxRef = useRef<THREE.Group>(null);
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    if (!boxRef.current) return;
    timeRef.current += delta;
    // Subtle breathing pulse for selection box
    const scalePulse = 1 + 0.02 * Math.sin(timeRef.current * 4);
    boxRef.current.scale.setScalar(scalePulse);
  });

  if (!asset) return null;

  const [x, y, z] = asset.position;
  const [w, h, d] = asset.size;

  const halfW = w / 2 + 0.15;
  const halfH = h / 2 + 0.15;
  const halfD = d / 2 + 0.15;

  const cyanColor = asset.statusColor || "#00d4ff";

  // Create 12 edges for box wireframe
  const edges = [
    // Top rectangle
    [[-halfW, halfH, -halfD], [halfW, halfH, -halfD]],
    [[halfW, halfH, -halfD], [halfW, halfH, halfD]],
    [[halfW, halfH, halfD], [-halfW, halfH, halfD]],
    [[-halfW, halfH, halfD], [-halfW, halfH, -halfD]],
    // Bottom rectangle
    [[-halfW, -halfH, -halfD], [halfW, -halfH, -halfD]],
    [[halfW, -halfH, -halfD], [halfW, -halfH, halfD]],
    [[halfW, -halfH, halfD], [-halfW, -halfH, halfD]],
    [[-halfW, -halfH, halfD], [-halfW, -halfH, -halfD]],
    // Vertical legs
    [[-halfW, -halfH, -halfD], [-halfW, halfH, -halfD]],
    [[halfW, -halfH, -halfD], [halfW, halfH, -halfD]],
    [[halfW, -halfH, halfD], [halfW, halfH, halfD]],
    [[-halfW, -halfH, halfD], [-halfW, halfH, halfD]],
  ];

  return (
    <group position={[x, y, z]}>
      {/* Selection Box Group */}
      <group ref={boxRef}>
        {/* Wireframe edges */}
        {edges.map(([p1, p2], idx) => {
          const v1 = new THREE.Vector3(...p1);
          const v2 = new THREE.Vector3(...p2);
          const dist = v1.distanceTo(v2);
          const mid = v1.clone().add(v2).multiplyScalar(0.5);

          // Direction rotation
          const dir = v2.clone().sub(v1).normalize();
          const quaternion = new THREE.Quaternion();
          quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);

          return (
            <mesh key={idx} position={mid} quaternion={quaternion}>
              <cylinderGeometry args={[0.02, 0.02, dist, 6]} />
              <meshBasicMaterial color={cyanColor} />
            </mesh>
          );
        })}

        {/* 8 Corner Brackets */}
        {[
          [-halfW, halfH, -halfD],
          [halfW, halfH, -halfD],
          [halfW, halfH, halfD],
          [-halfW, halfH, halfD],
          [-halfW, -halfH, -halfD],
          [halfW, -halfH, -halfD],
          [halfW, -halfH, halfD],
          [-halfW, -halfH, halfD],
        ].map(([cx, cy, cz], idx) => (
          <mesh key={`c-${idx}`} position={[cx, cy, cz]}>
            <boxGeometry args={[0.15, 0.15, 0.15]} />
            <meshBasicMaterial color={cyanColor} />
          </mesh>
        ))}

        {/* Semi-transparent inner glow plane */}
        <mesh>
          <boxGeometry args={[w, h, d]} />
          <meshBasicMaterial color={cyanColor} transparent opacity={0.06} side={THREE.DoubleSide} />
        </mesh>
      </group>

      {/* ── Callout Line & Floating Label (Matching Image 2) ── */}
      <group position={[0, halfH, 0]}>
        {/* Vertical riser */}
        <mesh position={[0, 0.75, 0]}>
          <cylinderGeometry args={[0.015, 0.015, 1.5, 6]} />
          <meshBasicMaterial color={cyanColor} />
        </mesh>
        {/* Horizontal pointer arm */}
        <mesh position={[-0.6, 1.5, 0]} rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.015, 0.015, 1.2, 6]} />
          <meshBasicMaterial color={cyanColor} />
        </mesh>

        {/* Floating Callout HTML Tag */}
        <Html position={[-1.3, 1.6, 0]} center distanceFactor={25}>
          <div
            className="flex items-center gap-2 px-3 py-1.5 rounded border whitespace-nowrap shadow-xl cursor-pointer select-none"
            onClick={(e) => {
              e.stopPropagation();
            }}
            style={{
              background: "rgba(5, 12, 24, 0.92)",
              borderColor: cyanColor,
              backdropFilter: "blur(8px)",
              boxShadow: `0 0 15px ${cyanColor}44`,
            }}
          >
            <span className="w-2 h-2 rounded-full animate-ping" style={{ background: cyanColor }} />
            <div className="flex flex-col">
              <span className="text-[10px] font-mono tracking-wider text-cyan-300 font-bold uppercase">
                {asset.category}
              </span>
              <span className="text-xs font-bold text-white tracking-wide">
                {asset.name}
              </span>
            </div>
            <span
              className="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ml-1"
              style={{
                background: asset.status === "VIOLATION" ? "rgba(255, 64, 64, 0.2)" : "rgba(0, 212, 255, 0.2)",
                color: asset.status === "VIOLATION" ? "#ff4d4d" : cyanColor,
                border: `1px solid ${asset.status === "VIOLATION" ? "#ff4d4d" : cyanColor}`,
              }}
            >
              {asset.status}
            </span>
          </div>
        </Html>
      </group>
    </group>
  );
}
