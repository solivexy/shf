"""
SHF Evaluation Suite - Report Utilities
========================================
Shared constants, helper functions, and AI recommendation logic
used across all report generators.
"""

import re
from evals.groq_llm import GroqEvalLLM

TARGET_OVERALL_SCORE = 85.0  # Percentage

LEVEL_MAP = {
    "L1-Agent": "Level 1: Agent",
    "L2-Interaction": "Level 2: Interaction",
    "L3-E2E": "Level 3: E2E & Operation",
    "L3-Operation": "Level 3: E2E & Operation",
}

LEVEL_COLORS = {
    "L1-Agent": "#3b82f6",       # Blue
    "L2-Interaction": "#8b5cf6", # Purple
    "L3-E2E": "#f59e0b",         # Amber
}


def detect_level(agent_name: str) -> str:
    """Extract the level prefix from agent name like '[L1-Agent] Market Data Agent'."""
    match = re.match(r"\[(L\d+-\w+)\]", agent_name)
    return match.group(1) if match else "Unknown"


def strip_level_prefix(agent_name: str) -> str:
    """Remove the level prefix for cleaner display."""
    return re.sub(r"^\[L\d+-\w+\]\s*", "", agent_name)


def split_by_level(results_data: list) -> dict:
    """Split combined results into per-level buckets (merging L3s)."""
    levels = {}
    for entry in results_data:
        raw_level = detect_level(entry["agent"])
        level = "L3-E2E" if raw_level == "L3-Operation" else raw_level
        if level not in levels:
            levels[level] = []
        levels[level].append(entry)
    return levels


def get_summary_stats(results_data: list) -> dict:
    """Compute pass/fail statistics for a list of results."""
    total_pass = sum(1 for e in results_data for m in e["metrics"] if m["passed"])
    total_tests = sum(1 for e in results_data for m in e["metrics"])
    pass_rate = (total_pass / total_tests * 100) if total_tests > 0 else 0
    return {
        "total_pass": total_pass,
        "total_tests": total_tests,
        "total_fail": total_tests - total_pass,
        "pass_rate": pass_rate,
        "target_score": TARGET_OVERALL_SCORE
    }


def get_real_fix_recommendation(agent: str, metric_name: str, score: float, reason: str, llm: GroqEvalLLM) -> str:
    """Uses Groq LLM to generate a targeted fix recommendation based on the evaluation failure."""
    if not reason or reason.strip() == "":
        return "No specific reason provided for failure. Review the agent's prompt instructions and output schema."

    prompt = (
        f"You are a helpful AI development assistant working on a quantitative hedge fund multi-agent system.\n"
        f"An agent named '{agent}' failed the '{metric_name}' evaluation metric with a score of {score}.\n"
        f"The evaluation judge provided this reason for the failure:\n"
        f"\"{reason}\"\n\n"
        f"Based on this reason, provide a concise, actionable, and specific 1-3 sentence recommendation "
        f"on how the developer should fix the agent's prompt or logic. Do not output anything else besides the recommendation."
    )

    try:
        recommendation = llm.generate(prompt)
        recommendation = recommendation.strip().replace("\n", " ").replace("\"", "")
        return recommendation
    except Exception as e:
        return f"Failed to generate LLM recommendation. Manual review required. (Error: {e})"


def enrich_with_fix_recommendations(results_data: list, llm: GroqEvalLLM):
    """Add AI fix recommendations to all failed metrics in-place."""
    for entry in results_data:
        for metric in entry["metrics"]:
            if metric["passed"]:
                metric["fix_recommendation"] = "N/A (Passed)"
            else:
                agent_display = strip_level_prefix(entry["agent"])
                print(f"    -> Generating fix for {agent_display} | {metric['metric']}...")
                metric["fix_recommendation"] = get_real_fix_recommendation(
                    agent_display,
                    metric["metric"],
                    metric["score"],
                    metric.get("reason", ""),
                    llm
                )


def safe_html(text: str) -> str:
    """Escape HTML special chars."""
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
