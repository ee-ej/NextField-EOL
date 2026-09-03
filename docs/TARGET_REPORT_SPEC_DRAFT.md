# NextField EOL Target Report Specification

Date: 2026-09-02
Status: Draft planning artifact; not approved for implementation

## Report Intent

Provide a governed portfolio decision experience that answers which sites and assets require investment first, while allowing C-suite, VP, Director, operations, and analyst users to move from the same trusted context into the level of evidence appropriate to their role.

## Leadership Landing Page

Primary question: **Which sites/assets require investment first?**

Working direction: **Combined experience**, with the leadership priority view as the landing page and controlled paths for VP, Director, operations, and analyst needs.

Candidate decision states:

- Invest
- Validate
- Sequence
- Monitor

These states are design candidates only. The workbook currently supplies replacement scores, risk scores, SPOF indicators, and capital forecasts, but not a validated rule that maps those measures into the four decision states.

## Proposed Page Map

| Page | Primary audience | Decision or job | Status |
|---|---|---|---|
| Portfolio Priority | C-suite, VP, Director | Which sites/assets require investment first? | Proposed landing page |
| Risk and Resiliency | VP, Director, Operations | Where is risk concentrated and which SPOF conditions drive it? | Proposed supporting page |
| Capital Outlook | C-suite, VP, Director | What capital exposure follows from the priority sequence? | Proposed supporting page |
| Site Action Review | Director, Operations | What should happen at this site and in what order? | Proposed drill page |
| Asset Evidence | Operations, Analysts | Which equipment and criteria explain the score? | Proposed drillthrough page |
| Source and Reconciliation | Analysts, governance stakeholders | Which source rows, grains, and KPI definitions support the result? | Proposed validation page |

The page map is intentionally provisional until workbook profiling confirms the grains and available fields for each decision.

### Proposed landing composition

1. **Priority decision view**
   - Rank sites or site/asset opportunities by candidate investment priority.
   - Show the decision state and the evidence supporting it.
   - Make data confidence and scope visible.
2. **Leadership context strip**
   - Distinct site count.
   - Distinct asset count.
   - Scored-row count.
   - Projected replacement capital exposure.
   - SPOF or resiliency exception count.
   - Each number requires a defined grain and reconciliation note.
3. **Risk concentration lens**
   - Show where risk is concentrated by site and equipment/risk category.
4. **Capital exposure lens**
   - Show projected replacement exposure by site, year, and relevant category.
5. **Resiliency/SPOF lens**
   - Show threshold exceptions and redundancy posture, with clear answer semantics.

## Role-Aware Navigation

| Role | Default view | Drill path |
|---|---|---|
| C-suite | Portfolio priority, business impact, capital posture, confidence | Priority -> site/business context |
| VP | Portfolio and regional/business-unit comparison | Priority -> site -> category/capital lens |
| Director | Ranked program and remediation queue | Priority -> site -> risk category -> affected assets |
| Operations | Exceptions, SPOFs, asset condition, remediation detail | Site -> question/equipment evidence |
| Analyst | Score composition, source evidence, reconciliation | Any view -> detailed rows and validation context |

The role model should use one governed metric layer and shared definitions. Tailoring may be implemented through navigation, audience views, personalization, saved views, or security controls after requirements are confirmed.

## Required Drill Paths

- Portfolio priority -> selected site.
- Site -> risk category and resiliency/SPOF evidence.
- Risk category -> affected assets.
- Asset -> nine-criteria score composition, age, cost, and source attributes.
- Capital exposure -> year and site detail.
- Any KPI -> definition, grain, and reconciliation context.

## Legacy-to-Modern Evaluation

Preserve from the legacy reports:

- Site and asset prioritization language.
- Risk and resiliency concepts.
- Familiar score thresholds where validated.
- Workbook-driven business questions and source traceability.

Evaluate or redesign:

- Dense dashboard packing.
- Static filter walls.
- Ambiguous red/amber/green semantics.
- Repeated absolute KPIs.
- Navigation and drillthrough behavior.
- Accessibility and screen-reader order.
- Dynamic context, confidence, freshness, and data-quality explanations.
- Modern Power BI/Fabric capabilities that improve decision quality without adding noise.

## Data and Model Dependencies

Before locking this specification:

- Re-evaluate the workbook directly.
- Confirm fact-table grains and key relationships.
- Resolve the 233-column asset source projection.
- Normalize and validate the transposed SPOF matrix.
- Confirm the nine scoring weights and score thresholds.
- Separate the cost exponent `0.8` from the overall correction factor `0.6`.
- Define the Invest/Validate/Sequence/Monitor mapping, including confidence and exception behavior.
- Define site, asset, equipment-row, and scored-row KPI measures.
- Confirm source-of-record direction: presumed CMMS/EAM, with Dataverse as a possible future source.

## Approval Gates

1. Approve the workbook-derived source mapping.
2. Approve the semantic model contract and KPI definitions.
3. Approve the decision-state business rules.
4. Approve the leadership landing-page composition and role drill paths.
5. Approve the target Fabric workspace and publication path.
6. Lock this specification before implementation.

## Explicitly Out of Scope for This Draft

- Creating PBIP/PBIR files.
- Copying or modifying the starter TMDL.
- Creating semantic models, Lakehouse tables, reports, or notebooks.
- Deploying to `NextField-EOL-Dev`.
- Treating the legacy screenshots as pixel-perfect requirements.
