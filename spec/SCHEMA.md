# Data model

This document is the contract between the people and agents who write content and the tools that check and use it. If a tool and this document disagree, the document is right and the tool has a bug.

## 1. Three kinds of file

| Kind | Where | What it says |
|---|---|---|
| Course | `graph/courses/<course-id>.yaml` | What must be covered: sections and items taken from a syllabus. It says nothing about teaching order. |
| Node | `graph/nodes/<course-id>/<node-id>.yaml` | One schedulable topic, with its edges, formal anchors and lesson guidance. One node per file, so parallel agents don't collide. |
| Viewpoint | `graph/viewpoints/<viewpoint-id>.yaml` | One option in every choice group. A viewpoint turns the graph into a plain DAG. |

Schemas: `schema/*.schema.json`. The validator (`tools/validate.py`) checks every file against them and then checks the semantics in §5.

## 2. Nodes

A node is the unit the scheduler works with: something a learner can be taught, practise and review in one sitting (15–45 minutes). It has 2–5 knowledge points (KPs). Each KP is one worked example followed by practice. KPs are the unit of spaced repetition; the node is the unit of gating.

Ids are `<course prefix>.<kebab-slug>` (e.g. `ts.compact-in-hausdorff-closed`). The prefix is set in the course file. The file name is the id plus `.yaml`.

`status`:
- `stub`: a placeholder so edges can point at it. Needs only id, title, course, kind and status. Stubs are work to do, and the validator counts them.
- `draft`: written by an agent and passing the validator.
- `reviewed`: a human has signed it off. Agents don't edit reviewed nodes except through a job that says so.

`verification` says how far Lean can check the node:
- `formal`: the key statements of every KP have anchors.
- `partial`: some do.
- `informal`: none can be checked in Lean (e.g. univalent or homotopy-type-theoretic content, which Lean's type theory can't express; see §7).

## 3. Edges

There are three relations. Mixing them up is the commonest modelling error.

**`requires`** (gating). A requires B: a learner must have mastered B before starting A, under the viewpoint in force. Every edge has a `reason`: one sentence naming the specific dependency ("the proof takes the supremum of the set of points reachable…"). Store only the transitive reduction: if A requires B and B requires C, A does not also list C. The validator warns about redundant edges.

**`encompasses`** (review credit, used by FIRe-style scheduling). A encompasses B with weight w ∈ (0, 1]: a successful review of A also counts as w of a review of B, because practising A exercises B. The rubric for w is in `spec/STYLE.md`. B should be an ancestor of A under every viewpoint where both exist; the validator warns otherwise.

**`illuminates`** (non-gating cross-link). A illuminates B: learning A sheds light on B, typically a reinterpretation (often categorical, from the nPOV). It never affects gating or scheduling; lessons and the explorer use it.

## 4. Alternative routes: choice groups and viewpoints

Some topics can be reached by genuinely different routes, for example:
- finite products of compact spaces via the tube lemma, or via stability of proper maps under base change and composition;
- subspace, product and quotient topologies built by hand, or as initial and final topologies.

A **choice group** records such an alternative inside `requires`:

```yaml
requires:
  - node: ts.product-topology
    reason: The statement is about the product topology.
  - choice: product-compactness-route
    default: tube-lemma
    options:
      tube-lemma:
        - node: ts.tube-lemma
          reason: The classical proof covers a compact fibre by open rectangles and applies the tube lemma.
      universally-closed:
        - node: ts.compact-universally-closed
          reason: X × Y → Y → point is a composite of proper maps, and proper maps compose.
```

An option is a conjunction (a list of edges). It may be empty, meaning "no extra prerequisite on this route". A group id is global: every node that uses a group must give it the same option names and the same default.

A **viewpoint** chooses one option per group (`graph/viewpoints/*.yaml`); groups it doesn't mention take their default. A node with `only_in: [v, …]` exists only in those viewpoints, e.g. `ct.categories` exists only in `npov`.

### Semantics

Without viewpoints, the requires relation is an AND–OR graph: each node needs all of its plain edges and, for each choice group, all edges of *one* option. That is knowledge-space theory (Doignon–Falmagne): the feasible knowledge states are the sets K closed under these clauses (if A ∈ K, then K contains A's plain prerequisites and some option of each of A's groups). Planning over an AND–OR graph is a hard search problem in general.

Fixing a viewpoint V removes the disjunctions:

1. Active nodes: N_V = { n : n has no `only_in`, or V ∈ n.only_in }.
2. Edges: every plain edge, plus the edges of the option V picks in each group.
3. The result must be a DAG on N_V, and every edge's target must be active (an active node may not require a node that doesn't exist in V).

On that DAG:
- the feasible knowledge states are the down-sets;
- a learner who knows K and wants target t must learn ancestors(t) ∖ K, in any topological order;
- choosing reviews that cover everything due, using encompasses credit, is a weighted set-cover problem, and greedy is adequate.

`tools/plan.py` implements the path computation; the scheduler (later) implements the review choice.

## 5. What the validator checks

Errors fail CI; warnings are reported.

Errors:
- A file doesn't match its JSON schema.
- Ids: duplicate ids; a file name that doesn't match its id; an id whose prefix doesn't match its course's prefix.
- A node names a course that doesn't exist, or a section number the course doesn't have.
- A `requires`, `encompasses` or `illuminates` target doesn't exist; a `covers` item doesn't exist.
- A choice group is inconsistent across nodes (different option names or defaults), or a viewpoint picks an option that doesn't exist.
- For some viewpoint: a cycle (the cycle is printed), or an active node requiring an inactive one.
- A node `encompasses` itself, or lists the same target twice.

Warnings:
- A requires edge redundant under every viewpoint in which it is active.
- An encompasses target that isn't an ancestor under some viewpoint where both nodes exist.
- A draft or reviewed node with no anchors whose verification isn't `informal`.

Reports (`--report`):
- Per course and section: items covered by draft or reviewed nodes, items covered only by stubs, items uncovered, and estimated minutes against lecture count.
- Per viewpoint: node count, edge count, total minutes, longest path.

Anchor existence is checked by building `lean/` (see `tools/gen_anchor_check.py`), not by the validator: Lean is the authority on what exists in the pinned Mathlib.

## 6. Coverage vs route

Courses are taken from a syllabus (currently the Cambridge Schedules 2026–27) and say what must be in. Viewpoints and choice groups say how to get there. A node may cover items from several courses, and a supplementary course (e.g. `x-categories`) may have nodes that cover nothing in the syllabus but exist on one viewpoint's route.

## 7. Limits of formal checking

Mathlib sits on Lean 4's type theory, where `Prop` has definitional proof irrelevance, so uniqueness of identity proofs holds and univalence is inconsistent. Content that needs univalence (homotopy type theory, the "higher" part of the nPOV) can't be anchored in Mathlib. Such nodes are `verification: informal`, or are anchored in another checker (Agda's cubical mode, Rzk) through a future `library` value. At undergraduate level this rarely matters: Mathlib's topology is already structural (filters, Galois connections between lattices of topologies, a large category theory library), so the categorical route through point-set topology is almost fully anchored.
