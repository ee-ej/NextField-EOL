# NextField EOL UX and Page Map Draft

Date: 2026-09-03
Status: Draft for business and report-design review

## Design Intent

Create one governed decision-support experience that answers:

> Which sites and assets require investment first?

Leadership is the first-use audience. Operations and analysts must be able to move from the same context into risk evidence, asset detail, source provenance, and reconciliation information.

The workbook remains the current PoC source of record. Candidate decision states such as Invest, Validate, Sequence, and Monitor are not yet governed business rules.

## Page Map

| Page | Primary audience | Decision or job | Grain | Main path |
|---|---|---|---|---|
| Portfolio Priority | C-suite, VP, Director | Which sites/assets require investment first? | Site and site/asset opportunity | Start here -> selected site |
| Risk and Resiliency | VP, Director, Operations | Where is risk concentrated and which SPOF conditions drive it? | Site, category, and normalized SPOF evidence | Site -> category -> questions |
| Capital Outlook | C-suite, VP, Director | What capital exposure follows from the priority sequence? | Site, forecast year, and budget category where available | Portfolio -> capital -> site detail |
| Site Action Review | Director, Operations | What should happen at this site and in what order? | Selected site and affected assets | Priority -> site -> action queue |
| Asset Evidence | Operations, Analysts | Which equipment and criteria explain the score? | Asset and nine-criteria score components | Site/category -> asset -> evidence |
| Source and Reconciliation | Analysts, governance stakeholders | Which source rows, grains, and KPI definitions support the result? | Source row, output row, KPI definition | Any KPI -> definition/evidence |

## Portfolio Priority Landing

### Required regions

1. **Priority decision region**
   - Ranked sites or site/asset opportunities.
   - Candidate decision state, clearly labeled as draft until approved.
   - Replacement score, site risk, capital exposure, resiliency/SPOF signal, and confidence.
2. **Leadership context strip**
   - Valid portfolio site count.
   - Valid source asset count.
   - Valid scored-asset or scored-row count once the output boundary is approved.
   - Projected replacement capital exposure.
   - SPOF/resiliency exception count once normalization is approved.
3. **Risk concentration lens**
   - Compare exposure by site and risk category.
   - Use direct labels and explicit score units.
4. **Capital exposure lens**
   - Show projected replacement exposure by forecast year and site.
   - Keep dollars and forecast year visible in titles or labels.
5. **Resiliency/SPOF lens**
   - Show exception count and selected-site posture.
   - Do not imply a final SPOF rule until threshold semantics are validated.
6. **Scope and confidence context**
   - Make the 70-site versus approximately 9,070-equipment-row distinction visible.
   - Surface unresolved source or calculation exceptions.

## Navigation and Drill Paths

- Portfolio Priority -> selected site.
- Selected site -> risk category and resiliency/SPOF evidence.
- Risk category -> affected assets.
- Asset -> nine criteria, age, cost, condition, and source attributes.
- Capital exposure -> forecast year and site detail.
- Any KPI -> definition, grain, filter, exclusion, and source context.

Use consistent back navigation, selected-context summaries, drillthrough, and tooltips. Avoid a permanent wall of filters; use focused slicers and contextual filters instead.

## Role Defaults

| Role | Default view | Required evidence |
|---|---|---|
| C-suite | Portfolio Priority | Enterprise exposure, capital posture, confidence |
| VP | Portfolio Priority | Site comparison, risk concentration, capital outlook |
| Director | Portfolio Priority or Site Action Review | Ranked queue, affected assets, sequencing context |
| Operations | Risk and Resiliency or Site Action Review | SPOFs, exceptions, condition, remediation detail |
| Analyst | Source and Reconciliation or Asset Evidence | Score composition, row-level provenance, KPI rules |

Use one metric layer and shared definitions. Personalization, saved views, audience navigation, and row-level security remain implementation decisions after governance requirements are confirmed.

## Visual and Accessibility Contract

- Use color to reinforce risk meaning, never as the only status signal.
- Use direct labels and human-readable names instead of raw workbook headers.
- Keep KPI cards limited to distinct decisions and avoid duplicate absolute measures.
- Use tables or matrices for action queues with explicit sort order and threshold definitions.
- Show score, dollar, kW, percentage, year, and age units wherever they appear.
- Validate contrast, keyboard navigation, focus order, alt text, and screen-reader order.
- Keep page regions non-overlapping and readable at the expected desktop viewport and smaller browser widths.
- Do not reproduce dense legacy layout or decorative elements without a documented decision benefit.

## Deferred Until Governance Is Complete

- Final Invest/Validate/Sequence/Monitor logic.
- Final scored-asset and scored-row boundaries.
- SPOF exception calculation and site-group coverage.
- Final score color bands and threshold inclusivity.
- PBIP/PBIR authoring, semantic-model creation, and publication to `NextField-EOL-Dev`.

## Review Questions

1. Does the landing page answer the investment-priority question within the first 10 seconds?
2. Are the six pages sufficient for leadership, operations, and analyst workflows?
3. Are the proposed drill paths enough to explain a priority without exposing unnecessary detail?
4. Which role should own review and approval of the decision-state mapping?
5. Which KPI definitions and confidence signals must be visible on every page?
