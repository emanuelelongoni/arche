# Spec: arche.academy v0, a static site generated from the graph

Status: proposed, awaiting approval. Nothing in `site/` is built until this spec is approved.

## Problem Statement

The Archē knowledge graph exists only as YAML in a repository. A learner who wants to know what Heine–Borel rests on, how the classical and nPOV routes to it differ, or what is left to learn given what they already know has to run Python tools from a terminal and read their output. The owner has no way to show the project to anyone who doesn't read YAML. A hand-maintained website would drift from the graph within a week, because agents change the graph every night.

## Solution

A calm, readable static site at https://arche.academy, generated at build time from `graph/` on every push to `main`, so the site always shows exactly what the graph says. It has:

- a home page that explains Archē and the two viewpoints;
- a map of the graph as a layered DAG with a classical/nPOV switch;
- one page per topic (node) with its knowledge points, prerequisites and the reasons for them, review credit, cross-links, Lean anchors, lesson notes and coverage;
- one page per course with its coverage table;
- a "route to" tool: pick a target and a viewpoint, tick what you already know, and get the topics to learn, in order, with total minutes.

There are no accounts, no tracking and no server. It works without JavaScript except for the two interactive tools, and those enhance pages that are already readable.

## User Stories

Learners

1. As a learner, I want a home page that says in a few sentences what Archē is and who it is for, so that I can tell whether it suits me.
2. As a learner, I want the home page to explain the two viewpoints (classical and nPOV) in plain words, so that I can choose a route knowingly.
3. As a learner, I want links from the home page to the map, the route tool, the courses and the list of all topics, so that I can start in the way that suits me.
4. As a learner, I want to see the whole graph as a map with prerequisites above the topics that need them, so that I can see the shape of the subject.
5. As a learner, I want to switch the map between classical and nPOV, so that I can see how the routes differ.
6. As a learner, I want stubs drawn dashed on the map, so that I can tell at once which topics aren't written yet.
7. As a learner, I want topics that exist only in the nPOV marked on the map, so that I can see what the categorical route adds.
8. As a learner, I want edges that come from a route choice drawn differently from edges every route shares, so that I can see where the viewpoints diverge.
9. As a learner, I want every topic on the map to be a link to its page, so that the map is a way in, not just a picture.
10. As a learner, I want a legend on the map, so that I don't have to guess what dashed or marked nodes mean.
11. As a learner, I want a list of all topics grouped by course, with a filter box, so that I can find a topic by name quickly.
12. As a learner, I want each topic page to show its title, kind (definition, theorem, …), course and section, minutes and status, so that I know what I'm looking at.
13. As a learner, I want each topic page to list its knowledge points, so that I know what I'll be able to do afterwards.
14. As a learner, I want each topic page to list its prerequisites with the reason for each, so that I understand why I need them.
15. As a learner, I want prerequisites that depend on the viewpoint shown under each viewpoint's name, so that I can see what each route asks of me here.
16. As a learner, I want each topic page to list the topics that build on it, so that I can see what it unlocks.
17. As a learner, I want each topic page to show what it encompasses, with weights, so that I understand which earlier topics get practised along the way.
18. As a learner, I want each topic page to show what it illuminates and what illuminates it, so that I can follow cross-links between viewpoints.
19. As a learner, I want the lesson notes for each viewpoint on the topic page, so that I can see how each route frames the topic.
20. As a learner, I want the off-platform prompt (when there is one) on the topic page, so that I have something to think about on a walk.
21. As a learner, I want to see which syllabus items a topic covers, linked to the course page, so that I can relate it to my course.
22. As a learner, I want a clear note on stub pages that the topic isn't written yet, so that I'm not confused by a thin page.
23. As a learner, I want a "route to this topic" link on every topic page that opens the route tool with that target, so that I can plan from where I am.
24. As a learner, I want to choose a target topic and a viewpoint in the route tool, so that I can plan a path to what I want to learn.
25. As a learner, I want to tick the topics I already know, so that the path leaves them out.
26. As a learner, I want ticking a topic to count its prerequisites as known too, and to see that shown, so that I don't have to tick everything below it.
27. As a learner, I want the route as an ordered list (prerequisites first) with minutes per topic and a total, so that I can schedule my study.
28. As a learner, I want the total to say how many stubs it leaves out because they have no estimate yet, so that I'm not misled.
29. As a learner, I want the route tool's state in the page address, so that I can bookmark or share a plan.
30. As a learner, I want the route tool to give the same answer as the project's own `plan.py`, so that the site and the tools never disagree.
31. As a learner, I want to compare the classical and nPOV routes to the same target, so that I can see the cost and content of each.

Mathematically curious readers

32. As a reader who knows Lean, I want each Lean anchor shown as its full name and linked to the Mathlib documentation, so that I can check the formal statement.
33. As a reader, I want each topic page to state its verification tier (formal, partial, informal) and what that means, so that I know how much of it Lean has checked.
34. As a reader, I want the site to say which Mathlib commit the anchors were checked against, so that I understand why a link might point at a renamed declaration.
35. As a reader, I want course pages that show each section's syllabus items and the topics that cover them, so that I can see how complete the graph is.
36. As a reader, I want course pages to show items covered only by stubs, and items not covered at all, so that gaps are visible.
37. As a reader, I want lectures and estimated minutes per section, so that I can compare the graph with the course.

Accessibility and comfort

38. As a reader on a phone, I want every page readable in one column with no sideways scrolling of the page, so that I can study on the move.
39. As a reader on a phone, I want a list view of the map ordered by layer, so that I can use the map without pinching and panning a large diagram.
40. As a keyboard user, I want to reach every link and control with Tab in a sensible order, with a visible focus ring, so that I never need a mouse.
41. As a keyboard user, I want a "skip to content" link, so that I don't tab through the header on every page.
42. As a keyboard user, I want to move through the map's topics with Tab in layer order and open one with Enter, so that the map is usable without a mouse.
43. As a screen-reader user, I want the route result announced when it changes, so that I know my ticks took effect.
44. As a screen-reader user, I want the map to have a text equivalent, so that I get the same information as a sighted reader.
45. As a reader who prefers dark screens, I want a dark theme that follows my system setting, with a manual override that's remembered on my device, so that reading at night is comfortable.
46. As a reader, I want generous, well-set serif type with correct mathematical symbols (ℝ, ⊆, →, ⊣), so that reading mathematics is a pleasure.
47. As a reader with motion sensitivity, I want no animations, so that nothing moves unexpectedly.

Privacy

48. As a reader, I want no cookies, no analytics and no third-party requests, so that my study isn't tracked.
49. As a reader, I want the site to keep working if JavaScript is off, apart from the two interactive tools, so that it's robust and light.

Owner and maintainers

50. As the owner, I want the site rebuilt and deployed automatically on every push to `main`, so that I never update it by hand.
51. As the owner, I want the build to fail if the graph doesn't validate, so that a broken graph never reaches the public site.
52. As the owner, I want pull requests to build and test the site without deploying it, so that I see breakage before merging.
53. As the owner, I want every page footer to show the commit the site was built from, so that I can tell at a glance whether the site is current.
54. As the owner, I want an exact list of the GitHub settings to click and the DNS records to create, so that I can set up the domain once without guesswork.
55. As a content agent, I want to change only `graph/` and have the site follow, so that I never edit site code to publish content.
56. As a maintainer, I want viewpoint and choice-group semantics to stay in one place (the Python graph module), so that the site can't disagree with the validator about what a viewpoint means.
57. As a maintainer, I want tests that show the TypeScript planner matches `plan.py` on many inputs, so that I can refactor either side safely.
58. As a maintainer, I want a check that every internal link on the built site resolves, so that renames don't leave dead links.

## Implementation Decisions

### Why Astro

Astro fits this site well. It emits static HTML with no client JavaScript by default, and it adds small interactive "islands" only where needed: here, the map switch and the route tool. It runs in Node at build time, so the layered layout (elkjs) is computed during the build and shipped as plain SVG instead of as a layout engine. It produces typed pages from data without a client-side app framework. Its static output deploys to GitHub Pages with the official Pages actions. I considered Eleventy, which is equally static but would mean hand-rolling the islands, the TypeScript build and the component model. I also considered SvelteKit and Next in static mode, which are app-first and ship more runtime than this site needs. Neither is better for this site, so: Astro, current major (7.x), with exact versions pinned in a lockfile.

### Data flow: the graph is the only source

- A new Python tool, `export_site`, sits beside the other tools and goes through the graph module (`mmgraph`), so viewpoint, choice-group and active-node semantics stay single-sourced. It writes one JSON document into the site's build directory, which is gitignored. It takes `--root` like `validate.py`, and it refuses to export (exit 1) a graph that has validator errors.
- The site's build script runs the export first, then Astro. Pages are generated from the JSON alone. Nothing in `site/` copies or restates graph content, and no generated data is committed.
- The export contains the raw YAML of every course, node and viewpoint, unchanged, plus a few derived values computed in Python:
  - per viewpoint: the active nodes; the resolved requires DAG (node → prerequisites, exactly as `plan.py` builds it); and every resolved edge with its reason and `via` (`null` for a plain edge, `group:option` for an edge that comes from a choice group);
  - per course item: coverage state (`covered`, `stub-only`, `uncovered`) and the covering nodes. This uses the same classification as `validate.py --report`, moved into the graph module so that the report and the export share it;
  - build provenance: the commit SHA, the build date, and the Mathlib rev from `lean/lakefile.toml`.
- The data's type shape, which the site validates at load so that a schema change fails the build loudly:

```ts
type NodeId = string; type ViewpointId = string;
interface SiteData {
  builtFrom: { commit: string; date: string; mathlibRev: string };
  courses: Record<string, CourseYaml & { coverage: Record<string /* item id */, { state: "covered" | "stub-only" | "uncovered"; nodes: NodeId[] }> }>;
  nodes: Record<NodeId, NodeYaml>;
  viewpoints: Record<ViewpointId, ViewpointYaml & {
    active: NodeId[];
    dag: Record<NodeId, NodeId[]>;                 // node -> prerequisites, active only
    edges: { from: NodeId; to: NodeId; reason: string; via: string | null }[];
  }>;
}
```

### Pages and URLs

| Page | URL | Content |
|---|---|---|
| Home | `/` | What Archē is; the two viewpoints, with their descriptions and references from the viewpoint files; entry points; a few graph statistics per viewpoint (topics, stubs, minutes) |
| Map | `/map/` | Layered DAG with a classical/nPOV switch; legend; list view by layer |
| All topics | `/topics/` | Every topic grouped by course and section, with a filter box (progressive enhancement) |
| Topic | `/topics/<node-id>/` | See "Topic page" |
| Course | `/courses/<course-id>/` | See "Course page" |
| Route to | `/route/` | The route tool; state in the URL fragment |
| Not found | `404.html` | Links to home and all topics |

Every page has the same header (Archē, Map, Topics, Courses, Route) and footer (licence, source on GitHub, "built from <short SHA> on <date>" linked to the commit, and a line saying the site sets no cookies and loads nothing from third parties).

### Map

- Built at build time with elkjs's layered algorithm, one layout per viewpoint, rendered as inline SVG. Prerequisites sit above the topics that need them, and arrows run from prerequisite to topic, as in `render.py`. No layout engine ships to the browser.
- Each node is a link to its topic page and shows the title. The course appears as a small coloured key (by course) plus its prefix in the accessible name.
- Stubs have a dashed outline. Nodes that exist only in nPOV have a double outline and a small "nPOV" label, and appear only in the nPOV layout. Edges whose `via` is a choice group use the accent colour and a distinct dash pattern, so the difference doesn't rely on colour alone.
- The switch is a two-option radio group styled as a segmented control. Without JavaScript, a CSS `:has(:checked)` rule toggles which SVG is shown. The choice is mirrored into the URL fragment (`#npov`) and remembered on the device as a convenience.
- Text equivalent and phone view: the same DAG as an ordered list by layer (topological depth), each entry with its prerequisites. On narrow screens the list is the default and the SVG sits in its own horizontally scrollable container.
- Tab order through the SVG follows layer order, then id.

### Topic page

In order:

1. Title, kind, course and section (linked), minutes, status badge (stub, draft, reviewed) and verification tier with a one-line explanation. Stubs get a notice that the topic isn't written yet.
2. Knowledge points, as a numbered list.
3. Prerequisites. Plain requires edges come first, each linked with its reason. Each choice group follows, showing every option with its edges and the viewpoints that pick it (including the default for viewpoints that don't mention the group). If the topic exists only in some viewpoints, that's stated.
4. "Builds towards": reverse requires edges, per viewpoint.
5. Encompasses, with weights and the encompassed topics linked.
6. Illuminates, and Illuminated by.
7. Lean anchors: the full name in monospace, its library (Mathlib or Lean core), and a link to `https://leanprover-community.github.io/mathlib4_docs/find/?pattern=<Decl>#doc`, which redirects to the declaration's documentation. A note says anchors are checked against the pinned Mathlib rev (shown), while the documentation tracks Mathlib master.
8. Lesson notes, one block per viewpoint, labelled with the viewpoint's title.
9. Off-platform prompt, if any.
10. Covers: the syllabus items, linked to their rows on the course page.
11. MSC codes and sources, if any.
12. "Route to this topic", linking to `/route/#to=<node-id>`.

### Course page

Title, part, term, lectures, status and source. Stated prerequisites and notes if present. Then one table per section, with columns: item text (starred items marked "non-examinable"), state (covered, stub only, uncovered, shown with words and not just colour), and covering topics (linked, with status). Each item row has a stable anchor (`#<item-id>`). A per-section summary row gives lectures, estimated minutes and minutes per lecture, matching `validate.py --report`. A course total line ends the page.

### Route tool and the TypeScript planner

- A pure TypeScript module, the planner, ports the logic of `plan.py` over one viewpoint's resolved DAG from the export:

```ts
function planRoute(dag: Record<NodeId, NodeId[]>, targets: NodeId[], known: Iterable<NodeId>): NodeId[]
```

  It returns `ancestors(targets) ∪ targets` minus (known plus all ancestors of known), in topological order. The tie-break must match `topo_order` exactly: start from the ready nodes sorted by id; repeatedly take the smallest ready id, release its dependents, and re-sort. Ids are ASCII, so JavaScript's default string sort agrees with Python's. The planner throws if a target isn't active, where `plan.py` exits.
- A second function sums minutes over a route and counts the stubs it left out, matching `plan.py`'s "total ≈ … (stubs not counted)".
- The UI has a target picker (a text input with a datalist of the active topics' titles and ids), a viewpoint radio, and a checklist of the target's ancestors in route order. Ticking one marks its ancestors as "known (implied)", which are shown but not ticked. Below that is the ordered result with minutes, the total, and the stub count, in an `aria-live="polite"` region. A "compare viewpoints" toggle shows both routes side by side with "only in classical" and "only in nPOV" lists, like `plan.py --compare`.
- State lives in the URL fragment (`#to=ts.heine-borel&vp=npov&known=a1.continuity,ns.least-upper-bound`). The fragment is never sent to the server. Unknown ids in the fragment are dropped with a visible note.
- The page ships only the DAGs, titles, minutes and statuses that the tool needs, not the whole export.

### Design

- Type: Source Serif 4 (variable, SIL OFL), self-hosted, for text and headings, with STIX Two Math as a self-hosted fallback restricted by `unicode-range` to the mathematical operator, arrow and letterlike blocks, so that ⊣, ⊆ and ℝ always render consistently. Lean names use the system monospace stack. Base size 18–20 px, line height about 1.55, measure 60–70 characters, old-style figures in prose and lining tabular figures in tables. Hierarchy comes from size and weight, not colour.
- Colour: a warm off-white page with near-black text, and one muted accent. The dark theme uses warm dark grey (not pure black) with off-white text. Body text meets WCAG AAA contrast (7:1), and everything else meets AA. The map's SVG uses the same CSS custom properties, so it follows the theme.
- Theme: follows `prefers-color-scheme` by default. A three-way control (system, light, dark) in the footer stores the choice in `localStorage`. A tiny inline script applies the theme before first paint, to avoid a flash.
- No animations or transitions. `prefers-reduced-motion` is respected in any case.
- Keyboard: a skip link, a logical heading order, a visible 2 px focus ring with offset, no positive `tabindex`, no keyboard traps, and native form controls throughout.
- Phone: a single column, tap targets of at least 44 px, no horizontal page scroll at 320 px width, and the map's list view by default.
- Budgets: no page ships JavaScript except the map (switch) and the route tool, each under 30 KB compressed. HTML and CSS are under 100 KB per page, excluding fonts. Fonts are subset and preloaded only for the regular weight.

### Privacy and security

- No accounts, cookies, analytics, or third-party requests of any kind: fonts and scripts are all self-hosted. The only device storage is the theme and viewpoint preferences in `localStorage`.
- GitHub Pages can't set headers, so a Content-Security-Policy `<meta>` limits every resource to the site's own origin. Inline scripts are allowed only by hash, using Astro's built-in CSP support. Outbound links use `rel="noopener"`, and the referrer policy is `strict-origin-when-cross-origin`.
- The footer states that GitHub, which hosts the site, may log visits under its own privacy statement. The project collects nothing.

### Build and CI

- A new workflow builds the site on every pull request and on every push to `main`, and deploys only on pushes to `main`. It has a `build` job and a `deploy` job. The build job:
  1. checks out the repo;
  2. sets up Python 3.12 and Node 24 LTS, matching Astro 7's `engines`;
  3. runs `tools/validate.py` as a gate;
  4. runs `npm ci` in `site/`;
  5. runs the site's tests (`npm test`, which includes the parity tests and needs Python);
  6. builds the site;
  7. checks internal links;
  8. uploads `site/dist` with `actions/upload-pages-artifact@v4`.
- The deploy job runs `actions/deploy-pages@v4` with `needs: build`, environment `github-pages`, permissions `pages: write` and `id-token: write`, and concurrency group `pages` without cancelling in-progress runs. `actions/configure-pages@v5` runs in the build job. These versions are the ones GitHub's custom-workflow docs show as of 2026-11-22.
- Astro config: `site: "https://arche.academy"`, base `/`, directory-style URLs. No `CNAME` file: with a custom Actions workflow, GitHub ignores one, and the domain is set in Settings.
- The site's dependencies are pinned exactly (`npm ci` with a committed lockfile): Astro 7.4, elkjs 0.12, Vitest 5, TypeScript 7, and Playwright for the browser checks. A `.nvmrc` pins Node 24.
- The Lean anchors check stays in its own workflow and doesn't gate deploys. A broken anchor on `main` still deploys, and its documentation link simply fails to resolve.

### Deployment: what the owner must do, once

The repository is public, so GitHub Pages is available on the current plan. Do the steps in this order. GitHub's docs ask for the custom domain to be added to the site before the DNS records, and verifying first closes the takeover window.

**At GitHub (verify the domain first):**

1. Profile picture → **Settings** → sidebar "Code, planning, and automation" → **Pages** → **Add a domain** → type `arche.academy` → **Add domain**. GitHub shows a TXT record. Leave the page open.
2. At the registrar, create that TXT record (below). Wait until `dig _github-pages-challenge-emanuelelongoni.arche.academy +nostats +nocomments +nocmd TXT` returns the value, then go back to the page → **⋯** → **Continue verifying** → **Verify**.

**At GitHub (the repository):**

3. Repository → **Settings** → **Pages** → "Build and deployment" → **Source**: **GitHub Actions**.
4. Same page → **Custom domain**: type `arche.academy` → **Save**. The DNS check fails until the records below exist; that's expected. If the box doesn't appear until the first deployment, do this step right after step 6 instead.

**At the registrar (DNS for `arche.academy`):**

| Type | Name (host) | Value | Notes |
|---|---|---|---|
| TXT | `_github-pages-challenge-emanuelelongoni` | the value GitHub shows in step 1 | Keep it permanently; it prevents domain takeover |
| A | `@` | `185.199.108.153` | |
| A | `@` | `185.199.109.153` | |
| A | `@` | `185.199.110.153` | |
| A | `@` | `185.199.111.153` | |
| AAAA | `@` | `2606:50c0:8000::153` | |
| AAAA | `@` | `2606:50c0:8001::153` | |
| AAAA | `@` | `2606:50c0:8002::153` | |
| AAAA | `@` | `2606:50c0:8003::153` | |
| CNAME | `www` | `emanuelelongoni.github.io.` | No repository name. GitHub then redirects `www.arche.academy` to `arche.academy` |

Also at the registrar:

- Delete any other `@` records of type A, AAAA, ALIAS or ANAME (registrar parking pages, for example), any other `www` record, and any wildcard (`*`) record. GitHub warns that wildcards risk takeover, and extra records can block the certificate.
- If the zone has CAA records, add one allowing Let's Encrypt: `@ CAA 0 issue "letsencrypt.org"`. If it has none, add nothing.

**Back at GitHub:**

5. Wait for the DNS check in Settings → Pages to pass. DNS can take up to 24 hours, and HTTPS up to an hour after that.
6. Merge the site PR (once it's built and approved). The workflow deploys. The site is built for the root of `arche.academy`, so its assets won't load correctly at the fallback `emanuelelongoni.github.io/arche/` address; use the custom domain.
7. Tick **Enforce HTTPS**. If it stays unavailable, click **Remove** next to the custom domain, retype `arche.academy` and **Save** again to restart certificate provisioning.
8. Repository → **Settings** → **Environments** → `github-pages` (created by the first deployment) → "Deployment branches and tags": make sure only `main` can deploy. Select "Selected branches and tags" and add `main`, unless it's already limited to protected branches.
9. Optional: repository → **About** (gear) → Website `https://arche.academy`.

## Testing Decisions

- A good test checks behaviour through a public seam: a command's output, a function's return value, or a built page. It doesn't check internals. Expected values come from an independent source: `plan.py` itself, or literal numbers from today's graph. They are never recomputed the way the code computes them.
- Three seams, from highest to lowest:
  1. **The built site.** A link checker walks `site/dist` and fails on any internal link that doesn't resolve, or on any `src`/`href` of a script, stylesheet, font or image that isn't same-origin (outbound `<a>` links are fine). A count check asserts that there is one topic page per node and one course page per course in the export. A small Playwright suite (about 10 tests) runs against the static build at 375 px and 1280 px, in light and dark: axe finds no violations on home, map, a topic, a course and the route tool; the map switch works with and without JavaScript; and a keyboard-only walk through the route tool (Tab to the target, type, choose the viewpoint, tick a known topic, hear the result) produces the expected route.
  2. **The TypeScript planner (Vitest).** For parity, a small Python oracle imports the planner from `tools/plan.py` and answers a batch of cases from the same graph in one run. Vitest compares the ordered lists and totals exactly. The cases are: every active node as a target with nothing known, under each viewpoint; plus 200 seeded random (target, known-set) cases per viewpoint; plus multi-target cases. As literal anchors: `ts.heine-borel` gives 26 topics and 575 minutes under classical, and 32 topics and 760 minutes under npov, with nothing known (today's `plan.py --compare` output).
  3. **The export (pytest, in the existing `tests/` suite).** On the real graph: `ts.finite-products-compact`'s prerequisites are `ts.interval-compact` and `ts.tube-lemma` under classical, and `ts.interval-compact` and `ts.compact-universally-closed` under npov; `ct.categories` is active only in npov; and the per-viewpoint node and edge counts match the report (49 and 73 classical, 56 and 90 npov, today). On a copy with a planted fault, the export exits 1.
- Prior art: `tests/test_validate.py` and `tests/conftest.py` (the planted-fault tests, run through the CLI on a copy of `graph/` made with `--root`). The export tests reuse that fixture.
- Seams to confirm with the owner before building: are the three seams above the right ones, and is a Playwright suite worth its CI minutes for v0, or should v0 stop at the link checker plus the parity tests?

## Out of Scope

- Exercises, worked examples and lesson text. The site shows knowledge points and lesson notes, not lessons.
- Scheduling and spaced repetition, including any use of encompasses weights beyond displaying them.
- Accounts, sign-in, saved progress across devices, and anything server-side.
- AI features of any kind.
- Full-text search (Pagefind would fit later), analytics, comments, newsletters, internationalisation, offline/PWA.
- Editing the graph from the site.
- Documentation links pinned to the Mathlib commit, which would need a declaration→module map from the Lean build.

## Further Notes

- **Deviation from the to-spec template.** The template asks for no file paths and for publication to the issue tracker. The brief required concrete locations (`site/`, this file), exact GitHub settings and DNS records, and a PR. So this spec names a few paths, versions and settings, and lives in the repo. Package versions are as of 2026-11-22; pin whatever is current when building.
- **URL stability.** Topic URLs use node ids. Renaming a node breaks inbound links. A later version could add a `renamed_from` field and emit redirect pages.
- **Documentation drift.** The Mathlib docs follow master, so a declaration renamed after the pinned rev will fail to resolve through the `find` link even though `lake build` passes. The page states the pinned rev, which is honest. A pinned link would need the declaration→module map mentioned above.
- **Glyph coverage.** A build-time check that every character in the graph's strings is covered by the bundled fonts would catch a missing symbol before readers do. It's cheap with a font-parsing library and could join the link checker.
- **Graph size.** Today there are 49–56 nodes per viewpoint. elkjs handles hundreds comfortably at build time. Past roughly 300 nodes the single map stops being readable, and per-course maps (already possible from the same layout code) become the default view.
