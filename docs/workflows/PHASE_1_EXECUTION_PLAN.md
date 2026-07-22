# Phase 1 Execution Plan — Revit-to-CDE Trace (Operator Runbook)

**Status:** Phase 1 planning
**Slice:** "Trace and verify a Revit deliverable from authoring to the CDE."
**Posture:** strictly **read-only**.

This is the technical operator runbook. For the learner-facing narrative, see
[01_REVIT_TO_CDE_TRACE.md](01_REVIT_TO_CDE_TRACE.md). Capabilities referenced here
are the confirmed read tools in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) (inventory
verified 2026-07-22).

## 1. Prerequisites

- A live Revit session (Claude Desktop) with the Harrismith model open, Revit MCP
  reachable.
- APS/Forma MCP authenticated in Claude Desktop (its own token store; never copied
  into this repository).
- This repository's schema and conventions present:
  [`schemas/phase-1-result.schema.json`](../../schemas/phase-1-result.schema.json)
  and [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md).
- A private, git-ignored workspace:
  - `.local/phase-1/raw-observations.json` — raw tool output;
  - `.local/phase-1/sanitisation-map.json` — alias ↔ real mapping.
  - `.local/` is git-ignored and must never be committed.

## 2. Read-only safeguards

- Invoke **only** confirmed read tools (Section 4).
- **Never** invoke: `create_forma_proposal`, `execute_revit_code`, `place_family`,
  `color_splash`, `clear_colors`, `prepare_native_floor_stack_preview`.
- No writes to Autodesk data; no edits to either component repository.
- `writes_require_explicit_approval` is honoured simply by never calling a write
  tool.

## 3. Tool signatures

Use the **exact MCP schemas exposed by the connected servers at execution time**.
This plan describes the *logical* order and inputs/outputs only; do not invent
parameters or assume a precise signature — inspect the live tool definition before
calling it.

## 4. Logical tool order, gates, and handling

### Stage A — Revit (Revit MCP)

| # | Tool (logical) | Input (logical) | Output used | Gate / handling |
|---|---|---|---|---|
| A1 | `get_revit_status` | — | reachability, reported status, server version if exposed | If not reachable: set `revit_observation.available=false`, add warning `REVIT_UNREACHABLE` (stage `revit`), skip A2–A5 |
| A2 | `get_revit_model_info` | — | model name/title | — |
| A3 | `list_levels` | — | level count + names | — |
| A4 | `list_revit_views` | — | view names | — |
| A5 | `get_current_view_info` / `get_current_view_elements` (optional) | — | active-view context | Optional; omit if not needed for comparison |

### Stage B — CDE locate (APS/Forma MCP)

| # | Tool (logical) | Input (logical) | Output used | Gate / handling |
|---|---|---|---|---|
| B1 | `list_autodesk_hubs` | — | hub id | If none: warning `HUB_NOT_FOUND` (stage `cde`), mark result partial/failed |
| B2 | `list_projects` | hub id | project id (Harrismith) | If not found: warning `PROJECT_NOT_FOUND` |
| B3 | `list_top_folders` | hub id, project id | deliverables folder id | — |
| B4 | `list_folder_contents` | project id, folder id | item id matching the Revit model | **Decision point:** name-based match. Descend one confirmed level at a time. Large folders are not paginated by the tool — record `FOLDER_NOT_PAGINATED` if the folder may exceed one page |
| B5 | `get_item_details` | project id, item id | item display name, tip version pointer | If not found: warning `ITEM_NOT_FOUND` |
| B6 | `list_item_versions` | project id, item id | current version number + version URN | — |

If a required CDE observation (item + current version) cannot be captured, the
result is **partial** or **failed** (Section 7).

### Stage C — Derivative (APS/Forma MCP)

| # | Tool (logical) | Input (logical) | Output used | Gate / handling |
|---|---|---|---|---|
| C1 | `get_derivative_manifest` | project id, item id | processing status | If status is not a success state: record status, warning `DERIVATIVE_NOT_READY` (stage `derivative`), **skip C2–C3**, set `properties_status=not_queried` |
| C2 | `list_model_views` | project id, item id | derivative view list | See view selection below |
| C3 | `get_model_properties` | project id, item id, selected view | allowlisted properties | See retry policy and property safety below |

**Derivative view selection (do not hardcode a view named `{3D}`):**
1. List available derivative views (C2).
2. Prefer an identifiable 3D view.
3. If several plausible candidates exist, request operator confirmation.
4. Record the chosen view with a sanitised alias (e.g. `VIEWGUID_1`) and a safe
   display label.

**Async / retry (C3):** When `get_model_properties` reports that properties are
still preparing or pending, repeat the MCP tool call using a bounded retry policy —
**at most three attempts with increasing waits**. If still pending, set
`derivative_observation.properties_status=pending` and add warning
`PROPERTIES_PENDING` (stage `derivative`). HTTP-level retry mechanics belong inside
the APS/Forma MCP component, not this reference layer.

**Property safety (C3):** Persist only an allowlist suitable for teaching:
`Category`, `Family`, `Type`, `Level`, and element/property counts. Enforce a
maximum sampled-element count (recommended: 25). **Exclude** local/cloud paths,
user names/emails, arbitrary shared/project parameter text, comments, URLs,
identifiers, and any property not required by the comparison.

### Stage D — Compare, sanitise, record (this repository)

1. Build the comparison entries (Section 5).
2. Sanitise raw observations into aliases per
   [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md); keep the
   map only in `.local/phase-1/sanitisation-map.json`.
3. Write the sanitised result JSON and validate it against the schema.

## 5. Comparison model

| Field | Revit source | CDE/derivative source | Expected result type |
|---|---|---|---|
| model/display name | A2 | B5 | `match` / `difference` |
| levels (count + names) | A3 | — | `no_equivalent` (Revit-only) |
| views | A4 | C2 | set overlap; per-field `difference`/`match` |
| current version | — | B6 | `no_equivalent` (CDE-only) |
| derivative status | — | C1 | `no_equivalent` (CDE-only) |
| selected properties | A5 (optional) | C3 | `match` / `difference` / `no_equivalent` |

Never fabricate a cross-side equivalence. Unsupported comparisons are recorded as
`no_equivalent` and, where relevant, a structured warning.

## 6. Runtime provenance

Record a `component_provenance` block for each component containing only:

- `repository_slug`;
- `inspected_revision` (`ae01d29` Revit, `befcce5` Forma);
- `runtime_worktree_state`: `clean` | `dirty` | `unknown` (a single flag — never a
  file list);
- `runtime_status`: `{ reachable, reported_status (ok|error|unavailable),
  server_version (or "unavailable") }`;
- `tools_invoked`: names of tools actually called.

Do **not** record local paths, hostnames, usernames, ports, endpoint URLs, or raw
status-response bodies. At the time of writing, the Revit MCP working tree is
`dirty` (unrelated pre-existing changes); the inventory remains pinned to
`ae01d29`.

## 7. Execution status

Set `execution.status`:

- `complete` — all acceptance criteria met (Section 8); this is the only status
  eligible to become the canonical expected-result artifact.
- `partial` — a required Revit or CDE observation is missing, or derivative
  properties remained pending.
- `failed` — Revit and/or CDE observation could not be captured at all.

Stages may degrade independently for diagnostics, but a missing required Revit or
CDE observation forces `partial` or `failed`.

## 8. Acceptance criteria

- All MCP operations were read-only (denylist untouched).
- Revit and CDE observations captured; derivative manifest status recorded.
- No private identifiers, paths, emails, or dirty-file lists committed.
- Evidence validates against
  [`schemas/phase-1-result.schema.json`](../../schemas/phase-1-result.schema.json).
- Another learner can reproduce the flow from
  [01_REVIT_TO_CDE_TRACE.md](01_REVIT_TO_CDE_TRACE.md).
- Unsupported comparisons and any pending/async results reported honestly in
  `warnings`.
- Provenance present for both components, including `runtime_worktree_state` and
  `runtime_status`.

## 9. Evidence handling

- Raw output and the alias map live in `.local/phase-1/` (git-ignored).
- Only the sanitised result JSON is committed, under
  `examples/harrismith-fire-station/expected-results/`.
- The canonical artifact is committed separately from this plan, and only when
  `execution.status` is `complete`.
