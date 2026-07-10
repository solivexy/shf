"use client";

import React from "react";
import { Layers } from "lucide-react";

interface Props {
  optionsFlow?: any;
}

export default function OptionsFlowCard({ optionsFlow }: Props) {
  if (!optionsFlow) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center text-[#787b86] text-xs font-mono">
        Awaiting Institutional Options Flow Scan...
      </div>
    );
  }

  const pcr = optionsFlow.put_call_ratio !== undefined ? Number(optionsFlow.put_call_ratio).toFixed(2) : "0.74";
  const maxPain = optionsFlow.max_pain || "$152.00";
  const sentiment = optionsFlow.sentiment || (Number(pcr) < 0.85 ? "Bullish Institutional Call Flow" : "Bearish Institutional Put Protection");

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs select-none flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-[#2a2e39] bg-[#131722]">
          <div className="flex items-center space-x-2">
            <Layers className="w-3.5 h-3.5 text-[#2962ff]" />
            <span className="font-bold text-[#d1d4dc] uppercase tracking-tight text-[11px]">OPTIONS FLOW</span>
          </div>
          <span className={`text-[10px] font-bold px-1.5 py-0.5 border ${
            Number(pcr) < 0.85
              ? "text-[#089981] border-[#089981]/30 bg-[#089981]/10"
              : "text-[#f23645] border-[#f23645]/30 bg-[#f23645]/10"
          }`}>
            PCR: {pcr}
          </span>
        </div>

        {/* Summary */}
        <div className="p-3 text-[11px] text-[#787b86] leading-relaxed border-b border-[#2a2e39] bg-[#131722]/30">
          {optionsFlow.summary || "Options chain assessment across gamma exposure and block trades."}
        </div>

        {/* Data Grid */}
        <div className="grid grid-cols-2 divide-x divide-[#2a2e39] text-[11px]">
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Put/Call Ratio</span>
            <span className={`font-bold ${Number(pcr) < 0.85 ? "text-[#089981]" : "text-[#f23645]"}`}>
              {pcr}
            </span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Max Pain Strike</span>
            <span className="font-bold text-[#d1d4dc]">{maxPain}</span>
          </div>
        </div>

        <div className="p-2 border-t border-[#2a2e39] text-[10px]">
          <span className="text-[#787b86] uppercase block text-[9px]">Flow Sentiment:</span>
          <span className="font-bold text-[#2962ff] truncate block mt-0.5">{sentiment}</span>
        </div>
      </div>
    </div>
  );
}
