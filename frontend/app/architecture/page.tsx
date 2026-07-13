"use client";

import React from "react";
import { 
  Database, LineChart, Globe, Briefcase, 
  ShieldAlert, Bot, BrainCircuit, Target,
  Cpu, AlignLeft, BarChart3, Binary
} from "lucide-react";

export default function ArchitecturePage() {
  return (
    <div className="min-h-screen bg-[#131722] text-[#d1d4dc] font-sans p-6 md:p-12 pb-24 selection:bg-[#2962ff]/30">
      <div className="max-w-4xl mx-auto space-y-12">
        
        {/* Header section */}
        <div className="border-b border-[#2a2e39] pb-8 mb-12">
          <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight mb-4">
            Under the Hood: System Architecture
          </h1>
          <p className="text-[#787b86] text-lg leading-relaxed max-w-3xl">
            This platform operates as a multi-agent system. Rather than relying on a single monolithic model, it deploys an ensemble of 8 specialized, independent AI agents. Each agent is strictly confined to a single domain of expertise to prevent bias, culminating in a synthesized decision by the Portfolio Manager.
          </p>
        </div>

        {/* Phase 1: Data Gathering */}
        <section className="space-y-6">
          <div className="flex items-center space-x-3 mb-6">
            <Database className="text-[#d1d4dc] w-6 h-6" />
            <h2 className="text-2xl font-bold text-white tracking-tight">1. Raw Intelligence Intake</h2>
          </div>
          <p className="text-[#787b86] leading-relaxed">
            Before any analysis begins, the system queries institutional-grade data providers to assemble a complete snapshot of the asset and the broader market. This includes high-frequency OHLCV (Open, High, Low, Close, Volume) data, global macroeconomic metrics (CPI, treasury yields), live options chain data, and real-time news headlines.
          </p>
        </section>

        {/* Phase 2: Specialist Agents */}
        <section className="space-y-8 pt-8 border-t border-[#2a2e39]">
          <div className="flex items-center space-x-3 mb-8">
            <Cpu className="text-[#d1d4dc] w-6 h-6" />
            <h2 className="text-2xl font-bold text-white tracking-tight">2. The Analyst Ensemble</h2>
          </div>
          
          <div className="space-y-6">
            
            {/* Technical Analyst */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <LineChart className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">Technical Analyst (TA)</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed mb-4">
                The TA agent processes historical price action using a comprehensive suite of mathematical indicators to identify momentum, trend strength, and mean-reversion setups.
              </p>
              <ul className="space-y-4 text-sm text-[#787b86]">
                <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                  <strong className="text-white">Moving Averages (SMA/EMA)</strong>
                  <p className="mt-1 mb-2">Identifies primary trend direction. EMA places higher weight on recent prices.</p>
                  <code className="block bg-[#1e222d] text-[#2962ff] p-2 rounded font-mono text-xs">
                    SMA = (P1 + P2 + ... + Pn) / n<br/>
                    EMA = Price(t) × k + EMA(y) × (1 - k)  [where k = 2 / (n + 1)]
                  </code>
                </li>
                <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                  <strong className="text-white">Relative Strength Index (RSI)</strong>
                  <p className="mt-1 mb-2">Measures momentum on a scale of 0 to 100. Values {'>'} 70 are overbought; {'<'} 30 are oversold.</p>
                  <code className="block bg-[#1e222d] text-[#2962ff] p-2 rounded font-mono text-xs">
                    RSI = 100 - [100 / (1 + (Average Gain / Average Loss))]
                  </code>
                </li>
                <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                  <strong className="text-white">MACD (Moving Average Convergence Divergence)</strong>
                  <p className="mt-1 mb-2">Tracks the relationship between two EMAs to spot trend changes.</p>
                  <code className="block bg-[#1e222d] text-[#2962ff] p-2 rounded font-mono text-xs">
                    MACD Line = 12-period EMA - 26-period EMA<br/>
                    Signal Line = 9-period EMA of MACD Line
                  </code>
                </li>
                <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                  <strong className="text-white">Bollinger Bands</strong>
                  <p className="mt-1 mb-2">Measures volatility using standard deviations away from the SMA.</p>
                  <code className="block bg-[#1e222d] text-[#2962ff] p-2 rounded font-mono text-xs">
                    Upper Band = 20-day SMA + (20-day Standard Deviation × 2)<br/>
                    Lower Band = 20-day SMA - (20-day Standard Deviation × 2)
                  </code>
                </li>
              </ul>
            </div>

            {/* Macro Economist */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <Briefcase className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">Macro Economist</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed mb-4">
                This agent ignores the stock entirely and evaluates the global economic climate to ensure systematic market risks won't invalidate the trade thesis.
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-[#787b86]">
                <li className="flex items-start space-x-2">
                  <span className="text-[#2962ff]">•</span>
                  <span><strong>Interest Rates & Yield Curve:</strong> Tracks Federal Reserve policy and treasury yields (e.g., 10Y/2Y inversion) to assess recessionary risk.</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-[#2962ff]">•</span>
                  <span><strong>Inflation (CPI/PCE):</strong> Evaluates purchasing power data to determine if monetary tightening will pressure equity valuations.</span>
                </li>
              </ul>
            </div>

            {/* Options Flow Analyst */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <BarChart3 className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">Options Flow Analyst</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed mb-4">
                Tracks "smart money" by analyzing institutional derivatives positioning, which often dictates underlying stock movements due to market maker hedging.
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-[#787b86]">
                <li className="flex items-start space-x-2">
                  <span className="text-[#2962ff]">•</span>
                  <span><strong>Gamma Exposure (GEX):</strong> Maps where market makers are forced to buy or sell stock to remain delta-neutral, creating synthetic support/resistance walls.</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-[#2962ff]">•</span>
                  <span><strong>Max Pain:</strong> Calculates the strike price where the maximum number of options expire worthless, acting as a "magnet" for the stock price.</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-[#2962ff]">•</span>
                  <span><strong>Put/Call Skew:</strong> Evaluates institutional sentiment by comparing the premiums paid for downside protection vs. upside speculation.</span>
                </li>
              </ul>
            </div>

            {/* ML Ensemble */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <BrainCircuit className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">Machine Learning (ML) Ensemble</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed">
                A purely quantitative, non-LLM agent. It utilizes heavily backtested algorithms (such as XGBoost and Random Forests) trained on decades of historical market regimes. It outputs a strict mathematical probability vector (e.g., 60% probability of positive returns over the next 30 days) devoid of narrative bias.
              </p>
            </div>

            {/* News & Catalyst Analyst */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <Globe className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">News & Catalyst Analyst</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed">
                Uses Natural Language Processing (NLP) to ingest real-time news headlines, SEC filings, and earnings transcripts. It scores the sentiment of the text (Bullish/Neutral/Bearish) and flags impending catalysts (like a scheduled FDA approval or earnings date) that could cause violent volatility, overriding standard technicals.
              </p>
            </div>

            {/* Risk Manager */}
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md">
              <div className="flex items-center space-x-3 mb-4">
                <ShieldAlert className="w-5 h-5 text-white" />
                <h3 className="text-lg font-bold text-white">Risk Manager</h3>
              </div>
              <p className="text-[#d1d4dc] text-sm leading-relaxed">
                Before a trade is authorized, the Risk Manager calculates the Value-at-Risk (VaR) and historical volatility metrics (like Beta and ATR). If a stock is demonstrating erratic behavior outside its normal standard deviations, this agent will aggressively reduce the allowed position size to protect the portfolio's capital.
              </p>
            </div>

          </div>
        </section>

        {/* Phase 3: CIO Synthesis */}
        <section className="space-y-6 pt-8 border-t border-[#2a2e39]">
          <div className="flex items-center space-x-3 mb-6">
            <Bot className="text-[#d1d4dc] w-6 h-6" />
            <h2 className="text-2xl font-bold text-white tracking-tight">3. Portfolio Manager Synthesis</h2>
          </div>
          <div className="bg-[#1e222d] border border-[#2a2e39] p-6 md:p-8 rounded-md">
            <p className="text-[#d1d4dc] leading-relaxed mb-6">
              The Portfolio Manager (Acting as the Chief Investment Officer) receives the disparate reports from all 6 specialized agents. Its sole job is to resolve conflicting data and calculate a final institutional consensus.
            </p>
            
            <h4 className="text-white font-bold mb-3">Conflict Resolution Logic:</h4>
            <ul className="space-y-3 text-sm text-[#787b86] list-disc pl-5">
              <li>If the <strong>Technical Analyst</strong> flags a "Strong Buy" breakout, but the <strong>Options Analyst</strong> detects massive institutional Put-buying (smart money betting against the stock), the Portfolio Manager will downgrade the trade to a "Hold".</li>
              <li>If the <strong>Macro Economist</strong> flags severe recession risks, the Portfolio Manager will tighten stop-losses globally and demand higher conviction from the ML Ensemble before authorizing buys.</li>
            </ul>

            <div className="mt-8 bg-[#131722] p-6 rounded border border-[#2a2e39]">
              <h4 className="text-white font-bold text-lg mb-4">Outputs generated:</h4>
              <ul className="text-sm text-[#d1d4dc] space-y-6">
                <li>
                  <strong className="text-white text-base">1. Final Decision:</strong> 
                  <p className="mt-1 text-[#787b86]">A distinct recommendation (Buy/Hold/Sell) that explicitly separates advice for people who already own the stock vs. people looking to start a new position.</p>
                </li>
                <li>
                  <strong className="text-white text-base">2. AI Certainty (%):</strong> 
                  <p className="mt-1 text-[#787b86]">A quantitative score (e.g. 77%) showing how uniformly the 6 agents agreed with the final decision. High certainty means the Technicals, Fundamentals, and Options data are all perfectly aligned.</p>
                </li>
                <li>
                  <strong className="text-white text-base">3. Portfolio Size (The Kelly Criterion Calculation):</strong> 
                  <p className="mt-1 text-[#787b86] mb-3">The AI uses the mathematical Kelly Criterion to calculate exactly what percentage of your portfolio to risk. This guarantees that over infinite trades, your compound growth is maximized and your chance of total ruin is exactly zero.</p>
                  <div className="bg-[#1e222d] p-4 rounded border border-[#2a2e39] font-mono text-xs text-[#d1d4dc]">
                    <span className="text-[#f2a900]">Formula:</span> K% = W - [(1 - W) / R]<br/><br/>
                    <span className="text-white">Where:</span><br/>
                    <span className="text-[#2962ff]">K%</span> = The optimal Kelly percentage of your portfolio to risk.<br/>
                    <span className="text-[#2962ff]">W</span> = Win Probability (Derived from the AI Certainty Score, e.g., 0.77).<br/>
                    <span className="text-[#2962ff]">R</span> = Reward-to-Risk Ratio (Calculated as [Take Profit Distance] / [Stop Loss Distance]).<br/><br/>
                    <span className="text-white italic">Example:</span> If Win Prob is 60% (0.6) and Reward/Risk is 2.0:<br/>
                    K% = 0.60 - [(1 - 0.60) / 2.0]<br/>
                    K% = 0.60 - [0.40 / 2.0]<br/>
                    K% = 0.60 - 0.20 = <strong className="text-[#089981]">0.40 (Risk 40% of standard unit)</strong>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Phase 4: Execution Plan */}
        <section className="space-y-6 pt-8 border-t border-[#2a2e39]">
          <div className="flex items-center space-x-3 mb-6">
            <Binary className="text-[#089981] w-6 h-6" />
            <h2 className="text-2xl font-bold text-[#089981] tracking-tight">4. The Execution Plan</h2>
          </div>
          <div className="bg-[#1e222d] border border-[#089981]/30 p-6 md:p-8 rounded-md">
            <p className="text-[#d1d4dc] leading-relaxed mb-6">
              If the Portfolio Manager authorizes a "Buy" or "Hold", the <strong className="text-[#089981]">Execution Agent</strong> takes over. Deciding what to buy is only half the battle; knowing <em>when</em> and <em>where</em> to execute the trade is what separates professionals from amateurs.
            </p>
            
            <h4 className="text-white font-bold mb-3">Mathematical Execution Formulas:</h4>
            <ul className="space-y-4 text-sm text-[#787b86]">
              <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                <strong className="text-[#089981] text-base">The Target Buy Zone (Volume Profile & Fibonacci)</strong> 
                <p className="mt-1 mb-2">The AI scans the chart for "Support Walls" using Volume Profile (identifying the Price at Maximum Volume) and Fibonacci retracement levels from the most recent swing low.</p>
                <code className="block bg-[#1e222d] text-[#089981] p-2 rounded font-mono text-xs">
                  Buy Zone Floor = Max(Recent Swing Low, Volume Point of Control)<br/>
                  Buy Zone Ceiling = Fibonacci 0.382 Retracement Level
                </code>
              </li>
              <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                <strong className="text-[#f23645] text-base">The Stop-Loss Price (Average True Range)</strong> 
                <p className="mt-1 mb-2">The AI calculates the Average True Range (ATR) to measure the stock's normal daily "wiggles". It places the Stop-Loss outside this normal noise, preventing you from being "whipsawed" out of a good trade.</p>
                <code className="block bg-[#1e222d] text-[#f23645] p-2 rounded font-mono text-xs">
                  True Range (TR) = Max[ (High - Low), |High - Prev Close|, |Low - Prev Close| ]<br/>
                  ATR = 14-day Simple Moving Average of TR<br/><br/>
                  Stop-Loss Price = Entry Price - (1.5 × ATR)
                </code>
              </li>
              <li className="bg-[#131722] p-4 rounded border border-[#2a2e39]">
                <strong className="text-[#2962ff] text-base">The Take-Profit Price (Risk-Multiplied Resistance)</strong> 
                <p className="mt-1 mb-2">The AI identifies the next major "Resistance Wall" overhead, but strictly enforces a minimum Reward-to-Risk ratio (usually 2:1 or higher).</p>
                <code className="block bg-[#1e222d] text-[#2962ff] p-2 rounded font-mono text-xs">
                  Minimum Take-Profit = Entry Price + (Entry Price - Stop-Loss Price) × 2.0<br/>
                  Optimized Take-Profit = Min(Next Pivot High, Fibonacci 1.618 Extension)
                </code>
              </li>
            </ul>
          </div>
        </section>

      </div>
    </div>
  );
}
