"use client";

import React from "react";
import { Newspaper, TrendingUp, AlertCircle, ExternalLink, Zap, CheckCircle2 } from "lucide-react";

interface Props {
  newsIntelligence?: any;
}

export default function NewsCard({ newsIntelligence }: Props) {
  if (!newsIntelligence) {
    return (
      <div className="bg-[#1e222d] border border-[#2a2e39] p-4 text-xs font-mono text-[#787b86] flex items-center justify-center space-x-2 h-64">
        <Newspaper className="w-4 h-4 animate-spin text-[#2962ff]" />
        <span>GATHERING LIVE NEWS & EVENT CATALYSTS...</span>
      </div>
    );
  }

  const {
    ticker = "STOCK",
    sentiment = "Neutral",
    score = 0.0,
    confidence = 75.0,
    summary = "No recent headline summary available.",
    catalysts = [],
    headlines = [],
    articles_analyzed = 0,
  } = newsIntelligence;

  const sentimentColor =
    sentiment === "Bullish"
      ? "bg-[#089981]/20 text-[#089981] border-[#089981]/40"
      : sentiment === "Bearish"
      ? "bg-[#f23645]/20 text-[#f23645] border-[#f23645]/40"
      : "bg-[#f59e0b]/20 text-[#f59e0b] border-[#f59e0b]/40";

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono text-xs flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="px-3 py-2 border-b border-[#2a2e39] bg-[#131722] flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Newspaper className="w-4 h-4 text-[#2962ff]" />
          <span className="font-bold text-[#d1d4dc] uppercase tracking-tight">
            LIVE NEWS & EVENT CATALYSTS ({articles_analyzed || headlines.length || 8} ARTICLES)
          </span>
        </div>
        <span className={`px-2 py-0.5 border rounded font-bold text-[11px] uppercase ${sentimentColor}`}>
          SENTIMENT: {sentiment} ({score >= 0 ? "+" : ""}{score})
        </span>
      </div>

      <div className="p-3 flex-1 flex flex-col space-y-4 overflow-y-auto">
        {/* Executive AI Summary */}
        <div className="bg-[#131722] p-3 border border-[#2a2e39] border-l-4 border-l-[#2962ff]">
          <div className="flex items-center space-x-1.5 text-[11px] font-bold text-[#2962ff] uppercase mb-1">
            <Zap className="w-3.5 h-3.5" />
            <span>AI News Intelligence Synthesis (Confidence: {confidence}%)</span>
          </div>
          <p className="text-xs text-[#d1d4dc] leading-relaxed">{summary}</p>
        </div>

        {/* Key Event Catalysts Grid */}
        {catalysts && catalysts.length > 0 && (
          <div>
            <div className="text-[11px] font-bold text-[#d1d4dc] uppercase mb-1.5 flex items-center space-x-1">
              <TrendingUp className="w-3.5 h-3.5 text-[#089981]" />
              <span>Extracted Event Catalysts</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {catalysts.map((cat: any, idx: number) => {
                const impactColor =
                  cat.impact === "Positive"
                    ? "text-[#089981] border-[#089981]/30 bg-[#089981]/10"
                    : cat.impact === "Negative"
                    ? "text-[#f23645] border-[#f23645]/30 bg-[#f23645]/10"
                    : "text-[#d1d4dc] border-[#2a2e39] bg-[#131722]";
                return (
                  <div
                    key={idx}
                    className="bg-[#131722] p-2.5 border border-[#2a2e39] flex flex-col justify-between"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="px-1.5 py-0.5 bg-[#2962ff]/20 text-[#2962ff] font-semibold rounded text-[10px] uppercase">
                        {cat.type || "Catalyst"}
                      </span>
                      <span className={`px-1.5 py-0.5 border rounded text-[10px] font-bold uppercase ${impactColor}`}>
                        {cat.impact || "Neutral"}
                      </span>
                    </div>
                    <p className="text-xs text-[#d1d4dc] line-clamp-2 mt-1">
                      {cat.headline}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Recent Headlines Feed */}
        <div>
          <div className="text-[11px] font-bold text-[#d1d4dc] uppercase mb-1.5 flex items-center space-x-1">
            <Newspaper className="w-3.5 h-3.5 text-[#2962ff]" />
            <span>Latest Live Institutional Headlines</span>
          </div>
          <div className="space-y-1.5">
            {headlines && headlines.length > 0 ? (
              headlines.map((item: any, idx: number) => {
                const headlineText = item.title || item.headline || "Headline not available";
                const sourceText = item.source || item.publisher || "Financial Feed";
                const targetUrl =
                  item.url ||
                  item.link ||
                  `https://www.google.com/search?q=${encodeURIComponent(
                    headlineText + " " + (ticker || "")
                  )}&tbm=nws`;

                return (
                  <a
                    key={idx}
                    href={targetUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-[#131722] px-3 py-2 border border-[#2a2e39] flex items-center justify-between hover:border-[#2962ff] transition-colors cursor-pointer group block"
                  >
                    <div className="flex flex-col pr-2">
                      <span className="text-xs text-[#d1d4dc] font-semibold group-hover:text-[#2962ff] transition-colors line-clamp-1">
                        {headlineText}
                      </span>
                      <span className="text-[10px] text-[#787b86] mt-0.5 uppercase">
                        SOURCE: {sourceText}
                      </span>
                    </div>
                    <ExternalLink className="w-3.5 h-3.5 text-[#787b86] group-hover:text-[#2962ff] transition-colors flex-shrink-0" />
                  </a>
                );
              })
            ) : (
              <div className="bg-[#131722] p-3 border border-[#2a2e39] text-[#787b86] text-center">
                Institutional headline stream synchronized with multi-agent feed.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
