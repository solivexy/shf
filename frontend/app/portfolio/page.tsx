"use client";

import React, { useState } from "react";
import axios from "axios";
import { PieChart, Sliders, CheckCircle2, Loader2, AlertCircle, Plus, Trash2 } from "lucide-react";

export default function PortfolioPage() {
  const [tickers, setTickers] = useState<string[]>(["AAPL", "NVDA", "MSFT", "AMZN"]);
  const [newTicker, setNewTicker] = useState<string>("");
  const [riskProfile, setRiskProfile] = useState<string>("Balanced");
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  const addTicker = (e: React.FormEvent) => {
    e.preventDefault();
    if (newTicker.trim() && !tickers.includes(newTicker.trim().toUpperCase())) {
      setTickers([...tickers, newTicker.trim().toUpperCase()]);
      setNewTicker("");
    }
  };

  const removeTicker = (t: string) => {
    setTickers(tickers.filter((item) => item !== t));
  };

  const handleOptimize = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await axios.post("http://localhost:8000/api/v1/portfolio/optimize", {
        tickers,
        target_risk: riskProfile,
      });
      setResult(resp.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Optimization request failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-44px)] bg-[#131722] text-[#d1d4dc] font-mono select-none">
      {/* Header Bar */}
      <div className="bg-[#1e222d] border-b border-[#2a2e39] px-4 py-3 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-3">
          <PieChart className="w-4 h-4 text-[#2962ff]" />
          <div>
            <span className="font-bold text-[#d1d4dc] uppercase">MEAN-VARIANCE & HRP PORTFOLIO OPTIMIZER</span>
            <span className="text-[#787b86] block text-[11px] mt-0.5">
              Ledoit-Wolf shrinkage matrix with Black-Litterman equilibrium adjustments
            </span>
          </div>
        </div>
        <span className="bg-[#131722] border border-[#2a2e39] text-[#089981] px-2.5 py-1 text-[11px] uppercase font-bold">
          QUANT ENGINE READY
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-px bg-[#2a2e39]">
        {/* Left Parameters Panel */}
        <div className="lg:col-span-1 bg-[#1e222d] p-4 space-y-5 text-xs">
          <div className="flex items-center space-x-2 border-b border-[#2a2e39] pb-2 text-[#d1d4dc] font-bold uppercase">
            <Sliders className="w-3.5 h-3.5 text-[#2962ff]" />
            <span>ALLOCATION PARAMETERS</span>
          </div>

          <div>
            <label className="text-[#787b86] text-[10px] uppercase block mb-2 font-bold">Target Risk Profile</label>
            <div className="grid grid-cols-3 gap-1">
              {["Conservative", "Balanced", "Aggressive"].map((profile) => (
                <button
                  key={profile}
                  type="button"
                  onClick={() => setRiskProfile(profile)}
                  className={`py-2 px-1 text-[11px] font-bold uppercase border transition-colors ${
                    riskProfile === profile
                      ? "bg-[#2962ff] text-white border-[#2962ff]"
                      : "bg-[#131722] border-[#2a2e39] text-[#787b86] hover:text-[#d1d4dc]"
                  }`}
                >
                  {profile}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-[#787b86] text-[10px] uppercase block mb-2 font-bold">Asset Universe ({tickers.length})</label>
            <form onSubmit={addTicker} className="flex items-center space-x-1 mb-3">
              <input
                type="text"
                value={newTicker}
                onChange={(e) => setNewTicker(e.target.value.toUpperCase())}
                placeholder="ADD TICKER..."
                className="flex-1 bg-[#131722] border border-[#2a2e39] px-2 py-1.5 text-xs text-[#d1d4dc] font-bold focus:outline-none focus:border-[#2962ff] placeholder-[#787b86]"
              />
              <button
                type="submit"
                className="bg-[#2962ff] hover:bg-[#1e4bd8] text-white px-3 py-1.5 font-bold transition-colors border border-[#2962ff]"
              >
                <Plus className="w-4 h-4" />
              </button>
            </form>

            <div className="flex flex-wrap gap-1.5 max-h-56 overflow-y-auto pr-1">
              {tickers.map((t) => (
                <div
                  key={t}
                  className="flex items-center space-x-1.5 bg-[#131722] border border-[#2a2e39] px-2 py-1 text-xs text-[#d1d4dc]"
                >
                  <span className="font-bold">{t}</span>
                  <button onClick={() => removeTicker(t)} className="text-[#787b86] hover:text-[#f23645]">
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={handleOptimize}
            disabled={loading || tickers.length < 2}
            className="w-full bg-[#089981] hover:bg-[#07806b] disabled:opacity-50 text-white py-2.5 text-xs font-bold uppercase flex items-center justify-center space-x-2 transition-colors border border-[#089981]"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
            <span>COMPUTE OPTIMAL WEIGHTS</span>
          </button>
        </div>

        {/* Right Output Workstation */}
        <div className="lg:col-span-3 bg-[#131722] p-6 flex flex-col justify-between">
          {error && (
            <div className="bg-[#f23645]/10 border border-[#f23645] text-[#f23645] p-3 flex items-center space-x-2 text-xs font-mono mb-4">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {result ? (
            <div className="space-y-6">
              <div className="flex items-center justify-between border-b border-[#2a2e39] pb-3 text-xs">
                <span className="font-bold text-[#d1d4dc] uppercase">OPTIMIZED ASSET ALLOCATION MATRIX</span>
                <span className="text-[#089981] bg-[#089981]/10 border border-[#089981]/30 px-2 py-0.5 font-bold uppercase text-[11px]">
                  STATUS: CONVERGED ({riskProfile})
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-[#2a2e39] border border-[#2a2e39]">
                {Object.entries(result.weights || {}).map(([symbol, weight]: [string, any]) => {
                  const pct = (Number(weight) * 100).toFixed(1);
                  return (
                    <div key={symbol} className="bg-[#1e222d] p-4">
                      <span className="text-[#787b86] block text-[11px] font-bold">{symbol}</span>
                      <span className="text-xl font-bold text-[#2962ff] mt-1 block">{pct}%</span>
                      <div className="w-full bg-[#131722] h-1 mt-3 overflow-hidden">
                        <div className="bg-[#2962ff] h-full" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>

              {result.metrics && (
                <div className="border border-[#2a2e39] grid grid-cols-3 divide-x divide-[#2a2e39] bg-[#1e222d] text-xs">
                  <div className="p-4">
                    <span className="text-[#787b86] uppercase block text-[10px]">Expected Annual Return</span>
                    <span className="font-bold text-[#089981] text-base mt-1 block">{(result.metrics.expected_return * 100).toFixed(2)}%</span>
                  </div>
                  <div className="p-4">
                    <span className="text-[#787b86] uppercase block text-[10px]">Portfolio Volatility</span>
                    <span className="font-bold text-[#f2a900] text-base mt-1 block">{(result.metrics.volatility * 100).toFixed(2)}%</span>
                  </div>
                  <div className="p-4">
                    <span className="text-[#787b86] uppercase block text-[10px]">Optimal Sharpe Ratio</span>
                    <span className="font-bold text-[#2962ff] text-base mt-1 block">{result.metrics.sharpe_ratio.toFixed(2)}</span>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-16 text-[#787b86] font-mono text-xs border border-dashed border-[#2a2e39] bg-[#1e222d]/40">
              <PieChart className="w-10 h-10 text-[#787b86]/40 mb-3" />
              <p className="uppercase tracking-wide font-bold">Configure asset universe and target risk above, then execute.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
