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
