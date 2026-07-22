# Claude Code Instructions

## Repository purpose

This repository is the orchestration, documentation, and educational reference
layer for the Autodesk BIM Workflow Reference Implementation.

It is not currently an MCP server and must not duplicate the implementations
inside the existing Forma or Revit MCP repositories.

## External component repositories

The project coordinates these independently maintained repositories:

- Autodesk APS/Forma MCP:
  `CognitiveStack/autodesk-aps-forma-mcp`

- Revit MCP:
  `CognitiveStack/revit-mcp-triviron`

Treat both as external components. Do not copy their source code into this
repository and do not create Git submodules unless explicitly authorised.

## Primary learning example

Use the Harrismith BIM Learning Project as the main synthetic teaching example.

Do not commit private Autodesk credentials, access tokens, refresh tokens,
client secrets, confidential project documents, or licensed Autodesk content.

## Architectural principles

1. Demonstrate BIM workflows rather than pursue complete API coverage.
2. Prefer stable Autodesk Platform Services APIs.
3. Isolate Beta and experimental integrations.
4. Accept hybrid manual-plus-API workflows.
5. Use Python for integration and validation utilities.
6. Keep write operations guarded and read-only by default.
7. Implement the smallest useful vertical slice before broadening scope.
8. Document actual limitations rather than inventing unsupported capabilities.

## Change control

Before making substantial changes:

1. Inspect the repository and Git status.
2. State the proposed files and purpose.
3. Avoid unrelated refactoring.
4. Run relevant checks.
5. Report changed files, checks, risks, and next steps.
