import json
from collections import Counter
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

DECISION_COLORS = {"AUTO_CLEAR": "#2F8F5B", "FLAG_FOR_REVIEW": "#C98A1E", "ESCALATE": "#B23A48"}
ENV_COLORS = {"low": "#2F8F5B", "moderate": "#C98A1E", "high": "#B23A48"}

def generate_report(all_cases: list[dict], pdf_path="report.pdf", json_path="dashboard_payload.json"):
    # --- 1. Dashboard-ready JSON payload ---
    payload = []
    for c in all_cases:
        payload.append({
            "pair_id": c["pair_id"],
            "final_decision": c["final_decision"],
            "confidence": c["confidence"],
            "change_description": c["change_description"],
            "change_severity": c["change_severity"],
            "environmental_notes": c["environmental_notes"],
            "environmental_severity": c.get("environmental_severity", ""),
            "reason": c["decision_reason"],
        })
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    # --- 2. Chart 1: count of decisions ---
    decision_counts = Counter(c["final_decision"] for c in all_cases)
    d_labels = list(decision_counts.keys())
    d_values = [decision_counts[l] for l in d_labels]
    d_colors = [DECISION_COLORS.get(l, "#5B6472") for l in d_labels]

    plt.figure(figsize=(4, 3))
    plt.bar(d_labels, d_values, color=d_colors)
    plt.title("Cases by Decision")
    plt.ylabel("Count")
    plt.tight_layout()
    decision_chart_path = "decision_chart.png"
    plt.savefig(decision_chart_path, dpi=150)
    plt.close()

    # --- 3. Chart 2: environmental severity distribution ---
    env_counts = Counter(c.get("environmental_severity", "unknown") for c in all_cases)
    e_labels = list(env_counts.keys())
    e_values = [env_counts[l] for l in e_labels]
    e_colors = [ENV_COLORS.get(l, "#5B6472") for l in e_labels]

    plt.figure(figsize=(4, 3))
    plt.bar(e_labels, e_values, color=e_colors)
    plt.title("Cases by Environmental Impact")
    plt.ylabel("Count")
    plt.tight_layout()
    env_chart_path = "environmental_chart.png"
    plt.savefig(env_chart_path, dpi=150)
    plt.close()

    # --- 4. PDF report ---
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Urban Change Intelligence Agent — Case Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total cases reviewed: {len(all_cases)}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # side-by-side charts using a table
    chart_table = Table(
        [[RLImage(decision_chart_path, width=3*inch, height=2.25*inch),
          RLImage(env_chart_path, width=3*inch, height=2.25*inch)]]
    )
    elements.append(chart_table)
    elements.append(Spacer(1, 20))

    # summary table — every case gets a row
    table_data = [["Parcel", "Decision", "Confidence", "Severity", "Env. Impact"]]
    for c in all_cases:
        table_data.append([
            c["permit_record"].get("parcel_id", "-"),
            c["final_decision"],
            f"{c['confidence']}%",
            c["change_severity"],
            c.get("environmental_severity", "-"),
        ])
    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#21295C")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))

    # detail sections — only for cases that need human attention
    elements.append(Paragraph("Cases Requiring Attention", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    attention_cases = [c for c in all_cases if c["final_decision"] != "AUTO_CLEAR"]

    for c in attention_cases:
        elements.append(Paragraph(
            f"<b>{c['pair_id']}</b> — {c['final_decision']} ({c['confidence']}% confidence)",
            styles["Heading3"]
        ))

        # before/after images side by side
        img_table = Table([[
            RLImage(c["before_path"], width=2.2*inch, height=2.2*inch),
            RLImage(c["after_path"], width=2.2*inch, height=2.2*inch),
        ]])
        elements.append(img_table)
        elements.append(Spacer(1, 6))

        elements.append(Paragraph(f"Change: {c['change_description']}", styles["Normal"]))
        elements.append(Paragraph(f"Environmental notes: {c['environmental_notes']}", styles["Normal"]))
        elements.append(Paragraph(f"Reason: {c['decision_reason']}", styles["Normal"]))
        elements.append(Spacer(1, 18))

    doc.build(elements)
    print(f"Saved {pdf_path} and {json_path}")