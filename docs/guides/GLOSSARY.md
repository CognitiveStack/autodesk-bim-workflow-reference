# Glossary

Canonical terminology for the Autodesk BIM Workflow Reference Implementation.
The terminology model behind this glossary is defined in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

Entries distinguish four tiers: **platform**, **product / offering**, **API
family**, and **historical name**. Naming an API family is not a claim about API
maturity; maturity (stable vs beta) is a separate concern and is only asserted
where verified and cited.

**Terminology last verified: 2026-07-22** against official Autodesk and APS
sources (see [References](#references)). Items awaiting official confirmation are
marked *to be verified*.

## Platform and product terms

### Autodesk Forma
The overall Autodesk industry cloud platform for architecture, engineering,
construction, and operations. Autodesk Construction Cloud has been brought into
Autodesk Forma. *(Tier: platform.)*

### Forma for Construction
Forma for Construction is Autodesk's current umbrella term for
construction-oriented workflows and offerings on the Autodesk Forma platform, and
is described by Autodesk as the successor terminology to Autodesk Construction
Cloud. Exact commercial bundles and included products may evolve, so individual
offerings should be named explicitly. *(Tier: product / offering — umbrella.)*

### Forma Data Management
The Forma offering for managing project files, folders, versions, and controlled
information — the common data environment capabilities of the platform. Automated
through the APS Data Management API. *(Tier: product / offering.)*

### Forma Build
The Forma offering for construction-phase workflows and information exchange.
Individual construction capabilities (for example issues, RFIs, and assets)
should be named explicitly rather than assumed from the umbrella name.
*(Tier: product / offering.)*

### Forma Site Design
The Forma offering for early-stage site and context design. In this project its
API automation is treated as experimental and read-first; write automation is
deferred. *(Tier: product / offering. Site Design API maturity: to be verified.)*

### Model Coordination
The Forma capability for coordinating discipline models and detecting clashes.
This project uses the native coordination engine rather than re-implementing
clash detection. *(Tier: product / offering.)*

### Design Collaboration
The Forma offering supporting multi-discipline design collaboration and the
controlled sharing of work between teams. *(Tier: product / offering.)*

## API terms

### Autodesk Platform Services (APS)
The Autodesk developer platform and API family (formerly the Forge platform).
Provides the APIs used for automation in this project, including the Data
Management API, Model Derivative API, Issues API, Assets API, Reviews API, and
RFI API. *(Tier: API family.)*

## Historical names

### Autodesk Construction Cloud (ACC)
Former name for Autodesk's construction cloud, now brought into Autodesk Forma /
Forma for Construction. Retained here for historical accuracy. *(Tier: historical
name.)*

### Autodesk Docs
Former name for the document-management / common data environment product now
represented by Forma Data Management. *(Tier: historical name.)*

### Autodesk Build
Former name for the construction-management product now represented within Forma
Build / Forma for Construction. *(Tier: historical name.)*

## Concept and component terms

### Common Data Environment (CDE)
The single agreed source of information for a project, used to collect, manage,
and disseminate project information through controlled processes. In this project
the CDE is represented by Forma Data Management.

### MCP (Model Context Protocol)
An open protocol for exposing tools and context to AI assistants. The two
software components of this project are implemented as MCP servers in their own
repositories.

### Revit MCP
The Revit / pyRevit MCP component, `CognitiveStack/revit-mcp-triviron`. Provides
Revit authoring and inspection automation. Referenced locally via the
`REVIT_MCP_REPO` environment variable. Its specific tools are treated as
capabilities to be confirmed by component inventory.

### APS/Forma MCP
The Autodesk Platform Services / Forma MCP component,
`CognitiveStack/autodesk-aps-forma-mcp`. Provides focused cloud and
information-management actions (authentication, Data Management, and related
APIs). Referenced locally via the `FORMA_MCP_REPO` environment variable. Its
specific tools are treated as capabilities to be confirmed by component
inventory.

## References

- Autodesk Construction Cloud is now Autodesk Forma —
  <https://www.autodesk.com/blogs/construction/autodesk-construction-cloud-is-now-forma/>
- Autodesk Construction Cloud is now Autodesk Forma (Autodesk News) —
  <https://adsknews.autodesk.com/en/news/autodesk-construction-cloud-is-now-autodesk-forma/>
- Forma for Construction Forums —
  <https://forums.autodesk.com/t5/forma-for-construction-forum/>
- Autodesk Platform Services — API & SDK documentation —
  <https://aps.autodesk.com/developer/documentation>
- APS Data Management API —
  <https://aps.autodesk.com/en/docs/data/v2>
- APS Model Derivative API —
  <https://aps.autodesk.com/en/docs/model-derivative/v2>
