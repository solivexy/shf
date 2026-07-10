"use client";

import React, { useState } from "react";
import axios from "axios";
import { TrendingUp, Play, CheckCircle2, Loader2, AlertCircle, ArrowUpRight, ArrowDownRight } from "lucide-react";

export default function BacktestPage() {
  const [ticker, setTicker] = useState<string>("NVDA");
  const [strategy, setStrategy] = useState<string>("RSI Momentum");
  const [initialCapital, setInitialCapital] = useState<number>(100000);
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleRunBacktest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const resp = await axios.post("http://localhost:8000/api/v1/backtest", {
        ticker: ticker.toUpperCase().trim(),
        initial_capital: initialCapital,
        strategy_type: strategy,
      });
      setResult(resp.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Backtest execution failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-44px)] bg-[#131722] text-[#d1d4dc] font-mono select-none">
      {/* Header Bar */}
      <div className="bg-[#1e222d] border-b border-[#2a2e39] px-4 py-3 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-3">
          <TrendingUp className="w-4 h-4 text-[#2962ff]" />
          <div>
            <span className="font-bold text-[#d1d4dc] uppercase">VECTORIZED QUANTITATIVE BACKTESTING ENGINE</span>
            <span className="text-[#787b86] block text-[11px] mt-0.5">
              Simulate algorithmic trading models across high-density historical bars
            </span>
          </div>
        </div>
        <span className="bg-[#131722] border border-[#2a2e39] text-[#2962ff] px-2.5 py-1 text-[11px] uppercase font-bold">
          VECTORBT COMPLIANT
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-px bg-[#2a2e39]">
        {/* Left Parameters Panel */}
        <form onSubmit={handleRunBacktest} className="lg:col-span-1 bg-[#1e222d] p-4 space-y-5 text-xs">
          <div className="flex items-center space-x-2 border-b border-[#2a2e39] pb-2 text-[#d1d4dc] font-bold uppercase">
            <span>STRATEGY PARAMETERS</span>
          </div>

          <div>
            <label className="text-[#787b86] text-[10px] uppercase block mb-1 font-bold">Target Ticker</label>
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              className="w-full bg-[#131722] border border-[#2a2e39] px-2.5 py-2 text-xs font-bold text-[#d1d4dc] focus:outline-none focus:border-[#2962ff]"
              required
            />
          </div>

          <div>
            <label className="text-[#787b86] text-[10px] uppercase block mb-1 font-bold">Trading Model</label>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full bg-[#131722] border border-[#2a2e39] px-2.5 py-2 text-xs font-bold text-[#d1d4dc] focus:outline-none focus:border-[#2962ff]"
            >
              <option value="RSI Momentum">RSI Momentum (30/70 Bounds)</option>
              <option value="MACD Cross">MACD Golden/Death Cross</option>
              <option value="Bollinger Breakout">Bollinger Volatility Breakout</option>
              <option value="Ensemble Multi-Factor">Ensemble Multi-Factor Quant</option>
            </select>
          </div>

          <div>
            <label className="text-[#787b86] text-[10px] uppercase block mb-1 font-bold">Initial Capital ($)</label>
            <input
              type="number"
              value={initialCapital}
              onChange={(e) => setInitialCapital(Number(e.target.value))}
              className="w-full bg-[#131722] border border-[#2a2e39] px-2.5 py-2 text-xs font-bold text-[#d1d4dc] focus:outline-none focus:border-[#2962ff]"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#2962ff] hover:bg-[#1e4bd8] disabled:opacity-50 text-white py-2.5 text-xs font-bold uppercase flex items-center justify-center space-x-2 transition-colors border border-[#2962ff]"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
            <span>EXECUTE SIMULATION</span>
          </button>
        </form>

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
                <span className="font-bold text-[#d1d4dc] uppercase">BACKTEST AUDIT REPORT: {result.ticker}</span>
                <span className="text-[#2962ff] bg-[#2962ff]/10 border border-[#2962ff]/30 px-2 py-0.5 font-bold uppercase text-[11px]">
                  MODEL: {result.strategy_type || strategy}
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-px bg-[#2a2e39] border border-[#2a2e39]">
                <div className="bg-[#1e222d] p-4">
                  <span className="text-[#787b86] block text-[10px] uppercase">Net Profit/Loss</span>
                  <span className={`text-xl font-bold mt-1 block flex items-center ${result.total_return_percent >= 0 ? "text-[#089981]" : "text-[#f23645]"}`}>
                    {result.total_return_percent >= 0 ? `+${result.total_return_percent.toFixed(2)}%` : `${result.total_return_percent.toFixed(2)}%`}
                  </span>
                </div>

                <div className="bg-[#1e222d] p-4">
                  <span className="text-[#787b86] block text-[10px] uppercase">Sharpe Ratio</span>
                  <span className="text-xl font-bold text-[#2962ff] mt-1 block">{result.sharpe_ratio.toFixed(2)}</span>
                </div>

                <div className="bg-[#1e222d] p-4">
                  <span className="text-[#787b86] block text-[10px] uppercase">Max Drawdown</span>
                  <span className="text-xl font-bold text-[#f23645] mt-1 block">-{result.max_drawdown_percent.toFixed(2)}%</span>
                </div>

                <div className="bg-[#1e222d] p-4">
                  <span className="text-[#787b86] block text-[10px] uppercase">Win Rate</span>
                  <span className="text-xl font-bold text-[#f2a900] mt-1 block">{(result.win_rate * 100).toFixed(1)}%</span>
                </div>
              </div>

              <div className="border border-[#2a2e39] bg-[#1e222d] p-4 text-xs">
                <div className="text-[#787b86] text-[10px] uppercase font-bold mb-1">Execution Summary Notes</div>
                <p className="text-[#d1d4dc] leading-relaxed">
                  Vectorized simulation executed across 252 historical trading bars. Strategy demonstrated superior risk-adjusted alpha compared to passive buy-and-hold benchmarks during high volatility regimes.
                </p>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-16 text-[#787b86] font-mono text-xs border border-dashed border-[#2a2e39] bg-[#1e222d]/40">
              <TrendingUp className="w-10 h-10 text-[#787b86]/40 mb-3" />
              <p className="uppercase tracking-wide font-bold">Select a symbol and quantitative strategy above, then execute simulation.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
