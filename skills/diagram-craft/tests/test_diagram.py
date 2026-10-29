"""Meaningful helper invariants; rendered layout is tested separately."""
import copy
import importlib.util
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("diagram", ROOT / "scripts" / "diagram.py")
diagram = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagram)


class DiagramTests(unittest.TestCase):
    def setUp(self):
        self.scene = json.loads((ROOT / "assets" / "architecture.scene.json").read_text())

    def test_both_shipped_scenes_validate_and_export(self):
        for asset in ROOT.glob("assets/*.scene.json"):
            scene = json.loads(asset.read_text())
            with self.subTest(asset=asset.name):
                self.assertEqual(diagram.validate(scene), [])
                svg = ET.fromstring(diagram.extract_svg(diagram.render_html(scene)))
                self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertEqual(len(svg.findall(".//{http://www.w3.org/2000/svg}polyline")), len(scene["edges"]))

    def test_missing_endpoint_refuses_render(self):
        self.scene["edges"][0]["to"] = "missing"
        with self.assertRaisesRegex(ValueError, "unknown to endpoint"):
            diagram.render_html(self.scene)

    def test_ids_are_unique_across_kinds(self):
        self.scene["regions"][0]["id"] = "client"
        self.assertTrue(any("duplicate ID" in e for e in diagram.validate(self.scene)))

    def test_nonfinite_and_boolean_coordinates_rejected(self):
        for bad in (float("nan"), float("inf"), True):
            scene = copy.deepcopy(self.scene)
            scene["nodes"][0]["x"] = bad
            self.assertTrue(diagram.validate(scene))

    def test_obstructed_edge_and_bad_port_rejected(self):
        self.scene["edges"][0]["points"] = [[280,160],[600,160],[470,160]]
        self.assertTrue(any("passes through node api" in e for e in diagram.validate(self.scene)))
        self.scene["edges"][0]["points"] = [[260,160],[470,160]]
        self.assertTrue(any("boundary" in e for e in diagram.validate(self.scene)))

    def test_diagonal_obstruction_geometry(self):
        self.assertTrue(diagram.segment_hits((0,0), (100,100), (40,40,60,60)))
        self.assertFalse(diagram.segment_hits((0,0), (100,0), (40,0,60,60)))
        self.assertFalse(diagram.segment_hits((0,0), (100,100), (0,80,20,100)))

    def test_node_label_overlap_and_canvas_bounds_rejected(self):
        self.scene["edges"][0]["label_at"] = [60,100]
        self.assertTrue(any("label overlaps node" in e for e in diagram.validate(self.scene)))
        self.scene["nodes"][0]["x"] = -1
        self.assertTrue(any("outside canvas" in e for e in diagram.validate(self.scene)))

    def test_low_contrast_rejected(self):
        self.scene["tokens"] = {"ink":"#ffffff"}
        self.assertTrue(any("contrast" in e for e in diagram.validate(self.scene)))

    def test_faint_node_border_rejected(self):
        self.scene["tokens"] = {"rule": "#d5d9d6"}
        self.assertTrue(any("contrast rule/paper" in e for e in diagram.validate(self.scene)))

    def test_default_palettes_meet_contrast_contract(self):
        for theme in diagram.PALETTES:
            self.scene["theme"] = theme
            self.scene.pop("tokens", None)
            with self.subTest(theme=theme):
                self.assertFalse([e for e in diagram.validate(self.scene) if "contrast" in e])

    def test_offline_font_check(self):
        rendered = diagram.render_html(self.scene)
        self.assertEqual(diagram.offline_font_findings(rendered), [])
        remote = '<style>@import url("https://fonts.googleapis.com/css2?family=Inter");</style>'
        self.assertTrue(any("remote font" in f for f in diagram.offline_font_findings(remote)))
        no_generic = '<svg font-family="Inter, Helvetica"></svg>'
        self.assertTrue(any("generic fallback" in f for f in diagram.offline_font_findings(no_generic)))

    def export(self, body, view="0 0 100 50", wrap="{}"):
        return wrap.format(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}">{body}</svg>')

    def test_shipped_exports_pass_export_checks(self):
        for path in ROOT.glob("assets/**/*.svg"):
            with self.subTest(path=path.name):
                self.assertEqual(diagram.export_findings(path.read_text(encoding="utf-8"), False), [])

    def test_content_outside_viewbox_is_flagged(self):
        inside = self.export('<rect x="0" y="0" width="100" height="50"/>')
        self.assertEqual(diagram.export_findings(inside), [])
        for body in ('<rect x="90" y="10" width="20" height="10"/>', '<circle cx="5" cy="5" r="10"/>',
                     '<polyline points="0,0 120,10"/>', '<text x="10" y="80">late</text>'):
            with self.subTest(body=body):
                found = diagram.export_findings(self.export(body))
                self.assertTrue(any("outside the viewBox" in f for f in found), found)

    def test_viewbox_check_skips_unmeasurable_content(self):
        for body in ('<g transform="translate(200 0)"><rect width="10" height="10"/></g>',
                     '<defs><rect x="500" width="10" height="10"/></defs>',
                     '<rect x="500" width="10" height="10" display="none"/>',
                     '<rect x="500" width="0" height="10"/>',
                     '<rect x="50%" width="10" height="10"/>',
                     '<g style="transform:translate(-200px,0)"><rect x="200" width="10" height="10"/></g>',
                     '<rect x="500" width="10" height="10" style="fill:red;/**/transform:translateX(-450px)"/>'):
            with self.subTest(body=body):
                self.assertEqual(diagram.export_findings(self.export(body)), [])

    def test_viewbox_offset_and_missing_size(self):
        shifted = self.export('<rect x="-20" y="-20" width="10" height="10"/>', view="-30 -30 100 50")
        self.assertEqual(diagram.export_findings(shifted), [])
        bad = self.export("", view="0 0 0 50")
        self.assertTrue(any("viewBox" in f for f in diagram.export_findings(bad)))
        bare = '<svg xmlns="http://www.w3.org/2000/svg"><rect width="5" height="5"/></svg>'
        self.assertTrue(any("cannot be checked" in f for f in diagram.export_findings(bare)))

    def test_alpha_paint_and_dangling_reference_flagged(self):
        found = diagram.export_findings(self.export('<rect width="5" height="5" fill="rgba(0,0,0,.5)" stroke="#11223380"/>'))
        self.assertEqual(sum("alpha" in f for f in found), 2)
        ok = self.export('<rect width="5" height="5" fill="#000" fill-opacity=".5"/>')
        self.assertEqual(diagram.export_findings(ok), [])
        dangling = self.export('<path d="M0 0" marker-end="url(#gone)"/>')
        self.assertTrue(any("missing id 'gone'" in f for f in diagram.export_findings(dangling)))

    def test_alpha_in_inline_style_flagged(self):
        for style in ("fill:rgba(0,0,0,.5)", "stroke: #11223380 !important", "stop-color:hsla(0,0%,0%,.4);opacity:1"):
            with self.subTest(style=style):
                found = diagram.export_findings(self.export(f'<rect width="5" height="5" style="{style}"/>'))
                self.assertTrue(any("alpha" in f for f in found), found)
        ok = self.export('<rect width="5" height="5" style="fill:#000;fill-opacity:.5;stroke:rgb(1,2,3)"/>')
        self.assertEqual(diagram.export_findings(ok), [])

    def test_embedded_figures_need_scoped_ids_and_styles(self):
        one = self.export('<style>.node{fill:red}</style><rect id="a" width="5" height="5"/>')
        self.assertEqual(diagram.export_findings(one), [])
        two = f"<main>{one}{one}</main>"
        found = diagram.export_findings(two)
        self.assertTrue(any("also used by" in f for f in found))
        self.assertTrue(any("not scoped" in f for f in found))
        scoped = lambda n: self.export(f'<style>#f{n} .node{{fill:red}}</style><rect id="f{n}" width="5" height="5"/>')
        self.assertEqual(diagram.export_findings(scoped(1) + scoped(2)), [])

    def test_selector_scan_reads_grouped_rules_and_ignores_comment_text_in_strings(self):
        css = ('@layer base,theme;@media print{.a{fill:red}#f1 .b{fill:blue}}@keyframes k{from{opacity:0}}'
               '@font-face{font-family:x}[data-label="a/*b"] .c{fill:red}/* .gone{} */.d{content:"}"}')
        self.assertEqual(diagram.css_selectors(css), [".a", "#f1 .b", '[data-label="a/*b"] .c', ".d"])

    def test_unscoped_rule_inside_media_is_flagged_when_figures_share_a_page(self):
        def figure(n, css):
            return self.export(f'<style>{css}</style><rect id="f{n}" width="5" height="5"/>')
        loose = figure(1, "@media print{.node{fill:#000}}") + figure(2, "#f2 .node{fill:red}")
        self.assertTrue(any("not scoped" in f for f in diagram.export_findings(f"<main>{loose}</main>")))
        scoped = figure(1, "@media print{#f1 .node{fill:#000}}") + figure(2, "@media print{#f2 .node{fill:#000}}")
        self.assertFalse(any("not scoped" in f for f in diagram.export_findings(f"<main>{scoped}</main>")))
        quoted = figure(1, '#f1 [data-label="a/*b"] .node{fill:red}') + figure(2, "#f2 .node{fill:red}")
        self.assertFalse(any("not scoped" in f for f in diagram.export_findings(f"<main>{quoted}</main>")))

    def test_cdata_is_html_only_and_comments_are_inert(self):
        body = '<style><![CDATA[.a{fill:red}]]></style><!-- note: a-b --><rect width="5" height="5"/>'
        svg = self.export(body)
        self.assertEqual(diagram.export_findings(svg, False), [])
        self.assertTrue(any("CDATA" in f for f in diagram.export_findings(svg, True)))

    def test_nested_icon_svg_does_not_end_the_figure_early(self):
        nested = self.export('<svg viewBox="0 0 10 10" x="2" y="2" width="10" height="10"><circle r="3" cx="5" cy="5"/></svg><rect x="90" width="20" height="5"/>')
        found = diagram.export_findings(nested)
        self.assertEqual(len(diagram.inline_svgs(nested)), 1)
        self.assertTrue(any("<rect> extends outside" in f for f in found), found)

    def test_check_command_reports_export_findings(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.svg"
            path.write_text(self.export('<rect x="200" width="5" height="5"/>'), encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts" / "diagram.py"), "check", str(path)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            result = json.loads(run.stdout)
            self.assertFalse(result["ok"])
            self.assertTrue(result["export"])

    def test_strings_are_escaped_and_model_is_preserved(self):
        self.scene["nodes"][0]["label"] = '<script>alert("x")</script> & café'
        self.scene["notes"] = ["<img src=x onerror=alert(1)>"]
        before = copy.deepcopy(self.scene)
        result = diagram.render_html(self.scene)
        self.assertNotIn("<script>", result)
        self.assertNotIn("<img", result)
        self.assertEqual(self.scene, before)
        ET.fromstring(diagram.extract_svg(result))

    def test_unicode_wrap_keeps_characters(self):
        value = "北京系统架构ABCDEFGHIJKLMN"
        self.assertEqual("".join(diagram.wrap(value, 100, 18)), value)

    def test_extract_rejects_ambiguity(self):
        svg = diagram.render_svg(self.scene)
        with self.assertRaises(ValueError):
            diagram.extract_svg(svg + svg)

    def test_extract_keeps_case_sensitive_svg_elements(self):
        source = '<svg viewBox="0 0 20 20"><defs><linearGradient id="a"><stop offset="0"/></linearGradient></defs><text>R&amp;D&nbsp;©</text></svg>'
        root = ET.fromstring(diagram.extract_svg(source))
        self.assertIsNotNone(root.find(".//{http://www.w3.org/2000/svg}linearGradient"))

    def test_writes_preserve_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "figure.svg"
            diagram.write_file(target, "first")
            with self.assertRaises(FileExistsError):
                diagram.write_file(target, "second")
            self.assertEqual(target.read_text().strip(), "first")
            diagram.write_file(target, "second", force=True)
            self.assertEqual(target.read_text().strip(), "second")


if __name__ == "__main__":
    unittest.main()
