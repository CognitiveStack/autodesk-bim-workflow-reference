# Repository Strategy

**Status:** Draft (Phase 0 foundations)
**Date:** 2026-07-22

This document defines how the three repositories are governed together. It is
consistent with the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md),
[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md), and
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md), and implements
[ADR-0002](../decisions/0002-multi-repo-no-submodules.md).

## 1. Repositories

- **This repository** — orchestration, documentation, educational reference.
- **Revit MCP** — `CognitiveStack/revit-mcp-triviron`.
- **APS/Forma MCP** — `CognitiveStack/autodesk-aps-forma-mcp`.

## 2. Why multi-repo, no submodules

A monorepo would couple independent release cycles and contradict
[ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md). Git
submodules add checkout friction and pin to commits that silently rot. Instead,
components are referenced by GitHub identity plus a local checkout path supplied
through environment variables. Trade-off: version alignment is managed by
documented expectations and a component inventory rather than by submodule pins.

## 3. Local wiring

Contributors clone the components separately and set:

```
FORMA_MCP_REPO=/path/to/autodesk-aps-forma-mcp
REVIT_MCP_REPO=/path/to/revit-mcp-triviron
```

These are declared as placeholders in `.env.example` and referenced in
`config/components.example.yaml`. Local `.env` and `config/local.*` files are
git-ignored.

## 4. Public-repository hygiene

This is a public educational repository. The following must never be committed:

- credentials, tokens, client IDs, client secrets, callback credentials;
- real Autodesk hub / project / folder identifiers;
- licensed Autodesk content or private project documents;
- machine-specific absolute paths.

Controls:

- `.gitignore` excludes credentials, tokens, keys, and Autodesk model binaries
  (`.rvt`, `.rfa`, `.nwc`, `.nwd`, `.ifc`, `.svf`, `.svf2`, `.dwg`, and others).
- Only synthetic, sanitised identifiers appear in examples and expected results.
- A pre-commit secret-scanning step is recommended (not yet installed; no
  dependencies are added during Phase 0).

## 5. Terminology and sourcing governance

- Terminology follows
  [ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)
  and [GLOSSARY.md](../guides/GLOSSARY.md).
- Claims about current Autodesk terminology or API maturity cite official
  Autodesk / APS sources and record "Terminology last verified: YYYY-MM-DD".
- Verified Autodesk facts are distinguished from architectural decisions made by
  this project.
- API maturity is never inferred from product maturity; use "to be verified" when
  official confirmation is unavailable.

## 6. Change control

Per the project instructions, before substantial changes:

1. Inspect the repository and Git status.
2. State the proposed files and their purpose.
3. Avoid unrelated refactoring.
4. Run relevant checks.
5. Report changed files, checks, risks, and next steps.

Writes to Autodesk data are read-only by default and require explicit approval.
Nothing is committed or pushed without separate authorisation.

## 7. Component drift and versioning

- Expected component behaviour is captured in
  [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) with capability-status labels.
- A component inventory should re-confirm those labels before each phase.
- When a component's tool surface changes, update the boundaries document and the
  capability ledger rather than pinning a submodule commit.

## 8. Licensing

This repository is licensed under the Apache License 2.0 (see `LICENSE`). The
component repositories carry their own licences; this repository does not restate
or override them.
