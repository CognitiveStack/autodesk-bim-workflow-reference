# Autodesk BIM Workflow Reference Implementation

An educational reference implementation demonstrating an end-to-end Autodesk
BIM information workflow from site and concept design through Revit authoring,
common data environment management, coordination, review, construction
information exchange, and asset handover.

The Harrismith BIM Learning Project is the primary example used throughout the
repository.

## Project goals

1. Demonstrate the Autodesk BIM workflow from concept to handover.
2. Use APIs and MCP automation where they genuinely simplify the workflow.
3. Prefer stable Autodesk Platform Services APIs for core demonstrations.
4. Isolate experimental Forma Site Design Beta functionality.
5. Preserve manual Autodesk workflows where API automation would add excessive
   complexity.
6. Provide a reusable Python-oriented learning resource for Autodesk developers.

## Component repositories

This repository coordinates and documents two independently maintained
software components:

- `CognitiveStack/autodesk-aps-forma-mcp`
  - Autodesk Platform Services and Forma integration
  - Data Management, Forma, Issues, Reviews, Assets, and related cloud APIs

- `CognitiveStack/revit-mcp-triviron`
  - Revit and pyRevit MCP automation
  - Revit model creation, inspection, views, sheets, and authoring workflows

The component repositories remain separate Git repositories. They are not
embedded as submodules.

## Reference workflow

```text
Site and context
    -> Concept design
    -> Revit authoring
    -> CDE information management
    -> Model coordination
    -> Reviews and issues
    -> Construction information exchange
    -> Asset handover
```
## Current Status

Repository bootstrap and master architecture definition.

The initial implementation will focus on one small end-to-end vertical slice
using the Harrismith Fire Station learning project.
