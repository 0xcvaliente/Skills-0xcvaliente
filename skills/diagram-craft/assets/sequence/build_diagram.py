#!/usr/bin/env python3
"""Editable authoring source for the order-flow sequence diagram.

Semantics come only from the request in evidence.json. Geometry is explicit;
no generic graph layout is used for the sequence notation.
"""
from html import escape
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
T = {
    "background": "#f8faf9", "surface": "#ffffff", "text": "#1d2e31",
    "secondary": "#59686b", "border": "#7c8d8f", "connector": "#37484b",
    "accent": "#1d625e", "accent_surface": "#e9f3f1",
}
actors = [("browser", "Browser", 178), ("api", "API", 402),
          ("database", "Database", 646), ("queue", "Queue", 866),
          ("worker", "Worker", 1100), ("fulfilment", "Fulfilment", 1326)]
source = (
    "The browser submits an order to the API. The API checks authorization: "
    "a denial returns 403 immediately; allowed requests store an order in the database, "
    "publish a job to a queue, then return 202. A worker later receives that job, "
    "calls the fulfilment service, and marks the order complete if fulfilment succeeds. "
    "On fulfilment failure, the worker records a failed state; retry policy is unknown."
)
ledger = [
    ("e1", "Browser → API: submit order", "user-provided"),
    ("e2", "API checks authorization", "user-provided"),
    ("e3", "If denied, API → Browser: 403 immediately; no allowed path work", "user-provided"),
    ("e4", "If allowed, API → Database: store order", "user-provided"),
    ("e5", "After storing, API → Queue: publish job", "user-provided"),
    ("e6", "After publishing, API → Browser: 202", "user-provided"),
    ("e7", "Later, Queue → Worker: job received asynchronously", "user-provided"),
    ("e8", "Worker → Fulfilment: call service", "user-provided"),
    ("e9", "If fulfilment succeeds, Worker marks order complete", "user-provided"),
    ("e10", "If fulfilment fails, Worker records failed state", "user-provided"),
    ("m1", "Storage target for the worker's state updates is unspecified; shown as worker self-actions", "explicit unknown"),
    ("m2", "Fulfilment outcome is represented as a response to the worker call", "notation inference"),
    ("u1", "Retry policy is unknown; no retry loop is drawn", "explicit unknown"),
    ("u2", "Store/publish failures, delivery guarantees and message payload details are unspecified", "omitted details"),
]
evidence = {
    "source": {"id": "brief", "kind": "supplied brief", "text": source},
    "entities": [{"id": i, "label": name, "source": "brief", "status": "user-provided"} for i, name, _ in actors],
    "relationships_and_notes": [{"id": i, "statement": statement, "source": "brief", "status": status} for i, statement, status in ledger],
    "style": {"name": "Porcelain and ink", "tokens": T},
}
(OUT / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")

svg = []
def add(s): svg.append(s)
def text(x, y, value, size=17, weight=400, color=None, anchor="start", extra=""):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or T["text"]}" text-anchor="{anchor}" {extra}>{escape(value)}</text>')
def label(i, x, y, value, width, anchor="start"):
    # Labels have surface masks so intermediate lifelines do not obscure text.
    left = x if anchor == "start" else x - width / 2
    add(f'<g data-label="{i}" data-x="{left-7}" data-y="{y-23}" data-w="{width+14}" data-h="32">')
    add(f'<rect x="{left-7}" y="{y-23}" width="{width+14}" height="32" fill="{T["surface"]}" rx="3"/>')
    text(x, y, value, 17, anchor=anchor)
    add('</g>')
def edge(i, x1, x2, y, value, kind="call", label_width=180):
    style = 'stroke-dasharray="7 5"' if kind == "return" else ''
    marker = "filled" if kind == "call" else "open"
    add(f'<polyline data-edge="{i}" points="{x1},{y} {x2},{y}" fill="none" stroke="{T["connector"]}" stroke-width="2" marker-end="url(#order-{marker})" {style}/>')
    label(i, (x1+x2)/2, y-15, value, label_width, "middle")

add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1480 1180" width="1480" height="1180" role="img" aria-labelledby="order-title order-desc">')
add('<title id="order-title">Order flow: authorization, acceptance and asynchronous fulfilment</title>')
add('<desc id="order-desc">Time runs downward through Browser, API, Database, Queue, Worker and Fulfilment lanes. Authorization denial returns 403 and ends the path. The allowed branch stores an order, publishes a job and returns 202 before the later queued phase. The worker calls fulfilment, then records complete on success or failed on failure. State updates are shown as worker self-actions because their storage target is unspecified. Retry policy is unknown.</desc>')
add('<defs>')
add(f'<marker id="order-filled" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M 0 0 L 12 6 L 0 12 Z" fill="{T["connector"]}"/></marker>')
add(f'<marker id="order-open" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M 1 1 L 11 6 L 1 11" fill="none" stroke="{T["connector"]}" stroke-width="1.5"/></marker>')
add('</defs>')
add(f'<rect x="0" y="0" width="1480" height="1180" fill="{T["background"]}"/>')
add('<g font-family="Arial, Helvetica, sans-serif">')

# Frames are beneath lifelines and messages. Alternative branches are separated
# by horizontal guard boundaries; they are mutually exclusive, not parallel.
add(f'<rect x="60" y="254" width="1370" height="818" rx="4" fill="{T["surface"]}" stroke="{T["connector"]}" stroke-width="1.5"/>')
add(f'<path d="M60 254 H120 V284 H60" fill="{T["accent_surface"]}" stroke="{T["connector"]}" stroke-width="1.5"/>')
text(76, 275, "alt", 15, 700)
add(f'<path d="M60 366 H1430" stroke="{T["connector"]}" stroke-width="1.5" stroke-dasharray="7 5"/>')
add(f'<rect x="588" y="760" width="818" height="294" rx="3" fill="{T["surface"]}" stroke="{T["connector"]}" stroke-width="1.5"/>')
add(f'<path d="M588 760 H648 V790 H588" fill="{T["accent_surface"]}" stroke="{T["connector"]}" stroke-width="1.5"/>')
text(604, 781, "alt", 15, 700)
add(f'<path d="M588 900 H1406" stroke="{T["connector"]}" stroke-width="1.5" stroke-dasharray="7 5"/>')

for actor_id, name, x in actors:
    add(f'<path d="M{x} 112 V1088" stroke="{T["border"]}" stroke-width="1.5" stroke-dasharray="5 6"/>')
    add(f'<g data-node="{actor_id}" data-x="{x-92}" data-y="44" data-w="184" data-h="68">')
    add(f'<rect x="{x-92}" y="44" width="184" height="68" rx="9" fill="{T["surface"]}" stroke="{T["border"]}" stroke-width="1.5"/>')
    text(x, 85, name, 19, 700, anchor="middle", extra=f'data-node-text="{actor_id}"')
    add('</g>')

# Header masks are drawn after lifelines so the frame's name stays unobscured.
add(f'<rect x="128" y="259" width="122" height="23" fill="{T["surface"]}"/>')
text(134, 276, "Authorization", 15, 700)
add(f'<rect x="655" y="765" width="156" height="23" fill="{T["surface"]}"/>')
text(661, 782, "Fulfilment result", 15, 700)

edge("e1", 178, 402, 165, "Submit order", label_width=122)
add(f'<polyline data-edge="e2" points="402,203 468,203 468,234 402,234" fill="none" stroke="{T["connector"]}" stroke-width="2" marker-end="url(#order-filled)"/>')
label("e2", 486, 222, "Check authorization", 160)
label("denied-guard", 82, 310, "[denied]", 69)
edge("e3", 402, 178, 339, "403 Forbidden", "return", 124)
text(483, 342, "Path ends immediately", 15, color=T["secondary"])
label("allowed-guard", 82, 397, "[allowed]", 78)
edge("e4", 402, 646, 440, "Store order", label_width=98)
edge("e5", 402, 866, 500, "Publish job", "async", 96)
edge("e6", 402, 178, 560, "202 Accepted", "return", 119)
text(938, 561, "Accepted ≠ fulfilled", 15, 600, T["secondary"])

# A time break is a diagram convention, not an inferred duration or concurrency
# guarantee. It represents the supplied "later" ordering.
add(f'<rect x="77" y="590" width="1336" height="52" rx="6" fill="{T["accent_surface"]}"/>')
text(95, 623, "LATER  /  ASYNCHRONOUS WORK", 16, 700, T["accent"])
text(682, 623, "Queue decouples the worker from the API response", 15, color=T["accent"])
edge("e7", 866, 1100, 687, "Deliver job", "async", 94)
edge("e8", 1100, 1326, 741, "Call fulfilment", label_width=124)
label("success-guard", 666, 816, "[succeeded]", 100)
edge("fulfilment-success", 1326, 1100, 843, "Success", "return", 70)
add(f'<polyline data-edge="e9" points="1100,867 1145,867 1145,890 1100,890" fill="none" stroke="{T["connector"]}" stroke-width="2" marker-end="url(#order-filled)"/>')
label("e9", 1165, 885, "Mark order complete", 173)
label("failure-guard", 666, 930, "[failed]", 60)
edge("fulfilment-failure", 1326, 1100, 959, "Failure", "return", 61)
label("retry-unknown", 838, 984, "Retry policy: unknown", 171)
add(f'<polyline data-edge="e10" points="1100,1009 1145,1009 1145,1033 1100,1033" fill="none" stroke="{T["connector"]}" stroke-width="2" marker-end="url(#order-filled)"/>')
label("e10", 1165, 1028, "Record failed state", 150)

text(61, 1111, "State updates are worker self-actions; their storage target is unspecified.", 15, color=T["secondary"])
for i, (x, kind, value) in enumerate([(70, "call", "Call / state write"), (400, "return", "Return / outcome"), (740, "async", "Asynchronous message")]):
    style = 'stroke-dasharray="7 5"' if kind == "return" else ''
    marker = "filled" if kind == "call" else "open"
    add(f'<path d="M{x} 1150 H{x+68}" fill="none" stroke="{T["connector"]}" stroke-width="2" marker-end="url(#order-{marker})" {style} aria-hidden="true"/>')
    text(x+83, 1156, value, 15, color=T["secondary"])
text(1131, 1156, "Time reads ↓", 15, 600, T["secondary"])
add('</g></svg>')
svg_string = "\n".join(svg)
(OUT / "order-sequence.svg").write_text(svg_string + "\n")

rows = "\n".join(f'<tr><td><code>{escape(i)}</code></td><td>{escape(statement)}</td><td>{escape(status)}</td></tr>' for i, statement, status in ledger)
html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Order flow — sequence companion</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f8faf9;color:#1d2e31;font:16px/1.6 Arial,Helvetica,sans-serif}
main{max-width:1536px;margin:auto;padding:42px 28px 52px}.eyebrow{font-size:12px;font-weight:700;letter-spacing:.12em;color:#1d625e;margin:0 0 8px}h1{font-size:36px;line-height:1.16;letter-spacing:-.02em;margin:0 0 14px}h2{font-size:22px;line-height:1.3;margin:0 0 12px}p{max-width:74ch;margin:0 0 14px}.lede{font-size:18px;color:#59686b}.canvas{width:100%;overflow:auto;border:1px solid #a7b3b4;border-radius:12px;background:#f8faf9;margin-top:22px}.canvas svg{display:block;width:1480px;height:auto;max-width:none}.scroll-note{font-size:14px;color:#59686b;margin:8px 0 30px}.columns{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-bottom:30px}.panel{background:#fff;border:1px solid #a7b3b4;border-radius:10px;padding:24px}.panel ol,.panel ul{padding-left:22px;margin:0}.panel li{margin:0 0 8px}.note{border-left:3px solid #1d625e;padding-left:15px}a{color:#1d625e;text-decoration-thickness:1px;text-underline-offset:3px}a:focus-visible{outline:3px solid #1d625e;outline-offset:4px}.table-scroll{overflow:auto;width:100%}table{border-collapse:collapse;width:100%;min-width:640px;font-size:14px}th,td{text-align:left;vertical-align:top;padding:11px 12px;border-bottom:1px solid #d8dfdf}th{background:#e9f3f1}th:first-child,td:first-child{width:100px}th:last-child,td:last-child{width:160px}code{font:13px/1.5 ui-monospace,monospace}.handoff{font-size:14px;color:#59686b;margin-top:20px}
@media(max-width:700px){main{padding:25px 16px 36px}h1{font-size:29px}.lede{font-size:17px}.columns{grid-template-columns:1fr;gap:16px}.panel{padding:19px}.canvas{border-radius:8px}}
@media print{main{padding:0}.canvas{overflow:visible;border:none}.canvas svg{width:100%;min-width:0}.scroll-note{display:none}.columns{grid-template-columns:1fr 1fr;gap:16px}.panel{padding:14px;break-inside:avoid}h1{font-size:28px}h2{font-size:19px}table{min-width:0}tr{break-inside:avoid}body{font-size:12px}.lede{font-size:14px}a{color:inherit}#evidence{break-before:page}}
</style></head><body><main>
<p class="eyebrow">ORDER PROCESSING · SEQUENCE</p>
<h1>Acceptance first. Fulfilment later.</h1>
<p class="lede">Authorization gates every order. An allowed request stores the order and queues work before returning 202; fulfilment and its final state happen afterward.</p>
<div class="canvas" tabindex="0" role="region" aria-label="Order sequence diagram; scroll horizontally to see all participants">''' + svg_string + '''</div>
<p class="scroll-note">Read time downward. Dashed arrows are returns; open solid arrows are asynchronous messages. On a narrow screen, scroll the diagram or read the flow below.</p>
<div class="columns"><section class="panel" aria-labelledby="flow-heading"><h2 id="flow-heading">The flow in words</h2>
<ol><li>The browser submits an order to the API.</li><li>The API checks authorization. If denied, it returns <code>403</code> immediately and the path ends.</li><li>If allowed, the API stores an order in the database, publishes a job to the queue, then returns <code>202</code>.</li><li>A worker later receives the queued job and calls the fulfilment service.</li><li>Success leads to an order marked complete. Failure leads to a recorded failed state.</li></ol>
</section><section class="panel" aria-labelledby="scope-heading"><h2 id="scope-heading">Known limits</h2>
<p class="note"><strong>Retry policy is unknown.</strong> The diagram does not introduce a retry loop, retry count, backoff or dead-letter path.</p>
<p>The worker's state updates are shown as self-actions. The brief does not specify where the worker records state, so no storage target is added.</p>
<p>Fulfilment outcomes appear as responses for readability. Storage/publish failures, queue delivery guarantees, timing durations and message fields are unspecified.</p>
<p><code>202</code> describes the API response before later processing; it does not mean fulfilment succeeded.</p>
</section></div>
<section class="panel" id="evidence" aria-labelledby="evidence-heading"><h2 id="evidence-heading">Evidence ledger</h2>
<p>All supplied claims come from the order-flow brief. There is no implementation source or observed runtime evidence.</p>
<div class="table-scroll"><table><thead><tr><th>ID</th><th>Statement</th><th>Status</th></tr></thead><tbody>''' + rows + '''</tbody></table></div></section>
<p class="handoff">Editable vector: <a href="order-sequence.svg">order-sequence.svg</a> · Authoring source: <a href="build_diagram.py">build_diagram.py</a> · Model and evidence: <a href="evidence.json">evidence.json</a>. Style: Porcelain and ink; local system fonts and no external assets.</p>
</main></body></html>'''
(OUT / "order-sequence.html").write_text(html)
print("Wrote order-sequence.svg, order-sequence.html, and evidence.json")
