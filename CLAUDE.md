# Instructions for agents working in this repo

This repo holds the knowledge graph of Archē (arche.academy), an open-source learning platform for "monk-mathematicians". It is content as code: YAML files checked by validators and by Lean. You will usually be running unattended on a scheduled task. A human reviews your pull request later with a small daily budget, so make PRs small and easy to review.

## Before anything else

1. Read `spec/SCHEMA.md` (the data model) and `spec/STYLE.md` (how to write content). They override anything you remember about other knowledge graphs.
2. Run `python3 tools/validate.py` and confirm it passes on `main` before you change anything. If it doesn't, stop and open an issue instead of a PR.

## How to pick work

- Take the lowest-numbered job in `jobs/open/` with `status: open` whose `depends_on` jobs are all `done`, or the job named in your task prompt.
- Set `status: claimed` and `claimed_by` in the job file as the first commit on your branch (`job/<id>`).
- Do only what the job's scope says. If you find other problems, list them in the PR description under "Noticed, not changed".

## Writing nodes

- One node per file at `graph/nodes/<course-id>/<node-id>.yaml`. To write many nodes, author them as one multi-document YAML file under `authoring/` and run `python3 tools/split_bundle.py authoring/<file>.yaml`, which writes the individual files. Then delete the bundle.
- Use the gold-standard slice as your model of quality and density: `graph/nodes/ib-topological-spaces/` and `graph/nodes/ib-analysis-ii/`.
- Every `requires` edge needs a specific `reason`. Every anchor must exist in the pinned Mathlib: check with the lean-lsp-mcp server if it's configured, otherwise search the Mathlib source at the commit in `lean/lakefile.toml`.
- New nodes are `status: draft`. Never set `status: reviewed`; only a human does that.
- Don't edit a node with `status: reviewed` unless the job explicitly lists it.

## Checks before opening a PR

```sh
python3 tools/validate.py              # must exit 0
python3 -m pytest -q tests             # validator and planner tests; must pass
python3 tools/validate.py --report     # paste the coverage lines for your course into the PR
python3 tools/gen_anchor_check.py      # regenerates lean/Arche/Anchors.lean
(cd lean && lake build)                # if Lean is available; CI runs it anyway
```

Fix every error, and fix the warnings your change introduced.

## The PR

- Title: `<job id>: <job title>`.
- Description: what you did; the coverage lines for the course; every judgment call a reviewer should check, listed first (edges you were unsure of, items you split or merged, anchors you couldn't find); "Noticed, not changed".
- Move the job file to `jobs/done/` only when the PR is merged. In your PR, set it to `status: in-review` with `pr:` set.
