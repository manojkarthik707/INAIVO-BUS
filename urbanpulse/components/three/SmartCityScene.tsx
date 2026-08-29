"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Fog, AdditiveBlending } from "three";
import * as THREE from "three";
import { MapControls } from "@react-three/drei";
import RoadEnvironment from "./RoadEnvironment";
import VehicleSystem from "./VehicleSystem";
import AIOverlayLayer from "./AIOverlayLayer";
import CameraController from "./CameraController";

interface SmartCityScenesProps {
  progressRef: React.MutableRefObject<number>;
  mode: "parallax" | "360";
}

function SceneFog() {
  const { scene } = useThree();
  useMemo(() => {
    scene.fog = new THREE.FogExp2(0xddeeff, 0.008);
    scene.background = new THREE.Color(0xddeeff);
  }, [scene]);
  return null;
}

function AtmosphericLighting() {
  return (
    <>
      {/* Ambient — bright day */}
      <ambientLight color={0xffffff} intensity={2.5} />

      {/* Main directional — sun */}
      <directionalLight
        position={[30, 50, -20]}
        color={0xffeedd}
        intensity={3.5}
        castShadow={true}
      />

      {/* Secondary fill — sky reflection */}
      <directionalLight
        position={[-20, 30, 20]}
        color={0xccddff}
        intensity={1.2}
        castShadow={false}
      />

      {/* Street lamp warm pools — point lights along road */}
      {[-20, -8, 4, 16, 28].map((z, i) => (
        <pointLight
          key={i}
          position={[8, 5, z]}
          color={0xffaa44}
          intensity={0.8}
          distance={14}
          decay={2}
        />
      ))}
      {[-20, -8, 4, 16, 28].map((z, i) => (
        <pointLight
          key={`r${i}`}
          position={[-8, 5, z]}
          color={0xffaa44}
          intensity={0.8}
          distance={14}
          decay={2}
        />
      ))}

      {/* Blue AI glow — centered above road */}
      <pointLight
        position={[0, 8, 0]}
        color={0x0066ff}
        intensity={1.2}
        distance={30}
        decay={2}
      />
    </>
  );
}

export default function SmartCityScene({ progressRef, mode }: SmartCityScenesProps) {
  return (
    <Canvas
      camera={{ position: [0, 45, 60], fov: 45, near: 0.1, far: 400 }}
      gl={{
        antialias: true,
        alpha: false,
        powerPreference: "high-performance",
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 0.9,
      }}
      shadows={false}
      style={{ width: "100%", height: "100%" }}
      dpr={[1, 1.5]}
    >
      <SceneFog />
      <AtmosphericLighting />
      
      {mode === "360" ? (
        <MapControls
          enableDamping={true}
          dampingFactor={0.05}
          minDistance={5}
          maxDistance={120}
          maxPolarAngle={Math.PI / 2.1}
          target={[0, 0, 0]}
        />
      ) : (
        <CameraController progressRef={progressRef} />
      )}

      <RoadEnvironment mode={mode} progressRef={progressRef} />
      <VehicleSystem mode={mode} progressRef={progressRef} />
      <AIOverlayLayer mode={mode} progressRef={progressRef} />
    </Canvas>
  );
}
