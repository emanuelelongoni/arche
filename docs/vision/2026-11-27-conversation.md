# Vision conversation, 27 November 2026

A record of one working conversation between the repo owner and Claude about a change of direction for Archē. Part 1 is the handoff: read it to pick things up. Part 2 is the full transcript, with the owner's messages verbatim.

**Nothing in the repo was changed in this conversation except this file.** The specs, glossary, jobs, README and `CLAUDE.md` still describe the old model.

**If you are an agent starting a new session:** do not pick up a job from `jobs/open/`. Jobs J0001–J0005 are scoped to Cambridge courses, which the owner has dropped. Read this file, then ask the owner what they want next.

---

## Part 1: Handoff

### The change of direction in one paragraph

Archē stops being a graph of topics on routes through university courses. It becomes a growing public library of small pieces built around several kinds of thing a learner can master: statements (definitions and theorems), proofs (many per theorem), moves (proof techniques, and also ways of making definitions and conjectures), and examples. Every explanation, worked example and exercise says what you need to know to use it, and a learner sees only what is within their reach. Curricula are recommendations computed over the library, not containers. The owner intends it as a resource for the world, from undergraduate level up to research level.

### Decided by the owner

1. **A resource for the world, with many points of view.** The global `classical`/`npov` switch goes away. A viewpoint is whatever the learner's current knowledge lets them see, as in Thurston's list of ways to think about the derivative.
2. **New stack for new work:** Next.js, Vercel and Neon.
3. **Statements, proofs and techniques are separate things,** each with its own material and progress. A topic presents many techniques; each technique is mastered across several topics. The balance of directness and variety matters.
4. **Many proofs per theorem,** found with AI where needed and simplified over time. Contributions to research in suitable venues are welcome.
5. **No courses.** Drop Cambridge and all university-course concepts from the basic approach, not just the presentation. The library is mini-lessons in organic clusters. Recommendations depend on intended depth, breadth and time. One target is the "honours-degree equivalent": the essential mathematics for three years of full-time study after Math Academy, with horizontal electives (extra sections per branch) and vertical or oblique electives (other macro-topics, such as category theory).
6. **Proof input.** When a learner enters a proof, the system checks it, works out which techniques it used, and presents other approaches. Over time it notices which techniques the learner leans on and widens their repertoire. It prevents forgetting and promotes deepening.
7. **Unlock rule.** A theorem unlocks only when its statement is fully intelligible and at least one known proof is accessible.
8. **Content stays in git** (YAML, validated, Lean-checked, reviewed in PRs) and syncs into Neon. Only learner data lives natively in the database.
9. **Ways of making definitions, theorems and other abstractions must be seen and practised,** to train pattern recognition and theory building.
10. **Any order of study.** A learner may study category theory (or any topic) before groups and rings. Dependencies must be granular enough to allow it. Bottom-up, top-down and mixed approaches are all supported, including "I want topic Y and have exactly this set of prerequisites to cover".
11. **External formal libraries.** Archē may use Lean libraries such as Tau Ceti, and may contribute to them.
12. **A deferred research question.** Whether logic, category theory, model theory, proof theory, Caramello's bridges, sheaves or other advanced structures already describe what Archē assesses, or offer the best way to link its contents, is to be assessed later by dedicated multi-agent sessions. The owner says they lack the mathematical knowledge to judge it.

On logical tools (contradiction, contrapositive and so on) the owner is unsure. They see value in proving one result with several logical tools and seeing whether the rest of the proof changes, and think this is mostly seen in the actual proofs.

### Proposed by Claude and accepted by the owner

- **Trust ledger.** A result may be used "on trust" before any proof is in reach, recorded as a debt to repay later.
- **Examples and counterexamples are a fourth kind,** alongside statements, proofs and moves.
- **Idea and packaging.** A proof has an idea and a logical packaging (direct, contrapositive, contradiction). The library groups variants under one idea. The owner's answer was "It surely seems so."

### Proposed by Claude, not yet answered

These came up in the replies and the owner has not yet said yes or no.

- **Prerequisites attach to proofs.** A statement needs only what is required to read it.
- **The exercise is the atom.** Each exercise counts as practice for every statement, proof and move it exercises. This replaces `encompasses`.
- **Which proof is shown is a scheduling decision.**
- **New knowledge reopens old topics.** Views that were out of reach become available, which reviews and deepens at once. `illuminates` becomes real material.
- **A technique entry** records its cue, outline of steps, relatives, where it fails, and common pairings. The catalogue grows bottom-up from tagged proof steps.
- **A proof either introduces a technique or assumes it.**
- **Moves** as one kind covering proving, defining and conjecturing. They are practised where the library holds both ends of a generalisation or analogy.
- **Each definition records its rationale:** the examples it captures, the theorems it was designed to make true, the alternatives rejected.
- **Proofs stored as outlines you can zoom.** A mastered technique lets a step collapse.
- **Understanding has testable facets:** state it, say why each hypothesis is needed, outline and expand a proof, give a second proof, use it, place it.
- **Record what the learner did and derive mastery from it,** so kinds can be added or split later without losing progress.
- **The library reports its own thin spots** (depth). Breadth needs the owner's own canon.
- **Analogy links carry an explicit dictionary** (normal subgroup ↔ ideal), so they can become formal translations later.
- **Interview mathematicians with AI** to capture oral culture as attributed views and rationales.
- **"Abstraction after several instances"** is a default suggestion only. The owner rejected it as a gate.
- **`only_in` goes away** along with the viewpoint switch. This is Claude's inference; the owner confirmed only that the switch goes.

### Open questions for the owner

From the last reply:

1. Is trust a dial each learner sets, or a rare exception the system grants?
2. Should Tau Ceti be only a source of anchors, or also something Archē contributes to?
3. The README says monk-mathematicians study mathematics "much of it machine-produced". Is auditing and digesting machine proofs central to the idea, or one skill among many?

Not yet discussed:

4. What exactly a learner is assumed to know on arrival ("post-Math Academy").
5. What the canon for the "honours-degree equivalent" contains, and who drafts it.

The owner also said: "I'll add much more about my vision later."

### What this means for the repo

Noticed, not changed:

- **GitHub Pages and DNS setup: on hold.** The site moves to Vercel. The `site` workflow on `main` still fails at its last step because Pages was never enabled.
- **J0006 (human review of the gold-standard slice): on hold.** The node shape is changing.
- **J0001–J0005: obsolete.** All are scoped to Cambridge courses. If a nightly agent task exists, it should stay paused.
- **The 47 draft nodes are raw material.** Each mixes a statement with one proof and will need re-cutting.
- **Courses, coverage items, course-prefixed ids, viewpoints, choice groups and `only_in`** all belong to the old model.
- **`GLOSSARY.md` needs resetting.** It defines node, viewpoint and choice group, and puts "lesson" on its avoid list.
- **`README.md` is out of date** even for the old model: it says eight open jobs and treats J0007 as pending.
- **`CLAUDE.md`, `spec/SCHEMA.md` and `spec/STYLE.md`** still instruct agents in the old model.
- **The Astro site in `site/`** is superseded for new work. Its TypeScript route planner may be reusable.

### Suggested next steps

Claude's suggestions, for the owner to choose from:

1. The owner adds the rest of their vision and answers the open questions.
2. Write the settled parts as a vision document and a first decision record under `docs/adr/`.
3. Reset `GLOSSARY.md` to the new vocabulary.
4. Draft the new data model, then re-cut one small cluster by hand as a test. "Finite products of compact spaces" is a good candidate: it already has two proofs with different prerequisites.
5. Write the brief for the deferred multi-agent assessment of formal structures.
6. Plan the Next.js and Neon application, including how git content syncs into the database.

### Provisional vocabulary

None of these terms is settled.

| Term | Meaning |
|---|---|
| Statement | A definition or theorem |
| Proof | One argument for a statement; many per theorem |
| Move | A way of making mathematics: proving (the owner's "technique"), defining, or conjecturing |
| Artefact | What moves produce: statements, proofs, examples |
| Example | A specific object, including counterexamples; one example can serve many statements |
| Idea / packaging | The mathematical content of a proof, and its logical form |
| View | One way of explaining something, with its own prerequisites |
| Facet | One testable aspect of understanding a statement or technique |
| Trust ledger | The record of results a learner has used without studying a proof |
| Thin spot | A place where the library lacks depth, such as a theorem with one proof |

### Caveats on the facts

Everything cited in the transcript was checked by web search on 27 November 2026, with these limits:

- **Read as abstracts or summaries only:** Kerr and Booth (1978); Lakatos (table of contents only); Gowers's post (link found, post not read).
- **Tau Ceti:** read from its GitHub README only. The lean-lang.org page and the Mathlib Initiative roadmap were unreachable from the session.
- **Self-reported figures:** the automatic textbook formalisation paper; Mathlib counts vary by snapshot date.
- **AI provers:** names confirmed, rankings not.
- **From memory, not confirmed by search:** Lean "blueprints"; what became of the Tricki.
- **Claude's account of what AI models have absorbed of oral culture** is a self-report it cannot check.

---

## Part 2: Transcript

Interim progress notes are left out. Headings inside Claude's replies are demoted to fit this document. "[…]" marks a short remark about user accounts that was trimmed.

### 1. Owner

> What is the state of the repo? […] worked on this a week ago, I've forgotten the details (of the repo, not of the idea behind and beyond it).

### 1. Claude

The repo is in good shape but has stood still since 22 November. You built it all that day and merged six PRs ([#1](https://github.com/emanuelelongoni/arche/pull/1)–[#6](https://github.com/emanuelelongoni/arche/pull/6)). There have been no commits, PRs or issues since, and every job is still unclaimed. I changed nothing; my branch is identical to `main`.

#### What's waiting on you

1. **The website has never deployed.** On `main` the site builds and every check passes: planner parity tests, link check and 38 browser tests. The workflow fails only at the last step, because GitHub Pages isn't turned on for the repo. To fix it:
   - Follow "Deployment: what the owner must do, once" in `docs/specs/site-v0.md`. It covers verifying the domain, setting Settings → Pages → Source to GitHub Actions, adding the custom domain, and the DNS records.
   - Then re-run the [failed run](https://github.com/emanuelelongoni/arche/actions/runs/45058550950), or push to `main`. Starting the workflow by hand won't deploy, because the deploy steps only run on a push.
   - I didn't check whether arche.academy resolves today.
2. **The nightly agent loop doesn't seem to be running.** The README says a scheduled Claude Code task takes the next job each night. I found no scheduled tasks […], and nothing has come out of one in 5 days, so it's either not set up or not working.
3. **J0006 is your review job, and it's top priority.** You're meant to review the gold-standard slice (Topological Spaces, Analysis II §3 and the category-theory nodes). You set `status: reviewed` on nodes you accept and correct `spec/STYLE.md` where you disagree. No node is `reviewed` yet. This matters because the agents use those nodes as their model of quality.

#### What the repo is

The repo is "content as code". A **node** is one topic of 15–45 minutes, with 2–5 knowledge points, and lives in its own YAML file under `graph/nodes/<course>/`. Nodes are linked by three kinds of edge:
- **`requires`** is gating: you must know B before A. Each edge carries a reason.
- **`encompasses`** gives review credit: reviewing A counts partly as reviewing B.
- **`illuminates`** is a cross-link that never gates.

A **choice group** marks a point where two routes really differ, such as building topologies by hand versus as initial/final topologies, or proving compact products with the tube lemma versus universal closedness. A **viewpoint** (`classical` or `npov`) picks one option in each group, which turns the graph into a plain DAG. **Anchors** tie each node to Mathlib names and are checked by building the Lean project. Courses paraphrase the Cambridge Schedules 2026–27 and say what must be covered, not the order.

The main tools:
- `tools/validate.py` checks the graph and reports coverage.
- `plan.py` computes a learner's path to a target.
- `render.py` draws the graph.
- `gen_anchor_check.py` generates the Lean file that checks anchors.
- `export_site.py` produces the JSON the website is built from.

`site/` is the Astro website, generated from `graph/`. Its route planner is a TypeScript copy of `plan.py`, tested to give the same answers.

**Checks:** the validator passes with 0 errors and 0 warnings, and all 20 tests pass when I run them here. In CI on `main`, the `validate` workflow passes, including the Lean anchor build. I didn't run Lean here.

#### Content so far

There are 56 nodes: 47 draft, 9 stubs, none reviewed.

| Course | Items covered | State |
|---|---|---|
| IB Topological Spaces | 28/37 | §1–3 complete; §4–5 (manifolds, surfaces) missing |
| IB Analysis II | 11/34 | §3 (metric spaces) complete, plus uniform continuity |
| IA Analysis I | 0/29 | 5 stubs |
| IA Numbers and Sets | 0/38 | 3 stubs |
| IA Vectors and Matrices | – | no syllabus items in the course file yet; 1 stub |
| x-categories (extra, nPOV route only) | – | 5 nodes |

The two viewpoints differ as intended:
- `classical` has 49 nodes, 73 `requires` edges and 1130 minutes.
- `npov` has 56 nodes, 90 `requires` edges and 1370 minutes.
- The route to Heine–Borel is 26 topics classically and 32 under nPOV.

#### Job queue (`jobs/open/`)

- **Can start now:**
  - **J0001**, Numbers and Sets in full. This is the next agent job under the rule in `CLAUDE.md`.
  - **J0004**, Topological Spaces §4–5.
  - **J0005**, Vectors and Matrices.
- **Waiting on J0001:** **J0002** (Analysis I), then **J0003** (the rest of Analysis II).
- **J0006** is your review, above.
- **J0008** is the monthly Mathlib update. Mathlib is pinned to a 22 November commit, so it isn't due until late December.
- **Done:** J0007 (first Lean build) is in `jobs/done/`.

#### Small loose ends

- The README is out of date: it says eight open jobs and treats the first Lean build as still to come. Seven are open and J0007 is done.
- The six merged PR branches are still on GitHub.
- Actions warns that some actions target the deprecated Node 20. It's harmless for now.

### 2. Owner

> I've changed my mind on a lot of topics, and had quite a few new ideas.
>
> I intend this website to be a resource for the world, not just a personal tool, so more one nPOV. This is handled by illumination and example/exercise-level prerequisites/illumination. A lesson may have an extensive library of examples/exercises/explainantions/etc, but only those accessible to the knowledge profile of the user are presented (a la Thurston's 20 views on the derivative).
>
> Next, I've become comfortable creating full-stack websites with NextJS + Vercel + Neon, so we'll have to change stack for new, actual work.
>
> Next is a separation of topics/subjects/theorems, proofs, and methods/techniques. One often studies a new topic, say a particular theorem, and one of its proofs, which uses a chain of techniques. More than a lemma, a technique is a sort of strategy. There are (mostly ubiquitous) logical techniques that are very well practiced (contradiction, contrapositive, for-all-elimination, etc), but also more specific techniques (in algebra, the projection-and-lift strategy: "kill the quotient, trap the kernel"). To master a technique, it's important to have worked examples and exercises in a wide variety of contexts; the technique likely comes in a family, and it's important to see where it works and where it doesn't, as well as adaptations, and common (and creative!) pairings of the technique with others to handle more complex results. So a topic presents many techniques, and each technique is mastered across several topics. This double (or multiple) encoding is essential for deep learning. It reminds me of the famous 2-metres vs 1-and-3-metres disk-throwing experiment. The optimal 'balance' of directness and variety is key.
>
> Progress and lessons are not only about topics, but also on proofs and techniques.
>
> So we need to create a data structure resilient enough to connect subjects, proofs, and techniques, and undoubtably more things in the future, across an ever-expanding scale. In the case of theorems, we are not content with one proof, but we wish to use (and thus often discover with AI) many proofs, and simplify those available. We may even contribute to math research along the way in appropriate venues (e.g. those allowing human-AI interactions).
>
> --
>
> We will not have out-of-the-box classes. Drop all references to Cambridge or any "class" or usual univeristy concepts, not just in 'marketing' but in the basic approach we take. Instead, we'll feature an ever expanding library of well-integrated mini-lessons forming organic clusters. We'll certainly generate recommendations depending on intended depth, breath, time, etc. For example, a user may desire to have the rough equivalent coverage of a (honours) undergraduate degree, by which I really mean, the essential math that should be studied by all in three years of full-time study post-Math Academy, so we'll determine the minimum breath and depth needed, with something unimaginable in most maths departments: topic-level, horizontal 'electives' (sets of extra sections for each branch), plus vertical/oblique 'electives' (different macro-topics, e.g. category theory).
>
> --
>
> Many mathematicians don't feel they thoroughly understand even their own work. We want to end that eventually, fostering a deep understanding of all of math, from undergraduate to master-s to PhD to research-level, starting from undergraduate.
>
> --
>
> When a user inputs a proof, the system not only checks it, but also tries to understand the techniques used. It then presents different approaches.
>
> Across different uses, the app will see what techniques the user leans towards, and try to expand his repertoire. So the system will prevent unlearning (forgetting learned topics, proofs, and techniques), but also promote expansion and deepening of learning.
>
> I'll add much more about my vision later.
>
> For now, try to get and fill in the gist of my fragile ideas. The best way to do so is to try to deepen and expand that yourself, and checking in with me to see if we're thinking on the same wavelength.

### 2. Claude

Here's the gist as I understand it, then where I'd push it further, then three questions.

#### What I think you're saying

The unit is no longer a topic on a route through a course. It's a growing library of small pieces built around three kinds of thing a learner can master:
- **statements**: definitions and theorems;
- **proofs**: many per theorem;
- **techniques**: strategies that recur across proofs, studied directly and not just used as labels.

Each kind has its own material and its own progress. Every explanation, worked example and exercise says what you need to know to use it, and you see only the ones within your reach. A curriculum such as "honours-degree equivalent" is a recommendation computed over the library, not a container.

I read "more one nPOV" as "many points of view, not one". On that reading the global classical/nPOV switch goes away, and your viewpoint is whatever your current knowledge lets you see, as in [Thurston's list](https://arxiv.org/abs/math/9404236) of ways to think about the derivative. Tell me if I misread.

#### A case already in the repo

`ts.finite-products-compact` today has a "choice group": tube lemma or universal closedness, picked by viewpoint. In the new model that is one statement with two proofs, each with its own prerequisites and techniques. A third proof can be added later without touching anything else.

The tube-lemma proof uses compactness to turn a choice made at each point into finitely many choices that work everywhere. The same move drives the Lebesgue number lemma and uniform continuity on compact spaces. Those are the technique's second and third contexts.

#### Where I'd take it further

These are my additions; push back freely.

1. **Prerequisites attach to proofs, not theorems.** A statement needs only the definitions required to read it, and a later result that cites it needs only the statement. Choice groups and viewpoints then become unnecessary. The cost is that "what do I need for X" has alternatives in it again, which `spec/SCHEMA.md` used viewpoints to avoid. Planning becomes "choose the cheapest set of proofs", which is harder but, I think, manageable.
2. **The exercise is the atom, and it counts for several things.** A worked example or exercise sits at an intersection: this theorem, this proof, these techniques. Doing it is practice for each. That is your double encoding, and it replaces `encompasses`. Your throwing experiment is [Kerr and Booth (1978)](https://journals.sagepub.com/doi/10.1177/003151257804600201): children who practised beanbag throws at 2 and 4 feet beat those who practised only at 3 feet, when tested at 3 feet. For us it becomes a scheduling rule: when a technique is due, pick an exercise in a context where you haven't met it.
3. **Which proof you're shown is a scheduling decision.** With three proofs available, the system can pick the one whose techniques you most need next. Breadth then means which statements you cover; depth means how many proofs, views and techniques you have per statement.
4. **New knowledge reopens old topics.** When you learn categories, dormant views of the product topology come within reach. Showing them reviews the old topic and deepens it in one go, so preventing forgetting and promoting deepening share a mechanism. `illuminates` becomes real material instead of a cross-link.
5. **A technique entry needs more than a name.** It needs the cue that should make you think of it, its outline of steps, its relatives, where it fails and why, and its common pairings. I'd grow the catalogue bottom-up: tag each proof's steps, and promote a recurring move to a named technique once it appears in several proofs in different areas. The closest precedent I know is the Tricki, a wiki of techniques Gowers launched in 2009; I haven't checked what became of it.
6. **Proof input depends on step-tagged library proofs.** If every library proof is stored as steps tagged with techniques and results used, understanding a user's proof means matching it against those, and showing other approaches means showing the ones it didn't match. A valid proof that matches none is a candidate for the library, which is your research pipeline. Checking free-text proofs reliably is the hardest technical piece of the whole vision.

#### What this does to the repo

- **Hold off on the Pages/DNS setup and the J0006 review.** The stack and the node shape are both changing, so this reverses my earlier list.
- **Jobs J0001–J0005 are obsolete.** They are all scoped to Cambridge courses. If a nightly task exists […], keep it paused.
- **The 47 draft nodes are raw material.** Each mixes a statement with one proof and will need re-cutting.
- **Something must replace coverage.** Without courses, nothing says what's missing. I don't have a proposal yet.
- **The glossary needs resetting.** It defines node, viewpoint and choice group, and bans "lesson".

#### Questions

1. Should a learner be able to build on a theorem knowing only its statement? I'd allow it in the data model and let the recommendation layer demand at least one proof by default.
2. What earns a technique its own entry and progress? In particular, do contradiction and contrapositive get the same treatment as "kill the quotient, trap the kernel", or are they a background layer?
3. Does content stay in git (YAML, validated, Lean-checked, reviewed in PRs) and sync into Neon, with only learner data living natively in the database? I'd recommend that, since it keeps the agent-and-review loop.

Sources:
- [Kerr & Booth 1978, abstract](https://journals.sagepub.com/doi/10.1177/003151257804600201) and [summary](https://coachsci.sdsu.edu/csa/vol31/kerr.htm); I read these, not the paper itself.
- [Thurston, "On Proof and Progress in Mathematics"](https://arxiv.org/abs/math/9404236)
- [Timothy Gowers, Wikipedia](https://en.wikipedia.org/wiki/Timothy_Gowers), for the Tricki's 2009 launch

### 3. Owner

> You are not misreading.
>
> On your questions:
>
> 1. It makes sense to 'unlock' a theorem only when the statement is fully intelligible and at least one known proof is accessible.
> 2. I don't know for sure. It does seem to me that, though mathematicians become soon well-versed with basic logic tools like contradiction, contrapositive, etc, there may be value in attempting to prove a result with multiple logical tools, and seeing whether the rest of the proof meaningfully changes. This is mostly seen by the actual proofs.
> 3. Yes, I agree with your recommendation.
>
> Also observe that modes of making definitions, theorems, or other abstractions is also something that needs to be seen and practiced; this way, we'll train pattern recognition and theory building.
>
> Again, think deeper and go farther.

### 3. Claude

Going further in three parts: what your new point turns into, what your unlock rule implies, and five additions of mine. Every new term is provisional.

#### Your new point: moves

**1. Proof techniques, definition-making and conjecture-making are one kind of thing.** Call them *moves*: ways of making mathematics. Call what they make *artefacts*: statements, proofs, examples. Each artefact links to the moves that produced it.

- **Proving moves** make proofs. This is your "technique".
- **Defining moves** make definitions. One is "read off what the proof used, and name it". The style guide already has a prompt of this kind: which properties of ℝ did the proof that [0,1] is connected actually use? Lakatos's *Proofs and Refutations* calls such concepts [proof-generated](https://assets.cambridge.org/97811071/13466/toc/9781107113466_toc.pdf), with uniform convergence as a case.
- **Conjecturing moves** make statements. Carrying the first isomorphism theorem from groups to rings forces you to invent the ideal.

Moves are practised where the library holds both ends: a special case and its generalisation, or two analogues. As you say, seen then practised: the move is shown in worked cases, then the learner makes it at the next such joint.

That gives a rule for when to offer an abstraction: once you've met its pattern several times. Category theory arrives after you've seen the same theorem in groups, rings and vector spaces. Each definition would also record its rationale: the examples it was built to capture, the theorems it was designed to make true, and the alternatives rejected.

**2. Logic is a proof's packaging, separate from its idea.** Euclid's proof of infinitely many primes is often told as a contradiction, but its idea is direct: from any finite list, build a prime outside it. So, tentatively:
- The library groups variants under one idea.
- "Repackage this proof; does anything else change?" is an exercise type.
- The system notes which packaging you reach for, with no separate drills.

Deciding that two proofs share an idea is a recorded human judgement; nobody has a test for it. [Gowers has a post on the question](https://gowers.wordpress.com/2007/10/04/when-are-two-proofs-essentially-the-same/), which I haven't read.

#### What your unlock rule implies

- **The planner now chooses among proofs.** A proof is within reach when everything it uses is learned, and that applies all the way down.
- **A proof either introduces a technique or assumes it.** A technique is first met inside some proof, so it can't always be a prerequisite. Each technique needs a few easy proofs that serve as its introductions.

#### My additions

**3. Store proofs as outlines you can zoom.** The top level is the outline and every step expands; [Lamport proposed this](https://www.microsoft.com/en-us/research/publication/write-21st-century-proof/) for written proofs. A mastered technique is what lets a step collapse to "by the usual compactness argument". That is also a working definition of understanding your own work: you can view the proof at any resolution and expand any step on demand.

**4. Understanding has facets that can each be tested.** For a theorem:
- state it and spot its hypotheses;
- say why each hypothesis is needed;
- outline a proof and expand a step;
- give a second proof or view;
- use it;
- place it among its generalisations.

"Why each hypothesis is needed" calls for counterexamples. That makes examples a fourth kind: the topologist's sine curve serves many statements. For techniques, choosing one unprompted is a different facet from carrying it out when told.

**5. Record what the learner did, and derive mastery from it.** You added a kind between two messages, and that will keep happening. If we store each attempt and tag exercises with what they exercise, we can re-tag and recompute when a technique is split or a kind is added. Nobody loses progress.

**6. The library reports its own thin spots.** This closes the gap I left open last time, in two parts.
- **Depth:** the validator lists thin spots:
  - a technique with fewer than three contexts;
  - a theorem with one proof;
  - a definition with no rationale;
  - a hypothesis with no counterexample.

  Each becomes a job. Some are proof requests for AI, such as "a proof of X that avoids Y", which is where new proofs come from.
- **Breadth:** these rules can't see a whole missing area. Your own canon, the "honours-degree equivalent", has to list what should exist.

The Lean project today only checks that anchor names exist. If library proofs were formalised, Lean could also report what each proof really depends on.

**7. A trust ledger.** Your rule stands; this is a possible exception, not a reopening. The Jordan curve theorem can be stated early, yet every proof is long or needs later machinery. Under the rule, everything that uses it stays locked for a long stretch. The alternative is a marked "taken on trust" use, recorded as a debt to repay when a proof comes within reach. At research level this is unavoidable: almost everyone who uses the classification of finite simple groups takes it on trust. The planner could then give a reading plan for any target, including a research paper: what you lack, and what you would be trusting.

#### Questions

1. Do you allow the "taken on trust" exception, tracked as a debt?
2. Are examples and counterexamples a fourth kind, alongside statements, proofs and moves?
3. Does the idea/packaging split match what you meant by trying several logical tools on one result?

Sources:
- [Lakatos, *Proofs and Refutations*, table of contents](https://assets.cambridge.org/97811071/13466/toc/9781107113466_toc.pdf); I confirmed only the contents page.
- [Lamport, "How to Write a 21st Century Proof"](https://www.microsoft.com/en-us/research/publication/write-21st-century-proof/)
- [Gowers, "When are two proofs essentially the same?"](https://gowers.wordpress.com/2007/10/04/when-are-two-proofs-essentially-the-same/)

### 4. Owner

> 1. Yes
> 2. Yes
> 3. It surely seems so.
>
> What if a student has already heard of category theory (or topic X), and would like to study it before going deep into group theory, ring theory, etc? We must make granular dependencies to allow this to happen; and what if someone badly wants to study topic Y, but has exactly this poset of prerequities to cover? The point is, we may have bottom-up and top-down approches, mixed.
>
> Now a real question to you. It appears to me that mathematical logic, category theory, proposed foundations of mathematics, model theory, proof theory, invariant theory, bridges techniques, and branches of math I don't even know the existence of--these may already objectify what we are trying to assess. Also, perhaps the best way to 'link' the innumerable things in our project (and perhaps their evolution!) is found in more advanced mathematical structures (I don't know anything about sheaves, but just saying...), even exotic ones.
>
> That question is really one you, in dedicated multi-agent sessions, at a later stage, need to assess; I do not have the mathematical knowledge to do that.
>
> Another matter: the math that is already formally proven. We may need to use external learn libraries, like TauCeti and beyond. If necessary, we may also contribute. I don't know much about this whole (growing!) ecosystem, but you can give me a rough idea of what I need to know.
>
> What about the role of computation and simulation in mathematical learning? And of visualisation?
>
> What of that is accessible to AI models, and what only to the oral culture in top math departments? Again, no knowledge of any of that!
>
> Again, think deeper and farther. What great advances are possible with AI (+ existing tools; e.g. SRS + AI + a curated data sctructure is not just AI) that were not available before? Besides this question, dance around to make novel, magnanimous pedagogical breakthroughs in advanced mathematics.

### 4. Claude

You're right about order, and it corrects something I proposed, so I'll start there.

#### Studying in any order

- **My rule becomes a suggestion.** I said category theory should arrive after groups, rings and vector spaces. That is now a default recommendation, never a gate.
- **A concept needs only what its definition needs.** For categories that is sets and functions. "Groups form a category" needs groups, and that prerequisite sits on the example. Start with categories and you see the examples within your reach, with an honest count (say, 6 of 40). Learn groups later and that example opens.
- **Target-first already works with your unlock rule.** The planner computes exactly the missing prerequisites for a target. The requirement on us is granularity: each prerequisite names the specific statement used, never "group theory".
- **Trust is a separate dial.** Taking a theorem on trust amounts to viewing its proof at zero zoom. The ledger must then tell a step you collapsed through mastery from one you never opened.

#### Do existing fields already describe this?

This is a first take, not the assessment you deferred. These fields describe the skeleton (dependencies, translations, learner states) and not the ideas. I read "bridges" as Caramello's toposes-as-bridges programme.

| Field | What it offers us | Limit |
|---|---|---|
| Knowledge space theory | Learner states with alternative prerequisites, which is your unlock rule | Says nothing about content |
| Formal concept analysis | Turns the "which exercise exercises what" table into natural clusters | Descriptive only |
| Theory graphs (MMT, "little theories") | Small theories linked by translations that carry theorems across | Formal theories only |
| Proof theory | Proofs as objects; Hilbert's 24th problem asks for the simplest proof | Still unanswered |
| Categorical data migration | Schemas as categories, data moved along schema maps | Doesn't cover evolving a live schema, as far as I found |

- **Caramello's programme** transfers results between theories that share a classifying topos. Its reach outside logic is disputed.
- **Invariant theory** is a branch of algebra, not a theory about mathematics. "Find an invariant" is one of our moves.
- **Sheaves** describe data given locally that glues consistently. Whether "what each learner can see" has that shape is for the later sessions.

Those sessions should ask of each candidate: what does it compute for us that a plain typed graph cannot, and at what cost? One thing is worth doing now: each analogy link carries an explicit dictionary (normal subgroup ↔ ideal, quotient group ↔ quotient ring), so it can become a formal translation later.

#### Formal mathematics: what you need to know

1. **Lean checks proofs, not meaning.** Whether a formal statement says what was intended is still a judgement. Tau Ceti's README says: "AI formalized definitions are, a priori, untrustworthy."
2. **Mathlib** is the human-curated centre, with about 290,000 theorems. This repo pins one commit of it.
3. **Tau Ceti** is an AI-written Lean library built on Mathlib, incubated by the Lean FRO and the Mathlib Initiative.
   - Humans write roadmaps and review rubrics; AI writes the Lean and reviews it adversarially.
   - It is Apache-2.0, like this repo.
   - It says it won't push material upstream to Mathlib.
   - Its roadmap areas are graduate-level, such as universal covers and reductive groups.
   - It is silent on teaching and on second proofs.
   - It tracks Mathlib's latest version, while we pin one commit. That is the practical cost of depending on it.
   - I read its GitHub page only; the lean-lang.org page was unreachable from here.
4. **Textbook formalisation is getting cheap.** Tao has a Lean companion to his *Analysis I*. One paper reports AI agents formalising a 500-page graduate textbook in a week; that figure is self-reported.
5. **AI provers** named in 2026 papers include Aristotle, Gauss and Seed-Prover. I confirmed the names, not any ranking.

Two non-formal models are worth copying. π-Base is a database of topological spaces and their properties, which is our "examples" kind. The Stacks project gives every result a permanent four-symbol tag that survives reorganisation. From memory and unchecked: Lean projects use "blueprints" that pair informal statements with formal ones in a dependency graph.

Tau Ceti is the same loop as this repo at larger scale. Its rubric-driven AI review is worth studying for when review outgrows your daily budget.

#### Computation, simulation, visualisation

- **Computation makes conjecturing practicable.** A guess can be tested in seconds, so "conjecture, then test" becomes an exercise with immediate feedback. The same goes for hunting counterexamples.
- **Some proofs are procedures.** The proof that gcd(a, b) is a combination of a and b can be run. "Run this proof" links the two.
- **A figure or simulation is one more view.** It has its own prerequisites, so nothing structural changes. AI can now write the code, so authoring cost falls.

#### Oral culture

What is mostly passed by word of mouth:
- which results matter and which are technicalities;
- the example to keep in mind;
- what was tried and failed;
- blackboard pictures;
- where the heart of a proof is;
- taste.

My self-report, which I can't check: I have absorbed the half-written version from lecture notes, blogs and question-and-answer sites. I am weakest on failed approaches, pictures, a narrow field's recent folklore, and taste. I can also produce plausible intuition that no expert holds. The test is to have experts blind-rate generated intuitions.

The opportunity is to capture it. AI can interview mathematicians at scale ("what did you try first?") and file the answers as attributed views and rationales. That is the strongest sense of "resource for the world".

#### What is newly possible

**Works at today's reliability**
- **The hint ladder is the proof outline.** When you're stuck, one more level is revealed.
- **Audit the machine.** Take a correct proof and plant a known fault, as this repo's tests do to its validator. Finding the fault needs no judging, since we know the answer.
- **A personal route to any target**, with the trust ledger showing what you skipped.
- **The neighbourhood of a theorem.** Drop or vary each hypothesis, and chart which variants hold, using computation and Lean. "Not recorded here" is not the same as "open".
- **Interviews**, as above.

**Waits on reliable judging of free text** (the hardest piece, as I said before)
- **Review that never repeats:** a fresh instance each time, so you can't memorise the card.
- **Fast feedback on open work:** proofs, definitions and conjectures.

**Needs many learners**
- **Measuring which proof teaches best.**

**Speculative**
- **Untried technique-and-area pairs as research leads.** An empty pair usually means poor fit or missing tags, and only occasionally a lead.

#### Questions

1. Is trust a dial each learner sets, or a rare exception the system grants?
2. Should Tau Ceti be only a source of anchors, or also something we contribute to?
3. Your README says monk-mathematicians study mathematics "much of it machine-produced". Is auditing and digesting machine proofs central to the idea, or one skill among many?

Sources:
- [Tau Ceti on GitHub](https://github.com/TauCetiProject/TauCeti)
- [Mathlib figures, October 2026](https://oyren.ai/blog/ai-theorem-proving-lean-4-2026)
- [Tao's *Analysis I* Lean companion](https://teorth.github.io/analysis)
- [Automatic Textbook Formalization](https://arxiv.org/abs/2604.03071)
- [ICML 2026 tutorial on Lean and machine learning](https://icml.cc/virtual/2026/75365)
- [Knowledge spaces and learning spaces](https://arxiv.org/pdf/1511.06757)
- [Formal concept analysis](https://en.wikipedia.org/wiki/Formal_concept_analysis)
- [MMT: A Scalable Module System](https://arxiv.org/pdf/1105.0548)
- [Hilbert's twenty-fourth problem](https://en.wikipedia.org/wiki/Hilbert%27s_twenty-fourth_problem)
- [Spivak, Functorial Data Migration](https://arxiv.org/abs/1009.1166)
- [Caramello, The unification of Mathematics via Topos Theory](https://arxiv.org/abs/1006.3930)
- [π-Base](https://github.com/pi-base/data/wiki)
- [Stacks project tags](https://stacks.math.columbia.edu/tags)

### 5. Owner

> Save this conversation somewhere in the repo to pick things up tomorrow.
