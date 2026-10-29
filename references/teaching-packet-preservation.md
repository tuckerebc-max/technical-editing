# Teaching packet preservation during transformation

Use before DOCX/PDF-to-Markdown extraction or repackaging of an existing teaching
packet. This TE-02/TE-08 supplement checks structural/content survival. It is not
a lesson-design framework, general PDF converter, answer-quality certification,
copyedit, release receipt, or a replacement for approved-baseline proof review.

## Inputs and authority

- Identified source version and authorized scope: whole packet or an explicit
  page/section range. Preserve the source; create a separate candidate.
- Expected parts supplied by the task or source: student material, teacher
  material, activities, figure/table assets, worked answers, rubric, references.
  Do not invent missing requirements or merge unrelated manuscript lanes.
- Target Markdown consumer and whether it permits embedded HTML. The bundled
  helper emits **HTML-in-Markdown**, not portable CommonMark-only tables.
- An owner for unclear answer content, unresolved objects, and approval.

If source, scope, target renderer, or a necessary companion asset is missing,
record `not_ready` or partial coverage with the exact missing input. A filename
that says “complete” does not establish completeness. Unknown answer material
stays unknown; it must not be filled from model memory.

## Ordered workflow

1. **Inventory before extracting.** Traverse DOCX body objects in order, not only
   the paragraph collection. For PDFs, inspect every in-scope rendered page;
   text extraction/OCR is a draft, never proof that tables or figures survived.
   Record each paragraph/heading, table row and cell, figure asset, caption,
   question/item ID, answer and rubric with a source locator. Retain repeated
   text as distinct occurrences. Check for notes, floating objects, text boxes,
   merged cells, equations, image-only pages, and answers embedded inside tables.
2. **Transform without summarizing.** Preserve ordered cells, empty cells,
   line breaks inside cells, repeated prompts, units, numeric values, worked
   steps, notes and callouts. Keep each figure with its caption and descriptive
   text. A figure filename, alt text or “see figure” marker alone is not the
   figure. Keep student and teacher material clearly separated; retaining an
   answer key does not authorize distributing it to students.
3. **Compare at object level.** Count objects, but also compare exact table-cell
   strings, paragraph multiplicity/order and answer content. Equal table counts
   can conceal a lost row or changed answer. Verify each image reference opens
   the intended asset. Record a narrow result per object: preserved, changed,
   missing, unsupported or intentionally excluded with authority.
4. **Check the teaching contract.** Map every in-scope question to its supplied
   response/answer guidance or an explicit author-owned gap. Check worked steps,
   alternatives, rationale, scoring criteria and misconception notes where the
   source provides them. Independently solve simple fixture problems; route
   real substantive discrepancies to the author/domain reviewer rather than
   silently changing an answer. A preserved wrong answer is still wrong.
5. **Render and inspect both surfaces.** Check all source and output pages or
   sections for reading order, clipped/merged cells, missing symbols, image
   placement, captions and teacher/student separation. Markdown dialect support
   must be verified in the intended consumer; HTML may be stripped elsewhere.
6. **Report the bounded outcome.** Deliver the transformed content and assets,
   source-located inventory, discrepancy report, coverage/unsupported list,
   teaching-contract review and open items with owner/next action. Only say
   “complete within the agreed scope” when both object and visual checks pass
   and teaching gaps are resolved or explicitly accepted. Full-stage readiness,
   artifact/review binding, and release approval remain with their existing
   completeness/orchestration/proof owners.

## Optional deterministic helper

`scripts/teaching_packet_preservation.py` uses Python 3.9 or later and its standard library.
It exports plain DOCX body paragraphs, standard Heading1–Heading6, rectangular
unmerged tables and uncropped inline PNG/JPEG figures to a canonical `.md`
file, `inventory.json` and image assets. Cells use HTML `<td>` elements so the
helper does not invent header semantics. It normalizes presentation to HTML;
it does **not** preserve Word styles, table header/accessibility semantics,
page breaks or document metadata. Blank layout paragraphs are counted and
omitted. Visible OOXML nonbreaking-hyphen tokens are retained as U+2011. Inherited style effects require visual/semantic review.

It fails closed on detected notes, headers/footers, tracked changes, fields,
hyperlinks, lists, merged/nested tables, direct emphasis/superscript, text boxes,
floating/cropped/transformed figures and several other complex structures.
This is a bounded profile, not exhaustive OOXML feature recognition. Do not
strip these features to get a pass: switch tools and explicitly review them.

The auditor checks **this canonical format**, not semantic equivalence of
arbitrary Markdown. Benign reformatting can produce a hold; compare the cited
block before deciding whether it is content loss. It cannot prove the source
inventory is truthful, infer a missing component outside the inventory, or
bind a report to an approved current artifact. Those remain separate checks.

From the skill directory, the following safe smoke test creates an isolated
temporary package and audits it. It requires no private files and changes no
installed skill or remote state:

```bash
python -m unittest discover -s evals/teaching-packet -p 'test_*.py' -v
```

For real inputs, use the helper's `docx SOURCE.docx NEW_OUTPUT_DIRECTORY`
subcommand; then `audit INVENTORY.json CANDIDATE.md`. The output directory must
not already exist. Exit codes: `0` supported-profile preservation pass, `1`
preservation mismatch/hold, `2` missing input or unsupported/not-ready. A `0`
does not close the visual, teaching-content or release reviews printed in the
result.

### Rendering target is part of the contract

For this helper's HTML-in-Markdown payload, a tested readback route is Pandoc's
**HTML reader** to DOCX, followed by a document renderer and all-page inspection.
Select the reader explicitly: `--from=html --to=docx`; provide the candidate
directory as the resource path so the retained figures resolve. A `.md` suffix
does not choose the right reader. A synthetic negative control using Pandoc's
Markdown reader flattened table structure and omitted figures. Do not use that
route as equivalent or infer compatibility with other Markdown consumers.

The readback may need presentation-only table widths, cell spacing and a page
break before teacher material. Recheck text order, exact cells and image bytes
after such changes, then inspect every rendered page. Keep these layout changes
separate from the preservation payload. The workflow proves content survival
within a named target profile; it does not promise original Word/PDF pagination.

### PDF path

There is no bundled automatic PDF parser. Build an inventory with the same
block structure as `evals/teaching-packet/fixtures/pdf-inventory.unreviewed.json`:
paragraphs/headings, ordered string-cell matrices and separately retained figure
assets. Compare the inventory against every source page, including table/figure
boundaries, numbers, repeated text and answer keys. Only then record
`visual_inventory_review` with named reviewer, total page count, exact reviewed
page list and `status: reviewed`. These fields are a review attestation, not
machine proof. Never self-populate them merely because an extractor ran.

Use `from-inventory INVENTORY.json ASSET_ROOT NEW_OUTPUT_DIRECTORY`, then audit.
Unreadable scans, ambiguous columns, clipped content or uncertain OCR require
source clarification or specialist/manual correction. Preserve the source and
uncertainty; do not guess. The supplied reviewed fixture is evidence for its
two simple, born-digital pages only—not scans, complex tables or arbitrary PDFs.

## Failure recovery and completion

- Missing table/row/answer: return to the located source object, restore the
  complete object into a new candidate, and recheck downstream item mappings.
- Unsupported structure: choose a richer conversion method; explicitly inspect
  that object and related fields instead of broadening a pass claim.
- Counts match but content differs: inspect cell identity and order, not just
  totals. An authorized editorial change needs a separate decision record.
- Figure file exists but wrong/changed: restore the intended original asset;
  rerun the affected figure/caption/callout checks.
- Missing source/approval or denied action: stop the dependent step, retain
  completed local evidence and name the owner/action needed. Do not bypass a
  permission denial through another interface.

Before handoff, reread this scope, reopen the saved candidate and assets, rerun
the audit, and inspect its actual rendered form. Keep machine preservation,
visual review, pedagogical review and release authorization as separate states.

## Tests and applicability limits

The bundled garden fixture is entirely synthetic: student observations, two
questions, a figure, teacher answers and rubric. The paragraph-only comparator
deliberately drops both tables and the figure. It is a simulated failure, not
evidence that a past user deliverable lost them. Tests also inject same-count
answer corruption, row loss, lost repeated text, order changes, missing image
bytes, missing inputs, malformed inventory types, visible nonbreaking-hyphen tokens,
unsupported structures and an unreviewed PDF inventory.

Regenerate safe inputs with `evals/teaching-packet/build_fixture.py` only when
needed; it requires python-docx, ReportLab, Pillow, and DejaVu Sans font files
at the paths declared in the builder. Regeneration resets the PDF inventory to
unreviewed. Do not copy an earlier reviewed receipt onto a regenerated PDF.
