#!/usr/bin/env python3
"""Styled PDF from a design preset (needs reportlab).

  pdf_starter.py OUT.pdf [--preset report-classic]

Uses the PDF standard fonts (Helvetica / Times / Courier), which every viewer has; the
preset's named fonts map to the closest of these. To use a brand font, register a TrueType
file with pdfmetrics.registerFont(TTFont(...)) and embed it.
"""
import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

TOKENS = Path(__file__).resolve().parents[1] / "design-tokens.json"
SERIF = {"Georgia", "Times New Roman", "Cambria"}


def hexc(h):
    return colors.HexColor(h)


def build(out, preset):
    p = json.loads(TOKENS.read_text(encoding="utf-8"))["presets"][preset]
    if "document" not in p.get("media", ["document"]):
        raise SystemExit(f"error: preset {preset!r} is not for documents (allowed media: {', '.join(p['media'])}); choose another preset")
    c, t, sp = p["colors"], p["type"]["document"], p["space"]
    serif = p["fonts"]["heading"] in SERIF
    heading = "Times-Bold" if serif else "Helvetica-Bold"
    body, body_bold = "Helvetica", "Helvetica-Bold"
    styles = {
        "title": ParagraphStyle("title", fontName=heading, fontSize=t["title"], leading=t["title"] * 1.15,
                                textColor=hexc(c["primary"]), spaceAfter=sp["scale"][3], alignment=TA_LEFT),
        "h1": ParagraphStyle("h1", fontName=heading, fontSize=t["h1"], leading=t["h1"] * 1.2, textColor=hexc(c["primary"]),
                             spaceBefore=sp["heading_before_pt"], spaceAfter=sp["scale"][1], keepWithNext=True),
        "body": ParagraphStyle("body", fontName=body, fontSize=t["body"], leading=t["body"] * t["line_height"],
                               textColor=hexc(c["text"]), spaceAfter=sp["paragraph_after_pt"]),
        "caption": ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=t["caption"], leading=t["caption"] * 1.3,
                                  textColor=hexc(c["muted"]), spaceBefore=4),
    }
    page = A4 if p["page"]["size"].upper() == "A4" else letter
    m = p["page"]["margin_mm"] * mm

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", t["footer"])
        canvas.setFillColor(hexc(c["muted"]))
        canvas.drawRightString(page[0] - m, m * 0.5, f"Page {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(out, pagesize=page, leftMargin=m, rightMargin=m, topMargin=m, bottomMargin=m,
                            title="Quarterly review", author="Team", subject="Quarterly review")
    story = [Paragraph("Quarterly review", styles["title"]),
             Paragraph("Summary", styles["h1"]),
             Paragraph("Revenue grew 12% quarter on quarter, driven by the new onboarding flow. Churn held flat. "
                       "The one risk is support load, which rose 18%.", styles["body"]),
             Paragraph("Key results", styles["h1"]),
             ListFlowable([ListItem(Paragraph(x, styles["body"])) for x in
                           ("Revenue: 4.2 M EUR, up 12%", "Churn: 2.1%, unchanged", "Support tickets: up 18%")],
                          bulletType="bullet", leftIndent=14)]
    rows = [["Region", "Q2 (k EUR)", "Q3 (k EUR)", "Change"],
            ["Nordics", "1 200", "1 380", "+15%"], ["DACH", "980", "1 040", "+6%"], ["UK", "820", "930", "+13%"]]
    tb = p["table"]
    ts = [("FONTNAME", (0, 0), (-1, 0), body_bold), ("FONTSIZE", (0, 0), (-1, -1), t["body"] - 1),
          ("BACKGROUND", (0, 0), (-1, 0), hexc(c[tb["header_fill"]])), ("TEXTCOLOR", (0, 0), (-1, 0), hexc(c[tb["header_text"]])),
          ("TEXTCOLOR", (0, 1), (-1, -1), hexc(c["text"])), ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
          ("LINEBELOW", (0, 0), (-1, -1), 0.5, hexc(c[tb["rule"]])), ("TOPPADDING", (0, 0), (-1, -1), 5),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("FONTNAME", (0, 1), (-1, -1), body)]
    table = Table(rows, colWidths=[55 * mm, 35 * mm, 35 * mm, 30 * mm], repeatRows=1)
    table.setStyle(TableStyle(ts))
    story += [Spacer(1, sp["scale"][3]), table, Paragraph("Table 1. Revenue by region. Source: finance ledger, September.", styles["caption"])]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"wrote {out} ({preset})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out")
    ap.add_argument("--preset", default="report-classic")
    a = ap.parse_args()
    build(a.out, a.preset)
