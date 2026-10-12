#!/usr/bin/env python3
"""Styled 16:9 deck from a design preset (needs python-pptx).

  pptx_starter.py OUT.pptx [--preset business-modern]

Copy the helpers (new_deck, add_title, add_bullets, add_chart_slide, set_alt) into your own
build script. Sizes come from the preset's slide scale; every text run gets an explicit size
and font so the result does not depend on the default template's theme.
"""
import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

TOKENS = Path(__file__).resolve().parents[1] / "design-tokens.json"
W, H = 13.333, 7.5


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_alt(shape, text):
    shape._element.xpath(".//p:cNvPr")[0].set("descr", text)


def style_run(run, p, size, color="text", bold=False, heading=False):
    run.font.name = p["fonts"]["heading" if heading else "body"]
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(p["colors"][color])


def new_deck(p):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    return prs


def blank(prs, p):
    s = prs.slides.add_slide(prs.slide_layouts[5])        # "Title Only"
    fill = s.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(p["colors"]["background"])
    return s


def add_title(slide, p, text):
    m = p["page"]["slide_margin_in"]
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Inches(m), Inches(0.45), Inches(W - 2 * m), Inches(1.2)
    tf = t.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.text = text
    for para in tf.paragraphs:
        para.alignment = PP_ALIGN.LEFT
        for r in para.runs:
            style_run(r, p, p["type"]["slide"]["title"], "text", True, heading=True)


def add_bullets(slide, p, items, left=None, width=None, top=1.9):
    m = p["page"]["slide_margin_in"]
    box = slide.shapes.add_textbox(Inches(left if left is not None else m), Inches(top),
                                   Inches(width if width is not None else W - 2 * m), Inches(4.8))
    tf = box.text_frame
    tf.word_wrap = True
    for i, text in enumerate(items):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.text = "•  " + text
        para.space_after = Pt(p["space"]["scale"][3])
        for r in para.runs:
            style_run(r, p, p["type"]["slide"]["body"])
    return box


def add_chart_slide(prs, p, title, categories, series_name, values, alt):
    s = blank(prs, p)
    add_title(s, p, title)
    cd = CategoryChartData()
    cd.categories = categories
    cd.add_series(series_name, values)
    m = p["page"]["slide_margin_in"]
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(m), Inches(1.9),
                            Inches(W - 2 * m), Inches(4.9), cd)
    set_alt(gf, alt)
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = False
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(p["type"]["slide"]["small"])
    dl.font.color.rgb = rgb(p["colors"]["text"])
    ser = plot.series[0]
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = rgb(p["chart"][0])
    for ax in (ch.category_axis, ch.value_axis):
        ax.tick_labels.font.size = Pt(p["type"]["slide"]["small"])
        ax.tick_labels.font.color.rgb = rgb(p["colors"]["muted"])
        ax.format.line.color.rgb = rgb(p["colors"]["rule"])
    ch.value_axis.has_major_gridlines = True
    ch.value_axis.major_gridlines.format.line.color.rgb = rgb(p["colors"]["rule"])
    ch.value_axis.minimum_scale = 0
    return s


def build(out, preset):
    p = json.loads(TOKENS.read_text(encoding="utf-8"))["presets"][preset]
    prs = new_deck(p)
    s1 = blank(prs, p)
    add_title(s1, p, "Quarterly review: growth is up, support load is the risk")
    box = s1.shapes.add_textbox(Inches(p["page"]["slide_margin_in"]), Inches(3.0), Inches(10), Inches(1))
    box.text_frame.text = "Leadership team · September"
    for r in box.text_frame.paragraphs[0].runs:
        style_run(r, p, p["type"]["slide"]["subtitle"], "muted")
    s1.notes_slide.notes_text_frame.text = "Open with the headline; the rest of the deck supports it."
    s2 = blank(prs, p)
    add_title(s2, p, "Three results this quarter")
    add_bullets(s2, p, ["Revenue up 12% to 4.2 M EUR", "Churn flat at 2.1%", "Support tickets up 18%"])
    s2.notes_slide.notes_text_frame.text = "One sentence per bullet. Ask for questions on support."
    s3 = add_chart_slide(prs, p, "Nordics grew fastest, up 15%", ["Nordics", "DACH", "UK"], "Q3 revenue (k EUR)",
                         (1380, 1040, 930), "Column chart of Q3 revenue by region: Nordics 1380, DACH 1040, UK 930 thousand euros")
    s3.notes_slide.notes_text_frame.text = "Source: finance ledger, September."
    prs.core_properties.title = "Quarterly review"
    prs.save(out)
    print(f"wrote {out} ({preset})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out")
    ap.add_argument("--preset", default="business-modern")
    a = ap.parse_args()
    build(a.out, a.preset)
