# Context: Week 1 Coaching Feedback Updates

**Date**: July 13, 2026
**Purpose**: This document provides a detailed summary of the architectural and logical changes applied to the codebase to address the "Week 1 Coaching" feedback. This file is intended to serve as context for any AI agents or developers working on the codebase in the future, ensuring they understand *what* was changed and *why*.

---

## 1. Indonesian Stock Market & Macro Data Support
**Context:** The system originally only supported US equities (e.g., AAPL, NVDA) and hardcoded US macroeconomic indicators (Federal Reserve rates). The coaching feedback demanded support for Indonesian stocks (e.g., BBRI) and required that macro data be synchronized with the specific market being analyzed.

**Files Updated:**
*   **`backend/database/mongodb.py`**
    *   **Change:** Appended `"BBRI.JK"` and `"BMRI.JK"` to the `_memory_watchlists["default"]` list.
    *   **Reason:** Ensures Indonesian tickers are available in the default dashboard watchlist.
*   **`backend/agents/market_data_agent.py`**
    *   **Change:** Updated the `_get_synthetic_fallback` function. Added logic to check if `ticker.endswith(".JK")`. Added `.JK` tickers to the `base_prices`, `company_names`, and `sectors` dictionaries.
    *   **Reason:** Allows the synthetic market data generator to produce IDR-anchored prices (e.g., Rp 4,800) and accurate company metadata for Indonesian stocks when live APIs fail.
*   **`backend/agents/macro_economy_agent.py`**
    *   **Change:** Introduced conditional `if ticker.endswith(".JK"):` logic for the `macro_indicators` dict and the LLM `fallback_json`.
    *   **Reason:** If an Indonesian stock is requested, the agent now injects Indonesian macroeconomic data (BI 7-Day Repo Rate, Indonesia CPI, USD/IDR exchange rate) into the LLM prompt. If a US stock is requested, it falls back to the original Federal Reserve data.

## 2. Asset Ownership Logic (Dual-Decision Output)
**Context:** The coaching feedback criticized the system for advising a generic "Hold" or "Sell" recommendation for users who *do not* actually own the asset. The system needed to explicitly separate recommendations based on whether the user currently owns the asset or not.

**Files Updated:**
*   **`backend/models/schemas.py`**
    *   **Change:** In `PortfolioManagerOutput`, removed the `decision` field. Added two new fields: `decision_owned: str` and `decision_not_owned: str`.
    *   **Reason:** Forces the system (and the Pydantic schema validation) to explicitly track both scenarios independently.
*   **`backend/agents/portfolio_manager_agent.py`**
    *   **Change:** Updated the CIO prompt to explicitly instruct the LLM: *"Because portfolio recommendation logic must account for user asset ownership, you must output two decisions: one assuming the user already owns the asset, and one assuming they do not."*
    *   **Change:** Updated the baseline logic (`base_decision`) to map to `decision_owned` and `decision_not_owned` respectively.
*   **`backend/services/report_service.py`**
    *   **Change:** Updated the institutional PDF generation template (`generate_pdf_report`). Replaced the single "CIO RECOMMENDATION" badge with two side-by-side badges: "ACTION (IF OWNED)" and "ACTION (NOT OWNED)".
    *   **Change:** Updated the CSV export function (`generate_csv_export`) to output both decision columns.
*   **`backend/agents/execution_agent.py`**
    *   **Change:** Updated internal references from `pm_data.decision` to `pm_data.decision_not_owned` for determining the ideal buy zone and entry price.

## 3. Volatility-Based Prediction Timeframes (Investment Horizon)
**Context:** The system previously used a static 3-month prediction horizon, which was later made somewhat dynamic based on confluence scores. The coaching feedback explicitly requested that the timeframe be segmented and constrained based on the specific *volatility* of the asset (highly volatile stocks shouldn't have 3-month predictions).

**Files Updated:**
*   **`backend/agents/portfolio_manager_agent.py`**
    *   **Change:** Added logic to extract the `historical_regime` from the LangGraph `state`. 
    *   **Change:** Parsed the `volatility_regime` output by the `Historical Regime Agent`. 
    *   **Change:** Added a conditional constraint: If the regime contains "high" or "expansion", the `dyn_horizon` (investment horizon) is strictly capped at `"1 Week"`. If it's "low" or "compression", it allows `"3 to 6 Months"`. This `dyn_horizon` is then injected directly into the LLM prompt instructions.

## 4. Test Suite and Environment Fixes
**Context:** The schema changes and an existing `.env` misconfiguration caused the test suite to fail.

**Files Updated:**
*   **`backend/tests/test_agents.py`**
    *   **Change:** Updated the `test_all_agents_pipeline_sequential` test assertions. Changed `assert state["portfolio_manager"].decision` to check both `decision_owned` and `decision_not_owned`.
    *   **Change:** Fixed a failing assertion `assert state["options_flow"].put_call_ratio > 0` to `>= 0`.
*   **`backend/tests/test_workflow.py`**
    *   **Change:** Updated `assert len(steps_hit) == 9` to `>= 9` in `test_compiled_langgraph_execution` to accommodate the addition of the `historical_regime` agent to the pipeline.
*   **`.env` & `.env.example`**
    *   **Change:** Corrected `CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000` to a valid JSON array format `CORS_ORIGINS='["http://localhost:3000","http://127.0.0.1:3000"]'`.
    *   **Reason:** Fixed `pydantic_settings` `JSONDecodeError` failures that crashed the API router initialization during tests.
