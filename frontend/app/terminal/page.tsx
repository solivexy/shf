"use client";

import React, { useState, useEffect } from "react";
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
  const [inputTicker, setInputTicker] = useState<string>("");
  const { ticker, taskId, state, loading, error, startAnalysis, loadAnalysis } = useLiveAnalysis("");
  const [activeTab, setActiveTab] = useState<"ALL" | "REGIME" | "NEWS" | "TECHNICAL" | "MACRO" | "OPTIONS" | "RISK">("ALL");
  const [recentReports, setRecentReports] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/reports?limit=6")
      .then((res) => res.json())
      .then((data) => {
        if (data.reports) setRecentReports(data.reports);
      })
      .catch((err) => console.error("Failed to load recent reports", err));

    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const passedTaskId = urlParams.get("taskId");
      if (passedTaskId) {
        loadAnalysis(passedTaskId);
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    }
  }, []);

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
      {(!state && !loading) ? (
        <div className="max-w-7xl mx-auto w-full px-6 py-12 flex flex-col items-center text-center animate-fade-in">
          <div className="w-16 h-16 rounded-full bg-accent/20 flex items-center justify-center text-accent mb-6 shadow-[0_0_30px_rgba(41,98,255,0.2)]">
            <Search className="w-8 h-8" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-4">Welcome to the AI Terminal</h2>
          <p className="text-textSecondary text-[17px] leading-relaxed max-w-2xl mb-12">
            Enter a stock symbol above (e.g., AAPL or BBRI.JK) to dispatch the autonomous multi-agent system. The AI will synthesize technicals, historical regimes, macroeconomics, and options flow to provide an institutional-grade recommendation.
          </p>
          
          <div className="w-full max-w-4xl text-left">
            <h3 className="text-xs font-bold text-[#787b86] uppercase tracking-wider mb-4 px-2">Popular Stocks (Click to Analyze)</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {[
                { symbol: "AAPL", name: "Apple Inc.", sector: "Technology" },
                { symbol: "NVDA", name: "NVIDIA Corp.", sector: "Semiconductors" },
                { symbol: "TSLA", name: "Tesla Inc.", sector: "Automotive" },
                { symbol: "BBRI.JK", name: "Bank Rakyat", sector: "Finance (ID)" },
                { symbol: "GOTO.JK", name: "GoTo Gojek", sector: "Tech (ID)" }
              ].map((stock) => (
                <button
                  key={stock.symbol}
                  onClick={() => {
                    setInputTicker(stock.symbol);
                    startAnalysis(stock.symbol);
                  }}
                  className="bg-[#1e222d] border border-[#2a2e39] p-4 rounded flex flex-col items-start text-left transition-all hover:border-[#2962ff] hover:-translate-y-1"
                >
                  <span className="text-[17px] font-bold text-white">{stock.symbol}</span>
                  <span className="text-[11px] text-[#787b86] truncate w-full mt-1">{stock.name}</span>
                  <span className="text-[9px] text-[#2962ff] mt-2 uppercase font-bold tracking-wide bg-[#2962ff]/10 px-1.5 py-0.5 rounded">{stock.sector}</span>
                </button>
              ))}
            </div>
          </div>

          {recentReports.length > 0 && (
            <div className="w-full max-w-4xl text-left mt-8">
              <h3 className="text-xs font-bold text-[#787b86] uppercase tracking-wider mb-4 px-2">Recent Analyses</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {recentReports.map((report) => (
                  <button
                    key={report.report_id}
                    onClick={() => {
                      setInputTicker(report.ticker);
                      loadAnalysis(report.report_id);
                    }}
                    className="bg-[#1e222d] border border-[#2a2e39] p-4 rounded flex flex-col items-start text-left transition-all hover:border-[#2962ff] hover:-translate-y-1 relative overflow-hidden group"
                  >
                    <div className="flex justify-between w-full items-center mb-2">
                      <span className="text-[17px] font-bold text-white">{report.ticker}</span>
                      <span className={`text-[10px] uppercase font-bold tracking-wide px-2 py-0.5 rounded ${report.decision.includes("Buy") ? "bg-[#089981]/10 text-[#089981]" : report.decision.includes("Sell") || report.decision.includes("Reduce") ? "bg-[#f23645]/10 text-[#f23645]" : "bg-[#f2a900]/10 text-[#f2a900]"}`}>
                        {report.decision}
                      </span>
                    </div>
                    <span className="text-[11px] text-[#787b86] line-clamp-2 w-full leading-relaxed">{report.summary}</span>
                    <div className="mt-4 text-[10px] text-[#787b86] flex justify-between w-full font-mono uppercase">
                      <span>Conf: {report.confidence}%</span>
                      <span>{new Date(report.created_at).toLocaleDateString()}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
      <div className="flex-1 w-full max-w-[1600px] mx-auto px-6 pb-12 flex flex-col space-y-6 animate-fade-in">
        
        {/* Top Section */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
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
          </div>

          {/* Right Sidebar: Timeline */}
          <div className="lg:col-span-1 glass-panel overflow-hidden relative min-h-[400px]">
            <div className="absolute inset-0 flex flex-col">
              <AgentTimeline logs={logs} />
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="flex flex-col w-full">
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
          <div className="bg-transparent p-0 space-y-6 mt-4">
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
      </div>
      )}
    </div>
  );
}
