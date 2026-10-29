#!/usr/bin/env python3
"""Bounded DOCX -> canonical Markdown exporter and object-preservation auditor.

Python standard library only. This is not a PDF parser, general Word converter,
Markdown equivalence engine, answer-quality reviewer, or release authorizer.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

VERSION = "teaching-packet-preservation/0.1.1"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}


class CoverageError(ValueError):
    pass


def q(prefix, local):
    return "{" + NS[prefix] + "}" + local


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local_file(root, relative):
    if not isinstance(relative, str) or not relative:
        raise CoverageError("asset path must be a nonempty string")
    p = PurePosixPath(relative)
    if p.is_absolute() or ".." in p.parts or "\\" in relative:
        raise CoverageError("unsafe asset path")
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise CoverageError("asset escapes package")
    return candidate


def plain_text(element):
    out = []
    for node in element.iter():
        if node.tag == q("w", "t"):
            out.append(node.text or "")
        elif node.tag == q("w", "tab"):
            out.append("\t")
        elif node.tag in (q("w", "br"), q("w", "cr")):
            out.append("\n")
        elif node.tag == q("w", "noBreakHyphen"):
            out.append("\u2011")
    return "".join(out)


def docx_inventory(source):
    """Read body order, nonempty paragraphs, simple cells and inline raster images.

    Unsupported content fails before any output directory is created. Formatting
    inherited through styles is not interpreted; the visual review remains open.
    """
    with zipfile.ZipFile(source) as z:
        if sum(i.file_size for i in z.infolist()) > 100_000_000:
            raise CoverageError("DOCX uncompressed size exceeds 100 MB profile limit")
        names = z.namelist()
        if any(re.match(r"word/(header|footer|footnotes|endnotes|comments).*\.xml$", n) for n in names):
            raise CoverageError("headers, footers, notes or comments require a richer converter")
        root = ET.fromstring(z.read("word/document.xml"))
        unsupported = {"sdt", "altChunk", "pict", "object", "txbxContent", "hyperlink",
                       "fldSimple", "instrText", "ins", "del", "moveFrom", "moveTo",
                       "numPr", "sym", "vertAlign", "gridSpan", "vMerge", "hMerge", "gridBefore", "gridAfter",
                       "footnoteReference", "endnoteReference", "commentReference",
                       "b", "i", "u", "strike", "dstrike", "vanish", "outline", "shadow"}
        for node in root.iter():
            tag = node.tag.rsplit("}", 1)[-1]
            if (node.tag.startswith("{" + NS["w"] + "}") and tag in unsupported) or tag in {"oMath", "oMathPara", "anchor", "srcRect", "AlternateContent", "chart"}:
                raise CoverageError("unsupported DOCX feature: " + tag)
            if tag == "xfrm" and any(k in node.attrib for k in ("rot", "flipH", "flipV")):
                raise CoverageError("transformed figure requires rendered comparison")
        rels = {}
        relfile = "word/_rels/document.xml.rels"
        if relfile in names:
            for rel in ET.fromstring(z.read(relfile)):
                rels[rel.get("Id")] = rel.attrib
        blocks, assets = [], {}
        body = root.find("w:body", NS)
        if body is None:
            raise CoverageError("missing DOCX body")
        blank_paragraphs = 0
        for number, node in enumerate(body, 1):
            loc = "body/" + str(number)
            if node.tag == q("w", "sectPr"):
                continue
            if node.tag == q("w", "tbl"):
                if len(node.findall(".//w:tbl", NS)):
                    raise CoverageError("nested table requires a richer converter")
                rows = []
                for row in node.findall("w:tr", NS):
                    cells = []
                    for cell in row.findall("w:tc", NS):
                        if cell.findall(".//w:drawing", NS):
                            raise CoverageError("figure inside table requires a richer converter")
                        cells.append("\n".join(plain_text(p) for p in cell.findall("w:p", NS)))
                    rows.append(cells)
                if not rows or not rows[0] or len({len(r) for r in rows}) != 1:
                    raise CoverageError("empty or irregular table")
                blocks.append({"kind": "table", "rows": rows, "locator": loc})
            elif node.tag == q("w", "p"):
                txt = plain_text(node)
                drawings = node.findall(".//w:drawing", NS)
                if txt and drawings:
                    raise CoverageError("mixed text/figure paragraph requires a richer converter")
                if txt:
                    style = node.find("w:pPr/w:pStyle", NS)
                    style_id = style.get(q("w", "val"), "") if style is not None else ""
                    heading = re.fullmatch(r"Heading([1-6])", style_id)
                    block = {"kind": "heading" if heading else "paragraph", "text": txt, "locator": loc}
                    if heading:
                        block["level"] = int(heading[1])
                    blocks.append(block)
                elif not drawings:
                    blank_paragraphs += 1
                for drawing in drawings:
                    blips = drawing.findall(".//a:blip", NS)
                    if len(blips) != 1 or not drawing.findall(".//wp:inline", NS):
                        raise CoverageError("unsupported drawing; only one inline raster image per drawing")
                    rid = blips[0].get(q("r", "embed"))
                    rel = rels.get(rid, {})
                    target = posixpath.normpath(posixpath.join("word", rel.get("Target", "")))
                    if rel.get("TargetMode") == "External" or not target.startswith("word/media/"):
                        raise CoverageError("unresolved or external image relationship")
                    ext = PurePosixPath(target).suffix.lower()
                    if ext not in {".png", ".jpg", ".jpeg"}:
                        raise CoverageError("unsupported image format: " + ext)
                    data = z.read(target)
                    asset = "assets/figure-" + str(len(assets) + 1).zfill(3) + ext
                    assets[asset] = data
                    props = drawing.find(".//wp:docPr", NS)
                    alt = props.get("descr", "") if props is not None else ""
                    blocks.append({"kind": "figure", "asset": asset, "sha256": digest(data), "alt": alt, "locator": loc})
            else:
                raise CoverageError("unsupported body object: " + node.tag.rsplit("}", 1)[-1])
        for i, block in enumerate(blocks, 1):
            block["id"] = "B" + str(i).zfill(4)
        return {"schema_version": 1, "tool_version": VERSION, "source_name": source.name,
                "source_kind": "docx", "coverage": "supported-body-content-only",
                "ignored_blank_paragraphs": blank_paragraphs, "blocks": blocks}, assets


def validate_inventory(inv):
    if not isinstance(inv, dict) or type(inv.get("schema_version")) is not int or inv.get("schema_version") != 1 or not isinstance(inv.get("blocks"), list) or not inv["blocks"]:
        raise CoverageError("missing or unsupported inventory")
    if not isinstance(inv.get("source_kind"), str) or inv["source_kind"] not in {"docx", "pdf"}:
        raise CoverageError("source_kind must be docx or pdf")
    if inv["source_kind"] == "pdf":
        review = inv.get("visual_inventory_review", {})
        if not isinstance(review, dict):
            raise CoverageError("PDF visual_inventory_review must be an object")
        pages = review.get("pages", [])
        count = review.get("page_count")
        if type(count) is not int or count < 1 or not isinstance(pages, list) or not all(type(page) is int for page in pages) or pages != list(range(1, count + 1)) or not isinstance(review.get("reviewer"), str) or not review["reviewer"].strip() or review.get("status") != "reviewed":
            raise CoverageError("PDF inventory requires named visual review of every page")
    ids = set()
    for b in inv["blocks"]:
        if not isinstance(b, dict):
            raise CoverageError("inventory block must be an object")
        key = b.get("id", "")
        if not isinstance(key, str) or not re.fullmatch(r"B\d{4,}", key) or key in ids or not isinstance(b.get("locator"), str) or not b["locator"].strip():
            raise CoverageError("invalid or duplicate block identity/locator")
        ids.add(key)
        kind = b.get("kind")
        if not isinstance(kind, str):
            raise CoverageError("block kind must be a string")
        if kind in {"paragraph", "heading"}:
            if not isinstance(b.get("text"), str) or not b["text"]:
                raise CoverageError("missing block text")
            if kind == "heading" and (type(b.get("level")) is not int or b["level"] not in range(1, 7)):
                raise CoverageError("heading level must be an integer from 1 through 6 (not boolean)")
        elif kind == "table":
            rows = b.get("rows")
            if not isinstance(rows, list) or not rows or not all(isinstance(r, list) and r and all(isinstance(c, str) for c in r) for r in rows) or len({len(r) for r in rows}) != 1:
                raise CoverageError("table requires rectangular string cells")
        elif kind == "figure":
            if not isinstance(b.get("sha256"), str) or not re.fullmatch(r"[a-f0-9]{64}", b["sha256"]) or not isinstance(b.get("alt"), str):
                raise CoverageError("figure requires asset digest and explicit alt text (empty means unresolved)")
            if not isinstance(b.get("asset"), str) or not b["asset"]:
                raise CoverageError("figure requires a nonempty asset path string")
            local_file(Path.cwd(), b["asset"])
        else:
            raise CoverageError("unknown block kind")


def escape(text):
    # HTML in Markdown preserves literal punctuation, pipes and line breaks.
    return html.escape(text, quote=False).replace("\t", "&#9;").replace("\n", "<br>")


def render_block(b):
    kind = b["kind"]
    if kind == "paragraph":
        body = "<p>" + escape(b["text"]) + "</p>"
    elif kind == "heading":
        tag = "h" + str(b["level"])
        body = "<" + tag + ">" + escape(b["text"]) + "</" + tag + ">"
    elif kind == "table":
        # Do not invent header semantics; a separate visual/accessibility review owns them.
        body = "<table>\n" + "\n".join("<tr>" + "".join("<td>" + escape(c) + "</td>" for c in row) + "</tr>" for row in b["rows"]) + "\n</table>"
    else:
        body = '<img src="' + html.escape(b["asset"], quote=True) + '" alt="' + html.escape(b["alt"], quote=True) + '">'
    return "<!-- TE:" + b["id"] + " -->\n" + body + "\n<!-- /TE:" + b["id"] + " -->"


def markdown(inv):
    validate_inventory(inv)
    return "\n\n".join(render_block(b) for b in inv["blocks"]) + "\n"


def counts(inv):
    blocks = inv["blocks"]
    return {"text_blocks": sum(b["kind"] in {"paragraph", "heading"} for b in blocks),
            "tables": sum(b["kind"] == "table" for b in blocks),
            "table_cells": sum(sum(len(r) for r in b["rows"]) for b in blocks if b["kind"] == "table"),
            "figures": sum(b["kind"] == "figure" for b in blocks), "ordered_blocks": len(blocks)}


def audit(inv, candidate, asset_root):
    validate_inventory(inv)
    expected = markdown(inv)
    issues = []
    pattern = r"<!-- TE:(B\d+) -->\n(.*?)\n<!-- /TE:\1 -->"
    found = re.findall(pattern, candidate, re.S)
    actual_ids = [key for key, _ in found]
    expected_ids = [b["id"] for b in inv["blocks"]]
    if actual_ids != expected_ids:
        issues.append({"code": "block_order_or_membership", "expected": expected_ids, "actual": actual_ids})
    actual = dict(found)
    for b in inv["blocks"]:
        want = render_block(b).split("\n", 1)[1].rsplit("\n", 1)[0]
        if actual.get(b["id"]) != want:
            issues.append({"code": "missing_or_changed_object", "id": b["id"], "kind": b["kind"], "locator": b["locator"]})
        if b["kind"] == "figure":
            f = local_file(asset_root, b["asset"])
            if not f.is_file() or digest(f.read_bytes()) != b["sha256"]:
                issues.append({"code": "missing_or_changed_asset", "id": b["id"], "asset": b["asset"]})
    if expected != candidate and not issues:
        issues.append({"code": "noncanonical_or_extra_content", "note": "Canonical HTML-in-Markdown profile only; review formatting-only differences separately."})
    return {"tool_version": VERSION, "pass": not issues,
            "status": "preserved_within_supported_profile" if not issues else "hold",
            "source_inventory_counts": counts(inv), "issues": issues,
            "remaining_review": ["source inventory coverage", "rendered appearance and reading order", "teacher/student separation", "answer correctness and pedagogical usability"]}


def write_export(inv, assets, output):
    content = markdown(inv)
    # Verify referenced image bytes before creating output; never overwrite a package.
    for b in inv["blocks"]:
        if b["kind"] == "figure" and digest(assets.get(b["asset"], b"")) != b["sha256"]:
            raise CoverageError("inventory asset missing or changed: " + b["asset"])
    if output.exists():
        raise CoverageError("output directory already exists; choose a new staging path")
    output.mkdir(parents=True)
    for name, data in assets.items():
        dest = local_file(output, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    (output / "inventory.json").write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "packet.md").write_text(content, encoding="utf-8")
    return audit(inv, content, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    doc = sub.add_parser("docx")
    doc.add_argument("source", type=Path)
    doc.add_argument("output", type=Path)
    manual = sub.add_parser("from-inventory")
    manual.add_argument("inventory", type=Path)
    manual.add_argument("asset_root", type=Path)
    manual.add_argument("output", type=Path)
    check = sub.add_parser("audit")
    check.add_argument("inventory", type=Path)
    check.add_argument("markdown", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "docx":
            inv, assets = docx_inventory(args.source)
            report = write_export(inv, assets, args.output)
        else:
            inv = json.loads(args.inventory.read_text(encoding="utf-8"))
            validate_inventory(inv)
            if args.command == "audit":
                report = audit(inv, args.markdown.read_text(encoding="utf-8"), args.markdown.parent)
            else:
                assets = {b["asset"]: local_file(args.asset_root, b["asset"]).read_bytes() for b in inv["blocks"] if b["kind"] == "figure"}
                report = write_export(inv, assets, args.output)
        print(json.dumps(report, indent=2))
        return 0 if report["pass"] else 1
    except (CoverageError, OSError, ValueError, KeyError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(json.dumps({"pass": False, "status": "not_ready", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
