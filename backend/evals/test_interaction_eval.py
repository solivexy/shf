"""
SHF Multi-Agent Quantitative Engine - Interaction Level Evaluation (Level 2)
=============================================================================
Tests the communication and state-handoff quality between sequential agents.
Since the pipeline is strictly sequential (not fan-out), this evaluates:

1. State Handoff Integrity: Does Agent N correctly pass its output fields
   to Agent N+1 via the shared HedgeFundState?
2. Downstream Dependency Validation: Does a downstream agent degrade
   gracefully when an upstream agent's output is missing or malformed?
3. Cumulative Context Coherence: Does the final agent's output remain
   logically consistent with the first agent's raw data after 10 handoffs?

Usage:
    cd backend
    python -m evals.test_interaction_eval
"""

import os
import sys
import json
import copy
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval

from evals.groq_llm import GroqEvalLLM
from evals.report_generator import generate_all_reports
from evals.mock_data import (
    FULL_STATE_SNAPSHOT,
    PIPELINE_SEQUENCE,
    DEGRADATION_PM_MISSING_NEWS_INPUT, DEGRADATION_PM_MISSING_NEWS_OUTPUT,
    DEGRADATION_EXEC_MISSING_RISK_INPUT, DEGRADATION_EXEC_MISSING_RISK_OUTPUT,
    DEGRADATION_PM_ALL_NULL_INPUT, DEGRADATION_PM_ALL_NULL_OUTPUT,
)

# ═══════════════════════════════════════════════════════════════════════════════
# Initialize the Groq-backed LLM Judge
# ═══════════════════════════════════════════════════════════════════════════════
groq_model = GroqEvalLLM(model_name="openai/gpt-oss-120b")


# ═══════════════════════════════════════════════════════════════════════════════
# G-Eval Metrics for Interaction Testing
# ═══════════════════════════════════════════════════════════════════════════════

handoff_integrity_metric = GEval(
    name="Handoff Integrity",
    criteria=(
        "Evaluate whether the downstream agent's output correctly references and uses "
        "data from its upstream dependencies. For example, if the upstream Market Data Agent "
        "reports AAPL at $228.40, the downstream Execution Agent's entry price should be "
        "logically derived from that number. Check that ticker symbols, price references, "
        "and analytical conclusions flow consistently through the pipeline without data loss "
        "or contradiction."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)

graceful_degradation_metric = GEval(
    name="Graceful Degradation",
    criteria=(
        "Evaluate how a downstream agent handles missing or null upstream data. "
        "The agent should NOT crash, produce nonsensical output, or silently ignore "
        "the missing data. Instead, it should either use reasonable defaults, flag "
        "the missing input explicitly, or reduce its confidence level. "
        "A score of 1.0 means the agent handled the gap perfectly. "
        "A score of 0.0 means the agent produced contradictory or broken output."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.6,
)

cumulative_coherence_metric = GEval(
    name="Cumulative Context Coherence",
    criteria=(
        "This test compares the FIRST agent's raw data (Market Data) with the LAST "
        "agent's final output (Execution Plan) to verify that the entire 10-agent "
        "sequential pipeline maintained logical coherence. The final execution plan's "
        "entry price, stop loss, and order type should be traceable back to the original "
        "market data price. No hallucinated numbers or contradictory recommendations "
        "should exist. A bullish pipeline should not produce a 'Sell' execution plan."
    ),
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
        SingleTurnParams.EXPECTED_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Build Interaction Test Cases
# ═══════════════════════════════════════════════════════════════════════════════

def build_handoff_test_cases():
    """
    For each agent in the pipeline that has upstream dependencies,
    create a test case that verifies the handoff from upstream -> downstream.
    """
    test_cases = []
    test_names = []
    test_metrics_map = []

    for agent_name, state_key, upstream_keys in PIPELINE_SEQUENCE:
        if not upstream_keys:
            continue

        upstream_data = {}
        for key in upstream_keys:
            upstream_data[key] = FULL_STATE_SNAPSHOT.get(key, {})

        actual_output = FULL_STATE_SNAPSHOT.get(state_key, {})

        expected = (
            f"The {agent_name} should produce output that is logically derived from "
            f"its upstream inputs: {', '.join(upstream_keys)}. All ticker references "
            f"should match 'AAPL', and any price-derived calculations should trace back "
            f"to the upstream market data price of $228.40."
        )

        tc = LLMTestCase(
            input=f"Upstream state for {agent_name}:\n{json.dumps(upstream_data, indent=2)}",
            actual_output=json.dumps(actual_output, indent=2),
            expected_output=expected,
        )
        test_cases.append(tc)
        test_names.append(f"Handoff: {upstream_keys[0]} -> {agent_name}")
        test_metrics_map.append([handoff_integrity_metric])

    return test_cases, test_names, test_metrics_map


def build_degradation_test_cases():
    """
    Simulate missing upstream data for critical agents and verify
    that the downstream agent's output degrades gracefully.
    """
    test_cases = []
    test_names = []
    test_metrics_map = []

    # Scenario 1: PM with missing news_intelligence
    test_cases.append(LLMTestCase(
        input=DEGRADATION_PM_MISSING_NEWS_INPUT,
        actual_output=DEGRADATION_PM_MISSING_NEWS_OUTPUT
    ))
    test_names.append("Degradation: PM with missing News Intelligence")
    test_metrics_map.append([graceful_degradation_metric])

    # Scenario 2: Execution with missing risk_manager
    test_cases.append(LLMTestCase(
        input=DEGRADATION_EXEC_MISSING_RISK_INPUT,
        actual_output=DEGRADATION_EXEC_MISSING_RISK_OUTPUT
    ))
    test_names.append("Degradation: Execution with missing Risk Manager")
    test_metrics_map.append([graceful_degradation_metric])

    # Scenario 3: PM with ALL upstream agents failed
    test_cases.append(LLMTestCase(
        input=DEGRADATION_PM_ALL_NULL_INPUT,
        actual_output=DEGRADATION_PM_ALL_NULL_OUTPUT
    ))
    test_names.append("Degradation: PM with ALL upstream agents failed")
    test_metrics_map.append([graceful_degradation_metric])

    return test_cases, test_names, test_metrics_map


def build_cumulative_coherence_test_case():
    """
    Compares the first agent's data to the last agent's output
    to verify end-to-end logical consistency across the full pipeline.
    """
    first_agent_data = json.dumps(FULL_STATE_SNAPSHOT["market_data"], indent=2)
    last_agent_data = json.dumps(FULL_STATE_SNAPSHOT["execution_plan"], indent=2)

    tc = LLMTestCase(
        input=(
            f"First Agent (Market Data Agent) raw output:\n{first_agent_data}\n\n"
            f"This data was passed through 10 sequential agents in the pipeline:\n"
            f"Market Data -> Historical Regime -> Technical Analysis -> News Intelligence -> "
            f"Macro Economy -> Options Flow -> Risk Manager -> ML Prediction -> "
            f"Portfolio Manager -> Execution Agent"
        ),
        actual_output=(
            f"Final Agent (Execution Agent) output after 10 handoffs:\n{last_agent_data}"
        ),
        expected_output=(
            "The Execution Agent's entry price ($227.49) should be logically derived from "
            "the Market Data Agent's current price ($228.40). The stop loss ($218.28) should "
            "come from the Risk Manager's analysis. The order type should align with a bullish "
            "recommendation. No numbers should be hallucinated or contradictory to the source data."
        ),
    )
    return [tc], ["Cumulative Coherence: Market Data -> Execution (10 handoffs)"], [[cumulative_coherence_metric]]


# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "=" * 70)
    print("  SHF INTERACTION LEVEL EVALUATION (Level 2)")
    print("  Tests: Handoff Integrity | Graceful Degradation | Cumulative Coherence")
    print("=" * 70 + "\n")

    all_test_cases = []
    all_test_names = []
    all_test_metrics = []

    tc1, tn1, tm1 = build_handoff_test_cases()
    tc2, tn2, tm2 = build_degradation_test_cases()
    tc3, tn3, tm3 = build_cumulative_coherence_test_case()

    all_test_cases.extend(tc1 + tc2 + tc3)
    all_test_names.extend(tn1 + tn2 + tn3)
    all_test_metrics.extend(tm1 + tm2 + tm3)

    results_data = []

    for i, (test_case, test_name, metrics) in enumerate(
        zip(all_test_cases, all_test_names, all_test_metrics)
    ):
        print(f"\n[{i+1}/{len(all_test_cases)}] Evaluating: {test_name}")
        print("-" * 50)

        test_result = {"agent": test_name, "metrics": []}

        for metric in metrics:
            try:
                metric.measure(test_case)
                score = metric.score
                passed = metric.is_successful()
                reason = getattr(metric, "reason", "")
            except Exception as e:
                score = 0.0
                passed = False
                reason = f"Evaluation error: {str(e)}"

            status = "PASS" if passed else "FAIL"
            score_display = f"{score:.2f}" if score is not None else "N/A"
            print(f"  {metric.name}: {score_display} [{status}]")
            if reason:
                safe_reason = reason[:120].encode('ascii', 'ignore').decode('ascii')
                print(f"    -> {safe_reason}")

            test_result["metrics"].append({
                "metric": metric.name,
                "score": score,
                "passed": passed,
                "reason": reason or "",
                "threshold": metric.threshold,
            })

        results_data.append(test_result)

    output_dir = os.path.join(os.path.dirname(__file__), "results")
    md_path, json_path, html_path = generate_all_reports(results_data, output_dir)

    print(f"\n{'='*70}")
    print(f"  INTERACTION LEVEL REPORTS GENERATED")
    print(f"{'='*70}")
    print(f"  Markdown: {md_path}")
    print(f"  JSON:     {json_path}")
    print(f"  HTML:     {html_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
