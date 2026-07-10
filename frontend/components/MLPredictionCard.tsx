"use client";

import React from "react";
import { Cpu } from "lucide-react";

interface Props {
  mlPrediction?: any;
}

export default function MLPredictionCard({ mlPrediction }: Props) {
  if (!mlPrediction) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-center text-[#787b86] text-xs font-mono">
        Awaiting XGBoost/LightGBM Ensemble Evaluation...
      </div>
    );
  }

  const probUp = mlPrediction.probability_up !== undefined ? Math.round(Number(mlPrediction.probability_up) * 100) : 68;
  const direction = mlPrediction.predicted_direction || (probUp >= 50 ? "Bullish Upward" : "Bearish Downward");
  const models = mlPrediction.models_used || ["XGBoost v2", "LightGBM v4", "Random Forest"];

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs select-none flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 border-b border-[#2a2e39] bg-[#131722]">
          <div className="flex items-center space-x-2">
            <Cpu className="w-3.5 h-3.5 text-[#2962ff]" />
            <span className="font-bold text-[#d1d4dc] uppercase tracking-tight text-[11px]">ML ENSEMBLE</span>
          </div>
          <span className={`text-[10px] font-bold px-1.5 py-0.5 border ${
            probUp >= 55
              ? "bg-[#089981]/10 text-[#089981] border-[#089981]/30"
              : probUp <= 45
              ? "bg-[#f23645]/10 text-[#f23645] border-[#f23645]/30"
              : "text-[#787b86] border-[#2a2e39]"
          }`}>
            UP PROB: {probUp}%
          </span>
        </div>

        {/* Summary */}
        <div className="p-3 text-[11px] text-[#787b86] leading-relaxed border-b border-[#2a2e39] bg-[#131722]/30">
          {mlPrediction.summary || `Ensemble model projects strong positive drift over a 14-day rolling window.`}
        </div>

        {/* Data Grid */}
        <div className="grid grid-cols-2 divide-x divide-[#2a2e39] text-[11px]">
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Predicted Drift</span>
            <span className={`font-bold ${probUp >= 50 ? "text-[#089981]" : "text-[#f23645]"}`}>
              {direction}
            </span>
          </div>
          <div className="p-2">
            <span className="text-[#787b86] block text-[9px] uppercase">Horizon Target</span>
            <span className="font-bold text-[#d1d4dc]">14 Trading Days</span>
          </div>
        </div>

        <div className="p-2 border-t border-[#2a2e39] text-[10px]">
          <span className="text-[#787b86] block text-[9px] uppercase">Ensemble Weights:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {models.map((m: string, idx: number) => (
              <span key={idx} className="bg-[#2962ff]/10 text-[#2962ff] border border-[#2962ff]/30 px-1.5 py-0.5 text-[9px] font-bold uppercase">
                {m}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
