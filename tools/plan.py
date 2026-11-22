#!/usr/bin/env python3
"""Plan a learning path to a target under a viewpoint.

The path is ancestors(target) minus what the learner knows, in topological order
(spec/SCHEMA.md §4). Knowing a node is assumed to imply knowing its ancestors.

Usage:
  python3 tools/plan.py ts.heine-borel --viewpoint npov
  python3 tools/plan.py ts.heine-borel --viewpoint classical --known a1.continuity,ns.least-upper-bound
  python3 tools/plan.py ts.heine-borel --compare classical npov
"""
from __future__ import annotations

import argparse
import sys

import mmgraph as G


def plan(g: G.Graph, vp: str, targets: list[str], known: set[str]) -> list[str]:
    act = g.active(vp)
    dag = {n: [t for t in (e["node"] for e in g.requires_under(vp, n)) if t in act] for n in act}
    for t in targets:
        if t not in act:
            sys.exit(f"{t} does not exist under viewpoint {vp}")
    closed_known = set(known)
    for k in known:
        closed_known |= G.ancestors(dag, k)
    need = set(targets)
    for t in targets:
        need |= G.ancestors(dag, t)
    need -= closed_known
    return G.topo_order(dag, need)


def show(g: G.Graph, vp: str, path: list[str]):
    total = 0
    print(f"\nViewpoint {vp}: {len(path)} topics")
    for i, n in enumerate(path, 1):
        node = g.nodes[n]
        m = node.get("minutes")
        total += m or 0
        tag = " [stub]" if node["status"] == "stub" else ""
        print(f"{i:3}. {n:42} {(str(m) + ' min') if m else '':>7}  {node['title']}{tag}")
    print(f"     total ≈ {total} min ≈ {total / 60:.1f} h (stubs not counted)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--viewpoint", default="classical")
    ap.add_argument("--known", default="", help="comma-separated node ids already mastered")
    ap.add_argument("--compare", nargs=2, metavar=("VP1", "VP2"))
    args = ap.parse_args()
    g = G.load()
    known = {k for k in args.known.split(",") if k}
    if args.compare:
        a, b = args.compare
        pa, pb = plan(g, a, args.targets, known), plan(g, b, args.targets, known)
        show(g, a, pa)
        show(g, b, pb)
        print(f"\nOnly in {a}: {', '.join(sorted(set(pa) - set(pb))) or '—'}")
        print(f"Only in {b}: {', '.join(sorted(set(pb) - set(pa))) or '—'}")
    else:
        show(g, args.viewpoint, plan(g, args.viewpoint, args.targets, known))


if __name__ == "__main__":
    main()
