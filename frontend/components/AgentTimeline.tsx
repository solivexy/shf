"use client";

import React, { useState } from "react";
import { TimelineLog } from "@/hooks/useLiveAnalysis";
import { ChevronDown, ChevronUp, Terminal, Zap } from "lucide-react";

interface Props {
  logs: TimelineLog[];
}

export default function AgentTimeline({ logs }: Props) {
  const [expandedLog, setExpandedLog] = useState<string | null>(null);

  return (
    <div className="bg-[#1e222d] border border-[#2a2e39] font-mono select-none flex flex-col h-full">
      {/* Sidebar Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#2a2e39] bg-[#131722] text-xs">
        <div className="flex items-center space-x-2">
          <Terminal className="w-3.5 h-3.5 text-[#2962ff]" />
          <span className="font-bold text-[#d1d4dc] uppercase tracking-tight">MULTI-AGENT STREAM</span>
        </div>
        <span className="text-[11px] text-[#787b86]">9 NODES</span>
      </div>

      {/* Log Rows Container */}
      <div className="divide-y divide-[#2a2e39] overflow-y-auto flex-1">
        {logs.map((log) => {
          const isCompleted = log.status === "COMPLETED";
          const isRunning = log.status === "RUNNING";
          const isFailed = log.status === "FAILED";
          const isExpanded = expandedLog === log.agent_name;

          const statusColor = isCompleted
            ? "text-[#089981]"
            : isRunning
            ? "text-[#2962ff] animate-pulse font-bold"
            : isFailed
            ? "text-[#f23645] font-bold"
            : "text-[#787b86]";

          return (
            <div key={log.agent_name} className="bg-[#1e222d] hover:bg-[#2a2e39]/40 transition-colors text-xs">
              <div
                className="p-2.5 flex items-center justify-between cursor-pointer"
                onClick={() => setExpandedLog(isExpanded ? null : log.agent_name)}
              >
                <div className="flex items-center space-x-2 min-w-0">
                  <span className={`text-[10px] uppercase font-bold px-1.5 py-0.5 border ${
                    isCompleted ? "border-[#089981]/30 text-[#089981] bg-[#089981]/10" :
                    isRunning ? "border-[#2962ff]/30 text-[#2962ff] bg-[#2962ff]/10" :
                    isFailed ? "border-[#f23645]/30 text-[#f23645] bg-[#f23645]/10" :
                    "border-[#2a2e39] text-[#787b86]"
                  }`}>
                    {log.status}
                  </span>

                  <span className="font-semibold text-[#d1d4dc] truncate text-xs">{log.agent_name}</span>
                </div>

                <div className="flex items-center space-x-3 flex-shrink-0">
                  {log.confidence !== undefined && log.confidence !== null && (
                    <span className="text-[10px] text-[#787b86] hidden sm:inline">
                      CF:<strong className="text-[#d1d4dc] ml-0.5">{log.confidence}%</strong>
                    </span>
                  )}
                  {log.runtime_ms ? (
                    <span className="text-[10px] text-[#787b86] flex items-center">
                      <Zap className="w-2.5 h-2.5 text-[#f2a900] mr-0.5" />
                      <span>{log.runtime_ms}ms</span>
                    </span>
                  ) : null}
                  <div className="text-[#787b86]">
                    {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </div>
                </div>
              </div>

              {/* Expandable Inspection Drawer */}
              {isExpanded && (
                <div className="p-2.5 border-t border-[#2a2e39] bg-[#131722] space-y-2 text-[11px] text-[#d1d4dc]">
                  {log.summary && (
                    <div>
                      <div className="text-[#787b86] text-[10px] uppercase mb-0.5 font-semibold">Execution Summary</div>
                      <div className="p-2 bg-[#1e222d] border border-[#2a2e39] leading-relaxed">{log.summary}</div>
                    </div>
                  )}
                  {log.reasoning && (
                    <div>
                      <div className="text-[#787b86] text-[10px] uppercase mb-0.5 font-semibold">Quant / AI Synthesis</div>
                      <div className="p-2 bg-[#1e222d] border border-[#2a2e39] leading-relaxed">{log.reasoning}</div>
                    </div>
                  )}
                  {log.output_json && (
                    <div>
                      <div className="text-[#787b86] text-[10px] uppercase mb-0.5 font-semibold">Structured JSON Payload</div>
                      <pre className="p-2 bg-[#0f111a] border border-[#2a2e39] overflow-x-auto text-[10px] text-[#38bdf8] max-h-96">
                        {JSON.stringify(log.output_json, null, 2)}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
