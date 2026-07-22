# ADR-0003: Autodesk platform, product, and API terminology

## Status

Accepted

## Date

2026-07-22

## Context

Autodesk terminology has evolved, and the early bootstrap configuration used
"Forma" loosely as a label for capabilities such as data management,
coordination, and construction workflows. An educational reference must use
terminology that is accurate and internally consistent, and it must not teach a
distorted platform model.

Two distinct things were being conflated:

1. **Product and platform branding** — how Autodesk names the platform and its
   offerings.
2. **API maturity** — whether a given developer API is stable or beta.

These are independent concerns. A product can be well established while a related
API is beta, and vice versa.

Verified terminology (Autodesk / APS sources; terminology last verified
2026-07-22):

- Autodesk Construction Cloud has been brought into **Autodesk Forma**, and
  **Forma for Construction** is Autodesk's current umbrella for
  construction-oriented workflows on the Forma platform, described by Autodesk as
  successor terminology to Autodesk Construction Cloud
  ([Autodesk blog](https://www.autodesk.com/blogs/construction/autodesk-construction-cloud-is-now-forma/),
  [Autodesk News](https://adsknews.autodesk.com/en/news/autodesk-construction-cloud-is-now-autodesk-forma/)).
- Autodesk Platform Services (APS) is the developer API family, including the
  Data Management API and Model Derivative API
  ([APS documentation](https://aps.autodesk.com/developer/documentation),
  [Data Management v2](https://aps.autodesk.com/en/docs/data/v2),
  [Model Derivative v2](https://aps.autodesk.com/en/docs/model-derivative/v2)).

## Decision

Adopt a four-tier terminology model and apply it consistently across all
documentation and configuration. Do **not** perform a wholesale "Forma → Autodesk
Construction Cloud" relabel.

1. **Platform:** Autodesk Forma.
2. **Product / workflow offering:** Forma Data Management, Forma Build, Model
   Coordination, Forma Site Design, Design Collaboration, and related offerings.
   "Forma for Construction" is used as the current construction-oriented umbrella
   term; because exact commercial bundles may evolve, individual offerings are
   always named explicitly.
3. **Developer API family:** Autodesk Platform Services (APS), including the Data
   Management API, Model Derivative API, Issues API, Assets API, Reviews API, RFI
   API, and related APIs.
4. **Historical names:** Autodesk Construction Cloud, Autodesk Docs, Autodesk
   Build, and other former names may be documented in the glossary where
   accurate.

Additional rules:

- **API maturity is a separate concern from product branding.** Naming an API
  family is not a claim about its maturity.
- Do not infer API maturity from product maturity.
- Assert a specific maturity level (stable vs beta) only when it is verified and
  cited; otherwise mark it "to be verified".
- Record "Terminology last verified: 2026-07-22" where terminology claims are
  made, and re-verify against official Autodesk / APS sources over time.

The canonical definitions live in [GLOSSARY.md](../guides/GLOSSARY.md).

## Consequences

- Documents distinguish platform, offering, API family, and historical name, so
  a learner sees an accurate model of Autodesk's structure.
- Configuration (for example `config/workflows/end-to-end-reference.yaml`)
  separates `platform`, `primary_system`, and `api_families` fields.
- Some stages carry `mcp_implementation_status: planned` (with `api_families: []`)
  until a component tool exists, and this is expected rather than a defect.
- Verified Autodesk facts are distinguished from architectural decisions made by
  this project.
