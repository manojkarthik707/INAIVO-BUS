"use client";

import { useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

// ─── Camera keyframes for scroll stages ─────────────────────
// Each keyframe: [progress, position, lookAt]
const CAMERA_KEYFRAMES = [
  // 0.00 — Stage 1: EDGE AI (Elevated cinematic descent)
  { p: 0.00, pos: new THREE.Vector3(0, 30, 45), target: new THREE.Vector3(0, 0, 10) },
  
  // 0.12 — Stage 2: EVENT GENERATION (Tracking close behind a bus, looking ahead)
  { p: 0.12, pos: new THREE.Vector3(-2, 4, 25), target: new THREE.Vector3(-2, 2.5, 0) },
  
  // 0.25 — Stage 3: CONFIDENCE & VERIFICATION (Lower road view, sweeping past events)
  { p: 0.25, pos: new THREE.Vector3(-2, 3, 10), target: new THREE.Vector3(-2, 1.5, -15) },
  
  // 0.38 — Stage 4: MESH SYSTEM (Pulling right to observe cross-lane corroboration)
  { p: 0.38, pos: new THREE.Vector3(6, 5, 2), target: new THREE.Vector3(0, 1, -20) },
  
  // 0.50 — Stage 5: ACTIONABLE ALERTS (Rising to reveal the distributed network)
  { p: 0.50, pos: new THREE.Vector3(12, 10, -5), target: new THREE.Vector3(-5, 2, -30) },
  
  // 0.63 — Stage 6: TRAFFIC ANALYSIS (Sweeping left to an authoritative "CCTV" angle)
  { p: 0.63, pos: new THREE.Vector3(-12, 18, -10), target: new THREE.Vector3(0, 0, -35) },
  
  // 0.75 — Stage 7: INSIGHTS & REPORTS (Pulling back to isometric traffic view)
  { p: 0.75, pos: new THREE.Vector3(-8, 28, 5), target: new THREE.Vector3(5, 0, -25) },
  
  // 0.88 — Stage 8: SERVER / PLATFORM (Centralizing, high data view)
  { p: 0.88, pos: new THREE.Vector3(0, 40, 15), target: new THREE.Vector3(0, 0, -20) },
  
  // 1.00 — FINAL: CITY DATABASE (Majestic, stable city-wide view)
  { p: 1.00, pos: new THREE.Vector3(0, 48, 20), target: new THREE.Vector3(0, 0, -20) },
];

function lerpKeyframes(progress: number) {
  let kfA = CAMERA_KEYFRAMES[0];
  let kfB = CAMERA_KEYFRAMES[1];

  for (let i = 0; i < CAMERA_KEYFRAMES.length - 1; i++) {
    if (progress >= CAMERA_KEYFRAMES[i].p && progress <= CAMERA_KEYFRAMES[i + 1].p) {
      kfA = CAMERA_KEYFRAMES[i];
      kfB = CAMERA_KEYFRAMES[i + 1];
      break;
    }
  }

  const range = kfB.p - kfA.p;
  const t = range === 0 ? 1 : (progress - kfA.p) / range;
  const smooth = t * t * (3 - 2 * t); // smoothstep interpolation

  return {
    pos: kfA.pos.clone().lerp(kfB.pos, smooth),
    target: kfA.target.clone().lerp(kfB.target, smooth),
  };
}

interface CameraControllerProps {
  progressRef: React.MutableRefObject<number>;
}

export default function CameraController({ progressRef }: CameraControllerProps) {
  const { camera } = useThree();
  const currentPos = useRef(new THREE.Vector3(0, 14, 38));
  const currentTarget = useRef(new THREE.Vector3(0, 0, 0));
  const timeRef = useRef(0);

  useFrame((_, delta) => {
    timeRef.current += delta;
    const progress = progressRef.current;
    const { pos, target } = lerpKeyframes(progress);

    // Subtle ambient sway
    const drift = Math.sin(timeRef.current * 0.3) * 0.08;
    pos.x += drift;

    // Delta-time independent smooth exponential lerp
    const lerpFactor = Math.min(1, 1 - Math.exp(-5 * delta));
    currentPos.current.lerp(pos, lerpFactor);
    currentTarget.current.lerp(target, lerpFactor);

    camera.position.copy(currentPos.current);
    camera.lookAt(currentTarget.current);
  });

  return null;
}
