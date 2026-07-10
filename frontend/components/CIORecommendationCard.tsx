"use client";

import React from "react";
import { ArrowUpRight, ArrowDownRight, CheckCircle2, AlertTriangle } from "lucide-react";

interface Props {
  portfolioManager?: any;
  executionPlan?: any;
}

export default function CIORecommendationCard({ portfolioManager, executionPlan }: Props) {
  if (!portfolioManager) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center font-mono text-xs text-[#787b86]">
        Awaiting Portfolio Manager quantitative synthesis...
      </div>
    );
  }

  const decision = portfolioManager.decision || "Hold";
  const isBuy = decision === "Buy" || decision === "Strong Buy";
  const isSell = decision === "Sell" || decision === "Strong Sell";

  const badgeColor = isBuy
    ? "bg-[#089981]/20 text-[#089981] border-[#089981]"
    : isSell
    ? "bg-[#f23645]/20 text-[#f23645] border-[#f23645]"
    : "bg-[#f2a900]/20 text-[#f2a900] border-[#f2a900]";

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs select-none">
      {/* Top Banner Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 border-b border-[#2a2e39] divide-x divide-[#2a2e39] bg-[#131722]/60">
        <div className="p-3 flex flex-col justify-center">
          <span className="text-[#787b86] text-[10px] uppercase">CIO Recommendation</span>
          <span className={`font-bold text-sm uppercase px-2 py-0.5 mt-1 border inline-block text-center ${badgeColor}`}>
            {decision}
          </span>
        </div>

        <div className="p-3 flex flex-col justify-center">
          <span className="text-[#787b86] text-[10px] uppercase">Model Confidence</span>
          <span className="font-bold text-sm text-[#d1d4dc] mt-1">{portfolioManager.confidence}%</span>
        </div>

        <div className="p-3 flex flex-col justify-center">
          <span className="text-[#787b86] text-[10px] uppercase">Target Position Sizing</span>
          <span className="font-bold text-sm text-[#2962ff] mt-1">{portfolioManager.position_size || "5.0%"}</span>
        </div>

        <div className="p-3 flex flex-col justify-center">
          <span className="text-[#787b86] text-[10px] uppercase">Risk Classification</span>
          <span className="font-bold text-sm text-[#f2a900] mt-1">{portfolioManager.risk || "Medium"}</span>
        </div>

        <div className="p-3 flex flex-col justify-center col-span-2 md:col-span-1">
          <span className="text-[#787b86] text-[10px] uppercase">Investment Horizon</span>
          <span className="font-bold text-sm text-[#d1d4dc] mt-1">{portfolioManager.investment_horizon || "3 Months"}</span>
        </div>
      </div>

      {/* CIO Synthesis Summary */}
      <div className="p-3.5 border-b border-[#2a2e39]">
        <div className="text-[10px] text-[#787b86] uppercase font-semibold mb-1">Executive Quant Synthesis</div>
        <p className="text-xs text-[#d1d4dc] leading-relaxed">
          {portfolioManager.summary || "Quantitative multi-agent evaluation completed."}
        </p>
      </div>

      {/* Bullish & Bearish Factors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-[#2a2e39]">
        <div className="p-3.5">
          <div className="flex items-center space-x-1.5 text-[#089981] font-semibold text-[11px] mb-2 uppercase">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>Primary Bullish Drivers</span>
          </div>
          <ul className="space-y-1.5 text-[#d1d4dc]">
            {(portfolioManager.bullish_reasons || []).map((reason: string, idx: number) => (
              <li key={idx} className="flex items-start space-x-2 text-[11px] leading-tight">
                <span className="text-[#089981] font-bold">+</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="p-3.5">
          <div className="flex items-center space-x-1.5 text-[#f23645] font-semibold text-[11px] mb-2 uppercase">
            <ArrowDownRight className="w-3.5 h-3.5" />
            <span>Key Bearish Headwinds / Risks</span>
          </div>
          <ul className="space-y-1.5 text-[#d1d4dc]">
            {(portfolioManager.bearish_reasons || []).map((reason: string, idx: number) => (
              <li key={idx} className="flex items-start space-x-2 text-[11px] leading-tight">
                <span className="text-[#f23645] font-bold">-</span>
                <span>{reason}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Institutional Execution Plan Bracket */}
      {executionPlan && (
        <div className="border-t border-[#2a2e39] bg-[#131722] p-3 flex flex-wrap items-center justify-between gap-3 text-[11px]">
          <div className="flex items-center space-x-6">
            <div>
              <span className="text-[#787b86] uppercase mr-1">Buy Zone:</span>
              <strong className="text-[#089981]">{executionPlan.ideal_buy_zone}</strong>
            </div>
            <div>
              <span className="text-[#787b86] uppercase mr-1">Stop Loss:</span>
              <strong className="text-[#f23645]">{executionPlan.stop_loss}</strong>
            </div>
            <div>
              <span className="text-[#787b86] uppercase mr-1">Take Profit:</span>
              <strong className="text-[#089981]">{executionPlan.take_profit}</strong>
            </div>
          </div>
          <div className="text-[#f2a900] bg-[#f2a900]/10 border border-[#f2a900]/30 px-2 py-0.5 font-semibold text-[10px] uppercase">
            {executionPlan.execution_warning}
          </div>
        </div>
      )}
    </div>
  );
}
