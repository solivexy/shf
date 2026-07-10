import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data


def test_portfolio_optimize_endpoint():
    response = client.post("/api/v1/portfolio/optimize", json={
        "tickers": ["AAPL", "NVDA", "MSFT"],
        "target_risk": "Balanced"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "weights" in data
    assert len(data["weights"]) == 3
    assert abs(sum(data["weights"].values()) - 1.0) < 0.05


def test_backtest_endpoint():
    response = client.post("/api/v1/backtest", json={
        "ticker": "AAPL",
        "initial_capital": 50000.0,
        "strategy_type": "RSI Momentum"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert "sharpe_ratio" in data
    assert "equity_curve" in data
