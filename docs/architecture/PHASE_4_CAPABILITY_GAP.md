# Phase 4 Capability Gap — Construction Information Exchange

**Status:** Phase 4A authoritative APS capability research assessment recorded.
Outcome **`additional_authoritative_research_required`**. No Phase 4 MCP
capability is implemented, and **no implementation is authorised by this
document**.
**Research date:** 2026-07-24

This document is the authoritative repository record of the Phase 4A capability
research assessment. It records what was verified against first-party Autodesk
sources, what remains unresolved, and which candidate is **recommended for
continued investigation** — not which candidate has been selected. It is
consistent with
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md),
the [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) Phase 4A
entry gate, and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless a first-party Autodesk source is cited
for it. No endpoint path appears here that the completed research did not
support. Following the Phase 2 and Phase 3 discipline, an absent or unretrievable
source is recorded as **unresolved**, never as a negative finding.

## 1. Status and purpose

| Baseline | Value |
|---|---|
| Research date | 2026-07-24 |
| Reference-repository baseline | `cc4321a0f585662367d940ae1c9b109d4b0f3753` (`main`, clean) |
| APS/Forma MCP baseline | `75b36b2635de3a5707fd1ff3dbf5cd487e3f0e0a` |
| Registered MCP tool count | 30 (28 read-only Autodesk, 1 guarded Autodesk write, 1 local-only) |
| Current recommendation | **`additional_authoritative_research_required`** |
| Phase 4 MCP capability implemented | **None** |
| Implementation authorised by this document | **None** |

The purpose of this document is to close the *research* portion of the Phase 4A
entry gate to the extent the available sources permit, and to state precisely
which gate items remain open. It replaces no existing document and amends no
roadmap. The PRD, [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md),
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and
`config/workflows/end-to-end-reference.yaml` are unchanged by this increment.

Per the [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §14
classification discipline, the modules below move from *unassessed* only to the
extent that authoritative APS capability verification supports it. Verifying that
an API exists does **not** make a module a `planned` project capability; that is a
separate roadmap decision (§17, §19).

## 2. Source policy and retrieval limitation

### 2.1 Policy

Capability claims are supported **only** by first-party Autodesk sources. The
permitted source classes are:

- official APS Field Guides and Reference Guides;
- official APS technical announcements;
- official APS change histories;
- official Autodesk GitHub samples and Postman collections;
- official Autodesk OpenAPI specifications.

Autodesk product help may explain product workflow terminology, but is **not**
used to prove that a public API exists. No third-party source — general search
summary, AI-generated summary, forum, blog, or Stack Overflow answer — was used to
prove any capability, and no endpoint path was taken from a third-party example.

### 2.2 Retrieval limitation (load-bearing)

**The normative APS Field Guides and Reference Guides under
`aps.autodesk.com/en/docs/**` were not retrievable in the research environment.**
Those pages are client-rendered; every direct retrieval returned only an
application shell containing no documentation content, across multiple user
agents and URL variants.

Consequently:

- the endpoint inventory in this document is derived from **official Autodesk
  announcements** and **official Autodesk GitHub Postman collections**;
- both are valid first-party sources, but **neither is a substitute for the
  normative Field Guides and Reference Guides**;
- **authentication scopes, entitlement requirements, rate limits and quotas, and
  some module limitations remain unresolved** for every candidate;
- a Postman collection evidences that an endpoint existed when the collection was
  published. **It does not establish that the collection is currently complete**,
  that no endpoint has since been added or removed, or that current behaviour
  matches.

Retrieving and verifying the normative documentation is the **first** open item
in §18 and the second increment in §19.

### 2.3 Source table

| # | Source title | Source class | Date | Capability supported | Currency |
|---|---|---|---|---|---|
| S1 | *Autodesk Forma Build RFI v3 API is released* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-rfi-v3-api-released)) | Official announcement | 2025-07-23 | RFI v3 GA; base path; endpoint list; v2 deprecation; `POST /search:rfis` semantics; workflow/permission model | current |
| S2 | *Autodesk Forma Transmittals API General Availability* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-construction-cloud-transmittals-api-general-availability)) | Official announcement | 2025-12-10 | Transmittals v1 GA; five read-only operations; module ownership = Forma Data Management | current |
| S3 | *Autodesk Forma Build Submittals API General Availability* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-submittals-api-general-availability)) | Official announcement | 2024-02-22 | Submittals GA read phase (nine read-only operations); custom-numbering fields | current |
| S4 | *Autodesk Forma Submittals Write API and Updates* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-construction-cloud-submittals-write-api-and-updates)) | Official announcement | 2024-08-05 (updated 2024-08-28) | Submittals write phase; added reads incl. `GET responses`, `GET metadata`, `GET users/me` | current |
| S5 | *Autodesk Forma Build Sheets API* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-sheets-api)) | Official announcement | 2022-08-22 | Original Sheets read/write surface; 2-legged and 3-legged support; PDF source only; no Revit-view-to-sheet extraction | historical baseline, carries a 2024-11 update pointer |
| S6 | *Forma Sheet API Added Endpoints of Reading Collection* ([aps.autodesk.com](https://aps.autodesk.com/blog/acc-sheet-api-added-endpoints-reading-collection)) | Official announcement | 2024-11-27 | `GET collections`, `GET collections/:collectionId`; both `b.`-prefixed and bare project IDs accepted | current |
| S7 | *API of Exporting Forma Sheet to PDF is Released* ([aps.autodesk.com](https://aps.autodesk.com/blog/api-exporting-acc-sheet-pdf-released)) | Official announcement | 2024-08-04 | `POST exports` / `GET exports/:exportId`; asynchronous job; 1000-sheet cap; 1-hour signed URL; Export permission | current |
| S8 | ACC Transmittals API Postman collection, `autodesk-platform-services/aps-autodesk.docs.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-autodesk.docs.api-postman.collection)) | Official Autodesk GitHub collection | — | Transmittals paths; `data:read` declared; 3-legged setup instruction; `limit` 1–200, `offset`, `sort`; project ID without `b.` prefix | current for the published collection |
| S9 | ACC RFIs and Submittals API Postman collections, `autodesk-platform-services/aps-autodesk.build.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-autodesk.build.api-postman.collection)) | Official Autodesk GitHub collection | — | RFI v3 and Submittals v2 paths and methods; collection-wide scope strings; 3-legged or SSA prerequisites; pagination and filter parameters | current for the published collections |
| S10 | ACC Sheet API Postman collection, `autodesk-platform-services/aps-acc-sheet.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-acc-sheet.api-postman.collection)) | Official Autodesk GitHub collection | — | Sheets read, batch-get, upload/review, export operation inventory | current for the published collection |
| S11 | Autodesk Forma APIs overview ([aps.autodesk.com](https://aps.autodesk.com/developer/overview/forma)) | Official overview | — | Forma and Forma-related API listing consulted during the Meetings check | current |
| S12 | `autodesk-platform-services/aps-sdk-openapi` ([github.com](https://github.com/autodesk-platform-services/aps-sdk-openapi)) | Official Autodesk OpenAPI specifications | — | Consulted; contains Account Admin, Issues and Secure Service Account specifications only | current; **absence of a module here proves nothing about that module's existence** |
| S13 | APS Field Guides and Reference Guides for RFIs, Submittals, Transmittals and Sheets | **Normative Field or Reference Guide — unavailable** | — | Would supply per-endpoint scopes, entitlement, rate limits, regional limits, webhooks, response schemas | **unresolved — not retrieved** |

## 3. Governing Phase 4A entry gate

The [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §15
requires all ten items below to be satisfied **before any Phase 4A implementation
increment**:

1. authoritative APS capability verification;
2. authentication-scope verification;
3. read/write operation inventory;
4. data-model and identifier-domain analysis;
5. privacy and sanitisation planning;
6. component-boundary decision;
7. read-only-first sequencing;
8. Harrismith scenario and data readiness;
9. no unsupported writes;
10. no monolithic Forma Build API assumption.

**Every gate must pass before component implementation begins.** A research
recommendation does not satisfy a gate, and a gate is not satisfied by analogy to
another module. Verdicts are recorded in §16.

## 4. Candidate capability matrix

| Module | Official API / module name | Version | Maturity | Module ownership | Read surface | Write surface | Authentication | Repository classification |
|---|---|---|---|---|---|---|---|---|
| **RFIs** | Autodesk Forma Build RFI API (S1) | v3 | General availability, announced 2025-07-23 (S1) | Forma Build | Verified present; includes a read-semantic POST search (S1, S9) | Verified present (S1, S9) | 3-legged or SSA evidenced; per-endpoint scopes unresolved (S9, S13) | verified GA capability; candidate; **not implementation-ready** |
| **Submittals** | Autodesk Forma Build Submittals API (S3) | v2 | General availability, read phase 2024-02-22, write phase 2024-08-05 (S3, S4) | Forma Build | Verified present and broad (S3, S4, S9) | Verified present, sharing the same base path (S4, S9) | 3-legged evidenced; per-endpoint scopes unresolved (S9, S13) | verified GA capability; candidate; **not implementation-ready** |
| **Transmittals** | Autodesk Forma Transmittals API (S2) | v1 | General availability, announced 2025-12-10 (S2) | **Autodesk Forma Data Management** (S2) | Verified present; five read-only operations (S2, S8) | **No public write operation identified in the researched surface** (S2, S8) | 3-legged evidenced; `data:read` declared by the official sample; entitlement unresolved (S8, S13) | verified GA capability; **recommended candidate pending decisions**; **not yet an adopted Phase 4A module**; **not implementation-ready** |
| **Sheets** | Autodesk Forma Build Sheets API (S5) | v1 | General availability (S5, S6, S7) | Forma Build | **Genuine read surface verified present** — sheets, version sets, collections (S5, S6, S10) | Verified present, including asynchronous export creation (S5, S7, S10) | 2-legged **and** 3-legged evidenced (S5, S6) | verified GA capability with a genuine read surface; **later candidate**; **not implementation-ready** |
| **Meetings** | — | — | — | — | — | — | — | **`meetings_public_api_not_verified`** |

The four verified modules are named, versioned and statused **independently**.
There is no single "Forma Build API", and none is assumed anywhere in this
document (gate 10).

## 5. RFI v3 assessment

**Official name and version.** Autodesk Forma Build RFI API, **v3**, project-scoped
under `…/construction/rfis/v3/projects/:projectId` (S1, S9). General availability
announced 2025-07-23 (S1).

**Version history.** The announcement records that Forma RFI v2 was consolidated
with the BIM 360 RFI API in 2022 and that **v2 has since been deprecated**, and
notes that not all Forma RFI features or entity data were supported through the
BIM 360 API (S1). Any future implementation must target v3; a migration article is
referenced from the announcement.

**Hierarchy.** Project-scoped: `rfi-types`, `workflow`, `attributes`, `users/me`,
and `rfis`, with `responses`, `comments` and `attachments` nested under an
individual RFI (S1, S9).

**Read operations** (S1, S9): `GET rfi-types`, `GET workflow`, `GET users/me`,
`GET attributes`, `GET rfis/custom-identifier`, `GET rfis/:id`,
`GET rfis/:rfiId/comments`, `GET rfis/:rfiId/attachments`, and
**`POST search:rfis`**.

**Write operations** (S1, S9): `POST rfis`, `PATCH rfis/:id`,
`POST rfis/:rfiId/responses`, `PATCH rfis/:rfiId/responses/:responseId`,
`POST rfis/:rfiId/comments`, `POST attributes`, `PATCH attributes/:attributeId`.

**`POST /search:rfis` is a state-free, read-semantic operation.** The announcement
records that there is no `GET` RFI-collection endpoint in this release, and that
`POST /search:rfis` performs the search and returns all RFIs when the payload is
an empty JSON object or the filter is empty (S1). It changes no server state and
is therefore classified as a **read**.

**Permission discovery.** `GET users/me` returns the calling user's workflow roles
together with permitted actions, permitted attributes and required attributes;
`GET workflow` reflects the configured permissions (S1).

**Workflow and type reads.** `GET rfi-types` returns the types and their default
managers, reviewers and watchers; `GET workflow` returns the current workflow with
the active RFI type (S1).

**Comments and attachments.** Both are listable through `GET` operations (S1, S9).
Retrieving attachment *content* additionally involves signed-URL retrieval outside
the RFI module; only attachment **metadata** listing is in scope for a read slice.

**Unresolved** (S13): per-endpoint minimal scopes; entitlement requirements; rate
limits and quotas; regional or project-type restrictions — the permitted-status
payload contains `wfUS` and `wfEU` workflow keys (S1), which is suggestive of
region-flavoured workflows but characterises nothing; webhook availability; live
response shapes.

**Privacy risk: high.** RFI question text, official answers, response bodies and
comment threads are narrative free text, and assignees, reviewers and watchers are
identities. This is the highest leakage surface of the verified modules (§13).

**Proposed read-only chain — not approved:**

```
users/me
  → rfi-types
    → workflow
      → search:rfis
        → one RFI
          → comments
            → attachments
```

Creation, patching, responding, transitioning and upload are excluded.

**POST-as-read policy decision required.** Because listing RFIs is only possible
through `POST /search:rfis`, an RFI read slice cannot be built without permitting
a POST inside the read-only boundary. The component's existing Model Coordination
reads are documented as **GET-only with internally constructed request paths**
([COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §3.1). Permitting POST-as-read
would therefore require an **explicit repository policy decision**, recorded before
implementation — it is not an implementation detail.

## 6. Submittals v2 assessment

**Official name and version.** Autodesk Forma Build Submittals API, **v2**,
project-scoped under `…/construction/submittals/v2/projects/:projectId` (S3, S9).

**Release phases.** The read phase reached general availability on 2024-02-22 with
nine read-only operations (S3). The write phase followed on 2024-08-05, adding
write operations **and** further reads — including `GET users/me`, `GET metadata`,
`GET settings/mappings` and `GET items:next-custom-identifier` — with `GET
responses` added on 2024-08-28 (S4). Reads and writes share one base path.

**Read inventory** (S3, S4, S9): `GET items`, `GET items/:itemId`,
`GET items/:itemId/revisions`, `GET items/:itemId/attachments`, `GET item-types`,
`GET item-types/:itemTypeId`, `GET metadata`, `GET packages`,
`GET packages/:packageId`, `GET specs`, `GET specs/:specId`, `GET responses`,
`GET responses/:responseId`, `GET users/me`, `GET settings/mappings`,
`GET items/:itemId/steps`, `GET items/:itemId/steps/:stepId`,
`GET items/:itemId/steps/:stepId/tasks`,
`GET items/:itemId/steps/:stepId/tasks/:taskId`, `GET templates` (admin-only),
`GET items:next-custom-identifier`, `GET async-jobs/:asyncJobId`, and
**`POST items:validate-custom-identifier`** (a validation call with read
semantics).

**Write inventory** (S4, S9): `POST items`, `PATCH items/:itemId`,
`POST items/{itemId}:transition`, `POST specs`, `POST items/:itemId/attachments`,
`PATCH items/:itemId/attachments/:attachmentId`,
`POST …/steps/:stepId/tasks/{taskId}:close`, `POST settings/mappings`,
`DELETE settings/mappings/:mappingId`, and
`POST settings/custom-identifier:change-sequence-type`.

**Project metadata.** `GET metadata` returns project metadata for submittal roles,
user types, statuses and the custom-numbering type — global numbering versus spec
sequence numbering (S4).

**Entity coverage.** Items, item types, packages, specifications (spec sections),
responses, attachments, revisions, review steps, tasks and manager mappings are
all represented in the read surface (S3, S4, S9).

**Permission discovery.** `GET users/me` returns the calling user's submittal
permissions (S4).

**Identifier surface.** The largest of the verified modules: item, item type,
package, spec, response, step, task, attachment, manager-mapping, template and
async-job identifiers all coexist (§12).

**Pagination and filtering** (S4, S9): `limit`, `offset` and `sort` are present,
with several endpoints documenting `limit` values of 1–50 and a default of 20;
filters include `filter[packageId]`, `filter[reviewResponseId]`,
`filter[statusId]`, `filter[title]`, `filter[categoryId]`, `filter[revision]` and
`filter[isFileUploaded]`, plus a `search` term.

**Unresolved** (S13): per-endpoint minimal scopes; entitlement requirements; rate
limits; module limitations; live response shapes.

**Privacy risk: high.** Item titles and descriptions, response text, ball-in-court
users, manager mappings (person-to-role), spec section titles and attachment
filenames.

**Proposed read-only chain — not approved:**

```
users/me
  → metadata
    → items
      → one item
        → packages
          → specifications
            → responses
              → attachment metadata
```

Creation, transition, task closure, attachment upload and project-setting changes
are excluded.

## 7. Transmittals v1 assessment

**Official name and version.** Autodesk Forma Transmittals API, **v1**,
project-scoped under `…/construction/transmittals/v1/projects/:projectId`
(S2, S8). **General availability announced 2025-12-10** (S2).

**Module ownership.** The announcement describes it as "another Autodesk Forma
**Data Management**-specific API" (S2). Ownership therefore sits with **Autodesk
Forma Data Management**, not Forma Build. This is the single most consequential
fact for the roadmap decision in §17.

**Read operations — the entire researched public surface** (S2, S8):

| Operation | Purpose |
|---|---|
| `GET transmittals` | list transmittal records in a project |
| `GET transmittals/:transmittalId` | retrieve one transmittal record |
| `GET transmittals/:transmittalId/recipients` | list the recipients of a transmittal record |
| `GET transmittals/:transmittalId/folders` | list the folders associated with the file versions included in a transmittal record |
| `GET transmittals/:transmittalId/documents` | list the file versions ("documents") included in a transmittal record |

**Write surface.** **No public write operation was identified in the researched
surface.** The announcement describes this as the first phase, consisting of
read-only endpoints (S2), and the official collection contains only `GET`
operations (S8). This is a statement about the researched surface and the sources
checked, not a guarantee that no write endpoint exists or will exist.

**Scope evidence.** The official Postman collection declares **`data:read`**
(S8). Consistent with a wholly read-only surface, but the **normative minimal
scope remains unresolved** (S13).

**Project identifier.** The official collection uses the project ID **without the
`b.` prefix** (S8).

**Permission discovery.** **None.** There is no `users/me` endpoint in this module
(S2, S8). Read permission would have to be confirmed outside the API — a named
limitation, not an oversight.

**Pagination.** `limit` (documented acceptable values 1–200), `offset` (default 0)
and `sort` are present; the collection lists a default sort of `sequenceId`
descending on the transmittal collection and `name` ascending on sub-collections
(S8).

**Unresolved** (S13): entitlement requirements; normative authentication
requirements and minimal scopes; whether application-context plus impersonation is
supported (an `x-user-id` header appears in the official collection (S8), which is
**suggestive only and proves nothing about impersonation support**); rate limits;
module limitations; live response shapes.

### 7.1 Proposed evidence chain

```
TRANSMITTAL_1
  → RECIPIENT_1
    → FOLDER_1
      → VERSION_1
```

Each node belongs to a **different identifier domain**, and the aliases are not
interchangeable:

- **`TRANSMITTAL_1`** — the **Transmittals module** domain. A transmittal record
  is a record of a sharing event. It is not a Review, an RFI, a Submittal, or a
  Data Management entity.
- **`RECIPIENT_1`** — the **recipient/person** domain. A recipient identity is
  personal data (§13).
- **`FOLDER_1`** — the **Data Management folder** domain. These are the folders
  associated with the included file versions.
- **`VERSION_1`** — an **exact Data Management document version**. This is the
  same domain as the exact coordinated version proven in Phase 3
  ([PHASE_3_CAPABILITY_GAP.md](PHASE_3_CAPABILITY_GAP.md) §4) and the version
  identified in Phase 1.

Two constraints carry forward from
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md):

- **Transmittals does not itself return the stable document lineage in the
  researched surface.** The `documents` operation returns file *versions*. A
  lineage reference must not be inferred from a version, and no lineage-level
  claim may be made from this module alone.
- **Matching alias suffixes prove nothing.** `TRANSMITTAL_1`, `RECIPIENT_1`,
  `FOLDER_1` and `VERSION_1` sharing the suffix `_1` implies no identity,
  correspondence or relationship. Suffixes are per-domain counters, never
  evidence.

### 7.2 Why Transmittals is recommended for continued investigation

- The researched public surface is **entirely read-only**, so the read-only-first
  posture is structural rather than a matter of discipline.
- It is **only five operations**, the smallest credible slice of the verified
  modules.
- The evidence chain is **compact** and each hop is a single call.
- It **reuses the Data Management document-version domain already governed in
  Phases 1–3**, extending a proven identifier lineage rather than opening a new
  one, and reusing existing alias families rather than minting new ones.
- **Lower privacy risk and lower implementation complexity** than RFIs or
  Submittals — there is no long-form narrative body comparable to an RFI question
  or official answer.
- **Existing training document versions could later be reused** as the included
  documents, rather than requiring new source material to be authored.

### 7.3 Why Transmittals is not yet adopted

- Its module ownership is **Autodesk Forma Data Management**, not Forma Build,
  whereas Phase 4A is currently defined as Forma Build construction information
  exchange. Adopting it is a **roadmap decision**, not a capability finding.
- **Exact authentication scopes and entitlement requirements remain unresolved**
  (S13).
- **Component ownership has not been formally recorded** in
  [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md).
- The **alias additions in §13 are proposed only and are not approved**; no change
  has been made to
  [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md).
- **Training-project module activation and data readiness are unverified** (§14).

## 8. Sheets v1 assessment

**A genuine Sheets read surface exists.** The naive reading that this module is
confined to exports is not supported: sheets, version sets and collections are all
readable (S5, S6, S10).

**Read operations** (S5, S6, S10): `GET sheets`, `GET version-sets`,
`GET collections`, `GET collections/:collectionId`, `GET uploads`,
`GET uploads/:uploadId`, `GET uploads/:uploadId/review-sheets`,
`GET exports/:exportId`, plus the **read-semantic POST** operations
`POST sheets:batch-get`, `POST version-sets:batch-get` and
`POST uploads/:uploadId/thumbnails:batch-get`.

**Write operations** (S5, S7, S10): `POST version-sets`,
`PATCH version-sets/:versionSetId`, `POST version-sets:batch-delete`,
`POST sheets:batch-update`, `POST sheets:batch-delete`,
`POST sheets:batch-restore`, `POST storage`, `POST uploads`,
`PATCH uploads/:uploadId/review-sheets`,
`POST uploads/:uploadId/review-sheets:publish`, and **`POST exports`**.

**PDF export creation is a write.** `POST exports` initiates an asynchronous job
that runs in the background and returns an export identifier for polling (S7). It
creates server-side job state and produces a new artifact. The source sheet data
is not modified, but the operation is not state-free and is **not** classified as
a read.

**Export status is readable.** `GET exports/:exportId` returns job progress and,
on completion, the download link (S7).

**Exported signed URLs are sensitive.** The download link is an S3 signed URL
valid for one hour (S7). Signed URLs, bucket keys and object keys **must never
appear in public evidence**, in any field, note, warning or free-text string.

**Source and relationship limits** (S5): the API release supports **PDF source
only**, and the announcement records that the API does not support extracting
Revit model 2D views to sheets, naming this an explicit gap between the product
interface and the API. **No Revit-view-to-sheet source relationship is verified.**

**Other recorded constraints:** a maximum of 1000 sheets per export call,
conjoined into one PDF; the caller requires at least Export permission (S7). Both
`b.`-prefixed and bare project identifiers are accepted (S6). Markups and
hyperlinks appear in the researched surface as **export-time options only**; no
markup or hyperlink read API is verified.

**Domain separation.** These are five distinct things and are never conflated:

| Thing | Domain |
|---|---|
| Forma Build **Sheets** | this Sheets API |
| **Revit sheets** stored in an RVT file | Revit API, reached through the Revit MCP |
| **Data Management file versions** | the Phases 1–3 version domain |
| **Model Derivative views** and **derivative manifests** | the component's `list_model_views` / `get_derivative_manifest` reads |
| **Exported PDFs** | S3 artifacts produced by `POST exports` |

The component's `list_model_views` and `get_derivative_manifest` are **Model
Derivative** reads and are **not** a Sheets module
([COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §3).

**Classification: viable later read-only candidate, but not first.** The read
surface is real, but the absence of a verified Revit-source relationship separates
it from this repository's Revit-to-CDE narrative, and the module's writes sit
alongside its reads on one base path.

## 9. Meetings result

**Recorded result: `meetings_public_api_not_verified`.**

- **No authoritative public surface was located in the official sources checked** —
  official APS documentation and announcements, the official Autodesk Forma APIs
  overview (S11), the official Autodesk OpenAPI specifications (S12), and the
  official Autodesk Postman collection repositories (S8, S9, S10), which do carry
  collections for other modules.
- **This does not prove non-existence.** It establishes only that no authoritative
  public surface was verified during this research, from these sources, on
  2026-07-24.
- **No API name, version, maturity, scope, operation set or entity model is
  asserted.** Meeting records, attendees, agenda items, minutes, attachments and
  action items are therefore entirely uncharacterised here.
- Should such a surface later be verified, **meeting minutes and attendee lists
  would require synthetic-only or extremely restrictive evidence handling** — they
  would be the highest-leakage content of any module surveyed, and the default
  public-evidence policy would be full omission of narrative content (§13).

Per [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §2 and the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §14, this
leaves Meetings **unassessed for capability purposes**; it is not upgraded on the
basis of product-interface presence.

## 10. Authentication and permissions matrix

| Concern | RFI v3 | Submittals v2 | Transmittals v1 | Sheets v1 |
|---|---|---|---|---|
| Two-legged support | Not evidenced | Not evidenced | Not evidenced | **Evidenced** (S5, S6) |
| Three-legged support | Evidenced (S9) | Evidenced (S9) | Evidenced (S8) | Evidenced, and recommended by Autodesk so user permissions apply (S5) |
| SSA support | **Evidenced** — tutorial prerequisites name a 3-legged **or SSA** token (S9) | Not evidenced | Not evidenced | Not evidenced |
| Scope evidence | Collection-wide `data:read data:write data:create` (S9) | Collection-wide `data:read data:write` (S9) | Collection declares **`data:read`** (S8) | Not isolated |
| Minimal per-endpoint read scope | **unresolved** (S13) | **unresolved** (S13) | **unresolved** (S13) | **unresolved** (S13) |
| User-context requirement | **Yes** — a user-context dependency unless SSA is used | **Yes** — a user-context dependency | **Yes** — a user-context dependency | Optional; application context is permitted |
| Entitlement status | **unresolved** | **unresolved** | **unresolved** | **unresolved** |
| Role requirements | Workflow roles (creator, manager, reviewer, watcher) gate visibility and actions (S1) | Submittal roles, manager mappings, ball-in-court; `GET templates` is admin-only (S4, S9) | **unresolved**; product-side permission controls are described in product help (S2) | At least Export permission for `POST exports` (S7) |
| Permission-discovery endpoint | `GET users/me` (S1) | `GET users/me` (S4) | **None** (S2, S8) | None evidenced |
| Unresolved fields | rate limits, quotas, regional restrictions, webhooks, response shapes | rate limits, quotas, module limitations, response shapes | entitlement, impersonation support, rate limits, module limitations, response shapes | entitlement, rate limits, markup/hyperlink reads, response shapes |

Two rules govern this table:

- **A collection-wide Postman scope string does not establish a minimal
  per-endpoint scope.** The RFI collection's `data:read data:write data:create`
  covers that collection's write requests as well; nothing may be inferred from it
  about what the read subset alone requires. The same applies to the Submittals
  collection.
- **A three-legged requirement is recorded as a user-context dependency**, not an
  implementation detail. It is a gate item, because the component's existing
  verified reads have not been shown to operate under an interactive user-consent
  flow for these modules.

**Gate 2 (authentication-scope verification) remains unresolved for every viable
candidate.**

## 11. Read/write operation inventory

Classification vocabulary: **read** · **read-semantic POST** (a POST that performs
a search, batch retrieval or validation without changing server state) · **write**
· **unresolved**. No endpoint path appears here that the completed research did not
support.

### 11.1 RFI v3 — `…/construction/rfis/v3/projects/:projectId` (S1, S9)

| Operation | Method | Class |
|---|---|---|
| `rfi-types` | GET | read |
| `workflow` | GET | read |
| `users/me` | GET | read |
| `attributes` | GET | read |
| `rfis/custom-identifier` | GET | read |
| `search:rfis` | POST | **read-semantic POST** |
| `rfis/:id` | GET | read |
| `rfis/:rfiId/comments` | GET | read |
| `rfis/:rfiId/attachments` | GET | read |
| `rfis` | POST | write |
| `rfis/:id` | PATCH | write |
| `rfis/:rfiId/responses` | POST | write |
| `rfis/:rfiId/responses/:responseId` | PATCH | write |
| `rfis/:rfiId/comments` | POST | write |
| `attributes` | POST | write |
| `attributes/:attributeId` | PATCH | write |
| Webhooks | — | unresolved |

### 11.2 Submittals v2 — `…/construction/submittals/v2/projects/:projectId` (S3, S4, S9)

| Operation | Method | Class |
|---|---|---|
| `items`, `items/:itemId`, `items/:itemId/revisions`, `items/:itemId/attachments` | GET | read |
| `item-types`, `item-types/:itemTypeId` | GET | read |
| `metadata` | GET | read |
| `packages`, `packages/:packageId` | GET | read |
| `specs`, `specs/:specId` | GET | read |
| `responses`, `responses/:responseId` | GET | read |
| `users/me` | GET | read |
| `settings/mappings` | GET | read |
| `items/:itemId/steps`, `…/steps/:stepId`, `…/steps/:stepId/tasks`, `…/tasks/:taskId` | GET | read |
| `templates` (admin-only) | GET | read |
| `items:next-custom-identifier` | GET | read |
| `async-jobs/:asyncJobId` | GET | read |
| `items:validate-custom-identifier` | POST | **read-semantic POST** |
| `items` | POST | write |
| `items/:itemId` | PATCH | write |
| `items/{itemId}:transition` | POST | write |
| `specs` | POST | write |
| `items/:itemId/attachments` | POST | write |
| `items/:itemId/attachments/:attachmentId` | PATCH | write |
| `…/steps/:stepId/tasks/{taskId}:close` | POST | write |
| `settings/mappings` | POST | write |
| `settings/mappings/:mappingId` | DELETE | write |
| `settings/custom-identifier:change-sequence-type` | POST | write |
| Webhooks | — | unresolved |

### 11.3 Transmittals v1 — `…/construction/transmittals/v1/projects/:projectId` (S2, S8)

| Operation | Method | Class |
|---|---|---|
| `transmittals` | GET | read |
| `transmittals/:transmittalId` | GET | read |
| `transmittals/:transmittalId/recipients` | GET | read |
| `transmittals/:transmittalId/folders` | GET | read |
| `transmittals/:transmittalId/documents` | GET | read |
| Any write operation | — | **none identified in the researched surface** |
| Webhooks | — | unresolved |

### 11.4 Sheets v1 — `…/construction/sheets/v1/projects/:projectId` (S5, S6, S7, S10)

| Operation | Method | Class |
|---|---|---|
| `sheets` | GET | read |
| `version-sets` | GET | read |
| `collections`, `collections/:collectionId` | GET | read |
| `uploads`, `uploads/:uploadId`, `uploads/:uploadId/review-sheets` | GET | read |
| `exports/:exportId` | GET | read |
| `sheets:batch-get` | POST | **read-semantic POST** |
| `version-sets:batch-get` | POST | **read-semantic POST** |
| `uploads/:uploadId/thumbnails:batch-get` | POST | **read-semantic POST** |
| `version-sets` | POST | write |
| `version-sets/:versionSetId` | PATCH | write |
| `version-sets:batch-delete` | POST | write |
| `sheets:batch-update`, `sheets:batch-delete`, `sheets:batch-restore` | POST | write |
| `storage` | POST | write |
| `uploads` | POST | write |
| `uploads/:uploadId/review-sheets` | PATCH | write |
| `uploads/:uploadId/review-sheets:publish` | POST | write |
| `exports` | POST | **write** (creates asynchronous server-side job state) |
| Markup / hyperlink reads | — | unresolved (export-time options only in the researched surface) |

## 12. Identifier-domain matrix

| Identifier | RFI v3 | Submittals v2 | Transmittals v1 | Sheets v1 | Class |
|---|---|---|---|---|---|
| Project ID | without `b.` prefix (S9) | without `b.` prefix (S9) | without `b.` prefix (S8) | **either** `b.`-prefixed or bare (S6) | stable; **format varies by module** |
| Module record ID | `rfiId` | `itemId`, `packageId` | `transmittalId` | `sheetId`, `versionSetId`, `collectionId` | stable; **local to the module** |
| Workflow / type ID | RFI type ID, workflow ID | `itemTypeId`, template ID | — | — | stable; local |
| User ID | Autodesk ID of assignees, reviewers, watchers | Autodesk ID; manager mappings | recipient identity | — | stable; **sensitive** |
| Role / company ID | workflow roles | submittal roles, manager-mapping ID | — | — | local |
| Attachment ID | attachment ID; storage bucket/object keys for content | `attachmentId`; storage bucket/object keys | — (included items are Data Management file versions) | storage bucket/object keys for the source PDF | mixed; storage keys are **version-specific** |
| Folder URN | RFI "virtual folder" — a **module-internal** construct | — | **Data Management folder** (`…/folders`) | — | the RFI folder is **not** a Data Management folder |
| Document lineage URN | — | — | **not returned in the researched surface** | — | absent from Transmittals |
| Document-version URN | — | referenced when attaching an existing Data Management file | **Data Management file version** (`…/documents`) | — | **version-specific; the Phases 1–3 `VERSION_n` domain** |
| Display / custom identifier | RFI number, `customIdentifier` | `customIdentifier`, `customIdentifierHumanReadable` | transmittal name, `sequenceId` | sheet number, sheet title | **display-only** |

Rules, carried forward from
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and the Phase 3
version-domain constraints:

- **Display and custom identifiers are never join keys.** A
  `customIdentifierHumanReadable`, an RFI number, a sheet number or a transmittal
  `sequenceId` may be recorded as a label, never used to establish identity or a
  relationship.
- **Module record IDs are local to their modules.** An `itemId` and a
  `transmittalId` inhabit unrelated identifier spaces.
- **Transmittals `folders` and `documents` cross into Data Management domains.**
  This is the only verified crossing point among the four modules, and it is what
  allows a Transmittals chain to compose with the Phases 1–3 evidence. Transmittals
  does **not** return the stable document lineage in the researched surface, so a
  lineage-level claim cannot be made from this module alone.
- **Numeric suffixes and similar string shapes prove no relationship.** Matching
  `_1` suffixes across alias families, and identifiers that merely resemble one
  another in shape or length, are never evidence of identity or correspondence.
- **All raw identifiers remain private.** Raw IDs, URNs, GUIDs, hrefs, storage
  bucket and object keys, and signed URLs are never published in any field, note,
  warning or free-text string.

## 13. Privacy and sanitisation findings

### 13.1 Risk ordering and sensitive fields

| Rank | Module | Likely sensitive fields |
|---|---|---|
| 1 (would be highest) | **Meetings** | meeting minutes, attendee lists, agenda items, action items — **no API verified** (§9) |
| 2 | **RFIs** | question text, official answers, response bodies, comment threads, assignees, reviewers, watchers, email addresses, custom-attribute free text, attachment filenames, exact timestamps |
| 3 | **Submittals** | item titles and descriptions, response text, ball-in-court users, manager mappings, spec section titles, revision notes, attachment filenames |
| 4 | **Transmittals** | recipient identities and email addresses, transmittal name and message, included document filenames, folder paths, send timestamps |
| 5 | **Sheets** | sheet numbers and titles (which often disclose project scope), markup text, hyperlink targets, uploader identity, signed URLs and storage keys |

### 13.2 Proposed alias families — provisional only

These are **proposed for future consideration and are not approved**. No change
has been made to
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md), and none of
these tokens may be used in committed evidence until that convention is amended by
a separate, explicitly approved increment.

| Module | Proposed families |
|---|---|
| RFIs | `RFI_1`, `RFI_TYPE_1`, `RFI_WORKFLOW_1`, `RFI_RESPONSE_1`, `RFI_COMMENT_1`, `RFI_ATTACHMENT_1`, `RFI_ATTRIBUTE_1` |
| Submittals | `SUBMITTAL_1`, `SUBMITTAL_PACKAGE_1`, `SUBMITTAL_ITEM_TYPE_1`, `SUBMITTAL_RESPONSE_1`, `SUBMITTAL_STEP_1`, `SPEC_SECTION_1` |
| Transmittals | `TRANSMITTAL_1`, `RECIPIENT_1` |
| Sheets | `SHEET_1`, `SHEET_VERSION_SET_1`, `SHEET_COLLECTION_1` |
| Meetings | `MEETING_1` (reserved, unused) |

All conform to the existing token pattern `^[A-Z][A-Z0-9_]*$`. A Transmittals
chain would **reuse** the existing `FOLDER_1` and `VERSION_1` families for its
Data Management nodes rather than minting new ones — which is precisely why its
evidence composes with Phases 1–3 rather than running parallel to them.

### 13.3 Recommended public-evidence policy

- **Omit narrative free text by default** — RFI questions and answers, comment
  bodies, submittal descriptions, transmittal messages, and any future meeting
  minutes.
- **Retain sanitised categorical summaries** — status, type, role, evidence class.
- **Use counts and presence booleans** — for example a recipient count, an
  included-version count, or presence flags in the style of the Phase 3
  `lineage_reference_present` and `coordinated_version_reference_present` fields.
- **Use synthetic titles only where educationally necessary**, and only for
  records authored synthetically for that purpose.
- **Never use real project correspondence or identities.**
- **Remove email addresses entirely**; represent a person as `USER_1` or
  `RECIPIENT_1` where a reference is required.
- **Reduce timestamps to dates (`YYYY-MM-DD`) where a date is needed**, and omit
  them where the comparison does not require them.

Sanitising values must never upgrade the strength of a claim, and an empty API
result is recorded as "no matching record was returned" — never as proof that no
record exists.

## 14. Harrismith data-readiness plans

No Autodesk call was made and no live project inspection was performed. The five
readiness axes are kept **separate**, as they were in Phase 3, where capability
and data readiness blocked independently.

| Axis | RFIs | Submittals | Transmittals | Sheets |
|---|---|---|---|---|
| **API capability readiness** | verified GA (S1) | verified GA (S3, S4) | verified GA (S2) | verified GA (S5, S6, S7) |
| **Project entitlement** | unverified | unverified | unverified | unverified |
| **Project-module activation** | unverified | unverified | unverified | unverified |
| **User permission** | unverified; discoverable via `users/me` once running | unverified; discoverable via `users/me` once running | unverified; **no discovery endpoint** | unverified |
| **Actual training data** | none confirmed | none confirmed | none confirmed | none confirmed |

**Minimum synthetic data for each viable candidate**, in an explicitly approved
training project such as *Revit Forma Coordination Lab - Training*:

- **RFIs** — at least one synthetic RFI; one RFI type with an active workflow;
  optionally one comment and one attachment. No real personal or commercial
  content in the title, question or answer.
- **Submittals** — at least one synthetic submittal item; a spec section and/or
  package where the project's numbering configuration requires one; optionally one
  response and one attachment; project metadata configured.
- **Sheets** — at least one published sheet in a version set, which requires a
  source PDF. Note the recorded source limitation (§8): the training RVT models
  cannot produce a sheet through this API, so this material would have to be
  prepared separately from the Phases 1–3 data.

**Transmittals data readiness** specifically requires:

- the **Transmittals module active** in the training project;
- the **caller able to read it** — confirmed outside the API, because the module
  exposes no permission-discovery endpoint;
- **one synthetic transmittal**;
- **one approved synthetic or test recipient**;
- **one or more existing training document versions included** in that
  transmittal;
- **no API write is required to prepare the record** — a transmittal can be
  authored in the Autodesk product interface, so gate 9 is preserved.

**None of these conditions has been live-verified.** This applies to every module
in this section, including Transmittals.

## 15. Candidate scoring

The scoring below is recorded transparently as a **research aid only**. It is not
an approval mechanism, and a total does not satisfy any entry gate. Scores are
1–5, higher being better *for a first read-only slice in this repository*;
criteria marked *(simpler/lower = higher)* invert.

| Criterion | RFIs | Submittals | Transmittals | Sheets |
|---|---|---|---|---|
| Official API maturity | 5 | 5 | 5 | 5 |
| Read-only completeness | 5 | 4 | 4 | 4 |
| Documentation quality (retrievable) | 5 | 5 | 4 | 4 |
| Authentication compatibility | 4 | 4 | 4 | 5 |
| Permission complexity *(simpler = higher)* | 2 | 2 | 3 | 4 |
| Identifier complexity *(simpler = higher)* | 3 | 2 | 5 | 3 |
| Attachment dependencies *(fewer = higher)* | 3 | 3 | 5 | 3 |
| Privacy risk *(lower = higher)* | 1 | 2 | 3 | 3 |
| Likely Harrismith data availability | 3 | 3 | 4 | 2 |
| Teaching value | 5 | 4 | 5 | 2 |
| Implementation size *(smaller = higher)* | 2 | 2 | 5 | 3 |
| Machine-readable evidence-chain clarity | 3 | 3 | 5 | 3 |
| Risk of needing writes to prepare data *(lower = higher)* | 4 | 3 | 4 | 3 |
| **Total** | **45** | **42** | **56** | **44** |

Meetings is **unscored** — no verified capability exists to score (§9).

**Scoring does not itself approve a module.** Selection was explicitly not made on
API size: RFIs have by far the largest surface and do not score highest.

**Why Transmittals scored highest:** its researched public surface is entirely
read-only; it is the smallest implementation at five operations; its identifier
surface is the least ambiguous; it carries no attachment-retrieval dependency
because its included items are already Data Management file versions; its privacy
exposure is lower than the narrative-text modules; and its evidence chain
terminates in the exact document-version domain this project has already governed
and proven across three phases.

## 16. Entry-gate verdicts

| # | Gate | RFIs | Submittals | Transmittals | Sheets | Meetings |
|---|---|---|---|---|---|---|
| 1 | Authoritative APS capability verification | pass | pass | **pass** | pass | fail |
| 2 | Authentication-scope verification | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 3 | Read/write operation inventory | pass | pass | **pass** | pass | fail |
| 4 | Data-model and identifier-domain analysis | pass | pass | **pass** | pass | fail |
| 5 | Privacy and sanitisation planning | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 6 | Component-boundary decision | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 7 | Read-only-first sequencing | pass, conditional on an explicit POST-as-read policy decision (§5) | pass | **pass** | pass | fail |
| 8 | Harrismith scenario and data readiness | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 9 | No unsupported writes | pass | pass | **pass** | pass | fail |
| 10 | No monolithic Forma Build API assumption | pass | pass | **pass** | pass | pass |

Recorded explicitly:

- For **Transmittals**, gates **1, 3, 4, 7, 9 and 10 are substantially supported**
  by the research.
- Gates **2, 5, 6 and 8 remain unresolved** — for Transmittals and for every other
  candidate.
- **No candidate is implementation-ready.**
- **Implementation cannot begin while any load-bearing gate remains unresolved.**

A research recommendation is not gate approval. Nothing in §15 or §17 converts an
unresolved gate into a passed one.

## 17. Recommended candidate and pending decision

**Architecture status: `transmittals_read_slice_recommended_pending_decision`**

Transmittals is the **recommended candidate — pending roadmap, authentication,
entitlement, sanitisation, component-boundary and data-readiness decisions**.

What this status means, precisely:

- it is a **research recommendation** arising from the assessment in §7 and §15;
- it is **not a PRD amendment**, and the
  [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) is unchanged
  by this document;
- it **does not add Transmittals formally to Phase 4A**, whose declared module set
  remains RFIs, Submittals, Sheets and Meetings;
- it **does not authorise implementation**, and no MCP tool may be built on the
  strength of it;
- adopting it would require a **deliberate roadmap decision**, because its module
  ownership is **Autodesk Forma Data Management** rather than Forma Build, whereas
  Phase 4A is currently scoped as Forma Build construction information exchange.

**Preferred second candidate.** If the Transmittals recommendation is later
rejected — for example because the roadmap decision keeps Phase 4A strictly within
Forma Build — or blocked by entitlement, authentication or data readiness, then
**RFIs are the preferred second candidate**. RFIs are the strongest Forma Build
module by read-surface completeness, documentation quality and teaching value
(§5, §15), and remain the module the PRD provisionally named. Selecting RFIs would
additionally require the POST-as-read policy decision recorded in §5 and a
correspondingly stricter free-text evidence policy (§13).

## 18. Missing evidence and open questions

1. **Normative Field Guide and Reference Guide retrieval** — the load-bearing gap.
   All items below depend partly or wholly on it (S13).
2. **Minimal read scopes** — the smallest scope set each read operation actually
   requires, for each module independently.
3. **Three-legged versus SSA behaviour** — whether a Secure Service Account path is
   viable for the candidate modules, and how it interacts with project entitlement.
4. **Entitlement requirements** — what account or project entitlement each module's
   reads require.
5. **Module activation** — whether each module is active in the training project.
6. **User permission** — the calling identity's read permission, particularly for
   Transmittals, which exposes no discovery endpoint.
7. **Rate limits and quotas** — none verified for any candidate.
8. **Regional restrictions** — including what the `wfUS` / `wfEU` workflow keys
   observed in the RFI payload actually govern (S1).
9. **Webhook availability** — unverified for every candidate.
10. **Live response shapes** — no live response was observed for any module.
11. **Pagination behaviour** — parameter names and bounds are recorded from
    official collections, but envelope shape and behaviour at boundaries are
    unverified.
12. **Current project data readiness** — no synthetic record of any kind is
    confirmed to exist (§14).
13. **Component authentication compatibility** — whether the APS/Forma MCP's
    existing authentication model can carry these calls is **inferred from its
    documented design, not tested**.

## 19. Required next increments

The following sequence must be kept **separate**; research must not be combined
with component implementation, and no increment may be collapsed into another.

1. **Commit this capability-gap research document.**
2. **Retrieve and verify the normative Transmittals documentation** — the Field
   Guide and Reference Guide — and record scopes, entitlement, limitations, rate
   limits and response shapes.
3. **Make the architecture decisions**: the roadmap decision (whether a Forma Data
   Management module may lead Phase 4A), the component-boundary decision, and the
   sanitisation decision on the proposed alias families.
4. **Amend the [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md)
   and [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) only if Transmittals is
   adopted** — and only after step 3.
5. **Create the Phase 4 result schema and execution plan.**
6. **Implement the MCP reads separately**, in the component repository, per
   [ADR-0002](../decisions/0002-multi-repo-no-submodules.md).
7. **Capture private live evidence** under the git-ignored `.local/` boundary.
8. **Publish sanitised evidence separately**, validated against the Phase 4 schema.

Steps 5 onward are conditional on every load-bearing gate in §16 being resolved.
