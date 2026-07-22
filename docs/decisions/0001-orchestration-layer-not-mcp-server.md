# ADR-0001: Orchestration and reference layer, not an MCP server

## Status

Accepted

## Date

2026-07-22

## Context

This repository is the master orchestration, documentation, and educational
reference layer for the Autodesk BIM Workflow Reference Implementation. Two
software components that actually implement Model Context Protocol (MCP)
tooling are maintained separately:

- Autodesk APS/Forma MCP — `CognitiveStack/autodesk-aps-forma-mcp`
- Revit MCP — `CognitiveStack/revit-mcp-triviron`

There is a temptation, in a repository that coordinates those components, to
begin implementing convenience tools, wrappers, or a thin MCP server here. Doing
so would duplicate logic that already lives in the component repositories,
create drift between two copies of the same behaviour, and blur the boundary
this project depends on.

## Decision

This repository is an orchestration, documentation, and educational reference
layer. It does not implement an MCP server, and it does not copy or vendor the
source code of either component repository.

Its permitted contents are:

- documentation (PRD, architecture, ADRs, guides, workflow narratives);
- configuration examples describing how components are wired together;
- Python integration and validation utilities that *invoke or verify* component
  behaviour without re-implementing it;
- synthetic learning examples (the Harrismith BIM Learning Project).

MCP tool implementations, Autodesk authentication logic, and Autodesk API
clients remain the responsibility of the component repositories. See
[ADR-0002](0002-multi-repo-no-submodules.md) for the multi-repository stance and
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) for the
responsibility matrix.

## Consequences

- The repository stays small, stable, and focused on demonstrating BIM
  workflows rather than pursuing API coverage.
- Contributors must resist adding tool implementations here; such work belongs
  in the relevant component repository.
- Utilities in `scripts/` must call component tools or validate their outputs,
  never reproduce their internal logic (auth, derivative processing, clash, and
  similar).
- Because this layer does not own the tools, any tool it references must be
  labelled by capability status (confirmed / required / planned) until a
  component inventory confirms it. See
  [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md).
