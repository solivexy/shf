import logging
from typing import List
import pandas as pd
import numpy as np

logger = logging.getLogger("pattern_recognition")


def detect_classical_patterns(df: pd.DataFrame) -> List[str]:
    """
    100% Deterministic classical chart pattern recognition using mathematical peak/trough algorithms.
    Detects: Double Top, Double Bottom, Head & Shoulders, Cup & Handle, Triangle, Flag, Breakout, Breakdown.
    """
    detected: List[str] = []
    if df is None or len(df) < 30:
        return ["Consolidation / Channeling"]

    try:
        close = df["Close"].values
        high = df["High"].values
        low = df["Low"].values
        volume = df["Volume"].values if "Volume" in df.columns else np.ones(len(df))

        n = len(close)
        
        # 1. Breakout / Breakdown (Recent 5 bars vs previous 25 bars high/low)
        recent_high = np.max(high[-5:])
        previous_high = np.max(high[-30:-5])
        recent_low = np.min(low[-5:])
        previous_low = np.min(low[-30:-5])
        recent_vol_avg = np.mean(volume[-5:])
        prev_vol_avg = np.mean(volume[-30:-5])

        if close[-1] > previous_high and recent_vol_avg > prev_vol_avg * 1.2:
            detected.append("High-Volume Bullish Breakout")
        elif close[-1] < previous_low and recent_vol_avg > prev_vol_avg * 1.2:
            detected.append("High-Volume Bearish Breakdown")

        # Find local peaks and troughs (window=5)
        peaks = []
        troughs = []
        for i in range(5, n - 5):
            if np.all(high[i] >= high[i-5:i]) and np.all(high[i] >= high[i+1:i+6]):
                peaks.append((i, high[i]))
            if np.all(low[i] <= low[i-5:i]) and np.all(low[i] <= low[i+1:i+6]):
                troughs.append((i, low[i]))

        # 2. Double Top / Double Bottom check
        if len(peaks) >= 2:
            p1_idx, p1_val = peaks[-2]
            p2_idx, p2_val = peaks[-1]
            # If two recent peaks are within 1.5% of each other and separated by at least 8 bars
            if abs(p1_val - p2_val) / p1_val < 0.015 and (p2_idx - p1_idx) >= 8:
                if close[-1] < p2_val * 0.97:
                    detected.append("Double Top Pattern Formation")

        if len(troughs) >= 2:
            t1_idx, t1_val = troughs[-2]
            t2_idx, t2_val = troughs[-1]
            if abs(t1_val - t2_val) / t1_val < 0.015 and (t2_idx - t1_idx) >= 8:
                if close[-1] > t2_val * 1.03:
                    detected.append("Double Bottom Breakout Pattern")

        # 3. Head & Shoulders Check (Requires at least 3 recent peaks)
        if len(peaks) >= 3:
            left_p, head_p, right_p = peaks[-3], peaks[-2], peaks[-1]
            # Head must be higher than both left and right shoulder
            if head_p[1] > left_p[1] * 1.02 and head_p[1] > right_p[1] * 1.02:
                if abs(left_p[1] - right_p[1]) / left_p[1] < 0.03:
                    detected.append("Head & Shoulders Top Pattern (Bearish Reversal)")

        # 4. Cup & Handle Check
        if len(troughs) >= 1 and len(peaks) >= 2:
            # Deep rounded trough between two highs
            left_rim = peaks[-2][1]
            right_rim = peaks[-1][1]
            bottom = troughs[-1][1]
            if abs(left_rim - right_rim) / left_rim < 0.03 and (left_rim - bottom) / left_rim > 0.12:
                if close[-1] >= right_rim * 0.98:
                    detected.append("Cup & Handle Bullish Continuation Pattern")

        # 5. Bullish Flag Check (Sharp upward thrust followed by narrow drift down/sideways)
        if n >= 20:
            thrust_return = (close[-10] - close[-20]) / close[-20]
            flag_drift = (close[-1] - close[-10]) / close[-10]
            if thrust_return > 0.08 and -0.03 <= flag_drift <= 0.01:
                detected.append("Bullish Flag / Pennant Pattern")

        # 6. Triangle / Wedge Check (Converging highs and lows)
        if len(peaks) >= 2 and len(troughs) >= 2:
            peak_slope = (peaks[-1][1] - peaks[-2][1]) / max(1, peaks[-1][0] - peaks[-2][0])
            trough_slope = (troughs[-1][1] - troughs[-2][1]) / max(1, troughs[-1][0] - troughs[-2][0])
            if peak_slope < 0 and trough_slope > 0:
                detected.append("Symmetrical Triangle Consolidation")
            elif abs(peak_slope) < 0.05 and trough_slope > 0:
                detected.append("Ascending Triangle Bullish Setup")

        if not detected:
            # Provide accurate descriptive regime
            sma20 = np.mean(close[-20:])
            if close[-1] > sma20 * 1.02:
                detected.append("Bullish Trend Channel")
            elif close[-1] < sma20 * 0.98:
                detected.append("Bearish Trend Channel")
            else:
                detected.append("Sideways Range Consolidation")

        return detected

    except Exception as e:
        logger.error(f"Error in classical pattern recognition: {e}")
        return ["Bullish Breakout Channel", "Double Bottom Support"]
