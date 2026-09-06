"use client";

import { useState, useEffect, useCallback, useRef, memo } from "react";
import Section from "@/components/layout/Section";
import { QA_DATA, type QAItem } from "@/data/qaData";

// ─── QA Card ──────────────────────────────────────────────────────────────
const QACard = memo(function QACard({
  item,
  position, // "center" | "left" | "right" | "far-left" | "far-right"
  index,
  total,
  onClick,
}: {
  item: QAItem;
  position: string;
  index: number;
  total: number;
  onClick: (idx: number) => void;
}) {
  const positionStyles: Record<string, React.CSSProperties> = {
    "far-left": {
      transform: "translateX(-110%) rotateY(45deg) scale(0.7)",
      opacity: 0.15,
      zIndex: 1,
      pointerEvents: "none",
    },
    left: {
      transform: "translateX(-65%) rotateY(30deg) scale(0.85)",
      opacity: 0.6,
      zIndex: 2,
      pointerEvents: "auto",
    },
    center: {
      transform: "translateX(0%) rotateY(0deg) scale(1)",
      opacity: 1,
      zIndex: 10,
      pointerEvents: "auto",
    },
    right: {
      transform: "translateX(65%) rotateY(-30deg) scale(0.85)",
      opacity: 0.6,
      zIndex: 2,
      pointerEvents: "auto",
    },
    "far-right": {
      transform: "translateX(110%) rotateY(-45deg) scale(0.7)",
      opacity: 0.15,
      zIndex: 1,
      pointerEvents: "none",
    },
    hidden: {
      transform: "translateX(0%) scale(0.5)",
      opacity: 0,
      zIndex: -1,
      pointerEvents: "none",
    },
  };

  const style = positionStyles[position] ?? positionStyles.hidden;
  const isCenter = position === "center";

  return (
    <div
      onClick={() => {
        if (position !== "center" && position !== "hidden") {
          onClick(index);
        }
      }}
      style={{
        position: "absolute",
        width: "min(460px, 85vw)",
        maxWidth: "460px",
        top: "50%",
        left: "50%",
        marginLeft: "max(-230px, -42.5vw)",
        marginTop: isCenter ? "-240px" : "-210px",
        transition: "transform 0.6s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.6s ease",
        willChange: "transform, opacity",
        cursor: isCenter ? "default" : "pointer",
        ...style,
      }}
    >
      <div
        style={{
          background: "linear-gradient(135deg, #2a2a2a 0%, #111111 100%)",
          border: isCenter 
            ? "2px solid #FFD700" 
            : "1px solid rgba(255, 215, 0, 0.3)",
          borderRadius: "16px",
          boxShadow: isCenter
            ? "0 0 25px rgba(255, 215, 0, 0.3), inset 0 0 15px rgba(255, 215, 0, 0.1), 0 20px 40px rgba(0,0,0,0.8)"
            : "0 10px 30px rgba(0,0,0,0.6)",
          overflow: "hidden",
          padding: isCenter ? "28px" : "24px",
          height: isCenter ? "480px" : "420px",
          display: "flex",
          flexDirection: "column",
          position: "relative",
        }}
      >
        {/* Glossy Reflection Overlay */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "linear-gradient(110deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.03) 30%, transparent 32%, transparent 100%)",
            pointerEvents: "none",
            zIndex: 0,
          }}
        />

        {/* Content Wrapper */}
        <div className="relative z-10 flex flex-col h-full">
          {/* Top Header */}
          <div className="flex items-center justify-between mb-5">
            <span
              className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-semibold tracking-wide"
              style={{
                background: "rgba(0, 210, 255, 0.1)",
                border: "1px solid rgba(0, 210, 255, 0.3)",
                color: "#4EE2FF",
              }}
            >
              Question
            </span>
            <span
              className="text-[11px] font-mono tracking-widest"
              style={{ color: "rgba(255,255,255,0.4)" }}
            >
              {String(index + 1).padStart(2, "0")} / {String(total).padStart(2, "0")}
            </span>
          </div>

          {/* Question */}
          <div className="mb-5">
            <h3
              className="font-display font-medium leading-snug"
              style={{
                fontSize: isCenter ? "22px" : "18px",
                color: "#FFFFFF",
                textShadow: "0 2px 4px rgba(0,0,0,0.5)",
              }}
            >
              {item.question}
            </h3>
          </div>
          
          {/* Divider */}
          <div
            style={{
              height: "1px",
              background: "rgba(255,255,255,0.06)",
              marginBottom: "16px",
            }}
          />

          {/* Answer */}
          <div 
            className="mb-5 flex-1 overflow-y-auto pr-2"
            style={{
              scrollbarWidth: "thin",
              scrollbarColor: "rgba(255,215,0,0.3) transparent"
            }}
          >
            <div className="mb-3">
              <span
                className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-semibold tracking-wide"
                style={{
                  background: "rgba(16, 185, 129, 0.1)",
                  border: "1px solid rgba(16, 185, 129, 0.3)",
                  color: "#34D399",
                }}
              >
                Answer
              </span>
            </div>
            <p
              className="leading-relaxed"
              style={{
                fontSize: "13px",
                color: "rgba(255,255,255,0.7)",
              }}
            >
              {item.answer}
            </p>
          </div>

          {/* Supporting Documents */}
          {item.documents.length > 0 && (
            <div className="mt-auto pt-2">
              <div className="mb-2">
                <span
                  className="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-semibold tracking-wide"
                  style={{
                    background: "rgba(168, 85, 247, 0.1)",
                    border: "1px solid rgba(168, 85, 247, 0.3)",
                    color: "#C084FC",
                  }}
                >
                  Supporting Document
                </span>
              </div>
              <div className="flex flex-col gap-2">
                {item.documents.map((doc, i) => (
                  <a
                    key={i}
                    href={doc.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="flex items-center justify-between gap-3 group"
                    style={{
                      background: "rgba(255,255,255,0.03)",
                      border: "1px solid rgba(255,255,255,0.06)",
                      borderRadius: "8px",
                      padding: "12px",
                      transition: "all 0.2s ease",
                      textDecoration: "none",
                    }}
                    onMouseEnter={(e) => {
                      (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(168, 85, 247, 0.4)";
                      (e.currentTarget as HTMLAnchorElement).style.background = "rgba(168, 85, 247, 0.08)";
                    }}
                    onMouseLeave={(e) => {
                      (e.currentTarget as HTMLAnchorElement).style.borderColor = "rgba(255,255,255,0.06)";
                      (e.currentTarget as HTMLAnchorElement).style.background = "rgba(255,255,255,0.03)";
                    }}
                  >
                    <div className="min-w-0 flex-1">
                      <p
                        className="font-medium truncate"
                        style={{
                          fontSize: "11px",
                          color: "rgba(255,255,255,0.85)",
                        }}
                      >
                        {doc.title}
                      </p>
                      {isCenter && (
                        <p
                          className="truncate mt-1"
                          style={{ fontSize: "9px", color: "rgba(255,255,255,0.4)" }}
                        >
                          {doc.url}
                        </p>
                      )}
                    </div>
                    <i
                      className="bi bi-box-arrow-up-right flex-shrink-0"
                      style={{ color: "rgba(255,255,255,0.5)", fontSize: "12px" }}
                    />
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
});

// ─── Main Section ──────────────────────────────────────────────────────────
export default function QADomeSection() {
  const [activeIndex, setActiveIndex] = useState(0);
  const isAnimatingRef = useRef(false);
  const touchStartX = useRef<number | null>(null);

  // All questions combined without categories
  const filtered = QA_DATA;
  const total = filtered.length;

  const prev = useCallback(() => {
    if (isAnimatingRef.current) return;
    isAnimatingRef.current = true;
    setActiveIndex((i) => (i - 1 + total) % total);
    setTimeout(() => { isAnimatingRef.current = false; }, 700);
  }, [total]);

  const next = useCallback(() => {
    if (isAnimatingRef.current) return;
    isAnimatingRef.current = true;
    setActiveIndex((i) => (i + 1) % total);
    setTimeout(() => { isAnimatingRef.current = false; }, 700);
  }, [total]);

  const goTo = useCallback(
    (i: number) => {
      setActiveIndex((current) => {
        if (isAnimatingRef.current || i === current) return current;
        isAnimatingRef.current = true;
        setTimeout(() => { isAnimatingRef.current = false; }, 700);
        return i;
      });
    },
    []
  );

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowLeft") prev();
      if (e.key === "ArrowRight") next();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [prev, next]);

  // Touch/swipe
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  };
  const handleTouchEnd = (e: React.TouchEvent) => {
    if (touchStartX.current === null) return;
    const diff = touchStartX.current - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 50) diff > 0 ? next() : prev();
    touchStartX.current = null;
  };

  // Build position map
  const getPosition = (idx: number): string => {
    const offset = (idx - activeIndex + total) % total;
    if (offset === 0) return "center";
    if (offset === 1) return "right";
    if (offset === total - 1) return "left";
    if (offset === 2) return "far-right";
    if (offset === total - 2) return "far-left";
    return "hidden";
  };

  return (
    <Section
      id="qa"
      style={{
        background: "#02060A", // Very dark space blue/black
        minHeight: "100svh",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {/* ── Background Glow ── */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: "40%",
          transform: "translate(-50%, -50%)",
          width: "100vw",
          height: "80vw",
          background: "radial-gradient(circle at center, rgba(0, 180, 255, 0.05) 0%, transparent 60%)",
          pointerEvents: "none",
        }}
      />

      <div
        className="relative flex-1 flex flex-col justify-start items-center"
        style={{ paddingBottom: "12vh", paddingTop: "12vh" }}
        onTouchStart={handleTouchStart}
        onTouchEnd={handleTouchEnd}
      >
        {/* ── Dome Arc Overlay ── */}
        <div
          style={{
            position: "absolute",
            left: "50%",
            top: "5vh",
            transform: "translateX(-50%)",
            width: "140vw",
            height: "140vw",
            maxWidth: "1800px",
            maxHeight: "1800px",
            borderRadius: "50%",
            borderTop: "2px solid rgba(0, 210, 255, 0.25)",
            boxShadow: "inset 0 30px 60px -20px rgba(0, 210, 255, 0.15)",
            background: "radial-gradient(ellipse at top, rgba(0, 150, 255, 0.03) 0%, transparent 50%)",
            pointerEvents: "none",
            zIndex: 0,
          }}
        />

        {/* ── Header Inside Dome (Now relative so it doesn't overlap) ── */}
        <div className="relative z-20 flex flex-col items-center text-center w-full mt-4 mb-8">
          <h4 className="text-[11px] font-bold tracking-[0.4em] text-[#00D2FF] mb-3 uppercase">
            Inetra
          </h4>
          <h2 className="font-display font-bold text-white mb-2 leading-none" style={{ fontSize: "clamp(48px, 6vw, 72px)" }}>
            Q&amp;A
          </h2>
          <h3 className="text-xl md:text-2xl text-gray-200 mb-4 font-medium tracking-wide">
            with Supporting Evidence
          </h3>
          <p className="text-[13px] text-gray-400 max-w-lg px-4 mt-2">
            Explore the key questions, our answers, and the official references that support our solution.
          </p>
        </div>

        {/* ── Perspective Container (Cards) ── */}
        <div
          style={{
            perspective: "1200px",
            perspectiveOrigin: "50% 50%",
            position: "relative",
            height: "500px", // slightly taller container to give cards room
            width: "100%",
            zIndex: 10,
            marginTop: "2rem",
          }}
        >
          {filtered.map((item, idx) => {
            const pos = getPosition(idx);
            return (
              <QACard
                key={item.id}
                item={item}
                position={pos}
                index={idx}
                total={total}
                onClick={goTo}
              />
            );
          })}
        </div>

        {/* ── Base Platform Details ── */}
        <div
          style={{
            position: "absolute",
            bottom: "-15vh",
            left: "50%",
            transform: "translateX(-50%)",
            width: "150vw",
            height: "35vh",
            background: "radial-gradient(ellipse at center top, rgba(0, 150, 255, 0.08) 0%, transparent 70%)",
            borderTop: "1px solid rgba(0, 180, 255, 0.2)",
            borderRadius: "50% 50% 0 0",
            pointerEvents: "none",
            zIndex: 1,
            boxShadow: "0 -20px 40px rgba(0, 150, 255, 0.05)",
          }}
        >
          <div style={{
            position: "absolute",
            top: "20px", left: "10%", right: "10%", height: "1px",
            background: "radial-gradient(ellipse at center, rgba(0, 210, 255, 0.15) 0%, transparent 70%)"
          }} />
          <div style={{
            position: "absolute",
            top: "45px", left: "5%", right: "5%", height: "1px",
            background: "radial-gradient(ellipse at center, rgba(0, 210, 255, 0.1) 0%, transparent 70%)"
          }} />
        </div>

        {/* ── Left / Right Navigation Buttons ── */}
        <div className="absolute top-[70%] left-0 right-0 transform -translate-y-1/2 flex justify-between px-[2vw] md:px-[10vw] lg:px-[18vw] z-30 pointer-events-none">
          <button
            onClick={prev}
            className="w-12 h-12 rounded-full flex items-center justify-center bg-black/50 border border-white/10 text-white hover:border-[#FFD700]/60 hover:bg-[#FFD700]/10 hover:text-[#FFD700] transition-all pointer-events-auto backdrop-blur-md"
            style={{ boxShadow: "0 0 20px rgba(0,0,0,0.5)" }}
          >
            <i className="bi bi-chevron-left text-lg" />
          </button>
          <button
            onClick={next}
            className="w-12 h-12 rounded-full flex items-center justify-center bg-black/50 border border-white/10 text-white hover:border-[#FFD700]/60 hover:bg-[#FFD700]/10 hover:text-[#FFD700] transition-all pointer-events-auto backdrop-blur-md"
            style={{ boxShadow: "0 0 20px rgba(0,0,0,0.5)" }}
          >
            <i className="bi bi-chevron-right text-lg" />
          </button>
        </div>

        {/* ── Pagination Dots ── */}
        <div className="absolute bottom-[6vh] left-0 right-0 flex justify-center gap-3 z-30">
          {filtered.map((_, i) => (
            <button
              key={i}
              onClick={() => goTo(i)}
              className="rounded-full transition-all duration-300"
              style={{
                width: i === activeIndex ? "8px" : "8px",
                height: "8px",
                background: i === activeIndex ? "#FFD700" : "rgba(255,255,255,0.15)",
                boxShadow: i === activeIndex ? "0 0 12px #FFD700" : "none",
              }}
            />
          ))}
        </div>
      </div>
    </Section>
  );
}
