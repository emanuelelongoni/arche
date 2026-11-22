#!/usr/bin/env python3
"""Render the graph under a viewpoint as Graphviz DOT (and SVG/PNG if `dot` is installed).

Arrows point from prerequisite to the topic that needs it (reading order).
Clusters are courses. Stubs are dashed. Edges that come from a choice group are coloured.

Usage:
  python3 tools/render.py --viewpoint npov --out build/npov        # writes .dot and .svg
  python3 tools/render.py --viewpoint classical --course ib-topological-spaces --out build/ts
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

import mmgraph as G


def dot(g: G.Graph, vp: str, course: str | None) -> str:
    act = g.active(vp)
    shown = {n for n in act if course is None or g.nodes[n]["course"] == course}
    # include direct prerequisites of shown nodes so cross-course edges are visible
    extra = set()
    for n in shown:
        for e in g.requires_under(vp, n):
            if e["node"] in act and e["node"] not in shown:
                extra.add(e["node"])
    nodes = shown | extra
    out = [
        "digraph G {",
        '  graph [rankdir=LR, fontname="Helvetica", fontsize=11, nodesep=0.15, ranksep=0.5];',
        '  node [shape=box, style="rounded,filled", fillcolor="#F5F4EE", fontname="Helvetica", fontsize=10, color="#999999"];',
        '  edge [color="#888888", arrowsize=0.6];',
    ]
    by_course: dict[str, list[str]] = {}
    for n in sorted(nodes):
        by_course.setdefault(g.nodes[n]["course"], []).append(n)
    for i, (cid, ns) in enumerate(sorted(by_course.items())):
        title = g.courses.get(cid, {}).get("title", cid)
        out.append(f'  subgraph cluster_{i} {{ label="{title}"; style="rounded"; color="#CCCCCC";')
        for n in ns:
            node = g.nodes[n]
            style = '"rounded,dashed"' if node["status"] == "stub" else '"rounded,filled"'
            fill = "#FFFFFF" if n in extra or node["status"] == "stub" else (
                "#E6F1FB" if node.get("only_in") else "#F5F4EE")
            label = node["title"].replace('"', "'")
            out.append(f'    "{n}" [label="{label}", style={style}, fillcolor="{fill}", tooltip="{n}"];')
        out.append("  }")
    for n in sorted(shown):
        for e in g.requires_under(vp, n):
            t = e["node"]
            if t not in nodes:
                continue
            attrs = ' [color="#D85A30", penwidth=1.4]' if e["via"] else ""
            out.append(f'  "{t}" -> "{n}"{attrs};')
    out.append("}")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--viewpoint", default="classical")
    ap.add_argument("--course")
    ap.add_argument("--out", default="build/graph")
    args = ap.parse_args()
    g = G.load()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".dot").write_text(dot(g, args.viewpoint, args.course), encoding="utf-8")
    print(f"wrote {out.with_suffix('.dot')}")
    if shutil.which("dot"):
        for fmt in ("svg", "png"):
            subprocess.run(["dot", f"-T{fmt}", "-Gdpi=110", str(out.with_suffix(".dot")),
                            "-o", str(out.with_suffix("." + fmt))], check=True)
            print(f"wrote {out.with_suffix('.' + fmt)}")


if __name__ == "__main__":
    main()
