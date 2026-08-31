import type { Metadata } from "next";
import "./globals.css";
import SmoothScrollProvider from "@/components/providers/SmoothScrollProvider";
import Navigation from "@/components/layout/Navigation";

export const metadata: Metadata = {
  title: "UrbanPulse Fusion — AI Urban Intelligence Platform",
  description:
    "UrbanPulse Fusion unifies public transport cameras, roadside AI cameras, and existing city CCTV into a cooperative, self-verifying urban intelligence network. BEL SIH26124.",
  keywords: [
    "urban intelligence",
    "AI traffic monitoring",
    "smart city",
    "BEL",
    "SIH",
    "pothole detection",
    "fleet intelligence",
    "CCTV analytics",
    "urban memory",
    "edge AI",
  ],
  openGraph: {
    title: "UrbanPulse Fusion",
    description: "One Urban Intelligence Layer Across Every Camera.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        <Navigation />
        <SmoothScrollProvider>{children}</SmoothScrollProvider>
      </body>
    </html>
  );
}
