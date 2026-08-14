---
name: technical-editing
description: Validate typed technical objects and production-facing chapter integrity across headings, tables, figures, captions, fields, cross-references, acronyms, quantitative notation, URLs, notes, appendices, accessibility, permissions, assets, and handoff dependencies. Use for MWM technical-editing or production-handoff review; do not use for copyediting, SGI language enforcement, citation identity, substantive claims, legal rights decisions, or final proof review.
---

# Technical Editing

Run TE as a typed technical-object integrity and handoff workflow. Treat
`01_SPECIFICATION.md` as design authority, `02_RULES/` as the versioned
technical rule/configuration layer, `schemas/` as contracts, `evals/` as
acceptance tests, and `CHANGELOG_REGRESSION/` as the maintenance record.

## Execute

1. Load the current chapter, technical profile, output format, stage, SGI and
   RCI versions, asset manifest, exceptions, prior findings, ownership map,
   parser/tool versions, and proof or production package identifier. Validate
   `schemas/run-manifest.schema.json` before inspecting content.
2. Return `not_ready` or `partial` when the output format, stage, profile,
   parser coverage, asset inventory, object package, or ownership map is
   missing. Never call an uninspected surface compliant.
3. Inventory headings, tables, figures, captions, legends, notes, equations,
   callouts, links, cross-references, acronyms, appendices, assets, rights,
   and accessibility records. Assign stable typed object IDs and dependencies.
4. Validate headings and hierarchy without taking over SGI capitalization or
   substantive section-order decisions.
5. Validate each table or figure as a composite object: identity, sequence,
   caption/title, callout, notes/legend, units, source/credit, permissions,
   alternate text, asset metadata, placement, and dependent references.
6. Resolve cross-references and fields against object IDs. Repair only a
   deterministic identity-preserving defect when the active profile permits;
   escalate ambiguous or cross-document targets.
7. Check acronym expansion and scope; classify numbers, dates, percentages,
   measurements, variables, equations, statistical notation, labels, and
   identifiers before applying a named rule. Preserve values and meaning.
8. Check URLs, notes, appendices, asset versions, accessibility flags, and
   rights evidence. Public visibility is not permission; a flag is not a
   conformance or legal conclusion.
9. Emit complete findings and object-completeness records with raw state,
   expected state, locator, evidence, rule/version, dependency graph, owner,
   severity, confidence, action, status, and disposition.
10. Route style/capitalization to SGI, citation identity to RCI, substantive
    meaning to Scholarly/Editorial Integrity, completeness to CPR, and
    proof/production release questions to their owning families. Do not
    rewrite data, equations, figure content, or statistical symbols.
11. Apply the release gate: no unresolved high-severity target failure;
    required object records, captions, callouts, sources/credits,
    accessibility/rights statuses, field tests, and dependencies are complete
    or explicitly escalated; all findings are reproducible and owned.

## Routing

- `TE-01`: headings and hierarchy.
- `TE-02`: tables, figures, captions, notes, and object packages.
- `TE-03`: cross-references and fields.
- `TE-04`: acronyms and abbreviations.
- `TE-05`: numbers, dates, measurements, and notation.
- `TE-06`: URLs, notes, appendices, and structural relationships.
- `TE-07`: accessibility and permissions flags.
- `TE-08`: technical report and handoff.

## Boundaries

TE does not perform developmental editing, sentence-level copyediting,
style-language enforcement, citation identity verification, substantive claim
validation, legal rights decisions, full WCAG/PDF/UA/DOCX conformance claims,
or final proof review. TE may preserve upstream RCI/SGI identifiers and pass
technical findings downstream; consumers must not reinterpret a technical flag
as a substantive or legal conclusion.

## Output and acceptance

Invoke as `$technical-editing` for typed object review or production handoff.
Return a validated result using `schemas/run-result.schema.json`, with object
records, findings, completeness records, decisions, and handoff dependencies
as applicable. Use actions `AUTO_FIX`, `SUGGEST`, `FLAG`, `ESCALATE`, `BLOCK`,
or `CLOSE`. Before handoff, run `evals/scorer.py --validate-suite`,
`scripts/validate_package.py`, and the standard Codex skill validator. Clean
controls must remain clean, protected values and names must remain untouched,
unknown rights/targets must not be inferred, and unresolved MWM decisions
must remain explicit decision hooks.