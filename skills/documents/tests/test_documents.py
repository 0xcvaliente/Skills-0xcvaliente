import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)

import inspect_office  # noqa: E402
from _common import PackageError, find_soffice  # noqa: E402

CT = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/'
      'content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>%s</Types>')
RELS = ('<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="%s"/></Relationships>')
WNS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
SNS = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" ' \
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
PNS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
       'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
       'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
PKG_RELS = "http://schemas.openxmlformats.org/package/2006/relationships"


def make_docx(path):
    doc = (f'<w:document {WNS}><w:body>'
           '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Plan</w:t></w:r></w:p>'
           '<w:p><w:r><w:t>Hello </w:t></w:r><w:ins w:id="1" w:author="Ana" w:date="2026-01-01T00:00:00Z">'
           '<w:r><w:t>new</w:t></w:r></w:ins><w:del w:id="2" w:author="Ana" w:date="2026-01-01T00:00:00Z">'
           '<w:r><w:delText>old</w:delText></w:r></w:del></w:p>'
           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>x</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
           '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr></w:body></w:document>')
    comments = (f'<w:comments {WNS}><w:comment w:id="0" w:author="Bo" w:date="2026-01-02T00:00:00Z">'
                '<w:p><w:r><w:t>Check this</w:t></w:r></w:p></w:comment></w:comments>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT % '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>')
        z.writestr("_rels/.rels", RELS % "word/document.xml")
        z.writestr("word/document.xml", doc)
        z.writestr("word/comments.xml", comments)
        z.writestr("docProps/core.xml", '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/'
                   'metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:creator>Ana</dc:creator>'
                   '</cp:coreProperties>')


def make_xlsx(path):
    wb = (f'<workbook {SNS}><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets>'
          '<definedNames><definedName name="Total">Data!$B$3</definedName></definedNames></workbook>')
    sheet = (f'<worksheet {SNS}><dimension ref="A1:B3"/><sheetData>'
             '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><v>10</v></c></row>'
             '<row r="2"><c r="A2" t="s"><v>1</v></c><c r="B2"><f>B1*2</f></c></row>'
             '<row r="3"><c r="A3" t="s"><v>2</v></c><c r="B3" t="e"><f>B1/0</f><v>#DIV/0!</v></c></row>'
             '</sheetData></worksheet>')
    sst = f'<sst {SNS}><si><t>Revenue</t></si><si><t>Double</t></si><si><t>Ratio</t></si></sst>'
    wrels = (f'<Relationships xmlns="{PKG_RELS}"><Relationship Id="rId1" '
             'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
             'Target="worksheets/sheet1.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT % "")
        z.writestr("_rels/.rels", RELS % "xl/workbook.xml")
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wrels)
        z.writestr("xl/worksheets/sheet1.xml", sheet)
        z.writestr("xl/sharedStrings.xml", sst)


def make_pptx(path):
    pres = (f'<p:presentation {PNS}><p:sldIdLst><p:sldId id="256" r:id="rId1"/><p:sldId id="257" r:id="rId2"/>'
            '</p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/></p:presentation>')
    prels = (f'<Relationships xmlns="{PKG_RELS}">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>'
             '</Relationships>')

    def slide(title, pic=False):
        pic_xml = ('<p:pic><p:nvPicPr><p:cNvPr id="9" name="Pic" descr=""/><p:cNvPicPr/><p:nvPr/></p:nvPicPr></p:pic>'
                   if pic else "")
        return (f'<p:sld {PNS}><p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="2" name="T"/><p:cNvSpPr/>'
                '<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>' + title +
                '</a:t></a:r></a:p></p:txBody></p:sp>' + pic_xml + '</p:spTree></p:cSld></p:sld>')

    notes = (f'<p:notes {PNS}><p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="2" name="N"/><p:cNvSpPr/>'
             '<p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>Say this</a:t></a:r></a:p>'
             '</p:txBody></p:sp></p:spTree></p:cSld></p:notes>')
    s1rels = (f'<Relationships xmlns="{PKG_RELS}"><Relationship Id="rId1" '
              'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" '
              'Target="../notesSlides/notesSlide1.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT % "")
        z.writestr("_rels/.rels", RELS % "ppt/presentation.xml")
        z.writestr("ppt/presentation.xml", pres)
        z.writestr("ppt/_rels/presentation.xml.rels", prels)
        z.writestr("ppt/slides/slide1.xml", slide("Q3 results"))
        z.writestr("ppt/slides/_rels/slide1.xml.rels", s1rels)
        z.writestr("ppt/slides/slide2.xml", slide("Next steps", pic=True))
        z.writestr("ppt/notesSlides/notesSlide1.xml", notes)


class InspectTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def test_docx(self):
        p = os.path.join(self.d, "a.docx")
        make_docx(p)
        info = inspect_office.inspect(p, want_text=True)
        self.assertEqual(info["outline"], [{"level": 1, "text": "Plan"}])
        self.assertEqual(info["tracked_changes"]["insertions"], 1)
        self.assertEqual(info["tracked_changes"]["deletions"], 1)
        self.assertEqual(info["tracked_changes"]["authors"], ["Ana"])
        self.assertEqual(info["comments"][0]["text"], "Check this")
        self.assertEqual(info["tables"], 1)
        self.assertEqual(info["page"]["width_in"], 8.5)
        self.assertEqual(info["metadata"]["creator"], "Ana")
        self.assertIn("Hello", info["text"])

    def test_xlsx(self):
        p = os.path.join(self.d, "a.xlsx")
        make_xlsx(p)
        info = inspect_office.inspect(p, want_text=True)
        s = info["sheets"][0]
        self.assertEqual(s["name"], "Data")
        self.assertEqual(s["formulas"], 2)
        self.assertEqual(s["formulas_without_cached_value"], 1)
        self.assertEqual(s["error_count"], 1)
        self.assertEqual(s["errors"][0]["cell"], "B3")
        self.assertEqual(info["defined_names"], ["Total"])
        self.assertEqual(s["rows"][0]["values"], ["Revenue", "10"])

    def test_pptx(self):
        p = os.path.join(self.d, "a.pptx")
        make_pptx(p)
        info = inspect_office.inspect(p, want_text=True)
        self.assertEqual(info["slide_count"], 2)
        self.assertEqual(info["size_in"], {"width": 13.33, "height": 7.5})
        self.assertEqual([s["title"] for s in info["slides"]], ["Q3 results", "Next steps"])
        self.assertEqual(info["slides"][0]["notes"], "Say this")
        self.assertEqual(info["slides"][1]["pictures_missing_alt"], 1)

    def test_rejects_non_zip_and_entities(self):
        bad = os.path.join(self.d, "bad.docx")
        with open(bad, "wb") as f:
            f.write(b"not a zip")
        with self.assertRaises(PackageError):
            inspect_office.inspect(bad)
        evil = os.path.join(self.d, "evil.docx")
        with zipfile.ZipFile(evil, "w") as z:
            z.writestr("[Content_Types].xml", CT % "")
            z.writestr("word/document.xml",
                       '<!DOCTYPE d [<!ENTITY x "boom">]><w:document ' + WNS + '><w:body/></w:document>')
        with self.assertRaises(PackageError):
            inspect_office.inspect(evil)

    def test_cli_json(self):
        p = os.path.join(self.d, "a.xlsx")
        make_xlsx(p)
        out = subprocess.run([sys.executable, os.path.join(SCRIPTS, "inspect_office.py"), p, "--json"],
                             capture_output=True, text=True, check=True).stdout
        self.assertEqual(json.loads(out)["type"], "xlsx")


class PackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        self.tool = os.path.join(SCRIPTS, "ooxml_pack.py")

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *args, ok=True):
        r = subprocess.run([sys.executable, self.tool, *args], capture_output=True, text=True)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr)
        return r

    def test_roundtrip(self):
        src = os.path.join(self.d, "a.docx")
        make_docx(src)
        folder = os.path.join(self.d, "u")
        self.run_tool("unpack", src, folder)
        p = os.path.join(folder, "word", "document.xml")
        with open(p, encoding="utf-8") as f:
            t = f.read().replace("Hello ", "Goodbye ")
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        out = os.path.join(self.d, "b.docx")
        self.run_tool("pack", folder, out, "--original", src)
        with zipfile.ZipFile(out) as z:
            self.assertEqual(z.namelist()[0], "[Content_Types].xml")
        self.assertIn("Goodbye", inspect_office.inspect(out, want_text=True)["text"])

    def test_refuses_malformed_xml(self):
        src = os.path.join(self.d, "a.docx")
        make_docx(src)
        folder = os.path.join(self.d, "u")
        self.run_tool("unpack", src, folder)
        with open(os.path.join(folder, "word", "document.xml"), "w") as f:
            f.write("<w:document><broken>")
        r = self.run_tool("pack", folder, os.path.join(self.d, "x.docx"), ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("refusing to pack", r.stderr)

    def test_zip_slip_and_symlink(self):
        evil = os.path.join(self.d, "evil.docx")
        with zipfile.ZipFile(evil, "w") as z:
            z.writestr("[Content_Types].xml", CT % "")
            z.writestr("../escape.txt", "x")
        r = self.run_tool("unpack", evil, os.path.join(self.d, "o1"), ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertFalse(os.path.exists(os.path.join(self.d, "escape.txt")))
        link = os.path.join(self.d, "link.docx")
        with zipfile.ZipFile(link, "w") as z:
            z.writestr("[Content_Types].xml", CT % "")
            zi = zipfile.ZipInfo("word/evil")
            zi.external_attr = (0o120777 << 16)
            z.writestr(zi, "/etc/passwd")
        r = self.run_tool("unpack", link, os.path.join(self.d, "o2"), ok=False)
        self.assertNotEqual(r.returncode, 0)


class XlsxCheckTests(unittest.TestCase):
    def test_flags_errors_without_soffice(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "a.xlsx")
            make_xlsx(p)
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "xlsx_check.py"), p, "--json"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 1)
            data = json.loads(r.stdout)
            self.assertEqual(data["errors"], 1)
            self.assertEqual(data["formulas_without_cached_value"], 1)
            self.assertEqual(data["error_cells"][0]["cell"], "B3")


class PdfToolTests(unittest.TestCase):
    def setUp(self):
        try:
            import pypdf  # noqa: F401
        except ImportError:
            self.skipTest("pypdf not installed")
        self.tmp = tempfile.TemporaryDirectory()
        self.d = self.tmp.name
        from pypdf import PdfWriter
        w = PdfWriter()
        for _ in range(3):
            w.add_blank_page(width=200, height=300)
        self.src = os.path.join(self.d, "in.pdf")
        with open(self.src, "wb") as f:
            w.write(f)
        self.tool = os.path.join(SCRIPTS, "pdf_tool.py")

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, *args):
        r = subprocess.run([sys.executable, self.tool, *args], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def test_info_extract_rotate_merge_split(self):
        from pypdf import PdfReader
        info = json.loads(self.run_tool("info", self.src))
        self.assertEqual(info["pages"], 3)
        out = os.path.join(self.d, "e.pdf")
        self.run_tool("extract", self.src, out, "--pages", "1,3")
        self.assertEqual(len(PdfReader(out).pages), 2)
        rot = os.path.join(self.d, "r.pdf")
        self.run_tool("rotate", self.src, rot, "--degrees", "90", "--pages", "2")
        self.assertEqual(PdfReader(rot).pages[1].rotation, 90)
        self.assertEqual(PdfReader(rot).pages[0].rotation, 0)
        merged = os.path.join(self.d, "m.pdf")
        self.run_tool("merge", merged, self.src, out)
        self.assertEqual(len(PdfReader(merged).pages), 5)
        self.run_tool("split", self.src, os.path.join(self.d, "parts"))
        self.assertEqual(len(os.listdir(os.path.join(self.d, "parts"))), 3)

    def test_form_fields_and_fill(self):
        form = os.path.join(self.d, "form.pdf")
        objs = [
            b"<< /Type /Catalog /Pages 2 0 R /AcroForm << /Fields [4 0 R] /DA (/Helv 0 Tf 0 g) "
            b"/DR << /Font << /Helv 5 0 R >> >> >> >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 200] /Annots [4 0 R] >>",
            b"<< /Type /Annot /Subtype /Widget /FT /Tx /T (fullname) /Rect [20 100 180 120] "
            b"/P 3 0 R /DA (/Helv 12 Tf 0 g) >>",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        ]
        raw = b"%PDF-1.4\n"
        offsets = []
        for i, body in enumerate(objs, 1):
            offsets.append(len(raw))
            raw += b"%d 0 obj\n" % i + body + b"\nendobj\n"
        xref = len(raw)
        raw += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
        for off in offsets:
            raw += b"%010d 00000 n \n" % off
        raw += b"trailer\n<< /Root 1 0 R /Size %d >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
        with open(form, "wb") as f:
            f.write(raw)
        self.assertIn("fullname", self.run_tool("fields", form))
        values = os.path.join(self.d, "v.json")
        with open(values, "w") as f:
            json.dump({"fullname": "Ada Lovelace"}, f)
        out = os.path.join(self.d, "filled.pdf")
        self.run_tool("fill", form, out, "--values", values)
        from pypdf import PdfReader
        self.assertEqual(PdfReader(out).get_fields()["fullname"].get("/V"), "Ada Lovelace")
        with open(values, "w") as f:
            json.dump({"nope": "x"}, f)
        r = subprocess.run([sys.executable, self.tool, "fill", form, os.path.join(self.d, "z.pdf"), "--values", values],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unknown field", r.stderr)

    def test_fill_without_form_is_clean_error(self):
        values = os.path.join(self.d, "v.json")
        with open(values, "w") as f:
            json.dump({"a": "b"}, f)
        r = subprocess.run([sys.executable, self.tool, "fill", self.src, os.path.join(self.d, "z.pdf"), "--values", values],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("Traceback", r.stderr)

    def test_refuses_overwrite(self):
        out = os.path.join(self.d, "e.pdf")
        self.run_tool("extract", self.src, out, "--pages", "1")
        r = subprocess.run([sys.executable, self.tool, "extract", self.src, out, "--pages", "1"],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)


class DoctorTests(unittest.TestCase):
    def test_json(self):
        out = subprocess.run([sys.executable, os.path.join(SCRIPTS, "doctor.py"), "--json"],
                             capture_output=True, text=True, check=True).stdout
        data = json.loads(out)
        self.assertTrue(data["workflows"]["inspect any docx/xlsx/pptx"])
        self.assertIn("LibreOffice", data["cli"])


@unittest.skipUnless(find_soffice(), "LibreOffice not installed")
class LibreOfficeTests(unittest.TestCase):
    def test_render_docx_to_pdf(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "a.docx")
            make_docx(src)
            r = subprocess.run([sys.executable, os.path.join(SCRIPTS, "render.py"), src, "--outdir", d],
                               capture_output=True, text=True)
            if "conversion failed" in r.stderr:
                self.skipTest("LibreOffice could not open the minimal fixture: " + r.stderr[:120])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(os.path.join(d, "a.pdf")))


if __name__ == "__main__":
    unittest.main()
