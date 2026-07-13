"use client";

import React, { useState } from "react";
import { useLiveAnalysis } from "@/hooks/useLiveAnalysis";
import AgentTimeline from "@/components/AgentTimeline";
import PriceChart from "@/components/PriceChart";
import CIORecommendationCard from "@/components/CIORecommendationCard";
import TechnicalIndicatorsTable from "@/components/TechnicalIndicatorsTable";
import MacroCard from "@/components/MacroCard";
import OptionsFlowCard from "@/components/OptionsFlowCard";
import RiskMetricsCard from "@/components/RiskMetricsCard";
import MLPredictionCard from "@/components/MLPredictionCard";
import HistoricalRegimeCard from "@/components/HistoricalRegimeCard";
import NewsCard from "@/components/NewsCard";
import { Search, Play, Loader2, AlertCircle, RefreshCw } from "lucide-react";

export default function TerminalPage() {
  const [inputTicker, setInputTicker] = useState<string>("AAPL");
  const { ticker, taskId, state, loading, error, startAnalysis } = useLiveAnalysis("AAPL");
  const [activeTab, setActiveTab] = useState<"ALL" | "REGIME" | "NEWS" | "TECHNICAL" | "MACRO" | "OPTIONS" | "RISK">("ALL");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputTicker.trim()) {
      startAnalysis(inputTicker.trim());
    }
  };

  const currentPrice = state?.market_data?.current_price || 150.0;
  const logs = state?.timeline_logs || [];

  return (
    <div className="min-h-[calc(100vh-44px)] bg-[#131722] text-[#d1d4dc] font-mono flex flex-col">
      {/* TradingView Top Toolbar */}
      <div className="bg-[#1e222d] border-b border-[#2a2e39] px-3 py-1.5 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center space-x-3">
          <form onSubmit={handleSubmit} className="flex items-center">
            <div className="flex items-center bg-[#131722] border border-[#2a2e39] px-2 py-1 text-xs">
              <span className="text-[#787b86] mr-1.5 uppercase font-bold text-[10px]">Symbol:</span>
              <input
                type="text"
                value={inputTicker}
                onChange={(e) => setInputTicker(e.target.value.toUpperCase())}
                placeholder="AAPL, NVDA, TSLA..."
                className="w-24 sm:w-32 bg-transparent text-[#d1d4dc] font-bold focus:outline-none placeholder-[#787b86]"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="bg-[#2962ff] hover:bg-[#1e4bd8] disabled:opacity-50 text-white font-bold px-3 py-1 text-xs flex items-center space-x-1.5 transition-colors border border-[#2962ff]"
            >
              {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5" />}
              <span>{loading ? "SCANNING..." : "LAUNCH SCAN"}</span>
            </button>
          </form>

          {/* Quick Symbol Tabs */}
          <div className="hidden lg:flex items-center space-x-1 border-l border-[#2a2e39] pl-3 text-[11px]">
            {["AAPL", "NVDA", "MSFT", "TSLA", "AMZN"].map((t) => (
              <button
                key={t}
                onClick={() => {
                  setInputTicker(t);
                  startAnalysis(t);
                }}
                className={`px-2 py-0.5 border ${
                  ticker === t
                    ? "border-[#2962ff] bg-[#2962ff]/10 text-[#2962ff] font-bold"
                    : "border-transparent text-[#787b86] hover:text-[#d1d4dc]"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Engine Status & Refresh */}
        <div className="flex items-center space-x-3 text-[11px]">
          <div className="flex items-center space-x-1.5 bg-[#131722] border border-[#2a2e39] px-2 py-1">
            <span className="text-[#787b86] uppercase">Engine:</span>
            <strong className={loading ? "text-[#2962ff] animate-pulse" : "text-[#089981]"}>
              {state?.status || "READY"}
            </strong>
          </div>
          {taskId && (
            <span className="text-[#787b86] hidden sm:inline truncate max-w-[150px]">
              ID: {taskId}
            </span>
          )}
        </div>
      </div>

      {error && (
        <div className="bg-[#f23645]/10 border-b border-[#f23645] text-[#f23645] px-4 py-2 flex items-center space-x-2 text-xs font-mono">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Split Workstation Container */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-px bg-[#2a2e39]">
        {/* Left 3 Columns: Chart, CIO Card, and Specialized Panes */}
        <div className="lg:col-span-3 bg-[#131722] flex flex-col space-y-px bg-[#2a2e39]">
          {/* CIO Recommendation & Order Execution Banner */}
          <CIORecommendationCard
            portfolioManager={state?.portfolio_manager}
            executionPlan={state?.execution_plan}
            ticker={ticker}
            marketData={state?.market_data}
          />

          {/* Candlestick Chart Pane */}
          <PriceChart ticker={ticker} currentPrice={currentPrice} marketData={state?.market_data} />

          {/* Lower Terminal Tabs Bar */}
          <div className="bg-[#1e222d] border-y border-[#2a2e39] px-3 py-1.5 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs font-semibold">
            <span className="text-[#787b86] uppercase text-[10px]">Intelligence Panes:</span>
            {[
              { id: "ALL", label: "ALL METRICS" },
              { id: "REGIME", label: "5Y HISTORICAL REGIME" },
              { id: "NEWS", label: "NEWS & CATALYSTS" },
              { id: "TECHNICAL", label: "TECHNICAL INDICATORS" },
              { id: "MACRO", label: "MACRO AUDIT" },
              { id: "OPTIONS", label: "OPTIONS FLOW" },
              { id: "RISK", label: "RISK & ML ENSEMBLE" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`pb-1 border-b-2 text-[11px] uppercase transition-colors ${
                  activeTab === tab.id
                    ? "border-[#2962ff] text-[#2962ff]"
                    : "border-transparent text-[#787b86] hover:text-[#d1d4dc]"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Lower Pane Content */}
          <div className="bg-[#131722] p-0">
            {(activeTab === "ALL" || activeTab === "REGIME") && (
              <div className="mb-px">
                <HistoricalRegimeCard historicalRegime={state?.historical_regime} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "NEWS") && (
              <div className="mb-px">
                <NewsCard newsIntelligence={state?.news_intelligence} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "TECHNICAL") && (
              <div className="mb-px">
                <TechnicalIndicatorsTable technicalAnalysis={state?.technical_analysis} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "MACRO" || activeTab === "OPTIONS" || activeTab === "RISK") && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-px bg-[#2a2e39]">
                {(activeTab === "ALL" || activeTab === "MACRO") && (
                  <MacroCard macroEconomy={state?.macro_economy} />
                )}
                {(activeTab === "ALL" || activeTab === "OPTIONS") && (
                  <OptionsFlowCard optionsFlow={state?.options_flow} ticker={ticker} />
                )}
                {(activeTab === "ALL" || activeTab === "RISK") && (
                  <RiskMetricsCard riskManager={state?.risk_manager} />
                )}
                {(activeTab === "ALL" || activeTab === "RISK") && (
                  <MLPredictionCard mlPrediction={state?.ml_prediction} />
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Sidebar: Real-Time Multi-Agent Execution Log */}
        <div className="lg:col-span-1 bg-[#1e222d] flex flex-col border-l border-[#2a2e39]">
          <AgentTimeline logs={logs} />
        </div>
      </div>
    </div>
  );
}
