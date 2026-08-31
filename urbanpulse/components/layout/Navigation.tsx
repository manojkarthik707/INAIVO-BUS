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
        
        {/* Geometric Logo */}
        <div className="flex items-center gap-3 cursor-pointer group">
          <div className="relative w-8 h-8">
            <div className="absolute inset-0 border-2 border-white/80 rounded-md rotate-45 group-hover:rotate-90 transition-transform duration-500 ease-in-out"></div>
            <div className="absolute inset-2 bg-blue-500 rounded-sm rotate-45 group-hover:bg-cyan-400 transition-colors duration-500"></div>
          </div>
          <span className="font-display font-bold text-lg tracking-tight text-white group-hover:text-blue-400 transition-colors">
            UrbanPulse
          </span>
        </div>

        {/* CTA Button */}
        <div className="flex items-center gap-4">
          <button className="hidden md:flex bg-blue-500 hover:bg-blue-600 text-white font-body font-semibold text-[15px] h-12 px-8 rounded-full items-center justify-center transition-colors shadow-[0_0_20px_rgba(47,129,247,0.3)] flex-shrink-0 whitespace-nowrap">
            View Demo
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
