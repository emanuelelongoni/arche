# Archē

The knowledge graph behind Archē (https://arche.academy), an open-source learning platform for monk-mathematicians: people who study mathematics, much of it machine-produced, for understanding rather than for production. Topics are nodes; prerequisites, review credit and cross-links are edges; formal anchors tie nodes to Lean's Mathlib; viewpoints (currently `classical` and the nLab's `npov`) choose between alternative routes.

This repo is content as code. Agents write YAML; validators and Lean check it; a human reviews small PRs.

## Status (first slice)

- Spec, schemas, validator, path planner, renderer, Lean anchor check and CI.
- Coverage specs paraphrased from the Cambridge Schedules 2026–27 for the pilot strand: IA Numbers and Sets → IA Analysis I → IB Analysis II → IB Topological Spaces.
- Gold-standard nodes for IB Analysis II §3 (metric spaces), uniform continuity, IB Topological Spaces §1–3, and a five-node supplementary category-theory course for the nPOV route: 47 draft nodes and 9 stubs.
- Two viewpoints with three choice groups: how subspace, quotient and product topologies are built (by hand vs initial/final topologies); how their universal properties are framed (concretely vs categorically); and how finite products of compact spaces are proved (tube lemma vs universal closedness).
- Every anchor checked against Mathlib commit `6ebcce3` (2026-11-22) by name lookup. The first `lake build` (job J0007) is the definitive check.
- Eight jobs in `jobs/open/` for the rest of the strand.

## Quick start

```sh
pip install pyyaml jsonschema pytest
python3 tools/validate.py --report                      # check everything, print coverage
python3 tools/plan.py ts.heine-borel --compare classical npov
python3 -m pytest -q tests                              # validator and planner tests
python3 tools/render.py --viewpoint npov --out build/npov   # needs graphviz for SVG/PNG
python3 tools/gen_anchor_check.py && (cd lean && lake update && lake exe cache get && lake build)
```

## Layout

```
spec/SCHEMA.md      data model and semantics (read first)
spec/STYLE.md       how to write nodes; the nPOV guidance
CLAUDE.md           instructions for agents
schema/             JSON Schemas for nodes, courses, viewpoints, jobs
graph/courses/      coverage specs (what must be covered)
graph/viewpoints/   classical.yaml, npov.yaml (which route)
graph/nodes/        one node per file, by course
tools/              validate, plan, render, gen_anchor_check, split_bundle, export_site
site/               the arche.academy website, generated from graph/ (see below)
lean/               Lean project pinned to Mathlib; Anchors.lean is generated
jobs/               the agent work queue
```

## Website

https://arche.academy is built from `graph/` on every push to `main` (`.github/workflows/site.yml`), so it can't drift from the graph. `tools/export_site.py` resolves the viewpoints through `mmgraph` into one JSON document, and the Astro site in `site/` renders only that. The spec is `docs/specs/site-v0.md`.

```sh
cd site && npm ci
npm run dev            # export the graph, then serve with live reload
npm test               # the route planner gives exactly what tools/plan.py gives
npm run build && npm run check:links && npx playwright install chromium && npm run e2e
```

## The hands-off loop

1. A scheduled Claude Code task runs nightly against this repo with a prompt like: "Read CLAUDE.md. Take the next open job, do it, and open a PR."
2. CI runs the validator and the Lean anchor check on the PR.
3. You review the PR: judgment calls are listed first in the description. When a pattern is wrong, fix `spec/STYLE.md`, not just the output.
4. Merge, and the next run takes the next job.

## Sources

- `cam-schedules-2026-27`: University of Cambridge, Faculty of Mathematics, *Schedules of Lecture Courses and Form of Examinations for the Mathematical Tripos 2026–27* (revised 19 August 2026), https://www.maths.cam.ac.uk/undergrad/course/schedules.pdf. Course files paraphrase its syllabus items and lecture counts.
- nPOV: https://ncatlab.org/nlab/show/nPOV
- Mathlib: https://github.com/leanprover-community/mathlib4

## Licence

Not chosen yet. Pick one for code and one for content before the first public push.
