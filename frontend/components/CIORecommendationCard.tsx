"use client";

import React from "react";
import { ArrowUpRight, ArrowDownRight, CheckCircle2, AlertTriangle } from "lucide-react";

interface Props {
  portfolioManager?: any;
  executionPlan?: any;
  ticker?: string;
  marketData?: any;
}

export default function CIORecommendationCard({ portfolioManager, executionPlan, ticker = "AAPL", marketData }: Props) {
  if (!portfolioManager) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center font-mono text-xs text-[#787b86]">
        Awaiting Portfolio Manager quantitative synthesis...
      </div>
    );
  }

  const decisionOwned = portfolioManager.decision_owned || decision;
  const decisionNotOwned = portfolioManager.decision_not_owned || decision;

  const isBuyOwned = decisionOwned === "Buy" || decisionOwned === "Strong Buy";
  const isSellOwned = decisionOwned === "Sell" || decisionOwned === "Strong Sell" || decisionOwned === "Reduce";
  const ownedColor = isBuyOwned ? "text-[#089981]" : isSellOwned ? "text-[#f23645]" : "text-[#f2a900]";

  const isBuyNotOwned = decisionNotOwned === "Buy" || decisionNotOwned === "Strong Buy";
  const isSellNotOwned = decisionNotOwned === "Sell" || decisionNotOwned === "Strong Sell" || decisionNotOwned.includes("Wait") || decisionNotOwned.includes("Do Not Buy");
  const notOwnedColor = isBuyNotOwned ? "text-[#089981]" : isSellNotOwned ? "text-[#f23645]" : "text-[#f2a900]";

  const curr = ticker.toUpperCase().endsWith(".JK") ? "IDR " : "$";
  const priceFormatted = marketData?.current_price ? marketData.current_price.toFixed(2) : "0.00";
  const changePercent = marketData?.daily_change_percent ? marketData.daily_change_percent.toFixed(2) : "0.00";
  const changeColor = Number(changePercent) >= 0 ? "text-[#089981]" : "text-[#f23645]";
  const changeSign = Number(changePercent) >= 0 ? "+" : "";

  const todayDate = new Date().toISOString().split('T')[0];
  const companyName = marketData?.company_name || ticker;

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-sans text-[#d1d4dc] select-none p-6 rounded-md">
      {/* Dossier Header */}
      <div className="mb-4">
        <h1 className="text-3xl font-extrabold tracking-tight text-white">
          {ticker} • {companyName}
        </h1>
        <div className="text-[#787b86] text-sm mt-2 border-b-2 border-[#2962ff] pb-3 mb-4 flex flex-wrap items-center gap-2">
          <span className="font-semibold text-[#d1d4dc]">AI Investment Recommendation</span>
          <span className="hidden sm:inline">•</span>
          <span>Spot Price: <strong className="text-white">{curr}{priceFormatted}</strong> (<span className={changeColor}>{changeSign}{changePercent}%</span>)</span>
          <span className="hidden sm:inline">•</span>
          <span>Evaluation Date: <strong className="text-white">{todayDate}</strong></span>
        </div>
      </div>

      {/* Actions Table */}
      <div className="border border-[#2a2e39] rounded-sm overflow-hidden mb-5 bg-[#131722]">
        <div className="grid grid-cols-4 border-b border-[#2a2e39] bg-[#1e222d] text-[11px] font-bold text-[#787b86] uppercase tracking-wider">
          <div className="p-3">Action (If Owned)</div>
          <div className="p-3 border-l border-[#2a2e39]">Action (Not Owned)</div>
          <div className="p-3 border-l border-[#2a2e39]">AI Certainty</div>
          <div className="p-3 border-l border-[#2a2e39]">Portfolio Size (Kelly)</div>
        </div>
        <div className="grid grid-cols-4 text-sm font-bold bg-[#131722]">
          <div className={`p-3 uppercase ${ownedColor}`}>{decisionOwned}</div>
          <div className={`p-3 uppercase border-l border-[#2a2e39] ${notOwnedColor}`}>{decisionNotOwned}</div>
          <div className="p-3 border-l border-[#2a2e39] text-[#d1d4dc]">{portfolioManager.confidence}%</div>
          <div className="p-3 border-l border-[#2a2e39] text-[#d1d4dc]">{portfolioManager.position_size || "5.0%"}</div>
        </div>
      </div>

      {/* CIO Synthesis Summary */}
      <div className="bg-[#131722] border border-[#2a2e39] rounded-sm mb-4">
        <div className="p-4 border-b border-[#2a2e39]">
          <div className="text-xs text-[#2962ff] font-bold uppercase mb-2">Executive Summary</div>
          <p className="text-sm text-[#d1d4dc] leading-relaxed">
            {portfolioManager.summary || "Quantitative multi-agent evaluation completed."}
          </p>
        </div>

        {/* Bullish & Bearish Factors Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-[#2a2e39]">
          <div className="p-4">
            <div className="flex items-center space-x-2 text-[#089981] font-bold text-xs mb-3 uppercase">
              <ArrowUpRight className="w-3.5 h-3.5" />
              <span>Primary Bullish Drivers</span>
            </div>
            <ul className="space-y-1.5 text-[#d1d4dc]">
              {(portfolioManager.bullish_reasons || []).map((reason: string, idx: number) => (
                <li key={idx} className="flex items-start space-x-2 text-xs leading-relaxed">
                  <span className="text-[#089981] font-bold mt-0.5">+</span>
                  <span className="text-[#d1d4dc]">{reason}</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="p-4">
            <div className="flex items-center space-x-2 text-[#f23645] font-bold text-xs mb-3 uppercase">
              <ArrowDownRight className="w-4 h-4" />
              <span>Key Bearish Headwinds / Risks</span>
            </div>
            <ul className="space-y-1.5 text-[#d1d4dc]">
              {(portfolioManager.bearish_reasons || []).map((reason: string, idx: number) => (
                <li key={idx} className="flex items-start space-x-2 text-xs leading-relaxed">
                  <span className="text-[#f23645] font-bold mt-0.5">-</span>
                  <span className="text-[#d1d4dc]">{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Institutional Execution Plan Bracket */}
      {executionPlan && (
        <div className="border border-[#2a2e39] bg-[#1e222d] rounded-sm p-4 flex flex-wrap items-center justify-between gap-4 text-xs font-mono">
          <div className="flex items-center space-x-6 flex-wrap gap-y-2">
            <div>
              <span className="text-[#787b86] uppercase mr-2">Target Buy Zone:</span>
              <strong className="text-[#089981] px-2 py-1 bg-[#089981]/10 rounded">{executionPlan.ideal_buy_zone}</strong>
            </div>
            <div>
              <span className="text-[#787b86] uppercase mr-2">Stop Loss:</span>
              <strong className="text-[#f23645] px-2 py-1 bg-[#f23645]/10 rounded">{executionPlan.stop_loss}</strong>
            </div>
            <div>
              <span className="text-[#787b86] uppercase mr-2">Take Profit:</span>
              <strong className="text-[#089981] px-2 py-1 bg-[#089981]/10 rounded">{executionPlan.take_profit}</strong>
            </div>
          </div>
          <div className="text-[#f2a900] bg-[#f2a900]/10 border border-[#f2a900]/30 px-3 py-1 font-semibold text-[10px] uppercase rounded">
            {executionPlan.execution_warning}
          </div>
        </div>
      )}
    </div>
  );
}
