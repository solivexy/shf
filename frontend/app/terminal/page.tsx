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
    <div className="min-h-[calc(100vh-64px)] bg-background text-textPrimary flex flex-col font-sans">
      {/* Top Toolbar - Minimalist */}
      <div className="bg-transparent px-6 py-6 flex flex-wrap items-center justify-between gap-6 z-10 relative max-w-7xl mx-auto w-full">
        <div className="flex items-center space-x-6">
          <form onSubmit={handleSubmit} className="flex items-center">
            <div className="flex items-center bg-surface/60 backdrop-blur-xl border border-white/10 rounded-full pl-5 pr-2 py-1.5 focus-within:border-accent/80 transition-all">
              <span className="text-textSecondary mr-2 font-medium text-[15px]">Symbol</span>
              <input
                type="text"
                value={inputTicker}
                onChange={(e) => setInputTicker(e.target.value.toUpperCase())}
                placeholder="AAPL, NVDA..."
                className="w-24 sm:w-36 bg-transparent text-textPrimary font-semibold text-[15px] focus:outline-none placeholder-textSecondary/50"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-accent hover:bg-accentHover disabled:opacity-50 text-white rounded-full p-2 transition-colors ml-2 flex items-center justify-center shadow-md shadow-accent/20"
              >
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-current ml-0.5" />}
              </button>
            </div>
          </form>

          {/* Quick Symbol Tabs */}
          <div className="hidden md:flex items-center space-x-2 border-l border-white/10 pl-6 text-[14px]">
            {["AAPL", "NVDA", "MSFT", "TSLA", "AMZN"].map((t) => (
              <button
                key={t}
                onClick={() => {
                  setInputTicker(t);
                  startAnalysis(t);
                }}
                className={`px-4 py-1.5 rounded-full font-medium transition-colors duration-200 ${
                  ticker === t
                    ? "bg-white text-black"
                    : "text-textSecondary hover:text-textPrimary hover:bg-surface"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {/* Engine Status */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-[14px]">
            <span className="text-textSecondary">Engine</span>
            <strong className={loading ? "text-accent animate-pulse" : "text-success"}>
              {state?.status || "Ready"}
            </strong>
          </div>
        </div>
      </div>

      {error && (
        <div className="max-w-7xl mx-auto w-full px-6 mb-4">
          <div className="bg-danger/10 text-danger px-6 py-4 rounded-2xl flex items-center space-x-3 text-[15px]">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span>{error}</span>
          </div>
        </div>
      )}

      {/* Main Container */}
      <div className="flex-1 w-full max-w-[1600px] mx-auto px-6 pb-12 grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Left 3 Columns: Workstation */}
        <div className="lg:col-span-3 flex flex-col space-y-6">
          
          <div className="glass-panel overflow-hidden p-2">
            <CIORecommendationCard
              portfolioManager={state?.portfolio_manager}
              executionPlan={state?.execution_plan}
              ticker={ticker}
              marketData={state?.market_data}
            />
          </div>

          <div className="glass-panel overflow-hidden p-2">
            <PriceChart ticker={ticker} currentPrice={currentPrice} marketData={state?.market_data} />
          </div>

          {/* Lower Terminal Tabs Bar - Minimalist */}
          <div className="flex flex-wrap items-center gap-x-2 gap-y-2 text-[14px] font-medium pt-2 pb-2">
            {[
              { id: "ALL", label: "Overview" },
              { id: "REGIME", label: "Historical Regime" },
              { id: "NEWS", label: "News & Catalysts" },
              { id: "TECHNICAL", label: "Technical Indicators" },
              { id: "MACRO", label: "Macro Audit" },
              { id: "OPTIONS", label: "Options Flow" },
              { id: "RISK", label: "Risk Ensemble" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-2 rounded-full transition-colors duration-200 ${
                  activeTab === tab.id
                    ? "bg-surfaceHover text-white shadow-sm border border-white/5"
                    : "text-textSecondary hover:text-textPrimary hover:bg-surface/50"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Lower Pane Content */}
          <div className="bg-transparent p-0 space-y-6">
            {(activeTab === "ALL" || activeTab === "REGIME") && (
              <div className="glass-panel overflow-hidden p-2">
                <HistoricalRegimeCard historicalRegime={state?.historical_regime} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "NEWS") && (
              <div className="glass-panel overflow-hidden p-2">
                <NewsCard newsIntelligence={state?.news_intelligence} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "TECHNICAL") && (
              <div className="glass-panel overflow-hidden p-2">
                <TechnicalIndicatorsTable technicalAnalysis={state?.technical_analysis} />
              </div>
            )}

            {(activeTab === "ALL" || activeTab === "MACRO" || activeTab === "OPTIONS" || activeTab === "RISK") && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {(activeTab === "ALL" || activeTab === "MACRO") && (
                  <div className="glass-panel overflow-hidden p-2"><MacroCard macroEconomy={state?.macro_economy} /></div>
                )}
                {(activeTab === "ALL" || activeTab === "OPTIONS") && (
                  <div className="glass-panel overflow-hidden p-2"><OptionsFlowCard optionsFlow={state?.options_flow} ticker={ticker} /></div>
                )}
                {(activeTab === "ALL" || activeTab === "RISK") && (
                  <div className="glass-panel overflow-hidden p-2"><RiskMetricsCard riskManager={state?.risk_manager} /></div>
                )}
                {(activeTab === "ALL" || activeTab === "RISK") && (
                  <div className="glass-panel overflow-hidden p-2"><MLPredictionCard mlPrediction={state?.ml_prediction} /></div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Right Sidebar: Timeline */}
        <div className="lg:col-span-1 glass-panel flex flex-col overflow-hidden relative min-h-[600px]">
          <AgentTimeline logs={logs} />
        </div>
      </div>
    </div>
  );
}
