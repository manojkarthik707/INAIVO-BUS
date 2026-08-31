"use client";

import Section from "@/components/layout/Section";

export default function HeroSection() {
  return (
    <Section
      id="hero"
      className="relative min-h-screen flex flex-col justify-center items-center overflow-hidden"
    >
      {/* Background Video */}
      <video
        autoPlay
        muted
        loop
        playsInline
        preload="auto"
        disablePictureInPicture
        className="absolute inset-0 w-full h-full object-cover z-0"
        style={{
          transform: "translate3d(0, 0, 0)",
          willChange: "transform"
        }}
      >
        <source src="/landing page background video.mp4" type="video/mp4" />
      </video>
      
      {/* Dark overlay to ensure the white text is readable, just like the reference image */}
      <div className="absolute inset-0 bg-black/40 z-10" />

      {/* Content - Styled like the reference image */}
      <div className="relative z-20 flex flex-col items-center justify-center text-center max-w-5xl mx-4 px-4 w-full pt-16">
        <h1 
          className="text-5xl md:text-7xl lg:text-[5.5rem] font-bold text-white mb-6 tracking-tight leading-tight"
          style={{ textShadow: "0 2px 10px rgba(0,0,0,0.3)" }}
        >
          UrbanPulse Fusion
        </h1>
        
        <p 
          className="text-xl md:text-3xl text-white font-medium max-w-4xl leading-snug mb-10"
          style={{ textShadow: "0 2px 8px rgba(0,0,0,0.3)" }}
        >
          AI-Powered Urban Intelligence Platform Transforming Public Transport Vision Into A Shared City Memory.
        </p>

        <a
          href="#simulation"
          className="inline-flex items-center justify-center px-8 py-3.5 rounded-full text-white font-semibold text-lg transition-transform hover:scale-105"
          style={{
            backgroundColor: "#024c3a", // Dark green from the reference image
          }}
        >
          See Our Story
        </a>
      </div>
    </Section>
  );
}
