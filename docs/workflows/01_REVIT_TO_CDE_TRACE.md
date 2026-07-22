# 01 · Trace and Verify a Revit Deliverable from Authoring to the CDE

A learner-facing walkthrough of the first vertical slice in the Autodesk BIM
Workflow Reference Implementation. It explains *why* each step matters and what
information crosses from **authoring** (Revit) into the **common data environment**
(Forma Data Management). For the operator runbook — exact tool order, gates,
retries, provenance — see
[PHASE_1_EXECUTION_PLAN.md](PHASE_1_EXECUTION_PLAN.md).

The example project is the synthetic **Harrismith Fire Station**. This slice is
strictly read-only: nothing is uploaded, published, or modified.

## Why this slice

In real BIM delivery, a model authored in Revit becomes a controlled *deliverable*
in the CDE, where it is versioned, translated for viewing, and coordinated with
other disciplines. A great deal can go wrong in that hand-off: the wrong version is
published, the translation (derivative) fails, or the cloud item no longer matches
what the author sees. Before automating anything, it is worth learning to simply
**trace one deliverable across the boundary and verify that the two sides agree**.

That is the whole ambition here: look at the model in Revit, find the same model in
the CDE, and compare what each side can honestly tell us.

## What crosses the authoring-to-CDE boundary

```
Revit (authoring)                     Forma Data Management (CDE)
------------------                    ---------------------------
model title                --->       item display name
levels, views              --.        (no direct CDE equivalent for levels)
                             \
                              '------> item versions (v1, v2, ...)
                                       Model Derivative:
                                         manifest status
                                         viewable views
                                         model properties
```

Some information travels cleanly; some does not. A Revit model's **levels** are an
authoring concept with no direct Data Management equivalent. A CDE **version
number** and a **derivative status** are cloud-side concepts with no Revit
equivalent. Recognising this asymmetry is part of the lesson.

## The walkthrough

### 1. Look at the model in Revit
Confirm the Revit session is live, then read the model's identity: its title, how
many levels it has and their names, and the names of its views. This is the
authoring "ground truth" — what the person designing the building sees.

### 2. Find the same deliverable in the CDE
Navigate the cloud structure the way a project actually is organised: hub →
project → folders → the deliverable item. The goal is to locate the CDE item that
*corresponds to* the Revit model, usually by name.

### 3. Read the item and its versions
A CDE item carries a **display name** and a series of **versions**. Recording the
current version number answers a question Revit alone cannot: *which iteration of
this model is the controlled, shared one?*

### 4. Read the derivative representation
When a model is published, the platform translates it (the **Model Derivative**)
so it can be viewed and queried in the cloud. We record:
- the **manifest status** — did translation succeed?
- the **available views** — what can be viewed cloud-side?
- a small set of **model properties** from a chosen 3D view.

If translation is not finished, that is itself a valid, honest result — we record
the status and move on rather than pretending properties exist.

### 5. Compare the two sides
Finally, line up what Revit said against what the CDE said, field by field, and
label each comparison as:
- **match** — the two sides agree;
- **difference** — both sides have the field but they differ;
- **no equivalent** — only one side has the concept at all.

The comparison is deliberately modest. It does not try to reconcile geometry or
prove correctness; it demonstrates the *shape* of authoring-to-CDE verification.

## What is comparable, and what is not

| Information | Comparable across the boundary? |
|---|---|
| Model / item name | Yes — often the clearest cross-check |
| Views | Partially — authoring views and derivative views overlap but are not 1:1 |
| Levels | No — a Revit authoring concept, no direct CDE equivalent |
| Version number | No — a CDE concept, no Revit equivalent |
| Derivative status | No — a cloud translation concept |
| Selected properties | Partially — only a small teaching allowlist, per chosen view |

## Privacy and honesty

The published evidence for this slice is **sanitised**: real hub, project, folder,
item, and version identifiers are replaced with stable aliases (see
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md)), and only a
small, safe set of model properties is ever recorded. Where the two sides cannot be
compared, the result says so plainly. The point of the exercise is a trustworthy
trace, not an impressive-looking one.

## Where this leads

Once a deliverable can be traced and verified read-only, later phases build on the
same boundary: issues and reviews, coordination evidence, and eventually a guarded,
explicitly approved write. Those are deferred by design — this slice earns trust
first.
