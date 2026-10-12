import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, "scripts")
STARTERS = os.path.join(ROOT, "assets", "starters")
sys.path.insert(0, SCRIPTS)
sys.path.insert(0, HERE)

import design_audit  # noqa: E402
import _design  # noqa: E402
from test_documents import CT, PNS, RELS, WNS, SNS, PKG_RELS  # noqa: E402


def has(mod):
    return importlib.util.find_spec(mod) is not None


class ContrastTests(unittest.TestCase):
    def test_known_ratios(self):
        self.assertAlmostEqual(_design.contrast_ratio("#000000", "#FFFFFF"), 21.0, places=1)
        self.assertAlmostEqual(_design.contrast_ratio("FFFFFF", "FFFFFF"), 1.0, places=2)
        self.assertLess(_design.contrast_ratio("#777777", "#FFFFFF"), 4.5)   # 4.48:1
        self.assertEqual(_design.required_ratio(11), 4.5)
        self.assertEqual(_design.required_ratio(18), 3.0)
        self.assertEqual(_design.required_ratio(14, bold=True), 3.0)

    def test_bad_hex(self):
        with self.assertRaises(ValueError):
            _design.parse_hex("blue")

    def test_every_preset_passes(self):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "contrast.py"), "--tokens"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertNotIn("FAIL", r.stdout)

    def test_cli_fail_exit(self):
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "contrast.py"), "999999", "FFFFFF", "--size", "11"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)

    def test_tokens_shape(self):
        tokens = _design.load_tokens()
        for name, p in tokens["presets"].items():
            for key in ("fonts", "colors", "chart", "type", "space", "page", "table", "media"):
                self.assertIn(key, p, f"{name} missing {key}")
            for mode in ("document", "slide", "sheet"):
                self.assertIn(mode, p["type"])
            self.assertGreaterEqual(p["type"]["slide"]["body"], 18)
            self.assertGreaterEqual(p["type"]["slide"]["footnote"], 12)


def write_zip(path, parts):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in parts.items():
            z.writestr(n, d)


class AuditFixtureTests(unittest.TestCase):
    """Bad files built by hand (no Office library needed) must be caught."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def rules(self, path):
        return {(i["severity"], i["rule"]) for i in design_audit.audit(path).items}

    def test_docx_small_low_contrast_narrow_margins(self):
        body = (f'<w:document {WNS}><w:body>'
                '<w:p><w:r><w:rPr><w:sz w:val="14"/><w:color w:val="BBBBBB"/></w:rPr><w:t>Tiny pale text</w:t></w:r></w:p>'
                '<w:p/><w:p/><w:p/>'
                '<w:sectPr><w:pgMar w:left="360" w:right="1440" w:top="1440" w:bottom="1440"/></w:sectPr>'
                '</w:body></w:document>')
        p = os.path.join(self.d, "bad.docx")
        write_zip(p, {"[Content_Types].xml": CT % "", "_rels/.rels": RELS % "word/document.xml", "word/document.xml": body})
        got = self.rules(p)
        self.assertIn(("error", "D-CONTRAST"), got)
        self.assertIn(("error", "D-MARGINS"), got)
        self.assertIn(("warn", "D-FONT-SIZE"), got)
        self.assertIn(("warn", "D-EMPTY-PARAS"), got)

    def test_docx_table_cell_shading_counts_as_background(self):
        body = (f'<w:document {WNS}><w:body><w:tbl><w:tr><w:tc><w:tcPr><w:shd w:val="clear" w:fill="1F4E79"/></w:tcPr>'
                '<w:p><w:r><w:rPr><w:color w:val="FFFFFF"/><w:sz w:val="22"/></w:rPr><w:t>Header</w:t></w:r></w:p>'
                '</w:tc></w:tr></w:tbl></w:body></w:document>')
        p = os.path.join(self.d, "ok.docx")
        write_zip(p, {"[Content_Types].xml": CT % "", "_rels/.rels": RELS % "word/document.xml", "word/document.xml": body})
        self.assertNotIn(("error", "D-CONTRAST"), self.rules(p))

    def test_pptx_small_text_offslide_wall(self):
        words = " ".join(["word"] * 100)
        sp_small = ('<p:sp><p:nvSpPr><p:cNvPr id="3" name="Box"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
                    '<p:spPr><a:xfrm><a:off x="12000000" y="0"/><a:ext cx="5000000" cy="1000000"/></a:xfrm></p:spPr>'
                    '<p:txBody><a:p><a:r><a:rPr sz="900"/><a:t>tiny</a:t></a:r></a:p></p:txBody></p:sp>')
        sp_wall = ('<p:sp><p:nvSpPr><p:cNvPr id="4" name="Wall"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:txBody><a:p><a:r>'
                   f'<a:rPr sz="2400"/><a:t>{words}</a:t></a:r></a:p></p:txBody></p:sp>')
        slide = f'<p:sld {PNS}><p:cSld><p:spTree>{sp_small}{sp_wall}</p:spTree></p:cSld></p:sld>'
        pres = (f'<p:presentation {PNS}><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>'
                '<p:sldSz cx="12192000" cy="6858000"/></p:presentation>')
        prels = (f'<Relationships xmlns="{PKG_RELS}"><Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>'
                 '</Relationships>')
        p = os.path.join(self.d, "bad.pptx")
        write_zip(p, {"[Content_Types].xml": CT % "", "_rels/.rels": RELS % "ppt/presentation.xml",
                      "ppt/presentation.xml": pres, "ppt/_rels/presentation.xml.rels": prels, "ppt/slides/slide1.xml": slide})
        got = self.rules(p)
        self.assertIn(("error", "P-FONT-SIZE"), got)
        self.assertIn(("error", "P-OFF-SLIDE"), got)
        self.assertIn(("error", "P-TEXT-DENSITY"), got)
        self.assertIn(("warn", "P-TITLE"), got)

    def test_xlsx_clipped_text_unstyled_header(self):
        wb = (f'<workbook {SNS}><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>')
        rows = ('<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
                '<row r="2"><c r="A2" t="s"><v>2</v></c><c r="B2"><v>123456.789</v></c></row>'
                '<row r="3"><c r="A3" t="s"><v>2</v></c><c r="B3"><v>234567.891</v></c></row>'
                '<row r="4"><c r="A4" t="s"><v>2</v></c><c r="B4"><v>345678.912</v></c></row>'
                '<row r="5"><c r="A5" t="s"><v>2</v></c><c r="B5"><v>456789.123</v></c></row>')
        sheet = f'<worksheet {SNS}><sheetData>{rows}</sheetData></worksheet>'
        sst = (f'<sst {SNS}><si><t>Customer name</t></si><si><t>Revenue</t></si>'
               '<si><t>A very long customer name that does not fit</t></si></sst>')
        wrels = (f'<Relationships xmlns="{PKG_RELS}"><Relationship Id="rId1" '
                 'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                 'Target="worksheets/sheet1.xml"/></Relationships>')
        p = os.path.join(self.d, "bad.xlsx")
        write_zip(p, {"[Content_Types].xml": CT % "", "_rels/.rels": RELS % "xl/workbook.xml", "xl/workbook.xml": wb,
                      "xl/_rels/workbook.xml.rels": wrels, "xl/worksheets/sheet1.xml": sheet, "xl/sharedStrings.xml": sst})
        got = self.rules(p)
        self.assertIn(("warn", "X-CLIPPED-TEXT"), got)
        self.assertIn(("warn", "X-HEADER-STYLE"), got)
        self.assertIn(("warn", "X-NUMBER-FORMAT"), got)

    def test_cli_exit_codes_and_json(self):
        p = os.path.join(self.d, "bad.docx")
        body = (f'<w:document {WNS}><w:body><w:p><w:r><w:rPr><w:color w:val="CCCCCC"/></w:rPr><w:t>x</w:t></w:r></w:p>'
                '</w:body></w:document>')
        write_zip(p, {"[Content_Types].xml": CT % "", "_rels/.rels": RELS % "word/document.xml", "word/document.xml": body})
        r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "design_audit.py"), p, "--json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertGreaterEqual(json.loads(r.stdout)["errors"], 1)


@unittest.skipUnless(all(has(m) for m in ("docx", "pptx", "openpyxl", "reportlab")),
                     "python-docx, python-pptx, openpyxl and reportlab are needed for the starter tests")
class StarterTests(unittest.TestCase):
    def test_every_starter_passes_its_own_audit(self):
        presets = _design.load_tokens()["presets"]
        medium = {"docx": "document", "pdf": "document", "xlsx": "sheet", "pptx": "slide"}
        with tempfile.TemporaryDirectory() as d:
            for name, p in presets.items():
                for kind, m in medium.items():
                    out = os.path.join(d, f"{name}.{kind}")
                    r = subprocess.run([sys.executable, os.path.join(STARTERS, f"{kind}_starter.py"), out, "--preset", name],
                                       capture_output=True, text=True)
                    if m not in p["media"]:
                        self.assertNotEqual(r.returncode, 0, f"{kind} starter should refuse {name}")
                        continue
                    self.assertEqual(r.returncode, 0, r.stderr)
                    audit = subprocess.run([sys.executable, os.path.join(SCRIPTS, "design_audit.py"), out, "--min-severity", "warn"],
                                           capture_output=True, text=True)
                    self.assertEqual(audit.returncode, 0, f"{name}.{kind}: {audit.stdout}")
                    self.assertIn("0 warning(s)", audit.stdout, f"{name}.{kind}: {audit.stdout}")


if __name__ == "__main__":
    unittest.main()
