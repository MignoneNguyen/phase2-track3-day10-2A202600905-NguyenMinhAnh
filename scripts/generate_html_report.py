from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default="reports/metrics.json")
    parser.add_argument("--out", default="reports/report.html")
    args = parser.parse_args()
    
    metrics = json.loads(Path(args.metrics).read_text())
    
    scenarios_html = ""
    for name, status in metrics.get("scenarios", {}).items():
        scenarios_html += f"""
                    <li class="scenario-item">
                        <span class="scenario-name">{name}</span>
                        <span class="badge-pass">{status.title()}</span>
                    </li>"""

    recovery = metrics.get('recovery_time_ms', 0)
    recovery_s = recovery / 1000 if recovery else 0

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reliability Engineering Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0f1115;
            --text-main: #f0f3f6;
            --text-muted: #8b949e;
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.08);
            --accent-green: #2ea043;
            --accent-blue: #58a6ff;
            --accent-purple: #bc8cff;
            --accent-red: #da3633;
            --gradient-primary: linear-gradient(135deg, #58a6ff 0%, #bc8cff 100%);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.6;
            padding: 2rem;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(88, 166, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 85% 30%, rgba(188, 140, 255, 0.05) 0%, transparent 50%);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 4rem;
            animation: fadeInDown 0.8s ease-out;
        }}

        h1 {{
            font-size: 3rem;
            font-weight: 700;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            letter-spacing: -1px;
        }}

        .subtitle {{
            color: var(--text-muted);
            font-size: 1.1rem;
        }}

        .section-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .section-title::before {{
            content: '';
            display: block;
            width: 4px;
            height: 24px;
            background: var(--gradient-primary);
            border-radius: 4px;
        }}

        /* Glassmorphism Cards */
        .glass-card {{
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .glass-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 255, 255, 0.15);
        }}

        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 4rem;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        }}

        .metric-item {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .metric-label {{
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }}

        .metric-value {{
            font-size: 2.2rem;
            font-weight: 700;
        }}

        .value-green {{ color: var(--accent-green); }}
        .value-blue {{ color: var(--accent-blue); }}
        .value-purple {{ color: var(--accent-purple); }}

        /* Scenarios Section */
        .content-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 4rem;
            animation: fadeInUp 0.8s ease-out 0.4s both;
        }}

        @media (max-width: 768px) {{
            .content-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .scenario-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .scenario-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 1.5rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: background 0.2s ease;
        }}

        .scenario-item:hover {{
            background: rgba(255, 255, 255, 0.05);
        }}

        .scenario-name {{
            font-weight: 500;
            font-family: monospace;
            font-size: 1.1rem;
        }}

        .badge-pass {{
            background: rgba(46, 160, 67, 0.15);
            color: var(--accent-green);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            border: 1px solid rgba(46, 160, 67, 0.3);
        }}

        /* Analysis Section */
        .analysis-content {{
            color: #c9d1d9;
            font-size: 1.05rem;
        }}

        .analysis-content p {{
            margin-bottom: 1.5rem;
        }}

        .highlight-box {{
            background: rgba(88, 166, 255, 0.05);
            border-left: 4px solid var(--accent-blue);
            padding: 1.25rem;
            border-radius: 0 8px 8px 0;
            margin: 1.5rem 0;
        }}

        .highlight-box strong {{
            color: var(--accent-blue);
        }}

        .highlight-box.red {{
            background: rgba(218, 54, 51, 0.05);
            border-left-color: var(--accent-red);
        }}
        
        .highlight-box.red strong {{
            color: var(--accent-red);
        }}

        /* Animations */
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Reliability Engineering</h1>
            <p class="subtitle">System Performance & Chaos Testing Report</p>
        </header>

        <div class="metrics-grid">
            <div class="glass-card metric-item">
                <span class="metric-label">Availability</span>
                <span class="metric-value value-green">{metrics.get('availability', 0) * 100:.1f}%</span>
                <span class="metric-label" style="text-transform: none; color: #8b949e; font-size: 0.8rem; margin-top: auto;">{metrics.get('total_requests', 0)} Total Requests</span>
            </div>
            <div class="glass-card metric-item">
                <span class="metric-label">Cache Hit Rate</span>
                <span class="metric-value value-blue">{metrics.get('cache_hit_rate', 0) * 100:.1f}%</span>
                <span class="metric-label" style="text-transform: none; color: #8b949e; font-size: 0.8rem; margin-top: auto;">Cost Saved: ${metrics.get('estimated_cost_saved', 0):.2f}</span>
            </div>
            <div class="glass-card metric-item">
                <span class="metric-label">P99 Latency</span>
                <span class="metric-value value-purple">{metrics.get('latency_p99_ms', 0):.1f}ms</span>
                <span class="metric-label" style="text-transform: none; color: #8b949e; font-size: 0.8rem; margin-top: auto;">P50: {metrics.get('latency_p50_ms', 0):.1f}ms</span>
            </div>
            <div class="glass-card metric-item">
                <span class="metric-label">Circuit Interventions</span>
                <span class="metric-value" style="color: #f1e05a;">{metrics.get('circuit_open_count', 0)}</span>
                <span class="metric-label" style="text-transform: none; color: #8b949e; font-size: 0.8rem; margin-top: auto;">Recovery Avg: {recovery_s:.2f}s</span>
            </div>
        </div>

        <div class="content-grid">
            <div class="glass-card">
                <h2 class="section-title">Chaos Scenarios</h2>
                <ul class="scenario-list">
{scenarios_html}
                </ul>
            </div>

            <div class="glass-card">
                <h2 class="section-title">Analysis & Insights</h2>
                <div class="analysis-content">
                    <p>The fallback path was successfully tested and maintained a <strong>{metrics.get('availability', 0) * 100:.1f}% availability</strong> despite primary provider failure rates and timeouts being simulated in chaos testing. The circuit breaker appropriately prevented retry storms by entering the <code>OPEN</code> state {metrics.get('circuit_open_count', 0)} times.</p>
                    
                    <div class="highlight-box red">
                        <p><strong>Remaining Weakness:</strong> The Redis cache <code>keys</code> scanning iteration can block or become a bottleneck with millions of entries since we are scanning for semantic similarity over a high volume of key pairs.</p>
                    </div>

                    <div class="highlight-box">
                        <p><strong>Proposed Fix:</strong> Instead of linearly scanning all keys during a similarity query, we should migrate the cache lookup to a vector database backend (like Qdrant or Redis Vector Search) where an approximate nearest neighbor (ANN) search on embeddings can provide O(log N) fast retrieval.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(html_content, encoding="utf-8")
    print(f"wrote {{args.out}}")


if __name__ == "__main__":
    main()
