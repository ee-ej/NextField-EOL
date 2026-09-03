# Initial Setup Prompt — NextField EOL (VS Code + GitHub Copilot + Fabric/Power BI Skills & MCP)

> Paste the block below into GitHub Copilot Chat (Agent mode) in VS Code, with the
> `C:\Dev\NextField\NextField-EOL` folder open as your workspace. It bootstraps the
> toolchain, verifies the Power BI Modeling MCP connection, ingests our source docs,
> and loads the starter TMDL — without making any changes until you approve a plan.

---

## ✅ Before you paste (one-time prerequisites)

Run these in a terminal first (the agent can't install system software for you):

```powershell
# 1. Node.js 18+ (required by the Power BI Modeling MCP server)
node --version        # expect v18+ ; if missing: winget install OpenJS.NodeJS.LTS

# 2. GitHub Copilot CLI (the Skills marketplace runs through it)
npm install -g @github/copilot        # or: winget install GitHub.CopilotCLI
copilot --version

# 3. Power BI Desktop installed (the LOCAL MCP drives it for authoring + screenshots)

# 4. Confirm the project + source docs exist
dir C:\Dev\NextField\NextField-EOL\source
```

---

## 📋 THE PROMPT (copy everything below this line)

```
You are my senior Fabric + Power BI platform engineer working inside VS Code with
GitHub Copilot Agent mode. We are setting up the toolchain for the "NextField EOL"
project. Work in small, verifiable steps and ASK BEFORE changing anything destructive.

# CONTEXT
- Workspace root: C:\Dev\NextField\NextField-EOL
- Reference docs live in: C:\Dev\NextField\NextField-EOL\source
  (read these first for project scope, source-tab mapping, and the target data model)
- Goal: reproduce the Flexential "EOL / Site Risk" Power BI dashboards as a governed
  Microsoft Fabric solution, and lift the scoring engine into a Direct Lake semantic
  model that becomes the NextField "Asset Record" backbone.
- Preview note: "Agent Skills for Power BI" and the Power BI Modeling MCP are in
  public preview and change weekly. Pin versions and tell me if anything drifts.

# STEP 0 — ORIENT (read-only, no changes)
1. Recursively list C:\Dev\NextField\NextField-EOL\source and summarize each doc in
   one line. Explicitly flag any of these if present: the PoC brief, the starter TMDL
   (FlexEOL_NextField.SemanticModel.tmdl), source-tab -> data-model mapping, and the
   Flex EOL workbook.
2. From those docs, restate back to me (concise bullets) your understanding of:
   - the 3 fact tables + dimensions (star schema),
   - the 9-criteria weighted scoring model and the exact weights,
   - the cost model exponent (should be 0.8),
   - the known risks: SPOF data is stored TRANSPOSED, and the dashboard KPI counts
     do not reconcile (70 sites / 9,070 asset base).
   Do not proceed until I confirm your understanding is correct.

# STEP 1 — INSTALL THE SKILLS + MCP
3. Verify prerequisites and print versions: node --version, copilot --version.
   If either is missing, stop and tell me exactly what to install.
4. Install the Power BI authoring toolkit via the Skills for Fabric marketplace:
       copilot plugin marketplace add microsoft/skills-for-fabric
       copilot plugin install powerbi-authoring@fabric-collection
5. Confirm the skills loaded by running `/skills` and verifying these appear:
   semantic-model-authoring, report-authoring, report-design, report-planner,
   report-management. List the exact installed versions so we can pin them.
6. Confirm the Power BI Modeling MCP server was auto-registered. Show me the relevant
   mcp.json / config entry. If it is NOT registered, register it manually and explain
   what you changed.

# STEP 2 — SCAFFOLD THE WORKSPACE (propose first, then apply on my approval)
7. Propose a clean repo structure for a PBIP + Fabric project, e.g.:
       /semantic-model      (the .SemanticModel folder / TMDL)
       /reports             (the .Report / PBIR definitions)
       /notebooks           (Lakehouse PySpark: SPOF unpivot, scoring rebuild)
       /source              (existing reference docs — leave as-is)
       /docs                (decisions, data-spec, KPI reconciliation notes)
       .gitignore, README.md
   Show me the plan as a tree and WAIT for my approval before creating folders.
8. After approval, initialize the structure and a README that captures project scope,
   the source-of-record decision (CMMS/EAM vs Dataverse — mark as OPEN), and the
   preview-version pins from Step 1.

# STEP 3 — LOAD THE STARTER MODEL
9. If FlexEOL_NextField.SemanticModel.tmdl exists in /source, copy it into the
   /semantic-model location as the scaffold. Then use the Power BI Modeling MCP to:
   - open/validate the model,
   - run a best-practice review and list findings (do NOT auto-fix yet),
   - validate the DAX for [Overall Score (weighted, dynamic)] and
     [# Items >= Threshold], reporting any errors.
   Summarize what is valid, what needs data wiring, and what needs my decisions.

# STEP 4 — CONNECTION CHECK (no data changes)
10. Confirm the MCP can connect to Power BI Desktop and/or a Fabric workspace.
    Tell me which Entra identity / workspace it will use, and stop before writing to
    any remote workspace so I can confirm the target.

# GUARDRAILS
- Never write to a remote Fabric workspace without explicit confirmation of the target.
- Never auto-accept best-practice fixes; present them as a checklist for my sign-off.
- Treat all MCP-generated DAX as draft pending SME validation.
- Keep a running /docs/SETUP_LOG.md of every command run and every version pinned.

# OUTPUT FOR THIS SESSION
End with: (a) a status table of Steps 0–4 (done / blocked / needs-my-decision),
(b) the exact skill + MCP versions pinned, and (c) the top 3 decisions you need from
me before we start building (source of record, target workspace, KPI reconciliation
rule).
```

---

## 🔎 What this prompt deliberately does

| Design choice | Why |
|---|---|
| **Read-only Step 0 first** | Grounds Copilot in *your* `\source` docs before it touches anything, so it uses the real schema and the 0.8 exponent — not generic assumptions. |
| **"Restate understanding, wait for confirmation"** | Catches drift early (especially the transposed-SPOF and KPI-mismatch traps) before code is written. |
| **Version pinning + SETUP_LOG.md** | The Skills/MCP are weekly-changing public preview; pinning keeps the PoC reproducible. |
| **"Propose tree, wait for approval"** | Prevents the agent from scaffolding folders you didn't want. |
| **Explicit guardrails on remote writes & DAX** | Keeps human-in-the-loop on governance and calculation correctness. |
| **Ends with a decisions list** | Surfaces the 3 real blockers (source of record, target workspace, KPI rule) so Thursday's call has a clear agenda. |

## 💡 Follow-on prompts (after setup succeeds)
1. *"Using the report-planner skill, plan the Asset Health by Facility page from the screenshot in `\source`, then build it with report-authoring and screenshot-diff against the original."*
2. *"Draft the PySpark notebook that unpivots `Entry- Site SPOF Data` (sites-as-columns) into `[SiteNo],[SPOFQuestion],[Value]` and rebuilds the site risk score."*
3. *"Scope the LAS03/LAS05 2-week PoC as GitHub issues with acceptance criteria from the PoC brief."*
