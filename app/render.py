from __future__ import annotations

from html import escape
from pathlib import Path

from app.services.evidence_ranking_service import EvidenceRankingService


def badge(label: str, tone: str) -> str:
    return f'<span class="badge {tone}">{escape(label)}</span>'


def shell(title: str, subtitle: str, current: str, body: str) -> str:
    summary = EvidenceRankingService.summary()
    nav = [
        ("/", "Overview", "overview"),
        ("/evidence-board", "Evidence Board", "evidence-board"),
        ("/conflicts", "Conflicts", "conflicts"),
        ("/owners", "Owners", "owners"),
        ("/docs", "Docs", "docs"),
    ]
    nav_links = "".join(
        f'<a class="nav-link {"active" if key == current else ""}" href="{href}">{label}</a>'
        for href, label, key in nav
    )
    tabs = "".join(
        f'<a class="tab {"active" if key == current else ""}" href="{href}">{label}</a>'
        for href, label, key in nav
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #07111c;
        --bg-2: #0b1725;
        --panel: #0d1c2b;
        --panel-2: #102235;
        --line: rgba(255,255,255,0.08);
        --text: #edf3fb;
        --muted: #9eb0c6;
        --cyan: #8fd7ff;
        --amber: #f3c876;
        --green: #78e1a8;
        --red: #ff8e9f;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", system-ui, sans-serif;
        background:
          radial-gradient(circle at top left, rgba(143,215,255,0.14), transparent 24%),
          radial-gradient(circle at top right, rgba(243,200,118,0.08), transparent 22%),
          linear-gradient(180deg, #04080d 0%, var(--bg) 100%);
        color: var(--text);
      }}
      a {{ color: inherit; text-decoration: none; }}
      .shell {{ min-height: 100vh; display: grid; grid-template-columns: 260px minmax(0, 1fr); }}
      .sidebar {{
        padding: 22px 18px;
        border-right: 1px solid rgba(255,255,255,0.06);
        background: rgba(0,0,0,0.24);
      }}
      .brand {{
        display: flex; gap: 14px; align-items: center; padding: 10px 12px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
      }}
      .mark {{
        width: 44px; height: 44px; display: grid; place-items: center;
        border-radius: 14px; font-weight: 900;
        background: linear-gradient(135deg, #1b8cc4, #8668ff);
        box-shadow: 0 0 24px rgba(134,104,255,0.3);
      }}
      .brand strong {{ display:block; font-size:14px; }}
      .brand span {{ display:block; margin-top:4px; color:var(--cyan); font-size:10px; letter-spacing:.18em; text-transform:uppercase; }}
      .nav {{ margin-top: 18px; }}
      .nav-link {{
        display:block; padding:13px 14px; border-radius:14px; color:#8395af;
        font-size:12px; font-weight:800; letter-spacing:.12em; text-transform:uppercase;
      }}
      .nav-link.active {{ color: var(--cyan); background: rgba(143,215,255,0.08); border: 1px solid rgba(143,215,255,0.16); }}
      .nav-link:hover {{ color: var(--text); background: rgba(255,255,255,0.03); }}
      .sidecard {{
        margin-top: auto; padding: 18px 12px 8px; border-top: 1px solid rgba(255,255,255,0.06);
      }}
      .sidecard .k {{ color:#6f829c; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
      .sidecard .v {{ margin-top:6px; font-size:12px; font-weight:700; line-height:1.5; }}
      .main {{ padding: 0 32px 32px; }}
      .topbar {{
        position: sticky; top: 0; z-index: 2; display:flex; justify-content:space-between; gap:16px; align-items:center;
        padding: 22px 0 18px; border-bottom: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(7,17,28,0.96), rgba(7,17,28,0.84));
        backdrop-filter: blur(16px);
      }}
      .status {{
        display:inline-flex; gap:10px; align-items:center; padding:10px 14px; border-radius:999px;
        border:1px solid rgba(143,215,255,0.16); background: rgba(143,215,255,0.06);
        color:#d9ebff; font-size:11px; font-weight:800; letter-spacing:.16em; text-transform:uppercase;
      }}
      .dot {{ width:8px; height:8px; border-radius:999px; background:var(--cyan); box-shadow:0 0 12px rgba(143,215,255,0.9); }}
      .meta-row {{ display:flex; gap:14px; flex-wrap:wrap; }}
      .meta-box {{
        padding:10px 14px; border-radius:16px; border:1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
      }}
      .meta-box span {{ display:block; color:#7285a0; font-size:9px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
      .meta-box strong {{ display:block; margin-top:6px; font-size:12px; font-weight:800; }}
      .hero {{
        margin-top: 28px; border-radius: 30px; border:1px solid var(--line);
        background: linear-gradient(180deg, rgba(10,20,33,0.98), rgba(6,12,20,0.98));
        box-shadow: 0 28px 58px rgba(0,0,0,0.28); overflow:hidden;
      }}
      .hero-grid {{ display:grid; grid-template-columns: minmax(0, 1.25fr) 340px; }}
      .hero-copy {{ padding: 30px; }}
      .eyebrow {{ color:var(--cyan); font-size:11px; font-weight:900; letter-spacing:.24em; text-transform:uppercase; }}
      h1 {{ margin:16px 0 0; font-size: clamp(42px,5vw,72px); line-height:.92; font-family: Georgia, "Times New Roman", serif; letter-spacing:-.05em; }}
      .hero-copy p {{ margin:14px 0 0; color:var(--muted); font-size:18px; line-height:1.58; max-width:760px; }}
      .tabs {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:20px; }}
      .tab {{
        padding:10px 14px; border-radius:999px; border:1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03); color:#b1c1d6; font-size:11px; font-weight:800; letter-spacing:.12em; text-transform:uppercase;
      }}
      .tab.active {{ color: var(--amber); border-color: rgba(243,200,118,0.18); background: rgba(243,200,118,0.08); }}
      .hero-callout {{ padding: 28px; border-left:1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.02); }}
      .hero-callout h3 {{ margin:0; color:#7d90aa; font-size:12px; font-weight:900; letter-spacing:.16em; text-transform:uppercase; }}
      .hero-callout p {{ margin:14px 0 0; font-size:15px; line-height:1.6; color:#dbe6f5; }}
      .hero-kpis {{ display:grid; grid-template-columns: repeat(5, minmax(0,1fr)); border-top:1px solid rgba(255,255,255,0.06); }}
      .hero-kpi {{ padding:18px 20px 20px; border-right:1px solid rgba(255,255,255,0.06); }}
      .hero-kpi:last-child {{ border-right:0; }}
      .label, .kicker {{ color:#6f839f; font-size:10px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
      .hero-kpi .value {{ margin-top:8px; font-size:34px; font-weight:900; }}
      .section {{
        margin-top: 24px; border-radius: 26px; border:1px solid var(--line); background: var(--panel);
        overflow:hidden; box-shadow: 0 18px 44px rgba(0,0,0,0.22);
      }}
      .section-head {{ padding:22px 24px 16px; border-bottom:1px solid rgba(255,255,255,0.05); }}
      .section-head h2 {{ margin:10px 0 0; font-size:26px; font-family: Georgia, "Times New Roman", serif; letter-spacing:-.03em; }}
      .section-head p {{ margin:10px 0 0; color:var(--muted); font-size:15px; line-height:1.56; max-width:920px; }}
      .section-body {{ padding:24px; }}
      .grid-4, .grid-3, .grid-2 {{ display:grid; gap:18px; }}
      .grid-4 {{ grid-template-columns: repeat(4, minmax(0,1fr)); }}
      .grid-3 {{ grid-template-columns: repeat(3, minmax(0,1fr)); }}
      .grid-2 {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
      .card, .panel {{
        border-radius:20px; border:1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(0,0,0,0.08));
        padding:18px;
      }}
      .card .value {{ margin-top:10px; font-size:36px; font-weight:900; }}
      .card p, .panel p {{ margin:10px 0 0; color:var(--muted); font-size:14px; line-height:1.5; }}
      .packet {{
        border-radius:22px; border:1px solid rgba(255,255,255,0.06); background: rgba(4,9,17,0.58); overflow:hidden;
      }}
      .packet-top {{
        padding:20px 22px; display:grid; grid-template-columns:minmax(0,1fr) auto; gap:18px; align-items:start;
      }}
      .packet-top h3 {{ margin:0; font-size:23px; letter-spacing:-.03em; }}
      .meta {{ margin-top:8px; color:var(--muted); font-size:13px; }}
      .packet-bottom {{ padding:18px 22px 22px; border-top:1px solid rgba(255,255,255,0.05); background: rgba(255,255,255,0.02); }}
      .pill-stack {{ display:flex; flex-wrap:wrap; gap:8px; }}
      .pill {{
        display:inline-flex; padding:7px 10px; border-radius:999px; background: rgba(143,215,255,0.08); color:var(--cyan);
        font-size:10px; font-weight:800; letter-spacing:.12em; text-transform:uppercase;
      }}
      .badge {{
        display:inline-flex; padding:8px 12px; border-radius:999px; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.16em;
      }}
      .ready {{ color:var(--green); background: rgba(120,225,168,0.12); border:1px solid rgba(120,225,168,0.14); }}
      .watch {{ color:var(--amber); background: rgba(243,200,118,0.12); border:1px solid rgba(243,200,118,0.14); }}
      .contested {{ color:var(--red); background: rgba(255,142,159,0.12); border:1px solid rgba(255,142,159,0.14); }}
      .stats {{ display:grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap:10px; margin-top:14px; }}
      .stat {{
        padding:12px 12px 10px; border-radius:16px; background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05);
      }}
      .stat strong {{ display:block; margin-top:6px; font-size:24px; }}
      .code {{
        border-radius:22px; border:1px solid rgba(255,255,255,0.08); background: rgba(2,6,12,0.9); overflow:hidden;
      }}
      .code-head {{
        padding:16px 18px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.03);
      }}
      .lights {{ display:flex; gap:8px; }}
      .lights i {{ width:11px; height:11px; display:block; border-radius:999px; }}
      .lights i:nth-child(1) {{ background: rgba(255,142,159,0.7); }}
      .lights i:nth-child(2) {{ background: rgba(243,200,118,0.7); }}
      .lights i:nth-child(3) {{ background: rgba(120,225,168,0.7); }}
      pre {{ margin:0; padding:18px; white-space:pre-wrap; overflow:auto; color:#dce8fb; font-size:13px; line-height:1.58; font-family:"Cascadia Code", Consolas, monospace; }}
      table {{ width:100%; border-collapse:collapse; }}
      th, td {{ text-align:left; padding:14px 12px; border-bottom:1px solid rgba(255,255,255,0.06); vertical-align:top; }}
      th {{ color:#7f93ad; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.14em; }}
      td {{ font-size:13px; color:var(--text); }}
      .footer {{ display:flex; flex-wrap:wrap; gap:18px; margin:18px 0 8px; color:#7388a6; font-size:10px; text-transform:uppercase; letter-spacing:.16em; }}
      .footer strong {{ color:#c2d1e3; }}
      @media (max-width:1200px) {{
        .shell {{ grid-template-columns:1fr; }}
        .sidebar {{ display:none; }}
        .hero-grid, .hero-kpis, .grid-4, .grid-3, .grid-2, .stats {{ grid-template-columns:1fr; }}
        .topbar {{ flex-direction:column; align-items:flex-start; position:static; }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <aside class="sidebar">
        <div>
          <div class="brand">
            <div class="mark">ER</div>
            <div>
              <strong>Evidence Ranking Engine</strong>
              <span>Trust scoring // v1.0</span>
            </div>
          </div>
          <div class="nav">{nav_links}</div>
        </div>
        <div class="sidecard">
          <div class="k">Lead recommendation</div>
          <div class="v">{escape(summary["leadRecommendation"])}</div>
        </div>
      </aside>
      <main class="main">
        <div class="topbar">
          <div class="status"><span class="dot"></span>Evidence ranking registry live</div>
          <div class="meta-row">
            <div class="meta-box"><span>Contested lanes</span><strong>{summary["contestedLanes"]} packets</strong></div>
            <div class="meta-box"><span>Freshness watch</span><strong>{summary["freshnessWatchCount"]} aging chains</strong></div>
            <div class="meta-box"><span>Average trust</span><strong>{summary["avgTrustScore"]:.1f} baseline</strong></div>
          </div>
        </div>
        <section class="hero">
          <div class="hero-grid">
            <div class="hero-copy">
              <div class="eyebrow">Evidence Ranking Engine</div>
              <h1>{escape(title)}</h1>
              <p>{escape(subtitle)}</p>
              <div class="tabs">{tabs}</div>
            </div>
            <div class="hero-callout">
              <h3>Why this matters</h3>
              <p>Decision systems usually fail by over-trusting weak evidence. This surface keeps freshness, contradiction pressure, and citation density visible before a recommendation locks in.</p>
            </div>
          </div>
          <div class="hero-kpis">
            <div class="hero-kpi"><div class="label">Evidence packets</div><div class="value">{summary["evidenceCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Contested lanes</div><div class="value">{summary["contestedLanes"]}</div></div>
            <div class="hero-kpi"><div class="label">Freshness watch</div><div class="value">{summary["freshnessWatchCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Owners</div><div class="value">{summary["ownerCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Avg trust</div><div class="value">{summary["avgTrustScore"]:.1f}</div></div>
          </div>
        </section>
        {body}
        <div class="footer">
          <span><strong>Discipline:</strong> decision intelligence</span>
          <span><strong>Focus:</strong> trust / freshness / contradictions / citations</span>
          <span><strong>Surface:</strong> operator-first / ranking-safe / replayable</span>
        </div>
      </main>
    </div>
  </body>
</html>"""


def render_overview() -> str:
    packets = EvidenceRankingService.evidence_packets()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Control-plane summary</div>
          <h2>Evidence should earn its place in a decision, not just show up near the prompt.</h2>
          <p>This engine ranks evidence packets by trust score, citation density, freshness, and contradiction pressure so operators can see which claims deserve to anchor a recommendation.</p>
        </div>
        <div class="section-body">
          <div class="grid-4">
            <div class="card"><div class="label">Ready packets</div><div class="value">{len([p for p in packets if p["status"] == "ready"])}</div><p>Evidence chains that still look safe to lead with.</p></div>
            <div class="card"><div class="label">Watch packets</div><div class="value">{len([p for p in packets if p["status"] == "watch"])}</div><p>Useful evidence carrying freshness or contradiction pressure.</p></div>
            <div class="card"><div class="label">Contested packets</div><div class="value">{len([p for p in packets if p["status"] == "contested"])}</div><p>Evidence that should not become a confident recommendation without refresh.</p></div>
            <div class="card"><div class="label">Owners</div><div class="value">{len(EvidenceRankingService.owner_lanes())}</div><p>Stewardship lanes responsible for evidence quality and review timing.</p></div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="kicker">Top-ranked evidence</div>
          <h2>The best evidence packets stay visible as reusable decision anchors.</h2>
          <p>Ranking is only useful when the operator can still inspect why one packet rose above another and where contradiction pressure starts to bend the story.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">
            {"".join(render_packet_card(packet) for packet in packets[:2])}
          </div>
        </div>
      </section>
    """
    return shell(
        "Rank evidence before it becomes confident advice.",
        "A Python and FastAPI engine for scoring evidence packets by trust, freshness, citations, and contradiction pressure.",
        "overview",
        body,
    )


def render_evidence_board() -> str:
    cards = "".join(render_packet_card(packet) for packet in EvidenceRankingService.evidence_packets())
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Evidence board</div>
          <h2>Each packet shows why it is strong, stale, or under contradiction pressure.</h2>
          <p>The board is sorted so contested and watch lanes stay visible before ready evidence gets treated as universal truth.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">{cards}</div>
        </div>
      </section>
    """
    return shell(
        "Evidence packets ordered by trust and review pressure.",
        "A Python and FastAPI engine for scoring evidence packets by trust, freshness, citations, and contradiction pressure.",
        "evidence-board",
        body,
    )


def render_conflicts() -> str:
    conflicts = EvidenceRankingService.conflicts()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Conflict board</div>
          <h2>Contradictions are visible before they mutate into confident-but-wrong recommendations.</h2>
          <p>Conflict scoring blends contradiction count, age, and trust posture so teams can see which evidence chains need fresh review first.</p>
        </div>
        <div class="section-body">
          <table>
            <thead>
              <tr>
                <th>Packet</th>
                <th>Domain</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Contradictions</th>
                <th>Freshness</th>
                <th>Review pressure</th>
              </tr>
            </thead>
            <tbody>
              {"".join(
                  f"<tr><td><strong>{escape(item['title'])}</strong></td><td>{escape(item['domain'])}</td><td>{escape(item['owner'])}</td><td>{badge(item['status'], item['status'])}</td><td>{item['contradictionCount']}</td><td>{item['freshnessDays']} days</td><td>{item['reviewPressure']}</td></tr>"
                  for item in conflicts
              )}
            </tbody>
          </table>
        </div>
      </section>
    """
    return shell(
        "Conflict lanes that should be re-ranked before the next recommendation cycle.",
        "A Python and FastAPI engine for scoring evidence packets by trust, freshness, citations, and contradiction pressure.",
        "conflicts",
        body,
    )


def render_owners() -> str:
    lanes = EvidenceRankingService.owner_lanes()
    owner_cards = "".join(render_owner_card(lane) for lane in lanes)
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">Owner lanes</div>
          <h2>Evidence stewardship gets better when ownership pressure is explicit.</h2>
          <p>Owner lanes reveal who is carrying stale or contested evidence chains and which packet should be refreshed before the next decision memo leans on it.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">{owner_cards}</div>
        </div>
      </section>
    """
    return shell(
        "Owner lanes for evidence stewardship and review pressure.",
        "A Python and FastAPI engine for scoring evidence packets by trust, freshness, citations, and contradiction pressure.",
        "owners",
        body,
    )


def render_docs() -> str:
    sample = EvidenceRankingService.evaluate(
        {
            "prompt": "Need fraud automation evidence for LATAM payments release board",
            "freshness_budget_days": 10,
            "minimum_trust_score": 80,
        }
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="kicker">API summary</div>
          <h2>A small route surface for evidence ranking, conflict inspection, and operator-safe reuse.</h2>
          <p>The engine exposes the minimum surface needed to store evidence packets, inspect contradiction lanes, and re-rank evidence against a live prompt.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">
            <div class="card"><div class="label">GET /api/evidence</div><div class="value" style="font-size:22px;">Evidence board</div><p>Returns ranked evidence packets with trust, freshness, and contradiction details.</p></div>
            <div class="card"><div class="label">GET /api/conflicts</div><div class="value" style="font-size:22px;">Conflict board</div><p>Returns contradiction lanes sorted by review pressure.</p></div>
            <div class="card"><div class="label">POST /api/analyze/rank</div><div class="value" style="font-size:22px;">Prompt fit</div><p>Re-ranks evidence against a fresh prompt, trust threshold, and freshness budget.</p></div>
          </div>
          <div class="code" style="margin-top:18px;">
            <div class="code-head"><span class="label" style="color:#92d9ff;">Sample rank response</span><div class="lights"><i></i><i></i><i></i></div></div>
            <pre>{escape(str(sample))}</pre>
          </div>
        </div>
      </section>
    """
    return shell(
        "API surface for evidence ranking and contradiction-aware review.",
        "A Python and FastAPI engine for scoring evidence packets by trust, freshness, citations, and contradiction pressure.",
        "docs",
        body,
    )


def render_packet_card(packet: dict[str, object]) -> str:
    signal_pills = "".join(f"<span class='pill'>{escape(signal)}</span>" for signal in packet["keySignals"])
    source_pills = "".join(
        f"<span class='pill'>{escape(source)}</span>" for source in packet["supportingSources"]
    )
    return f"""
      <div class="packet">
        <div class="packet-top">
          <div>
            <h3>{escape(str(packet['title']))}</h3>
            <div class="meta">{escape(str(packet['owner']))} · {escape(str(packet['domain']))} · {escape(str(packet['sourceSystem']))}</div>
          </div>
          {badge(str(packet['status']), str(packet['status']))}
        </div>
        <div class="packet-bottom">
          <p>{escape(str(packet['claim']))}</p>
          <div class="stats">
            <div class="stat"><div class="label">Rank score</div><strong>{packet['rankScore']}</strong></div>
            <div class="stat"><div class="label">Trust</div><strong>{packet['trustScore']}</strong></div>
            <div class="stat"><div class="label">Citations</div><strong>{packet['citationCount']}</strong></div>
            <div class="stat"><div class="label">Conflicts</div><strong>{packet['contradictionCount']}</strong></div>
          </div>
          <div class="pill-stack" style="margin-top:14px;">
            {signal_pills}
          </div>
          <div class="pill-stack" style="margin-top:10px;">
            {source_pills}
          </div>
        </div>
      </div>
    """


def render_owner_card(lane: dict[str, object]) -> str:
    domains = "".join(f"<span class='pill'>{escape(str(domain))}</span>" for domain in lane["domains"])
    return f"""
      <div class="card">
        <div class="label">Owner lane</div>
        <div class="value" style="font-size:26px;">{escape(str(lane['owner']))}</div>
        <p>{lane['evidenceCount']} packets · {lane['contestedCount']} contested lanes · trust {lane['averageTrustScore']}</p>
        <div class="pill-stack" style="margin-top:14px;">{domains}</div>
        <p style="margin-top:14px;"><strong>Focus packet:</strong> {escape(str(lane['focusPacket']))}</p>
      </div>
    """


def write_static_proof_pages(screenshot_dir: Path) -> list[Path]:
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-evidence-board.html": render_evidence_board(),
        "03-conflicts.html": render_conflicts(),
        "04-api-summary.html": render_docs(),
    }
    written = []
    for name, content in pages.items():
        page = screenshot_dir / name
        page.write_text(content, encoding="utf-8")
        written.append(page)
    return written
