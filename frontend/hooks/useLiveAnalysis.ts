"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";

export interface TimelineLog {
  agent_name: string;
  status: string;
  runtime_ms?: number;
  confidence?: number;
  summary?: string;
  reasoning?: string;
  output_json?: any;
}

export interface AnalysisState {
  task_id: string;
  ticker: string;
  status: "RUNNING" | "COMPLETED" | "FAILED";
  timeline_logs: TimelineLog[];
  market_data?: any;
  historical_regime?: any;
  technical_analysis?: any;
  news_intelligence?: any;
  macro_economy?: any;
  options_flow?: any;
  risk_manager?: any;
  ml_prediction?: any;
  portfolio_manager?: any;
  execution_plan?: any;
}

export function useLiveAnalysis(initialTicker: string = "") {
  const [ticker, setTicker] = useState<string>(initialTicker);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [state, setState] = useState<AnalysisState | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const startAnalysis = useCallback(async (targetTicker: string) => {
    setLoading(true);
    setError(null);
    setTicker(targetTicker.toUpperCase().trim());
    try {
      const resp = await axios.post("http://localhost:8000/api/v1/analyze", {
        ticker: targetTicker.toUpperCase().trim(),
      });
      const data = resp.data as AnalysisState;
      setTaskId(data.task_id);
      setState(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Failed to start analysis job.");
      setLoading(false);
    }
  }, []);

  const loadAnalysis = useCallback(async (targetTaskId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`http://localhost:8000/api/v1/analyze/status/${targetTaskId}`);
      if (res.data) {
        setTicker(res.data.ticker);
        setTaskId(res.data.task_id);
        setState(res.data);
        if (res.data.status === "COMPLETED" || res.data.status === "FAILED") {
          setLoading(false);
        }
      }
    } catch (err: any) {
      setError("Failed to load historical analysis.");
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!taskId) return;
    if (state?.status === "COMPLETED" || state?.status === "FAILED") return; // Skip WS if already done

    // Connect WebSocket
    const wsUrl = `ws://localhost:8000/api/v1/ws/live/${taskId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === "STEP_COMPLETED" || payload.type === "ANALYSIS_COMPLETED" || payload.type === "ANALYSIS_STARTED") {
          if (payload.data) {
            setState(payload.data);
            if (payload.data.status === "COMPLETED" || payload.data.status === "FAILED") {
              setLoading(false);
            }
          }
        }
      } catch (e) {
        console.error("WebSocket payload parsing error:", e);
      }
    };

    ws.onerror = () => {
      console.warn("WebSocket error or fallback triggered. Polling HTTP status...");
    };

    // Polling fallback every 1.5s while RUNNING
    const interval = setInterval(async () => {
      if (ws.readyState !== WebSocket.OPEN || state?.status === "RUNNING") {
        try {
          const res = await axios.get(`http://localhost:8000/api/v1/analyze/status/${taskId}`);
          if (res.data) {
            setState(res.data);
            if (res.data.status === "COMPLETED" || res.data.status === "FAILED") {
              setLoading(false);
              clearInterval(interval);
            }
          }
        } catch (e) {}
      }
    }, 1500);

    return () => {
      clearInterval(interval);
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [taskId]);

  return {
    ticker,
    taskId,
    state,
    loading,
    error,
    startAnalysis,
    loadAnalysis,
  };
}
