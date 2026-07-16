# Context: Week 2 Coaching Feedback Updates

**Date**: July 16, 2026
**Purpose**: This document provides a detailed summary of the architectural and logical changes applied to the codebase to address the "Week 2 Coaching" feedback. This file is intended to serve as context for any AI agents or developers working on the codebase in the future, ensuring they understand *what* was changed and *why*.

---

## 1. Decision Making Logic Validation (Bearish Override)
**Context:** The lecturer noted an anomaly where the system could recommend a "Hold" despite technical indicators showing a strong bearish trend. While mathematically possible in our weighted score model (due to other bullish factors like news), it lacked strict financial logic boundaries.

**Files Updated:**
*   **`backend/agents/portfolio_manager_agent.py`**
    *   **Change:** Introduced a strict `apply_bearish_override` logical guard inside the CIO evaluation logic. If the `technical_analysis` score drops significantly low (<= 35.0), the system forcibly caps the overall `weighted_score` and enforces a "Sell" or "Strong Sell" baseline decision.
    *   **Reason:** Ensures the quantitative logic respects critical market downtrends, preventing the system from producing conflicting recommendations that appear random or unjustified.

## 2. Terminal Onboarding Empty State
**Context:** The application previously lacked an onboarding process, immediately running a hardcoded scan for "AAPL" upon loading the dashboard. This was deemed confusing for new users.

**Files Updated:**
*   **`frontend/app/terminal/page.tsx`**
    *   **Change:** Removed the automatic `startAnalysis("AAPL")` hook on mount. Replaced the empty `state` view with a clean "Welcome/Onboarding" UI that features a brief guide and a quick-start grid of popular stocks (e.g., AAPL, NVDA, BBRI.JK).
    *   **Reason:** Improves UI/UX by giving new users context on what the platform does and how to interact with it, satisfying the lecturer's onboarding requirements.

## 3. Agent Timeline Layout Constraints
**Context:** The Agent Timeline (Right Sidebar) was wasting vertical space, and expanding highly verbose agent logs (such as the Historical Regime Agent) caused the entire layout to break its grid constraint and stretch infinitely downwards.

**Files Updated:**
*   **`frontend/app/terminal/page.tsx`**
    *   **Change:** Refactored the CSS Grid layout. Wrapped the `<AgentTimeline />` in an `absolute inset-0` container.
    *   **Reason:** Detaches the timeline's internal height from the CSS Grid row calculation, perfectly locking the sidebar's height to match the adjacent Workstation column (CIO Card + Charts).
*   **`frontend/components/AgentTimeline.tsx`**
    *   **Change:** Removed `max-h-[500px]` constraints and implemented `flex-1 overflow-y-auto` for native internal scrolling. Additionally, updated the JSON payload syntax highlighter to a high-contrast dark theme (`#38bdf8` on `#0f111a`).
    *   **Reason:** Prevents the expanded logs from breaking the UI layout and drastically improves text readability in dark mode.

## 4. Research Dossier Management (Delete & Seamless Navigation)
**Context:** Users needed a way to manage database clutter by deleting old dossiers. Additionally, there was a need to easily revisit past analyses in the Terminal without triggering an expensive and redundant LLM pipeline re-run.

**Files Updated:**
*   **`backend/database/mongodb.py`** & **`backend/services/analysis_service.py`**
    *   **Change:** Implemented robust individual (`delete_analysis_run`) and bulk (`delete_all_analysis_runs`) erasure capabilities that work against both the live MongoDB collections and the offline in-memory fallback state.
*   **`backend/api/routers/reports.py`**
    *   **Change:** Exposed `DELETE /api/v1/reports/{task_id}` and `DELETE /api/v1/reports` endpoints.
*   **`frontend/app/reports/page.tsx`**
    *   **Change:** Added a destructive "DELETE ALL" button (protected by a confirmation modal) and individual single-click "DELETE" buttons. Rewired the "CHART SCAN" link to `href={\`/terminal?taskId=\${task_id}\`}`.
*   **`frontend/app/terminal/page.tsx`**
    *   **Change:** Added URL query parameter parsing (`window.location.search`) on component mount to intercept the `taskId` and instantly trigger `loadAnalysis(taskId)`.
    *   **Reason:** Allows users to effortlessly manage their database state and seamlessly beam past historical states directly back into the live interactive Terminal UI.
