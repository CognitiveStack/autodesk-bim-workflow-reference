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

> **Status:** the model-set and participating-version foundation is now
> implemented and **live-verified** (2026-07-23), and the coordination training
> data is ready, so this trace is **partially executable**. Selecting a
> coordination issue and proving a supported model-context relationship remain
> outstanding, and clash-level reads stay deferred. **No Phase 3 evidence artifact
> exists yet**, so the current honest public proof ceiling is
> `coordination_evidence_incomplete`.

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

## Why the current evidence is incomplete

What is now in place (detailed in the capability gap):

- **Model-set/version foundation — done.** The component can discover coordination
  *model sets*, read a set's detail, list its coordination snapshot versions, and
  read the latest/specific snapshot with its **participating documents and their
  exact coordinated versions**. It also reads coordination *issues* and generic
  issue-to-document relationships.
- **Data readiness — done.** The training project now has a usable coordination
  model set (two discipline-context models processed, both participating versions
  visible through the version-level reads).

What still blocks a completed trace:

1. **Issue/relationship portion outstanding** — a coordination issue must be
   selected through the Autodesk UI, read through the existing Issues tools, and
   tied to the coordination models by a **supported model-context relationship**.
   No such trace has been captured or committed.
2. **Clash-level capability gap** — the component still cannot read clash results,
   clash identities/groups/status, clash element references, a direct
   clash-to-issue relationship, clash history, or any recheck/resolution state.

Until a selected issue and a supported relationship are traced and committed, an
honest run yields `coordination_evidence_incomplete`. Any issue selection or
creation remains a **manual Autodesk-UI action** unless a separate write workflow
is explicitly approved.

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
  weaker, valuable proof — and is the *most* this slice could establish.

Navisworks (desktop) and cloud Model Coordination evidence must **not** be silently
merged unless their identifiers or provenance can be correlated.

## Where this leads

Once clash-level reads and coordination data exist, later sub-phases can attempt
clash identity, clash-to-issue linkage, and — most carefully — geometric
resolution verification. As always, write actions (running coordination, creating
or closing issues) are deferred by design: the reference observes before it acts.
