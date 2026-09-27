# AGENTS.md

Context for any AI coding agent (Claude, GPT, Copilot, etc.) working in this repository. Read this before touching any file.

---

## 1. What this project is

Climora is a climate-adaptation decision-support platform. It is **not** a scientific climate-modeling library and **not** an "AI generates the plan" product. The computational chain is fixed and must not be reordered:

```
DATA → SCIENCE (hazard/exposure/vulnerability → risk) → INTERVENTION CATALOG
     → RESOURCE-CONSTRAINED OPTIMIZATION → SCENARIO EXPLORATION
     → AI EXPLANATION → HUMAN DECISION → ACTION PLAN → MONITORING
```

Full detail: `docs/architecture.md`. ADRs (don't relitigate): `docs/decisions.md`.

## 2. Non-negotiable structural rules

These are architectural invariants, not style preferences. Do not "simplify" them away even under time pressure:

- **AI never computes risk, cost, or effectiveness values.** The AI Advisor (`backend/domain/ai_advisor/`) only reads already-persisted structured outputs (risk_assessments, optimization_results, scenario diffs) and explains them. If you're tempted to have the LLM estimate a number the structured data doesn't have, don't — surface that the value is unavailable instead.
- **The Constraint Validator is a non-bypassable gate.** `backend/domain/optimization/constraint_validator.py` is the only path by which an optimizer result is persisted or returned. Never persist an optimizer output directly from `optimizer.py`, and never "round" or "adjust" a near-miss result to make it pass — reject it and log why.
- **Every derived value carries a data-class tag** (`REAL` / `MODELED` / `DEMO`) and a provenance reference. If you add a new computed field anywhere in `risk_assessments`, `vulnerability_indicators`, or `optimization_results`, it must carry this tag from day one — don't add it later as an afterthought.
- **New hazards implement the existing abstraction.** `backend/domain/risk_engine/base_hazard_engine.py` defines the interface every hazard engine (heat, and later flood/drought/water-stress) must implement. Don't special-case a new hazard directly in the API or Optimizer layers.
- **The frontend never calls a model, the optimizer, or Docker directly.** Every interaction goes through `frontend/src/services/api.ts` and the versioned `/api/v1/*` routes. No `fetch()` calls anywhere else in `frontend/src/`.

## 3. Domain module boundaries

`backend/domain/` is organized around the risk → decision chain (see `docs/backend.md` for the full table). Keep responsibilities where they belong:

| If your change involves... | It belongs in... |
|---|---|
| Hazard/exposure/vulnerability computation | `domain/risk_engine/`, `domain/exposure/`, `domain/vulnerability/` |
| Intervention cost/resource/effectiveness data | `domain/interventions/` |
| Budget/land/water/workforce/time limits | `domain/resource_manager/` |
| Portfolio selection | `domain/optimization/` |
| "What if the budget changes" logic | `domain/scenarios/` |
| Explaining a result in natural language | `domain/ai_advisor/` |
| Dataset lineage / REAL-MODELED-DEMO tagging | `domain/provenance/` |

`api/` routers stay thin — validate, call one domain/service function, return. Do not put business logic in `api/`.

## 4. Data integrity rules

- Never fabricate a climate measurement, population figure, infrastructure count, risk value, intervention cost, or effectiveness number. If real data isn't available, use a clearly-tagged `MODELED` or `DEMO` value — never present either as `REAL`.
- Any new dataset added to `data/` or `config/data_sources.yaml` needs a provenance entry (source, timestamp, version, spatial/temporal resolution) before it's used by any domain module.
- Don't hardcode hazard thresholds, intervention costs, or optimization objective weights in code — they belong in `config/hazards.yaml`, `config/interventions.yaml`, and `config/optimization.yaml` respectively (see `docs/configuration.md`).

## 5. Testing expectations

Before proposing a change as done, make sure it's covered by the relevant suite in `tests/`:

- `tests/geospatial/` — spatial ops, invalid geometry rejection
- `tests/risk/` — hazard engine outputs, hazard-abstraction conformance
- `tests/optimization/` — constraint satisfaction, no negative costs, hard-limit enforcement
- `tests/scenarios/` — scenario diffs actually reflect changed inputs
- `tests/api/` — request validation, error shapes

A change to `optimization/` or `risk_engine/` without a corresponding test is not ready for review.

## 6. Git workflow boundary

**Never commit directly to `main`.** The required sequence is: branch → implement → test → review diff → commit → push → PR.

**If you are an AI coding agent, you stop after "review diff."** Prepare a suggested commit message and summary of the diff, but do not run `git commit`, `git push`, or open/merge a PR yourself. The human developer performs every Git and PR mutation. See `docs/git-workflow.md` for the full branching/commit-message conventions.

## 7. Documentation discipline

If you add or change a domain module, update the matching doc in `docs/` in the same change (e.g., a new hazard engine → update `docs/climate-risk-engine.md`; a new optimization objective → update `docs/optimization.md`). Architecture is documented, not just coded — see `README.md`'s reading order for how these docs relate.

## 8. Reading order for an AI session

1. This file.
2. `docs/project-context.md`
3. `docs/architecture.md`
4. `docs/decisions.md`
5. Whatever domain doc matches the task at hand (`docs/climate-risk-engine.md`, `docs/optimization.md`, `docs/ai-advisor.md`, etc.)
