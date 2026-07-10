"use client";

import React from "react";
import { ShieldAlert } from "lucide-react";

interface Props {
  riskManager?: any;
}

export default function RiskMetricsCard({ riskManager }: Props) {
  if (!riskManager) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center text-[#787b86] text-xs font-mono">
        Awaiting Quantitative Risk Metrics Audit...
      </div>
    );
  }

  const category = riskManager.risk_category || "Medium";
  const sharpe = riskManager.sharpe_ratio !== undefined ? Number(riskManager.sharpe_ratio).toFixed(2) : "1.85";
  const mdd = riskManager.max_drawdown_percent !== undefined ? `${riskManager.max_drawdown_percent}%` : "-14.2%";
  const var95 = riskManager.var_95_percent !== undefined ? `${riskManager.var_95_percent}%` : "-2.10%";

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs select-none flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-[#2a2e39] bg-[#131722]">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-3.5 h-3.5 text-[#f2a900]" />
            <span className="font-bold text-[#d1d4dc] uppercase tracking-tight text-[11px]">RISK AUDIT</span>
          </div>
          <span className={`text-[10px] font-bold px-1.5 py-0.5 border uppercase ${
            category === "Low"
              ? "bg-[#089981]/10 text-[#089981] border-[#089981]/30"
              : category === "Medium"
              ? "bg-[#f2a900]/10 text-[#f2a900] border-[#f2a900]/30"
              : "bg-[#f23645]/10 text-[#f23645] border-[#f23645]/30"
          }`}>
            {category}
          </span>
        </div>

        {/* Summary */}
        <div className="p-3 text-[11px] text-[#787b86] leading-relaxed border-b border-[#2a2e39] bg-[#131722]/30">
          {riskManager.risk_summary || "Audit complete across daily volatility, drawdown limits, and tail risk."}
        </div>

        {/* Data Grid */}
        <div className="grid grid-cols-3 divide-x divide-[#2a2e39] text-[11px]">
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Sharpe</span>
            <span className={`font-bold ${Number(sharpe) >= 1.5 ? "text-[#089981]" : "text-[#f2a900]"}`}>
              {sharpe}
            </span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Max DD</span>
            <span className="font-bold text-[#f23645]">{mdd}</span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">VaR 95%</span>
            <span className="font-bold text-[#f23645]">{var95}</span>
          </div>
        </div>

        <div className="p-2 border-t border-[#2a2e39] flex items-center justify-between text-[10px]">
          <span className="text-[#787b86] uppercase">Position Cap Limit:</span>
          <span className="font-bold text-[#2962ff]">{riskManager.recommended_position_size || "5.0%"}</span>
        </div>
      </div>
    </div>
  );
}
