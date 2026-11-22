# Style guide

Every agent loads this file before writing content. When agents keep making the same mistake, fix this file, not each output.

## Granularity

- A node takes 15–45 minutes for a learner meeting it for the first time. If it takes longer, split it. If it takes under 15, merge it into a neighbour, unless it's a named theorem that later nodes cite on its own.
- A node has 2–5 knowledge points (KPs). A KP is one move a learner can make: state X and recognise its hypotheses; carry out a standard argument; produce or refute an example. Write each as a short noun phrase or imperative, not as a paragraph.
- One schedule bullet becomes 1–3 nodes. A 24-lecture course ends up with roughly 60–100 nodes.
- Minutes are a first estimate for a capable learner. Learner data will correct them later.

## Requires edges

- A requires B only if, under some viewpoint, a learner can't follow A's statement or its taught proof without B. "B is related" is not enough; use `illuminates` for that.
- Every edge gets one sentence naming the specific use: "The proof takes the supremum of…", "The statement is about the product topology.", never "needed".
- Store the transitive reduction. Before adding A → C, check whether some B with A → B →…→ C already exists. The validator warns about redundant edges; fix them.
- When two viewpoints really do teach A by different routes, use a choice group (spec/SCHEMA.md §4). Don't encode a route difference with `only_in` on edges, and don't put both routes' prerequisites on the node.
- Prerequisites that cross courses are normal. Point at the earlier course's node, creating a stub there if needed.

## Encompasses weights

| w | Meaning |
|---|---|
| 1.0 | Every successful attempt at A performs B in full (B is a step that can't be skipped, at full difficulty). |
| 0.5–0.7 | A's standard proof or exercises use B as a substantial step most of the time. |
| 0.2–0.4 | A uses B lightly or only in some exercises. |
| (none) | A merely mentions B. Don't add an edge. |

B must be an ancestor of A. Weights are priors; learner data will re-estimate them.

## Viewpoints

`classical` follows the source syllabus (currently the Cambridge Schedules) and its usual textbooks.

`npov` follows the nLab's higher-structures point of view, at undergraduate strength:
- Universal property first, construction second. Define the product topology by what maps into it do, then exhibit it.
- Prefer maps to elements: connectedness as "every map to the discrete two-point space is constant"; open sets as maps to Sierpiński space.
- Name the category. Top is a category, homeomorphisms are its isomorphisms, and a "topological property" is one invariant under isomorphism.
- Name adjunctions when they're present: induced and coinduced topologies are adjoint; discrete ⊣ forget ⊣ indiscrete.
- Keep the topological content honest. When the nPOV repackages an argument rather than avoiding it (a closed projection still needs a tube-style argument), say so in `lesson_notes`.
- The "higher" part of the nPOV (homotopy types, ∞-categories) belongs to later courses. Don't force it into undergraduate point-set topology.

Supplementary nodes that only the nPOV route needs (categories, functors, Galois connections, universal properties) live in `x-categories` with `only_in: [npov]`.

`lesson_notes` holds per-viewpoint guidance for whoever writes the lesson later. Keep it to one or two sentences.

## Anchors

- An anchor is a fully qualified Lean name in the pinned Mathlib (`lean/lakefile.toml`). Check it exists before writing it: with lean-lsp-mcp (`lean_hover`, `#check`), or by searching the Mathlib source at the pinned commit. Never guess a name from memory; Mathlib renames often (`QuotientMap` became `Topology.IsQuotientMap`).
- Anchor the main statement or definition of each KP if one exists. Two to five anchors per node is typical.
- A name defined in Lean core (e.g. `Function.Injective`, `Setoid`) gets `library: lean-core`.
- If the content isn't in Mathlib, leave anchors empty, set `verification` to `partial` or `informal`, and add a line to `jobs/open/` proposing a Prove2Me mission or a local formalisation.

## Coverage

- Every schedule item of a course must end up in the `covers` of some draft or reviewed node. One node may cover several items, and one item may be covered by several nodes.
- Course files paraphrase the syllabus. Don't paste long passages from it.

## Off-platform prompts

Optional. One open-ended question a learner could think about on a walk, not an exercise with an answer key. Good: "Which properties of ℝ did the proof that [0,1] is connected actually use? Find an ordered set where it fails." Bad: "Prove that [0,1] is connected."

## Language

English, British spelling where Cambridge uses it (neighbourhood, generalise). Write mathematics in Unicode (ℝ, ⊆, →), not LaTeX, in YAML strings.
