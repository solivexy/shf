"""
SHF Multi-Agent Quantitative Engine - Full Evaluation Suite Runner
===================================================================
Runs all evaluation levels in sequence and produces a unified combined report.

Levels:
    Level 1: Agent Level Evaluation (individual agent output quality)
    Level 2: Interaction Level Evaluation (handoff, degradation, coherence)
    Level 3: End-to-End & Operation Level (stability, schema, latency, resilience)

Usage:
    cd backend
    python -m evals.run_all_evals
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from deepeval.metrics import GEval

from evals.groq_llm import GroqEvalLLM
from evals.report_generator import generate_all_reports

# Import test case builders from each level
from evals.test_agents_eval import (
    test_cases as agent_test_cases,
    test_case_names as agent_test_names,
    test_case_metrics as agent_test_metrics,
)
from evals.test_interaction_eval import (
    build_handoff_test_cases,
    build_degradation_test_cases,
    build_cumulative_coherence_test_case,
)
from evals.test_e2e_eval import (
    build_stability_test,
    build_schema_compliance_test,
    build_latency_test,
    build_error_resilience_test,
)


def run_llm_tests(test_cases, test_names, test_metrics_map, level_label):
    """Run a batch of LLM-judged tests and return results_data list."""
    results = []
    total = len(test_cases)

    for i, (tc, name, metrics) in enumerate(zip(test_cases, test_names, test_metrics_map)):
        print(f"\n  [{i+1}/{total}] {name}")
        print("  " + "-" * 50)

        entry = {"agent": f"[{level_label}] {name}", "metrics": []}

        for metric in metrics:
            try:
                metric.measure(tc)
                score = metric.score
                passed = metric.is_successful()
                reason = getattr(metric, "reason", "")
            except Exception as e:
                score = 0.0
                passed = False
                reason = f"Evaluation error: {str(e)}"

            status = "PASS" if passed else "FAIL"
            score_display = f"{score:.2f}" if score is not None else "N/A"
            print(f"    {metric.name}: {score_display} [{status}]")
            if reason:
                safe = reason[:120].encode('ascii', 'ignore').decode('ascii')
                print(f"      -> {safe}")

            entry["metrics"].append({
                "metric": metric.name,
                "score": score,
                "passed": passed,
                "reason": reason or "",
                "threshold": metric.threshold,
            })

        results.append(entry)

    return results


def main():
    print("\n" + "=" * 70)
    print("  SHF FULL EVALUATION SUITE (All Levels)")
    print("  Level 1: Agent | Level 2: Interaction | Level 3: E2E & Operation")
    print("=" * 70)

    all_results = []

    # ── Level 1: Agent Level ──
    print(f"\n{'='*70}")
    print("  LEVEL 1: AGENT LEVEL EVALUATION")
    print(f"{'='*70}")
    level1 = run_llm_tests(agent_test_cases, agent_test_names, agent_test_metrics, "L1-Agent")
    all_results.extend(level1)

    # ── Level 2: Interaction Level ──
    print(f"\n{'='*70}")
    print("  LEVEL 2: INTERACTION LEVEL EVALUATION")
    print(f"{'='*70}")
    tc_h, tn_h, tm_h = build_handoff_test_cases()
    tc_d, tn_d, tm_d = build_degradation_test_cases()
    tc_c, tn_c, tm_c = build_cumulative_coherence_test_case()

    l2_cases = tc_h + tc_d + tc_c
    l2_names = tn_h + tn_d + tn_c
    l2_metrics = tm_h + tm_d + tm_c

    level2 = run_llm_tests(l2_cases, l2_names, l2_metrics, "L2-Interaction")
    all_results.extend(level2)

    # ── Level 3: E2E & Operation Level ──
    print(f"\n{'='*70}")
    print("  LEVEL 3: END-TO-END & OPERATION LEVEL EVALUATION")
    print(f"{'='*70}")
    tc_s, tn_s, tm_s = build_stability_test()
    tc_sc, tn_sc, tm_sc = build_schema_compliance_test()
    tc_e, tn_e, tm_e = build_error_resilience_test()

    l3_cases = tc_s + tc_sc + tc_e
    l3_names = tn_s + tn_sc + tn_e
    l3_metrics = tm_s + tm_sc + tm_e

    level3 = run_llm_tests(l3_cases, l3_names, l3_metrics, "L3-E2E")
    all_results.extend(level3)

    # Latency test (deterministic, no LLM)
    print(f"\n  [Deterministic] Operation: Latency Budget")
    print("  " + "-" * 50)
    latency = build_latency_test()
    lat_status = "PASS" if latency["passed"] else "FAIL"
    print(f"    Latency Budget: avg={latency['avg_latency_seconds']}s, "
          f"max={latency['max_latency_seconds']}s [{lat_status}]")

    all_results.append({
        "agent": "[L3-Operation] Latency Budget",
        "metrics": [{
            "metric": "Latency Budget",
            "score": 1.0 if latency["passed"] else 0.0,
            "passed": latency["passed"],
            "reason": latency["reason"],
            "threshold": 0.5,
        }]
    })

    # ── Generate Combined Report ──
    output_dir = os.path.join(os.path.dirname(__file__), "results")
    md_path, json_path, html_path = generate_all_reports(all_results, output_dir)

    print(f"\n{'='*70}")
    print(f"  FULL EVALUATION SUITE REPORTS GENERATED")
    print(f"{'='*70}")
    print(f"  Markdown: {md_path}")
    print(f"  JSON:     {json_path}")
    print(f"  HTML:     {html_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
