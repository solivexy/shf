"use client";

import React from "react";
import { History, TrendingUp, AlertCircle, Calendar, BarChart2, CheckCircle2 } from "lucide-react";

interface Props {
  historicalRegime?: any;
}

export default function HistoricalRegimeCard({ historicalRegime }: Props) {
  if (!historicalRegime) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-xs font-mono text-[#787b86] flex items-center justify-center space-x-2 h-64">
        <History className="w-4 h-4 animate-spin text-[#2962ff]" />
        <span>COMPUTING 5-YEAR HISTORICAL QUANTITATIVE REGIME AUDIT...</span>
      </div>
    );
  }

  const {
    cagr_5y = 0.0,
    cagr_3y = 0.0,
    cagr_1y = 0.0,
    sharpe_ratio_5y = 0.0,
    sortino_ratio_5y = 0.0,
    max_drawdown_percent = 0.0,
    volatility_regime = "Stable Volatility",
    cyclicality_verdict = "Secular Growth",
    tail_risk_var_95 = 0.0,
    monthly_seasonality = [],
    regime_summary = "Long-term historical regime audit complete.",
    bars_analyzed = 1260,
  } = historicalRegime;

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-3 py-2 border-b border-[#2a2e39] bg-[#131722] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <History className="w-4 h-4 text-[#2962ff]" />
          <span className="font-bold text-[#d1d4dc] uppercase tracking-tight">
            5-YEAR QUANTITATIVE REGIME AUDIT ({bars_analyzed} BARS)
          </span>
        </div>
        <span className="px-2 py-0.5 bg-[#2962ff]/20 text-[#2962ff] font-semibold rounded text-[10px] border border-[#2962ff]/40">
          MULTI-YEAR ALPHA
        </span>
      </div>

      <div className="p-3 flex-1 flex flex-col space-y-4 overflow-y-auto">
        {/* Top Key Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          <div className="bg-[#131722] p-2.5 border border-[#2a2e39]">
            <div className="text-[10px] text-[#787b86] uppercase mb-0.5">5-Year CAGR</div>
            <div className={`text-base font-bold ${cagr_5y >= 0 ? "text-[#089981]" : "text-[#f23645]"}`}>
              {cagr_5y >= 0 ? "+" : ""}{cagr_5y}%
            </div>
            <div className="text-[10px] text-[#787b86] mt-0.5">1Y: {cagr_1y >= 0 ? "+" : ""}{cagr_1y}% | 3Y: {cagr_3y >= 0 ? "+" : ""}{cagr_3y}%</div>
          </div>

          <div className="bg-[#131722] p-2.5 border border-[#2a2e39]">
            <div className="text-[10px] text-[#787b86] uppercase mb-0.5">5Y Sharpe Ratio</div>
            <div className={`text-base font-bold ${sharpe_ratio_5y >= 1.0 ? "text-[#089981]" : "text-[#f59e0b]"}`}>
              {sharpe_ratio_5y}
            </div>
            <div className="text-[10px] text-[#787b86] mt-0.5">Sortino: {sortino_ratio_5y}</div>
          </div>

          <div className="bg-[#131722] p-2.5 border border-[#2a2e39]">
            <div className="text-[10px] text-[#787b86] uppercase mb-0.5">Max Drawdown</div>
            <div className="text-base font-bold text-[#f23645]">
              -{max_drawdown_percent}%
            </div>
            <div className="text-[10px] text-[#787b86] mt-0.5">Tail VaR 95%: {tail_risk_var_95}%</div>
          </div>

          <div className="bg-[#131722] p-2.5 border border-[#2a2e39]">
            <div className="text-[10px] text-[#787b86] uppercase mb-0.5">Cyclical Classification</div>
            <div className="text-xs font-bold text-[#d1d4dc] truncate" title={cyclicality_verdict}>
              {cyclicality_verdict}
            </div>
            <div className="text-[10px] text-[#089981] mt-0.5 truncate">{volatility_regime}</div>
          </div>
        </div>

        {/* Gemini Quantitative AI Synthesis */}
        <div className="bg-[#131722] p-3 border border-[#2a2e39] border-l-4 border-l-[#2962ff]">
          <div className="flex items-center space-x-1.5 text-[11px] font-bold text-[#2962ff] uppercase mb-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>AI Quantitative Historical Synthesis</span>
          </div>
          <p className="text-xs text-[#d1d4dc] leading-relaxed italic">{regime_summary}</p>
        </div>

        {/* Monthly Return Seasonality Heatmap */}
        <div>
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] font-bold text-[#d1d4dc] uppercase flex items-center space-x-1">
              <Calendar className="w-3.5 h-3.5 text-[#089981]" />
              <span>Historical Monthly Seasonality Heatmap (Avg % Return)</span>
            </span>
          </div>
          <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-12 gap-1">
            {monthly_seasonality.map((m: any, idx: number) => {
              const ret = Number(m.avg_return || 0);
              const isPos = ret >= 0;
              return (
                <div
                  key={idx}
                  className={`p-1.5 border text-center flex flex-col justify-between ${
                    isPos
                      ? "bg-[#089981]/15 border-[#089981]/40 text-[#089981]"
                      : "bg-[#f23645]/15 border-[#f23645]/40 text-[#f23645]"
                  }`}
                >
                  <span className="text-[10px] font-bold text-[#d1d4dc] uppercase">{m.month}</span>
                  <span className="text-xs font-bold my-1">{isPos ? "+" : ""}{ret}%</span>
                  <span className="text-[9px] text-[#787b86]">{m.win_prob || 60}% win</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
