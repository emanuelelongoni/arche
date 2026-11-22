#!/usr/bin/env python3
"""Validate the knowledge graph against spec/SCHEMA.md §5.

Usage:
  python3 tools/validate.py              # errors and warnings; exit 1 on errors
  python3 tools/validate.py --report     # also print coverage and viewpoint reports
  python3 tools/validate.py --report-md out.md   # write the report as Markdown
  python3 tools/validate.py --root /tmp/copy/graph   # check another graph directory

--root names a graph directory (courses/, nodes/, viewpoints/; default graph/ in
this repo). Jobs are read from the jobs/ directory beside it, if there is one.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator

import mmgraph as G

LECTURE_MINUTES = 50  # rough study-minutes per lecture, for the minutes/lectures ratio


class Log:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def rel(g: G.Graph, key: str) -> str:
    p = g.files.get(key)
    return g.display(p) if p else key


def check_schemas(g: G.Graph, log: Log):
    validators = {k: Draft202012Validator(G.load_schema(k)) for k in ("node", "course", "viewpoint")}
    for kind, items in (("course", g.courses), ("viewpoint", g.viewpoints), ("node", g.nodes)):
        for iid, d in items.items():
            for e in sorted(validators[kind].iter_errors(d), key=lambda e: list(e.path)):
                where = "/".join(str(x) for x in e.path) or "(root)"
                log.err(f"{rel(g, f'{kind}:{iid}')}: schema: {where}: {e.message}")


def check_jobs(g: G.Graph, log: Log):
    import yaml
    v = Draft202012Validator(G.load_schema("job"))
    jobs = {}
    for p in sorted((g.root.parent / "jobs").glob("*/J*.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        where = g.display(p)
        for e in v.iter_errors(d):
            log.err(f"{where}: schema: {'/'.join(map(str, e.path)) or '(root)'}: {e.message}")
        if d.get("id") and p.stem != d["id"]:
            log.err(f"{where}: file name must be {d['id']}.yaml")
        jobs[d.get("id")] = d
        course = (d.get("scope") or {}).get("course")
        if course and course not in g.courses:
            log.err(f"{where}: unknown course {course}")
    for jid, d in jobs.items():
        for dep in d.get("depends_on", []) or []:
            if dep not in jobs:
                log.err(f"jobs: {jid} depends on unknown job {dep}")


def check_structure(g: G.Graph, log: Log):
    items = {}  # "course#item" -> section n
    for cid, c in g.courses.items():
        path = g.files[f"course:{cid}"]
        if path.stem != cid:
            log.err(f"{rel(g, f'course:{cid}')}: file name must be {cid}.yaml")
        seen_n = set()
        for s in c.get("sections", []) or []:
            if s["n"] in seen_n:
                log.err(f"{rel(g, f'course:{cid}')}: duplicate section {s['n']}")
            seen_n.add(s["n"])
            for it in s.get("items", []) or []:
                key = f"{cid}#{it['id']}"
                if key in items:
                    log.err(f"{rel(g, f'course:{cid}')}: duplicate item id {it['id']}")
                items[key] = s["n"]
    prefixes = {c["prefix"]: cid for cid, c in g.courses.items()}
    if len(prefixes) != len(g.courses):
        log.err("two courses share a prefix")

    for nid, n in g.nodes.items():
        where = rel(g, f"node:{nid}")
        path = g.files[f"node:{nid}"]
        if path.stem != nid:
            log.err(f"{where}: file name must be {nid}.yaml")
        course = g.courses.get(n.get("course"))
        if course is None:
            log.err(f"{where}: unknown course {n.get('course')!r}")
            continue
        if path.parent.name != n["course"]:
            log.err(f"{where}: must live in graph/nodes/{n['course']}/")
        if not nid.startswith(course["prefix"] + "."):
            log.err(f"{where}: id must start with '{course['prefix']}.' (course prefix)")
        sec = n.get("section")
        if sec is not None and sec not in {s["n"] for s in course.get("sections", [])}:
            log.err(f"{where}: course {course['id']} has no section {sec}")
        for t in g.all_requires_targets(nid):
            if t not in g.nodes:
                log.err(f"{where}: requires unknown node {t}")
            if t == nid:
                log.err(f"{where}: requires itself")
        seen = set()
        for e in n.get("encompasses", []) or []:
            if e["node"] not in g.nodes:
                log.err(f"{where}: encompasses unknown node {e['node']}")
            if e["node"] == nid:
                log.err(f"{where}: encompasses itself")
            if e["node"] in seen:
                log.err(f"{where}: encompasses {e['node']} twice")
            seen.add(e["node"])
        for e in n.get("illuminates", []) or []:
            if e["node"] not in g.nodes:
                log.err(f"{where}: illuminates unknown node {e['node']}")
        for cov in n.get("covers", []) or []:
            if cov not in items:
                log.err(f"{where}: covers unknown item {cov}")
        for vp in n.get("only_in", []) or []:
            if vp not in g.viewpoints:
                log.err(f"{where}: only_in names unknown viewpoint {vp}")
        for vp in (n.get("lesson_notes") or {}):
            if vp not in g.viewpoints:
                log.err(f"{where}: lesson_notes names unknown viewpoint {vp}")
        if n.get("status") in ("draft", "reviewed") and not n.get("anchors") \
                and n.get("verification") != "informal":
            log.warn(f"{where}: no anchors but verification is {n.get('verification')!r}")
    return items


def check_choices(g: G.Graph, log: Log):
    for group, occ in g.choice_groups().items():
        first_nid, first = occ[0]
        opts = set(first["options"])
        if first["default"] not in opts:
            log.err(f"{rel(g, f'node:{first_nid}')}: choice {group}: default {first['default']!r} is not an option")
        for nid, ch in occ[1:]:
            if set(ch["options"]) != opts or ch["default"] != first["default"]:
                log.err(f"{rel(g, f'node:{nid}')}: choice {group} differs from {first_nid} "
                        f"(options {sorted(ch['options'])} default {ch['default']!r} vs "
                        f"{sorted(opts)} default {first['default']!r})")
    groups = g.choice_groups()
    for vid, v in g.viewpoints.items():
        for group, opt in (v.get("choices") or {}).items():
            if group not in groups:
                log.err(f"{rel(g, f'viewpoint:{vid}')}: unknown choice group {group}")
            elif opt not in groups[group][0][1]["options"]:
                log.err(f"{rel(g, f'viewpoint:{vid}')}: group {group} has no option {opt!r}")


def check_viewpoints(g: G.Graph, log: Log):
    redundant_in: dict[tuple[str, str], list[bool]] = defaultdict(list)
    not_ancestor: dict[tuple[str, str], list[str]] = defaultdict(list)
    for vp in g.viewpoints:
        act = g.active(vp)
        dag = {}
        for nid in act:
            prereqs = []
            for e in g.requires_under(vp, nid):
                t = e["node"]
                if t not in g.nodes:
                    continue
                if t not in act:
                    log.err(f"{rel(g, f'node:{nid}')}: under viewpoint {vp}, requires {t}, "
                            f"which does not exist in {vp} (only_in)")
                    continue
                prereqs.append(t)
            dag[nid] = prereqs
        cyc = G.find_cycle(dag)
        if cyc:
            log.err(f"viewpoint {vp}: cycle: " + " requires ".join(cyc))
            continue
        anc = {n: G.ancestors(dag, n) for n in dag}
        for nid, prereqs in dag.items():
            for t in prereqs:
                others = [p for p in prereqs if p != t]
                redundant = any(t == o or t in anc[o] for o in others)
                redundant_in[(nid, t)].append(redundant)
            for e in g.nodes[nid].get("encompasses", []) or []:
                t = e["node"]
                if t in act and t not in anc[nid]:
                    not_ancestor[(nid, t)].append(vp)
    for (nid, t), flags in sorted(redundant_in.items()):
        if flags and all(flags):
            log.warn(f"{rel(g, f'node:{nid}')}: requires {t} is redundant (implied by another prerequisite) "
                     f"in every viewpoint where it is active")
    for (nid, t), vps in sorted(not_ancestor.items()):
        log.warn(f"{rel(g, f'node:{nid}')}: encompasses {t}, which is not an ancestor under {', '.join(vps)}")


def coverage_report(g: G.Graph, items: dict[str, int]) -> list[str]:
    covered: dict[str, set[str]] = defaultdict(set)  # item -> statuses
    for n in g.nodes.values():
        for cov in n.get("covers", []) or []:
            covered[cov].add(n["status"])
    lines = ["## Coverage", ""]
    minutes_by_sec: dict[tuple[str, int], int] = defaultdict(int)
    for n in g.nodes.values():
        if n.get("section") and n.get("minutes"):
            minutes_by_sec[(n["course"], n["section"])] += n["minutes"]
    for cid, c in sorted(g.courses.items(), key=lambda kv: kv[0]):
        if not c.get("sections"):
            continue
        tot = done = stub = 0
        lines.append(f"### {cid}: {c['title']} ({c.get('lectures', '?')} lectures, status {c['status']})")
        lines.append("")
        lines.append("| § | Section | Lectures | Items | Covered | Stub only | Uncovered | Minutes | Min/lecture |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for s in c["sections"]:
            ids = [f"{cid}#{it['id']}" for it in s["items"]]
            d = sum(1 for i in ids if covered[i] & {"draft", "reviewed"})
            st = sum(1 for i in ids if covered[i] and not covered[i] & {"draft", "reviewed"})
            u = len(ids) - d - st
            tot += len(ids); done += d; stub += st
            mins = minutes_by_sec.get((cid, s["n"]), 0)
            lec = s.get("lectures") or 0
            ratio = f"{mins / lec:.0f}" if lec and mins else "–"
            lines.append(f"| {s['n']} | {s['title']} | {lec} | {len(ids)} | {d} | {st} | {u} | {mins} | {ratio} |")
        lines.append("")
        lines.append(f"Total: {done}/{tot} items covered by draft or reviewed nodes, {stub} by stubs only, "
                     f"{tot - done - stub} uncovered.")
        lines.append("")
    return lines


def viewpoint_report(g: G.Graph) -> list[str]:
    lines = ["## Viewpoints", "", "| Viewpoint | Nodes | Stubs | Requires edges | Minutes | Longest chain |",
             "|---|---|---|---|---|---|"]
    for vp in sorted(g.viewpoints):
        act = g.active(vp)
        dag = {n: [t for t in (e["node"] for e in g.requires_under(vp, n)) if t in act] for n in act}
        if G.find_cycle(dag):
            lines.append(f"| {vp} | (cycle) | | | | |")
            continue
        order = G.topo_order(dag, act)
        depth = {}
        for n in order:
            depth[n] = 1 + max((depth[p] for p in dag[n]), default=0)
        stubs = sum(1 for n in act if g.nodes[n]["status"] == "stub")
        mins = sum(g.nodes[n].get("minutes", 0) for n in act)
        edges = sum(len(v) for v in dag.values())
        lines.append(f"| {vp} | {len(act)} | {stubs} | {edges} | {mins} | {max(depth.values(), default=0)} |")
    lines.append("")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--report-md")
    ap.add_argument("--root", type=Path, default=G.GRAPH,
                    help="graph directory to check (default: graph/ in this repo)")
    args = ap.parse_args()

    g = G.load(args.root)
    log = Log()
    for e in g.load_errors:
        log.err(e)
    check_schemas(g, log)
    items = check_structure(g, log)
    check_choices(g, log)
    check_jobs(g, log)
    if not log.errors:  # graph checks need a structurally sound graph
        check_viewpoints(g, log)

    for w in log.warnings:
        print(f"warning: {w}")
    for e in log.errors:
        print(f"ERROR: {e}")
    print(f"\n{len(g.courses)} courses, {len(g.nodes)} nodes "
          f"({sum(1 for n in g.nodes.values() if n['status'] == 'stub')} stubs), "
          f"{len(g.viewpoints)} viewpoints: {len(log.errors)} errors, {len(log.warnings)} warnings")

    if args.report or args.report_md:
        report = coverage_report(g, items) + viewpoint_report(g)
        if args.report:
            print("\n" + "\n".join(report))
        if args.report_md:
            with open(args.report_md, "w", encoding="utf-8") as f:
                f.write("# Graph report\n\n" + "\n".join(report) + "\n")
    sys.exit(1 if log.errors else 0)


if __name__ == "__main__":
    main()
