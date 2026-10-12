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
