"""
SHF Multi-Agent Quantitative Engine - Agent Level Evaluation (Level 1)
======================================================================
Tests each individual agent's output quality in isolation using the
G-Eval metric framework (LLM-as-Judge), this evaluates:

1. Input/Output Correctness: Verify that the agent’s output is factually 
    correct and aligns with the expected output.
2. Input/Output Relevance: Verify that the output is relevant to the input
    query.
3. Coherence: Verify the logical consistency and structure of the output.
4. Completeness: Verify that the output covers all essential fields and
    information.
5. Financial Reasoning Quality: Verify the depth and quality of financial
    reasoning in the output.
6. Bearish Override Logic: Verify that the agent correctly enforces bearish
    override logic when technical indicators are strongly bearish.
7. Dual-Decision Logic: Verify that the agent correctly enforces dual-
    decision logic for both owned and not-owned positions.

Usage:
    cd backend
    python -m evals.test_agents_eval
"""

import os
import sys
import json
from datetime import datetime

# Ensure the backend root is on sys.path so relative imports resolve
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deepeval import evaluate
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval

from evals.groq_llm import GroqEvalLLM
from evals.report_generator import generate_all_reports
from evals.mock_data import (
    MARKET_DATA_INPUT, MARKET_DATA_OUTPUT,
    NEWS_INTELLIGENCE_INPUT, NEWS_INTELLIGENCE_OUTPUT, NEWS_INTELLIGENCE_EXPECTED,
    MACRO_ECONOMY_INPUT, MACRO_ECONOMY_OUTPUT, MACRO_ECONOMY_EXPECTED,
    PORTFOLIO_MANAGER_INPUT, PORTFOLIO_MANAGER_OUTPUT, PORTFOLIO_MANAGER_EXPECTED,
    EXECUTION_AGENT_INPUT, EXECUTION_AGENT_OUTPUT, EXECUTION_AGENT_EXPECTED,
    RISK_MANAGER_INPUT, RISK_MANAGER_OUTPUT, RISK_MANAGER_EXPECTED,
    BEARISH_OVERRIDE_INPUT, BEARISH_OVERRIDE_OUTPUT, BEARISH_OVERRIDE_EXPECTED,
)

# ═══════════════════════════════════════════════════════════════════════════════
# Initialize the Groq-backed LLM Judge
# ═══════════════════════════════════════════════════════════════════════════════
groq_model = GroqEvalLLM(model_name="openai/gpt-oss-120b")


# ═══════════════════════════════════════════════════════════════════════════════
# Define G-Eval Metrics (LLM-as-Judge with Chain-of-Thought)
# ═══════════════════════════════════════════════════════════════════════════════

correctness_metric = GEval(
    name="Correctness",
    criteria=(
        "Determine whether the actual output is factually correct and aligns "
        "with the expected output. Check that numerical values, decisions, "
        "and financial reasoning are accurate and consistent."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model=groq_model,
    threshold=0.6,
)

relevance_metric = GEval(
    name="Relevance",
    criteria=(
        "Assess whether the actual output is relevant to the input query. "
        "The output should directly address the financial analysis request, "
        "mention the correct ticker symbol, and provide information "
        "pertinent to the specific analysis domain (technical, macro, news, etc.)."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)

coherence_metric = GEval(
    name="Coherence",
    criteria=(
        "Evaluate whether the actual output is logically coherent, well-structured, "
        "and internally consistent. Financial recommendations should not contradict "
        "the supporting data. For example, a bullish recommendation must be supported "
        "by predominantly bullish evidence, and bearish overrides must fire when "
        "technical indicators are strongly negative."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)

completeness_metric = GEval(
    name="Completeness",
    criteria=(
        "Assess whether the output covers all essential fields and information "
        "expected from a professional institutional-grade financial analysis agent. "
        "Missing critical data points (e.g., no confidence level, no stop-loss, "
        "no risk category) should lower the score significantly."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.6,
)

financial_reasoning_metric = GEval(
    name="Financial Reasoning Quality",
    criteria=(
        "Evaluate the depth and quality of financial reasoning in the output. "
        "Assess whether the agent demonstrates institutional-grade analytical rigor: "
        "quantitative evidence, risk-adjusted metrics (Sharpe, VaR, drawdown), "
        "multi-factor synthesis, and actionable trade parameters. "
        "Penalize vague or generic statements that lack numerical backing."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.6,
)

bearish_override_metric = GEval(
    name="Bearish Override Logic",
    criteria=(
        "CRITICAL: When technical analysis indicators are strongly bearish "
        "(bullish score <= 35, RSI < 30, death cross detected), the system MUST NOT "
        "recommend 'Hold' or 'Buy'. Verify that the output correctly enforces "
        "a 'Strong Sell' for owners and 'Wait / Do Not Buy' for non-owners. "
        "Any recommendation of Hold or Buy under these conditions is a FAILURE "
        "and must receive a score of 0."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)

dual_decision_metric = GEval(
    name="Dual-Decision Logic",
    criteria=(
        "Verify that the Portfolio Manager output contains TWO distinct decisions: "
        "one for users who already own the asset (decision_owned) and one for "
        "users who do not (decision_not_owned). The decisions must be logically "
        "appropriate: 'Hold'/'Reduce'/'Sell' for owned, 'Buy'/'Wait' for not owned. "
        "A single generic recommendation without ownership distinction is a FAILURE."
    ),
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
    ],
    model=groq_model,
    threshold=0.7,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Build Test Cases
# ═══════════════════════════════════════════════════════════════════════════════

test_cases = [
    # --- Market Data Agent ---
    LLMTestCase(
        input=MARKET_DATA_INPUT,
        actual_output=MARKET_DATA_OUTPUT,
    ),

    # --- News Intelligence Agent ---
    LLMTestCase(
        input=NEWS_INTELLIGENCE_INPUT,
        actual_output=NEWS_INTELLIGENCE_OUTPUT,
        expected_output=NEWS_INTELLIGENCE_EXPECTED,
    ),

    # --- Macro Economy Agent ---
    LLMTestCase(
        input=MACRO_ECONOMY_INPUT,
        actual_output=MACRO_ECONOMY_OUTPUT,
        expected_output=MACRO_ECONOMY_EXPECTED,
    ),

    # --- Portfolio Manager Agent (Bullish Scenario) ---
    LLMTestCase(
        input=PORTFOLIO_MANAGER_INPUT,
        actual_output=PORTFOLIO_MANAGER_OUTPUT,
        expected_output=PORTFOLIO_MANAGER_EXPECTED,
    ),

    # --- Execution Agent ---
    LLMTestCase(
        input=EXECUTION_AGENT_INPUT,
        actual_output=EXECUTION_AGENT_OUTPUT,
        expected_output=EXECUTION_AGENT_EXPECTED,
    ),

    # --- Risk Manager Agent ---
    LLMTestCase(
        input=RISK_MANAGER_INPUT,
        actual_output=RISK_MANAGER_OUTPUT,
        expected_output=RISK_MANAGER_EXPECTED,
    ),

    # --- Bearish Override Scenario (Critical Logic Test) ---
    LLMTestCase(
        input=BEARISH_OVERRIDE_INPUT,
        actual_output=BEARISH_OVERRIDE_OUTPUT,
        expected_output=BEARISH_OVERRIDE_EXPECTED,
    ),
]

# Map test cases to descriptive agent names
test_case_names = [
    "Market Data Agent",
    "News Intelligence Agent",
    "Macro Economy Agent",
    "Portfolio Manager Agent (Bullish)",
    "Execution Agent",
    "Risk Manager Agent",
    "Portfolio Manager Agent (Bearish Override)",
]

# Map each test case to the metrics it should be evaluated against
test_case_metrics = [
    # Market Data: relevance, coherence, completeness
    [relevance_metric, coherence_metric, completeness_metric],
    # News Intelligence: correctness, relevance, coherence, completeness, reasoning
    [correctness_metric, relevance_metric, coherence_metric, completeness_metric, financial_reasoning_metric],
    # Macro Economy: correctness, relevance, coherence, reasoning
    [correctness_metric, relevance_metric, coherence_metric, financial_reasoning_metric],
    # Portfolio Manager (Bullish): correctness, relevance, coherence, completeness, reasoning, dual-decision
    [correctness_metric, relevance_metric, coherence_metric, completeness_metric, financial_reasoning_metric, dual_decision_metric],
    # Execution Agent: correctness, relevance, coherence, completeness
    [correctness_metric, relevance_metric, coherence_metric, completeness_metric],
    # Risk Manager: correctness, relevance, coherence, completeness, reasoning
    [correctness_metric, relevance_metric, coherence_metric, completeness_metric, financial_reasoning_metric],
    # Bearish Override: correctness, coherence, bearish override, dual-decision
    [correctness_metric, coherence_metric, bearish_override_metric, dual_decision_metric],
]


# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("\n" + "=" * 70)
    print("  SHF AGENT LEVEL EVALUATION (Level 1)")
    print("  Tests: Correctness | Relevance | Coherence | Completeness | Reasoning")
    print("=" * 70 + "\n")

    results_data = []

    for i, (test_case, agent_name, metrics) in enumerate(
        zip(test_cases, test_case_names, test_case_metrics)
    ):
        print(f"\n[{i+1}/{len(test_cases)}] Evaluating: {agent_name}")
        print("-" * 50)

        agent_results = {"agent": agent_name, "metrics": []}

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

            agent_results["metrics"].append({
                "metric": metric.name,
                "score": score,
                "passed": passed,
                "reason": reason or "",
                "threshold": metric.threshold,
            })

        results_data.append(agent_results)

    # Generate reports
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    md_path, json_path, html_path = generate_all_reports(results_data, output_dir)
    
    print(f"\n{'='*70}")
    print(f"  EVALUATION REPORTS GENERATED")
    print(f"{'='*70}")
    print(f"  Markdown: {md_path}")
    print(f"  JSON:     {json_path}")
    print(f"  HTML:     {html_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
