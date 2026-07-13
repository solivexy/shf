"use client";

import React from "react";
import { BookOpen, Target, Cpu, Shield, HelpCircle } from "lucide-react";

export default function TutorialPage() {
  return (
    <div className="min-h-screen bg-[#131722] text-[#d1d4dc] font-sans p-6 md:p-12 pb-24 selection:bg-[#2962ff]/30">
      <div className="max-w-3xl mx-auto space-y-16">
        
        {/* Header section */}
        <div className="border-b border-[#2a2e39] pb-8 mb-12">
          <div className="flex items-center space-x-4 mb-6">
            <div className="bg-[#2962ff]/10 p-3 rounded-lg border border-[#2962ff]/30">
              <BookOpen className="w-8 h-8 text-[#2962ff]" />
            </div>
            <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
              Beginner's Guide
            </h1>
          </div>
          <p className="text-[#787b86] text-lg leading-relaxed">
            Welcome to the AI Hedge Fund. This platform is designed to do the heavy lifting of financial analysis for you. Here is a simple guide on how to run your first scan and understand the results.
          </p>
        </div>

        {/* Step-by-Step Guide */}
        <section className="space-y-8">
          <h2 className="text-2xl font-bold text-white tracking-tight mb-6">How to Run a Scan</h2>
          
          <div className="space-y-6">
            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md flex gap-6">
              <div className="text-[#2962ff] font-black text-4xl opacity-50">1</div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Launch the Scan</h3>
                <p className="text-[#d1d4dc] leading-relaxed">
                  Go to the <strong>Chart Terminal</strong> tab. Type in any stock symbol (like <code className="bg-[#131722] text-[#2962ff] px-1.5 py-0.5 rounded text-sm border border-[#2a2e39]">AAPL</code>) and click the blue <strong>Launch Scan</strong> button.
                </p>
              </div>
            </div>

            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md flex gap-6">
              <div className="text-[#089981] font-black text-4xl opacity-50">2</div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Wait for the AI</h3>
                <p className="text-[#d1d4dc] leading-relaxed">
                  On the right side of your screen, you'll see a live timeline. The AI agents are reading the news, looking at charts, and checking the economy. This usually takes about 15-30 seconds.
                </p>
              </div>
            </div>

            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md flex gap-6">
              <div className="text-[#f2a900] font-black text-4xl opacity-50">3</div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Read the Recommendation</h3>
                <p className="text-[#d1d4dc] leading-relaxed">
                  Once finished, a large Dossier will appear at the top. The AI will give you a clear <strong>BUY</strong>, <strong>HOLD</strong>, or <strong>SELL</strong> rating.
                </p>
              </div>
            </div>

            <div className="bg-[#1e222d] border border-[#2a2e39] p-6 rounded-md flex gap-6">
              <div className="text-[#f23645] font-black text-4xl opacity-50">4</div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Follow the Execution Plan</h3>
                <p className="text-[#d1d4dc] leading-relaxed">
                  If you decide to buy the stock, use the <strong>Execution Plan</strong> provided. It tells you exactly what price to buy at, and more importantly, where to set your Stop-Loss to protect your money.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How to Read the Results */}
        <section className="space-y-6 pt-8 border-t border-[#2a2e39]">
          <h2 className="text-2xl font-bold text-white tracking-tight mb-6">How to Read the Results</h2>
          <div className="bg-[#1e222d] border border-[#2a2e39] rounded-md overflow-hidden">
            <div className="p-6 border-b border-[#2a2e39] bg-[#131722]/50">
              <h3 className="text-white font-bold mb-2">The AI Recommendation</h3>
              <p className="text-[#d1d4dc] text-sm leading-relaxed mb-4">The top row of the dossier is the most important. It summarizes everything into 4 simple columns:</p>
              <ul className="space-y-3 text-sm text-[#787b86]">
                <li><strong className="text-white">1. Action (If Owned):</strong> If you already have this stock in your portfolio, should you keep holding it, or sell it right now?</li>
                <li><strong className="text-white">2. Action (Not Owned):</strong> If you <em>don't</em> have this stock, is today a safe day to buy it?</li>
                <li><strong className="text-[#2962ff]">3. AI Certainty:</strong> If this number is below 60%, the AI is conflicted and you should avoid the trade. If it's above 80%, the AI is highly confident.</li>
                <li><strong className="text-[#089981]">4. Portfolio Size:</strong> This tells you exactly how much to buy. If your total portfolio is $10,000 and it says 5.0%, you should only buy $500 worth of this stock.</li>
              </ul>
            </div>
            <div className="p-6">
              <h3 className="text-white font-bold mb-2">The Execution Plan</h3>
              <p className="text-[#d1d4dc] text-sm leading-relaxed mb-4">If you decide to buy, never just click "Market Buy". Use the exact prices the AI calculated for you:</p>
              <ul className="space-y-3 text-sm text-[#787b86]">
                <li><strong className="text-white">Target Buy Zone:</strong> Try to buy the stock between the Floor and Ceiling prices. If the stock is currently trading <em>above</em> the Ceiling, it's too expensive—wait for it to drop into the zone.</li>
                <li><strong className="text-[#f23645]">Stop Loss:</strong> As soon as you buy the stock, set an automatic "Stop-Loss" order at your broker for this exact price. If the stock drops to this price, it will automatically sell, preventing you from losing a catastrophic amount of money.</li>
                <li><strong className="text-[#089981]">Take Profit:</strong> Place an automatic "Limit Sell" order at this price. When the stock goes up and hits this target, you lock in your profits automatically.</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Glossary of Terms */}
        <section className="space-y-6 pt-8 border-t border-[#2a2e39]">
          <h2 className="text-2xl font-bold text-white tracking-tight mb-6">Simple Dictionary</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#131722] border border-[#2a2e39] p-5 rounded-md">
              <div className="flex items-center space-x-2 mb-2">
                <Target className="w-5 h-5 text-[#089981]" />
                <h3 className="text-white font-bold">Portfolio Size (Kelly)</h3>
              </div>
              <p className="text-sm text-[#787b86] leading-relaxed">
                The percentage of your total money the AI suggests risking on this stock. It's a math formula used by pros to grow money quickly without going broke.
              </p>
            </div>

            <div className="bg-[#131722] border border-[#2a2e39] p-5 rounded-md">
              <div className="flex items-center space-x-2 mb-2">
                <Cpu className="w-5 h-5 text-[#2962ff]" />
                <h3 className="text-white font-bold">AI Certainty</h3>
              </div>
              <p className="text-sm text-[#787b86] leading-relaxed">
                A score from 0% to 100%. If it's high, it means all the AI agents agreed with each other.
              </p>
            </div>

            <div className="bg-[#131722] border border-[#2a2e39] p-5 rounded-md">
              <div className="flex items-center space-x-2 mb-2">
                <Shield className="w-5 h-5 text-[#f23645]" />
                <h3 className="text-white font-bold">Stop Loss</h3>
              </div>
              <p className="text-sm text-[#787b86] leading-relaxed">
                An exact price to sell your stock if the trade goes bad. You should always use a stop-loss to protect yourself from losing too much money.
              </p>
            </div>

            <div className="bg-[#131722] border border-[#2a2e39] p-5 rounded-md">
              <div className="flex items-center space-x-2 mb-2">
                <HelpCircle className="w-5 h-5 text-[#f2a900]" />
                <h3 className="text-white font-bold">"If Owned" vs "Not Owned"?</h3>
              </div>
              <p className="text-sm text-[#787b86] leading-relaxed">
                The AI might tell someone who already owns the stock to "Hold" it, but tell someone who doesn't own it to "Wait". This is because buying a stock at today's high price is riskier than holding a stock you bought cheaper yesterday.
              </p>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}
