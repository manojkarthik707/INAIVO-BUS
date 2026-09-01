"use client";

import { useEffect, useState } from "react";

export default function Navigation() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 w-full z-[100] transition-all duration-300 ease-out ${
        scrolled
          ? "bg-[rgba(3,5,8,0.75)] backdrop-blur-[16px] border-b border-white/5 py-4"
          : "bg-transparent py-6"
      }`}
    >
      <div className="w-full max-w-[1600px] mx-auto px-6 md:px-12 flex items-center justify-between">
        
        {/* INETRA Logo */}
        <div className="flex items-center gap-3 cursor-pointer group">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src="/INETRA LOGO.jpeg"
            alt="INETRA"
            className="h-12 w-auto object-contain"
            style={{ mixBlendMode: "screen" }}
          />
          <span className="font-display font-bold text-xl tracking-tight text-white group-hover:text-blue-400 transition-colors">
            INETRA
          </span>
        </div>

        {/* CTA Button */}
        <div className="flex items-center gap-4">
          <button 
            className="hidden md:flex flex-col items-center justify-center w-[52px] h-[52px] rounded-full border-[2.5px] border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white transition-all duration-300 shadow-[0_0_15px_rgba(59,130,246,0.3)] hover:shadow-[0_0_20px_rgba(59,130,246,0.6)] group"
            title="Live Demo"
          >
            {/* Play Icon with rounded corners */}
            <svg viewBox="0 0 24 24" className="w-5 h-5 fill-current mb-0.5 stroke-current" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round">
              <path d="M8 6.82v10.36c0 .79.86 1.28 1.54.88l8.8-5.18a1 1 0 000-1.76l-8.8-5.18c-.68-.4-1.54.09-1.54.88z" stroke="none" />
            </svg>
            <span className="font-bold text-[9px] tracking-wider leading-none">
              DEMO
            </span>
          </button>
          
          {/* Mobile menu icon */}
          <button className="lg:hidden text-white/80 hover:text-white p-2 flex-shrink-0">
            <i className="bi bi-list text-2xl"></i>
          </button>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="text-[14px] font-body font-medium text-gray-400 hover:text-white transition-colors tracking-wide"
    >
      {children}
    </a>
  );
}
