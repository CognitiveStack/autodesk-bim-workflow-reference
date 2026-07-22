# ADR-0002: Multi-repository, no submodules

## Status

Accepted

## Date

2026-07-22

## Context

The reference implementation spans three repositories: this orchestration layer
and the two MCP components (`CognitiveStack/autodesk-aps-forma-mcp` and
`CognitiveStack/revit-mcp-triviron`). We need a way for this repository to
reference and coordinate the components without coupling their release cycles or
duplicating their code.

Options considered:

1. Monorepo — merge all three into one repository.
2. Git submodules — embed the component repositories as pinned submodules.
3. Independent repositories referenced by identity and local path (chosen).

A monorepo would collapse independently maintained components into a single
release cycle and contradict [ADR-0001](0001-orchestration-layer-not-mcp-server.md).
Submodules add checkout friction, pin to specific commits that silently rot, and
still invite treating component source as local to this repository.

## Decision

Keep all three repositories independent. This repository references the
components by:

- GitHub identity (the `CognitiveStack/...` slugs), and
- a local checkout path supplied via environment variables (`FORMA_MCP_REPO`,
  `REVIT_MCP_REPO`), as declared in `config/components.example.yaml` and
  `.env.example`.

Do not add Git submodules. Do not vendor or copy component source. Component
version expectations are recorded in documentation rather than pinned as
submodule commits.

## Consequences

- Contributors clone the components separately and point the environment
  variables at their local checkouts.
- This repository never contains component source, avoiding duplication and
  divergence.
- Version alignment is managed by documented expectations and a component
  inventory step, not by submodule pins; documentation drift is a known risk to
  manage (see [REPOSITORY_STRATEGY.md](../architecture/REPOSITORY_STRATEGY.md)).
- Tooling in this repository must degrade gracefully when a component path is
  unset or a referenced tool is absent.
