"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Terminal, PieChart, TrendingUp, FileText, Circle } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Chart Terminal", href: "/", icon: Terminal },
    { name: "Research Dossiers", href: "/reports", icon: FileText },
    { name: "How to Use AI", href: "/tutorial", icon: PieChart },
    { name: "Under the Hood", href: "/architecture", icon: TrendingUp },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#131722] border-b border-[#2a2e39] px-4 font-mono select-none">
      <div className="flex items-center justify-between h-11 text-xs">
        {/* Left Brand / Terminal Header */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <span className="bg-[#2962ff] text-white font-bold px-1.5 py-0.5 text-[11px] tracking-wider uppercase">
              SHF
            </span>
            <span className="text-[#d1d4dc] font-semibold text-xs tracking-tight">
              QUANTITATIVE TERMINAL
            </span>
            <span className="text-[#787b86] text-[11px] hidden sm:inline">v1.0.0</span>
          </div>

          {/* Navigation Tabs (TradingView style sharp tabs) */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-3 border-b-2 text-[11px] font-medium tracking-wide transition-colors ${
                    isActive
                      ? "text-[#2962ff] border-[#2962ff] bg-[#1e222d]"
                      : "text-[#787b86] border-transparent hover:text-[#d1d4dc] hover:bg-[#1e222d]/50"
                  }`}
                >
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Right Status / Connection Indicators */}
        <div className="flex items-center space-x-4">
          <div className="hidden lg:flex items-center space-x-1.5 text-[11px] text-[#089981]">
            <Circle className="w-2 h-2 fill-[#089981] text-[#089981] animate-pulse" />
            <span>INSTITUTIONAL FEED LIVE</span>
          </div>
          <div className="bg-[#1e222d] border border-[#2a2e39] text-[#787b86] px-2 py-0.5 text-[10px] tracking-widest uppercase">
            SIMULATION ONLY
          </div>
        </div>
      </div>
    </header>
  );
}
