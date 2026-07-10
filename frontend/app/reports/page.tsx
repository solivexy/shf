"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { FileText, Loader2, RefreshCw, AlertCircle, Calendar, ExternalLink, Download, BarChart2 } from "lucide-react";

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await axios.get("http://localhost:8000/api/v1/reports?limit=25");
      setReports(resp.data?.reports || []);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Failed to retrieve institutional dossiers.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <div className="min-h-[calc(100vh-44px)] bg-[#131722] text-[#d1d4dc] font-mono select-none flex flex-col">
      {/* Header Bar */}
      <div className="bg-[#1e222d] border-b border-[#2a2e39] px-4 py-3 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-3">
          <FileText className="w-4 h-4 text-[#2962ff]" />
          <div>
            <span className="font-bold text-[#d1d4dc] uppercase">INSTITUTIONAL AI RESEARCH DOSSIERS</span>
            <span className="text-[#787b86] block text-[11px] mt-0.5">
              Persistent quantitative evaluation logs across multi-agent workflows
            </span>
          </div>
        </div>
        <button
          onClick={fetchReports}
          disabled={loading}
          className="bg-[#131722] hover:bg-[#2a2e39] border border-[#2a2e39] text-[#d1d4dc] px-3 py-1.5 text-xs font-bold uppercase flex items-center space-x-1.5 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-[#2962ff]" : ""}`} />
          <span>REFRESH DOSSIERS</span>
        </button>
      </div>

      <div className="flex-1 p-6">
        {error && (
          <div className="bg-[#f23645]/10 border border-[#f23645] text-[#f23645] p-3 flex items-center space-x-2 text-xs font-mono mb-4">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 text-[#787b86] space-y-3">
            <Loader2 className="w-8 h-8 text-[#2962ff] animate-spin" />
            <span className="text-xs uppercase tracking-wider font-bold">Querying MongoDB Dossier Vault...</span>
          </div>
        ) : reports.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center text-[#787b86] border border-dashed border-[#2a2e39] bg-[#1e222d]/40 p-10">
            <FileText className="w-10 h-10 text-[#787b86]/40 mb-3" />
            <span className="uppercase tracking-wide font-bold">No research dossiers archived in database yet.</span>
            <p className="text-[11px] mt-1">Run an analysis scan in the Chart Terminal to generate dossiers.</p>
          </div>
        ) : (
          <div className="divide-y divide-[#2a2e39] border border-[#2a2e39] bg-[#1e222d]">
            {reports.map((r, idx) => (
              <div key={idx} className="p-4 hover:bg-[#2a2e39]/30 transition-colors flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div className="space-y-1.5 flex-1 pr-4">
                  <div className="flex items-center space-x-2.5">
                    <span className="font-bold text-base text-[#d1d4dc] uppercase tracking-tight">{r.ticker || "UNKNOWN"}</span>
                    <span className="text-[10px] text-[#787b86] border border-[#2a2e39] px-2 py-0.5 bg-[#131722] font-semibold">
                      ID: {r.report_id || r._id || `DOSSIER-${idx + 1}`}
                    </span>
                    <span className={`px-2 py-0.5 border font-bold uppercase text-[11px] ${
                      r.decision === "Buy" || r.decision === "Strong Buy"
                        ? "text-[#089981] border-[#089981]/30 bg-[#089981]/10"
                        : r.decision === "Sell" || r.decision === "Strong Sell"
                        ? "text-[#f23645] border-[#f23645]/30 bg-[#f23645]/10"
                        : "text-[#f2a900] border-[#f2a900]/30 bg-[#f2a900]/10"
                    }`}>
                      {r.decision || "HOLD"} ({r.confidence || "85"}%)
                    </span>
                  </div>
                  <p className="text-xs text-[#d1d4dc] leading-relaxed">{r.summary || "Complete multi-agent quantitative evaluation."}</p>
                  <div className="text-[10px] text-[#787b86] flex items-center space-x-1 pt-0.5">
                    <Calendar className="w-3 h-3 text-[#2962ff]" />
                    <span>ARCHIVED: {r.created_at ? new Date(r.created_at).toLocaleString() : "TODAY"}</span>
                  </div>
                </div>

                <div className="flex flex-wrap items-center gap-2 flex-shrink-0 text-xs">
                  <a
                    href={`http://localhost:8000${r.pdf_url || `/api/v1/reports/pdf/${r.report_id || r._id}`}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1.5 bg-[#2962ff]/20 hover:bg-[#2962ff]/40 text-[#2962ff] border border-[#2962ff]/40 font-bold flex items-center space-x-1.5 transition-colors uppercase text-[11px]"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>PDF DOSSIER</span>
                  </a>
                  <a
                    href={`http://localhost:8000${r.csv_url || `/api/v1/reports/csv/${r.report_id || r._id}`}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1.5 bg-[#131722] hover:bg-[#2a2e39] text-[#d1d4dc] border border-[#2a2e39] font-bold flex items-center space-x-1.5 transition-colors uppercase text-[11px]"
                  >
                    <FileText className="w-3.5 h-3.5 text-[#787b86]" />
                    <span>CSV EXPORT</span>
                  </a>
                  <a
                    href={`/?ticker=${r.ticker || "AAPL"}`}
                    className="px-3 py-1.5 bg-[#089981]/20 hover:bg-[#089981]/40 text-[#089981] border border-[#089981]/40 font-bold flex items-center space-x-1.5 transition-colors uppercase text-[11px]"
                  >
                    <BarChart2 className="w-3.5 h-3.5" />
                    <span>CHART SCAN</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
