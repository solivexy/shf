"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Terminal, PieChart, TrendingUp, FileText, Circle } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Tutorial & Onboarding", href: "/", icon: PieChart },
    { name: "Terminal", href: "/terminal", icon: Terminal },
    { name: "Research", href: "/reports", icon: FileText },
    { name: "Architecture", href: "/architecture", icon: TrendingUp },
  ];

  return (
    <header className="sticky top-0 z-50 bg-background/40 backdrop-blur-3xl backdrop-saturate-[1.8] border-b border-white/5 px-6 font-sans select-none">
      <div className="flex items-center justify-between h-16 text-[15px] max-w-7xl mx-auto w-full">
        {/* Left Brand */}
        <div className="flex items-center space-x-10">
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-accent to-accentHover flex items-center justify-center shadow-lg shadow-accent/20">
              <span className="text-white font-bold text-[10px] tracking-tighter">SHF</span>
            </div>
            <span className="text-textPrimary font-semibold tracking-tight text-lg">
              Terminal
            </span>
          </Link>

          {/* Navigation Links (Apple Style text links) */}
          <nav className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => {
              const isActive = pathname === item.href || (item.href === "/terminal" && pathname.startsWith("/terminal"));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`transition-colors duration-200 ${
                    isActive
                      ? "text-white font-medium"
                      : "text-textSecondary hover:text-textPrimary"
                  }`}
                >
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Right Status / Connection Indicators */}
        <div className="flex items-center space-x-6">
          <div className="hidden lg:flex items-center space-x-2 text-[13px] text-textSecondary">
            <Circle className="w-2 h-2 fill-success text-success animate-pulse" />
            <span>System Online</span>
          </div>
          <div className="text-textSecondary text-[11px] uppercase tracking-widest font-medium">
            Simulation
          </div>
        </div>
      </div>
    </header>
  );
}
