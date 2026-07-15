"use client";

import React from "react";
import Link from "next/link";
import { ArrowRight, Activity, Cpu, TrendingUp, Shield } from "lucide-react";

export default function LandingTutorialPage() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-background text-textPrimary flex flex-col font-sans selection:bg-accent/30 selection:text-white">
      <div className="flex-1 w-full max-w-5xl mx-auto px-6 py-24 md:py-32 flex flex-col items-center">
        
        {/* Hero Section */}
        <section className="text-center space-y-8 mb-32 animate-fade-up max-w-4xl">
          <div className="inline-flex items-center space-x-2 bg-surface/50 rounded-full px-4 py-1.5 text-xs font-medium text-textSecondary mb-4">
            <span className="flex h-2 w-2 rounded-full bg-accent animate-pulse-glow"></span>
            <span>v1.0 Institutional AI Engine Active</span>
          </div>
          
          <h1 className="text-6xl md:text-8xl font-bold tracking-tight text-white leading-tight">
            Autonomous<br />Hedge Fund.
          </h1>
          <p className="text-xl md:text-2xl text-textSecondary mx-auto leading-relaxed font-light max-w-2xl">
            An institutional-grade multi-agent AI research & execution terminal. Designed to do the heavy lifting of financial analysis for you.
          </p>
          
          <div className="pt-10 flex justify-center items-center">
            <Link 
              href="/terminal" 
              className="inline-flex items-center justify-center px-8 py-4 text-[17px] font-semibold text-white bg-accent hover:bg-accentHover rounded-full transition-all duration-300"
            >
              Enter Chart Terminal <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </section>

        {/* Step-by-Step Guide */}
        <section className="w-full mb-32">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 text-white">How it works.</h2>
            <p className="text-textSecondary text-xl font-light">Four simple steps to professional quantitative analysis.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="glass-panel p-10 glass-panel-hover flex flex-col gap-6 animate-fade-up" style={{ animationDelay: '0.1s' }}>
              <div className="w-12 h-12 rounded-full bg-accent/20 flex items-center justify-center text-accent">
                <Activity className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold text-white mb-3">Launch Scan</h3>
                <p className="text-textSecondary text-[17px] leading-relaxed">
                  Enter any stock symbol in the top toolbar of the terminal and click Launch Scan to dispatch the multi-agent AI system.
                </p>
              </div>
            </div>

            <div className="glass-panel p-10 glass-panel-hover flex flex-col gap-6 animate-fade-up" style={{ animationDelay: '0.2s' }}>
              <div className="w-12 h-12 rounded-full bg-success/20 flex items-center justify-center text-success">
                <Cpu className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold text-white mb-3">AI Agents Work</h3>
                <p className="text-textSecondary text-[17px] leading-relaxed">
                  The agents analyze historical regimes, news catalysts, technical indicators, macro economics, and options flow in real-time.
                </p>
              </div>
            </div>

            <div className="glass-panel p-10 glass-panel-hover flex flex-col gap-6 animate-fade-up" style={{ animationDelay: '0.3s' }}>
              <div className="w-12 h-12 rounded-full bg-warning/20 flex items-center justify-center text-warning">
                <TrendingUp className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold text-white mb-3">Recommendation</h3>
                <p className="text-textSecondary text-[17px] leading-relaxed">
                  Review the Chief Investment Officer's final Dossier. The AI synthesizes the data to give you a definitive BUY, HOLD, or SELL rating.
                </p>
              </div>
            </div>

            <div className="glass-panel p-10 glass-panel-hover flex flex-col gap-6 animate-fade-up" style={{ animationDelay: '0.4s' }}>
              <div className="w-12 h-12 rounded-full bg-danger/20 flex items-center justify-center text-danger">
                <Shield className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold text-white mb-3">Execution Plan</h3>
                <p className="text-textSecondary text-[17px] leading-relaxed">
                  If you decide to trade, follow the calculated Target Buy Zone, precise Stop-Loss, and Take-Profit limits to strictly manage risk.
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
