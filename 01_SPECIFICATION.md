# Modeling What Matters Editorial Skills
## Technical Editing — Operational Skill-Family Specification

**Specification ID:** `MWM-TE-SPEC`  
**Version:** `0.1.0-draft`  
**Corpus ID:** `MWM-TE-2026-08`  
**Status:** Draft for editorial review  
**Prepared:** August 13, 2026  
**Scope:** Technical and production-facing integrity of MWM chapter manuscripts

## 1. Purpose

Technical Editing (TE) verifies that a chapter’s structure, visual objects, numbers, cross-references, links, notes, accessibility information, and production metadata remain intelligible and correct across authoring, editing, production, and proof stages.

Its governing invariant is:

> A technical component is release-ready only when its identity, internal structure, relationship to the text, required metadata, accessibility/rights status, and production behavior are separately checked.

TE is a typed component-integrity and handoff system. Its core unit is not a sentence; it is an object or relationship that must survive editing and production.

## 2. Scope and non-goals

### In scope

- headings and hierarchy;
- tables, figures, charts, captions, legends, notes, source/credit lines, and callouts;
- cross-references, hyperlinks, and field integrity;
- acronyms and abbreviations;
- numbers, dates, percentages, measurement units, equations, and statistical notation flags;
- URLs, notes, appendices, and technical component relationships;
- accessibility and alternate-text flags;
- permissions, copyright, and credit-line flags;
- technical issue reporting, ownership, escalation, and production handoff.

### Out of scope

- developmental editing or argument restructuring;
- full grammar, syntax, spelling, punctuation, or sentence-level copyediting;
- deciding whether a statistical result or claim is substantively correct;
- deciding whether a figure supports an argument;
- legal conclusions about copyright or permission;
- final post-typesetting proof review, although TE creates checks that Proof & Post-Typesetting Review reruns;
- asserting full WCAG, PDF/UA, or accessible-DOCX conformance without a format-specific test plan.

## 3. Trigger and editorial stage

| Trigger | Mode | Purpose |
|---|---|---|
| Chapter intake | Baseline inventory | Identify components, object IDs, required metadata, and parser coverage. |
| After author revision | Incremental check | Recheck changed components and dependent callouts/cross-references. |
| Before copyedit close | Full technical edit | Validate structures, object packages, links, numbers, and handoff records. |
| Production handoff | Release check | Confirm assets, captions, permissions flags, fields, and required metadata. |
| After typesetting | Proof dependency check | Recheck numbering, cross-references, tables, figures, captions, and layout-driven defects. |
| After proof corrections | Targeted rerun | Verify each changed component and its dependencies. |

The Editorial QA & Orchestration family decides which mode runs. TE reports technical readiness; it does not independently authorize publication.

## 4. Inputs

### Required inputs

1. Current chapter file, preferably DOCX plus a rendered PDF when available.
2. MWM project/volume/chapter technical profile.
3. Active style, citation, and production rule packages where they affect technical components.
4. Figure/table asset files, captions, notes, and source/credit information.
5. Current exception and decision register.
6. Target stage and output format.

### Optional inputs

- template file;
- JATS/XML or structured content package;
- prior technical-edit reports;
- data/analysis files behind tables or charts;
- accessibility descriptions and alt-text drafts;
- permissions/licenses and rights correspondence;
- author component inventory;
- typeset proof and change list.

### Minimum run manifest

```yaml
run_id: "MWM-TE-<chapter>-<date>-<sequence>"
manuscript_file: "absolute path or managed file identifier"
manuscript_version: "author or production version"
project_profile: "MWM-TECH-v<version>"
style_registry_version: "MWM-SGI-RULES-v<version>"
stage: "intake | technical_edit | production_handoff | proof_dependency"
output_format: "docx | pdf | jats | typeset_package"
asset_manifest: "path or managed identifier"
exception_register: "path or decision-log identifier"
prior_run_id: "null or previous run"
```

## 5. Authority boundary

The corpus is stored in:

`Editorial Skills Research Corpus/03_Technical_Editing/`

Manifest: `03_Crosswalk/corpus_manifest.json`  
Source capsules: `02_Extracted_Notes/source_capsules.md`

| Tier | Authority | Use |
|---|---|---|
| 1 | MWM guidance and approved project decisions | Controls MWM component, asset, notes, caption, permission, and proof requirements. |
| 2 | MWM style, volume, chapter, and production profile | Controls adopted technical conventions and output format. |
| 3 | Delegated APA or discipline-specific notation rules | Controls only the explicit domain delegated by MWM. |
| 4 | Template/production profile | Controls assigned layout/component behavior; conflicts must be reported. |
| 5 | Structured standards such as JATS | Provide object/relationship modeling and exchange patterns. |
| 6 | Accessibility standards such as WCAG/WAI | Provide accessibility flags and design principles; do not by themselves certify Word/PDF conformance. |
| 7 | Publisher and tool documentation | Provide production examples and field behavior. |
| 8 | Model inference | Can suggest or explain; cannot infer permissions, identity, or substantive correctness. |

Chicago, JATS, WCAG, Microsoft Word, and NIST sources in the corpus are technical references and implementation exemplars. They are not automatic MWM style rules.

## 6. Preconditions

TE may claim a technical result only when:

- the output format and review stage are known;
- the current project profile is identified;
- the file parser preserves structural locations and relevant fields;
- all submitted assets are inventoried or the asset inventory is explicitly partial;
- the object package includes the available captions/notes/source/credit records;
- unresolved prior findings are imported;
- ownership is defined for style, design, accessibility, permissions, production, and proof questions.

If a required surface cannot be inspected, TE reports `coverage_partial` or `not_ready`, not `compliant`.

## 7. Family architecture

| Skill ID | Name | Primary question |
|---|---|---|
| `TE-01` | Headings and hierarchy | Is the document structure logical, complete, and technically navigable? |
| `TE-02` | Tables, figures, captions, notes | Is each visual object a complete, understandable, correctly labeled package? |
| `TE-03` | Cross-references and fields | Do visible references resolve to existing targets and update through change? |
| `TE-04` | Acronyms and abbreviations | Are terms expanded, scoped, and used consistently without damaging official names? |
| `TE-05` | Numbers, dates, percentages, notation | Are quantitative forms applied under the correct rule family without changing meaning? |
| `TE-06` | URLs, notes, appendices | Are links, note types, appendices, and component relationships intact? |
| `TE-07` | Accessibility and permissions flags | Are non-text content, table structure, alternate text, source/credit, and rights records surfaced? |
| `TE-08` | Technical report and handoff | Can a human or production vendor act on each issue with clear evidence and ownership? |

## 8. Operating principles

1. **Structure before appearance.** Inspect object type, relationships, IDs, and fields—not only visible formatting.
2. **Visual objects are composite records.** An object includes its asset, number, caption, callout, notes/legend, source/credit, permissions, accessibility, and placement.
3. **Cross-references must update.** A visible string is not enough when the workflow requires live fields or links.
4. **Quantitative notation is typed.** Distinguish numbers, variables, units, statistical symbols, labels, and ordinary prose.
5. **Ownership is explicit.** A technical editor may flag a rights or design issue without deciding it.
6. **Accessibility starts at intake.** Missing descriptions, unclear table structure, or uninformative labels should not wait for proof.
7. **Do not infer rights.** Public visibility is not permission.
8. **Do not change statistical meaning.** Apply deterministic notation rules only when the authority is clear.
9. **Preserve author data.** Never silently change a table value, chart label, equation, or figure content.
10. **Rerun dependent checks.** Any change to a target, label, number, page, or asset triggers dependent checks.

## 9. Typed technical-object registry

The object registry is the technical source of truth. It should support Word, PDF, structured XML, and proof workflows.

### Common object fields

```yaml
object_id: "FIG-003"
object_type: "figure | table | heading | appendix | note | equation | link"
label: "Figure 3"
title_or_caption: "..."
source_locator: "chapter.docx#paragraph-or-object"
callouts: ["body.p8.paragraph3"]
dependencies: ["CIT-014", "PERM-003", "ALT-003"]
status: "complete | partial | blocked | not_checked"
stage: "author | copyedit | production | proof"
```

### Figure record

```yaml
figure_id: "FIG-003"
asset_file: "figure-03.tif"
asset_version: "v2"
number: 3
caption: "..."
legend_or_key: "..."
callouts: ["Figure 3", "Fig. 3"]
source_or_credit: "..."
permission_record_id: "PERM-003"
alt_text_record_id: "ALT-003"
resolution_dpi: 300
intended_width_mm: 160
placement_state: "inline | separate | production_asset"
cross_references: []
verification: []
```

### Table record

```yaml
table_id: "TAB-002"
number: 2
title: "..."
header_structure: "simple | multi_level | unclear"
stub_structure: "simple | grouped | unclear"
data_source: "..."
notes: []
source_or_credit: "..."
alt_or_summary_record_id: "ALT-002"
callouts: ["Table 2"]
cross_references: []
verification: []
```

### Cross-reference record

```yaml
cross_reference_id: "XREF-014"
raw_text: "See Figure 3"
source_locator: "body.p8.paragraph3"
target_object_id: "FIG-003"
target_exists: true
visible_target_text: "Figure 3"
field_or_link_type: "live_field | hyperlink | static_text | unknown"
update_test: "pass | fail | not_run"
status: "verified | mismatch | broken | unresolved"
```

### Permissions/accessibility record

```yaml
permission_record_id: "PERM-003"
object_id: "FIG-003"
source: "..."
rights_status: "owned | licensed | public_domain | open_license | permission_pending | unknown"
permission_evidence: "path or correspondence identifier"
credit_line: "..."
rights_owner: "..."
alt_text_record_id: "ALT-003"
status: "verified | pending | blocked | not_applicable"
```

## 10. Procedure

### Step 0 — Initialize the technical profile

Load MWM rules, output format, stage, template/production profile, prior findings, asset manifest, and ownership map. Record whether fields, captions, hyperlinks, and cross-document references are expected to remain live.

### Step 1 — Inventory components and assets

Extract or record:

- headings and levels;
- tables and figures;
- captions, legends, table/figure notes, and source/credit lines;
- equations and statistical displays;
- callouts in the body;
- hyperlinks, URLs, and cross-references;
- acronyms and expansions;
- appendices and internal targets;
- footnotes/endnotes;
- asset files and metadata;
- permissions and alternate-text records.

Create stable object IDs. If the same object is represented in the DOCX, asset folder, and proof PDF, link the representations rather than creating unrelated records.

### Step 2 — Validate headings and hierarchy

Check:

- levels do not skip without an approved reason;
- each heading has a logical parent;
- headings are not used only to create visual size;
- repeated headings are intentional and navigable;
- required sections are present when the chapter profile requires them;
- capitalization and style are delegated to SGI;
- cross-reference targets resolve.

TE reports structure; SGI owns language/capitalization enforcement.

### Step 3 — Validate tables and figures as composite objects

For each object, check:

1. identity and sequence number;
2. title/caption presence and content;
3. in-text callout and location;
4. notes, legend/key, labels, and units;
5. source/credit and citation relationship;
6. permissions/rights record;
7. alternate text or equivalent description where required;
8. asset format, resolution, dimensions, and version;
9. placement and separation requirements;
10. consistency with other objects of the same family.

Do not modify source data or figure content. Flag content/meaning questions for Scholarly/Editorial Integrity or the author.

### Step 4 — Validate captions and fields

Prefer updateable caption fields where the production profile requires them. Check:

- caption label and number match the object;
- number sequence is current;
- caption text is present and distinct from the object title if the profile requires both;
- field code is not displayed to the reader;
- caption style and placement meet the active MWM profile;
- moving or inserting an object does not create stale numbering.

### Step 5 — Validate cross-references

For each callout or cross-reference:

1. identify the referenced object or heading;
2. verify target exists;
3. compare visible label/number to target;
4. identify field, hyperlink, static text, or unknown state;
5. run update/reorder checks where possible;
6. record cross-document limitations;
7. rerun after numbering or layout changes.

### Step 6 — Validate acronyms and abbreviations

Track first use, expansion, subsequent use, scope, and exceptions. Preserve official organization names, formal titles, direct quotations, and source-specific forms. Route style-preference questions to SGI and substantive terminology questions to Scholarly/Editorial Integrity.

### Step 7 — Validate numbers, dates, percentages, measurements, and notation

Classify the expression as:

- ordinary prose number;
- date/time;
- percentage/proportion;
- measurement with unit;
- variable or quantity symbol;
- statistical symbol or result;
- equation/formula;
- table/figure label;
- identifier or code.

Apply the highest applicable MWM/APA/discipline rule. Use NIST-style checks only for relevant measurement notation. Do not change a statistical symbol, value, decimal, or unit when the applicable authority is uncertain.

### Step 8 — Validate URLs, notes, and appendices

Check URL visibility/format and accessibility status without equating access failure with source invalidity. Verify note types, associations, numbering, and placement. Verify appendix labels, titles, internal callouts, and required metadata. RCI owns citation identity; TE owns structural placement and relationship.

### Step 9 — Validate accessibility and permissions flags

Flag missing or unclear:

- alternate text/equivalent descriptions;
- table titles and complex-table summaries;
- meaningful headings and labels;
- link purpose in context;
- source/credit lines;
- rights/permission records;
- output-format-specific accessibility metadata.

Do not assert conformance or permission without an appropriate review owner and evidence.

### Step 10 — Produce findings and handoff

Every issue receives an owner category: `style`, `technical`, `design`, `accessibility`, `rights`, `production`, `proof`, `citation`, or `substantive`. Include dependencies so changing one object triggers related checks.

### Step 11 — Apply the release gate

Release-ready requires:

- no unresolved high-severity target/cross-reference failures;
- all required tables/figures have complete object records;
- required captions, callouts, notes, sources, and credits are present;
- asset and permission/accessibility records are complete or explicitly escalated;
- fields/cross-references pass the defined update test or are accepted as static under the production profile;
- quantitative notation conflicts are resolved or routed;
- all findings have evidence, owner, status, and disposition;
- production and proof dependencies are handed forward.

## 11. Detection logic by Skill

### TE-01 — Headings and hierarchy

**Detect.** Missing/duplicate/skipped levels, orphan headings, inconsistent structural nesting, heading targets absent from navigation, and required components missing from the hierarchy.

**Do not detect as TE defects.** Capitalization or sentence/title case unless routed from SGI; substantive section order unless the project profile explicitly requires it.

### TE-02 — Tables, figures, captions, notes

**Detect.** Missing object fields, sequence gaps, absent captions/notes/legends, missing callouts, inconsistent labels, unclear table structure, incomplete source/credit, and asset metadata problems.

**Intervention.** Suggest metadata completion; never invent source, permission, data value, or caption meaning.

### TE-03 — Cross-references and fields

**Detect.** Missing targets, mismatched numbers/titles, broken fields, displayed field codes, stale static references, and cross-document references without a defined production path.

**Intervention.** Repair deterministic field/label defects when the target is certain; escalate cross-document or production-model uncertainty.

### TE-04 — Acronyms and abbreviations

**Detect.** Missing first expansion, inconsistent subsequent form, unexplained acronym in a defined scope, or abbreviation conflict with official name.

**Intervention.** Suggest expansion or consistency repair; preserve protected names and quotations.

### TE-05 — Numbers, dates, percentages, notation

**Detect.** Wrong rule family, inconsistent expression, unit-symbol errors, decimal/spacing errors under an adopted technical rule, or ambiguous statistical notation.

**Intervention.** Auto-fix only deterministic notation under a named rule. Escalate values, equations, or disciplinary symbols whose meaning could change.

### TE-06 — URLs, notes, appendices

**Detect.** Broken or malformed links, note-type mismatch, orphan notes, appendix callout/label failures, and missing structural relationships.

**Intervention.** Preserve source identity and access status; route citation issues to RCI and content completeness to Production Readiness.

### TE-07 — Accessibility and permissions

**Detect.** Missing alternate text, table explanation, meaningful label, source/credit, or rights evidence.

**Intervention.** Flag or escalate; never infer legal status or full conformance.

### TE-08 — Report and handoff

**Detect.** Findings missing object ID, owner, stage, dependency, evidence, severity, confidence, or disposition.

**Intervention.** An incomplete report cannot be a release artifact.

## 12. Intervention thresholds

| Action | Allowed when | Examples | Not allowed when |
|---|---|---|---|
| `AUTO_FIX` | Deterministic, reversible, identity-preserving, and supported by an active rule | Repair an exact field label, update a target number, normalize a defined unit symbol | It changes data, statistical meaning, source/rights status, or caption meaning |
| `SUGGEST` | Likely technical defect with low semantic risk | Add missing acronym expansion, flag absent callout, repair a clear sequence gap | Target or ownership is uncertain |
| `FLAG` | Evidence indicates a risk but no safe edit is known | Missing alt-text record, inaccessible URL, unclear table complexity | A policy/rights/design decision is needed |
| `ESCALATE` | Human/design/rights/production judgment is required | Caption placement conflict, permission status, discipline notation, cross-document fields | Never suppress unresolved dependencies |
| `BLOCK` | Technical integrity prevents responsible handoff | Broken target, missing required caption/asset, unresolved high-risk rights or field issue | Do not block on permitted design variation |

## 13. Output schema

### Run result

```yaml
run_id: "MWM-TE-chapter-20260813-01"
specification_id: "MWM-TE-SPEC"
specification_version: "0.1.0-draft"
project_profile: "MWM-TECH-v0.1"
stage: "technical_edit"
output_format: "docx"
parser_coverage: "high | partial | low"
summary:
  headings_reviewed: 0
  tables_reviewed: 0
  figures_reviewed: 0
  captions_reviewed: 0
  cross_references_reviewed: 0
  links_reviewed: 0
  findings_total: 0
  blocking_findings: 0
  escalations: 0
release_status: "ready | ready_with_conditions | not_ready"
objects: []
findings: []
handoff_dependencies: []
```

### Technical finding

```yaml
finding_id: "TE-20260813-0001"
skill_id: "TE-03"
object_id: "XREF-014"
owner_category: "technical | style | design | accessibility | rights | production | proof | citation | substantive"
rule_id: "TE-XREF-002"
severity: "critical | high | medium | low | informational"
status: "verified | needs_review | blocked | permitted | not_checked"
action: "AUTO_FIX | SUGGEST | FLAG | ESCALATE | BLOCK | CLOSE"
confidence: 0.93
location:
  file: "chapter.docx"
  locator: "body.p8.paragraph3"
  context_type: "body | heading | table | figure | caption | note | appendix | asset"
observed:
  raw_text: "See Figure 3"
  structural_state: "static_text"
expected:
  value: "live cross-reference to FIG-003"
evidence:
  - source_id: "S011"
    locator: "Microsoft Word Cross-reference"
    relevance: "field/update behavior"
dependencies: ["FIG-003", "CAP-003"]
reason: "Plain-language explanation."
proposed_change: "..."
owner: "technical editor"
decision_log_id: null
```

### Object completeness record

```yaml
object_id: "FIG-003"
object_type: "figure"
required_fields:
  asset: "pass"
  number: "pass"
  caption: "pass"
  callout: "pass"
  source_or_credit: "pass"
  permissions: "pending"
  alternate_text: "needs_review"
  resolution_and_size: "pass"
  cross_references: "pass"
overall_status: "ready_with_conditions"
dependencies: ["PERM-003", "ALT-003"]
```

## 14. Evidence requirements

Every material finding must preserve:

- exact file/asset and structural locator;
- object ID and dependent IDs;
- raw observed state;
- expected technical state;
- active rule/profile and source evidence;
- parser/tool or visual-inspection method;
- severity, confidence, action, owner, and status;
- production or proof dependency;
- human decision and evidence when escalated.

For numeric/notation findings, preserve the original value and the proposed representation. For assets, preserve filename/version and metadata. For rights/accessibility flags, preserve the evidence status without making a legal or conformance claim.

## 15. Confidence and uncertainty

| Band | Range | Typical condition | Allowed action |
|---|---:|---|---|
| High | 0.95–1.00 | Exact target/field/object match or deterministic schema violation | Close or safe repair |
| Strong | 0.80–0.94 | Clear issue with a minor format/ownership uncertainty | Suggest or routine review |
| Moderate | 0.60–0.79 | Object is identifiable but design, discipline, or output-format question remains | Flag; no automatic semantic change |
| Low | <0.60 | Missing asset, ambiguous target, unresolved rights, or incomplete parser/visual evidence | Escalate / not ready |

Lower confidence when:

- output format is not the format tested by the source standard;
- object is in a floating/anchored layout or a scanned/OCR region;
- field state cannot be inspected;
- a number or symbol could carry substantive meaning;
- permissions/accessibility evidence is absent;
- cross-document compilation behavior is unknown.

## 16. Human-escalation rules

Escalate when:

1. a technical change could alter a number, statistical symbol, equation, or data value;
2. a figure/table source or rights status is uncertain;
3. a caption or placement decision is editorially versus design-owned;
4. the output-format accessibility requirement is undefined;
5. a cross-reference crosses document/package boundaries without a defined production model;
6. a table’s complexity makes its relationships unclear;
7. a formal title, official name, quotation, or cited source term would be changed;
8. the parser cannot establish whether a field is live or static;
9. an asset’s resolution, dimensions, or transformation history is incomplete;
10. the question belongs to RCI, SGI, Copyediting, Scholarly/Editorial Integrity, Production Readiness, or Proof.

The escalation record must identify the object, evidence, owner, options, consequence, and requested decision.

## 17. Tool and model routing

| Task | Preferred capability | Model role |
|---|---|---|
| DOCX structure/field inspection | Structured document parser plus OOXML inspection | Deterministic extraction and field-state report |
| PDF visual/layout inspection | PDF renderer and page-image review | Visual confirmation; not semantic truth alone |
| Asset metadata | Image/PDF metadata tools | Deterministic dimensions, resolution, and format |
| Cross-reference graph | Rule-based object/target graph | Deterministic target resolution; model explains ambiguity |
| Tables/figures | Object registry and visual review | Model can suggest missing fields; editor confirms content/meaning |
| Numbers/units | Pattern/rule engine plus discipline-aware review | Deterministic notation checks; escalate meaning changes |
| Accessibility | Format-specific checker plus manual review | Model flags likely issues; no unsupported conformance claim |
| Permissions | Rights-record workflow | Model extracts evidence; human owner decides rights |
| Final handoff | Independent QA pass | Compare object inventory, findings, and release checklist |

## 18. QA and evaluation

Evaluation set: `04_Evaluation_Set/evaluation_set.md`  
Evaluation ID: `MWM-TE-EVAL-01`

It includes heading, table, figure, caption, field, cross-reference, table complexity, alt text, permissions, acronyms, units, numeric notation, statistical ambiguity, URLs, notes, appendices, captions, reorder regressions, and asset metadata.

### QA gates

**Gate A — object inventory**

- all in-scope objects have stable IDs;
- assets are linked to object records;
- callouts, captions, notes, sources, credits, and dependencies are inventoried;
- partial parser/asset coverage is disclosed.

**Gate B — structural integrity**

- heading hierarchy is valid;
- tables/figures/captions are sequenced and called out;
- cross-reference targets exist and match;
- fields or static-reference policy are tested.

**Gate C — quantitative/technical integrity**

- numbers/units/symbols are checked under named rules;
- no substantive data or statistical meaning has been changed;
- discipline conflicts are escalated.

**Gate D — accessibility/rights**

- alternate-text/table-description status is recorded;
- source/credit and permission records are present or escalated;
- no unsupported conformance or permission claim appears.

**Gate E — handoff**

- every finding has owner, severity, confidence, evidence, action, status, and dependency;
- unresolved blocking issues are visible;
- downstream Proof and Production Readiness dependencies are recorded.

## 19. Examples and counterexamples

### Example 1 — broken field, certain target

**Observed:** “See Figure 3” is followed by a field error, but `FIG-003` exists and is clearly identified.  
**Action:** Report field failure and repair/update the field if the production profile requires live fields.

### Counterexample 1 — target inferred from visual similarity

**Observed:** “See Figure 3” appears, but three similar figures exist and object IDs are missing.  
**Incorrect action:** Link it to the first similar figure.  
**Correct action:** Escalate and request object identification.

### Example 2 — table accessibility flag

**Observed:** A multi-level table has a title but no explanation of row/column relationships.  
**Action:** Flag a complex-table summary/structure risk and route to the accessibility/production owner.

### Counterexample 2 — formatting-only table check

**Observed:** Table has aligned borders and attractive shading.  
**Incorrect action:** Mark it accessible.  
**Correct action:** Inspect header relationships, caption/title, notes, and output-format semantics.

### Example 3 — unit notation

**Observed:** `75 cms` appears in a technical measurement context where the active rule uses SI symbols.  
**Action:** Suggest or auto-fix to `75 cm` if the rule is adopted and no meaning changes.

### Counterexample 3 — statistical rewrite

**Observed:** A model sees an unusual statistical symbol and “normalizes” it to a familiar form.  
**Incorrect action:** Replace it.  
**Correct action:** Preserve the symbol and escalate to the statistical/substantive owner.

### Example 4 — rights flag

**Observed:** A web image is publicly visible but has no rights/permission record.  
**Action:** Flag `permission_status: unknown` and assign a rights owner.

### Counterexample 4 — public URL equals permission

**Incorrect action:** Mark the image free to reuse because it is online.  
**Correct action:** Keep rights status unresolved.

### Example 5 — object move

**Observed:** Figure 2 moves before Figure 1 during production.  
**Action:** Recalculate caption numbering, callouts, cross-references, list of figures, and dependent object IDs.

### Counterexample 5 — local repair only

**Incorrect action:** Change the visible caption number but not the field, callout, or list of figures.  
**Correct action:** Run the dependency graph and update all affected surfaces.

## 20. Failure modes and mitigations

| Failure mode | Consequence | Required mitigation |
|---|---|---|
| Object inventory incomplete | Missing figures/tables/appendices go to production unnoticed | Asset and component inventory gate |
| Visual formatting treated as structure | Accessibility and cross-reference defects remain | Inspect fields, IDs, header roles, and relationships |
| Typed captions/refs become static | Numbers go stale after movement | Field-state and reorder tests |
| Table looks readable but is structurally ambiguous | Readers using alternative presentation cannot interpret it | Caption/header/summary checks |
| Permissions inferred from URL | Rights exposure | Separate rights evidence and owner |
| Alt text treated as a generic caption | Accessibility description may not convey function | Separate caption, source, and alternate-text records |
| NIST/discipline rule applied to ordinary prose | Unnecessary edits | Scope notation checks to relevant contexts |
| Statistical symbol normalized | Meaning changes | Preserve and escalate ambiguity |
| Design choice reported as editorial defect | Duplicate/conflicting work | Owner category and escalation boundary |
| Cross-document reference not tested | Book compilation breaks links | Production profile and proof dependency |
| Asset transformed without version record | Reproducibility and resolution uncertainty | Asset version/hash/metadata record |
| Report lacks dependencies | Fix creates downstream defects | Object graph and dependent recheck |

## 21. Versioning and maintenance

Use semantic versioning:

- **major** — object model, output schema, authority boundary, or intervention authority changes;
- **minor** — new component family, output format, accessibility rule, or production check;
- **patch** — wording, locator, example, or nonbehavioral correction.

Pin:

- specification version;
- MWM technical profile;
- style/citation rule versions;
- output format and template version;
- parser/field/asset tool versions;
- evaluation-set version;
- asset manifest/version;
- proof/production package identifier.

Maintenance triggers include a template change, new object type, production vendor requirement, output-format change, accessibility finding, permissions incident, cross-reference defect, or proof regression.

## 22. Release checklist

- [ ] Output format and technical stage are recorded.
- [ ] All in-scope headings, tables, figures, captions, notes, appendices, equations, links, and assets are inventoried.
- [ ] Heading hierarchy and required component structure pass.
- [ ] Tables/figures have IDs, numbers, captions/titles, callouts, notes/legends, source/credit, and dependencies.
- [ ] Cross-references resolve and field/static policy is tested.
- [ ] Acronym and abbreviation scope is checked.
- [ ] Numbers, dates, percentages, units, and statistical notation are checked under named rules.
- [ ] URLs and notes are structurally valid and routed to RCI where identity matters.
- [ ] Accessibility flags and permissions/credit records are present or escalated.
- [ ] Asset resolution/dimensions/version status is recorded where MWM requires it.
- [ ] Findings include evidence, severity, confidence, action, owner, status, and dependencies.
- [ ] No unresolved high-severity technical defect remains for handoff.
- [ ] Downstream Production Readiness and Proof dependencies are recorded.

## 23. Open decisions for editorial adjudication

The technical queue tracks:

- required fields for every MWM figure/table record;
- whether Word fields are required at author handoff;
- output-format accessibility standard and test method;
- caption/title placement;
- alt-text/long-description workflow;
- permissions owner and evidence threshold;
- adopted statistical/measurement notation;
- note types and locations;
- cross-document reference architecture;
- automatic resolution/width checks for visual assets.

These questions are intentionally not solved by external exemplars. They become enforceable when recorded in the MWM decision log, rule registry, and evaluation set.

## 24. Research basis

The specification is grounded in:

- `03_Crosswalk/corpus_manifest.json`;
- `02_Extracted_Notes/source_capsules.md`;
- `03_Crosswalk/technical_rule_crosswalk.md`;
- `03_Crosswalk/exemplar_comparison_and_gaps.md`;
- `03_Crosswalk/verification_queue.md`;
- `04_Evaluation_Set/evaluation_set.md`.

The corpus’s central synthesis is that technical editing preserves structure, meaning, navigation, accessibility, rights evidence, and production behavior through change. It is not a decorative formatting pass.

