"use client";

import { useRef, useMemo, useState } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

interface AIOverlayLayerProps {
  progressRef: React.MutableRefObject<number>;
  mode: "parallax" | "360";
}

// ─── Detection box (3D plane with emissive border) ───────────
function DetectionBox({
  position,
  size,
  color,
  visible,
  pulsing = false,
}: {
  position: [number, number, number];
  size: [number, number];
  color: number;
  visible: boolean;
  pulsing?: boolean;
}) {
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    if (!matRef.current || !pulsing) return;
    timeRef.current += delta;
    matRef.current.opacity = 0.5 + 0.4 * Math.sin(timeRef.current * 3);
  });

  if (!visible) return null;

  const [w, h] = size;

  // Build box outline from 4 thin planes
  return (
    <group position={position}>
      {/* Top edge */}
      <mesh position={[0, h / 2, 0]}>
        <planeGeometry args={[w, 0.06]} />
        <meshBasicMaterial ref={matRef} color={color} opacity={0.9} transparent side={THREE.DoubleSide} />
      </mesh>
      {/* Bottom edge */}
      <mesh position={[0, -h / 2, 0]}>
        <planeGeometry args={[w, 0.06]} />
        <meshBasicMaterial color={color} opacity={0.9} transparent side={THREE.DoubleSide} />
      </mesh>
      {/* Left edge */}
      <mesh position={[-w / 2, 0, 0]}>
        <planeGeometry args={[0.06, h]} />
        <meshBasicMaterial color={color} opacity={0.9} transparent side={THREE.DoubleSide} />
      </mesh>
      {/* Right edge */}
      <mesh position={[w / 2, 0, 0]}>
        <planeGeometry args={[0.06, h]} />
        <meshBasicMaterial color={color} opacity={0.9} transparent side={THREE.DoubleSide} />
      </mesh>
      {/* Corner accents */}
      {[[-w / 2, h / 2], [w / 2, h / 2], [-w / 2, -h / 2], [w / 2, -h / 2]].map(([cx, cy], i) => (
        <mesh key={i} position={[cx, cy, 0]}>
          <planeGeometry args={[0.15, 0.15]} />
          <meshBasicMaterial color={color} opacity={1} transparent side={THREE.DoubleSide} />
        </mesh>
      ))}
    </group>
  );
}

// ─── Trajectory arrow path ───────────────────────────────────
function TrajectoryArrow({
  points,
  color,
  visible,
}: {
  points: THREE.Vector3[];
  color: number;
  visible: boolean;
}) {
  const timeRef = useRef(0);

  const lineObj = useMemo(() => {
    const geo = new THREE.BufferGeometry().setFromPoints(points);
    const mat = new THREE.LineBasicMaterial({ color, opacity: 0.8, transparent: true });
    return new THREE.Line(geo, mat);
  }, [points, color]);

  useFrame((_, delta) => {
    timeRef.current += delta;
    (lineObj.material as THREE.LineBasicMaterial).opacity =
      0.4 + 0.5 * Math.sin(timeRef.current * 2);
  });

  if (!visible) return null;

  return <primitive object={lineObj} />;
}

// ─── Floating event packet (sphere that flies from vehicle to map) ──
function EventPacket({
  from,
  to,
  color,
  visible,
}: {
  from: THREE.Vector3;
  to: THREE.Vector3;
  color: number;
  visible: boolean;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const tRef = useRef(0);

  useFrame((_, delta) => {
    if (!meshRef.current || !visible) return;
    tRef.current = (tRef.current + delta * 0.4) % 1;
    const t = tRef.current;
    meshRef.current.position.lerpVectors(from, to, t);
    const arc = Math.sin(t * Math.PI) * 4;
    meshRef.current.position.y += arc;
    meshRef.current.scale.setScalar(0.5 + 0.5 * Math.sin(t * Math.PI));
  });

  if (!visible) return null;

  return (
    <mesh ref={meshRef} position={from}>
      <sphereGeometry args={[0.15, 10, 10]} />
      <meshBasicMaterial color={color} />
    </mesh>
  );
}

// ─── Lane segmentation overlay ───────────────────────────────
function LaneSegmentation({ visible }: { visible: boolean }) {
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    if (!matRef.current) return;
    timeRef.current += delta;
    matRef.current.opacity = 0.06 + 0.03 * Math.sin(timeRef.current * 1.5);
  });

  if (!visible) return null;

  return (
    <mesh position={[-3, 0.05, -5]} rotation={[-Math.PI / 2, 0, 0]}>
      <planeGeometry args={[5.5, 40]} />
      <meshBasicMaterial ref={matRef} color={0x00aaff} opacity={0.08} transparent />
    </mesh>
  );
}

// ─── Pothole highlight ────────────────────────────────────────
function PotholeHighlight({ visible }: { visible: boolean }) {
  const matRef = useRef<THREE.MeshBasicMaterial>(null);
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    if (!matRef.current) return;
    timeRef.current += delta;
    matRef.current.opacity = 0.5 + 0.4 * Math.abs(Math.sin(timeRef.current * 2.5));
  });

  if (!visible) return null;

  return (
    <mesh position={[2.5, 0.05, -8]} rotation={[-Math.PI / 2, 0, 0]}>
      <circleGeometry args={[1.2, 32]} />
      <meshBasicMaterial ref={matRef} color={0xff6600} opacity={0.6} transparent />
    </mesh>
  );
}

// ─── Urban object merge node ──────────────────────────────────
function UrbanObjectNode({ visible }: { visible: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    if (!meshRef.current) return;
    timeRef.current += delta;
    const scale = 0.8 + 0.4 * Math.sin(timeRef.current * 2);
    meshRef.current.scale.setScalar(visible ? scale : 0);
  });

  return (
    <group position={[2.5, 3, -8]}>
      <mesh ref={meshRef}>
        <octahedronGeometry args={[0.4, 0]} />
        <meshBasicMaterial color={0x00ff88} opacity={0.9} transparent />
      </mesh>
      {/* Orbit ring */}
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.8, 0.02, 8, 32]} />
        <meshBasicMaterial color={0x00ff88} opacity={visible ? 0.4 : 0} transparent />
      </mesh>
    </group>
  );
}

// ─── Grid overlay for digital twin view ──────────────────────
function DigitalTwinGrid({ visible }: { visible: boolean }) {
  const gridPoints = useMemo(() => {
    const pts: THREE.Vector3[] = [];
    for (let x = -40; x <= 40; x += 10) {
      pts.push(new THREE.Vector3(x, 0.1, -80));
      pts.push(new THREE.Vector3(x, 0.1, 80));
    }
    for (let z = -80; z <= 80; z += 10) {
      pts.push(new THREE.Vector3(-40, 0.1, z));
      pts.push(new THREE.Vector3(40, 0.1, z));
    }
    return pts;
  }, []);

  const geo = useMemo(() => {
    const g = new THREE.BufferGeometry().setFromPoints(gridPoints);
    return g;
  }, [gridPoints]);

  if (!visible) return null;

  return (
    <lineSegments geometry={geo}>
      <lineBasicMaterial color={0x0044aa} opacity={0.2} transparent />
    </lineSegments>
  );
}

// ─── Main AI overlay controller ───────────────────────────────
export default function AIOverlayLayer({ progressRef, mode }: AIOverlayLayerProps) {
  const [showBusPerception, setShowBusPerception] = useState(mode === "360");
  const [showPothole, setShowPothole] = useState(mode === "360");
  const [showUrbanObject, setShowUrbanObject] = useState(mode === "360");
  const [showEventPacket, setShowEventPacket] = useState(false);
  const [showTwinGrid, setShowTwinGrid] = useState(false);

  const trajectoryPoints = useMemo(
    () => [
      new THREE.Vector3(4, 0.5, 5),
      new THREE.Vector3(4.5, 0.5, 0),
      new THREE.Vector3(5, 0.5, -8),
    ],
    []
  );

  const packetFrom = useMemo(() => new THREE.Vector3(-2, 3, 10), []);
  const packetTo = useMemo(() => new THREE.Vector3(2.5, 4, -8), []);

  useFrame(() => {
    if (mode === "360") {
      if (!showBusPerception) {
        setShowBusPerception(true);
        setShowPothole(true);
        setShowUrbanObject(true);
        setShowEventPacket(false);
        setShowTwinGrid(false);
      }
      return;
    }

    const progress = progressRef.current;
    setShowBusPerception(progress > 0.1 && progress < 0.43);
    setShowPothole(progress > 0.12 && progress < 0.5);
    setShowUrbanObject(progress > 0.3 && progress < 0.58);
    setShowEventPacket(progress > 0.3 && progress < 0.45);
    setShowTwinGrid(progress > 0.86);
  });

  return (
    <group>
      {/* Vehicle detection boxes */}
      <group rotation={[0, 0, 0]} position={[-4.5, 1, -15]}>
        <DetectionBox
          position={[0, 0.8, 0]}
          size={[2.2, 1.8]}
          color={0x00aaff}
          visible={showBusPerception}
        />
      </group>

      <group position={[4.5, 1, -10]}>
        <DetectionBox
          position={[0, 0.6, 0]}
          size={[2.0, 1.4]}
          color={0x00aaff}
          visible={showBusPerception}
        />
      </group>

      {/* Removed Pothole DetectionBox as requested (only orange circle remains) */}

      {/* Lane segmentation */}
      <LaneSegmentation visible={showBusPerception} />

      {/* Pothole pulse ring */}
      <PotholeHighlight visible={showPothole} />

      {/* Event packet flying to map node */}
      <EventPacket
        from={packetFrom}
        to={packetTo}
        color={0x00d4ff}
        visible={showEventPacket}
      />

      {/* Urban Object node (appears after merge) */}
      <UrbanObjectNode visible={showUrbanObject} />

      {/* Vehicle trajectory */}
      <TrajectoryArrow
        points={trajectoryPoints}
        color={0x00d4ff}
        visible={showBusPerception}
      />

      {/* Digital twin grid */}
      <DigitalTwinGrid visible={showTwinGrid} />
    </group>
  );
}
