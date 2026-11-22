# Archē knowledge graph

The vocabulary of the Archē knowledge graph: the topics a learner meets, the relations between them, and the routes and checks built on them. `spec/SCHEMA.md` is the authority; this file only names things, and where the two disagree the schema wins.

## Language

### Nodes

**Node**:
One schedulable topic that a learner can be taught, practise and review in a single sitting of 15–45 minutes. The node is the unit of gating.
_Avoid_: lesson, concept, card

**Knowledge point** (KP):
One move a learner can make inside a node (state a result and recognise its hypotheses, carry out a standard argument, produce or refute an example), taught as one worked example followed by practice. KPs are the unit of spaced repetition; a node has 2–5 of them.
_Avoid_: step, skill, learning objective

**Stub**:
A placeholder node with only an id, title, course, kind and status, so that edges can point at it before it is written. A stub is work still to do.

**Draft**:
A node written by an agent that passes the validator but that no human has signed off yet. Every new node starts as a draft.

**Reviewed**:
A node a human has signed off. Agents change it only through a job that names it.

### Edges

**Requires**:
The gating relation: A requires B when a learner must have mastered B before starting A, under the viewpoint in force. Every requires edge carries a reason naming the specific use, and only the transitive reduction is stored.
_Avoid_: depends on (that is for jobs), related to

**Encompasses**:
The review-credit relation: A encompasses B with weight w in (0, 1] when a successful review of A also counts as w of a review of B, because practising A exercises B. B should be an ancestor of A.
_Avoid_: subsumes, includes

**Illuminates**:
A non-gating cross-link: learning A sheds light on B, typically by reinterpreting it (often categorically). It never affects gating or scheduling.
_Avoid_: see also, related to

### Routes

**Choice group**:
A named alternative inside a node's requires: a set of options, each a (possibly empty) list of requires edges, plus a default; a learner needs all the edges of one option. The group id is global, so every node that uses it gives the same option names and default.
_Avoid_: branch, alternative prerequisite

**Viewpoint**:
A choice of one option in every choice group (a group it doesn't mention takes its default), which turns the requires graph into a plain DAG. The current viewpoints are `classical` and `npov`.
_Avoid_: track, curriculum, perspective

**Active node**:
A node that exists under a given viewpoint: it has no `only_in`, or its `only_in` names that viewpoint. Only active nodes are part of that viewpoint's DAG, and an active node may not require an inactive one.

### Coverage and checking

**Coverage item**:
One item of a course's syllabus, named `<course-id>#<item-id>`, which some draft or reviewed node must cover. Courses say what must be covered, never in what order.
_Avoid_: requirement, objective

**Anchor**:
A fully qualified Lean name in the pinned Mathlib (or in Lean core) for the main statement or definition of a knowledge point. Lean, not the validator, decides whether an anchor exists.
_Avoid_: reference, citation

**Verification tier**:
How far Lean can check a node: `formal` (the key statements of every KP are anchored), `partial` (some are) or `informal` (none can be, for example univalent content).

### Work

**Job**:
One small unit of agent work that ends in one pull request a human can review in 20–30 minutes. It moves through open, claimed, in-review and done.
_Avoid_: task, ticket (those are GitHub issues)
