# 03 · Model Coordination-to-Issue Trace

A learner-facing walkthrough of the third vertical slice in the Autodesk BIM
Workflow Reference Implementation. It explains *why* coordination matters and what
a narrow, honest coordination-to-issue trace would prove. For the operator runbook
see [PHASE_3_EXECUTION_PLAN.md](PHASE_3_EXECUTION_PLAN.md); for the capability and
data blockers see
[PHASE_3_CAPABILITY_GAP.md](../architecture/PHASE_3_CAPABILITY_GAP.md).

The example project is the synthetic **Harrismith Fire Station**. Phase 3 is
strictly read-only: no model is uploaded or published, no coordination is run, no
issue is created or changed.

> **Status:** the Phase 3C read-only inspection has been **completed**. It proves a
> **shared model context** — `shared_model_context_proven` — between a coordination
> issue and the participating documents of a coordination snapshot (see below).
> Clash-level reads stay deferred, so a direct clash-to-issue link and any resolution
> claim remain **not established**. No issue was created. The sanitised public
> Phase 3 evidence artifact **is committed** at
> `examples/harrismith-fire-station/expected-results/model-coordination-to-issue-trace.result.json`.

## What Model Coordination does

When several disciplines each author their own model — architecture, structure,
mechanical, and so on — those models must be checked against one another. Autodesk
**Model Coordination** aggregates the discipline models into a **model set**,
processes them, and reports **clashes**: places where, for example, a structural
beam and a mechanical duct occupy the same space. Teams then raise **coordination
issues** to assign and resolve those conflicts, and re-check after the models are
revised.

## The conceptual flow

```
discipline model versions   (e.g. structural, mechanical)
  → coordination model set    (the aggregation that is checked)
    → clash result             (a specific conflict)
      → clash identity/group    (how the conflict is tracked)
        → coordination issue     (who fixes it, and its status)
          → revised model version (the fix)
            → clash recheck        (is the conflict gone?)
```

Every arrow is a claim that must be **proven by API evidence**, not assumed.

## The synthetic teaching scenario

For teaching only — **not** proven live evidence — imagine:

- **HFS-STR** (structural) contains a beam;
- **HFS-MEC** (mechanical) contains a duct;
- the two overlap → a **coordination clash**;
- a **coordination issue** ("clarify/relocate the duct") is raised and assigned to
  the mechanical discipline;
- a **revised mechanical version** is produced;
- on re-coordination, the clash is **no longer present**.

In any published evidence these would appear only as sanitised aliases
(`MODEL_1`, `MODEL_2`, `MODEL_SET_1`, `ISSUE_1`, …), never as real names.

## What the first narrow slice intends to prove

The provisional first slice (a deliberately small "Option A") aims only for:

```
model-set context
  → participating discipline models and coordinated versions
    → coordination issue
      → issue type, assignment and status
        → shared-model-context comparison
```

That is: *this coordination set contains these discipline models at these
versions, and this coordination issue refers to the same models.* It intends to
prove a **shared model context** — **not** a clash, **not** a direct
clash-to-issue link, and **not** a resolution.

## What the Phase 3C inspection proved

The read-only inspection established a **shared model context**
(`shared_model_context_proven`):

- `ISSUE_1` carries a **typed placement-lineage reference** that **exactly matches
  `MODEL_1`**, a participant in the coordination snapshot `MODEL_SET_VERSION_1`;
- **two version references decoded from the issue's viewer-state field** (already
  returned by a read-only tool) **exactly match `VERSION_1` and `VERSION_2`**, the
  coordinated versions of the two participating documents in that same snapshot.

So the issue and the coordination snapshot demonstrably refer to the **same models
at the same coordinated versions**. That is the shared model context — a real,
useful, medium-strength proof.

### What it deliberately does *not* prove

- It is **not** a Relationships API record: `list_issue_relationships` returned
  **zero records**, and an empty result proves only that no matching record was
  returned — not that the issue is unrelated.
- The typed placement match is a **typed issue-field** match; the version matches are
  **viewer-state-derived contextual** matches. Neither is a typed issue-to-model-set
  or issue-to-snapshot relationship.
- The Forma **Clashes tab** shows `ISSUE_1` beside one clash, but that is **UI
  context only** — the API exposed no clash identifier, group, member, or origin, so
  there is **no direct clash-to-issue provenance**. Viewer-state element isolation is
  **not** clash membership.
- No discipline field was returned (and none was inferred); no numeric document
  version was inferred from a URN.

## What is still deferred

- **Clash-level capability gap** — the component still cannot read clash results,
  clash identities/groups/status, clash element references, a direct clash-to-issue
  relationship, clash history, or any recheck/resolution state. So
  `clash_issue_link_proven`, `clash_resolution_claimed_not_verified`, and
  `clash_resolution_verified` are **not** established.
- **Write actions remain deferred.** Any issue selection or creation remains a
  **manual Autodesk-UI action** unless a separate write workflow is explicitly
  approved.

The sanitised public evidence artifact is **no longer outstanding** — it is
committed, and you can read it at
`examples/harrismith-fire-station/expected-results/model-coordination-to-issue-trace.result.json`.

## Distinctions this slice keeps honest

These are easy to conflate and must not be:

- **Issue status** (e.g. "closed") is a workflow state — it does **not** prove
  geometric resolution.
- **Clash status** (e.g. "resolved") does **not** by itself prove the revised model
  was actually reprocessed.
- **Geometric resolution** means the specific conflict is no longer present after
  re-coordination — the strongest claim, and the hardest to prove.
- **A later model version** existing does **not** prove any clash disappeared.
- **A direct clash-to-issue linkage** requires explicit API evidence tying a clash
  to an issue.
- **Shared model context** (issue and coordination refer to the same models) is a
  weaker, valuable proof — and is exactly what this slice **established**.

Navisworks (desktop) and cloud Model Coordination evidence must **not** be silently
merged unless their identifiers or provenance can be correlated.

## Where this leads

Coordination data now exists in the training project. Once clash-level reads exist,
later sub-phases can attempt clash identity, clash-to-issue linkage, and — most
carefully — geometric resolution verification. As always, write actions (running coordination, creating
or closing issues) are deferred by design: the reference observes before it acts.
