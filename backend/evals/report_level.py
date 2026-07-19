"""
SHF Evaluation Suite - Per-Level Report Generator
===================================================
Generates detailed HTML, Markdown, and JSON reports for a single
evaluation level (Agent, Interaction, or E2E/Operation).

These reports are stored in sub-folders and linked from the main report.
"""

import os
import json
from datetime import datetime

from evals.report_utils import (
    TARGET_OVERALL_SCORE, LEVEL_MAP,
    strip_level_prefix, get_summary_stats, safe_html,
)


# ═══════════════════════════════════════════════════════════════════════════════
# JSON
# ═══════════════════════════════════════════════════════════════════════════════

def generate_level_json(results_data: list, output_path: str, summary_stats: dict):
    report_payload = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "evaluation_model": "openai/gpt-oss-120b",
            "framework": "DeepEval (G-Eval)",
            "summary": summary_stats
        },
        "results": results_data
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2, ensure_ascii=False)
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# Markdown
# ═══════════════════════════════════════════════════════════════════════════════

def generate_level_markdown(results_data: list, output_path: str, summary_stats: dict, title: str):
    is_ready = summary_stats['pass_rate'] >= TARGET_OVERALL_SCORE
    ready_status = "DEPLOYMENT READY" if is_ready else "NEEDS IMPROVEMENT"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
        f.write(f"**Evaluation Model**: Groq `openai/gpt-oss-120b`\n")
        f.write(f"**Framework**: DeepEval (G-Eval with Chain-of-Thought)\n\n")

        f.write("## Executive Summary\n\n")
        f.write(f"- **Target Pass Rate**: {TARGET_OVERALL_SCORE}%\n")
        f.write(f"- **Actual Pass Rate**: {summary_stats['pass_rate']:.1f}% ({summary_stats['total_pass']}/{summary_stats['total_tests']} metrics)\n")
        f.write(f"- **Status**: **{ready_status}**\n\n")

        f.write("---\n\n")

        f.write("## Overview\n\n")
        f.write("| Agent | Metric | Score | Status |\n")
        f.write("|-------|--------|-------|--------|\n")

        for entry in results_data:
            display_name = strip_level_prefix(entry["agent"])
            for metric in entry["metrics"]:
                score_str = f"{metric['score']:.2f}" if metric['score'] is not None else "N/A"
                status = "PASS" if metric["passed"] else "FAIL"
                f.write(f"| {display_name} | {metric['metric']} | {score_str} | {status} |\n")

        f.write("\n---\n\n")

        f.write("## Detailed Results & AI Recommendations\n\n")
        for entry in results_data:
            display_name = strip_level_prefix(entry["agent"])
            f.write(f"### {display_name}\n\n")
            for metric in entry["metrics"]:
                score_str = f"{metric['score']:.2f}" if metric['score'] is not None else "N/A"
                status = "PASS" if metric["passed"] else "FAIL"
                f.write(f"#### {metric['metric']} - {score_str} ({status})\n")
                if metric.get("reason"):
                    f.write(f"- **Reason**: {metric['reason']}\n")
                if not metric["passed"] and metric.get("fix_recommendation"):
                    f.write(f"- **AI Fix Recommendation**: {metric['fix_recommendation']}\n")
            f.write("\n")

    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# HTML (Per-Level Detail Page)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_level_html(results_data: list, output_path: str, summary_stats: dict, title: str, main_link: str = None):
    is_ready = summary_stats['pass_rate'] >= TARGET_OVERALL_SCORE
    ready_status = "DEPLOYMENT READY" if is_ready else "NEEDS IMPROVEMENT"
    ready_color = "#10b981" if is_ready else "#ef4444"

    # Prepare chart data — use SCORE not pass rate so 0-score bars show up
    agent_labels = []
    agent_scores = []
    agent_colors = []

    for entry in results_data:
        display_name = strip_level_prefix(entry["agent"])
        for metric in entry["metrics"]:
            label = f"{display_name} | {metric['metric']}"
            # Truncate long labels for chart readability
            if len(label) > 50:
                label = label[:47] + "..."
            agent_labels.append(label)
            score = metric["score"] if metric["score"] is not None else 0
            agent_scores.append(round(score * 100, 1))  # normalize to percentage
            agent_colors.append("#10b981" if metric["passed"] else "#ef4444")

    back_btn = ""
    if main_link:
        back_btn = f'<a href="{main_link}" class="back-btn">&larr; Back to Main Dashboard</a>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        .back-btn {{ display: inline-block; color: #38bdf8; text-decoration: none; padding: 0.5rem 1rem; border: 1px solid #38bdf8; border-radius: 6px; margin-bottom: 1.5rem; transition: all 0.2s; }}
        .back-btn:hover {{ background: #38bdf8; color: #0f172a; }}
        .header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }}
        .header h1 {{ color: #38bdf8; margin: 0 0 0.5rem; font-size: 1.5rem; }}
        .header-meta {{ color: #94a3b8; font-size: 0.875rem; }}
        .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .stat-card {{ background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1.25rem; text-align: center; }}
        .stat-card .value {{ font-size: 2rem; font-weight: bold; color: #38bdf8; }}
        .stat-card .label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.25rem; }}
        .stat-card.status .value {{ color: {ready_color}; }}
        .chart-section {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }}
        .chart-section h2 {{ color: #cbd5e1; margin: 0 0 1rem; font-size: 1.1rem; }}
        .chart-container {{ position: relative; height: {max(300, len(agent_labels) * 28)}px; }}
        h2.section-title {{ color: #cbd5e1; border-bottom: 1px solid #334155; padding-bottom: 0.3rem; margin-top: 2rem; }}
        .metric-card {{ background: #1e293b; border: 1px solid #334155; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem; }}
        .metric-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }}
        .metric-title {{ font-weight: 600; font-size: 1rem; }}
        .pass {{ color: #10b981; }}
        .fail {{ color: #ef4444; }}
        .reason {{ background: #0f172a; padding: 1rem; border-left: 4px solid #3b82f6; border-radius: 6px; margin-top: 0.75rem; font-size: 0.9rem; }}
        .recommendation {{ background: #451a1a; padding: 1rem; border-left: 4px solid #f59e0b; border-radius: 6px; margin-top: 0.5rem; font-size: 0.9rem; color: #fde68a; }}
        .agent-block {{ margin-bottom: 2rem; }}
        .agent-block h3 {{ color: #94a3b8; margin-bottom: 0.75rem; font-size: 1.1rem; }}
    </style>
</head>
<body>
    <div class="container">
        {back_btn}
        <div class="header">
            <h1>{title}</h1>
            <div class="header-meta">
                DeepEval (G-Eval) &bull; Groq <code>openai/gpt-oss-120b</code> &bull; {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-card">
                <div class="value">{TARGET_OVERALL_SCORE}%</div>
                <div class="label">Target Score</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: {ready_color};">{summary_stats['pass_rate']:.1f}%</div>
                <div class="label">Actual Score</div>
            </div>
            <div class="stat-card">
                <div class="value">{summary_stats['total_pass']}/{summary_stats['total_tests']}</div>
                <div class="label">Passed Metrics</div>
            </div>
            <div class="stat-card status">
                <div class="value">{ready_status}</div>
                <div class="label">Deployment Status</div>
            </div>
        </div>

        <div class="chart-section">
            <h2>Metric Scores (per test case)</h2>
            <div class="chart-container">
                <canvas id="metricsChart"></canvas>
            </div>
        </div>

        <h2 class="section-title">Detailed Breakdown & AI Recommendations</h2>
"""

    for entry in results_data:
        display_name = strip_level_prefix(entry["agent"])
        html += f'<div class="agent-block"><h3>{safe_html(display_name)}</h3>\n'
        for metric in entry["metrics"]:
            status_class = "pass" if metric["passed"] else "fail"
            status_text = "PASS" if metric["passed"] else "FAIL"
            score_str = f"{metric['score']:.2f}" if metric['score'] is not None else "N/A"

            html += f"""<div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">{safe_html(metric['metric'])}</span>
                <span class="{status_class}"><strong>{status_text}</strong> (Score: {score_str})</span>
            </div>\n"""
            if metric.get("reason"):
                html += f'<div class="reason"><strong>Reason:</strong> {safe_html(metric["reason"])}</div>\n'
            if not metric["passed"] and metric.get("fix_recommendation"):
                html += f'<div class="recommendation"><strong>AI Fix Recommendation:</strong> {safe_html(metric["fix_recommendation"])}</div>\n'
            html += "</div>\n"
        html += "</div>\n"

    html += f"""
    </div>
    <script>
        const ctx = document.getElementById('metricsChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(agent_labels)},
                datasets: [{{
                    label: 'Score (%)',
                    data: {json.dumps(agent_scores)},
                    backgroundColor: {json.dumps(agent_colors)},
                    borderWidth: 0,
                    borderRadius: 4,
                    barThickness: 20
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ beginAtZero: true, max: 100, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ grid: {{ display: false }}, ticks: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                }},
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{ callbacks: {{ label: function(ctx) {{ return ctx.parsed.x + '%'; }} }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
