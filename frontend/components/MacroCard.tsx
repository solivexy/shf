"use client";

import React from "react";
import { Globe } from "lucide-react";

interface Props {
  macroEconomy?: any;
}

export default function MacroCard({ macroEconomy }: Props) {
  if (!macroEconomy) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center text-[#787b86] text-xs font-mono">
        Awaiting Macroeconomic Audit...
      </div>
    );
  }

  const ind = macroEconomy.indicators || {};

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs select-none flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-[#2a2e39] bg-[#131722]">
          <div className="flex items-center space-x-2">
            <Globe className="w-3.5 h-3.5 text-[#2962ff]" />
            <span className="font-bold text-[#d1d4dc] uppercase tracking-tight text-[11px]">MACRO AUDIT</span>
          </div>
          <span className={`text-[10px] font-bold px-1.5 py-0.5 border ${
            macroEconomy.macro_score >= 0
              ? "text-[#089981] border-[#089981]/30 bg-[#089981]/10"
              : "text-[#f23645] border-[#f23645]/30 bg-[#f23645]/10"
          }`}>
            SCORE: {macroEconomy.macro_score > 0 ? "+" : ""}{macroEconomy.macro_score}
          </span>
        </div>

        {/* Summary */}
        <div className="p-3 text-[11px] text-[#787b86] leading-relaxed border-b border-[#2a2e39] bg-[#131722]/30">
          {macroEconomy.summary || "Macroeconomic evaluation completed across rates and CPI."}
        </div>

        {/* Data Grid */}
        <div className="grid grid-cols-2 divide-x divide-y divide-[#2a2e39] text-[11px]">
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Fed Funds Rate</span>
            <span className="font-bold text-[#d1d4dc]">{ind.fed_funds_rate !== undefined ? `${ind.fed_funds_rate}%` : "5.25%"}</span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">US 10Y Yield</span>
            <span className="font-bold text-[#f2a900]">{ind.us_10y_yield !== undefined ? `${ind.us_10y_yield}%` : "4.30%"}</span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Core CPI YoY</span>
            <span className="font-bold text-[#f23645]">{ind.cpi_yoy !== undefined ? `${ind.cpi_yoy}%` : "3.1%"}</span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">DXY Index</span>
            <span className="font-bold text-[#089981]">{ind.dxy_index !== undefined ? ind.dxy_index : "103.8"}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
