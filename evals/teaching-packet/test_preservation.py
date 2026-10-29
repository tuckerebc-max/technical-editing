#!/usr/bin/env python3
"""Exercise output behavior, content identity and calibrated synthetic faults."""
import importlib.util
import copy
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent / "fixtures"
SCRIPT = ROOT / "scripts/teaching_packet_preservation.py"
spec = importlib.util.spec_from_file_location("preservation", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class CellReader(HTMLParser):
    """Independent readback of serialized table cells, not exporter code."""
    def __init__(self):
        super().__init__()
        self.cells, self.current = [], None
    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.current = ""
        elif tag == "br" and self.current is not None:
            self.current += "\n"
    def handle_data(self, text):
        if self.current is not None:
            self.current += text
    def handle_endtag(self, tag):
        if tag == "td":
            self.cells.append(self.current)
            self.current = None


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inv, self.assets = m.docx_inventory(FIX / "garden-packet.docx")
        self.out = self.root / "candidate"
        m.write_export(self.inv, self.assets, self.out)
        self.md = (self.out / "packet.md").read_text()

    def tearDown(self):
        self.temp.cleanup()

    def check(self, candidate):
        return m.audit(self.inv, candidate, self.out)

    def test_known_counts_and_cell_values(self):
        expected = json.loads((FIX / "expected.json").read_text())
        self.assertEqual(m.counts(self.inv), {k:expected[k] for k in m.counts(self.inv)})
        tables = [b["rows"] for b in self.inv["blocks"] if b["kind"] == "table"]
        self.assertEqual(tables[0], [["Plant","Start height (cm)","End height (cm)"],["Bean","4","10"],["Pea","6","9"]])
        self.assertEqual(tables[1][2][1], expected["answers"][1])
        self.assertEqual(sum(b.get("text") == "Explain your reasoning." for b in self.inv["blocks"]), 2)
        self.assertTrue(self.check(self.md)["pass"])

    def test_simulated_paragraph_only_baseline_fails(self):
        # Explicitly synthetic comparator, NOT an observed production failure.
        baseline = "\n\n".join(m.render_block(b) for b in self.inv["blocks"] if b["kind"] in {"heading", "paragraph"}) + "\n"
        report = self.check(baseline)
        self.assertFalse(report["pass"])
        changed = [x for x in report["issues"] if x["code"] == "missing_or_changed_object"]
        self.assertEqual([x["kind"] for x in changed], ["table", "figure", "table"])

    def test_output_cell_readback_independent_of_exporter(self):
        reader = CellReader()
        reader.feed(self.md)
        self.assertEqual(reader.cells, ["Plant","Start height (cm)","End height (cm)","Bean","4","10","Pea","6","9","Item","Worked answer","Common error","Q1","10 - 4 = 6 cm.","Subtracting in reverse order.","Q2","Bean: 6 cm; pea: 3 cm.\nBean grew 3 cm more.","Comparing final heights instead of growth."])

    def test_empty_cells_pipes_and_markup_are_literal(self):
        values = ["", "x | y", "a < b & c", "line 1\nline 2"]
        reader = CellReader()
        reader.feed(m.render_block({"kind":"table","id":"B0001","rows":[values]}))
        self.assertEqual(reader.cells, values)

    def test_missing_answer_row_detected_even_with_same_table_count(self):
        line = next(x for x in self.md.splitlines() if "10 - 4 = 6 cm." in x)
        report = self.check(self.md.replace(line, ""))
        self.assertFalse(report["pass"])
        self.assertEqual([x["kind"] for x in report["issues"] if x["code"] == "missing_or_changed_object"], ["table"])

    def test_same_count_changed_answer_detected(self):
        report = self.check(self.md.replace("10 - 4 = 6 cm.", "10 - 4 = 8 cm."))
        self.assertFalse(report["pass"])
        self.assertIn("missing_or_changed_object", [x["code"] for x in report["issues"]])

    def test_duplicate_paragraph_cardinality_and_order(self):
        block = next(b for b in self.inv["blocks"] if b.get("text") == "Explain your reasoning.")
        self.assertFalse(self.check(self.md.replace(m.render_block(block), ""))["pass"])
        reversed_text = "\n\n".join(m.render_block(b) for b in reversed(self.inv["blocks"])) + "\n"
        self.assertIn("block_order_or_membership", [x["code"] for x in self.check(reversed_text)["issues"]])

    def test_missing_and_changed_figure_asset(self):
        f = self.out / "assets/figure-001.png"
        f.unlink()
        self.assertIn("missing_or_changed_asset", [x["code"] for x in self.check(self.md)["issues"]])
        f.write_bytes(b"wrong image bytes")
        self.assertIn("missing_or_changed_asset", [x["code"] for x in self.check(self.md)["issues"]])

    def test_extra_content_and_duplicate_marker(self):
        self.assertFalse(self.check(self.md + "Unapproved extra answer\n")["pass"])
        self.assertFalse(self.check(self.md + m.render_block(self.inv["blocks"][0]))["pass"])

    def test_missing_input_cli_exits_not_ready(self):
        run = subprocess.run([sys.executable,str(SCRIPT),"docx",str(self.root / "absent.docx"),str(self.root / "absent-output")],capture_output=True,text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "not_ready")
        self.assertFalse((self.root / "absent-output").exists())

    def test_merged_table_and_track_changes_stop_before_write(self):
        for marker, insert in [("gridSpan",'<w:gridSpan w:val="2"/>'),("ins",'<w:ins w:id="1"/>')]:
            altered = self.root / (marker + ".docx")
            with ZipFile(FIX / "garden-packet.docx") as z, ZipFile(altered,"w",ZIP_DEFLATED) as out:
                for name in z.namelist():
                    data = z.read(name)
                    if name == "word/document.xml":
                        data = data.replace(b"<w:tcPr>", b"<w:tcPr>" + insert.encode(), 1)
                    out.writestr(name, data)
            run = subprocess.run([sys.executable,str(SCRIPT),"docx",str(altered),str(self.root / (marker + "-output"))],capture_output=True,text=True)
            self.assertEqual(run.returncode, 2)
            self.assertIn(marker, json.loads(run.stdout)["error"])
            self.assertFalse((self.root / (marker + "-output")).exists())

    def test_pdf_unreviewed_inventory_blocks(self):
        inv = json.loads((FIX / "pdf-inventory.unreviewed.json").read_text())
        with self.assertRaisesRegex(m.CoverageError, "named visual review"):
            m.markdown(inv)

    def test_pdf_reviewed_inventory_preserves_all_objects(self):
        inv = json.loads((FIX / "pdf-inventory.reviewed.json").read_text())
        assets = {b["asset"]:(FIX / b["asset"]).read_bytes() for b in inv["blocks"] if b["kind"] == "figure"}
        report = m.write_export(inv, assets, self.root / "pdf-candidate")
        self.assertTrue(report["pass"])
        self.assertEqual(report["source_inventory_counts"], m.counts(self.inv))

    def test_no_overwrite_or_asset_escape(self):
        with self.assertRaisesRegex(m.CoverageError, "already exists"):
            m.write_export(self.inv, self.assets, self.out)
        with self.assertRaisesRegex(m.CoverageError, "unsafe asset path"):
            m.local_file(self.root, "../outside.png")

    def test_malformed_inventory_returns_explicit_error(self):
        bad = self.root / "bad.json"
        bad.write_text("[]")
        run = subprocess.run([sys.executable,str(SCRIPT),"audit",str(bad),str(self.out / "packet.md")],capture_output=True,text=True)
        self.assertEqual(run.returncode, 2)
        self.assertIn("missing or unsupported inventory", json.loads(run.stdout)["error"])

    def reject_inventory(self, inv, expected_message):
        source = self.root / "malformed.json"
        source.write_text(json.dumps(inv))
        output = self.root / "must-not-be-created"
        run = subprocess.run([sys.executable,str(SCRIPT),"from-inventory",str(source),str(FIX),str(output)],capture_output=True,text=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)["status"], "not_ready")
        self.assertIn(expected_message, json.loads(run.stdout)["error"])
        self.assertEqual(run.stderr, "")
        self.assertFalse(output.exists())

    def test_null_block_id_is_not_ready_without_traceback(self):
        inv = copy.deepcopy(self.inv)
        inv["blocks"][0]["id"] = None
        self.reject_inventory(inv, "invalid or duplicate block identity/locator")

    def test_list_pdf_review_is_not_ready_without_traceback(self):
        inv = json.loads((FIX / "pdf-inventory.reviewed.json").read_text())
        inv["visual_inventory_review"] = []
        self.reject_inventory(inv, "visual_inventory_review must be an object")

    def test_boolean_heading_level_is_not_an_integer(self):
        inv = copy.deepcopy(self.inv)
        next(b for b in inv["blocks"] if b["kind"] == "heading")["level"] = True
        self.reject_inventory(inv, "heading level must be an integer")

    def test_related_wrong_json_types_fail_before_rendering(self):
        mutations = [
            (lambda inv: inv.update(source_kind=[]), "source_kind"),
            (lambda inv: inv.update(schema_version=True), "unsupported inventory"),
            (lambda inv: inv["blocks"][0].update(kind=[]), "kind must be a string"),
            (lambda inv: inv["blocks"][0].update(locator=[]), "identity/locator"),
            (lambda inv: next(b for b in inv["blocks"] if b["kind"] == "figure").update(sha256=None), "asset digest"),
            (lambda inv: next(b for b in inv["blocks"] if b["kind"] == "figure").update(asset=[]), "asset path string"),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message):
                inv = copy.deepcopy(self.inv)
                mutate(inv)
                self.reject_inventory(inv, message)

    def test_nonbreaking_hyphen_visible_token_is_preserved(self):
        source = self.root / "nonbreaking-hyphen.docx"
        with ZipFile(FIX / "garden-packet.docx") as z, ZipFile(source, "w", ZIP_DEFLATED) as out:
            for name in z.namelist():
                data = z.read(name)
                if name == "word/document.xml":
                    before = b"<w:t>Garden measurement packet</w:t>"
                    after = b"<w:t>Garden</w:t><w:noBreakHyphen/><w:t>measurement packet</w:t>"
                    self.assertIn(before, data)
                    data = data.replace(before, after, 1)
                out.writestr(name, data)
        output = self.root / "hyphen-output"
        run = subprocess.run([sys.executable,str(SCRIPT),"docx",str(source),str(output)],capture_output=True,text=True)
        self.assertEqual(run.returncode, 0)
        inv = json.loads((output / "inventory.json").read_text())
        self.assertEqual(inv["blocks"][0]["text"], "Garden\u2011measurement packet")
        self.assertIn("Garden\u2011measurement packet", (output / "packet.md").read_text())
        self.assertNotIn("Gardenmeasurement packet", (output / "packet.md").read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
