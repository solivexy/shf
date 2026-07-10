import pytest
import pandas as pd
import numpy as np
from indicators.technical import calculate_all_indicators, calculate_confluence_scores
from indicators.patterns import detect_classical_patterns
from indicators.risk_metrics import calculate_risk_metrics
from indicators.options_math import calculate_options_metrics


def test_deterministic_technical_indicators():
    np.random.seed(42)
    close = np.linspace(100, 150, 100) + np.random.normal(0, 1, 100)
    df = pd.DataFrame({
        "Close": close,
        "High": close + 2,
        "Low": close - 2,
        "Volume": np.random.randint(1_000_000, 5_000_000, 100)
    })
    
    indicators = calculate_all_indicators(df)
    assert "current_price" in indicators
    assert "sma_20" in indicators
    assert "rsi_14" in indicators
    assert "macd" in indicators
    assert "bollinger_bands" in indicators
    assert "ichimoku_cloud" in indicators

    bull, bear, neut = calculate_confluence_scores(indicators)
    assert 0.0 <= bull <= 100.0
    assert 0.0 <= bear <= 100.0
    assert 0.0 <= neut <= 100.0
    assert abs(bull + bear + neut - 100.0) < 1.0


def test_classical_pattern_recognition():
    np.random.seed(101)
    # Create simple dataframe
    close = np.ones(60) * 100.0
    df = pd.DataFrame({
        "Close": close,
        "High": close + 1,
        "Low": close - 1,
        "Volume": np.ones(60) * 2_000_000
    })
    patterns = detect_classical_patterns(df)
    assert isinstance(patterns, list)
    assert len(patterns) > 0


def test_risk_metrics():
    np.random.seed(202)
    returns = np.random.normal(0.0005, 0.015, 252)
    prices = 100 * np.cumprod(1 + returns)
    df = pd.DataFrame({"Close": prices, "Volume": np.ones(252) * 5_000_000})

    risk = calculate_risk_metrics(df)
    assert "sharpe_ratio" in risk
    assert "max_drawdown_percent" in risk
    assert "var_95_percent" in risk
    assert "risk_category" in risk
    assert risk["risk_category"] in ["Low", "Medium", "High", "Extreme"]


def test_options_math():
    options_chain = {
        "calls": [
            {"strike": 150.0, "openInterest": 5000, "impliedVolatility": 0.28},
            {"strike": 155.0, "openInterest": 3000, "impliedVolatility": 0.30}
        ],
        "puts": [
            {"strike": 145.0, "openInterest": 4000, "impliedVolatility": 0.29},
            {"strike": 140.0, "openInterest": 2000, "impliedVolatility": 0.31}
        ]
    }
    res = calculate_options_metrics(options_chain, current_price=150.0)
    assert "put_call_ratio" in res
    assert res["put_call_ratio"] == round(6000 / 8000, 2)
    assert "max_pain_strike" in res
    assert "institutional_sentiment" in res
