"""
SHF Evaluation Suite - Report Generator (Main Entrypoint)
==========================================================
Orchestrates report generation for the full evaluation suite.

- Main reports (root of eval folder) contain SUMMARY ONLY — pass rates per
  level, visualizations, and navigation links to detailed level reports.
- Per-level reports (sub-folders) contain the full breakdown with every
  metric, reason, and AI fix recommendation.

Output structure:
    results/
    └── evaluation_YYYYMMDD_HHMMSS/
        ├── main_visualization_YYYYMMDD_HHMMSS.html   (summary dashboard)
        ├── main_report_YYYYMMDD_HHMMSS.md            (summary markdown)
        ├── level1_agent_YYYYMMDD_HHMMSS/
        │   ├── summary_visualization_level1.html
        │   ├── breakdown_report_level1.md
        │   └── metrics_data_level1.json
        ├── level2_interaction_YYYYMMDD_HHMMSS/
        │   └── ...
        └── level3_e2e_operation_YYYYMMDD_HHMMSS/
            └── ...
"""

import os
import json
from datetime import datetime

from evals.groq_llm import GroqEvalLLM
from evals.report_utils import (
    TARGET_OVERALL_SCORE, LEVEL_MAP, LEVEL_COLORS,
    strip_level_prefix, split_by_level, get_summary_stats,
    enrich_with_fix_recommendations, safe_html,
)
from evals.report_level import (
    generate_level_json, generate_level_markdown, generate_level_html,
)

FOLDER_MAP = {
    "L1-Agent": "level1_agent",
    "L2-Interaction": "level2_interaction",
    "L3-E2E": "level3_e2e_operation",
}
SHORT_TITLE_MAP = {
    "L1-Agent": "level1",
    "L2-Interaction": "level2",
    "L3-E2E": "level3",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Main Summary Markdown (links to sub-reports, NO full metric dump)
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_main_markdown(results_data, output_path, global_stats, level_info):
    is_ready = global_stats['pass_rate'] >= TARGET_OVERALL_SCORE
    ready_status = "DEPLOYMENT READY" if is_ready else "NEEDS IMPROVEMENT"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# SHF Multi-Agent Evaluation Summary\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}\n")
        f.write(f"**Evaluation Model**: Groq `openai/gpt-oss-120b`\n")
        f.write(f"**Framework**: DeepEval (G-Eval with Chain-of-Thought)\n\n")

        f.write("---\n\n")

        f.write("## Executive Summary\n\n")
        f.write(f"| Metric | Value |\n")
        f.write(f"|--------|-------|\n")
        f.write(f"| Target Pass Rate | {TARGET_OVERALL_SCORE}% |\n")
        f.write(f"| Actual Pass Rate | {global_stats['pass_rate']:.1f}% |\n")
        f.write(f"| Passed / Total | {global_stats['total_pass']} / {global_stats['total_tests']} |\n")
        f.write(f"| Status | **{ready_status}** |\n\n")

        f.write("---\n\n")

        f.write("## Evaluation Levels\n\n")
        f.write("| Level | Pass Rate | Passed | Failed | Report |\n")
        f.write("|-------|-----------|--------|--------|--------|\n")

        for lvl_key, info in level_info.items():
            label = LEVEL_MAP.get(lvl_key, lvl_key)
            stats = info["stats"]
            md_link = info["md_link"]
            f.write(
                f"| {label} | {stats['pass_rate']:.1f}% | "
                f"{stats['total_pass']} | {stats['total_fail']} | "
                f"[View Report]({md_link}) |\n"
            )

        f.write("\n---\n\n")

        # Per-level highlights (top failures)
        f.write("## Key Findings\n\n")
        levels = split_by_level(results_data)
        for lvl_key in sorted(levels.keys()):
            if lvl_key == "Unknown":
                continue
            label = LEVEL_MAP.get(lvl_key, lvl_key)
            entries = levels[lvl_key]
            failures = []
            passes = []
            for e in entries:
                for m in e["metrics"]:
                    name = strip_level_prefix(e["agent"])
                    if m["passed"]:
                        passes.append(f"{name} — {m['metric']}")
                    else:
                        failures.append(f"{name} — {m['metric']} (score: {m['score']:.2f})")

            f.write(f"### {label}\n\n")
            if failures:
                f.write(f"**Failed ({len(failures)}):**\n")
                for fail in failures[:5]:  # top 5
                    f.write(f"- {fail}\n")
                if len(failures) > 5:
                    f.write(f"- _...and {len(failures) - 5} more (see detailed report)_\n")
            else:
                f.write("All metrics passed!\n")
            f.write("\n")

    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# Main Summary HTML Dashboard
# ═══════════════════════════════════════════════════════════════════════════════

def _generate_main_html(results_data, output_path, global_stats, level_info):
    is_ready = global_stats['pass_rate'] >= TARGET_OVERALL_SCORE
    ready_status = "READY" if is_ready else "NOT READY"
    ready_color = "#10b981" if is_ready else "#ef4444"

    # Per-level chart data
    level_labels = []
    level_pass = []
    level_fail = []
    level_rates = []
    level_chart_colors = []

    for lvl_key in sorted(level_info.keys()):
        label = LEVEL_MAP.get(lvl_key, lvl_key)
        stats = level_info[lvl_key]["stats"]
        level_labels.append(label)
        level_pass.append(stats["total_pass"])
        level_fail.append(stats["total_fail"])
        level_rates.append(round(stats["pass_rate"], 1))
        level_chart_colors.append(LEVEL_COLORS.get(lvl_key, "#64748b"))

    # Build level nav cards
    nav_cards = ""
    for lvl_key in sorted(level_info.keys()):
        info = level_info[lvl_key]
        label = LEVEL_MAP.get(lvl_key, lvl_key)
        stats = info["stats"]
        color = LEVEL_COLORS.get(lvl_key, "#64748b")
        rate = stats["pass_rate"]
        rate_color = "#10b981" if rate >= TARGET_OVERALL_SCORE else "#ef4444"
        html_link = info["html_link"]

        nav_cards += f"""
        <a href="{html_link}" class="level-card" style="border-color: {color};">
            <div class="level-label">{label}</div>
            <div class="level-rate" style="color: {rate_color};">{rate:.1f}%</div>
            <div class="level-detail">{stats['total_pass']}/{stats['total_tests']} passed</div>
            <div class="level-view">View Details</div>
        </a>
"""

    # Per-level failure highlights for the summary section
    highlights_html = ""
    levels = split_by_level(results_data)
    for lvl_key in sorted(levels.keys()):
        if lvl_key == "Unknown":
            continue
        label = LEVEL_MAP.get(lvl_key, lvl_key)
        color = LEVEL_COLORS.get(lvl_key, "#64748b")
        entries = levels[lvl_key]
        failures = []
        for e in entries:
            for m in e["metrics"]:
                if not m["passed"]:
                    name = strip_level_prefix(e["agent"])
                    failures.append((name, m["metric"], m["score"]))

        highlights_html += f'<div class="highlight-block" style="border-left-color: {color};">\n'
        highlights_html += f'<h3>{safe_html(label)}</h3>\n'
        if failures:
            highlights_html += f'<p class="fail-count">{len(failures)} failed metric(s)</p>\n<ul>\n'
            for name, metric, score in failures[:5]:
                score_str = f"{score:.2f}" if score is not None else "N/A"
                highlights_html += f'<li><span class="fail">{safe_html(name)}</span> — {safe_html(metric)} <code>{score_str}</code></li>\n'
            if len(failures) > 5:
                highlights_html += f'<li class="more">...and {len(failures) - 5} more</li>\n'
            highlights_html += '</ul>\n'
        else:
            highlights_html += '<p class="all-pass">All metrics passed!</p>\n'
        highlights_html += '</div>\n'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHF Multi-Agent Evaluation Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; line-height: 1.6; }}
        .dashboard {{ max-width: 1100px; margin: 0 auto; padding: 2rem; }}

        /* Header */
        .header {{ background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; }}
        .header-top {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }}
        .header h1 {{ color: #38bdf8; font-size: 1.6rem; margin-bottom: 0.25rem; }}
        .header-meta {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }}
        .header-tag {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; border: 1px solid #475569; color: #94a3b8; }}
        .status-pill {{ background: {ready_color}; color: #fff; padding: 0.4rem 1.2rem; border-radius: 9999px; font-weight: 700; font-size: 1rem; white-space: nowrap; }}

        /* Stats row */
        .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .stat-card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; text-align: center; }}
        .stat-card .value {{ font-size: 2.25rem; font-weight: 700; color: #38bdf8; }}
        .stat-card .label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.25rem; }}

        /* Level nav cards */
        .level-nav {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .level-card {{ display: block; text-decoration: none; color: inherit; background: #1e293b; border: 2px solid #334155; border-radius: 12px; padding: 1.5rem; text-align: center; transition: all 0.25s; }}
        .level-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }}
        .level-label {{ font-weight: 700; font-size: 1rem; color: #cbd5e1; }}
        .level-rate {{ font-size: 2rem; font-weight: 700; margin: 0.25rem 0; }}
        .level-detail {{ font-size: 0.8rem; color: #94a3b8; }}
        .level-view {{ margin-top: 0.75rem; color: #38bdf8; font-size: 0.85rem; }}

        /* Chart sections */
        .chart-section {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }}
        .chart-section h2 {{ color: #cbd5e1; font-size: 1.1rem; margin-bottom: 1rem; }}
        .chart-container {{ position: relative; height: 320px; }}

        /* Highlights */
        .highlights {{ margin-bottom: 2rem; }}
        .highlights > h2 {{ color: #cbd5e1; border-bottom: 1px solid #334155; padding-bottom: 0.3rem; margin-bottom: 1rem; }}
        .highlight-block {{ background: #1e293b; border: 1px solid #334155; border-left: 4px solid #64748b; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem; }}
        .highlight-block h3 {{ color: #cbd5e1; font-size: 1rem; margin-bottom: 0.5rem; }}
        .fail-count {{ color: #ef4444; font-size: 0.85rem; margin-bottom: 0.5rem; }}
        .all-pass {{ color: #10b981; font-size: 0.9rem; }}
        .highlight-block ul {{ list-style: none; padding: 0; }}
        .highlight-block li {{ padding: 0.25rem 0; font-size: 0.875rem; color: #cbd5e1; }}
        .highlight-block li code {{ background: #0f172a; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.8rem; color: #f59e0b; }}
        .highlight-block li.more {{ color: #64748b; font-style: italic; }}
        .pass {{ color: #10b981; }}
        .fail {{ color: #ef4444; }}

        /* Footer */
        .footer {{ text-align: center; color: #475569; font-size: 0.8rem; padding: 2rem 0 1rem; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <div class="header-top">
                <div>
                    <h1>SHF Multi-Agent Evaluation Dashboard</h1>
                    <div class="header-meta">
                        <span class="header-tag">DeepEval (G-Eval)</span>
                        <span class="header-tag">Groq &middot; openai/gpt-oss-120b</span>
                        <span class="header-tag">{datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</span>
                    </div>
                </div>
                <div class="status-pill">{ready_status}</div>
            </div>
        </div>

        <div class="stats-row">
            <div class="stat-card">
                <div class="value">{TARGET_OVERALL_SCORE}%</div>
                <div class="label">Target Score</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: {ready_color};">{global_stats['pass_rate']:.1f}%</div>
                <div class="label">Actual Score</div>
            </div>
            <div class="stat-card">
                <div class="value">{global_stats['total_pass']}/{global_stats['total_tests']}</div>
                <div class="label">Passed / Total</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: #ef4444;">{global_stats['total_fail']}</div>
                <div class="label">Failed Metrics</div>
            </div>
        </div>

        <div class="level-nav">
{nav_cards}
        </div>

        <div class="chart-section">
            <h2>Pass Rate by Evaluation Level</h2>
            <div class="chart-container">
                <canvas id="levelBarChart"></canvas>
            </div>
        </div>

        <div class="chart-section">
            <h2>Overall Pass / Fail Distribution</h2>
            <div class="chart-container" style="height: 280px; max-width: 400px; margin: 0 auto;">
                <canvas id="pieChart"></canvas>
            </div>
        </div>

        <div class="highlights">
            <h2>Key Findings by Level</h2>
{highlights_html}
        </div>

        <div class="footer">
            SHF Multi-Agent Quantitative Engine
        </div>
    </div>

    <script>
        // Level pass-rate bar chart
        new Chart(document.getElementById('levelBarChart').getContext('2d'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(level_labels)},
                datasets: [
                    {{ label: 'Passed', data: {json.dumps(level_pass)}, backgroundColor: '#10b981', borderRadius: 6 }},
                    {{ label: 'Failed', data: {json.dumps(level_fail)}, backgroundColor: '#ef4444', borderRadius: 6 }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ stacked: true, grid: {{ display: false }}, ticks: {{ color: '#94a3b8', font: {{ size: 13 }} }} }},
                    y: {{ stacked: true, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', stepSize: 1 }}, title: {{ display: true, text: 'Metrics', color: '#64748b' }} }}
                }},
                plugins: {{
                    legend: {{ position: 'top', labels: {{ color: '#94a3b8', usePointStyle: true }} }}
                }}
            }}
        }});

        // Pie chart
        new Chart(document.getElementById('pieChart').getContext('2d'), {{
            type: 'doughnut',
            data: {{
                labels: ['Passed', 'Failed'],
                datasets: [{{
                    data: [{global_stats['total_pass']}, {global_stats['total_fail']}],
                    backgroundColor: ['#10b981', '#ef4444'],
                    borderWidth: 0,
                    hoverOffset: 8
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                cutout: '55%',
                plugins: {{
                    legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', usePointStyle: true, padding: 16 }} }}
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


# ═══════════════════════════════════════════════════════════════════════════════
# Main Entrypoint
# ═══════════════════════════════════════════════════════════════════════════════

def generate_all_reports(results_data: list, base_output_dir: str):
    """Main entrypoint for generating all report formats."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    eval_dir = os.path.join(base_output_dir, f"evaluation_{timestamp}")
    os.makedirs(eval_dir, exist_ok=True)

    # Enrich with AI fix recommendations
    print("\n  [Report Generator] Consulting LLM for AI Fix Recommendations on failed metrics...")
    llm = GroqEvalLLM("openai/gpt-oss-120b")
    enrich_with_fix_recommendations(results_data, llm)

    # Global stats
    global_stats = get_summary_stats(results_data)

    # Split by level
    levels = split_by_level(results_data)

    if len(levels) > 1 or ("Unknown" not in levels and list(levels.keys())[0] in FOLDER_MAP):
        # === Unified suite: generate per-level sub-folders + main summary ===
        level_info = {}
        root_html_name = f"main_visualization_{timestamp}.html"

        for lvl_key, lvl_entries in levels.items():
            if lvl_key == "Unknown":
                continue

            folder_prefix = FOLDER_MAP.get(lvl_key, "other")
            short_title = SHORT_TITLE_MAP.get(lvl_key, "other")
            lvl_folder_name = f"{folder_prefix}_{timestamp}"
            lvl_dir = os.path.join(eval_dir, lvl_folder_name)
            os.makedirs(lvl_dir, exist_ok=True)

            lvl_stats = get_summary_stats(lvl_entries)
            lvl_label = LEVEL_MAP.get(lvl_key, lvl_key)

            # Generate per-level reports
            generate_level_json(
                lvl_entries,
                os.path.join(lvl_dir, f"metrics_data_{short_title}.json"),
                lvl_stats
            )
            generate_level_markdown(
                lvl_entries,
                os.path.join(lvl_dir, f"breakdown_report_{short_title}.md"),
                lvl_stats,
                f"SHF Evaluation - {lvl_label}"
            )
            generate_level_html(
                lvl_entries,
                os.path.join(lvl_dir, f"summary_visualization_{short_title}.html"),
                lvl_stats,
                f"SHF Evaluation - {lvl_label}",
                main_link=f"../{root_html_name}"
            )

            level_info[lvl_key] = {
                "stats": lvl_stats,
                "html_link": f"{lvl_folder_name}/summary_visualization_{short_title}.html",
                "md_link": f"{lvl_folder_name}/breakdown_report_{short_title}.md",
            }

        # Generate main summary reports
        root_md = os.path.join(eval_dir, f"main_report_{timestamp}.md")
        root_html = os.path.join(eval_dir, root_html_name)

        _generate_main_markdown(results_data, root_md, global_stats, level_info)
        _generate_main_html(results_data, root_html, global_stats, level_info)

        return root_md, None, root_html

    else:
        # === Single level (legacy): flat output ===
        json_path = os.path.join(eval_dir, f"metrics_data_{timestamp}.json")
        md_path = os.path.join(eval_dir, f"breakdown_report_{timestamp}.md")
        html_path = os.path.join(eval_dir, f"summary_visualization_{timestamp}.html")

        generate_level_json(results_data, json_path, global_stats)
        generate_level_markdown(results_data, md_path, global_stats, "SHF Evaluation Report")
        generate_level_html(results_data, html_path, global_stats, "SHF Evaluation Report")

        return md_path, json_path, html_path
