# 02 · Review-to-Issue Governance Trace

A learner-facing walkthrough of the second vertical slice in the Autodesk BIM
Workflow Reference Implementation. It explains *why* each step matters as a
project's information passes through **formal review** and **issue governance** in
the common data environment. For the operator runbook — exact tool order, gates,
and warnings — see
[PHASE_2_EXECUTION_PLAN.md](PHASE_2_EXECUTION_PLAN.md). For what must be built
first, see
[PHASE_2_CAPABILITY_GAP.md](../architecture/PHASE_2_CAPABILITY_GAP.md).

The example project is the synthetic **Harrismith Fire Station**. This slice is
strictly read-only: no review is initiated, no issue is created or changed, nothing
is approved.

## Why this slice

Phase 1 traced a deliverable across the authoring-to-CDE boundary. But a CDE is not
just storage — it is where information is **governed**: documents are formally
reviewed, decisions are recorded, and open questions become **issues** with an
owner, a type, and a status. The value of the CDE is only realised if you can show
*how a decision was reached and whether the resulting action was closed out*.

This slice learns to trace that governance chain end to end, and — just as
importantly — to be honest about the links it cannot prove.

## The governance chain

```
CDE document version
   -> approval workflow            (which review process applies)
      -> review instance           (the actual review that ran)
         -> progress & outcome      (where it got to; approved / rejected / ...)
            -> related issue         (a question the review raised)
               -> type, status, owner
                  -> relationship     (does the issue actually link back?)
                     -> resolution evidence (a response document/version)
```

Each arrow is a claim that must be **proven by API evidence**, not assumed.

## The teaching scenario

Using the synthetic Harrismith Fire Station governance story:

- a **reviewed document** — a building-overview drawing set;
- a **review** — a client/design review of that set;
- an **issue** raised by the review — a request to clarify the mezzanine floor
  extent;
- a **planned response** — a later clarification drawing.

In the published evidence these appear only as sanitised aliases
(`DOCUMENT_1.pdf`, `REVIEW_1`, `ISSUE_1`, `DOCUMENT_2.pdf`, …), never as real
titles or identifiers.

## Two honesty rules

1. **Not every review has an issue, and not every issue belongs to a review.** The
   relationship must be proven through API evidence, or recorded as *unproven*
   (`no_equivalent`). Sharing a project is not proof of a link.
2. **Outcomes are independent.** The issue's status is never inferred from the
   review's outcome, and the review's outcome is never inferred from the issue's
   status. A closed issue does not mean an approved review, and vice versa.

## What crosses, and what does not

| Information | Comparable / provable across the chain? |
|---|---|
| Reviewed document version ↔ CDE version | Yes — a direct governance check |
| Review workflow ↔ project | Yes |
| Review progress ↔ outcome | Internal consistency check |
| Review outcome ↔ issue status | **No** — must not be inferred |
| Issue ↔ reviewed file/review | Only if references positively prove it |
| Response document ↔ issue closure | Traceable as a separate document; closure is not assumed |

## A capability caveat

Since Phase 2B (2026-07-23) the reference project can read **issues**
(`list_issues`, `get_issue_details`, `list_issue_types`), **reviews** (seven
read-only tools), and a narrow **issue-relationship lookup**
(`list_issue_relationships`) — all live-verified. A **direct** Review-to-Issue
relationship is **not** established by the platform: the relationship lookup
compares **shared documents**, and can prove that an issue and a review point at
the **same document version** or the **same document lineage** (a weaker proof
than an exact version). A valid **empty** lookup result is not proof that no
relationship exists, and legitimately leads to a `relationship_not_proven`
outcome. So a live run can now reach every stage — but honest qualification of the
relationship still matters, and the sanitised **Phase 2C evidence is still
pending**.

## Where this leads

Once a review-to-issue chain can be traced and honestly qualified, the same
discipline extends to construction information exchange and asset handover. As
always, write actions (initiating reviews, creating or closing issues) are deferred
by design — the reference earns trust by observing before it acts.
