"use client";

import { useRef } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "three";

// ─── Camera keyframes for scroll stages ─────────────────────
// Each keyframe: [progress, position, lookAt]
const CAMERA_KEYFRAMES = [
  // 0.00 — elevated overview looking down road
  { p: 0.00, pos: new THREE.Vector3(0, 14, 38), target: new THREE.Vector3(0, 0, 0) },
  
  // 0.10 — Mobile Perception Start (Hover in front of the bus, looking at dashcam)
  { p: 0.10, pos: new THREE.Vector3(-2, 3, 11), target: new THREE.Vector3(-2, 2.3, 17) },
  
  // 0.20 — Mobile Perception Ongoing (Tracking the moving bus from the front)
  { p: 0.20, pos: new THREE.Vector3(-2, 3, 2), target: new THREE.Vector3(-2, 2.3, 8) },
  
  // 0.30 — Exit bus and view Pothole / Urban Memory
  { p: 0.30, pos: new THREE.Vector3(3, 4, 8), target: new THREE.Vector3(0, 0, -5) },
  
  // 0.43 — glide to intersection, raise toward junction cam
  { p: 0.43, pos: new THREE.Vector3(-12, 9, -5), target: new THREE.Vector3(0, 2, -20) },
  
  // 0.58 — wider city block perspective
  { p: 0.58, pos: new THREE.Vector3(-8, 14, -15), target: new THREE.Vector3(0, 2, -25) },
  
  // 0.72 — back to road level for incident
  { p: 0.72, pos: new THREE.Vector3(4, 5, 5), target: new THREE.Vector3(10, 2, -10) },
  
  // 0.86 — pull up for city twin view
  { p: 0.86, pos: new THREE.Vector3(0, 35, 20), target: new THREE.Vector3(0, 0, -10) },
  
  // 0.94 — steady city view for closed loop
  { p: 0.94, pos: new THREE.Vector3(0, 40, 15), target: new THREE.Vector3(0, 0, -15) },
  
  // 1.00 — final position
  { p: 1.00, pos: new THREE.Vector3(0, 40, 15), target: new THREE.Vector3(0, 0, -15) },
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
