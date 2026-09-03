# UX Evaluation Principles

Date: 2026-09-02

## Role of the Legacy Reports

The Power BI dashboard screenshots embedded in the Word source documents are a primary reference for the intended business experience. They should strongly influence the target UI/UX, but they are not a pixel-perfect specification. Their age means the team should preserve the business intent while testing the experience against current Power BI and Fabric capabilities.

The screenshots should be used to identify:

- The questions business users need answered first.
- The KPI hierarchy and risk vocabulary users already recognize.
- The expected relationship between site, asset, equipment category, score, SPOF, and replacement cost.
- The workflow from portfolio overview to site detail to asset-level action.
- The visual patterns that help users compare sites and prioritize work.

## Modernization Rule

For every legacy visual or interaction, record:

1. What business decision it supports.
2. Which source fields and measures support it.
3. Whether the visual remains the clearest current experience.
4. Whether a modern interaction improves the decision path.
5. What accessibility, performance, and governance requirements apply.

Do not reproduce decorative layout, dense visual packing, unexplained colors, or static controls solely because they appear in the screenshots.

## Target Experience Criteria

### Role-aware experience

Leadership is the first-use audience. The target should support a shared governed experience that can be tailored for the role layers common in datacenter operators, telecommunications providers, and large enterprises:

- C-suite: enterprise exposure, strategic risk, capital posture, and business impact.
- VP: portfolio prioritization, investment tradeoffs, regional or business-unit comparison, and trend context.
- Director: remediation sequencing, program execution, accountability, and evidence behind scores.
- Operations: immediate exceptions, SPOFs, equipment condition, and remediation status.
- Analysts: score composition, source evidence, reconciliation, and controlled what-if analysis.

The first page should optimize for leadership decisions, but it should connect cleanly to role-appropriate drill paths. Prefer one governed metric and navigation architecture with tailored views over duplicated reports that can drift apart. The exact use of personalization, audience-specific navigation, saved views, and row-level security should be evaluated after the model and security requirements are known.

### Business workflow

- Start with an executive portfolio priority view answering: "Which sites/assets require investment first?" Use risk concentration, replacement capital exposure, and resiliency/SPOF posture as supporting lenses.
- Evaluate an Invest / Validate / Sequence / Monitor decision layer as a candidate NextField experience. Treat its mapping from score, confidence, and capital as new business logic requiring SME validation; it is not present as an established rule in the workbook.
- Support a clear path from portfolio to site, site to risk category, and risk category to affected assets.
- Make thresholds, selected filters, comparison baselines, and data freshness visible.
- Separate monitoring views from investigation views; a wallboard-style summary should not carry the full analyst workload.
- Expose the reason behind a score where the source data supports it, including the criteria contribution, SPOF condition, age, cost, and business priority.

### Interaction

- Prefer focused slicers and contextual filtering over a large permanent control wall.
- Use drillthrough, report-page navigation, and tooltips to preserve overview space while retaining detail.
- Provide consistent back navigation and a visible selected-context summary.
- Use bookmarks only where they represent a meaningful user mode, such as portfolio versus remediation planning.
- Treat the 70-site and approximately 9,070-asset reconciliation as a visible data-quality or scope explanation, not as a hidden implementation detail.

### Visual design

- Preserve the recognizable Enabled Energy / NextField visual language where it helps adoption, while maintaining strong contrast and semantic color discipline.
- Use color to communicate risk state, not decoration. Do not rely on color alone to convey status.
- Prefer direct labels, meaningful titles, and human-readable field names over raw source names.
- Keep KPI cards limited to decisions and avoid repeating the same absolute measure in multiple places.
- Use tables or matrices for action lists, with conditional formatting tied to explicit thresholds and clear sort order.

### Accessibility and usability

- Validate contrast, keyboard navigation, focus order, alt text, and screen-reader reading order.
- Provide text or icon-plus-text alternatives for red/amber/green states and other color-coded meaning.
- Keep labels readable at normal report size and avoid dense text inside visuals.
- Make thresholds and units explicit, especially scores, dollars, kW, tons, years, and percentages.
- Test the report at the expected desktop viewport and in smaller browser windows before sign-off.

### Current-capability evaluation

During report planning, explicitly evaluate whether the latest available capabilities improve the experience, including:

- Modern report-page navigation and drillthrough patterns.
- Dynamic titles, subtitles, and selected-context summaries.
- Personalization or saved views where governance permits.
- Certified or governed semantic-model measures rather than workbook-only calculations.
- Fabric lineage, sensitivity labeling, row-level security, and data-quality explanations.
- Copilot or Data Agent experiences only after the semantic model has verified names, descriptions, synonyms, relationships, and business definitions.

These capabilities are candidates for evaluation, not automatic requirements. The business workflow and verified model should decide which are adopted.

## Required UX Artifacts Before Build

Before PBIR/report authoring begins, produce:

- A screenshot-to-business-question inventory.
- A page map with audience, decision, grain, and drill path for every page.
- A legacy-to-target comparison showing preserved, redesigned, removed, and deferred elements.
- A color and threshold contract tied to the scoring model.
- A KPI reconciliation note explaining site, asset, and equipment counts.
- A design brief with non-overlapping layout regions, field bindings, accessibility checks, and validation criteria.

## Initial Position

The legacy screenshots are strong evidence for the product's information architecture and adoption needs. The target should be a governed decision-support experience that feels familiar in its questions and terminology, but clearer, more navigable, more accessible, and more trustworthy than the original workbook-driven dashboards.
